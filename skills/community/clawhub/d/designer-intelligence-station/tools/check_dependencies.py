#!/usr/bin/env python3
"""
依赖检查工具 - 检测并自动安装缺失的 Python 依赖
"""

import subprocess
import sys
import os

def get_script_dir():
    """获取脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))

def get_root_dir():
    """获取技能根目录"""
    return os.path.dirname(get_script_dir())

def check_python_version():
    """检查 Python 版本"""
    try:
        result = subprocess.run(
            [sys.executable, '--version'],
            capture_output=True,
            text=True
        )
        version = result.stdout.strip()
        print(f"✓ Python 版本：{version}")
        
        # 解析版本号
        version_str = version.split()[1]
        major, minor = map(int, version_str.split('.')[:2])
        
        if major < 3 or (major == 3 and minor < 10):
            print(f"⚠ 警告：Python 3.10+ 推荐，当前版本 {version_str}")
            return False
        return True
    except Exception as e:
        print(f"✗ 无法检查 Python 版本：{e}")
        return False

def check_package(package_name):
    """检查单个包是否已安装"""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def get_required_packages():
    """从 requirements.txt 读取所需的包"""
    root_dir = get_root_dir()
    requirements_path = os.path.join(root_dir, 'requirements.txt')
    
    packages = []
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 提取包名（去掉版本约束）
                    package_name = line.split('>=')[0].split('==')[0].split('<=')[0].strip()
                    packages.append(package_name)
    return packages

def check_all_dependencies():
    """检查所有依赖"""
    print("\n=== 依赖检查 ===\n")
    
    # 检查 Python 版本
    python_ok = check_python_version()
    if not python_ok:
        print("\n⚠ Python 版本不符合要求\n")
    
    # 检查所需的包
    required_packages = get_required_packages()
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        if check_package(package):
            installed_packages.append(package)
            print(f"✓ {package}")
        else:
            missing_packages.append(package)
            print(f"✗ {package} (缺失)")
    
    print(f"\n已安装：{len(installed_packages)}/{len(required_packages)}")
    
    if missing_packages:
        print(f"缺失：{len(missing_packages)}")
        print(f"缺失列表：{', '.join(missing_packages)}")
        return False, missing_packages
    else:
        print("\n✓ 所有依赖已安装")
        return True, []

def install_packages(packages):
    """安装缺失的包"""
    print(f"\n=== 安装缺失的依赖 ===\n")
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 
             os.path.join(get_root_dir(), 'requirements.txt')],
            check=True
        )
        print("\n✓ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 依赖安装失败：{e}")
        return False

def main():
    """主函数"""
    # 切换到技能根目录
    root_dir = get_root_dir()
    os.chdir(root_dir)
    
    # 检查依赖
    all_installed, missing_packages = check_all_dependencies()
    
    if not all_installed:
        # 询问是否自动安装
        print("\n是否自动安装缺失的依赖？[Y/n]")
        try:
            response = input().strip().lower()
        except EOFError:
            # 非交互模式，自动安装
            response = 'y'
        
        if response in ['', 'y', 'yes']:
            success = install_packages(missing_packages)
            if success:
                # 重新检查
                all_installed, _ = check_all_dependencies()
                return 0 if all_installed else 1
            else:
                return 1
        else:
            print("\n⚠ 请手动安装依赖后重试")
            print(f"运行：pip install -r requirements.txt")
            return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
