#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Everything Search v1 - Install & Discovery Script
自动发现 Everything 安装位置和 es.exe，配置 es.exe

作者: OneToken
版本: 1.0.0
仓库: https://github.com/1TOKENer/everything-search-skill
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
from typing import Optional, Tuple


# ============================================================
# 常量定义
# ============================================================

# 常用 Everything 安装路径
EVERYTHING_COMMON_PATHS = [
    r"C:\Program Files\Everything",
    r"C:\Program Files (x86)\Everything",
    r"D:\Program Files\Everything",
    r"D:\Program Files (x86)\Everything",
]


# Everything 官方下载地址
EVERYTHING_DOWNLOAD_URL = "https://www.voidtools.com/zh-cn/downloads/"
ES_CLI_URL = "https://www.voidtools.com/zh-cn/downloads/#cli"
EVERYTHING_SUPPORT_URL = "https://www.voidtools.com/zh-cn/support/everything/"

# 路径配置文件路径
PATH_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "path.env")


# ============================================================
# 显示优化工具
# ============================================================

def print_header(title: str) -> None:
    """打印带装饰的标题"""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def print_step(step_num: int, description: str) -> None:
    """打印步骤信息"""
    print(f"  [{step_num}] {description}")


def print_success(message: str) -> None:
    """打印成功信息"""
    print(f"  ✅ {message}")


def print_warning(message: str) -> None:
    """打印警告信息"""
    print(f"  ⚠️  {message}")


def print_error(message: str) -> None:
    """打印错误信息"""
    print(f"  ❌ {message}")


def print_info(message: str) -> None:
    """打印信息"""
    print(f"  ℹ️  {message}")


# ============================================================
# 路径发现
# ============================================================


