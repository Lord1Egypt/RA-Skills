#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader 跨平台外部后端发现（platform_paths.py）。

用途
----
把散落在各业务脚本里的「macOS-only 探测逻辑」收拢成一张跨平台表：
  1. 优先在 PATH 里找可执行文件（三平台通用）；
  2. 找不到再按平台查常见安装目录（Windows / macOS / Linux 各自一张表）；
  3. 调用方还可以通过 ``extra_dirs`` 追加自定义安装目录。

本模块只做路径发现，不做解析、不执行外部命令，纯 Python 标准库。

三平台设计
----------
- Windows（win）：程序目录形如 ``%USERPROFILE%\\.codex``、``%LOCALAPPDATA%\\Programs\\...``、
  ``%ProgramFiles%\\...``；可执行名要额外尝试 ``.exe`` / ``.bat`` / ``.cmd``；
  venv Python 在 ``Scripts\\python.exe``。
- macOS / Linux：``$HOME/.codex``、`/usr/bin`、`/usr/local/bin`、`/opt/...`；
  venv Python 在 ``bin/python``；可执行文件需要同时具备可执行位。
- LibreDWG ``dwg2dxf`` 在 Windows 无官方包：平台表不做 Windows 探测，
  通过 ``tool_hint()`` 提示改用 ODAFileConverter 兜底。

约束
----
- 仅使用 Python 标准库；不硬编码本机用户目录、虚拟环境绝对路径、
  homebrew 前缀等机器专属字符串。
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# 工具名到平台表键的别名映射（大小写、扩展名均归一化处理）。
_ALIASES: dict[str, str] = {
    "dwg2dxf": "dwg2dxf",
    "libredwg": "dwg2dxf",
    "odafileconverter": "odafileconverter",
    "odafileconverter.exe": "odafileconverter",
    "oda": "odafileconverter",
    "pdftoppm": "pdftoppm",
    "pdftoppm.exe": "pdftoppm",
    "poppler-pdftoppm": "pdftoppm",
    "poppler": "pdftoppm",
    "tesseract": "tesseract",
    "tesseract.exe": "tesseract",
    "ocr_image": "ocr_image",
    "ocr-image": "ocr_image",
    "ocr_image.exe": "ocr_image",
    "pdf-inspector-python": "pdf-inspector-python",
    "pdf_inspector_python": "pdf-inspector-python",
    "pdf-venv-python": "pdf-inspector-python",
    "pdfinspectorpython": "pdf-inspector-python",
}

# 每个工具在磁盘上的真实可执行名（pdf-inspector 返回的是它自家 venv 的 Python）。
_EXEC_NAMES: dict[str, str] = {
    "dwg2dxf": "dwg2dxf",
    "odafileconverter": "ODAFileConverter",
    "pdftoppm": "pdftoppm",
    "tesseract": "tesseract",
    "ocr_image": "ocr_image",
    "pdf-inspector-python": "python",
}

# 平台提示文案：某些工具在特定平台没有官方包，需要给用户可操作的兜底说明。
_TOOL_NOTES: dict[tuple[str, str], str] = {
    ("dwg2dxf", "win"): (
        "Windows 无官方 LibreDWG 包；请安装 ODAFileConverter 并让它进入 PATH，"
        "或用 find_tool('ODAFileConverter') 找到后做 DWG→DXF 兜底。"
    ),
}

# 各工具在常见 Linux 目录下的父目录集合。
_DEFAULT_PATH_DIRS = ("/usr/bin", "/usr/local/bin", "/usr/sbin")


def normalize_platform(platform_hint: str | None = None) -> str:
    """把任意平台写法归一化到 ``win`` / ``darwin`` / ``linux`` 三档。

    未传时读取 ``sys.platform``（保持 stdlib）。
    """
    raw = (platform_hint or sys.platform or "").strip().lower()
    if raw.startswith("win") or raw in ("cygwin", "msys", "mingw"):
        return "win"
    if raw in ("darwin", "mac", "macos", "osx"):
        return "darwin"
    if raw.startswith("linux"):
        return "linux"
    return raw or "darwin"


def home_codex(platform_hint: str | None = None) -> Path:
    """返回本机 Codex 技能根目录：Windows 用 %USERPROFILE%\\.codex。

    macOS/Linux 传统路径 ``$HOME/.codex`` 保持不变；Windows 显式读
    ``%USERPROFILE%``，避免 HOME 不存在时误判。
    """
    plat = normalize_platform(platform_hint)
    if plat == "win":
        base = Path(os.environ.get("USERPROFILE") or str(Path.home()))
    else:
        base = Path(os.environ.get("HOME") or str(Path.home()))
    return base / ".codex"


