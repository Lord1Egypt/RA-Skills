#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查和安装脚本
"""

import subprocess
import sys
import os

# 需要检查的依赖
DEPENDENCIES = {
    'python': {
        'check': lambda: sys.version_info >= (3, 8),
        'install': None,
        'name': 'Python 3.8+'
    },
    'requests': {
        'check': lambda: __import__('requests', fromlist=['']) is not None,
        'install': 'pip install requests',
        'name': 'requests'
    },
    'beautifulsoup4': {
        'check': lambda: __import__('bs4', fromlist=['']) is not None,
        'install': 'pip install beautifulsoup4',
        'name': 'beautifulsoup4'
    },
    'websocket-client': {
        'check': lambda: __import__('websocket', fromlist=['']) is not None,
        'install': 'pip install websocket-client',
        'name': 'websocket-client'
    }
}


def check_chrome():
    """检查 Chrome 是否可用"""
    import requests
    
    try:
        resp = requests.get('http://localhost:9222/json/list', timeout=3)
        pages = resp.json()
        for p in pages:
            if p['type'] == 'page':
                return True, "Chrome 已在运行"
    except:
        pass
    
    # 检查 Chrome 是否安装
    if sys.platform == 'win32':
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        for path in paths:
            if os.path.exists(path):
                return True, f"Chrome 已安装，可通过 CDP 连接"
        return False, "Chrome 未安装"
    else:
        # macOS/Linux
        result = subprocess.run(['which', 'google-chrome'], capture_output=True)
        if result.returncode == 0:
            return True, "Chrome 已安装"
        return False, "Chrome 未安装"


def check_dependencies():
    """检查所有依赖"""
    missing = []
    
    print("=" * 50)
    print("依赖检查")
    print("=" * 50)
    
    # 检查 Python
    if sys.version_info < (3, 8):
        print(f"[FAIL] Python 版本过低: {sys.version_info.major}.{sys.version_info.minor}")
        print(f"   需要 Python 3.8+")
        missing.append('python')
    else:
        print(f"[OK] Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # 检查 pip 包
    for name, info in DEPENDENCIES.items():
        if name == 'python':
            continue
        try:
            if info['check']():
                print(f"[OK] {info['name']}: 已安装")
            else:
                print(f"[FAIL] {info['name']}: 未安装")
                missing.append(name)
        except Exception as e:
            print(f"[FAIL] {info['name']}: 检查失败 - {str(e)[:30]}")
            missing.append(name)
    
    # 检查 Chrome
    chrome_ok, chrome_msg = check_chrome()
    if chrome_ok:
        print(f"[OK] Chrome: {chrome_msg}")
    else:
        print(f"[WARN]  Chrome: {chrome_msg}")
    
    print("=" * 50)
    
    return missing


def install_dependencies(deps):
    """安装缺失的依赖"""
    print(f"\n正在安装依赖: {', '.join(deps)}")
    print("-" * 50)
    
    for dep in deps:
        info = DEPENDENCIES.get(dep)
        if info and info.get('install'):
            print(f"安装 {info['name']}...")
            try:
                result = subprocess.run(
                    info['install'].split(),
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"  [OK] {info['name']} 安装成功")
                else:
                    print(f"  [FAIL] {info['name']} 安装失败: {result.stderr[:100]}")
            except Exception as e:
                print(f"  [FAIL] 安装失败: {str(e)[:50]}")


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("AI 资讯简报 - 依赖检查工具")
    print("=" * 50 + "\n")
    
    # 检查依赖
    missing = check_dependencies()
    
    if not missing:
        print("\n[OK] 所有依赖已满足，可以使用 Skill！")
        print("运行命令: python scripts/fetch_ai_news.py")
    else:
        print(f"\n[WARN]  缺少 {len(missing)} 个依赖")
        print("\n请选择安装方式：")
        print("  1. 自动安装（推荐）")
        print("  2. 手动安装")
        print("\n请回复数字或选项：")
        
        # 这里只是提示，实际安装由 AI 引导用户完成
        choice = input("> ").strip()
        
        if choice in ['1', 'auto', '自动', '是', '安装']:
            install_dependencies(missing)
            
            # 再次检查
            missing = check_dependencies()
            if not missing:
                print("\n[OK] 所有依赖已安装完成！")
        else:
            print("\n请手动运行以下命令安装依赖：")
            for dep in missing:
                info = DEPENDENCIES.get(dep)
                if info and info.get('install'):
                    print(f"  {info['install']}")


if __name__ == "__main__":
    main()