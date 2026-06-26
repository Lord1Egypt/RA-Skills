#!/usr/bin/env python3
"""
依赖自动安装脚本
在skill首次使用时自动检查并安装缺失的依赖
"""

import subprocess
import sys
import importlib.util
from pathlib import Path

# 需要的依赖库及其最低版本（仅 yfinance，无 akshare）
REQUIRED_PACKAGES = {
    'yfinance': '0.2.36',
    'pandas': '2.0.0',
    'numpy': '1.24.0',
    'matplotlib': '3.7.0',
    'plotly': '5.18.0',
    'scipy': '1.11.0',
    'statsmodels': '0.14.0',
    'requests': '2.31.0',
    'openpyxl': '3.1.0',
    'Jinja2': '3.1.0',
}

def check_package(package_name):
    """检查包是否已安装"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name, version):
    """安装指定版本的包"""
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--quiet', f'{package_name}>={version}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """主函数：检查并安装缺失的依赖"""
    missing_packages = []
    
    print("🔍 检查 financial-data-analyzer 依赖...")
    
    for package, version in REQUIRED_PACKAGES.items():
        # 某些包的导入名和pip名不同
        import_name = {
            'Jinja2': 'jinja2'
        }.get(package, package)
        
        if not check_package(import_name):
            missing_packages.append((package, version))
    
    if not missing_packages:
        print("✅ 所有依赖已安装")
        return True
    
    print(f"⚠️  发现 {len(missing_packages)} 个缺失的依赖")
    print("📦 正在自动安装...")
    
    failed = []
    for package, version in missing_packages:
        print(f"   安装 {package}>={version}...", end=' ')
        if install_package(package, version):
            print("✅")
        else:
            print("❌")
            failed.append(package)
    
    if failed:
        print(f"\n❌ 以下依赖安装失败: {', '.join(failed)}")
        print(f"请手动运行: pip install {' '.join(failed)}")
        return False
    
    print("\n✅ 所有依赖安装完成！")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
