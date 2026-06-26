#!/usr/bin/env python3
"""
环境变量配置脚本

功能：
- 向配置文件追加环境变量
- 自动备份原文件
- 支持多种配置文件格式
- 防止重复配置
"""

import argparse
import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path


def backup_file(file_path):
    """备份文件"""
    if not os.path.exists(file_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"✓ 已备份配置文件到: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"✗ 备份失败: {str(e)}")
        return None


def read_config_file(file_path):
    """读取配置文件"""
    if not os.path.exists(file_path):
        return ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"✗ 读取文件失败: {str(e)}")
        return ""


def write_config_file(file_path, content):
    """写入配置文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 配置已写入: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 写入文件失败: {str(e)}")
        return False


def check_env_exists(content, env_key):
    """检查环境变量是否已存在"""
    # 检查 export KEY= 或 KEY= 格式
    patterns = [
        f"export {env_key}=",
        f"{env_key}=",
    ]
    
    for pattern in patterns:
        if pattern in content:
            return True
    return False


def generate_env_export(env_vars, comment="Added by ubuntu-dev-setup"):
    """生成环境变量 export 语句"""
    lines = []
    
    if comment:
        lines.append(f"\n# {comment}")
    
    for key, value in env_vars.items():
        # 处理包含 $ 符号的值（保留变量引用）
        if '$' in str(value):
            lines.append(f'export {key}="{value}"')
        else:
            lines.append(f'export {key}={value}')
    
    return '\n'.join(lines)


def append_env_to_file(file_path, env_vars, backup=True):
    """向配置文件追加环境变量"""
    
    # 备份
    if backup:
        backup_file(file_path)
    
    # 读取现有内容
    content = read_config_file(file_path)
    
    # 过滤已存在的环境变量
    new_vars = {}
    for key, value in env_vars.items():
        if not check_env_exists(content, key):
            new_vars[key] = value
        else:
            print(f"⚠️  环境变量 {key} 已存在，跳过")
    
    if not new_vars:
        print("没有需要添加的环境变量")
        return True
    
    # 生成新的配置
    env_export = generate_env_export(new_vars)
    
    # 追加到文件
    new_content = content.rstrip() + '\n' + env_export + '\n'
    
    return write_config_file(file_path, new_content)


def generate_condarc_content(envs_dirs, pkgs_dirs=None):
    """生成 .condarc 配置内容"""
    config = {}
    
    if envs_dirs:
        config['envs_dirs'] = envs_dirs
    
    if pkgs_dirs:
        config['pkgs_dirs'] = pkgs_dirs
    
    # 添加其他常用配置
    config['channels'] = ['defaults']
    config['show_channel_urls'] = True
    
    import yaml
    return yaml.dump(config, default_flow_style=False)


def create_condarc(envs_dirs, pkgs_dirs=None, backup=True):
    """创建或更新 .condarc 文件"""
    condarc_path = os.path.expanduser("~/.condarc")
    
    # 备份
    if backup and os.path.exists(condarc_path):
        backup_file(condarc_path)
    
    try:
        import yaml
        config = {}
        
        if envs_dirs:
            config['envs_dirs'] = envs_dirs
        
        if pkgs_dirs:
            config['pkgs_dirs'] = pkgs_dirs
        
        config['channels'] = ['defaults']
        config['show_channel_urls'] = True
        
        with open(condarc_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"✓ 已创建/更新 .condarc: {condarc_path}")
        print(f"  环境目录: {envs_dirs}")
        return True
    
    except ImportError:
        print("⚠️  需要安装 PyYAML: pip install pyyaml")
        return False
    except Exception as e:
        print(f"✗ 创建 .condarc 失败: {str(e)}")
        return False


def setup_cuda_env(cuda_version="12.6", config_file=None):
    """配置 CUDA 环境变量"""
    if config_file is None:
        config_file = os.path.expanduser("~/.bashrc")
    
    cuda_path = f"/usr/local/cuda-{cuda_version}"
    
    env_vars = {
        "CUDA_PATH": cuda_path,
        "PATH": f"{cuda_path}/bin:$PATH",
        "LD_LIBRARY_PATH": f"{cuda_path}/lib64:$LD_LIBRARY_PATH",
        "CUDADIR": cuda_path
    }
    
    return append_env_to_file(config_file, env_vars)


def setup_cudnn_env(cuda_version="12.6", config_file=None):
    """配置 cuDNN 环境变量"""
    if config_file is None:
        config_file = os.path.expanduser("~/.bashrc")
    
    cuda_path = f"/usr/local/cuda-{cuda_version}"
    
    env_vars = {
        "CUDNN_INCLUDE_DIR": f"{cuda_path}/include",
        "CUDNN_LIB_DIR": f"{cuda_path}/lib64"
    }
    
    return append_env_to_file(config_file, env_vars)


def setup_conda_env(conda_path=None, config_file=None):
    """配置 conda 环境变量"""
    if conda_path is None:
        conda_path = os.path.expanduser("~/anaconda3")
    
    if config_file is None:
        config_file = os.path.expanduser("~/.bashrc")
    
    conda_bin = os.path.join(conda_path, "bin")
    
    # 检查 conda 是否已初始化
    content = read_config_file(config_file)
    if "conda initialize" in content:
        print("✓ conda 已初始化，跳过")
        return True
    
    env_vars = {
        "PATH": f"{conda_bin}:$PATH"
    }
    
    return append_env_to_file(config_file, env_vars, comment="Conda environment")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='环境变量配置工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加环境变量到 .bashrc
  python config_env.py --config-file ~/.bashrc --env-vars '{"MY_VAR": "/path/to/value"}'
  
  # 配置 CUDA 环境
  python config_env.py --setup-cuda --cuda-version 12.6
  
  # 配置 conda 环境
  python config_env.py --setup-conda --conda-path ~/anaconda3
  
  # 创建 .condarc
  python config_env.py --create-condarc --envs-dirs '["~/workspace/anaconda3/envs"]'
        """
    )
    
    parser.add_argument(
        '--config-file',
        help='配置文件路径 (如 ~/.bashrc, ~/.zshrc)'
    )
    
    parser.add_argument(
        '--env-vars',
        help='环境变量 JSON 格式 (如 \'{"KEY": "value"}\')'
    )
    
    parser.add_argument(
        '--backup',
        action='store_true',
        default=True,
        help='修改前备份原文件 (默认: True)'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='不备份原文件'
    )
    
    # CUDA 配置
    parser.add_argument(
        '--setup-cuda',
        action='store_true',
        help='配置 CUDA 环境变量'
    )
    
    parser.add_argument(
        '--cuda-version',
        default='12.6',
        help='CUDA 版本 (默认: 12.6)'
    )
    
    # cuDNN 配置
    parser.add_argument(
        '--setup-cudnn',
        action='store_true',
        help='配置 cuDNN 环境变量'
    )
    
    # Conda 配置
    parser.add_argument(
        '--setup-conda',
        action='store_true',
        help='配置 conda 环境变量'
    )
    
    parser.add_argument(
        '--conda-path',
        default='~/anaconda3',
        help='conda 安装路径 (默认: ~/anaconda3)'
    )
    
    # .condarc 配置
    parser.add_argument(
        '--create-condarc',
        action='store_true',
        help='创建或更新 .condarc 文件'
    )
    
    parser.add_argument(
        '--envs-dirs',
        help='conda 环境目录列表 (JSON 格式)'
    )
    
    parser.add_argument(
        '--pkgs-dirs',
        help='conda 包缓存目录列表 (JSON 格式)'
    )
    
    args = parser.parse_args()
    
    backup = not args.no_backup
    success = True
    
    # 通用环境变量配置
    if args.config_file and args.env_vars:
        config_file = os.path.expanduser(args.config_file)
        
        try:
            env_vars = json.loads(args.env_vars)
        except json.JSONDecodeError as e:
            print(f"✗ JSON 格式错误: {str(e)}")
            return 1
        
        if not append_env_to_file(config_file, env_vars, backup):
            success = False
    
    # CUDA 配置
    if args.setup_cuda:
        if not setup_cuda_env(args.cuda_version, os.path.expanduser("~/.bashrc")):
            success = False
    
    # cuDNN 配置
    if args.setup_cudnn:
        if not setup_cudnn_env(args.cuda_version, os.path.expanduser("~/.bashrc")):
            success = False
    
    # Conda 配置
    if args.setup_conda:
        conda_path = os.path.expanduser(args.conda_path)
        if not setup_conda_env(conda_path):
            success = False
    
    # .condarc 配置
    if args.create_condarc:
        try:
            envs_dirs = json.loads(args.envs_dirs) if args.envs_dirs else None
            pkgs_dirs = json.loads(args.pkgs_dirs) if args.pkgs_dirs else None
            
            if envs_dirs:
                envs_dirs = [os.path.expanduser(d) for d in envs_dirs]
            if pkgs_dirs:
                pkgs_dirs = [os.path.expanduser(d) for d in pkgs_dirs]
            
            if not create_condarc(envs_dirs, pkgs_dirs, backup):
                success = False
        
        except json.JSONDecodeError as e:
            print(f"✗ JSON 格式错误: {str(e)}")
            success = False
    
    if success:
        print("\n✓ 配置完成")
        print("⚠️  请执行 'source ~/.bashrc' 或重新打开终端使配置生效")
        return 0
    else:
        print("\n✗ 配置过程中出现错误")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
