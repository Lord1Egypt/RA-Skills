#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台 Python 自举模块（纯标准库，供每个技能主入口共用）。

用法
----
```python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import pyboot
    pyboot.ensure_utf8_io()
except Exception:
    pass
```

职责
----
- ``ensure_utf8_io()``：stdout/stderr 与子进程环境统一 UTF-8，
  解决 Windows cp1252 locale 下中文 JSON/CSV 乱码或无输出的根因。
- ``find_python()``：跨平台定位可用的 Python 解释器（py/python3/python），
  供 .sh / .cmd / .ps1 薄转发使用；不执行 shell。
- ``skill_version()``：读 manifest.json（回退 SKILL.md frontmatter）的版本号。

约束
----
- 仅标准库；不联网、不写系统配置、不硬编码机器专属路径。
- 重复调用安全；任何异常均由调用方 try/except 兜底，不影响业务主流程。
"""
from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path


def ensure_utf8_io() -> None:
    """stdout/stderr 与子进程环境切 UTF-8（重复调用安全）。"""
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ.setdefault("PYTHONUTF8", "1")
    for _name in ("stdout", "stderr"):
        _stream = getattr(sys, _name, None)
        _reconf = getattr(_stream, "reconfigure", None)
        if callable(_reconf):
            try:
                _reconf(encoding="utf-8", errors="replace")
            except Exception:
                pass


def find_python(env_name: str = "SKILL_PYTHON",
                names: tuple[str, ...] = ("python3", "python", "py")) -> str | None:
    """跨平台定位 Python 解释器绝对路径；找不到返回 None。"""
    candidates: list[str] = []
    env_value = os.environ.get(env_name, "").strip()
    if env_value:
        candidates.append(env_value)
    for name in names:
        found = shutil.which(name)
        if found:
            candidates.append(found)
    for candidate in candidates:
        p = Path(candidate).expanduser()
        if p.is_file():
            if platform.system() == "Windows":
                return str(p)
            if os.access(p, os.X_OK):
                return str(p)
    return None


def skill_root() -> Path:
    """返回技能根目录（pyboot.py 所在 scripts/ 的上一级）。"""
    return Path(__file__).resolve().parent.parent


def skill_version() -> str:
    """读 manifest.json 版本号，回退 SKILL.md frontmatter。"""
    root = skill_root()
    manifest = root / "manifest.json"
    if manifest.is_file():
        try:
            data = __import__("json").loads(manifest.read_text(encoding="utf-8"))
            version = data.get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()
        except Exception:
            pass
    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            if line.startswith("version:"):
                version = line.split(":", 1)[1].strip().strip('"').strip("'")
                if version:
                    return version
    return "unknown"
