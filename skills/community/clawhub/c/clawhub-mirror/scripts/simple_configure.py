#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的ClawHub镜像配置工具
优先国内镜像，需要时使用VPN
"""

import os
import sys
import json
import urllib.request
from urllib.error import URLError

def test_url(url, timeout=3):
    """测试URL是否可访问"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        urllib.request.urlopen(req, timeout=timeout).close()
        return True
    except:
        return False

def main():
    print("ClawHub镜像配置工具")
    print("=" * 40)
    
    # 镜像源列表（按优先级排序）
    mirrors = [
        {"name": "国内镜像", "site": "https://mirror.clawhub.cn", "registry": "https://api.mirror.clawhub.cn", "type": "china"},
        {"name": "官方源", "site": "https://clawhub.ai", "registry": "https://api.clawhub.ai", "type": "official"}
    ]
    
    print("\n测试镜像源可用性...")
    
    selected = None
    for mirror in mirrors:
        print(f"测试 {mirror['name']}...", end="")
        if test_url(mirror['site']):
            print(" [可用]")
            if mirror['type'] == 'china' and selected is None:
                selected = mirror
        else:
            print(" [不可用]")
    
    # 如果没有选择国内镜像，选择第一个可用的
    if selected is None:
        for mirror in mirrors:
            if test_url(mirror['site']):
                selected = mirror
                break
    
    if selected is None:
        print("\n错误：所有镜像都不可用！")
        print("\n可能的原因：")
        print("1. 网络连接问题")
        print("2. 需要VPN访问国外源")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 连接VPN后重试")
        print("3. 手动设置环境变量：")
        print("   set CLAWHUB_SITE=https://clawhub.ai")
        print("   set CLAWHUB_REGISTRY=https://api.clawhub.ai")
        return 1
    
    print(f"\n选择镜像源：{selected['name']}")
    print(f"   Site: {selected['site']}")
    print(f"   Registry: {selected['registry']}")
    
    # 设置环境变量
    os.environ['CLAWHUB_SITE'] = selected['site']
    os.environ['CLAWHUB_REGISTRY'] = selected['registry']
    
    print(f"\n环境变量已设置：")
    print(f"   CLAWHUB_SITE={os.environ['CLAWHUB_SITE']}")
    print(f"   CLAWHUB_REGISTRY={os.environ['CLAWHUB_REGISTRY']}")
    
    # 保存配置
    config_dir = os.path.expanduser("~/.clawhub")
    os.makedirs(config_dir, exist_ok=True)
    
    config = {
        "mirror": {
            "name": selected['name'],
            "site": selected['site'],
            "registry": selected['registry'],
            "type": selected['type']
        }
    }
    
    config_file = os.path.join(config_dir, "config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n配置文件已保存：{config_file}")
    
    # VPN提示
    if selected['type'] != 'china':
        print("\nVPN提示：")
        print("当前使用的是国外镜像源，可能需要VPN才能稳定访问")
        print("如果您有VPN，建议连接后使用")
    
    print("\n使用说明：")
    print("1. 当前会话已配置镜像源")
    print("2. 如需永久配置，请将环境变量添加到系统设置")
    print("3. 需要VPN时，请先连接VPN")
    
    print("\n配置完成！")
    
    # 测试clawhub命令
    print("\n测试clawhub命令...")
    try:
        import subprocess
        result = subprocess.run(['clawhub', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("测试成功！")
        else:
            print("测试有警告")
    except FileNotFoundError:
        print("clawhub命令未找到")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())