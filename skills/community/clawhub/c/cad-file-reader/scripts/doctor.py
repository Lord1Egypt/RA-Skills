#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader 环境体检（doctor）：一条命令输出分档结论。

档 0：当前机器能直接处理哪些、缺哪些（DXF/DWG/PDF 矢量/扫描 OCR/测量/算量联动
      分别列出：可用 / 需外部转换 / 需OCR引擎 / 不可用）。
档 1：每项缺失给最小修复命令（优先本技能自带 scripts/setup.sh、install_vendor.sh、
      ensure_runtime.sh；PDF/OCR 依赖给对应技能安装命令；测量给 numpy 安装命令）。
档 2：DWG 缺少 ODA / LibreDWG 等转换后端时，给出下一步说明（含 --dwg-dxf-fallback
      复扫路径）。

规则：只读，不自动安装、不联网、不下载。检测逻辑复用 deps_check.sh / cad_scan /
read_cad / cad_pdf_ocr 的既有约定（vendor 目录、python 自举、常见可执行位路径），
不推翻重写。输出两份：人类可读（stdout + 可选 Markdown 文件）与 JSON 报告文件。

用法：
  python3 scripts/doctor.py                # 写 doctor-report.json + doctor-report.md 到当前目录，stdout 输出摘要
  python3 scripts/doctor.py --out-dir /tmp/doc
  python3 scripts/doctor.py --json-only    # 不写文件，JSON 打到 stdout（供脚本/CI）
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import platform
import shutil
import sys
from pathlib import Path

import platform_paths

REPORT_JSON = "doctor-report.json"
REPORT_MD = "doctor-report.md"
STATUS_OK = "可用"
STATUS_CONVERT = "需外部转换"
STATUS_OCR = "需OCR引擎"
STATUS_NONE = "不可用"
STATUSES = {STATUS_OK, STATUS_CONVERT, STATUS_OCR, STATUS_NONE}


def _norm_platform(hint: str | None = None) -> str:
    """把 ``darwin`` / ``win`` / ``linux`` 归一化（供 fix 分支与 os 字段）。"""
    return platform_paths.normalize_platform(hint)


def _fix_templates(platform_key: str) -> dict[str, str]:
    """按平台返回安装/修复命令模板。

    - darwin：保留 brew；
    - linux：apt-get / dnf / yum 二选一（命令内注明）;
    - win：winget / choco / 官方下载页。
    """
    if platform_key == "win":
        return {
            "setup": "powershell -ExecutionPolicy Bypass -File scripts/setup_windows.ps1",
            "vendor": "powershell -ExecutionPolicy Bypass -File scripts/setup_windows.ps1",
            "libredwg": ("winget install --id=ODA.FileConverter   # Windows 无官方 LibreDWG 包，用 ODAFileConverter 兜底；"
                         "或 choco install oda-file-converter；官方下载页 https://www.opendesign.com/guestfiles/oda_file_converter"),
            "poppler": ("winget install --id=oschwartz10692.Poppler   # 或 choco install poppler；"
                        "官方下载页 https://github.com/oschwartz10612/poppler-windows/releases"),
            "image_ocr": "codex skill install image-ocr",
            "pdf_inspector": "codex skill install pdf-inspector",
        }
    if platform_key == "linux":
        return {
            "setup": "bash scripts/setup_linux.sh",
            "vendor": "bash scripts/install_vendor.sh",
            "libredwg": ("sudo apt-get install -y libredwg-tools   # Debian/Ubuntu；"
                         "Fedora/RHEL/SUSE 用 sudo dnf install -y libredwg-tools"),
            "poppler": ("sudo apt-get install -y poppler-utils   # Debian/Ubuntu；"
                        "Fedora/RHEL/SUSE 用 sudo dnf install -y poppler-utils"),
            "image_ocr": "codex skill install image-ocr",
            "pdf_inspector": "codex skill install pdf-inspector",
        }
    return {
        "setup": "bash scripts/setup.sh",
        "vendor": "bash scripts/install_vendor.sh",
        "libredwg": "brew install libredwg",
        "poppler": "brew install poppler",
        "image_ocr": "codex skill install image-ocr",
        "pdf_inspector": "codex skill install pdf-inspector",
    }