def _exec_names(canonical: str, plat: str) -> tuple[str, ...]:
    """按平台生成候选可执行名（Windows 补 .exe/.bat/.cmd，其余平台补 .sh）。"""
    base = _EXEC_NAMES.get(canonical, canonical)
    names = [base]
    if plat == "win":
        names.extend([base + ".exe", base + ".bat", base + ".cmd"])
    else:
        names.append(base + ".sh")
    return tuple(dict.fromkeys(names))


def _canonical_name(name: str) -> str:
    """归一化工具名：去空白、统一小写、去掉常见可执行扩展名后查别名表。"""
    clean = (name or "").strip().lower()
    for ext in (".exe", ".bat", ".cmd", ".sh"):
        if clean.endswith(ext):
            clean = clean[: -len(ext)]
            break
    return _ALIASES.get(clean, clean)


def _is_executable_file(path: Path, plat: str) -> bool:
    if not path.is_file():
        return False
    # Windows 用扩展名判定可执行性，不要求 chmod +x；
    # macOS/Linux 仍要可执行位，和 shell 直接调用口径一致。
    if plat == "win":
        return True
    return os.access(str(path), os.X_OK)


def _local(localappdata: str | None, home: Path) -> Path:
    if localappdata:
        return Path(localappdata)
    return home / "AppData" / "Local"


def _oda_parents(plat: str, env: dict[str, str], home: Path) -> list[Path]:
    """ODAFileConverter 常见父目录（含版本号子目录的扩展）。"""
    if plat == "darwin":
        return [
            Path("/Applications/ODAFileConverter.app/Contents/MacOS"),
            Path("/Applications/ODAFileConverter/ODAFileConverter.app/Contents/MacOS"),
            home / "Applications" / "ODAFileConverter.app" / "Contents" / "MacOS",
        ]
    if plat == "linux":
        return [Path("/opt/ODAFileConverter"), Path("/opt/ODA"), Path("/opt")]
    local = _local(env.get("LOCALAPPDATA"), home)
    pf = Path(env.get("ProgramFiles") or "C:/Program Files")
    pf86_str = env.get("ProgramFiles(x86)")
    pf86 = Path(pf86_str) if pf86_str else Path("C:/Program Files (x86)")
    return [
        pf / "ODA" / "ODAFileConverter",
        pf / "ODAFileConverter",
        pf86 / "ODA" / "ODAFileConverter",
        local / "Programs" / "ODA" / "ODAFileConverter",
        local / "Programs" / "ODAFileConverter",
        local / "ODA",
    ]


def _expand_oda_dirs(parents: list[Path]) -> list[Path]:
    """把 ODA 父目录展开成真正可能含可执行文件的目录（含版本目录）。"""
    result: list[Path] = []
    for parent in parents:
        if not parent:
            continue
        result.append(parent)
        if parent.is_dir():
            for child in parent.glob("ODAFileConverter*"):
                if child.is_dir():
                    result.append(child)
            for pel in ("Program Files", "Program Files (x86)"):
                if parent.name == pel:
                    for child in parent.glob("ODA*"):
                        if child.is_dir():
                            result.append(child)
    return result


def _pdftoppm_dirs(plat: str, env: dict[str, str], home: Path, codex: Path) -> list[Path]:
    if plat == "darwin":
        return [
            Path("/opt/homebrew/bin"),
            Path("/usr/local/bin"),
            home / ".cache" / "codex-runtimes" / "codex-primary-runtime"
                 / "dependencies" / "bin" / "override",
        ]
    if plat == "linux":
        return _linux_path_dirs()
    local = _local(env.get("LOCALAPPDATA"), home)
    dirs = [
        local / "Programs" / "poppler" / "bin",
        local / "Programs" / "pdftoppm" / "bin",
    ]
    prefix = env.get("CONDA_PREFIX")
    if prefix:
        dirs.append(Path(prefix) / "Library" / "bin")
    dirs.extend([
        home / "miniconda3" / "Library" / "bin",
        home / "anaconda3" / "Library" / "bin",
        home / "AppData" / "Local" / "Continuum" / "anaconda3" / "Library" / "bin",
    ])
    pf = env.get("ProgramFiles")
    if pf:
        dirs.append(Path(pf) / "poppler" / "bin")
    return dirs