def _find_from_running_process() -> Optional[str]:
    """
    从运行中的 Everything 进程获取 es.exe 路径
    
    Returns:
        es.exe 的完整路径，未找到返回 None
    """
    try:
        result = subprocess.run(
            ["wmic", "process", "where", "name='Everything.exe'", "get", "ExecutablePath"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10
        )
        
        for line in result.stdout.strip().split(chr(10)):
            line = line.strip()
            if line and line != "ExecutablePath" and os.path.isfile(line):
                everything_dir = os.path.dirname(line)
                es_path = os.path.join(everything_dir, "es.exe")
                if os.path.isfile(es_path):
                    return es_path
    except Exception:
        pass
    
    return None


def find_es_exe() -> Optional[str]:
    """
    查找 es.exe 的路径（供 search_core.py 调用）

    按优先级查找：
    0. 检测运行中的 Everything 进程
    1. path.env 配置文件中的 ES_PATH
    2. 环境变量 EVERYTHING_PATH 下的 es.exe
    3. 常用安装路径下的 es.exe
    4. 环境变量 ES_PATH
    5. 系统 PATH 中的 es.exe
    6. 尝试启动 Everything 后重试

    Returns:
        es.exe 的完整路径，未找到返回 None
    """
    # 0. 检测运行中的 Everything 进程
    es_path = _find_from_running_process()
    if es_path:
        return es_path

    # 1. 检查 path.env 配置文件
    _, env_es = load_path_config()
    if env_es and os.path.isfile(env_es):
        return env_es

    # 2. 检查环境变量 EVERYTHING_PATH
    everything_path = os.environ.get("EVERYTHING_PATH")
    if everything_path:
        es_path = os.path.join(everything_path, "es.exe")
        if os.path.isfile(es_path):
            return es_path

    # 3. 检查常用安装路径
    for base_path in EVERYTHING_COMMON_PATHS:
        es_path = os.path.join(base_path, "es.exe")
        if os.path.isfile(es_path):
            return es_path

    # 4. 检查环境变量 ES_PATH
    es_path = os.environ.get("ES_PATH")
    if es_path and os.path.isfile(es_path):
        return es_path

    # 5. 检查系统 PATH
    es_in_path = shutil.which("es") or shutil.which("es.exe")
    if es_in_path:
        return es_in_path

    # 6. 尝试启动 Everything 后重试
    if start_everything_background():
        es_path = _find_from_running_process()
        if es_path:
            return es_path

    return None


def find_everything_exe() -> Optional[str]:
    """
    查找 Everything.exe 的路径

    Returns:
        Everything.exe 的完整路径，未找到返回 None
    """
    # 1. 检查环境变量
    everything_path = os.environ.get("EVERYTHING_PATH")
    if everything_path:
        exe_path = os.path.join(everything_path, "Everything.exe")
        if os.path.isfile(exe_path):
            return exe_path

    # 2. 检查 path.env 配置文件
    env_everything, _ = load_path_config()
    if env_everything:
        exe_path = os.path.join(env_everything, "Everything.exe")
        if os.path.isfile(exe_path):
            return exe_path

    # 3. 检查常用安装路径
    for base_path in EVERYTHING_COMMON_PATHS:
        exe_path = os.path.join(base_path, "Everything.exe")
        if os.path.isfile(exe_path):
            return exe_path

    # 4. 检查系统 PATH
    exe_in_path = shutil.which("Everything")
    if exe_in_path:
        return exe_in_path

    return None


def is_wsl() -> bool:
    """
    检测是否在 WSL (Windows Subsystem for Linux) 环境中运行
    
    Returns:
        True 如果在 WSL 中
    """
    try:
        with open('/proc/version', 'r') as f:
            return 'microsoft' in f.read().lower()
    except Exception:
        return False


def is_everything_running() -> bool:
    """
    检查 Everything 是否在后台运行

    Returns:
        True 如果 Everything 正在运行
    """
    try:
        if is_wsl():
            # WSL 环境：使用 cmd.exe 调用 tasklist
            result = subprocess.run(
                ["cmd.exe", "/c", "tasklist", "/FI", "IMAGENAME eq Everything.exe"],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=10
            )
        elif sys.platform == 'win32':
            # Windows 原生环境
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Everything.exe"],
                capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
        else:
            return False
        return "Everything.exe" in result.stdout
    except Exception:
        return False


def start_everything_background() -> bool:
    """
    后台启动 Everything

    Returns:
        True 如果启动成功或已在运行
    """
    if is_everything_running():
        return True

    everything_exe = find_everything_exe()
    if not everything_exe:
        return False

    try:
        if is_wsl():
            # WSL 环境：直接执行 /mnt/c/.../Everything.exe
            subprocess.Popen(
                [everything_exe, "-startup"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        elif sys.platform == 'win32':
            # Windows 原生环境
            subprocess.Popen(
                [everything_exe, "-startup"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            return False
        
        # 等待启动完成
        for _ in range(10):  # 最多等待 5 秒
            time.sleep(0.5)
            if is_everything_running():
                return True
        return is_everything_running()
    except Exception:
        return False

# ============================================================
# 路径配置管理
# ============================================================

def save_path_config(everything_path: str, es_path: str, silent: bool = False) -> bool:
    """
    保存路径配置到 path.env 文件（不重复保存但可更新）

    Args:
        everything_path: Everything 安装目录
        es_path: es.exe 完整路径
        silent: 静默模式，不打印输出

    Returns:
        True 如果保存成功
    """
    try:
        env_dir = os.path.dirname(PATH_ENV_FILE)
        os.makedirs(env_dir, exist_ok=True)

        # 读取现有配置（如果存在）
        existing_config = {}
        if os.path.isfile(PATH_ENV_FILE):
            with open(PATH_ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing_config[key.strip()] = value.strip()

        # 更新配置
        existing_config['EVERYTHING_PATH'] = everything_path
        existing_config['ES_PATH'] = es_path

        # 写入文件
        with open(PATH_ENV_FILE, 'w', encoding='utf-8') as f:
            f.write("# Everything Search v1 路径配置\n")
            f.write("# 此文件由 install.py 自动生成/更新\n\n")
            for key, value in existing_config.items():
                f.write(f"{key}={value}\n")

        if not silent:
            print_success(f"路径配置已保存到: {PATH_ENV_FILE}")
        return True
    except Exception as e:
        if not silent:
            print_error(f"保存配置失败: {e}")
        return False


def load_path_config() -> Tuple[Optional[str], Optional[str]]:
    """
    从 path.env 文件加载路径配置
    
    Returns:
        (everything_path, es_path) 元组
    """
    if not os.path.isfile(PATH_ENV_FILE):
        return None, None
    
    everything_path = None
    es_path = None
    
    try:
        with open(PATH_ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "EVERYTHING_PATH":
                        everything_path = value
                    elif key == "ES_PATH":
                        es_path = value
        
        return everything_path, es_path
    except Exception:
        return None, None


# ============================================================
# 验证安装
# ============================================================

def verify_installation(everything_path: str, es_path: str, silent: bool = False) -> bool:
    """
    验证安装是否成功

    Args:
        everything_path: Everything 安装目录
        es_path: es.exe 完整路径
        silent: 静默模式，不打印输出

    Returns:
        True 如果验证通过
    """
    if not silent:
        print()
        print_header("验证安装")

    success = True

    # 检查 Everything
    everything_exe = os.path.join(everything_path, "Everything.exe")
    if os.path.isfile(everything_exe):
        if not silent:
            print_success(f"Everything.exe 存在: {everything_exe}")
    else:
        if not silent:
            print_error(f"Everything.exe 不存在: {everything_exe}")
        success = False

    # 检查 es.exe
    if os.path.isfile(es_path):
        if not silent:
            print_success(f"es.exe 存在: {es_path}")
    else:
        if not silent:
            print_error(f"es.exe 不存在: {es_path}")
        success = False

    # 测试 es.exe 是否可运行
    if os.path.isfile(es_path):
        try:
            result = subprocess.run(
                [es_path, "-version"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10
            )
            if result.returncode == 0:
                if not silent:
                    print_success("es.exe 可正常运行")
            else:
                if not silent:
                    print_warning(f"es.exe 返回非零状态码: {result.returncode}")
                if result.stderr:
                    if not silent:
                        print_warning(f"错误信息: {result.stderr.strip()}")
        except Exception as e:
            if not silent:
                print_error(f"es.exe 运行失败: {e}")
            success = False

    return success


# ============================================================
# 主流程
# ============================================================

def discover_and_configure(silent: bool = False) -> bool:
    """
    自动发现 Everything + es.exe 并保存配置

    供 search_core.py 在 es.exe 未找到时自动调用，也作为 install.py
    主流程的核心逻辑。

    流程：
    1. 检查已有 path.env 配置，验证通过则直接返回 True
    2. 调用 find_es_exe() 7 级优先级查找
    3. 找到后保存到 path.env 并验证

    Args:
        silent: 静默模式，不打印输出（供 search_core.py 自动调用时使用）

    Returns:
        True 如果配置成功
    """
    # 检查是否已有有效配置
    existing_everything, existing_es = load_path_config()
    if existing_everything and existing_es:
        if verify_installation(existing_everything, existing_es, silent=silent):
            return True

    # 全量发现
    es_path = find_es_exe()
    if not es_path:
        return False

    everything_path = os.path.dirname(es_path)
    save_path_config(everything_path, es_path, silent=silent)

    if verify_installation(everything_path, es_path, silent=silent):
        return True
    return False


def main():
    """主入口 — 交互式安装配置（输出完整信息）"""
    print_header("Everything Search v1 - 安装配置工具")
    print("  此工具将自动发现 Everything 安装位置并配置 es.exe")
    print()

    # 显示已有配置信息
    existing_everything, existing_es = load_path_config()
    if existing_everything and existing_es:
        print_info("发现已有 path.env 配置:")
        print_info(f"  EVERYTHING_PATH = {existing_everything}")
        print_info(f"  ES_PATH = {existing_es}")
        print()

        # 尝试验证现有配置
        if verify_installation(existing_everything, existing_es):
            print()
            print_success("配置验证通过，无需重新配置")
            return 0
        else:
            print()
            print_warning("配置验证失败，需要重新发现")

    # 委托给核心发现逻辑
    if discover_and_configure(silent=False):
        print()
        print_header("🎉 配置完成！")
        print("  现在可以使用 search_core.py 进行文件搜索:")
        print()
        print('    python search_core.py "*.pdf"')
        print('    python search_core.py "report"')
        print()
        return 0
    else:
        print()
        print_error("未能找到 es.exe")
        print_info("请先安装 Everything: https://www.voidtools.com/zh-cn/downloads/")
        print_info("并下载 es.exe: https://www.voidtools.com/zh-cn/downloads/#cli")
        return 1


if __name__ == "__main__":
    sys.exit(main())
