"""安装/卸载生成的 CLI wrapper 包。"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from clam.registry import registry


def _entry_point_path(app_id: str) -> str:
    """Resolve the full path to an installed entry point script."""
    venv_bin = Path(sys.executable).parent
    ep = venv_bin / f"clam-{app_id}"
    if ep.exists():
        return str(ep)
    return f"clam-{app_id}"


def install_wrapper(app_id: str, wrapper_dir: Path) -> bool:
    """以 editable 模式安装 wrapper 包。

    Args:
        app_id: 应用标识（如 "music"）。
        wrapper_dir: 包含 setup.py 的目录。

    Returns:
        安装和验证均成功则返回 True。
    """
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(wrapper_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"pip install failed:\n{result.stderr}")
        return False

    # 验证入口点可用
    ep_path = _entry_point_path(app_id)
    result = subprocess.run(
        [ep_path, "--help"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Verification failed: {ep_path} --help returned {result.returncode}")
        print(result.stderr)
        return False

    return True


def uninstall_wrapper(app_id: str) -> bool:
    """卸载 wrapper：pip uninstall + 删除文件 + 注销注册表。"""
    # pip uninstall
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", f"clam-{app_id}"],
        capture_output=True,
        text=True,
    )

    # 删除 wrapper 目录
    wrapper_dir = registry.REGISTRY_DIR / "wrappers" / app_id
    if wrapper_dir.exists():
        shutil.rmtree(wrapper_dir)

    # 注销
    registry.unregister(app_id)
    return True
