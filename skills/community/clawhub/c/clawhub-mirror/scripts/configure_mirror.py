#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClawHub镜像源配置工具
优先使用国内镜像，国内没有则使用国外源
需要VPN时会明确提示
"""

import os
import sys
import json
import time
import socket
import urllib.request
from urllib.error import URLError, HTTPError

# 镜像源定义
MIRRORS = [
    {
        "name": "国内镜像1",
        "site": "https://mirror.clawhub.cn",
        "registry": "https://api.mirror.clawhub.cn",
        "type": "china",
        "priority": 1
    },
    {
        "name": "国内镜像2", 
        "site": "https://clawhub.gitee.io",
        "registry": "https://api.clawhub.gitee.io",
        "type": "china",
        "priority": 2
    },
    {
        "name": "官方源",
        "site": "https://clawhub.ai",
        "registry": "https://api.clawhub.ai",
        "type": "official",
        "priority": 3
    },
    {
        "name": "备用源",
        "site": "https://clawhub.net",
        "registry": "https://api.clawhub.net",
        "type": "backup",
        "priority": 4
    }
]

def test_connection(url, timeout=3):
    """测试URL是否可访问"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(req, timeout=timeout)
        response.close()
        return True
    except (URLError, HTTPError, socket.timeout):
        return False

def get_latency(hostname, timeout=2):
    """获取网络延迟（简单实现）"""
    try:
        start = time.time()
        socket.gethostbyname(hostname)
        return int((time.time() - start) * 1000)  # 毫秒
    except socket.gaierror:
        return None

def select_best_mirror():
    """选择最佳镜像源"""
    print("🔍 扫描可用镜像源...")
    
    available_mirrors = []
    
    for mirror in MIRRORS:
        print(f"测试 {mirror['name']} ({mirror['site']})...", end="")
        
        if test_connection(mirror['site']):
            # 获取延迟
            try:
                hostname = urllib.request.urlparse(mirror['site']).hostname
                latency = get_latency(hostname)
                if latency:
                    print(f" ✅ 可用 (延迟: {latency}ms)")
                    mirror['latency'] = latency
                else:
                    print(" ✅ 可用")
                    mirror['latency'] = 999
            except:
                print(" ✅ 可用")
                mirror['latency'] = 999
            
            mirror['available'] = True
            available_mirrors.append(mirror)
        else:
            print(" ❌ 不可用")
            mirror['available'] = False
    
    if not available_mirrors:
        print("\n⚠️  所有镜像源都不可用！")
        return None
    
    # 优先选择国内镜像
    china_mirrors = [m for m in available_mirrors if m['type'] == 'china']
    if china_mirrors:
        # 按延迟排序
        china_mirrors.sort(key=lambda x: x.get('latency', 999))
        selected = china_mirrors[0]
    else:
        # 没有国内镜像，选择延迟最低的
        available_mirrors.sort(key=lambda x: x.get('latency', 999))
        selected = available_mirrors[0]
    
    return selected

def save_config(selected_mirror, all_mirrors):
    """保存配置到文件"""
    config_dir = os.path.expanduser("~/.clawhub")
    os.makedirs(config_dir, exist_ok=True)
    
    config = {
        "selected": {
            "name": selected_mirror["name"],
            "site": selected_mirror["site"],
            "registry": selected_mirror["registry"],
            "type": selected_mirror["type"],
            "selected_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "available_mirrors": [
            {
                "name": m["name"],
                "site": m["site"],
                "registry": m["registry"],
                "type": m["type"],
                "latency": m.get("latency"),
                "available": m.get("available", False)
            }
            for m in all_mirrors
        ]
    }
    
    config_file = os.path.join(config_dir, "mirror-config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置文件已保存: {config_file}")
    return config_file