def _make_fix(cap_id: str, label: str, status: str, detail: str,
              command: str, suggest: str = "") -> dict:
    """构造档 1 单条修复（含平台建议字段，供 --json-only 消费）。"""
    return {
        "capability": cap_id,
        "label": label,
        "status": status,
        "issue": detail,
        "command": command,
        "suggest": suggest,
        "note": "",
    }

# 与本技能既有 python 自举保持一致（deps_check.sh / run_cad.sh / setup.sh）
_RUNTIME_CANDIDATES = [
    Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3",
]
try:
    _RUNTIME_CANDIDATES += sorted((Path.home() / ".cache" / "codex-runtimes").glob("*/dependencies/python/bin/python3"))
except OSError:
    pass
_RUNTIME_CANDIDATES += [shutil.which("python3") or ""]


def _singular(path: str) -> Path | None:
    """把空字符串/Path('.') 归一成 None；只认真实存在的可执行文件。"""
    if not path:
        return None
    p = Path(path)
    return p if p.is_file() and os.access(str(p), os.X_OK) else None


def find_python() -> Path | None:
    seen: list[str] = []
    for cand in _RUNTIME_CANDIDATES:
        item = _singular(str(cand))
        if item and str(item) not in seen and item.is_file():
            seen.append(str(item))
            return item
    return None


def spec_available(name: str, vendor_root: Path) -> bool:
    try:
        old = list(sys.path)
        sys.path.insert(0, str(vendor_root))
        try:
            return bool(importlib.util.find_spec(name))
        finally:
            sys.path[:] = old
    except Exception:
        return False


def probe_python(python: Path, vendor_root: Path) -> dict:
    """用当前解读器做一次最小探测（只 import，不跑业务解析）。"""
    code = (
        "import importlib.util,sys\n"
        "for m in ['ezdwg','ezdxf','numpy','fontTools']:\n"
        "    try:\n"
        f"        sys.path.insert(0, {str(vendor_root)!r})\n"
        "        spec=importlib.util.find_spec(m)\n"
        "        print(m + '=' + ('1' if spec else '0'))\n"
        "    except Exception:\n"
        "        print(m + '=0')\n"
    )
    try:
        import subprocess
        proc = subprocess.run([str(python), "-I", "-c", code],
                              capture_output=True, text=True, timeout=30)
        result: dict[str, bool] = {}
        for line in (proc.stdout or "").splitlines():
            key, _, val = line.partition("=")
            if key:
                result[key] = val == "1"
        return result
    except Exception:
        return {}


def is_exec(path: Path | None) -> bool:
    return bool(path) and path.is_file() and os.access(str(path), os.X_OK)


def find_exec(*names: str, extra_dirs: list[Path] | None = None) -> Path | None:
    for name in names:
        found = shutil.which(name)
        if found:
            fmt = _singular(found)
            if fmt:
                return fmt
    for d in (extra_dirs or []):
        if not d.is_dir():
            continue
        for name in names:
            p = d / name
            if is_exec(p):
                return p
    return None


def calc_python_version(python: Path) -> str:
    try:
        import subprocess
        proc = subprocess.run([str(python), "-V"], capture_output=True, text=True, timeout=10)
        return (proc.stdout or proc.stderr or "").strip()
    except Exception:
        return str(python)




