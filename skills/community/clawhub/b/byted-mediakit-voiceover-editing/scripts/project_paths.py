"""
产物工程根目录解析：<root>/output/ 及 --output-dir 约束均相对此 root。

不硬编码任何磁盘路径或固定目录名字符串；仅环境变量 + 相对于技能目录的层级推断。
"""
from __future__ import annotations

import os
from pathlib import Path


def get_project_root() -> Path:
    """
    解析顺序：
    1. VOICEOVER_EDITING_PROJECT_ROOT：显式指定工程根（expanduser + resolve）
    2. 否则：从 SKILL_DIR（本文件所在 `scripts/` 的父目录）向上一级走 3 步（parents[2]），
       作为工程根；路径过浅则再退一级。不依赖中间各级目录的命名。

    例：技能在 ``.../A/B/C/<SKILL_NAME>``（C 为 SKILL_DIR）→ 工程根为 ``.../A``，
    默认产物目录为 ``.../A/output``。若层级与预期不符，请使用环境变量①。
    """
    skill_root = Path(__file__).resolve().parents[1]

    override = (os.getenv("VOICEOVER_EDITING_PROJECT_ROOT") or "").strip()
    if override:
        root = Path(override).expanduser().resolve()
        print(f"[project_paths] 工程根（环境变量）: {root}")
        print(f"[project_paths] 产物目录: {root / 'output'}")
        return root

    try:
        root = skill_root.parents[2]
    except IndexError:
        root = skill_root.parent

    print(f"[project_paths] 技能目录 (SKILL_DIR): {skill_root}")
    print(f"[project_paths] 工程根（自动推导 parents[2]）: {root}")
    print(f"[project_paths] 产物目录: {root / 'output'}")
    return root
