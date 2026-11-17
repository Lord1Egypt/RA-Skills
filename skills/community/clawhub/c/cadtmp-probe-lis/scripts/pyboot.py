#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台 Python 自举模块（cad-file-reader 专用）。

用途
----
- 跨平台找到可用的 Python 解释器：优先读取环境变量 ``CAD_PYTHON``，
  否则在 PATH 中按 ``python3`` -> ``python`` -> ``py`` 顺序探测。
- 统一把 PYTHONPATH 组装为「技能根 + skill_root/vendor」，并同步更新
  当前进程的 ``sys.path`` 与 ``os.environ["PYTHONPATH"]``，保证后续
  import ezdwg / ezdxf / fontTools 等 vendor 包即可用。
- vendor 缺失时打印安装指引并以退出码 3 结束。

三平台设计
----------
- macOS / Linux：同族命令 ``python3`` 最通用。
- Windows：优先 ``py``（官方 py launcher），其次 ``python`` / ``python3``；
  具体 Python 可执行名由调用方或 ``CAD_PYTHON`` 决定，脚本不做平台硬编码。
- 不调用 bash / subprocess，不依赖 shell 启动器，脚本可在 Windows
  的 cmd / PowerShell、macOS/Linux 的 shell 乃至各类集成环境直接运行。

约束
----
- 仅使用 Python 标准库。
- 不硬编码任何机器专属解释器路径（应用目录、homebrew 前缀、虚拟环境 bin 子目录等一律不写死）。
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path

# 本脚本位于 scripts/ 下，技能根 = 脚本所在目录的上一级。
SKILL_ROOT = Path(__file__).resolve().parent.parent
VENDOR_DIR = SKILL_ROOT / "vendor"
MIN_PY_VERSION = (3, 10)

# PATH 上需要探测的 Python 可执行名（按优先级排列，覆盖三平台常见命名）。
DEFAULT_PYTHON_NAMES = ("python3", "python", "py")

# vendor 完整可用所需的关键包目录；任一缺失都视为未安装完成。
REQUIRED_VENDOR_PACKAGES = ("ezdwg", "ezdxf", "fontTools")



def ensure_utf8_io() -> None:
    """跨平台中文兜底：stdout/stderr 切 UTF-8，并给子进程设 UTF-8 环境。

    特别解决 Windows cp1252 / 非 UTF-8 locale 下
    ``json.dump(..., ensure_ascii=False)`` 抛 UnicodeEncodeError 的问题。
    只读配置，不改变业务逻辑；重复调用安全。
    """
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


def skill_version() -> str:
    """读取技能版本号：优先 manifest.json，其次 SKILL.md front matter。

    manifest.json 是技能机器可读的权威入口；SKILL.md 作为可展示回退。
    """
    manifest = SKILL_ROOT / "manifest.json"
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            version = data.get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    skill_md = SKILL_ROOT / "SKILL.md"
    if skill_md.is_file():
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            if line.startswith("version:"):
                version = line.split(":", 1)[1].strip().strip('"').strip("'")
                if version:
                    return version
    return "unknown"


def vendor_ok(vendor_dir: Path = VENDOR_DIR) -> bool:
    """判断 vendor 是否已安装到可用状态。

    与 ensure_runtime.sh 保持一致的判定口径：核心包目录都存在才算完整。
    """
    if not vendor_dir.is_dir():
        return False
    return all((vendor_dir / pkg).is_dir() for pkg in REQUIRED_VENDOR_PACKAGES)


def find_python(env_name: str = "CAD_PYTHON",
                names: tuple[str, ...] = DEFAULT_PYTHON_NAMES) -> str | None:
    """跨平台定位 Python 解释器绝对路径。

    优先级：
    1. ``CAD_PYTHON`` 环境变量（显式指定的解释器，最优先）。
    2. PATH 中依次探测 python3 / python / py。

    返回第一个可用且可执行的结果；找不到返回 None。
    本函数绝不执行 shell / subprocess。
    """
    candidates: list[str] = []
    env_value = os.environ.get(env_name, "").strip()
    if env_value:
        candidates.append(env_value)
    for name in names:
        found = shutil.which(name)
        if found:
            candidates.append(found)

    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    return None


def pythonpath_entries(skill_root: Path = SKILL_ROOT,
                       vendor_dir: Path = VENDOR_DIR) -> list[str]:
    """组装 PYTHONPATH 条目：先技能根，后 vendor。

    返回去重后的绝对路径列表，不修改外部状态（纯计算）。
    """
    entries: list[str] = []
    for item in (skill_root, vendor_dir):
        resolved = str(Path(item).resolve())
        if resolved not in entries:
            entries.append(resolved)
    return entries