def _find_bus_client() -> tuple[str, str | None]:
    """只读探测 lis-skill-bus 联动脉冲（已装/未装/禁用）。与 cad_statesync.py 同口径。"""
    if os.environ.get("SKILLBUS_DISABLE") == "1":
        return "禁用（SKILLBUS_DISABLE=1）", None
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    cands: list[Path] = []
    sbc = os.environ.get("SKILLBUS_CLIENT")
    sbh = os.environ.get("SKILLBUS_HOME")
    if sbc:
        cands.append(Path(sbc))
    if sbh:
        cands.append(Path(sbh) / "skillbus_client.py")
    cands += [
        codex_home / "mcp_servers" / "lis-skill-bus" / "skillbus_client.py",
        codex_home / "skills" / "lis-skill-bus" / "skillbus_client.py",
        codex_home / "skills" / ".skillbus" / "skillbus_client.py",
    ]
    for cand in cands:
        if cand.is_file():
            return "已安装", str(cand)
    return "未装", None

def build_report(skill_root: Path, platform_hint: str | None = None) -> dict:
    plat = _norm_platform(platform_hint)
    fix_tpl = _fix_templates(plat)
    python = find_python()
    vendor = skill_root / "vendor"
    vendor_ok = bool(
        (vendor / "ezdwg").is_dir()
        and (vendor / "ezdxf").is_dir()
        and (vendor / "ezdxf" / "__init__.py").is_file()
        and (vendor / "fontTools").is_dir()
    )
    if python is None:
        python_ver = "缺失"
        probes: dict[str, bool] = {}
    else:
        python_ver = calc_python_version(python)
        probes = probe_python(python, vendor)

    ezdwg_ok = probes.get("ezdwg", False) or spec_available("ezdwg", vendor)
    ezdxf_ok = probes.get("ezdxf", False) or spec_available("ezdxf", vendor)
    numpy_ok = probes.get("numpy", False) or spec_available("numpy", vendor)
    font_tools_ok = probes.get("fontTools", False) or spec_available("fontTools", vendor)
    psutil_ok = bool(importlib.util.find_spec("psutil")) or spec_available("psutil", vendor)

    # 外部后端探测：统一走 platform_paths（dwg2dxf/ODA/pdftoppm/tesseract/ocr/pdf-inspector）
    home = Path.home()
    dwg2dxf = platform_paths.find_tool("dwg2dxf", platform_hint=platform_hint)
    oda = platform_paths.find_tool("ODAFileConverter", platform_hint=platform_hint)
    tesseract = platform_paths.find_tool("tesseract", platform_hint=platform_hint)

    pdf_route = None
    for cand in [
        Path(os.environ.get("PDF_INSPECTOR_ROUTE", "")),
        skill_root.parent / "pdf-inspector" / "scripts" / "pdf_route.py",
        home / ".codex" / "skills" / "pdf-inspector" / "scripts" / "pdf_route.py",
    ]:
        p = _singular(str(cand)) if cand else None
        if p:
            pdf_route = p
            break
    pdf_venv = _singular(str(Path(os.environ.get("PDF_INSPECTOR_VENV", ""))))
    if not pdf_venv:
        pdf_venv = _singular(platform_paths.find_tool("pdf-inspector-python", platform_hint=platform_hint) or "")
    pdf_py_ok = bool(python) or bool(pdf_venv)

    pdftoppm = platform_paths.find_tool(
        "pdftoppm",
        extra_dirs=[Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime"
                    / "dependencies" / "bin" / "override"],
        platform_hint=platform_hint,
    )
    ocr_image = None
    env_ocr = os.environ.get("OCR_IMAGE", "").strip()
    if env_ocr:
        ocr_image = _singular(env_ocr)
    if not ocr_image:
        ocr_image = _singular(platform_paths.find_tool("ocr_image", platform_hint=platform_hint) or "")
    image_ocr_skill = home / ".codex" / "skills" / "image-ocr"
    tessdata = home / ".cache" / "tessdata"

    qto_project = skill_root / "scripts" / "qto_project.py"
    qto_validate = skill_root / "scripts" / "qto_validate.sh"

    caps: dict[str, dict] = {}

    # ---- DXF ----
    if python is None:
        caps["dxf"] = {"label": "DXF", "status": STATUS_NONE, "detail": "未找到 Python 3.10+", "fix": ""}
    elif ezdxf_ok and font_tools_ok:
        caps["dxf"] = {"label": "DXF", "status": STATUS_OK,
                       "detail": "vendored ezdxf/fontTools 可用，可直接流式扫描并做几何候选", "fix": ""}
    else:
        caps["dxf"] = {"label": "DXF", "status": STATUS_NONE, "detail": "缺 vendored ezdxf/fontTools（文字扫描不受影响，几何会降级）",
                       "fix": fix_tpl["setup"]}

    # ---- DWG（直读 + 转换后端分开看） ----
    fixes_dwg: list[str] = []
    if python is None:
        caps["dwg"] = {"label": "DWG/DWT", "status": STATUS_NONE, "detail": "未找到 Python 3.10+", "fix": ""}
    elif vendor_ok and ezdwg_ok:
        caps["dwg"] = {"label": "DWG/DWT", "status": STATUS_OK,
                       "detail": ("本机 ezdwg 直读可用（同时检出转换后端：LibreDWG dwg2dxf=%s，ODAFileConverter=%s）"
                                  % ("有" if dwg2dxf else "无", "有" if oda else "无"))}
    elif vendor_ok and not ezdwg_ok:
        caps["dwg"] = {"label": "DWG/DWT", "status": STATUS_CONVERT,
                       "detail": "ezdwg C 扩展与当前解释器不匹配；cad_scan/read_cad 会自动尝试换解释器，仍不行则走 DWG→DXF 回退",
                       "fix": fix_tpl["libredwg"] + "   # 之后用 cad_scan.sh --dwg-dxf-fallback 复扫（或先恢复 vendor）"}
    elif not vendor_ok:
        caps["dwg"] = {"label": "DWG/DWT", "status": STATUS_NONE,
                       "detail": "vendored 解析库缺失", "fix": fix_tpl["setup"]}
    else:
        caps["dwg"] = {"label": "DWG/DWT", "status": STATUS_NONE, "detail": "未知原因（请跑 bash scripts/deps_check.sh --minimal 复核）",
                       "fix": fix_tpl["setup"]}

    # ---- PDF 矢量 ----
    if pdf_route and pdf_py_ok:
        caps["pdf_vector"] = {"label": "PDF 矢量", "status": STATUS_OK,
                              "detail": f"pdf-inspector 路由存在（{pdf_route}），原生文字坐标走本机分流", "fix": ""}
    elif pdf_route and not pdf_py_ok:
        caps["pdf_vector"] = {"label": "PDF 矢量", "status": STATUS_NONE,
                              "detail": "找到 pdf_route.py 但缺可执行 Python", "fix": fix_tpl["setup"] + " 后重试"}
    else:
        caps["pdf_vector"] = {"label": "PDF 矢量", "status": STATUS_NONE,
                              "detail": "缺 pdf-inspector 技能（pdf_route.py 不存在）", "fix": fix_tpl["pdf_inspector"] + "（或重建 $HOME/.codex/skills/pdf-inspector）"}

    # ---- PDF 扫描 OCR ----
    ocr_engine_ok = bool(ocr_image) and image_ocr_skill.is_dir()
    if pdftoppm and ocr_engine_ok:
        ocr_detail = "pdftoppm + image-ocr 齐备，扫描/混合页走本地 OCR"
        if tessdata.is_dir():
            ocr_detail += "（tessdata 语言包就位）"
        else:
            ocr_detail += "（tessdata 缺失时 OCR 可能降级，见档1）"
        caps["pdf_raster_ocr"] = {"label": "PDF 扫描/混合 OCR", "status": STATUS_OK, "detail": ocr_detail, "fix": ""}
    elif pdftoppm and not ocr_engine_ok:
        caps["pdf_raster_ocr"] = {"label": "PDF 扫描/混合 OCR", "status": STATUS_OCR,
                                  "detail": "缺 image-ocr / ocr_image 引擎，扫描页无法本地 OCR",
                                  "fix": fix_tpl["image_ocr"] + "   # 或确认 $HOME/.codex/skills/image-ocr/scripts/ocr_image 在 PATH"}
    elif not pdftoppm and ocr_engine_ok:
        caps["pdf_raster_ocr"] = {"label": "PDF 扫描/混合 OCR", "status": STATUS_CONVERT,
                                  "detail": "缺 pdftoppm（Poppler），PDF 无法渲染成像素页",
                                  "fix": fix_tpl["poppler"] + "   # 或配置 Codex 运行时自带 override/pdftoppm 到 PATH"}
    else:
        caps["pdf_raster_ocr"] = {"label": "PDF 扫描/混合 OCR", "status": STATUS_OCR,
                                  "detail": "缺 pdftoppm 且缺 image-ocr，扫描/混合页 OCR 不可用",
                                  "fix": fix_tpl["poppler"] + " && " + fix_tpl["image_ocr"]}

    # ---- 测量候选 ----
    if python is None:
        caps["measure"] = {"label": "长度/面积/体积测量候选", "status": STATUS_NONE, "detail": "未找到 Python", "fix": ""}
    elif ezdxf_ok and numpy_ok and font_tools_ok:
        caps["measure"] = {"label": "长度/面积/体积测量候选", "status": STATUS_OK,
                           "detail": "ezdxf + numpy 齐备，cad_measure 可跑几何测量候选", "fix": ""}
    elif ezdxf_ok and not numpy_ok:
        caps["measure"] = {"label": "长度/面积/体积测量候选", "status": STATUS_NONE,
                           "detail": "缺 numpy（只影响测量/梁线几何估算；DXF/DWG 文字图层仍可用）",
                           "fix": fix_tpl["vendor"] + "   # 会把 numpy、ezdwg、ezdxf、fontTools 装进 vendor/"}
    else:
        caps["measure"] = {"label": "长度/面积/体积测量候选", "status": STATUS_NONE, "detail": "缺 vendored ezdxf/fontTools/numpy",
                           "fix": fix_tpl["setup"]}

    # ---- 算量联动 ----
    qto_ok = qto_project.is_file() and qto_validate.is_file()
    caps["qto_linkage"] = {"label": "算量联动 (qto-project/v1)", "status": STATUS_OK if qto_ok else STATUS_NONE,
                           "detail": "qto init/wrap/validate 可用，五件套登记联动手册齐全" if qto_ok else "缺 qto_project.py/qto_validate.sh，可能下载包不完整",
                           "fix": "" if qto_ok else fix_tpl["setup"] + "   # 或重下完整包"}
    bus_state, bus_path = _find_bus_client()
    if bus_state == "已安装":
        caps["lis_skill_bus"] = {"label": "lis-skill-bus 联动总线（推荐）", "status": bus_state,
                                 "detail": f"已安装（{bus_path}）：同一张图只解析一次，五件套共享识图契约与项目状态",
                                 "fix": ""}
    else:
        caps["lis_skill_bus"] = {"label": "lis-skill-bus 联动总线（推荐）", "status": bus_state,
                                 "detail": "未安装：bus 缺失时各技能自动降级到本机状态，功能不受影响；推荐安装（SkillHub slug: lis-skill-bus；GitHub: lisong2003-lgtm/lis-skill-bus）。",
                                 "fix": ""}


    # ---- 档 1 修复清单（每条带平台专属 command + 跨平台 suggest） ----
    suggestions = {
        "dxf": "三平台通用：先跑本技能安装脚本；非 macOS 请用 scripts/setup_* 对应平台脚本。",
        "dwg": "Windows 建议 ODAFileConverter（winget/choco/官方下载页）；Linux 建议 libredwg-tools（apt/dnf/yum）；macOS 用 brew install libredwg。",
        "pdf_vector": "pdf-inspector venv：Windows 在 Scripts\\python.exe，Linux/macOS 在 .venv/bin/python；找不到就重建技能。",
        "pdf_raster_ocr": "Poppler：win 用 winget/choco/官方下载页；linux 用 poppler-utils（apt/dnf）；macOS 用 brew install poppler。",
        "measure": "缺 numpy 也可 pip 装进 vendor：python3 -m pip install --target vendor numpy。",
        "qto_linkage": "检查下载包完整性，或重下完整包后运行对应平台 setup。",
        "lis_skill_bus": "推荐安装 lis-skill-bus（SkillHub slug: lis-skill-bus；GitHub: lisong2003-lgtm/lis-skill-bus），装好后同一张图只解析一次；不装自动降级，功能不受影响。",
    }
    fixes: list[dict] = []
    for cap_id, cap in caps.items():
        if cap["status"] == STATUS_OK or not cap.get("fix"):
            continue
        fixes.append(_make_fix(cap_id, cap["label"], cap["status"], cap["detail"],
                               cap["fix"], suggestions.get(cap_id, "")))
    # 去重相同 command 的条目（vendor/setup 类）
    seen_cmd: set[str] = set()
    deduped: list[dict] = []
    for f in fixes:
        key = f["command"]
        if key and key in seen_cmd:
            continue
        if key:
            seen_cmd.add(key)
        deduped.append(f)

    # ---- 档 2：DWG 转换后端 ----
    dwg_backends = {
        "libredwg_dwg2dxf": bool(dwg2dxf),
        "odafileconverter": bool(oda),
    }
    if not (dwg_backends["libredwg_dwg2dxf"] or dwg_backends["odafileconverter"]):
        if plat == "win":
            dwg_next = (
                "当前机器没有检出 ODAFileConverter。下一步：\n"
                "  1) 首选安装 ODAFileConverter：winget install --id=ODA.FileConverter（或 choco install oda-file-converter；"
                "官方下载页 https://www.opendesign.com/guestfiles/oda_file_converter）；\n"
                "  2) 装好后把 ODAFileConverter 放进 PATH，read_cad/cad_scan 会自动走 ODA 转换；\n"
                "  3) 临时规避：用 CAD 软件把 DWG 另存为 DXF 再扫描，或用 cad_scan.sh 图纸.dwg --dwg-dxf-fallback 先试一次；\n"
                "  说明：Windows 没有官方 LibreDWG 包，转换后端以 ODAFileConverter 为准。"
            )
        elif plat == "linux":
            dwg_next = (
                "当前机器没有检出 LibreDWG(dwg2dxf) 或 ODAFileConverter。下一步：\n"
                "  1) 首选安装 LibreDWG：sudo apt-get install -y libredwg-tools（Debian/Ubuntu；"
                "Fedora/RHEL/SUSE 用 sudo dnf install -y libredwg-tools）；\n"
                "  2) 或安装 ODAFileConverter（放到 PATH）后 read_cad/cad_scan 会自动走 ODA 转换；\n"
                "  3) 临时规避：用 CAD 软件把 DWG 另存为 DXF 再扫描，或用 cad_scan.sh 图纸.dwg --dwg-dxf-fallback 先试一次；\n"
                "  说明：ezdwg 只能直读能解析的部分 DWG；遇到 unsupported DWG version / section map 报错时必须加转换后端。"
            )
        else:
            dwg_next = (
                "当前机器没有检出 LibreDWG(dwg2dxf) 或 ODAFileConverter。下一步：\n"
                "  1) 首选安装 LibreDWG：brew install libredwg（装到 /opt/homebrew/bin/dwg2dxf 后会被自动发现）；\n"
                "  2) 或安装 ODAFileConverter（放到 PATH）后 read_cad/cad_scan 会自动走 ODA 转换；\n"
                "  3) 临时规避：用 CAD 软件把 DWG 另存为 DXF 再扫描，或用 cad_scan.sh 图纸.dwg --dwg-dxf-fallback 先试一次；\n"
                "  说明：本机 ezdwg 只能直读能解析的部分 DWG；遇到 unsupported DWG version / section map 报错时必须加转换后端。"
            )
        dwg_tier2_status = "缺少转换后端"
    else:
        dwg_next = None
        dwg_tier2_status = "已有转换后端（LibreDWG/ODA）"

    report = {
        "tool": "cad-file-reader-doctor",
        "schema": "cad-file-reader/doctor-v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "skill_root": str(skill_root),
        "os": plat,
        "suggest": {f["capability"]: f["suggest"] for f in deduped},
        "python": {"found": bool(python), "resolved": str(python) if python else "", "version": python_ver,
                   "vendor_ok": vendor_ok,
                   "modules": {"ezdwg": ezdwg_ok, "ezdxf": ezdxf_ok, "numpy": numpy_ok, "fontTools": font_tools_ok}},
        "external": {"pdftoppm": bool(pdftoppm), "ocr_image": bool(ocr_image),
                     "tesseract": bool(tesseract), "image_ocr_skill": image_ocr_skill.is_dir(),
                     "pdf_route": bool(pdf_route), "pdf_inspector_venv_python": bool(pdf_venv), "tessdata": tessdata.is_dir()},
        "platform": {"os": platform.system(),
                     "memory_guard": {
                         "psutil_ok": psutil_ok,
                         "hint": "POSIX 优先 resource.getrusage；Windows/阻断时回退 psutil。psutil 可选，缺失时内存闸降级为协作式超时。",
                     }},
        "tier0": {
            "summary": {k: caps[k]["status"] for k in caps},
            "capabilities": caps,
        },
        "tier1": {"fixes": deduped},
        "tier2": {
            "dwg_conversion_backends": dwg_backends,
            "status": dwg_tier2_status,
            "next_steps": dwg_next,
        },
    }
    return report