def _tesseract_dirs(plat: str, env: dict[str, str], home: Path) -> list[Path]:
    if plat == "darwin":
        return [Path("/opt/homebrew/bin"), Path("/usr/local/bin")]
    if plat == "linux":
        return _linux_path_dirs()
    local = _local(env.get("LOCALAPPDATA"), home)
    dirs = [
        local / "Programs" / "Tesseract-OCR",
        local / "Programs" / "Tesseract-OCR" / "bin",
    ]
    pf = env.get("ProgramFiles")
    if pf:
        dirs.insert(0, Path(pf) / "Tesseract-OCR")
    prefix = env.get("CONDA_PREFIX")
    if prefix:
        dirs.append(Path(prefix) / "Library" / "bin")
    dirs.extend([
        home / "miniconda3" / "Library" / "bin",
        home / "anaconda3" / "Library" / "bin",
    ])
    return dirs


def _linux_path_dirs() -> list[Path]:
    return [Path(d) for d in _DEFAULT_PATH_DIRS]


def _pdf_venv_dirs(plat: str, env: dict[str, str], codex: Path) -> list[Path]:
    root_env = env.get("PDF_INSPECTOR_ROOT", "").strip()
    root = Path(root_env) if root_env else codex / "skills" / "pdf-inspector"
    if plat == "win":
        return [root / ".venv" / "Scripts"]
    return [root / ".venv" / "bin"]


def known_dirs(name: str, platform_hint: str | None = None) -> list[Path]:
    """返回某工具在指定平台的『常见安装目录』（不检查是否存在）。"""
    plat = normalize_platform(platform_hint)
    canonical = _canonical_name(name)
    codex = home_codex(plat)

    if canonical == "dwg2dxf":
        if plat == "win":
            return []  # Windows 无官方 LibreDWG，靠 ODA 兜底
        dirs = [codex / "bin", Path("/usr/local/bin")]
        if plat == "darwin":
            dirs.insert(0, Path("/opt/homebrew/bin"))
        else:
            dirs.insert(0, Path("/usr/bin"))
        dirs.append(Path("/tmp/libredwg_install/bin"))
        return dirs

    if canonical == "odafileconverter":
        return _expand_oda_dirs(_oda_parents(plat, os.environ, Path.home()))

    if canonical == "pdftoppm":
        return _pdftoppm_dirs(plat, os.environ, Path.home(), codex)

    if canonical == "tesseract":
        return _tesseract_dirs(plat, os.environ, Path.home())

    if canonical == "ocr_image":
        return [codex / "bin", codex / "skills" / "image-ocr" / "scripts"]

    if canonical == "pdf-inspector-python":
        return _pdf_venv_dirs(plat, os.environ, codex)

    return []


def tool_hint(name: str, platform_hint: str | None = None) -> str:
    """返回工具在当前平台的提示文案（无则返回空字符串）。"""
    plat = normalize_platform(platform_hint)
    canonical = _canonical_name(name)
    return _TOOL_NOTES.get((canonical, plat), "")


def _which_path(name: str, plat: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    if plat == "win":
        for ext in (".exe", ".bat", ".cmd"):
            found = shutil.which(name + ext)
            if found:
                return found
    return None


def find_tool(name: str,
              extra_dirs=(),
              platform_hint: str | None = None) -> str | None:
    """跨平台定位外部后端：先 PATH，再查平台表，最后追加 ``extra_dirs``。

    - ``name``：工具名，如 ``dwg2dxf`` / ``ODAFileConverter`` / ``pdftoppm`` /
      ``tesseract`` / ``ocr_image`` / ``pdf-inspector-python``。
    - ``extra_dirs``：调用方自定义的搜索目录（目录本身即可，如 ``["/opt/mytools/bin"]``）。
    - ``platform_hint``：``"win"`` / ``"darwin"`` / ``"linux"``，缺省自动探测。
    - 返回绝对路径字符串；找不到返回 ``None``。
    """
    plat = normalize_platform(platform_hint)
    canonical = _canonical_name(name)

    path_hit = _which_path(name, plat)
    if path_hit:
        return path_hit

    directories = known_dirs(canonical, plat)
    for extra in extra_dirs:
        if extra:
            directories.append(Path(extra))

    for directory in directories:
        for exe in _exec_names(canonical, plat):
            candidate = directory / exe
            if _is_executable_file(candidate, plat):
                return str(candidate)
    return None


if __name__ == "__main__":  # 轻量自检，便于直接验证
    for tool in ("dwg2dxf", "ODAFileConverter", "pdftoppm", "tesseract",
                 "ocr_image", "pdf-inspector-python"):
        print(f"{tool}: {find_tool(tool, [], None)!r}  提示={tool_hint(tool)!r}")
