"""
审核页 / 导出服务共用的产物目录解析：与 review_import_data.json 所在目录对齐。

未指定 --output-dir 时：在 output/ 根目录与各一级子目录中收集 review_import_data.json，
取修改时间最新的一份，避免子目录任务仍命中过期的 output/review_import_data.json。
"""
from __future__ import annotations

from pathlib import Path

from project_paths import get_project_root


def output_base(output_dir_override: str = "") -> Path:
    if not output_dir_override:
        return get_project_root() / "output"

    out_str = str(output_dir_override).strip()
    proj_root = get_project_root()
    out_base = (proj_root / "output").resolve()

    cand = Path(out_str)
    if cand.is_absolute():
        resolved = cand.resolve()
        return resolved

    resolved = (proj_root / out_str).resolve()
    return resolved


def review_import_data_path(output_dir_override: str = "") -> Path:
    """
    查找 review_import_data.json。
    - 已指定 output/<任务>：仅在该目录及其直接子目录中解析（与旧行为一致）。
    - 仅默认 output/：根文件与子目录内文件一并候选，按 mtime 取最新。
    """
    base = output_base(output_dir_override)
    direct = base / "review_import_data.json"
    user_scoped = bool(str(output_dir_override).strip())

    if user_scoped:
        if direct.exists():
            return direct
        if base.is_dir():
            for child in sorted(base.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
                cand = child / "review_import_data.json"
                if child.is_dir() and cand.exists():
                    return cand
        return direct

    candidates: list[Path] = []
    if direct.is_file():
        candidates.append(direct)
    if base.is_dir():
        for child in base.iterdir():
            if child.is_dir():
                cand = child / "review_import_data.json"
                if cand.is_file():
                    candidates.append(cand)
    if not candidates:
        return direct
    return max(candidates, key=lambda p: p.stat().st_mtime)


def infer_task_output_dir(output_dir_override: str = "") -> Path:
    """review_import_data.json 所在目录；若无此文件则回退到 output_base。"""
    rdp = review_import_data_path(output_dir_override)
    if rdp.exists():
        return rdp.parent
    return output_base(output_dir_override)


def safe_task_dir_name(name: str) -> str:
    """素材文件名（无扩展名）安全化，用作 output/<任务名> 单段目录名。"""
    s = (name or "").strip()
    if not s or s in (".", ".."):
        return "task"
    s = s.replace("\x00", "").replace("/", "_").replace("\\", "_")
    return s[:200] if s else "task"


def infer_prepare_output_dir(step6_filename: str) -> Path:
    """
    prepare_export_data 未指定 --output-dir 时：在 output/ 根目录与各一级子目录中查找 step6，
    按文件 mtime 取最新的一份所在目录（与流水线写入子目录后的布局一致）。
    """
    base = get_project_root() / "output"
    candidates: list[Path] = []
    direct = base / step6_filename
    if direct.is_file():
        candidates.append(direct)
    if base.is_dir():
        for child in base.iterdir():
            if child.is_dir():
                cand = child / step6_filename
                if cand.is_file():
                    candidates.append(cand)
    if not candidates:
        return base
    best = max(candidates, key=lambda p: p.stat().st_mtime)
    return best.parent