def _bullet(cap: dict) -> str:
    name = cap["label"]
    st = cap["status"]
    det = cap.get("detail") or ""
    fix = cap.get("fix") or ""
    line = f"- {name}：{st}"
    if det:
        line += f" — {det}"
    if fix and st != STATUS_OK:
        line += f"\n   修复：{fix}"
    return line


def _t(lang, key, **kw):
    try:
        import i18n
        return i18n.T(lang, key, **kw)
    except Exception:
        return kw.get("default", key)


def render_text(report: dict, lang: str = "zh") -> str:
    lines = [_t(lang, "doctor_title"), ""]
    py = report["python"]
    vendor = _t(lang, "found" if py["vendor_ok"] else "missing")
    lines.append(_t(lang, "doctor_python", ver=py["version"] or "-", resolved=py["resolved"] or "-", vendor=vendor))
    pg = report.get("platform", {})
    guard = _t(lang, "memory_guard_on" if (pg.get("memory_guard") or {}).get("psutil_ok") else "memory_guard_off")
    lines.append(_t(lang, "doctor_platform", os=pg.get("os", "-"), guard=guard, hint=pg.get("memory_guard", {}).get("hint", "-")))
    lines.append("")
    lines.append(_t(lang, "tier0_title"))
    for cap in report["tier0"]["capabilities"].values():
        lines.append(_bullet(cap))
    lines.append("")
    lines.append(_t(lang, "tier1_title"))
    for f in report["tier1"]["fixes"]:
        lines.append(f"- {f['label']} [{f['status']}]：{f['command']}")
    lines.append("")
    lines.append(_t(lang, "tier2_title"))
    lines.append(f"- {report['tier2']['status']}")
    if report["tier2"]["next_steps"]:
        lines.append(report["tier2"]["next_steps"])
    return "\n".join(lines)


