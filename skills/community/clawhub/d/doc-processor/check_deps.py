#!/usr/bin/env python3
"""依赖检测脚本 - 文档处理 Skill"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_system_cmd(cmd):
    """检查系统命令"""
    try:
        result = subprocess.run(
            [cmd, '--version' if cmd != 'pdfinfo' else '-v'],
            capture_output=True,
            timeout=5
        )
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

def check_python_module(module):
    """检查 Python 模块"""
    return importlib.util.find_spec(module) is not None

def get_install_commands():
    """返回安装命令"""
    return {
        'linux_apt': 'sudo apt install poppler-utils',
        'linux_yum': 'sudo yum install poppler-utils',
        'macos_brew': 'brew install poppler',
        'pip': 'pip install python-docx openpyxl pandas'
    }

def main():
    """生成依赖报告"""
    deps = {
        'system': {
            'pdftotext': check_system_cmd('pdftotext'),
            'pdfinfo': check_system_cmd('pdfinfo'),
        },
        'python': {
            'python-docx': check_python_module('docx'),
            'openpyxl': check_python_module('openpyxl'),
            'pandas': check_python_module('pandas'),
        }
    }
    
    # 计算能力
    capabilities = {
        'pdf_read': all(deps['system'].values()),
        'word_full': deps['python']['python-docx'],
        'excel_full': deps['python']['openpyxl'] and deps['python']['pandas']
    }
    
    # 生成报告
    report = {
        'dependencies': deps,
        'capabilities': capabilities,
        'install_commands': get_install_commands(),
        'all_ok': all(capabilities.values())
    }
    
    # 输出 JSON
    import json
    print(json.dumps(report, indent=2))
    
    # 视觉化输出到 stderr
    print("\n📊 依赖状态:", file=sys.stderr)
    for category, items in deps.items():
        print(f"\n  {category.upper()}:", file=sys.stderr)
        for name, ok in items.items():
            status = '✅' if ok else '❌'
            print(f"    {status} {name}", file=sys.stderr)
    
    print("\n📦 能力状态:", file=sys.stderr)
    for name, ok in capabilities.items():
        status = '✅' if ok else '❌'
        print(f"  {status} {name}", file=sys.stderr)
    
    if not report['all_ok']:
        print("\n⚠️  部分功能不可用，运行 setup.sh 安装缺失依赖", file=sys.stderr)
    
    return 0 if report['all_ok'] else 1

if __name__ == "__main__":
    sys.exit(main())