def create_load_script(config_file):
    """创建快速加载脚本"""
    # 使用转义处理路径
    config_file_escaped = config_file.replace('\\', '\\\\').replace('"', '\\"')
    
    script_content = f'''#!/bin/bash
# ClawHub镜像源快速加载脚本
# 自动加载最佳镜像配置

CONFIG_FILE="{config_file_escaped}"

if [ -f "$CONFIG_FILE" ]; then
    SITE=$(python -c "import json; data=json.load(open(r'$CONFIG_FILE')); print(data['selected']['site'])")
    REGISTRY=$(python -c "import json; data=json.load(open(r'$CONFIG_FILE')); print(data['selected']['registry'])")
    
    export CLAWHUB_SITE="$SITE"
    export CLAWHUB_REGISTRY="$REGISTRY"
    
    echo "✅ ClawHub镜像源已加载: $(python -c "import json; data=json.load(open(r'$CONFIG_FILE')); print(data['selected']['name'])")"
else
    echo "⚠️  未找到ClawHub镜像配置，使用默认源"
fi
'''
    
    script_file = os.path.join(os.path.expanduser("~/.clawhub"), "load-mirror.sh")
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_file, 0o755)
    print(f"✅ 快速加载脚本已创建: {script_file}")
    
    # 创建Windows批处理文件
    # 使用简单的批处理语法避免复杂转义
    batch_content = '''@echo off
REM ClawHub镜像源快速加载脚本（Windows）
REM 配置文件路径在脚本生成时已硬编码

set CONFIG_FILE=%USERPROFILE%\\.clawhub\\mirror-config.json

if exist "%CONFIG_FILE%" (
    python -c "import json, sys; data=json.load(open(r'%CONFIG_FILE%', encoding='utf-8')); sys.stdout.write(data['selected']['site'])" > temp_site.txt
    set /p CLAWHUB_SITE=<temp_site.txt
    del temp_site.txt
    
    python -c "import json, sys; data=json.load(open(r'%CONFIG_FILE%', encoding='utf-8')); sys.stdout.write(data['selected']['registry'])" > temp_reg.txt
    set /p CLAWHUB_REGISTRY=<temp_reg.txt
    del temp_reg.txt
    
    echo ✅ ClawHub镜像源已加载
) else (
    echo ⚠️  未找到ClawHub镜像配置，使用默认源
)
'''
    
    batch_file = os.path.join(os.path.expanduser("~/.clawhub"), "load-mirror.bat")
    with open(batch_file, 'w', encoding='gbk') as f:
        f.write(batch_content)
    
    print(f"✅ Windows批处理文件已创建: {batch_file}")

def main():
    print("🔧 ClawHub智能镜像配置工具")
    print("=" * 50)
    
    # 选择最佳镜像
    selected = select_best_mirror()
    
    if not selected:
        print("\n❌ 配置失败！")
        print("\n可能的原因：")
        print("1. 网络连接问题")
        print("2. 需要VPN访问国外源")
        print("3. 镜像源暂时不可用")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 连接VPN后重试")
        print("3. 手动设置环境变量：")
        print("   set CLAWHUB_SITE=https://clawhub.ai")
        print("   set CLAWHUB_REGISTRY=https://api.clawhub.ai")
        return 1
    
    print(f"\n✅ 选择最佳镜像源：")
    print(f"   名称: {selected['name']}")
    print(f"   类型: {selected['type']}")
    print(f"   Site: {selected['site']}")
    print(f"   Registry: {selected['registry']}")
    if 'latency' in selected:
        print(f"   延迟: {selected['latency']}ms")
    
    # 设置环境变量
    os.environ['CLAWHUB_SITE'] = selected['site']
    os.environ['CLAWHUB_REGISTRY'] = selected['registry']
    
    print(f"\n⚙️  环境变量已设置：")
    print(f"   CLAWHUB_SITE={os.environ['CLAWHUB_SITE']}")
    print(f"   CLAWHUB_REGISTRY={os.environ['CLAWHUB_REGISTRY']}")
    
    # 保存配置
    config_file = save_config(selected, MIRRORS)
    
    # 创建加载脚本
    create_load_script(config_file)
    
    # VPN提示
    if selected['type'] != 'china':
        print("\n⚠️  VPN提示：")
        print("当前使用的是国外镜像源，可能需要VPN才能稳定访问")
        print("如果您有VPN，建议连接后使用以获得更好体验")
    
    print("\n📝 使用说明：")
    print("1. 当前会话已配置镜像源")
    print("2. 在新会话中快速加载：")
    print("   Windows: 运行 %USERPROFILE%\\.clawhub\\load-mirror.bat")
    print("   Linux/Mac: source ~/.clawhub/load-mirror.sh")
    print("3. 或手动设置环境变量")
    
    print("\n🚀 配置完成！现在可以使用clawhub命令了")
    
    # 测试命令
    print("\n🧪 测试命令...")
    try:
        import subprocess
        result = subprocess.run(['clawhub', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 测试成功！")
        else:
            print("⚠️  测试命令有误，但配置已保存")
            print(f"错误信息: {result.stderr}")
    except FileNotFoundError:
        print("⚠️  clawhub命令未找到，请确保已安装")
    except Exception as e:
        print(f"⚠️  测试时出错: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())