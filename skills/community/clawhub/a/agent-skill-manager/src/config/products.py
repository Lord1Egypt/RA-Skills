"""Product definitions for supported AI agent platforms."""

from __future__ import annotations

import os
import platform
from pathlib import Path

from ..models.product import ProductSpec

HOME = Path.home()
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", HOME / "AppData" / "Local"))
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"

# Central repository - the authoritative source for all skills
CENTRAL_DIR = HOME / ".agents" / "skills"

PRODUCTS: list[ProductSpec] = [
    {
        "name": "AutoClaw",
        "short": "autoclaw",
        "macos_path": HOME / ".openclaw" / "skills",
        "windows_path": HOME / ".openclaw" / "skills",
        "sync_method": "symlink",
        "note": "AutoClaw also scans ~/.openclaw-autoclaw/skills/ and ~/.agents/skills/",
        "extra_dirs_macos": [HOME / ".openclaw-autoclaw" / "skills"],
        "extra_dirs_windows": [HOME / ".openclaw-autoclaw" / "skills"],
    },
    {
        "name": "Kimi",
        "short": "kimi",
        "macos_path": HOME / ".config" / "agents" / "skills",
        "windows_path": HOME / ".config" / "agents" / "skills",
        "sync_method": "symlink",
        "note": "Kimi also scans ~/.kimi-code/skills/",
        "extra_dirs_macos": [HOME / ".kimi-code" / "skills"],
        "extra_dirs_windows": [HOME / ".kimi-code" / "skills"],
    },
    {
        "name": "MiniMax Code",
        "short": "minimax",
        "macos_path": HOME / ".agents" / "skills",
        "windows_path": HOME / ".agents" / "skills",
        "sync_method": "native",
        "note": "MiniMax Code natively scans ~/.agents/skills/, no sync needed",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "WorkBuddy",
        "short": "workbuddy",
        "macos_path": HOME / ".workbuddy" / "skills",
        "windows_path": HOME / ".workbuddy" / "skills",
        "sync_method": "symlink",
        "note": "Enable skill in settings.json",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
        "settings_file": HOME / ".workbuddy" / "settings.json",
    },
    {
        "name": "Trae",
        "short": "trae",
        "macos_path": HOME / ".trae" / "skills",
        "windows_path": HOME / ".trae" / "skills",
        "sync_method": "symlink",
        "note": "Trae also supports project-level .trae/skills/ and .agents/skills/",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "DuMate (Baidu)",
        "short": "dumate",
        "macos_path": None,
        "windows_path": None,
        "sync_method": "pack",
        "note": "DuMate manages skills via App; use pack command to generate .zip",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "CodeBuddy (Tencent)",
        "short": "codebuddy",
        "macos_path": HOME / ".codebuddy" / "skills",
        "windows_path": HOME / ".codebuddy" / "skills",
        "sync_method": "symlink",
        "note": "CodeBuddy CLI also scans ~/.agents/skills/; settings in ~/.codebuddy/settings.json",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
        "settings_file": HOME / ".codebuddy" / "settings.json",
    },
    {
        "name": "Comate / Wenxin Kuaima (Baidu)",
        "short": "comate",
        "macos_path": HOME / ".comate" / "skills",
        "windows_path": HOME / ".comate" / "skills",
        "sync_method": "symlink",
        "note": "Comate auto-loads skills from ~/.comate/skills/ on startup",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "Qoder / Tongyi Lingma (Alibaba)",
        "short": "qoder",
        "macos_path": HOME / ".qoderwork" / "skills",
        "windows_path": HOME / ".qoderwork" / "skills",
        "sync_method": "symlink",
        "note": "QoderWork CN stores skills in ~/.qoderwork/skills/",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "QwenWork / Qianwen Office (Alibaba)",
        "short": "qwenwork",
        "macos_path": HOME / ".qwenworkcn" / "skills",
        "windows_path": HOME / ".qwenworkcn" / "skills",
        "sync_method": "symlink",
        "note": "QwenWork desktop scans ~/.qwenworkcn/skills/; frontmatter needs name+version+description+description_zh",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
    {
        "name": "DoubaoWork (ByteDance)",
        "short": "doubaowork",
        "macos_path": HOME / ".super_doubao" / "super-doubao-runtime" / "workspace" / ".user_skills",
        "windows_path": LOCALAPPDATA / "DoubaoWork" / "User Data" / "Default" / ".doubaowork" / "agent_mode" / "workspace" / ".user_skills",
        "sync_method": "symlink",
        "note": "DoubaoWork user skills live in workspace/.user_skills; system skills in workspace/.skills",
        "extra_dirs_macos": [],
        "extra_dirs_windows": [],
    },
]


def get_product_path(product: ProductSpec) -> Path | None:
    """Get the primary skill directory for a product on the current platform."""
    if IS_WINDOWS:
        return product.get("windows_path")
    else:
        return product.get("macos_path")


def get_all_product_dirs(product: ProductSpec) -> list[Path]:
    """Get all skill directories for a product on the current platform."""
    primary = get_product_path(product)
    dirs = []
    if primary:
        dirs.append(primary)
    if IS_WINDOWS:
        dirs.extend(product.get("extra_dirs_windows", []))
    else:
        dirs.extend(product.get("extra_dirs_macos", []))
    return dirs


def get_product_by_short(name: str) -> ProductSpec | None:
    """Find a product by its short name."""
    for p in PRODUCTS:
        if p["short"] == name:
            return p
    return None
