#!/usr/bin/env python3
"""
DolphinDB Python 环境初始化模块

功能：
1. 自动检测系统中已安装的 DolphinDB Python SDK
2. 如果找到，返回 Python 路径
3. 如果未找到，提供安装指导

使用方法：
    from init_dolphindb_env import get_dolphindb_python
    python_path = get_dolphindb_python()
    
    # 或者直接运行脚本
    python3 init_dolphindb_env.py
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, shell=True):
    """运行 shell 命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout"
    except Exception as e:
        return False, "", str(e)


def check_python_has_dolphindb(python_path):
    """检查指定的 Python 是否安装了 dolphindb SDK"""
    success, stdout, stderr = run_command(
        f'{python_path} -c "import dolphindb; print(dolphindb.__version__)"'
    )
    if success:
        return True, stdout
    return False, None


def find_conda_environments():
    """查找所有 conda 环境"""
    envs = []
    
    # 尝试 conda env list
    success, stdout, stderr = run_command('conda env list 2>/dev/null')
    if success:
        for line in stdout.split('\n'):
            if line.strip() and not line.startswith('#') and '*' not in line:
                parts = line.split()
                if parts:
                    envs.append(parts[0])
    
    # 常见 conda 路径
    conda_paths = [
        Path.home() / 'anaconda3',
        Path.home() / 'miniconda3',
        Path.home() / 'anaconda',
        Path.home() / 'miniconda',
        Path('/opt/anaconda3'),
        Path('/opt/miniconda3'),
    ]
    
    for conda_base in conda_paths:
        if conda_base.exists():
            envs.append(str(conda_base))
            # 检查 envs 目录
            envs_dir = conda_base / 'envs'
            if envs_dir.exists():
                for env in envs_dir.iterdir():
                    if env.is_dir():
                        envs.append(str(env))
    
    return list(set(envs))


def find_system_python():
    """查找系统 Python"""
    python_paths = [
        '/usr/bin/python3',
        '/usr/local/bin/python3',
        str(Path.home() / '.pyenv/shims/python3'),
        '/opt/homebrew/bin/python3',
    ]
    
    found = []
    for path in python_paths:
        if Path(path).exists():
            found.append(path)
    
    return found


def search_dolphindb_environment():
    """
    搜索已安装 DolphinDB SDK 的 Python 环境
    
    返回：
        (found: bool, python_path: str, version: str)
    """
    print("🔍 正在搜索 DolphinDB Python SDK 环境...")
    
    # 1. 优先检查环境变量
    env_python = os.environ.get('DOLPHINDB_PYTHON_BIN')
    if env_python:
        found, version = check_python_has_dolphindb(env_python)
        if found:
            print(f"✅ 从环境变量找到：{env_python} (SDK {version})")
            return True, env_python, version
    
    # 2. 检查 conda 环境
    print("   检查 conda 环境...")
    conda_envs = find_conda_environments()
    for env_path in conda_envs:
        python_bin = Path(env_path) / 'bin' / 'python'
        if not python_bin.exists():
            python_bin = Path(env_path) / 'python.exe'  # Windows
        
        if python_bin.exists():
            found, version = check_python_has_dolphindb(str(python_bin))
            if found:
                print(f"✅ 在 conda 环境找到：{python_bin} (SDK {version})")
                return True, str(python_bin), version
    
    # 3. 检查系统 Python
    print("   检查系统 Python...")
    system_pythons = find_system_python()
    for python_path in system_pythons:
        found, version = check_python_has_dolphindb(python_path)
        if found:
            print(f"✅ 在系统 Python 找到：{python_path} (SDK {version})")
            return True, python_path, version
    
    # 4. 检查当前 Python
    print("   检查当前 Python...")
    found, version = check_python_has_dolphindb(sys.executable)
    if found:
        print(f"✅ 在当前 Python 找到：{sys.executable} (SDK {version})")
        return True, sys.executable, version
    
    print("❌ 未找到已安装 DolphinDB SDK 的 Python 环境")
    return False, None, None


def install_dolphindb_sdk(python_path):
    """在指定的 Python 环境中安装 DolphinDB SDK"""
    print(f"📦 正在 {python_path} 中安装 DolphinDB SDK...")
    
    success, stdout, stderr = run_command(
        f'{python_path} -m pip install dolphindb -q'
    )
    
    if success:
        found, version = check_python_has_dolphindb(python_path)
        if found:
            print(f"✅ 安装成功！SDK 版本：{version}")
            return True, version
        else:
            print("❌ 安装完成但无法验证")
            return False, None
    else:
        print(f"❌ 安装失败：{stderr}")
        return False, None


def get_dolphindb_python(auto_install=True):
    """
    获取可用的 DolphinDB Python 环境
    
    参数：
        auto_install: 如果未找到，是否自动安装
    
    返回：
        python_path: Python 可执行文件路径
        version: SDK 版本
    """
    found, python_path, version = search_dolphindb_environment()
    
    if found:
        return python_path, version
    
    if not auto_install:
        print("\n❌ 未找到 DolphinDB SDK，且未启用自动安装")
        return None, None
    
    # 尝试安装
    print("\n💡 尝试在当前 Python 环境中安装...")
    success, version = install_dolphindb_sdk(sys.executable)
    
    if success:
        return sys.executable, version
    
    # 尝试在 conda base 环境安装
    conda_base = Path.home() / 'anaconda3'
    if conda_base.exists():
        conda_python = conda_base / 'bin' / 'python'
        if conda_python.exists():
            print(f"\n💡 尝试在 conda base 环境安装：{conda_python}")
            success, version = install_dolphindb_sdk(str(conda_python))
            if success:
                return str(conda_python), version
    
    print("\n❌ 无法自动安装 DolphinDB SDK")
    print("\n请手动安装:")
    print(f"  {sys.executable} -m pip install dolphindb")
    print(f"或 {conda_base}/bin/python -m pip install dolphindb")
    
    return None, None


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DolphinDB Python 环境初始化工具')
    parser.add_argument('--no-install', action='store_true', help='不自动安装')
    parser.add_argument('--export', action='store_true', help='导出环境变量')
    
    args = parser.parse_args()
    
    python_path, version = get_dolphindb_python(auto_install=not args.no_install)
    
    if python_path:
        print(f"\n✅ 找到 DolphinDB Python 环境:")
        print(f"   Python: {python_path}")
        print(f"   SDK: {version}")
        
        if args.export:
            print(f"\n# 在 shell 中运行以下命令:")
            print(f"export DOLPHINDB_PYTHON_BIN={python_path}")
            print(f"export DOLPHINDB_SDK_VERSION={version}")
        
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