def render_md(report: dict, lang: str = "zh") -> str:
    py = report.get("python") or {}
    pg = report.get("platform") or {}
    guard = _t(lang, "memory_guard_on" if (pg.get("memory_guard") or {}).get("psutil_ok") else "memory_guard_off")
    lines = [_t(lang, "md_title"), "",
             _t(lang, "md_generated", t=report["generated_at"]),
             _t(lang, "md_skill_root", p=report["skill_root"]),
             _t(lang, "md_python", p=py.get("version") or "-", r=py.get("resolved") or "-"),
             _t(lang, "md_platform", os=pg.get("os", "-"), guard=guard, hint=(pg.get("memory_guard") or {}).get("hint", "-")),
             "",
             _t(lang, "md_tier0"), ""]
    lines.append(f"| {_t(lang, 'capability')} | {_t(lang, 'tier')} | {_t(lang, 'detail')} | {_t(lang, 'minimal_fix')} |")
    lines.append("|---|---|---|---|")
    for cap in report["tier0"]["capabilities"].values():
        fix = (cap.get("fix") or "").replace("|", "\\|")
        det = (cap.get("detail") or "").replace("|", "\\|")
        lines.append(f"| {cap['label']} | {cap['status']} | {det} | {fix or '—'} |")
    lines += ["", _t(lang, "md_tier1"), ""]
    if report["tier1"]["fixes"]:
        for f in report["tier1"]["fixes"]:
            lines.append(f"- **{f['label']}**（{f['status']}）：`{f['command']}`  · {f['issue']}")
    else:
        lines.append(_t(lang, "none_all_ok"))
    lines += ["", _t(lang, "md_tier2"), ""]
    lines.append(f"- {_t(lang, 'status')}：{report['tier2']['status']}")
    lines.append(f"- LibreDWG(dwg2dxf)：{'有' if report['tier2']['dwg_conversion_backends']['libredwg_dwg2dxf'] else '无'}")
    lines.append(f"- ODAFileConverter：{'有' if report['tier2']['dwg_conversion_backends']['odafileconverter'] else '无'}")
    if report["tier2"]["next_steps"]:
        lines.append("")
        lines.append(_t(lang, "next_step"))
        lines.append("")
        for ln in report["tier2"]["next_steps"].splitlines():
            lines.append(ln if ln.startswith(("  ", "1)", "2)", "3)", "-")) else f"- {ln}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    import i18n
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    _t = i18n.T
    ap = argparse.ArgumentParser(description=_t(lang, "doctor_desc"))
    ap.add_argument("--out-dir", default=".", help=_t(lang, "doctor_out_dir_help"))
    ap.add_argument("--json-out", default=None, help=_t(lang, "doctor_json_out_help"))
    ap.add_argument("--md-out", default=None, help=_t(lang, "doctor_md_out_help"))
    ap.add_argument("--skip-md", action="store_true", help=_t(lang, "doctor_skip_md_help"))
    ap.add_argument("--no-write", action="store_true", help=_t(lang, "doctor_no_write_help"))
    ap.add_argument("--json-only", action="store_true", help=_t(lang, "doctor_json_only_help"))
    ap.add_argument("--md-only", action="store_true", help=_t(lang, "doctor_md_only_help"))
    i18n.add_lang_arg(ap, default=lang)
    args = ap.parse_args(raw)
    lang = args.lang
    _t = i18n.T

    skill_root = Path(__file__).resolve().parent.parent
    report = build_report(skill_root)

    if args.json_only:
        out = dict(report)
        out["status"] = "ok"
        out["message"] = _t(lang, "ok")
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    if args.md_only:
        print(render_md(report, lang))
        return 0

    out_dir = Path(args.out_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    written = []
    if not args.no_write:
        json_path = Path(args.json_out) if args.json_out else out_dir / REPORT_JSON
        md_path = Path(args.md_out) if args.md_out else out_dir / REPORT_MD
        try:
            json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            written.append(str(json_path))
        except OSError as exc:
            print(_t(lang, "write_json_fail", exc=exc), file=sys.stderr)
        if not args.skip_md:
            try:
                md_path.write_text(render_md(report, lang) + "\n", encoding="utf-8")
                written.append(str(md_path))
            except OSError as exc:
                print(_t(lang, "write_md_fail", exc=exc), file=sys.stderr)

    print(render_text(report, lang))
    if written:
        print(_t(lang, "written_to", paths="，".join(written)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