def configure_pythonpath(merge_existing: bool = True,
                         skill_root: Path = SKILL_ROOT,
                         vendor_dir: Path = VENDOR_DIR) -> list[str]:
    """把「技能根 + vendor」写入环境变量并同步到当前 sys.path。

    - 更新当前进程 os.environ["PYTHONPATH"] 与 sys.path，
      使导入 vendor 包立即生效。
    - merge_existing=True 时保留原有 sys.path / 已有 PYTHONPATH 条目，
      避免覆盖调用方注入的路径。
    """
    computed = pythonpath_entries(skill_root, vendor_dir)
    if merge_existing:
        existing = [p for p in sys.path if p and p not in computed]
        computed = computed + existing

    # 同步 sys.path：把本项目路径前插，保证本地 vendor 优先。
    for entry in pythonpath_entries(skill_root, vendor_dir):
        if entry not in sys.path:
            sys.path.insert(0, entry)

    current_env = os.environ.get("PYTHONPATH", "")
    if current_env:
        extra = [p for p in current_env.split(os.pathsep) if p and p not in computed]
        computed = computed + extra
    os.environ["PYTHONPATH"] = os.pathsep.join(computed)
    return computed


def build_guidance(vendor_dir: Path | None = None) -> str:
    """生成 vendor 缺失时的可操作安装指引（纯文本，不做任何网络/执行动作）。"""
    target_dir = vendor_dir or VENDOR_DIR
    setup_help = [
        "cad-file-reader 缺少 vendor 依赖包。",
        f"  期望目录：{target_dir!s}",
        f"  需要包含：{', '.join(REQUIRED_VENDOR_PACKAGES)}",
        "",
        "修复方式（选择其一）：",
        "  1) 运行安装器：scripts/setup.sh（macOS/Linux）或 scripts/setup_windows.ps1（Windows，如提供）",
        "  2) 已联网环境：执行 scripts/install_vendor.sh 自动补齐",
        "  3) 手动离线：把 ezdwg / ezdxf / fontTools（含 dist-info）解压到 vendor/ 目录",
        "",
        "补齐后重新运行本脚本即可。",
    ]
    return "\n".join(setup_help)


def bootstrap(require_vendor: bool = True,
              python_path: str | None = None,
              vendor_dir: Path | None = None) -> dict[str, object]:
    """执行一次跨平台自举：定位解释器、配置 PYTHONPATH、校验 vendor。

    vendor_dir 可显式指定（主要供测试/统一入口覆盖），缺省取项目 vendor/。
    返回结构化结果供调用方（含后续 run_cad.py 等统一入口）复用。
    """
    resolved_python = python_path or find_python()
    if not resolved_python:
        raise SystemExit(
            "❌ 未找到可用的 Python 解释器（已检查 CAD_PYTHON 与 PATH 上的 "
            "python3/python/py）。请先安装 Python 3.10+ 或设置 CAD_PYTHON。"
        )

    vendor = vendor_dir or VENDOR_DIR
    configured = configure_pythonpath(vendor_dir=vendor)
    ok = vendor_ok(vendor)

    result: dict[str, object] = {
        "skill_root": str(SKILL_ROOT),
        "vendor_dir": str(vendor),
        "python": resolved_python,
        "python_version": platform.python_version(),
        "python_paths": configured,
        "vendor_ok": ok,
        "skill_version": skill_version(),
        "os": platform.system(),
    }

    if require_vendor and not ok:
        print(build_guidance(vendor), file=sys.stderr)
        raise SystemExit(3)

    return result


def main(argv: list[str] | None = None) -> int:
    """CLI 入口。

    支持参数：
      --version    打印技能版本号，exit 0（不依赖 vendor）。
      --python     仅打印解析到的 Python 解释器路径（vendor 缺失也照常）。
      （无参数）    执行完整自举，vendor 缺失时打印指引并 exit 3。
    """
    ensure_utf8_io()
    args = list(sys.argv[1:] if argv is None else argv)

    if "--version" in args:
        print(skill_version())
        return 0

    if "--python" in args:
        resolved = find_python()
        if not resolved:
            print("❌ 未找到可用的 Python 解释器（已检查 CAD_PYTHON 与 PATH）。",
                  file=sys.stderr)
            return 1
        print(resolved)
        return 0

    result = bootstrap()
    status = "ok" if result["vendor_ok"] else "missing"
    print(f"python={result['python']}")
    print(f"python_version={result['python_version']}")
    print(f"skill_root={result['skill_root']}")
    print(f"vendor_dir={result['vendor_dir']}")
    print(f"vendor_status={status}")
    print(f"skill_version={result['skill_version']}")
    print(f"os={result['os']}")
    values = result["python_paths"]
    if isinstance(values, list):
        print(f"PYTHONPATH={os.pathsep.join(str(v) for v in values)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
