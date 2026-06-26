#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Akshare Stock Analyzer skill 环境检查与依赖安装脚本

用法（在 skill 根目录运行）：

    python3 scripts/setup_env.py

功能：
- 检查当前 Python 环境是否已安装本 skill 运行所需的核心依赖
- 如未安装，自动通过 `python -m pip install` 安装缺失包

说明：
- 默认使用当前解释器 (`sys.executable`) 对应的 pip
- 仅安装与本 skill 直接相关的最小依赖集合：akshare、pandas
"""

from __future__ import annotations

import subprocess
import sys
from typing import List

REQUIRED_PACKAGES: List[str] = [
    "akshare",
    "pandas",
]


def is_package_installed(package: str) -> bool:
    """使用 `python -m pip show` 判断包是否已安装。"""

    try:
        subprocess.check_output(
            [sys.executable, "-m", "pip", "show", package],
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package: str) -> None:
    """通过当前解释器调用 `pip install` 安装指定包。"""

    print(f"[INFO] 安装依赖包: {package} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main() -> None:
    print("[INFO] 使用解释器:", sys.executable)

    missing = [pkg for pkg in REQUIRED_PACKAGES if not is_package_installed(pkg)]

    if not missing:
        print("[OK] 所有必需依赖已经安装: ", ", ".join(REQUIRED_PACKAGES))
        return

    print("[WARN] 检测到以下依赖未安装: ", ", ".join(missing))
    for pkg in missing:
        try:
            install_package(pkg)
        except subprocess.CalledProcessError as exc:
            print(f"[ERROR] 安装 {pkg} 失败: {exc}")
            print("[HINT] 可手动执行: python3 -m pip install", pkg)
            # 不立即退出，尝试安装后续包

    # 再次检查
    still_missing = [pkg for pkg in REQUIRED_PACKAGES if not is_package_installed(pkg)]
    if still_missing:
        print("[WARN] 仍有依赖未成功安装: ", ", ".join(still_missing))
    else:
        print("[OK] 所有必需依赖已成功安装。")


if __name__ == "__main__":
    main()
