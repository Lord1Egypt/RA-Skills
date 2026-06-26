#!/usr/bin/env python3
"""
Ubuntu 系统信息检测脚本

功能：
- 检测 Ubuntu 版本和内核
- 检测已安装的开发工具
- 检测 GPU 信息
- 检测可用磁盘空间
- 检测 conda 环境
"""

import subprocess
import json
import os
import sys
from pathlib import Path


def run_command(cmd, shell=False):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", -1
    except Exception as e:
        return str(e), -1


def get_ubuntu_version():
    """获取 Ubuntu 版本信息"""
    output, code = run_command(["lsb_release", "-a"])
    if code == 0:
        lines = output.split('\n')
        version_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                version_info[key.strip()] = value.strip()
        return version_info
    return {"error": "无法获取 Ubuntu 版本信息"}


def get_kernel_version():
    """获取内核版本"""
    output, code = run_command(["uname", "-r"])
    return output if code == 0 else "unknown"


def get_disk_space():
    """获取磁盘空间信息"""
    output, code = run_command(["df", "-h", "/"])
    if code == 0:
        lines = output.split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 4:
                return {
                    "total": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4]
                }
    return {"error": "无法获取磁盘空间信息"}


def get_gpu_info():
    """获取 GPU 信息"""
    gpu_info = {"available": False}
    
    # 检查是否有 NVIDIA GPU
    output, code = run_command(["lspci"])
    if code == 0 and "NVIDIA" in output:
        gpu_info["available"] = True
        gpu_info["type"] = "NVIDIA"
        
        # 尝试获取详细信息
        nvidia_output, nvidia_code = run_command(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"])
        if nvidia_code == 0:
            lines = nvidia_output.split('\n')
            if lines and lines[0]:
                parts = lines[0].split(',')
                if len(parts) >= 3:
                    gpu_info["name"] = parts[0].strip()
                    gpu_info["driver_version"] = parts[1].strip()
                    gpu_info["memory"] = parts[2].strip()
        else:
            gpu_info["driver_installed"] = False
    
    return gpu_info


def check_installed_tools():
    """检查已安装的开发工具"""
    tools = {
        "browser": {
            "google-chrome": "google-chrome --version",
            "microsoft-edge": "microsoft-edge --version",
            "firefox": "firefox --version"
        },
        "editor": {
            "code": "code --version",
            "cursor": "cursor --version"
        },
        "communication": {
            "feishu": "dpkg -l | grep feishu",
            "todesk": "todesk --version",
            "tencent-meeting": "dpkg -l | grep tencent-meeting"
        },
        "input": {
            "sogou-pinyin": "dpkg -l | grep sogou"
        },
        "office": {
            "wps-office": "wps --version"
        },
        "terminal": {
            "terminator": "terminator --version",
            "zsh": "zsh --version"
        },
        "development": {
            "conda": "conda --version",
            "git": "git --version",
            "cmake": "cmake --version",
            "cuda": "nvcc --version",
            "ros": "rosversion -d"
        },
        "tools": {
            "gparted": "gparted --version",
            "kazam": "kazam --version"
        }
    }
    
    installed = {}
    
    for category, apps in tools.items():
        installed[category] = {}
        for app, check_cmd in apps.items():
            output, code = run_command(check_cmd, shell=True)
            if code == 0 and output:
                installed[category][app] = {
                    "installed": True,
                    "version": output.split('\n')[0][:100]  # 限制长度
                }
            else:
                installed[category][app] = {"installed": False}
    
    return installed


def get_conda_envs():
    """获取 conda 环境列表"""
    conda_path = os.path.expanduser("~/anaconda3/bin/conda")
    if not os.path.exists(conda_path):
        conda_path = os.path.expanduser("~/miniconda3/bin/conda")
    
    if not os.path.exists(conda_path):
        return {"installed": False}
    
    output, code = run_command([conda_path, "env", "list"])
    if code == 0:
        envs = []
        lines = output.split('\n')
        for line in lines:
            if line and not line.startswith('#'):
                parts = line.split()
                if parts:
                    envs.append(parts[0])
        return {
            "installed": True,
            "env_count": len(envs),
            "envs": envs
        }
    
    return {"installed": False}


def check_cuda_version():
    """检查 CUDA 版本"""
    output, code = run_command(["nvcc", "--version"])
    if code == 0:
        # 解析版本号
        for line in output.split('\n'):
            if "release" in line:
                parts = line.split("release")
                if len(parts) > 1:
                    version = parts[1].split(',')[0].strip()
                    return {"installed": True, "version": version}
    return {"installed": False}


def main():
    """主函数"""
    print("正在检测系统信息...\n")
    
    system_info = {
        "ubuntu_version": get_ubuntu_version(),
        "kernel_version": get_kernel_version(),
        "disk_space": get_disk_space(),
        "gpu": get_gpu_info(),
        "installed_tools": check_installed_tools(),
        "conda": get_conda_envs(),
        "cuda": check_cuda_version()
    }
    
    # 输出 JSON 格式
    print(json.dumps(system_info, indent=2, ensure_ascii=False))
    
    # 输出人类可读格式
    print("\n" + "="*60)
    print("系统信息摘要")
    print("="*60)
    
    if "Description" in system_info["ubuntu_version"]:
        print(f"系统版本: {system_info['ubuntu_version']['Description']}")
    
    print(f"内核版本: {system_info['kernel_version']}")
    
    if "total" in system_info["disk_space"]:
        print(f"磁盘空间: 总计 {system_info['disk_space']['total']}, "
              f"已用 {system_info['disk_space']['used']}, "
              f"可用 {system_info['disk_space']['available']}")
    
    if system_info["gpu"]["available"]:
        print(f"GPU: {system_info['gpu'].get('name', 'NVIDIA GPU')}")
        if "driver_version" in system_info["gpu"]:
            print(f"驱动版本: {system_info['gpu']['driver_version']}")
    else:
        print("GPU: 未检测到或未安装驱动")
    
    if system_info["cuda"]["installed"]:
        print(f"CUDA 版本: {system_info['cuda']['version']}")
    
    if system_info["conda"]["installed"]:
        print(f"Conda 环境: {system_info['conda']['env_count']} 个环境")
    
    # 统计已安装工具
    installed_count = 0
    for category, apps in system_info["installed_tools"].items():
        for app, info in apps.items():
            if info["installed"]:
                installed_count += 1
    
    print(f"已安装工具: {installed_count} 个")
    
    return system_info


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
