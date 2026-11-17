#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_scan.py — 低内存、免 CAD 软件的 DWG/DXF 图纸文字与构件型号提取器。

设计要点（与 cad-file-reader 的区别）：
  * 不构建整张图的实体对象树（那是内存/耗时大户），只按需解出文字、图层、块名。
  * DWG 走 ezdwg.raw.* 单类解码器；DXF 走逐行 tag 流式解析，两者都不渲染图片。
  * 每个解码阶段带 SIGALRM 时间预算，超时自动跳过，绝不卡死。

用法：
  python3 cad_scan.py 图纸.dwg                      # Markdown 构件清单到 stdout
  python3 cad_scan.py 目录 --glob "*.dwg" -o out     # 批量，写 out.md/out.json/out.csv
  python3 cad_scan.py 图纸.dwg --filter "板厚|C30"    # 只要含关键词的原文
  python3 cad_scan.py 图纸.dwg --cache-dir /tmp/cad-cache --roi 0,0,30000,20000
"""
from __future__ import annotations

import argparse

# ---- 内存看门狗（2026-08-31）：大文件会被 read_cad.py 的 20MB 入口闸导流到这里，
#      低内存路径同样要兜底，越线立即自杀，绝不允许把整机拖到卡死 ====
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
try:
    import mem_guard as _mg
    _mg.start(int(_os.environ.get("CAD_MEM_LIMIT_MB", "4096")), name="cad_scan内存闸")
except Exception as _e:
    print("[cad_scan内存闸] 看门狗未启用: %s" % _e, file=_sys.stderr)

import csv
import math
import fnmatch
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from cad_scan_cache import (
    load_cached_scan, file_digest, profile_for, save_cached_scan,
    records_in_roi, segments_in_roi, sheets_in_roi, sheet_bbox, sheet_id,
)

from cad_preflight import preflight_file

def _resolve_vendor() -> Path:
    """vendor 定位：环境变量 → 技能自身 vendor → 其他 Agent 技能目录（跨 Agent 复用）。"""
    env = os.environ.get("CAD_SKILL_VENDOR")
    if env and Path(env).is_dir():
        return Path(env)
    own = Path(__file__).resolve().parent.parent / "vendor"
    if own.is_dir():
        return own
    for cand in sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader/vendor")):
        if cand.is_dir():
            return cand
    for cand in (Path.home() / ".claude/skills/cad-file-reader/vendor",
                 Path.home() / ".codex/skills/cad-file-reader/vendor"):
        if cand.is_dir():
            return cand
    return own


VENDOR = _resolve_vendor()
if VENDOR.is_dir():
    sys.path.insert(0, str(VENDOR))


def ensure_runtime() -> None:
    """ezdwg 的 C 扩展按特定 Python 版本编译；当前解释器不匹配时自动换到可用解释器。"""
    if os.environ.get("CAD_SCAN_REEXEC") or not str(sys.argv[0]).endswith("cad_scan.py"):
        return
    try:
        sys.path.insert(0, str(VENDOR)) if str(VENDOR) not in sys.path else None
        import ezdwg  # noqa: F401
        return
    except Exception:
        pass
    import glob
    cands = [str(Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3")]
    cands += sorted(glob.glob(str(Path.home() / ".cache/codex-runtimes/*/dependencies/python/bin/python3")))
    cur = os.path.realpath(sys.executable)
    for c in cands:
        if os.path.isfile(c) and os.path.realpath(c) != cur:
            os.environ["CAD_SCAN_REEXEC"] = "1"
            os.execv(c, [c] + sys.argv)


ensure_runtime()

# ---------------------------------------------------------------- 超时保护
class Budget(Exception):
    pass


class stage:
    """with stage(60): ...  超时会抛 Budget，不影响主进程。

    跨平台：POSIX 走 safe_timeout 的 SIGALRM 硬超时（与原行为一致）；
    Windows 走协作式 Deadline，调用返回对象的 check() 触发超时。
    """

    def __init__(self, seconds: float):
        self.seconds = seconds

    def __enter__(self):
        import safe_timeout
        self._ctx = safe_timeout.deadline(self.seconds)
        self._dl = self._ctx.__enter__()
        return self._dl

    def __exit__(self, exc_type, exc_value, exc_tb):
        import safe_timeout
        try:
            return self._ctx.__exit__(exc_type, exc_value, exc_tb)
        except safe_timeout.DeadlineExceeded:
            raise Budget("time budget exceeded") from None


# ---------------------------------------------------------------- 构件型号规则
# 平法/结构图常见编号。顺序敏感：先长前缀，后单字母。
CODE_PATTERNS = [
    ("梁", re.compile(r"(?<![A-Za-z])(WKL|XL|LL|JZL|JGL|TXL|KL|DL|TL|WL|ZHL|QL|L)(\d{1,3}[a-f]?)\s*(\(\s*\d{1,3}\s*[AB]?\s*\))?", re.I)),
    ("板", re.compile(r"(?<![A-Za-z])(YKB|ZKB|KB|ZJB|QJB|XJB|LB|WB|XB|YB|DB|SB|CB|B|板)(\d{1,3}[a-f]?)(?![A-Za-z0-9])")),
    ("柱", re.compile(r"(?<![A-Za-z])(ZKZ|KZ|LZ|XKZ|GZ|GJZ|GGZ|ZH|TZ|JZ)(\d{1,3}[a-f]?)(?![A-Za-z0-9])")),
    ("墙", re.compile(r"(?<![A-Za-z])(YQZ|GBZ|FBZ|JLQ|LLQ|YQ|Q)(\d{1,3}[a-f]?)(?![A-Za-z0-9])")),
    ("基础", re.compile(r"(?<![A-Za-z])(JL|DJ|PJ|YJ|BJ|ZJ|JC|CT|RMB)(\d{1,3}[a-f]?)(?![A-Za-z0-9])")),
    # 门窗：前缀 + 4 位数字（前2位x100=洞口宽，后2位x100=洞口高）[推测]
    ("门窗", re.compile(r"(?<![A-Za-z0-9])(FBM|MHC|YHC|FHC|LMC|LGC|QMC|MFC|MC|FM|LC|SC|TC|PC|KC|GC|XC|ZC|DC|BC|VC|WM|CM|HM|LM|GM|DM|TM|XM|ZM|YLM|M|C)([甲乙丙]?)(\d{4})([A-Za-z]?)(?![0-9A-Za-z])")),
]
SIZE = re.compile(r"(?<!\d)(\d{2,4})\s*[x×*X]\s*(\d{2,4})(?!\d)")
CONC = re.compile(r"(?<![A-Za-z0-9])(C\d{2})(?![0-9A-Za-z])")
SLAB_THK = re.compile(r"(?:板厚|h\s*[=:]\s*|t\s*[=:]\s*)(6\d|7\d|8\d|9\d|[123]\d{2})(?:\s*mm)?", re.I)
REBAR = re.compile("[Φ\u03a6ⅠⅡⅢⅣ]{0,2}\\s*\\d{1,2}\\s*@\\s*\\d{2,3}(?:\\s*/\\s*\\d{2,3})?(?:\\s*\\(\\s*\\d{1,2}\\s*\\))?|[ⅠⅡⅢⅣΦ\u03a6]\\s*\\d{1,2}")

# 平法标注拆解
SPAN = re.compile(r"\(\s*(\d{1,3})\s*([AB])?\s*\)")
SEC_BH = re.compile(r"(?<![\d.])(\d{2,3})\s*[x×*X]\s*(\d{3,4})(?![\d.])")
STIRRUP = re.compile(r"([ⅠⅡⅢⅣΦ\u03a6])?\s*(\d{1,2})\s*@\s*(\d{2,3})(?:\s*/\s*(\d{2,3}))?(?:\s*\(\s*(\d{1,2})\s*\))?")
LONGIT_SEQ = re.compile(r"(?<![\d.A-Za-z\u2160-\u2163\u03a6])(\d{1,2}\s*[\u2160\u2161\u2162\u2163\u03a6]\s*\d{1,2}(?:\s*\+\s*\d{1,2}\s*[\u2160\u2161\u2162\u2163\u03a6]\s*\d{1,2})*)")
LONGIT_ONE = re.compile(r"(\d{1,2})\s*([\u2160\u2161\u2162\u2163\u03a6])\s*(\d{1,2})")
COVER = re.compile(r"保护层[^\d]{0,6}(\d{2,3})")
SEISMIC = re.compile(r"抗震等级?\s*[为:\uff1a=]?\s*(特[一二三]级|一级|二级|三级|四级)")
SPEC_ORDER = ("板厚", "混凝土等级", "保护层", "抗震等级")
DOOR_LAYER = re.compile(r"门窗|洞口|玻璃|m-|c-|win|door", re.I)
PRACTICE_PAT = re.compile(
    r"(屋面|楼面|地面|墙面|内墙|外墙|顶棚|天棚|散水|勒脚|踢脚|防水|保温|门窗|栏杆|涂料|饰面|防潮)"
    r"(?:做法)?\s*[:：]"
)

TEXT_KINDS = ("text", "mtext", "attrib")
_OK_CHARS = re.compile(r"[\u4e00-\u9fff\w\u3000-\u303f．，、；：（）()／/%±≤≥Φ\-+.,;:()\[\]/*=&#°~@\u2014\u2018\u2019\u201c\u201d\\s]")


def readable(s: str) -> bool:
    """过滤天正/T3 导出对象等产生的乱码串：有效字符占比过低就丢弃。"""
    s = (s or "").strip()
    if not s:
        return False
    return len(_OK_CHARS.findall(s)) / max(1, len(s)) >= 0.8


def extract_practices(t: str, file_idx, sheet, layer):
    rows = []
    for seg in re.split(r"[。；;\n]+", t or ""):
        seg = seg.strip()
        m = PRACTICE_PAT.search(seg)
        if m and len(seg) <= 400:
            txt = re.sub(r"^\s*[（(]?\d+[）).、]?\s*", "", seg)
            rows.append({"part": m.group(1), "text": txt[:200],
                         "file": file_idx, "sheet": sheet, "layer": layer})
    return rows


CAD_ESCAPES = {
    "%%130": "\u2160", "%%131": "\u2161", "%%132": "\u2162", "%%133": "\u2163", "%%134": "\u2164",
    "%%c": "\u03a6", "%%d": "\u00b0", "%%p": "\u00b1", "%%%%": "%",
}


def normalize(s: str) -> str:
    '''AutoCAD/天正 文字转义还原：%%130~%%134 = 一~四级钢符号，%%c=直径，反斜杠U+XXXX=Unicode。'''
    if not s:
        return ""
    for k, v in CAD_ESCAPES.items():
        s = s.replace(k, v).replace(k.upper(), v)
    s = re.sub(r"\\U\+([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), s)
    return s


def clean_mtext(s: str) -> str:
    s = re.sub(r"\\[A-Za-z][^;{}]*;", " ", s or "")
    s = re.sub(r"[{}]", " ", s)
    s = s.replace("\\P", " ").replace("\\~", " ")
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- DWG
DECODERS = {
    "layers": "decode_layer_names",
    "text": "decode_text_entities",
    "mtext": "decode_mtext_entities",
    "attrib": "decode_attrib_entities",
    "insert": "decode_insert_entities",
    "blocks": "decode_block_header_names",
    "line": "decode_line_entities",
    "lwpoly": "decode_lwpolyline_entities",
    "circle": "decode_circle_entities",
    "placements": "decode_entity_placements",
}
GEOM_KINDS = ("line", "lwpoly")


def _insert_worker_row(row, layer_name: str) -> list:
    """把 ezdwg INSERT 行转成 worker 输出行（可单测，不依赖子进程）。

    ezdwg 现行 9 字段：(handle, x, y, z, xscale, yscale, zscale, rotation_rad, block_name)。
    旧版 8 字段没有块名，末位仍是 rotation_rad；块名为空时由上层如实标注缺失。
    """
    block_name = str(row[8] or "") if len(row) >= 9 else ""
    rot = row[7] if len(row) >= 8 and isinstance(row[7], (int, float)) else None
    rot_deg = math.degrees(float(rot)) if rot is not None else None
    scales = [float(v) if isinstance(v, (int, float)) else None
              for v in (row[4:7] if len(row) >= 7 else [])]
    while len(scales) < 3:
        scales.append(None)
    point = [row[1] if isinstance(row[1], (int, float)) else None,
             row[2] if isinstance(row[2], (int, float)) else None,
             row[3] if len(row) > 3 and isinstance(row[3], (int, float)) else None]
    return [row[0], block_name, point, layer_name, rot_deg, scales]


def _worker(name: str, path: str) -> int:
    """子进程模式：只解一类对象，逐行输出 JSON，进程退出即彻底释放内存。"""
    import ezdwg  # noqa: F401
    from ezdwg import raw

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    def safe(v):
        if isinstance(v, str):
            v = v.encode("utf-8", "replace").decode("utf-8", "replace")
            return "".join(ch if ch >= " " or ch == "\t" else " " for ch in v)
        return v

    fn = getattr(raw, DECODERS[name])
    rows = fn(path) or []
    layer_by_handle: dict[int, str] = {}
    layer_names: dict[int, str] = {}
    layer_names_ok = False
    try:
        layer_names = dict(raw.decode_layer_names(path) or [])
        layer_names_ok = any(str(v).strip() for v in layer_names.values())
    except Exception:
        layer_names = {}
        layer_names_ok = False
    if name not in ("layers", "blocks") and rows:
        try:
            handles = [r[0] for r in rows if isinstance(r[0], int)]
            if handles:
                ent_layers = raw.decode_object_entity_layer_handles(path, handles) or []
                # 图层名解不出来时（实测 AC1021 某些文件 decode_layer_names 返回整表空串，
                # 但句柄完全可解），退到「句柄即图层身份」：同一图层的实体仍能归到一组，
                # 只是语义名不可得。用 #xxxx 前缀明确标注这不是真实图层名，绝不伪造名字。
                for ent_handle, layer_handle in ent_layers:
                    name_text = str(layer_names.get(layer_handle, "") or "").strip()
                    layer_by_handle[ent_handle] = name_text if name_text else handle_layer_label(layer_handle)
        except Exception:
            pass
    if name not in ("layers", "blocks") and rows and not layer_names_ok:
        try:
            sys.stdout.write(json.dumps({"__note__": "图层名解码失败（图层表可读但名称为空），已用句柄标识图层（#xxxx）；语义图层名不可得，分类请依赖文字/几何"}) + "\n")
        except Exception:
            pass
    if name == "placements":
        for row in rows:
            if not isinstance(row, (tuple, list)) or len(row) < 3:
                continue
            try:
                sys.stdout.write(json.dumps([int(row[0]), int(row[1]), int(row[2])], ensure_ascii=True) + "\n")
            except Exception:
                continue
        sys.stdout.flush()
        return 0
    for row in rows:
        layer_name = str(layer_by_handle.get(row[0], "") or "") if isinstance(row[0], int) else ""
        out = [None, None, None, layer_name]
        for item in row:
            if out[2] is None and isinstance(item, (tuple, list)) and len(item) == 3:
                out = [row[0], row[1] if isinstance(row[1], str) else None, [float(x) if isinstance(x, (int, float)) else None for x in item]]
                out.append(layer_name)
                break
        if out[1] is None and isinstance(row[1], str):
            out[1] = row[1]
            out[3] = layer_name
        if name in ("layers", "blocks"):
            label = str(row[1] or "")
            if name == "layers" and not label.strip() and isinstance(row[0], int):
                label = handle_layer_label(row[0])  # 与实体侧同一套标识，保证两处能对上
            out = [row[0], label, None, None]
        if name == "insert":
            out = _insert_worker_row(row, layer_name)
        if name == "line" and len(row) >= 6:
            out = [row[0], None, [row[1], row[2], row[4], row[5]], layer_name]
        if name == "lwpoly":
            flat = []
            vs = row[2] if len(row) > 2 and isinstance(row[2], list) else []
            for pt in vs[:300]:
                if isinstance(pt, (tuple, list)) and len(pt) >= 2:
                    flat += [pt[0], pt[1]]
            out = [row[0], None, flat, layer_name]
        if name == "circle" and len(row) >= 5:
            # 行格式 (handle, x, y, z, r)；把半径放进坐标槽第 3 位，主流程按圆消费。
            out = [row[0], None, [row[1], row[2], row[4]], layer_name]
        try:
            sys.stdout.write(json.dumps([safe(x) for x in out], ensure_ascii=True, default=float) + "\n")
        except Exception:
            continue
    sys.stdout.flush()
    return 0


def handle_layer_label(handle) -> str:
    """图层名解不出来时用句柄当图层身份。`#` 前缀明确标注这不是真实图层名，绝不伪造名字。"""
    try:
        return f"#{int(handle):04X}"
    except Exception:
        return "#UNKNOWN"


def parse_worker_lines(text: str) -> tuple[list, list[str]]:
    """解析 worker 的 stdout：数据行成 list，{"__note__": ...} 转成 notes，坏行跳过。"""
    rows: list = []
    notes: list[str] = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue  # 个别乱码行跳过，不影响整体
        if isinstance(obj, dict):
            if obj.get("__note__"):
                notes.append(str(obj["__note__"]))
            continue
        rows.append(obj)
    return rows, notes


def _rows(name: str, path: str, budget: float, notes: list):
    """在子进程里解一类对象，逐行收回 JSON；子进程退出即释放内存。"""
    import subprocess
    cmd = [sys.executable, os.path.abspath(__file__), "--worker", name, path]
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        notes.append(f"{name} 解码超 {budget:.0f}s 预算，已终止（该图纸此类对象过多）")
        return None
    except Exception as e:
        notes.append(f"{name} 解码异常：{e}")
        return None
    if cp.returncode != 0:
        err = (cp.stderr or "").strip().splitlines()
        notes.append(f"{name} 解码失败：{err[-1][:120] if err else cp.returncode}")
        return None
    rows, worker_notes = parse_worker_lines(cp.stdout)
    notes.extend(worker_notes)
    return rows


def dwg_records(path: str, want: set[str], per_stage: float, max_rows: int, log, want_blocks: bool = False,
                 roi=None) -> tuple[list[dict], list[str], list[str], dict]:
    notes: list[str] = []
    recs: list[dict] = []
    layers: list[str] = []
    meta: dict = {}
    import subprocess

    def call(name, budget):
        if name in ("mtext", "attrib"):
            budget *= 3  # 这两类是 C 层全对象扫描，大图明显更慢
        return _rows(name, path, budget, notes)

    rows = call("layers", per_stage)
    if rows:
        layers = [str(r[1]) for r in rows if r and r[1]]
    log(f"图层 {len(layers)} 个")

    for name, kind in (("text", "TEXT"), ("mtext", "MTEXT"), ("attrib", "ATTRIB")):
        if name not in want:
            continue
        rows = call(name, per_stage)
        if not rows:
            continue
        for r in rows:
            if len(recs) >= max_rows:
                notes.append(f"文字数达上限 {max_rows}，已截断")
                break
            txt = str(r[1] or "")
            if name != "text":
                txt = clean_mtext(txt)
            pt = r[2] or [None, None]
            x = pt[0] if len(pt) > 0 else None
            y = pt[1] if len(pt) > 1 else None
            if not _rc_in_roi(x, y, roi):
                continue
            recs.append({"kind": kind, "text": txt, "x": x, "y": y,
                         "layer": r[3] if len(r) > 3 else None})
        log(f"{kind} {len([x for x in recs if x['kind'] == kind])} 条")

    if "insert" in want:
        rows = call("insert", per_stage)
        if rows:
            meta["insert_count"] = len(rows)
            named_ins = [r for r in rows if r and len(r) > 1 and r[1]]
            meta["block_refs"] = dict(Counter(str(r[1]) for r in named_ins).most_common(40))
            empty_ins = len(rows) - len(named_ins)
            if empty_ins and empty_ins == len(rows):
                notes.append("DWG 块引用名解码为空，块级/苗木块语义建议转 DXF 复核")
            elif empty_ins:
                notes.append(f"DWG 块引用名有 {empty_ins}/{len(rows)} 条解码为空，块级语义建议转 DXF 复核")
            for r in rows:
                if len(recs) >= max_rows:
                    break
                if r[1] and not r[1].startswith("*"):
                    pt = r[2] or [None, None]
                    x = pt[0] if len(pt) > 0 else None
                    y = pt[1] if len(pt) > 1 else None
                    if not _rc_in_roi(x, y, roi):
                        continue
                    rec = {"kind": "INSERT", "text": r[1], "block_name": r[1],
                           "x": x, "y": y,
                           "z": pt[2] if len(pt) > 2 else None,
                           "layer": r[3] if len(r) > 3 else None}
                    if len(r) > 4 and r[4] is not None:
                        rec["rotation"] = r[4]
                    if len(r) > 5 and isinstance(r[5], (list, tuple)):
                        scales = list(r[5]) + [None, None, None]
                        rec["xscale"] = scales[0]
                        rec["yscale"] = scales[1]
                        rec["zscale"] = scales[2]
                    # DWG 直读不提供 BLOCK 基点；明确标空，由下游决定是否只能用插入点。
                    rec["base_point"] = None
                    rec["base_point_source"] = "unavailable"
                    recs.append(rec)
        log(f"块引用 {meta.get('insert_count', 0)} 个")

    rows = call("blocks", per_stage) if want_blocks else None
    if rows:
        raw_defs = [str(r[1]).strip() for r in rows if r[1] and str(r[1]).strip()]
        garble_count = sum(1 for x in raw_defs if _is_garble_name(x))
        if garble_count:
            notes.append(f"块定义中 {garble_count} 个块名疑似编码乱码，已用 _BLK# 占位，建议转 DXF 复核")
        seen_defs: dict[str, str] = {}
        for x in raw_defs:
            if x.startswith("*"):
                continue
            seen_defs.setdefault(_safe_block_key(seen_defs, x), x)
        meta["block_defs"] = sorted(seen_defs)[:2000]
        log(f"块定义 {len(meta['block_defs'])} 个")

    return recs, layers, notes, meta


def _f(row, idx, comp):
    try:
        v = row[idx]
        if isinstance(v, (tuple, list)) and len(v) > comp:
            return float(v[comp])
    except Exception:
        pass
    return None


# ---------------------------------------------------------------- DXF（流式，不加载几何）
def dxf_records(path: str, max_rows: int, log, roi=None,
                include_insert: bool = False) -> tuple[list[dict], list[str], list[str], dict]:
    recs: list[dict] = []
    layers: set[str] = set()
    blocks: Counter = Counter()
    block_bases: dict[str, dict] = {}
    notes: list[str] = []
    meta: dict = {}
    kind = None
    buf: dict = {}
    mtext_parts: list[str] = []

    def flush():
        nonlocal buf, mtext_parts
        if not buf:
            return
        layer = buf.get("8")
        if layer:
            layers.add(layer)
        if buf.get("_kind") in ("TEXT", "MTEXT", "ATTRIB", "ATTDEF"):
            txt = " ".join(p for p in ([buf.get("1", "")] + mtext_parts) if p)
            if txt.strip():
                xv, yv = _num(buf.get("10")), _num(buf.get("20"))
                if _rc_in_roi(xv, yv, roi):
                    recs.append({"kind": buf["_kind"], "text": clean_mtext(txt),
                                 "x": xv, "y": yv,
                                 "layer": layer or None,
                                 "rotation": _num(buf.get("50"))})
        if buf.get("_kind") == "BLOCK" and buf.get("2"):
            name = str(buf.get("2") or "").strip()
            if name:
                bx, by = _num(buf.get("10")), _num(buf.get("20"))
                block_bases[name.upper()] = {
                    "name": name,
                    "base_point": [bx if bx is not None else 0.0,
                                   by if by is not None else 0.0],
                }
        if buf.get("_kind") == "INSERT" and buf.get("2"):
            name = str(buf.get("2") or "").strip()
            blocks[name] += 1
            xv, yv = _num(buf.get("10")), _num(buf.get("20"))
            if include_insert and sec == "ENTITIES" and name and not name.startswith("*") \
                    and sane(xv, yv) and _rc_in_roi(xv, yv, roi):
                sx, sy, sz = (_num(buf.get("41")), _num(buf.get("42")),
                              _num(buf.get("43")))
                rec = {
                    "kind": "INSERT",
                    "text": name,
                    "block_name": name,
                    "x": xv,
                    "y": yv,
                    "z": _num(buf.get("30")),
                    "layer": layer or None,
                    "rotation": _num(buf.get("50")) or 0.0,
                    "xscale": sx if sx is not None else 1.0,
                    "yscale": sy if sy is not None else 1.0,
                    "zscale": sz if sz is not None else 1.0,
                }
                ext = (_num(buf.get("210")), _num(buf.get("220")), _num(buf.get("230")))
                if any(v is not None for v in ext):
                    rec["extrusion"] = [ext[0] if ext[0] is not None else 0.0,
                                        ext[1] if ext[1] is not None else 0.0,
                                        ext[2] if ext[2] is not None else 1.0]
                bp = block_bases.get(name.upper())
                if bp:
                    rec["base_point"] = list(bp["base_point"])
                    rec["base_point_source"] = "block_header"
                else:
                    rec["base_point"] = None
                    rec["base_point_source"] = "missing_block_header"
                recs.append(rec)
        buf = {}
        mtext_parts = []

    with open(path, "r", errors="ignore", encoding="utf-8", newline=None) as fh:
        sec = ""
        it = iter(fh)
        for a, b in zip(it, it):
            try:
                code = a.strip()
                val = b.rstrip("\r\n")
            except Exception:
                continue
            if code == "0":
                if val == "SECTION":
                    # 不能置 None：紧随其后的 2/<段名> 依赖 kind=="SECTION" 才能
                    # 记录当前段。置 None 会让 sec 永远为空，DXF 的 INSERT 全部
                    # 被误判为“不在 ENTITIES 段”（2026-11-09 实测合成 DXF 复现）。
                    kind = "SECTION"
                    buf = {}
                    mtext_parts = []
                    continue
                flush()
                kind = val
                if val == "ENDSEC":
                    sec = ""
                if val in ("TEXT", "MTEXT", "ATTRIB", "ATTDEF", "INSERT", "BLOCK"):
                    buf = {"_kind": val}
                else:
                    buf = {}
            elif code == "2" and kind == "SECTION":
                sec = val
            elif code == "3" and buf.get("_kind") == "MTEXT":
                mtext_parts.append(val)
            elif code == "8" and val.strip():
                layers.add(val.strip())
                buf["8"] = val.strip()
            elif buf:
                buf[code] = val
            if len(recs) >= max_rows:
                notes.append(f"文字数达上限 {max_rows}，已截断")
                break
    flush()
    # 单遍解析兜底：非标准 DXF 可能把 ENTITIES 放在 BLOCKS 之前。扫描结束后只对
    # “缺块基点”的 INSERT 回填一次；找不到块头仍保持 null，不拿 (0,0) 冒充。
    for rec in recs:
        if rec.get("kind") != "INSERT" or rec.get("base_point") is not None:
            continue
        bp = block_bases.get(str(rec.get("block_name") or "").upper())
        if bp:
            rec["base_point"] = list(bp["base_point"])
            rec["base_point_source"] = "block_header_backfill"
    meta["block_refs"] = dict(blocks.most_common(40))
    meta["insert_count"] = sum(blocks.values())
    used_bases = {k: v for k, v in block_bases.items() if k in {n.upper() for n in blocks}}
    if used_bases:
        meta["block_bases"] = {
            v["name"]: list(v["base_point"])
            for _k, v in sorted(used_bases.items())[:2000]
        }
    log(f"  流式解析 DXF：文字 {len(recs)} 条 / 图层 {len(layers)} 个 / 块引用 {meta['insert_count']} 个")
    return recs, sorted(layers), notes, meta


def detect_format(head: bytes, suffix: str) -> str:
    if head[:2] == b"AC" and len(head) >= 6 and head[2:6].isdigit():
        return "DWG"
    if head.lstrip()[:4] == b"  0" or b"SECTION" in head or suffix in (".dxf", ".dwt"):
        return "DXF"
    return "DWG"


def _num(v):
    try:
        return float(v)
    except Exception:
        return None


# ---------------------------------------------------------------- 图框/几何
LIMIT = 1e8  # 超出此量级的坐标是解码脏值，一律丢弃


def sane(*vals):
    for v in vals:
        if v is None or not isinstance(v, (int, float)) or not math.isfinite(v) or abs(v) > LIMIT:
            return False
    return True


def _is_garble_name(name) -> bool:
    """粗略判定 DWG 块名是否解码乱码（高比例不可读字符，如 @`/€/燖 等）。"""
    if not name:
        return False
    upper = name.upper()
    # 纯 ASCII 可打印常见块名（字母数字、下划线、-、空格）
    if all((c.isascii() and c.isprintable() and (c.isalnum() or c in "_- .")) or c == " " for c in upper):
        return False
    import unicodedata
    readable = 0
    n = 0
    for ch in name:
        if ch.isspace():
            continue
        n += 1
        try:
            cat = unicodedata.category(ch)
        except Exception:
            cat = "Cn"
        if ch.isalnum() or cat in ("Lo", "Lm", "So"):
            readable += 1
    if n == 0:
        return False
    return readable / n < 0.55


def _safe_block_key(base: dict, raw_name: str) -> str:
    """乱码块名换成稳定占位 _BLK#N，避免污染 JSON/语义。"""
    if not _is_garble_name(raw_name):
        return str(raw_name or "").strip()
    i = len(base) + 1
    while f"_BLK#{i}" in base:
        i += 1
    return f"_BLK#{i}"


def _rc_in_roi(x, y, roi):
    """文字/插入点是否落在 ROI 内（roi=None 表示不限）。"""
    if roi is None:
        return True
    if x is None or y is None or not sane(x, y):
        return False
    x1, y1, x2, y2 = roi
    return x1 <= x <= x2 and y1 <= y <= y2


def _seg_in_roi(ax, ay, bx, by, roi):
    """线段是否与 ROI 有交集（用 AABB 判定，roi=None 表示不限）。"""
    if roi is None:
        return True
    if not sane(ax, ay, bx, by):
        return False
    x1, y1, x2, y2 = roi
    return not (min(ax, bx) > x2 or max(ax, bx) < x1 or
                min(ay, by) > y2 or max(ay, by) < y1)


FRAME_PAT = re.compile(r"图框|frame|边框|title|tlk|gb\s*a\d", re.I)


def frame_anchors(recs, min_count=2):
    """图框块的插入点通常在图框左下角，用它分图框比按空隙猜更准。"""
    seen = {}
    for r in recs:
        if r.get("kind") != "INSERT" or not r.get("text"):
            continue
        if not sane(r.get("x"), r.get("y")):
            continue
        if not FRAME_PAT.search(str(r["text"])):
            continue
        seen.setdefault((int(r["x"]), int(r["y"])), str(r["text"]))
    if len(seen) < min_count:
        return []
    return [(float(k[0]), float(k[1])) for k in seen]


def assign_sheets_by_frames(recs, anchors, min_texts=60):
    """文字归到"图框块插入点的右上侧、且在推算图幅内"的那个图框。

    图幅宽高取相邻图框块 X/Y 间距的中位数；命中率低于 45% 时返回 []，
    由调用方退回坐标空隙聚类，避免块定义区文字被远处的图框抢走。
    """
    try:
        import numpy as np
    except Exception:
        return []
    if not anchors:
        return []
    for r in recs:
        r["sheet"] = None
    xs = np.asarray([a[0] for a in anchors], float)
    ys = np.asarray([a[1] for a in anchors], float)

    def span(v):
        u = np.unique(np.round(v, 1))
        if u.size < 2:
            return 0.0
        d = np.diff(u)
        d = d[d > 1000.0]
        return float(np.median(d)) if d.size else 0.0

    w, h = span(xs), span(ys)
    if w <= 0 and h <= 0:
        return []
    w = w or h * 1.4
    h = h or w / 1.4
    idxs = [i for i, r in enumerate(recs) if sane(r.get("x"), r.get("y"))]
    if not idxs:
        return []
    PX = np.asarray([recs[i]["x"] for i in idxs], float)
    PY = np.asarray([recs[i]["y"] for i in idxs], float)
    out = np.full(len(idxs), -1, dtype=np.int64)
    CH = 2048
    for s in range(0, len(idxs), CH):
        px = PX[s:s + CH][:, None]
        py = PY[s:s + CH][:, None]
        ok = ((xs[None, :] <= px + 0.1 * w) & (ys[None, :] <= py + 0.1 * h) &
              (px - xs[None, :] <= 1.05 * w) & (py - ys[None, :] <= 1.05 * h))
        dist = np.where(ok, (px - xs[None, :]) + (py - ys[None, :]), np.inf)
        m = np.argmin(dist, axis=1)
        sel = np.nonzero(np.isfinite(dist[np.arange(m.size), m]))[0]
        out[s:s + CH][sel] = m[sel] + 1
    groups = {}
    for k, i in enumerate(idxs):
        if out[k] > 0:
            sid = int(out[k])
            recs[i]["sheet"] = sid
            groups.setdefault(sid, []).append((recs[i]["x"], recs[i]["y"]))
    hit = sum(len(v) for v in groups.values())
    if hit < 0.45 * len(idxs):
        return []
    for sid in [k for k, v in groups.items() if len(v) < min_texts]:
        groups.pop(sid, None)
        for r in recs:
            if r.get("sheet") == sid:
                r["sheet"] = None
    ordered = sorted(groups, key=lambda sid: (-max(p[1] for p in groups[sid]),
                                              min(p[0] for p in groups[sid])))
    remap = {old: new for new, old in enumerate(ordered, 1)}
    sheets = []
    for old in ordered:
        pts = groups[old]
        sheets.append({
            "id": remap[old],
            "texts": len(pts),
            "bbox": [min(p[0] for p in pts), min(p[1] for p in pts),
                     max(p[0] for p in pts), max(p[1] for p in pts)],
        })
        for r in recs:
            if r.get("sheet") == old:
                r["sheet"] = remap[old]
    return sheets


def assign_sheets(recs, bin_size=10000.0, min_texts=60):
    """按文字坐标做占据网格 + 8 邻接连通块，把一张 DWG 里的多个图框分开。

    返回 [{id, texts, bbox}]；每条记录加上 r["sheet"]（无坐标为 None）。
    """
    cells = {}
    for i, r in enumerate(recs):
        if not sane(r.get("x"), r.get("y")):
            r["sheet"] = None
            continue
        key = (int(r["x"] // bin_size), int(r["y"] // bin_size))
        cells.setdefault(key, []).append(i)
    seen = set()
    groups = []
    for key in cells:
        if key in seen:
            continue
        stack = [key]
        seen.add(key)
        comp = []
        while stack:
            cx, cy = stack.pop()
            comp.append((cx, cy))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nk = (cx + dx, cy + dy)
                    if nk in cells and nk not in seen:
                        seen.add(nk)
                        stack.append(nk)
        groups.append(comp)
    groups.sort(key=lambda g: -sum(len(cells[c]) for c in g))
    sheets = []
    for gid, comp in enumerate(groups):
        n = sum(len(cells[c]) for c in comp)
        if n < min_texts:
            for c in comp:
                for i in cells[c]:
                    recs[i]["sheet"] = None
            continue
        xs = [c[0] for c in comp]
        ys = [c[1] for c in comp]
        for c in comp:
            for i in cells[c]:
                recs[i]["sheet"] = gid
        sheets.append({"_gid": gid, "texts": n,
                       "bbox": [min(xs) * bin_size, min(ys) * bin_size,
                                (max(xs) + 1) * bin_size, (max(ys) + 1) * bin_size]})
    sheets.sort(key=lambda s: (-s["bbox"][3], s["bbox"][0]))
    old_to_new = {}
    for i, s in enumerate(sheets, 1):
        old_to_new[s["_gid"]] = i
        s["id"] = i
        s.pop("_gid", None)
    for r in recs:
        if r.get("sheet") is not None:
            r["sheet"] = old_to_new.get(r["sheet"], r["sheet"])
    return sheets


def geometry_segments(path, budget, log, include_layers=False, roi=None, max_rows=None):
    """解 LINE / LWPOLYLINE 成线段表；include_layers 时额外返回同名列表。

    roi 为 AABB；max_rows 为线段数上限，超限停止并记 note（大图保护，结果自动回退）。
    """
    notes = []
    segs = []
    seg_layers = [] if include_layers else None
    nline = 0
    stop = False
    for name in GEOM_KINDS:
        if stop:
            break
        rows = _rows(name, path, budget, notes) or []
        for r in rows:
            if stop:
                break
            c = r[2] if len(r) > 2 else None
            if not c:
                continue
            if name == "line":
                if len(c) >= 4 and sane(*c[:4]) and _seg_in_roi(c[0], c[1], c[2], c[3], roi):
                    segs.append((c[0], c[1], c[2], c[3]))
                    if include_layers:
                        seg_layers.append(str(r[3] or "") if len(r) > 3 else "")
                    nline += 1
                    if max_rows and nline >= max_rows:
                        notes.append(f"几何线段达上限 {max_rows}，已截断（大图回退近邻几何）")
                        stop = True
                        break
            else:
                pts = [(c[i], c[i + 1]) for i in range(0, len(c) - 1, 2)]
                pts = [p for p in pts if sane(*p)]
                for a, b in zip(pts, pts[1:]):
                    if stop:
                        break
                    if not _seg_in_roi(a[0], a[1], b[0], b[1], roi):
                        continue
                    segs.append((a[0], a[1], b[0], b[1]))
                    if include_layers:
                        seg_layers.append(str(r[3] or "") if len(r) > 3 else "")
                    nline += 1
                    if max_rows and nline >= max_rows:
                        notes.append(f"几何线段达上限 {max_rows}，已截断（大图回退近邻几何）")
                        stop = True
                        break
        log(f"{name} {len(rows)} 个对象")
    return (segs, seg_layers, notes) if include_layers else (segs, notes)


def circle_entities(path, budget, log, roi=None, min_radius=1.0, max_rows=None):
    """解 CIRCLE 成实体表 [x, y, r, layer]（市政井圈/池边等实体几何）。

    r < min_radius 的图元（图例符号、原点杂点）不进实体表；roi 为 AABB 时按
    圆心过滤。max_rows 上限防刷屏，超限记 note。这是块实体提取能力的第一步：
    匿名块（INSERT）名字多为解码乱码，语义不可得，本轮只提取圆，诚实记录边界。
    """
    notes: list[str] = []
    ents: list[list] = []
    rows = _rows("circle", path, budget, notes) or []
    for r in rows:
        c = r[2] if len(r) > 2 else None
        if not c or len(c) < 3:
            continue
        x, y, rad = c[0], c[1], c[2]
        if not isinstance(rad, (int, float)) or not math.isfinite(rad) or rad < min_radius:
            continue
        if not sane(x, y) or not _rc_in_roi(x, y, roi):
            continue
        ents.append([float(x), float(y), float(rad), str(r[3] or "") if len(r) > 3 else ""])
        if max_rows and len(ents) >= max_rows:
            notes.append(f"圆实体达上限 {max_rows}，已截断")
            break
    notes.append(f"圆实体 {len(ents)} 个（半径≥{min_radius:g}）")
    log(f"圆实体 {len(ents)} 个")
    return ents, notes


def dxf_circle_entities(path, budget=None, log=None, roi=None, min_radius=1.0,
                        max_rows=None):
    """流式提取 DXF ENTITIES 段的 CIRCLE，返回 [x, y, r, layer]。

    块定义里的 CIRCLE 不计入模型空间实体表；图例符号和原点杂点由调用方按
    min_radius/图层再过滤。这里只描述“图上确实画了一个圆”，不推断用途。
    """
    notes: list[str] = []
    ents: list[list] = []
    sec = ""
    kind = None
    buf: dict = {}

    def flush():
        if kind != "CIRCLE" or sec != "ENTITIES":
            return
        xv, yv, rv = _num(buf.get("10")), _num(buf.get("20")), _num(buf.get("40"))
        if rv is None or rv < min_radius or not sane(xv, yv, rv):
            return
        if not _rc_in_roi(xv, yv, roi):
            return
        ents.append([float(xv), float(yv), float(rv), str(buf.get("8") or "")])
        if max_rows and len(ents) >= max_rows:
            notes.append(f"圆实体达上限 {max_rows}，已截断")

    with open(path, "r", errors="ignore", encoding="utf-8", newline=None) as fh:
        it = iter(fh)
        for a, b in zip(it, it):
            code = a.strip()
            val = b.rstrip("\r\n")
            if code == "0":
                flush()
                kind = val
                buf = {}
                if max_rows and len(ents) >= max_rows:
                    break
            elif code == "2" and kind == "SECTION":
                sec = val
            elif kind == "CIRCLE" and code in ("8", "10", "20", "40"):
                buf[code] = val
    flush()
    notes.append(f"圆实体 {len(ents)} 个（半径≥{min_radius:g}）")
    if log:
        log(f"圆实体 {len(ents)} 个")
    return ents, notes


def dxf_geometry_stream(path, include_layers=False, roi=None, max_rows=None):
    """流式按 group code 扫 DXF 抓 LINE / LWPOLYLINE（ezdxf 读不了时的兜底）。

    为什么需要：LibreDWG 转出的 DXF 常缺 EOF tag、实体 handle 重复、图层名空，
    ezdxf.readfile 抛 DXFStructureError，连 recover.readfile 都救不了
    （实测 J-2#/J-3#4#6#7# 两张结构图因此几何全空，跨专业轴网核对做不了）。
    但这些文件里的 LINE 数据本身是完整的——按 0 组码切实体逐段读就能取到。
    """
    notes = []
    segs = []
    seg_layers = [] if include_layers else None
    kind = None
    buf = {}
    lw_pts: list[tuple[float, float]] = []

    def emit(seg):
        if not sane(*seg) or not _seg_in_roi(seg[0], seg[1], seg[2], seg[3], roi):
            return
        segs.append(seg)
        if include_layers:
            seg_layers.append(str(buf.get("8") or ""))

    def flush():
        nonlocal buf, lw_pts
        if kind == "LINE":
            x1, y1 = _num(buf.get("10")), _num(buf.get("20"))
            x2, y2 = _num(buf.get("11")), _num(buf.get("21"))
            if None not in (x1, y1, x2, y2):
                emit((float(x1), float(y1), float(x2), float(y2)))
        elif kind == "LWPOLYLINE" and len(lw_pts) >= 2:
            for a, b in zip(lw_pts, lw_pts[1:]):
                emit((a[0], a[1], b[0], b[1]))
        buf = {}
        lw_pts = []

    stop = False
    try:
        with open(path, "r", errors="ignore", encoding="utf-8", newline=None) as fh:
            it = iter(fh)
            for a, b in zip(it, it):
                if stop:
                    break
                code = a.strip()
                val = b.rstrip("\r\n")
                if code == "0":
                    flush()
                    kind = val.strip()
                    continue
                if kind == "LINE":
                    if code in ("10", "20", "11", "21", "8"):
                        buf[code] = val.strip()
                elif kind == "LWPOLYLINE":
                    if code == "10":
                        lw_pts.append([_num(val), None])
                    elif code == "20" and lw_pts and lw_pts[-1][1] is None:
                        lw_pts[-1][1] = _num(val)
                    elif code == "8":
                        buf[code] = val.strip()
                    if len(lw_pts) >= 4096:
                        lw_pts = [(p[0], p[1]) for p in lw_pts if p[1] is not None]
                if max_rows and len(segs) >= max_rows:
                    notes.append(f"几何线段达上限 {max_rows}，已截断（流式兜底扫描）")
                    stop = True
            flush()
    except Exception as exc:
        notes.append(f"流式 DXF 几何扫描失败：{type(exc).__name__} {exc}")
    notes.append(f"已改用流式 DXF 扫描（ezdxf 拒绝该文件）：线段 {len(segs)} 条")
    return (segs, seg_layers, notes) if include_layers else (segs, notes)


def dxf_geometry_segments(path, budget, log, include_layers=False, roi=None, max_rows=None):
    """用 ezdxf 从 DXF 模型空间取 LINE/LWPOLYLINE 线段。

    roi 为 AABB 过滤；max_rows 为线段数上限，超限停止并记 note（大图保护）。
    """
    notes = []
    segs = []
    seg_layers = [] if include_layers else None
    try:
        import ezdxf
    except Exception as exc:
        notes.append(f"DXF 几何解码不可用：{exc}")
        return (segs, seg_layers, notes) if include_layers else (segs, notes)
    stop = False
    try:
        with stage(budget) as dl:
            doc = ezdxf.readfile(str(path))
            for e in doc.modelspace():
                dl.check()
                if stop:
                    break
                try:
                    if e.dxftype() == "LINE":
                        s = e.dxf.start
                        t = e.dxf.end
                        if sane(float(s.x), float(s.y), float(t.x), float(t.y)) and                                 _seg_in_roi(float(s.x), float(s.y), float(t.x), float(t.y), roi):
                            segs.append((float(s.x), float(s.y), float(t.x), float(t.y)))
                            if include_layers:
                                seg_layers.append(str(e.dxf.layer or ""))
                            if max_rows and len(segs) >= max_rows:
                                notes.append(f"几何线段达上限 {max_rows}，已截断（大图回退近邻几何）")
                                stop = True
                                break
                    elif e.dxftype() == "LWPOLYLINE":
                        pts = [(float(p[0]), float(p[1])) for p in e.get_points("xy")]
                        for a, b in zip(pts, pts[1:]):
                            if stop:
                                break
                            if not sane(a[0], a[1], b[0], b[1]) or not _seg_in_roi(a[0], a[1], b[0], b[1], roi):
                                continue
                            segs.append((a[0], a[1], b[0], b[1]))
                            if include_layers:
                                seg_layers.append(str(e.dxf.layer or ""))
                            if max_rows and len(segs) >= max_rows:
                                notes.append(f"几何线段达上限 {max_rows}，已截断（大图回退近邻几何）")
                                stop = True
                                break
                except Exception:
                    continue
    except Exception as exc:
        notes.append(f"DXF 几何解码失败：{exc}")
        # ezdxf 严格模式读不了（缺 EOF / 重复 handle / 图层名空）时走流式兜底，
        # 否则这类图的几何全空，下游轴网核对会误判成「图上没有轴网」。
        s2, l2, n2 = dxf_geometry_stream(path, include_layers=include_layers,
                                         roi=roi, max_rows=max_rows)
        if s2:
            segs, notes = s2, notes + n2
            if include_layers:
                seg_layers = l2
    return (segs, seg_layers, notes) if include_layers else (segs, notes)


def dxf_block_geometries(path, budget, log, max_rows=None):
    """用 ezdxf 从 DXF 块定义提取几何指纹所需的线段。

    返回 {块名: {"segments": [(x1,y1,x2,y2), ...], "layers": [图层,...]}}。
    只处理 BLOCK 定义内的 LINE/LWPOLYLINE，不展开嵌套块，避免过度膨胀；
    max_rows 为全量段数上限，超限截断并 note（大图保护）。
    """
    notes = []
    out: dict[str, dict] = {}
    try:
        import ezdxf
    except Exception as exc:
        notes.append(f"DXF 块几何解码不可用：{exc}")
        return out, notes
    n_seg = 0
    stop = False
    try:
        with stage(budget) as dl:
            doc = ezdxf.readfile(str(path))
            for block in doc.blocks:
                dl.check()
                if stop:
                    break
                name = str(block.name or "").strip()
                if not name or name.startswith("*"):
                    continue
                segs = []
                layers = []
                for e in block:
                    dl.check()
                    if stop:
                        break
                    try:
                        if e.dxftype() == "LINE":
                            s, t = e.dxf.start, e.dxf.end
                            if sane(float(s.x), float(s.y), float(t.x), float(t.y)):
                                segs.append((float(s.x), float(s.y), float(t.x), float(t.y)))
                                layers.append(str(e.dxf.layer or ""))
                                n_seg += 1
                                if max_rows and n_seg >= max_rows:
                                    notes.append(f"DXF 块几何段数达上限 {max_rows}，已截断")
                                    stop = True
                        elif e.dxftype() == "LWPOLYLINE":
                            pts = [(float(p[0]), float(p[1])) for p in e.get_points("xy")]
                            for a, b in zip(pts, pts[1:]):
                                if stop:
                                    break
                                if sane(a[0], a[1], b[0], b[1]):
                                    segs.append((a[0], a[1], b[0], b[1]))
                                    layers.append(str(e.dxf.layer or ""))
                                    n_seg += 1
                                    if max_rows and n_seg >= max_rows:
                                        notes.append(f"DXF 块几何段数达上限 {max_rows}，已截断")
                                        stop = True
                    except Exception:
                        continue
                if segs:
                    out[name] = {"segments": segs, "layers": layers}
    except Exception as exc:
        notes.append(f"DXF 块几何解码失败：{exc}")
    return out, notes



# ---------------------------------------------------------------- 块几何展开（0.41.0）
# 土建 cad_geometry.py 原先自己 import ezdwg、展开 INSERT 并做二维仿射。
# 0.41.0 把这段能力收进 cad_scan：其他技能只消费本模块结果，不再各自解 DWG。
# 注意：这里保留旧实现的坐标口径和 max_depth=8；DXF 与 DWG 两条路都输出同一结构。
_STRUCT_MAX_DEPTH = 8
_IDENT_MATRIX = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _struct_insert_matrix(values) -> tuple[float, float, float, float, float, float]:
    """旧 cad_geometry._insert_matrix 的等价实现。

    values=(ix, iy, iz, sx, sy, sz, rotation_rad)。只保留二维仿射，z 不影响平面线段。
    """
    ix, iy, _iz, sx, sy, _sz, rot = [float(x) for x in values]
    return (sx * math.cos(rot), -sy * math.sin(rot),
            sx * math.sin(rot), sy * math.cos(rot), ix, iy)


def _struct_compose(a, b):
    return (a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[0] * b[4] + a[1] * b[5] + a[4],
            a[2] * b[4] + a[3] * b[5] + a[5])


def _struct_apply(pt, m):
    return (m[0] * pt[0] + m[1] * pt[1] + m[4],
            m[2] * pt[0] + m[3] * pt[1] + m[5])


def _struct_segment(handle, kind, a, b, layer="", source_block="MODELSPACE"):
    try:
        if not all(math.isfinite(float(v)) for v in tuple(a) + tuple(b)):
            return None
        if abs(float(a[0]) - float(b[0])) + abs(float(a[1]) - float(b[1])) < 1e-4:
            return None
    except (TypeError, ValueError):
        return None
    return {"handle": handle, "kind": kind,
            "geometry": [float(a[0]), float(a[1]), float(b[0]), float(b[1])],
            "layer": str(layer or ""), "source_block": source_block}


def _struct_block_record(name, base_point=None, insert=None, rotation_deg=None,
                         scale=None, layer=None, parent=None, handle=None, source="block_definition"):
    return {"type": "block", "block_name": str(name or ""), "name": str(name or ""),
            "base_point": list(base_point) if isinstance(base_point, (list, tuple)) else None,
            "insert": list(insert) if isinstance(insert, (list, tuple)) else None,
            "rotation": rotation_deg, "rotation_deg": rotation_deg,
            "scale": list(scale) if isinstance(scale, (list, tuple)) else None,
            "layer": layer, "parent": parent, "handle": handle, "source": source}


def _struct_units_from_insunits(value):
    table = {1: (25.4, "inch"), 2: (304.8, "foot"), 4: (1.0, "mm"),
             5: (10.0, "cm"), 6: (1000.0, "m")}
    try:
        return table.get(int(value or 0))
    except Exception:
        return None


def _dxf_expand_block_geometry(path, budget, log):
    """DXF 等价展开：模型空间直画实体 + 顶层 INSERT 的递归块展开。"""
    import ezdxf
    notes = []
    segments, blocks = [], []
    units = {"drawing_unit": None, "drawing_mm_per_unit": None, "source": "DXF $INSUNITS"}
    with stage(budget) as dl:
        doc = ezdxf.readfile(str(path))
        dl.check()
        unit_info = _struct_units_from_insunits(doc.header.get("$INSUNITS"))
        if unit_info:
            units["drawing_mm_per_unit"], units["drawing_unit"] = unit_info

        def ehandle(entity):
            raw = getattr(entity.dxf, "handle", None)
            if raw in (None, ""):
                return None
            try:
                return int(str(raw), 16)
            except Exception:
                return str(raw)

        def emit_entity(entity, matrix, source_block):
            typ = entity.dxftype()
            layer = str(getattr(entity.dxf, "layer", "") or "")
            handle = ehandle(entity)
            if typ == "LINE":
                s, t = entity.dxf.start, entity.dxf.end
                seg = _struct_segment(handle, "LINE",
                                      _struct_apply((float(s.x), float(s.y)), matrix),
                                      _struct_apply((float(t.x), float(t.y)), matrix),
                                      layer, source_block)
                if seg:
                    segments.append(seg)
                return 0
            if typ in ("LWPOLYLINE", "POLYLINE"):
                try:
                    if typ == "LWPOLYLINE":
                        pts = [(float(p[0]), float(p[1])) for p in entity.get_points("xy")]
                    else:
                        pts = [(float(v.dxf.location.x), float(v.dxf.location.y)) for v in entity.vertices]
                except Exception:
                    return 0
                n = 0
                for a, b in zip(pts, pts[1:]):
                    seg = _struct_segment(handle, typ,
                                          _struct_apply(a, matrix), _struct_apply(b, matrix),
                                          layer, source_block)
                    if seg:
                        segments.append(seg)
                        n += 1
                return n
            return 0

        # 旧实现先输出模型空间直画几何，再按顶层 INSERT 顺序展开块。
        direct = []
        top_inserts = []
        for entity in doc.modelspace():
            dl.check()
            if entity.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE"):
                direct.append(entity)
            elif entity.dxftype() in ("INSERT", "MINSERT"):
                top_inserts.append(entity)
        for entity in direct:
            emit_entity(entity, _IDENT_MATRIX, "MODELSPACE")

        block_by_name = {}
        for block in doc.blocks:
            name = str(block.name or "").strip()
            if not name or name.startswith("*"):
                continue
            record = getattr(getattr(block, "block_record", None), "dxf", None)
            block_dxf = getattr(getattr(block, "block", None), "dxf", None)
            # ezdxf 的块基点放在 BLOCK 实体上，BLOCK_RECORD 上只有句柄/名称；
            # 两处都取，避免把可得的基点误报成缺失。
            bp = getattr(block_dxf, "base_point", None) if block_dxf is not None else None
            bp2 = [float(bp[0]), float(bp[1])] if bp is not None else None
            block_by_name[name] = block
            blocks.append(_struct_block_record(name, base_point=bp2,
                                               handle=str(getattr(record, "handle", "") or "") or None,
                                               source="dxf_block_definition"))

        for top in top_inserts:
            name = str(getattr(top.dxf, "name", "") or "")
            if name not in block_by_name:
                notes.append(f"顶层块引用 {name or '<空名>'} 无同名块定义，已跳过")
                continue
            try:
                top_matrix = top.matrix44()
                m = (float(top_matrix.m11), float(top_matrix.m12),
                     float(top_matrix.m21), float(top_matrix.m22),
                     float(top_matrix.m41), float(top_matrix.m42))
            except Exception:
                # 没有 matrix44 时退回旧式二维矩阵。
                m = _struct_insert_matrix((top.dxf.insert.x, top.dxf.insert.y, 0,
                                           getattr(top.dxf, "xscale", 1.0), getattr(top.dxf, "yscale", 1.0), 1.0,
                                           math.radians(float(getattr(top.dxf, "rotation", 0.0) or 0.0))))
            blocks.append(_struct_block_record(
                name, insert=[float(top.dxf.insert.x), float(top.dxf.insert.y)],
                rotation_deg=float(getattr(top.dxf, "rotation", 0.0) or 0.0),
                scale=[float(getattr(top.dxf, "xscale", 1.0) or 1.0), float(getattr(top.dxf, "yscale", 1.0) or 1.0), 1.0],
                layer=str(getattr(top.dxf, "layer", "") or ""), handle=ehandle(top), source="dxf_top_insert"))
            stack = [(block_by_name[name], m, 0, name)]
            visited = set()
            while stack:
                block, matrix, depth, source_block = stack.pop()
                if block.name in visited or depth > _STRUCT_MAX_DEPTH:
                    continue
                visited.add(block.name)
                nested = []
                for entity in block:
                    dl.check()
                    if entity.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE"):
                        emit_entity(entity, matrix, source_block)
                    elif entity.dxftype() in ("INSERT", "MINSERT"):
                        nested.append(entity)
                for child in nested:
                    child_name = str(getattr(child.dxf, "name", "") or "")
                    if child_name not in block_by_name:
                        continue
                    try:
                        cm = child.matrix44()
                        local = (float(cm.m11), float(cm.m12), float(cm.m21), float(cm.m22),
                                 float(cm.m41), float(cm.m42))
                        child_matrix = _struct_compose(matrix, local)
                    except Exception:
                        child_matrix = _struct_compose(matrix, _struct_insert_matrix((
                            child.dxf.insert.x, child.dxf.insert.y, 0,
                            getattr(child.dxf, "xscale", 1.0), getattr(child.dxf, "yscale", 1.0), 1.0,
                            math.radians(float(getattr(child.dxf, "rotation", 0.0) or 0.0)))))
                    blocks.append(_struct_block_record(
                        child_name, insert=[float(child.dxf.insert.x), float(child.dxf.insert.y)],
                        rotation_deg=float(getattr(child.dxf, "rotation", 0.0) or 0.0),
                        scale=[float(getattr(child.dxf, "xscale", 1.0) or 1.0), float(getattr(child.dxf, "yscale", 1.0) or 1.0), 1.0],
                        layer=str(getattr(child.dxf, "layer", "") or ""), parent=source_block,
                        handle=ehandle(child), source="dxf_nested_insert"))
                    stack.append((block_by_name[child_name], child_matrix, depth + 1,
                                  f"{source_block}/{child_name}"))
    log(f"DXF 块几何展开：{len(segments)} 段，块记录 {len(blocks)} 条")
    return {"segments": segments, "blocks": blocks, "units": units, "notes": notes}


def _dwg_expand_block_geometry(path, budget, log):
    """DWG 等价展开：保留旧 cad_geometry.py 的 raw 解码与二维变换口径。

    这一步是能力上移，不修旧算法。旧行为要点：
      * 模型空间直画 LINE/LWPOLYLINE/POLYLINE_2D 原样输出；
      * 每个顶层 INSERT 独立 visited，嵌套同名块只走第一条路径；
      * max_depth=8；LWPOLYLINE 只连顶点、不展开 bulge、不补闭合边。
    """
    import ezdwg  # noqa: F401  (触发 C 扩展加载)
    from ezdwg import raw
    notes = []
    segments, blocks = [], []
    units = {"drawing_unit": None, "drawing_mm_per_unit": None, "source": "DWG 未声明"}
    try:
        with stage(budget):
            doc = ezdwg.read(path)
            lines = list(raw.decode_line_entities(path) or [])
            lwps = list(raw.decode_lwpolyline_entities(path) or [])
            pols = list(raw.decode_polyline_2d_with_vertices(path) or [])
            inserts = list(raw.decode_insert_entities(path) or [])

            layer_names = {}
            try:
                layer_names = {int(h): str(n or "") for h, n in (raw.decode_layer_names(path) or [])}
            except Exception:
                pass
            all_handles = [int(r[0]) for r in lines + lwps + pols + inserts if r and isinstance(r[0], int)]
            layer_by_handle = {}
            try:
                for ent_h, layer_h in raw.decode_object_entity_layer_handles(path, all_handles) or []:
                    layer_by_handle[int(ent_h)] = layer_names.get(int(layer_h), "")
            except Exception:
                pass

            block_by_name = {}
            for handle, name in raw.decode_block_header_names(path) or []:
                nm = str(name or "").strip()
                if nm and nm not in block_by_name:
                    block_by_name[nm] = int(handle)
                    blocks.append(_struct_block_record(nm, handle=handle, source="dwg_block_definition"))

            line_by_owner, lwp_by_owner, pol_by_owner = defaultdict(list), defaultdict(list), defaultdict(list)
            direct = []
            for kind, rows in (("LINE", lines), ("LWPOLYLINE", lwps), ("POLYLINE_2D", pols)):
                for row in rows:
                    try:
                        placement = doc.entity_placement(int(row[0]))
                    except Exception:
                        continue
                    if placement is None:
                        continue
                    if placement[0] == 0 and placement[1] is not None:
                        {"LINE": line_by_owner, "LWPOLYLINE": lwp_by_owner, "POLYLINE_2D": pol_by_owner}[kind][int(placement[1])].append(row)
                    elif placement[0] == 2:
                        direct.append((kind, row))
            insert_by_owner, top_inserts = defaultdict(list), []
            for row in inserts:
                try:
                    placement = doc.entity_placement(int(row[0]))
                except Exception:
                    continue
                if placement is None:
                    continue
                if placement[0] == 0 and placement[1] is not None:
                    insert_by_owner[int(placement[1])].append(row)
                elif placement[0] == 2:
                    nm = str(row[-1] or "")
                    if nm in block_by_name:
                        top_inserts.append((row, block_by_name[nm]))

            def emit(kind, row, matrix, source_block="MODELSPACE"):
                try:
                    handle = int(row[0])
                except Exception:
                    handle = row[0]
                layer = layer_by_handle.get(int(row[0]), "") if isinstance(row[0], int) else ""
                if kind == "LINE":
                    seg = _struct_segment(handle, kind,
                                          _struct_apply((float(row[1]), float(row[2])), matrix),
                                          _struct_apply((float(row[4]), float(row[5])), matrix),
                                          layer, source_block)
                    if seg:
                        segments.append(seg)
                    return
                pts = row[2]
                if kind == "POLYLINE_2D":
                    pts = [(float(p[0]), float(p[1])) for p in pts]
                for i in range(1, len(pts)):
                    seg = _struct_segment(handle, kind,
                                          _struct_apply((float(pts[i - 1][0]), float(pts[i - 1][1])), matrix),
                                          _struct_apply((float(pts[i][0]), float(pts[i][1])), matrix),
                                          layer, source_block)
                    if seg:
                        segments.append(seg)

            for kind, row in direct:
                emit(kind, row, _IDENT_MATRIX)

            for row, block_handle in top_inserts:
                top_name = str(row[-1] or "BLOCK")
                try:
                    m = _struct_insert_matrix(row[1:8])
                    blocks.append(_struct_block_record(
                        top_name, insert=[float(row[1]), float(row[2])],
                        rotation_deg=math.degrees(float(row[7])),
                        scale=[float(row[4]), float(row[5]), float(row[6])],
                        layer=layer_by_handle.get(int(row[0]), ""),
                        handle=int(row[0]), source="dwg_top_insert"))
                except Exception:
                    continue
                stack = [(block_handle, m, 0, top_name)]
                visited = set()
                while stack:
                    owner, matrix, depth, source_block = stack.pop()
                    if owner in visited or depth > _STRUCT_MAX_DEPTH:
                        continue
                    visited.add(owner)
                    for kind, group in (("LINE", line_by_owner), ("LWPOLYLINE", lwp_by_owner),
                                        ("POLYLINE_2D", pol_by_owner)):
                        for entity_row in group.get(owner, []):
                            emit(kind, entity_row, matrix, source_block)
                    for nested in insert_by_owner.get(owner, []):
                        nm = str(nested[-1] or "")
                        if nm not in block_by_name:
                            continue
                        try:
                            local = _struct_insert_matrix(nested[1:8])
                            blocks.append(_struct_block_record(
                                nm, insert=[float(nested[1]), float(nested[2])],
                                rotation_deg=math.degrees(float(nested[7])),
                                scale=[float(nested[4]), float(nested[5]), float(nested[6])],
                                layer=layer_by_handle.get(int(nested[0]), ""),
                                parent=source_block, handle=int(nested[0]),
                                source="dwg_nested_insert"))
                        except Exception:
                            local = _IDENT_MATRIX
                        stack.append((block_by_name[nm], _struct_compose(matrix, local),
                                      depth + 1, f"{source_block}/{nm}"))
            if not blocks:
                notes.append("DWG 未解出块定义/块引用；只输出模型空间直画几何")
            if not segments:
                notes.append("DWG 块几何展开为空；请用 --with-geom 查看模型空间几何")
    except Exception as exc:
        notes.append(f"DWG 块几何展开失败：{type(exc).__name__}: {exc}")
    log(f"DWG 块几何展开：{len(segments)} 段，块记录 {len(blocks)} 条")
    return {"segments": segments, "blocks": blocks, "units": units, "notes": notes}


def expand_block_geometry(path, budget: float = 60.0, log=None):
    """统一入口：展开 DWG/DXF 模型空间直画实体与 INSERT 块几何。

    返回 {"segments":[{handle,kind,geometry,layer,source_block}], "blocks":[...],
          "units":{...}, "notes":[...]}。
    只出几何候选；不识别构件、不算量，也不改变旧技能的坐标口径。
    """
    log = log or (lambda _msg: None)
    suffix = Path(str(path)).suffix.lower()
    if suffix == ".dxf":
        return _dxf_expand_block_geometry(path, budget, log)
    if suffix == ".dwg":
        return _dwg_expand_block_geometry(path, budget, log)
    return {"segments": [], "blocks": [],
            "units": {"drawing_unit": None, "drawing_mm_per_unit": None, "source": "unsupported"},
            "notes": [f"不支持的块几何输入格式：{suffix or '<none>'}"]}

def _dwg_entity_lines_by_handle(path, budget, notes, roi=None, max_rows=None):
    """DWG 只解 LINE/LWPOLYLINE，返回 {实体句柄: (线段列表, 图层集合)}。

    复用 _rows 的子进程+预算机制；line 一条一条，lwpoly 摊成线段，
    与 dxf_block_geometries 的 “segments” 口径一致；roi 过滤、max_rows 截断。
    """
    out: dict[int, tuple[list, set]] = {}
    total_seg = 0
    stop = False
    try:
        line_budget = max(4.0, budget * 0.6)
        for name in ("line", "lwpoly"):
            if stop:
                break
            rows = _rows(name, path, line_budget, notes) or []
            for r in rows:
                if stop:
                    break
                if not isinstance(r, (list, tuple)) or len(r) < 4:
                    continue
                try:
                    h = int(r[0])
                except Exception:
                    continue
                segs: list = []
                layer = str(r[3] or "") if len(r) > 3 else ""
                if name == "line":
                    c = r[2] if len(r) > 2 and isinstance(r[2], (list, tuple)) else None
                    if c and len(c) >= 4 and sane(float(c[0]), float(c[1]), float(c[2]), float(c[3])) and                             _seg_in_roi(float(c[0]), float(c[1]), float(c[2]), float(c[3]), roi):
                        segs.append((float(c[0]), float(c[1]), float(c[2]), float(c[3])))
                else:
                    c = r[2] if len(r) > 2 and isinstance(r[2], (list, tuple)) else None
                    pts = []
                    if c:
                        pts = [(float(c[i]), float(c[i + 1])) for i in range(0, len(c) - 1, 2)
                               if sane(float(c[i]), float(c[i + 1]))]
                    for a, b in zip(pts, pts[1:]):
                        if stop:
                            break
                        if not _seg_in_roi(a[0], a[1], b[0], b[1], roi):
                            continue
                        segs.append((a[0], a[1], b[0], b[1]))
                if not segs:
                    continue
                cur = out.setdefault(h, ([], set()))
                cur[0].extend(segs)
                if layer:
                    cur[1].add(layer)
                total_seg += len(segs)
                if max_rows and total_seg >= max_rows:
                    notes.append(f"DWG 块几何实体段数达上限 {max_rows}，已截断（回退近邻几何）")
                    stop = True
    except Exception as exc:
        notes.append(f"DWG 块几何实体解码异常：{exc}")
    return out


def _build_dwg_block_geometries(block_rows, placement_rows, geom_rows, max_blocks=200):
    """纯逻辑组装块定义内部几何（不触盘，便于单测）。

    block_rows:   blocks worker 行 [handle, name]
    placement_rows: placements worker 行 [handle, mode, owner]
    geom_rows:    _dwg_entity_lines_by_handle 的输出
    返回 (out, notes)；out 结构与 dxf_block_geometries 一致。
    """
    notes: list[str] = []
    block_by_handle: dict[int, str] = {}
    for r in block_rows or []:
        try:
            h = int(r[0])
        except Exception:
            continue
        name = str(r[1] or "").strip()
        if h and name and not name.startswith("*") and h not in block_by_handle:
            if _is_garble_name(name):
                notes.append(f"块名疑似乱码，已用 {_safe_block_key(block_by_handle, name)} 占位（块句柄 {h}），建议转 DXF 复核原文块名")
            block_by_handle[h] = _safe_block_key(block_by_handle, name)
    if not block_by_handle:
        notes.append("DWG 未解出命名块定义；回退近邻几何")
        return {}, notes

    owner_by_handle: dict[int, int] = {}
    for r in placement_rows or []:
        try:
            owner_by_handle[int(r[0])] = int(r[2])
        except Exception:
            continue
    if not owner_by_handle:
        notes.append("DWG 实体归属表未解出；回退近邻几何")

    out: dict[str, dict] = {}
    for blk_handle, name in block_by_handle.items():
        if len(out) >= max_blocks:
            notes.append(f"块定义超过 {max_blocks} 个，已截断")
            break
        segs: list = []
        layers: set = set()
        for eh, (esegs, elayers) in (geom_rows or {}).items():
            if owner_by_handle.get(eh) != blk_handle:
                continue
            segs.extend(esegs)
            layers.update(elayers)
        if segs:
            out[name] = {"segments": segs[:4000], "layers": sorted(layers)[:200]}
    if not out:
        notes.append("DWG 命名块内未取到 LINE/LWPOLYLINE 几何；回退近邻几何")
    return out, notes


def dwg_block_geometries(path, budget, log, max_blocks=200, geom_budget=None, geom_max_rows=None, roi=None):
    """DWG 短预算块内几何试探：在预算内解块名 + 实体归属 + LINE/LWPOLY。

    超时/缺数据/超过段数上限时只给 note，由上层回退近邻几何，绝不阻塞整张图。
    返回与 dxf_block_geometries 一致： {块名: {"segments": [...], "layers": [...]}}
    """
    notes: list[str] = []
    place_budget = max(4.0, min(20.0, budget * 0.3))
    block_rows = _rows("blocks", path, min(8.0, budget), notes) or []
    placement_rows = _rows("placements", path, place_budget, notes) or []
    geom_budget = geom_budget if geom_budget and geom_budget > 0 else max(8.0, budget * 0.6)
    geom_rows = _dwg_entity_lines_by_handle(path, geom_budget, notes, roi=roi, max_rows=geom_max_rows)
    out, build_notes = _build_dwg_block_geometries(block_rows, placement_rows, geom_rows, max_blocks=max_blocks)
    notes += build_notes
    log(f"DWG 块几何试探：命名块 {len({str(r[1]) for r in block_rows if r and len(r) > 1})} 个，命中 {len(out)} 个")
    return out, notes


def _merge_intervals(iv):
    iv = sorted(iv)
    out = [list(iv[0])]
    for a, b in iv[1:]:
        if a - out[-1][1] <= 200:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def estimate_beam_lengths(res, seg_files, radius=3000.0):
    """[推测] 对每个带截面的梁标注点，取就近共线线段合并长度作为该处梁长。

    seg_files: 按文件分组的线段表 [[(x1,y1,x2,y2), ...], ...]，避免跨文件坐标串台。
    """
    try:
        import numpy as np
    except Exception:
        res["meta"]["geom_note"] = "环境缺少 numpy，跳过梁长估算"
        return
    pts = []
    for code, d in (res["members"].get("梁") or {}).items():
        for b in d["buckets"].values():
            if b.get("size") and sane(b.get("x"), b.get("y")):
                pts.append((code, b.get("file") or 0, b["x"], b["y"]))
    if not pts:
        return
    arrs = {}
    for fi in {p[1] for p in pts}:
        segs = seg_files[fi] if fi < len(seg_files) else []
        if not segs:
            continue
        S = np.asarray(segs, float)
        if S.ndim != 2 or S.shape[1] < 4:
            continue
        mx = (S[:, 0] + S[:, 2]) / 2.0
        my = (S[:, 1] + S[:, 3]) / 2.0
        ang = np.degrees(np.arctan2(S[:, 3] - S[:, 1], S[:, 2] - S[:, 0])) % 180.0
        ln = np.hypot(S[:, 2] - S[:, 0], S[:, 3] - S[:, 1])
        arrs[fi] = (S, mx, my, ang, ln)
    res["meta"]["geom_files"] = len(arrs)
    per = defaultdict(list)
    miss = 0
    for code, fi, x, y in pts:
        if fi not in arrs:
            miss += 1
            continue
        S, mx, my, ang, ln = arrs[fi]
        idx = np.nonzero(np.hypot(mx - x, my - y) <= radius)[0]
        idx = idx[ln[idx] > 500]
        if idx.size == 0:
            miss += 1
            continue
        base = idx[np.argmax(ln[idx])]
        a0 = ang[base]
        near = idx[np.abs(((ang[idx] - a0 + 90.0) % 180.0) - 90.0) <= 3.0]
        u = (math.cos(math.radians(a0)), math.sin(math.radians(a0)))
        iv = []
        for i in near:
            p1 = (S[i, 0] - x) * u[0] + (S[i, 1] - y) * u[1]
            p2 = (S[i, 2] - x) * u[0] + (S[i, 3] - y) * u[1]
            iv.append([min(p1, p2), max(p1, p2)])
        merged = _merge_intervals(iv)
        best = max(merged, key=lambda z: z[1] - z[0])
        per[code].append(best[1] - best[0])
    for code, lens in per.items():
        d = res["members"]["梁"][code]
        d["len_mm"] = int(round(sum(lens)))
        d["len_n"] = len(lens)
        d["len_max"] = int(round(max(lens)))
    res["meta"]["geom_radius"] = radius
    res["meta"]["geom_points"] = len(pts) - miss
    if miss:
        res["meta"]["geom_miss"] = miss


# ---------------------------------------------------------------- 分析
def cluster_records(recs, step: float):
    """把同一网格内的文字按位置合并，用于还原平法“集中标注 + 原位标注”。"""
    if step <= 0:
        return recs
    import math
    buckets = defaultdict(list)
    for r in recs:
        if not (isinstance(r.get("x"), float) and isinstance(r.get("y"), float)
                and math.isfinite(r["x"]) and math.isfinite(r["y"])):
            buckets[(10**9, 10**9)].append(r)
            continue
        buckets[(int(r["x"] // step), int(r["y"] // step))].append(r)
    out = []
    for key, group in buckets.items():
        if len(group) == 1:
            out.append(group[0])
            continue
        text = "  ".join((g["text"] or "").strip() for g in group if (g["text"] or "").strip())
        out.append({"kind": "CLUSTER", "text": text, "x": key[0] * step, "y": key[1] * step,
                    "sheet": group[0].get("sheet"), "file": group[0].get("file")})
    return out


def _spec_add(spec, spec_src, item, val, r):
    spec[item][val] += 1
    f = r.get("file")
    spec_src[item][val].add("" if f is None else str(f))


def stirrup_of(d):
    # 箍筋还原成 III6@200(2) 形式
    if not d.get("gd"):
        return ""
    s = "%s%s@%s" % (d.get("gl", ""), d["gd"], d["gp"])
    if d.get("ga"):
        s += "/" + d["ga"]
    if d.get("ge"):
        s += "(%s)" % d["ge"]
    return s


def size_key(x):
    return (x.startswith("h="), x)


def new_slot():
    return {"count": 0, "sizes": set(), "raws": [], "rebar": set(), "buckets": {}, "sheets": set(),
            "span": "", "cant": "", "w": "", "ht": "", "b": "", "h": "",
            "gl": "", "gd": "", "gp": "", "ga": "", "ge": "",
            "lt": Counter(), "note": "",
            "l_cnt": "", "l_txt": "", "l_dia": ""}


def angle_bucket(rotation: float, bucket_deg: float = 5.0) -> int | None:
    """把旋转角归一到 0-180° 后按 bucket_deg 分桶；缺失返回 None。"""
    if not isinstance(rotation, (int, float)) or not math.isfinite(float(rotation)):
        return None
    deg = float(rotation) % 180.0
    return int(deg // max(1e-9, float(bucket_deg)))


def analyse(recs, layers, meta, keep=None, dedupe=1500.0, count_by="auto"):
    """按文字规则识别构件编号。

    三种计数口径同时算出来：
      count   原文次数      —— 同一段文字出现几次（会重复计，最多）
      pos_n   标注位置数    —— 同一图框内同一位置只算一次
      sized_n 含截面/板厚数 —— 该位置的原文里带 b×h 或 h=（平法"集中标注"），最接近根数
    """
    by_cat = defaultdict(lambda: defaultdict(new_slot))
    conc = Counter()
    thk = Counter()
    spec = defaultdict(Counter)
    spec_src = defaultdict(lambda: defaultdict(set))
    keyword_rows = []
    hits = []
    practices = []
    seen_practices = set()
    for n, r in enumerate(recs):
        if r["kind"] == "INSERT":
            continue
        t = normalize((r["text"] or "")).strip()
        if not t or not readable(t):
            continue
        for p in extract_practices(t, r.get("file"), r.get("sheet"), r.get("layer")):
            key = (p["part"], p["text"])
            if key not in seen_practices:
                seen_practices.add(key)
                practices.append(p)
        x, y = r.get("x"), r.get("y")
        ab = angle_bucket(r.get("rotation"), bucket_deg=5.0)
        if sane(x, y):
            bk = (r.get("file"), r.get("sheet"), int(x // dedupe), int(y // dedupe), ab)
        else:
            bk = ("@", n, ab)
        sized = False
        for cat, pat in CODE_PATTERNS:
            for m in pat.finditer(t):
                head_ = m.group(1).upper()
                num = m.group(3) if cat == "门窗" else (m.group(2) or "").upper()
                span_val = cant_val = wd = hg = ""
                if cat == "门窗":
                    try:
                        wi, hi = int(num[:2]) * 100, int(num[2:]) * 100
                    except ValueError:
                        wi = hi = 0
                    if not (600 <= hi <= 3900 and 300 <= wi <= 12000):
                        continue  # 尺寸不像洞口，按误命中丢弃
                    code = head_ + (m.group(2) or "") + num + (m.group(4) or "").upper()
                    wd, hg = str(wi), str(hi)
                    span_ = ""
                else:
                    code = ("板" + num) if head_ == "板" else (head_ + num)
                    try:
                        span_ = (m.group(3) or "").replace(" ", "")
                    except IndexError:
                        span_ = ""
                    if cat == "梁" and span_.startswith("("):
                        spm = SPAN.search(span_)
                        if spm:
                            span_val = spm.group(1)
                            cant_val = {"A": "一端悬挑", "B": "两端悬挑"}.get(spm.group(2) or "", "")
                if span_:
                    code += span_
                slot = by_cat[cat][code]
                slot["count"] += 1
                if span_val and not slot["span"]:
                    slot["span"], slot["cant"] = span_val, cant_val
                if wd:
                    if not slot["w"]:
                        slot["w"], slot["ht"] = wd, hg
                    slot["sizes"].add(wd + "x" + hg)
                if cat == "门窗" and head_ in ("M", "C") and not slot["note"]:
                    slot["note"] = "单字母前缀，需人工核对"
                b = slot["buckets"].get(bk)
                if b is None:
                    b = {"size": False, "x": x, "y": y, "file": r.get("file") or 0}
                    slot["buckets"][bk] = b
                if r.get("sheet"):
                    slot["sheets"].add(r["sheet"])
                sz = SIZE.search(t)
                if sz:
                    slot["sizes"].add(f"{sz.group(1)}x{sz.group(2)}")
                    b["size"] = True
                    sized = True
                sb = SEC_BH.search(t)
                if sb and not slot["b"]:
                    slot["b"], slot["h"] = sb.group(1), sb.group(2)
                sti = STIRRUP.search(t)
                if sti and not slot["gd"]:
                    slot["gl"], slot["gd"], slot["gp"] = sti.group(1) or "", sti.group(2), sti.group(3)
                    slot["ga"], slot["ge"] = sti.group(4) or "", sti.group(5) or ""
                lq = LONGIT_SEQ.search(t)
                if lq:
                    txt = re.sub(r"\s+", "", lq.group(1))
                    if sum(int(a) for a, _s, _d in LONGIT_ONE.findall(txt)):
                        slot["lt"][txt] += 1
                th = SLAB_THK.search(t)
                if th:
                    slot["sizes"].add("h=" + th.group(1))
                    b["size"] = True
                    sized = True
                for rb in REBAR.finditer(t):
                    slot["rebar"].add(re.sub(r"\s+", "", rb.group(0)))
                if len(slot["raws"]) < 3:
                    slot["raws"].append(t[:120])
                hits.append({"cat": cat, "code": code, "raw": t[:160], "x": x, "y": y,
                             "sheet": r.get("sheet"), "file": r.get("file"),
                             "kind": r["kind"]})
        for c in CONC.findall(t):
            conc[c.upper()] += 1
            _spec_add(spec, spec_src, "混凝土等级", c.upper(), r)
        th_ = SLAB_THK.search(t)
        if th_:
            thk[th_.group(1)] += 1
            _spec_add(spec, spec_src, "板厚", th_.group(1) + "mm", r)
        cv = COVER.search(t)
        if cv:
            _spec_add(spec, spec_src, "保护层", cv.group(1) + "mm", r)
        sv = SEISMIC.search(t)
        if sv:
            _spec_add(spec, spec_src, "抗震等级", sv.group(1), r)
        if keep and keep.search(t):
            keyword_rows.append({"kind": r["kind"], "text": t, "x": r["x"], "y": r["y"],
                                 "file": r.get("file"), "sheet": r.get("sheet"),
                                 "layer": r.get("layer")})
        _ = sized

    def est_of(d):
        pos_n = len(d["buckets"])
        sized_n = sum(1 for b in d["buckets"].values() if b.get("size"))
        if count_by == "raw":
            est, basis = d["count"], "原文次数"
        elif count_by == "pos":
            est, basis = pos_n, "标注位置"
        elif count_by == "label":
            est, basis = (sized_n, "集中标注") if sized_n else (pos_n, "标注位置")
        else:
            est, basis = (sized_n, "集中标注") if sized_n else (pos_n, "标注位置")
        return pos_n, sized_n, est, basis

    # 同编号梁：标了跨数的行把跨数/悬挑回填给只写编号的行
    annotated = defaultdict(list)
    for code, d in (by_cat.get("梁") or {}).items():
        sm = SPAN.search(code)
        if sm:
            annotated[code[:sm.start()]].append(d)
    for code, d in (by_cat.get("梁") or {}).items():
        if not d["span"]:
            for sib in annotated.get(code, []):
                if sib["span"]:
                    d["span"], d["cant"] = sib["span"], sib["cant"]
                    d["span_note"] = "同编号并入"
                    break
    members = {}
    for cat, v in by_cat.items():
        for code, d in v.items():
            pos_n, sized_n, est, basis = est_of(d)
            d["pos_n"], d["sized_n"], d["est"], d["basis"] = pos_n, sized_n, est, basis
            d["sheet_n"] = len(d["sheets"])
            if d["lt"]:
                d["l_txt"] = d["lt"].most_common(1)[0][0]
                ones = LONGIT_ONE.findall(d["l_txt"])
                d["l_cnt"] = sum(int(a) for a, _s, _d in ones)
                d["l_dia"] = "/".join(sorted(set(g for _a, _s, g in ones), key=int))
        members[cat] = dict(sorted(v.items(), key=lambda kv: (-kv[1]["est"], -kv[1]["count"], kv[0])))

    rebar_agg: dict[str, dict[str, list]] = {"箍筋": {}, "纵筋": {}}
    for cat in ("梁", "柱"):
        for code, d in members.get(cat, {}).items():
            s = stirrup_of(d)
            if s:
                a = rebar_agg["箍筋"].setdefault(s, [0, 0, set()])
                a[0] += 1
                a[1] += d["est"]
                a[2].add(code)
            ltxt = d.get("l_txt", "")
            if ltxt:
                a = rebar_agg["纵筋"].setdefault(ltxt, [0, 0, set()])
                a[0] += 1
                a[1] += d["est"]
                a[2].add(code)
    rebar_summary = {
        k: [
            {"型号": model, "构件型数": n, "估算根数": est,
             "构件编号": "、".join(sorted(codes)[:8])}
            for model, (n, est, codes) in sorted(v.items(), key=lambda kv: (-kv[1][1], kv[0]))
        ]
        for k, v in rebar_agg.items()
    }

    return {
        "spec": {k: dict(v.most_common()) for k, v in spec.items()},
        "spec_src": {k: {val: sorted(s) for val, s in v.items()} for k, v in spec_src.items()},
        "door_layer": [x for x in layers if DOOR_LAYER.search(x)][:10],
        "members": members,
        "concrete": dict(conc.most_common()),
        "slab_thk": dict(thk.most_common()),
        "rebar_summary": rebar_summary,
        "practices": practices[:500],
        "layers": layers,
        "meta": meta,
        "text_total": len(recs),
        "keyword_rows": keyword_rows,
        "hits": hits,
    }


# ---------------------------------------------------------------- 输出
MD_COLS = {
    "梁": ["编号", "标注跨数", "悬挑", "截面b×h", "箍筋", "纵筋", "纵筋根数", "纵筋直径",
           "根数估计", "依据", "标注位置数", "含截面数", "原文次数", "图框数",
           "梁线候选合计(m)", "单根均长(m)", "原文示例"],
    "柱": ["编号", "截面b×h", "箍筋", "纵筋", "纵筋根数", "纵筋直径",
           "根数估计", "依据", "标注位置数", "含截面数", "原文次数", "图框数", "原文示例"],
    "门窗": ["编号", "洞口宽×高(mm)", "数量估计", "依据", "标注位置数", "原文次数", "图框数", "备注", "原文示例"],
    "_": ["编号", "根数估计", "依据", "标注位置数", "含截面数", "原文次数", "图框数",
          "截面/尺寸", "配筋片段", "原文示例"],
}
CAT_UNIT = {"梁": "根", "板": "块", "柱": "根", "墙": "片", "基础": "个", "门窗": "个"}


def bh_of(d):
    return "%sx%s" % (d["b"], d["h"]) if d.get("b") and d.get("h") else ""


def md_cells(cat, code, d):
    raw = (d["raws"][0] if d["raws"] else "").replace("|", "/")[:60]
    if cat == "梁":
        ln = round(d["len_mm"] / 1000.0, 1) if d.get("len_mm") else ""
        avg = round(d["len_mm"] / 1000.0 / d["len_n"], 1) if d.get("len_mm") and d.get("len_n") else ""
        sp = d.get("span", "")
        if d.get("span_note"):
            sp = sp + chr(0x203b) if sp else ""
        return [code, sp, d.get("cant", ""), bh_of(d), stirrup_of(d), d.get("l_txt", ""),
                d.get("l_cnt", ""), d.get("l_dia", ""), d["est"], d["basis"], d["pos_n"],
                d["sized_n"], d["count"], d.get("sheet_n") or "", ln, avg, raw]
    if cat == "柱":
        return [code, bh_of(d), stirrup_of(d), d.get("l_txt", ""),
                d.get("l_cnt", ""), d.get("l_dia", ""), d["est"], d["basis"], d["pos_n"],
                d["sized_n"], d["count"], d.get("sheet_n") or "", raw]
    if cat == "门窗":
        return [code, "%sx%s" % (d["w"], d["ht"]) if d.get("w") else "", d["est"], d["basis"],
                d["pos_n"], d["count"], d.get("sheet_n") or "", d.get("note", ""), raw]
    return [code, d["est"], d["basis"], d["pos_n"], d["sized_n"], d["count"],
            d.get("sheet_n") or "", "、".join(sorted(d["sizes"], key=size_key)),
            "、".join(sorted(d["rebar"])[:3]), raw]


def spec_rows(res, files):
    name_of = dict((i, f["name"]) for i, f in enumerate(files))
    sp = res.get("spec") or {}
    order = [x for x in SPEC_ORDER if x in sp] + [x for x in sp if x not in SPEC_ORDER]
    rows = []
    for k in order:
        for val, cnt in list(sp[k].items()):
            src = (res.get("spec_src") or {}).get(k, {}).get(val, [])
            names = [name_of.get(int(i), "") for i in src[:3] if i != ""]
            rows.append([k, val, cnt, len([x for x in src if x != ""]), "；".join(n for n in names if n)])
    return rows


SPEC_CSV_HEAD = ["项目", "数值", "出现次数", "出处文件数", "出处文件"]


def to_md(res, files):
    o = io.StringIO()
    o.write("# CAD 图纸解析结果\n\n")
    o.write("| 文件 | 格式 | 文字数 | 图层数 | 耗时 | 峰值内存 |\n|---|---|---|---|---|---|\n")
    for f in files:
        o.write(f"| {f['name']} | {f['fmt']} | {f['texts']} | {f['layers']} | {f['secs']}s | {f['rss']}MB |\n")
    sheets = res["meta"].get("sheets") or []
    if len(sheets) > 1:
        o.write(f"\n**自动分图框**：识别出 {len(sheets)} 个图框（同一编号在同一图框内只计一次）\n\n")
        o.write("| 图框 | 文字数 | 坐标范围 X / Y |\n|---|---|---|\n")
        for s in sheets[:40]:
            b = s["bbox"]
            o.write(f"| {s['id']} | {s['texts']} | {int(b[0])}~{int(b[2])} / {int(b[1])}~{int(b[3])} |\n")
    if res["meta"].get("geom_note"):
        o.write("\n[提示] " + res["meta"]["geom_note"] + "\n")
    if res["concrete"]:
        o.write("\n**混凝土等级**：" + "、".join(f"{k}×{v}" for k, v in res["concrete"].items()) + "\n")
    if res["slab_thk"]:
        o.write("\n**板厚候选**：" + "、".join(f"{k}mm×{v}" for k, v in res["slab_thk"].items()) + "\n")
    for cat in ("梁", "板", "柱", "墙", "基础", "门窗"):
        items = res["members"].get(cat)
        if not items:
            continue
        total = sum(d["est"] for d in items.values())
        cols = MD_COLS.get(cat, MD_COLS["_"])
        if cat == "门窗":
            dl = res.get("door_layer") or []
            o.write("\n" + ("[提示] 本图门窗图层：" + "、".join(dl) if dl else
                                 "[提示] 本图未找到门窗图层，门窗编号可能混入预埋件等标注，务必人工核对"))
        if cat == "梁" and any(d.get("span_note") for d in items.values()):
            o.write("\n[提示] 跨数后的 ※ 表示该编号另有标了跨数的图面位置，跨数按同编号借用。\n")
        unit = CAT_UNIT.get(cat, "处")
        o.write(f"\n## {cat}（{len(items)} 种编号 / 合计约 {total} {unit}）\n\n")
        o.write("| " + " | ".join(cols) + " |\n")
        o.write("|" + "---|" * len(cols) + "\n")
        for code, d in list(items.items()):
            cells = [str(c) if c != "" else "-" for c in md_cells(cat, code, d)]
            o.write("| " + " | ".join(cells) + " |\n")
    if res.get("rebar_summary") and any(res["rebar_summary"].values()):
        o.write("\n## 钢筋型号汇总 [图面识别]\n\n")
        for kind, rows in (("箍筋", res["rebar_summary"].get("箍筋") or []),
                           ("纵筋", res["rebar_summary"].get("纵筋") or [])):
            if not rows:
                continue
            o.write(f"**{kind}**\n\n")
            o.write("| 型号 | 构件型数 | 估算根数 | 构件编号 |\n|---|---|---|---|\n")
            for row in rows:
                o.write(f"| {row['型号']} | {row['构件型数']} | {row['估算根数']} | {row['构件编号']} |\n")
            o.write("\n")
    if res.get("practices"):
        name_of = {i: f["name"] for i, f in enumerate(files)}
        o.write("\n## 建筑做法 [图面识别]\n\n")
        o.write("| 部位 | 做法原文 | 文件 | 图框 | 图层 |\n|---|---|---|---|---|\n")
        for row in res["practices"][:200]:
            o.write(f"| {row['part']} | {row['text']} | "
                    f"{name_of.get(row.get('file'), '-')} | {row.get('sheet') or '-'} | "
                    f"{row.get('layer') or '-'} |\n")
    if res.get("spec_table") and res.get("spec"):
        o.write("\n## 规格表（图面与设计说明数值汇总）\n\n")
        o.write("| 项目 | 数值 | 出现次数 | 出处文件数 | 出处文件（最多 3 个） |\n|---|---|---|---|---|\n")
        for row in spec_rows(res, files):
            o.write("| " + " | ".join(str(c) if c != "" else "-" for c in row) + " |\n")
    if res["keyword_rows"]:
        name_of = {i: f["name"] for i, f in enumerate(files)}
        seen = set()
        rows = []
        for r in res["keyword_rows"]:
            key = (r["text"], r.get("file"), r.get("sheet"),
                   round(r["x"], 1) if isinstance(r.get("x"), (int, float)) else None,
                   round(r["y"], 1) if isinstance(r.get("y"), (int, float)) else None)
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)
        o.write(f"\n## 关键词命中原文（{len(res['keyword_rows'])} 条 / 去重 {len(rows)} 条）\n\n")
        o.write("| 原文 | 文件 | 图框 | 图层 | 坐标 |\n|---|---|---|---|---|\n")
        for r in rows[:400]:
            xy = (f"{r['x']:.0f},{r['y']:.0f}" if isinstance(r.get("x"), (int, float))
                  and isinstance(r.get("y"), (int, float)) else "-")
            o.write(f"| {r['text'][:160]} | {name_of.get(r.get('file'), '-')} | "
                    f"{r.get('sheet') or '-'} | {r.get('layer') or '-'} | {xy} |\n")
    if res["meta"].get("block_refs"):
        o.write("\n## 块/图例使用频次（前 20）\n\n")
        for k, v in list(res["meta"]["block_refs"].items())[:20]:
            o.write(f"- {k}：{v}\n")
    if res["layers"]:
        o.write(f"\n<details><summary>图层清单（{len(res['layers'])}）</summary>\n\n")
        o.write("、".join(res["layers"][:600]) + "\n\n</details>\n")
    o.write("\n> 根数估计口径：集中标注 > 标注位置 > 原文次数，三者同时给出便于核对；"
            "梁线候选长度为就近共线线段合并结果 [推测]，只作图面证据，不替代专业算量。\n")
    return o.getvalue()


CSV_HEAD = ["类别", "编号", "根数估计", "依据", "标注位置数", "含截面数", "原文次数", "图框数",
            "标注跨数", "悬挑", "洞口宽mm", "洞口高mm", "截面b", "截面h", "箍筋", "箍筋非加密间距",
            "箍筋肢数", "纵筋根数", "纵筋直径", "纵筋原文",
            "截面尺寸", "配筋片段", "梁线候选合计mm", "单根均长mm", "备注", "原文示例"]
REBAR_CSV_HEAD = ["类别", "型号", "构件型数", "估算根数", "构件编号"]
PRACTICE_CSV_HEAD = ["部位", "做法原文", "文件", "图框", "图层"]


def csv_rows(res):
    rows = []
    for cat, items in res["members"].items():
        for code, d in items.items():
            rows.append([cat, code, d["est"], d["basis"], d["pos_n"], d["sized_n"], d["count"],
                         d.get("sheet_n") or "", 
                         ("%s" + chr(0x203b)) % d["span"] if d.get("span_note") else d.get("span", ""),
                         d.get("cant", ""),
                         d.get("w", ""), d.get("ht", ""), d.get("b", ""), d.get("h", ""),
                         stirrup_of(d), d.get("ga", ""), d.get("ge", ""),
                         d.get("l_cnt", ""), d.get("l_dia", ""), d.get("l_txt", ""),
                         "、".join(sorted(d["sizes"], key=size_key)),
                         "、".join(sorted(d["rebar"])[:4]), d.get("len_mm") or "",
                         round(d["len_mm"] / d["len_n"]) if d.get("len_mm") and d.get("len_n") else "",
                         d.get("note", ""), (d["raws"][0] if d["raws"] else "")])
    return rows


def jsonable(res):
    keep = ("est", "basis", "pos_n", "sized_n", "count", "sheet_n", "len_mm", "len_avg_mm",
            "sizes", "rebar", "raws", "span", "cant", "span_note", "w", "ht", "b", "h",
            "gl", "gd", "gp", "ga", "ge", "l_cnt", "l_dia", "l_txt", "note")
    m = {}
    for c, v in res["members"].items():
        m[c] = {}
        for k, d in v.items():
            e = {kk: d[kk] for kk in keep if kk in d}
            e["sizes"] = sorted(d["sizes"], key=size_key)
            e["rebar"] = sorted(d["rebar"])
            e["raws"] = d["raws"]
            m[c][k] = e
    return {"members": m, "spec": res.get("spec"), "spec_src": res.get("spec_src"),
            "rebar_summary": res.get("rebar_summary"),
            "practices": res.get("practices"),
            "concrete": res["concrete"], "slab_thk": res["slab_thk"],
            "layers": res["layers"], "meta": res["meta"], "text_total": res["text_total"],
            "cache": res.get("cache"),
            "keyword_rows": res["keyword_rows"][:2000], "notes": res["notes"], "files": res["files"]}


# ---------------------------------------------------------------- main
def main():
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="低内存 CAD 文字/构件提取（DWG/DXF，免装 CAD 软件）")
    ap.add_argument("--worker", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--worker-path", default=None, help=argparse.SUPPRESS)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--glob", default="*.dwg", help="配合目录使用，默认 *.dwg")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--with-mtext", action="store_true", help="解 MTEXT（大图很慢，默认关）")
    ap.add_argument("--with-attrib", action="store_true", help="解 ATTRIB（极慢，默认关）")
    ap.add_argument("--with-insert", action="store_true", help="解块引用统计")
    ap.add_argument("--with-blocks", action="store_true", help="解块定义清单（大图较慢）")
    ap.add_argument("--with-block-geom", action="store_true", help="提取块定义内部几何，供几何指纹识图（DXF 全量；DWG 走短预算试探，超时自动回退近邻几何；需 --with-geom）")
    ap.add_argument("--with-block-expand", action="store_true",
                    help="展开模型空间直画实体与 INSERT 块内 LINE/LWPOLYLINE 几何，写入 --detail-json 的 block_geometry[]；每张图只读一次")
    ap.add_argument("--block-expand-max-segments", type=int, default=200000,
                    help="块几何展开段数上限，默认 200000；超限截断并写 notes/review")
    ap.add_argument("--detail-json", default=None,
                    help="额外写出 text_records/hits/geometry 的 detail JSON，供规范目录与规则解读使用")
    ap.add_argument("--only", default=None, help="只要这些类别，逗号分隔：梁,板,柱,墙,基础,门窗")
    ap.add_argument("--filter", dest="flt", default=None, help="只输出命中该正则的原文，如 '板厚|C30'")
    ap.add_argument("--search", dest="flt", default=None,
                    help="同 --filter：按关键词/正则查找图纸内容，输出文件、图框、图层、坐标")
    ap.add_argument("--budget", type=float, default=45.0, help="单阶段时间预算/秒，默认 45")
    ap.add_argument("--max-rows", type=int, default=200000)
    ap.add_argument("--geom-budget", type=float, default=0.0,
                    help="几何/块几何独立时间预算/秒（默认继承 --budget，大图可设更小）")
    ap.add_argument("--geom-max-rows", type=int, default=0,
                    help="几何线段数上限，0 表示不限；超限自动截断并回退近邻几何")
    ap.add_argument("--count-by", default="auto", choices=["auto", "label", "pos", "raw"],
                    help="根数口径：auto/label=集中标注(最接近根数)，pos=标注位置去重，raw=原文次数")
    ap.add_argument("--dedupe", type=float, default=1500.0, help="标注位置去重半径/图纸单位，默认 1500")
    ap.add_argument("--no-sheet", action="store_true", help="不自动分图框（跨图框重复计）")
    ap.add_argument("--sheet-min", type=int, default=60, help="图框至少容纳多少条文字才参与去重，默认 60")
    ap.add_argument("--sheets", default="auto", choices=["auto", "frame", "grid"],
                    help="分图框方式：auto=有图框块就用块(需 --with-insert)，否则按坐标空隙；frame/grid 强制")
    ap.add_argument("--sheet-bin", type=float, default=10000.0, help="分图框网格尺寸/图纸单位，默认 10000")
    ap.add_argument("--with-geom", action="store_true", help="提取 LINE/LWPOLYLINE 几何候选，用于识图定位和复核")
    ap.add_argument("--with-geom-layer", action="store_true",
                    help="额外保存每段几何所在的图层（DWG 需解码实体句柄，供识图定位）")
    ap.add_argument("--geom-radius", type=float, default=3000.0, help="几何候选关联取标注点附近多大范围，默认 3000")
    ap.add_argument("--cluster", type=float, default=0.0, help="按此网格尺寸(图纸单位,如 1500)合并邻近文字，还原平法集中标注")
    ap.add_argument("-o", "--out", default=None, help="输出前缀，写 .md/.json/.csv/.xlsx/.docx")
    ap.add_argument("--format", default="md", help="md|json|csv|xlsx|docx|all")
    ap.add_argument("--concise", action="store_true", help="精简输出（省 Token）：候选只保留主干字段")
    ap.add_argument("--full", action="store_true", help="完整输出（含 evidence/bbox 等全部字段，默认）")
    ap.add_argument("--with-evidence", action="store_true", help="同 --full")
    ap.add_argument("--spec-table", action="store_true",
                    help="额外出规格表：板厚/混凝土等级/保护层/抗震等级（md 追加一节，csv 另写 -spec.csv）")
    ap.add_argument("--cache-dir", default=None,
                    help="启用 cad_scan 证据缓存并指定目录；同图重复查询不再重复解码")
    ap.add_argument("--roi", default=None,
                    help="局部读取图面矩形 left,bottom,right,top（图纸单位）")
    ap.add_argument("--sheet", default=None,
                    help="局部读取缓存中的一个图框编号")
    ap.add_argument("--dwg-dxf-fallback", action="store_true",
                    help="DWG 块名解码为空/乱码时，自动转 DXF 后复扫一层（较稳，慢一些；CAD_DWG_DXF_FALLBACK=1 可默认开启）")
    args = ap.parse_args()
    if args.with_block_expand and not args.detail_json:
        print("[提示] --with-block-expand 的结果写入 --detail-json；未指定详情文件，本次展开结果不会落盘。", file=sys.stderr)

    if args.full or args.with_evidence:
        os.environ["CAD_CONCISE"] = "0"
    elif args.concise:
        os.environ["CAD_CONCISE"] = "1"
    else:
        os.environ.setdefault("CAD_CONCISE", os.environ.get("CAD_CONCISE", "0"))

    want = set(TEXT_KINDS[:1])
    if args.with_mtext:
        want.add("mtext")
    if args.with_attrib:
        want.add("attrib")

    files: list[Path] = []
    for p in args.paths:
        pp = Path(p).expanduser()
        if pp.is_dir():
            it = pp.rglob("*") if args.recursive else pp.glob("*")
            files += sorted(x for x in it if x.is_file() and fnmatch.fnmatch(x.name.lower(), args.glob.lower()))
        elif pp.is_file():
            files.append(pp)
    if not files:
        print("没有找到文件", file=sys.stderr)
        return 2

    def rss_mb():
        try:
            import resource
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys.platform == "darwin":
                return round(rss / 1e6)
            if sys.platform.startswith("linux"):
                return round(rss / 1024)
        except Exception:
            pass
        try:
            import psutil
            return round(psutil.Process().memory_info().rss / 1048576.0)
        except Exception:
            return 0

    if args.worker:
        sys.exit(_worker(args.worker, args.paths[0]))

    roi = None
    if args.roi:
        try:
            vals = [float(x) for x in args.roi.split(",")]
            if len(vals) != 4 or not all(math.isfinite(x) for x in vals):
                raise ValueError
            roi = (min(vals[0], vals[2]), min(vals[1], vals[3]),
                   max(vals[0], vals[2]), max(vals[1], vals[3]))
        except Exception:
            print("❌ --roi 参数无效；请使用 left,bottom,right,top", file=sys.stderr)
            return 2
    sheet = None
    if args.sheet is not None:
        try:
            sheet = int(args.sheet)
            if sheet <= 0:
                raise ValueError
        except Exception:
            print("❌ --sheet 参数无效；请使用缓存图框编号", file=sys.stderr)
            return 2
    if roi is not None and sheet is not None:
        print("❌ --roi 和 --sheet 只能选择一个局部范围", file=sys.stderr)
        return 2
    cache_dir = Path(args.cache_dir).expanduser() if args.cache_dir else None
    scan_profile = profile_for(args, want)

    keep = re.compile(args.flt, re.I) if args.flt else None
    all_recs: list[dict] = []
    all_layers: set[str] = set()
    all_meta: dict = {"block_refs": {}}
    fstats: list[dict] = []
    notes: list[str] = []
    seg_files: list[list] = []
    gents_all: list = []
    seg_layers_files: list[list] = []
    block_geometry_entries: list[dict] = []
    sheet_base = 0
    partial = roi is not None or sheet is not None

    for f in files:
        import time
        t0 = time.time()
        log = lambda s: print(f"{f.name}: {s}", file=sys.stderr)
        log("开始")
        pf = preflight_file(f)
        if not pf.get("ok"):
            msg = f"快速失败 - {pf.get('reason')}"
            notes.append(f"{f.name}: {msg}")
            log(f"跳过：{msg}")
            continue
        try:
            head = pf.get("head") or f.read_bytes()[:128]
        except Exception as e:
            notes.append(f"{f.name}: 读取失败 {e}")
            continue
        fmt = detect_format(head, f.suffix.lower())
        if args.with_block_expand and fmt in ("DWG", "DXF"):
            block_limit = max(1, int(args.block_expand_max_segments or 200000))
            try:
                block_budget = args.geom_budget if args.geom_budget and args.geom_budget > 0 else args.budget
                expanded = expand_block_geometry(f, budget=block_budget, log=log)
                block_segments = list(expanded.get("segments") or [])
                block_notes = list(expanded.get("notes") or [])
                truncated = len(block_segments) > block_limit
                if truncated:
                    block_segments = block_segments[:block_limit]
                    msg = f"块几何展开 {len(expanded.get('segments') or [])} 段，超过上限 {block_limit}，已截断"
                    block_notes.append(msg)
                    notes.append(f"{f.name}: {msg}")
                entry = {
                    "source_path": str(f.resolve()),
                    "segments": block_segments,
                    "blocks": list(expanded.get("blocks") or []),
                    "units": expanded.get("units") or {},
                    "notes": block_notes,
                    "truncated": truncated,
                }
                if truncated:
                    entry["review"] = [{
                        "type": "block_geometry_truncated",
                        "reason": f"块几何段数超过安全上限 {block_limit}，仅保留前 {block_limit} 段；后续候选不完整，需缩小范围或分图复核",
                        "evidence": {"limit": block_limit, "original_segments": len(expanded.get("segments") or [])},
                    }]
                block_geometry_entries.append(entry)
            except Exception as exc:
                msg = f"块几何展开失败：{type(exc).__name__}: {exc}"
                notes.append(f"{f.name}: {msg}")
                block_geometry_entries.append({
                    "source_path": str(f.resolve()), "segments": [], "blocks": [],
                    "units": {}, "notes": [msg], "truncated": False,
                    "review": [{"type": "block_geometry_failed", "reason": msg, "evidence": {"exception": type(exc).__name__}}],
                })
        elif args.with_block_expand and fmt not in ("DWG", "DXF"):
            notes.append(f"{f.name}: --with-block-expand 仅支持 DWG/DXF，当前格式 {fmt} 已跳过")
        cached = None
        digest = None
        cache_read_ms = 0.0
        cache_write_ms = 0.0
        cache_file = None
        if cache_dir is not None:
            try:
                digest = file_digest(f)
                query_sheet = None
                if sheet is not None:
                    local_sheet = sheet - sheet_base
                    query_sheet = local_sheet if local_sheet > 0 else 0
                cache_t0 = time.perf_counter()
                cached = load_cached_scan(f, cache_dir, digest, scan_profile,
                                          roi=roi, sheet=query_sheet)
                cache_read_ms = (time.perf_counter() - cache_t0) * 1000.0
                if cached and cached.get("cache_file"):
                    cache_file = str(cached["cache_file"])
            except Exception as e:
                cache_read_ms = (time.perf_counter() - cache_t0) * 1000.0 if 'cache_t0' in locals() else 0.0
                notes.append(f"{f.name}: 缓存读取失败 {e}")
                cached = None

        file_notes: list[str] = []
        fallback_dxf: Path | None = None
        local_sheets: list[dict] = []
        gsegs: list = []
        gents: list = []
        glayers: list[str] | None = [] if args.with_geom_layer else None
        if cached is not None:
            recs, layers, meta = cached["recs"], cached["layers"], cached["meta"]
            local_sheets = list(meta.pop("sheets", []) or [])
            file_sheet_count = int(cached.get("sheet_count") or len(local_sheets))
            gsegs = list(cached.get("segs") or []) if args.with_geom else []
            glayers = list(cached.get("seg_layers") or []) if args.with_geom_layer else None
            if args.with_geom and fmt in ("DWG", "DXF"):
                # 圆实体不入 sqlite 缓存（表结构保持稳定），缓存命中时现解一遍；
                # 解码有预算护栏，代价小。
                gb = args.geom_budget if args.geom_budget and args.geom_budget > 0 else args.budget
                gm = args.geom_max_rows if args.geom_max_rows and args.geom_max_rows > 0 else None
                try:
                    if fmt == "DXF":
                        gents, en = dxf_circle_entities(str(f), gb, log, max_rows=gm)
                    else:
                        gents, en = circle_entities(str(f), gb, log, max_rows=gm)
                    notes += [f"{f.name}: {x}" for x in en]
                except Exception as e:
                    notes.append(f"{f.name}: 圆实体提取失败 {type(e).__name__} {e}")
            notes.append(f"{f.name}: 缓存命中（{'局部' if cached.get('partial') else '全量'}）")
            for x in cached.get("notes") or []:
                notes.append(f"{f.name}: {x}")
        else:
            if fmt == "DXF":
                try:
                    de_roi = roi if cache_dir is None else None
                    recs, layers, n, meta = dxf_records(str(f), args.max_rows, log, roi=de_roi, include_insert=args.with_insert)
                except Exception as e:
                    n, recs, layers, meta = [f"DXF 解析失败：{e}"], [], [], {}
            else:
                try:
                    de_roi = roi if cache_dir is None else None
                    recs, layers, n, meta = dwg_records(
                        str(f), want | ({"insert"} if args.with_insert else set()),
                        args.budget, args.max_rows, log, want_blocks=args.with_blocks, roi=de_roi)
                except Exception as e:
                    n, recs, layers, meta = [f"DWG 解析失败：{e}（如需可转 DXF）"], [], [], {}
            file_notes = list(n)
            notes += [f"{f.name}: {x}" for x in n]
            if fmt == "DWG" and (args.dwg_dxf_fallback or os.environ.get("CAD_DWG_DXF_FALLBACK") == "1" or not recs) and (
                not recs
                or any(k in x for x in file_notes for k in (
                    "解码为空", "解码失败", "疑似编码乱码", "块名疑似乱码", "DWG 解析失败", "section map page not found", "section map has no entries",
                ))
            ):
                try:
                    from read_cad import convert_dwg_to_dxf
                    dxf_path, cnote = convert_dwg_to_dxf(Path(f))
                except Exception as e:
                    dxf_path, cnote = None, f"自动转 DXF 复扫失败：{type(e).__name__} {e}"
                if dxf_path:
                    try:
                        fdx = Path(dxf_path)
                        recs2, layers2, n2, meta2 = dxf_records(str(fdx), args.max_rows, log, roi=de_roi, include_insert=args.with_insert)
                        if recs2 or layers2 or meta2:
                            recs, layers, meta, n = recs2, layers2, meta2, list(n2)
                            fallback_dxf = fdx
                            engine = "LibreDWG" if ("dwg2dxf" in (cnote or "")) else "ezdwg"
                            msg = f"DWG 直读失败，已自动转 DXF（{engine}）复扫：块引用 {meta.get('insert_count', 0)} / 文字 {len(recs)}"
                            file_notes = list(n) + [msg]
                            notes.append(f"{f.name}: {msg}")
                    except Exception as e:
                        notes.append(f"{f.name}: 自动转 DXF 复扫失败：{type(e).__name__} {e}")
            for r in recs:
                r["file"] = len(fstats)
            if recs and not args.no_sheet:
                anchors = []
                if args.sheets in ("auto", "frame"):
                    anchors = frame_anchors(recs)
                try:
                    if anchors and args.sheets != "grid":
                        local_sheets = assign_sheets_by_frames(recs, anchors, args.sheet_min)
                        if local_sheets:
                            notes.append(f"{f.name}: 按图框块定位（{len(local_sheets)}/{len(anchors)} 个图框有内容）")
                    if not local_sheets:
                        local_sheets = assign_sheets(recs, args.sheet_bin, args.sheet_min)
                        if anchors and args.sheets != "grid":
                            notes.append(f"{f.name}: 图框块命中率低，改用坐标空隙分图框")
                        elif args.sheets == "frame":
                            notes.append(f"{f.name}: 没找到图框块，改用坐标空隙分图框（--with-insert 可提高准确率）")
                except Exception as e:
                    local_sheets = []
                    notes.append(f"{f.name}: 分图框失败 {e}")

            block_geometries = meta.get("block_geometries")
            if args.with_block_geom and fmt == "DXF" and not block_geometries:
                gb = args.geom_budget if args.geom_budget and args.geom_budget > 0 else args.budget
                gm = args.geom_max_rows if args.geom_max_rows and args.geom_max_rows > 0 else None
                bg_res, bg_notes = dxf_block_geometries(str(f), gb, log, max_rows=gm)
                if bg_res:
                    meta["block_geometries"] = bg_res
                if bg_notes:
                    notes += [f"{f.name}: {x}" for x in bg_notes]
                    file_notes.extend(bg_notes)
            elif args.with_block_geom and fmt == "DWG" and fallback_dxf is not None:
                bg_res, bg_notes = dxf_block_geometries(
                    str(fallback_dxf),
                    args.geom_budget if args.geom_budget and args.geom_budget > 0 else args.budget,
                    log,
                    max_rows=args.geom_max_rows if args.geom_max_rows and args.geom_max_rows > 0 else None)
                if bg_res:
                    meta["block_geometries"] = bg_res
                if bg_notes:
                    notes += [f"{f.name}: {x}" for x in bg_notes]
                    file_notes += bg_notes

            if args.with_geom:
                gb = args.geom_budget if args.geom_budget and args.geom_budget > 0 else args.budget
                gm = args.geom_max_rows if args.geom_max_rows and args.geom_max_rows > 0 else None
                de_roi = roi if cache_dir is None else None
                if fmt == "DWG" and fallback_dxf is not None:
                    if args.with_geom_layer:
                        gsegs, glayers, gn = dxf_geometry_segments(str(fallback_dxf), gb, log, include_layers=True, roi=de_roi, max_rows=gm)
                    else:
                        gsegs, gn = dxf_geometry_segments(str(fallback_dxf), gb, log, roi=de_roi, max_rows=gm)
                elif fmt == "DWG":
                    if args.with_geom_layer:
                        gsegs, glayers, gn = geometry_segments(str(f), gb, log, include_layers=True, roi=de_roi, max_rows=gm)
                    else:
                        gsegs, gn = geometry_segments(str(f), gb, log, roi=de_roi, max_rows=gm)
                elif fmt == "DXF":
                    if args.with_geom_layer:
                        gsegs, glayers, gn = dxf_geometry_segments(str(f), gb, log, include_layers=True, roi=de_roi, max_rows=gm)
                    else:
                        gsegs, gn = dxf_geometry_segments(str(f), gb, log, roi=de_roi, max_rows=gm)
                else:
                    gsegs, gn = [], []
                glayers = glayers if args.with_geom_layer else None
                file_notes.extend(gn)
                notes += [f"{f.name}: {x}" for x in gn]
                if fmt in ("DWG", "DXF"):
                    try:
                        if fmt == "DXF":
                            gents, en = dxf_circle_entities(str(f), gb, log, max_rows=gm)
                        else:
                            gents, en = circle_entities(str(f), gb, log, max_rows=gm)
                        file_notes.extend(en)
                        notes += [f"{f.name}: {x}" for x in en]
                    except Exception as e:
                        notes.append(f"{f.name}: 圆实体提取失败 {type(e).__name__} {e}")

            if cache_dir is not None:
                cache_meta = dict(meta)
                cache_meta["sheets"] = local_sheets
                cache_t0 = time.perf_counter()
                saved = save_cached_scan(
                    f, cache_dir, digest, scan_profile, recs, layers, cache_meta,
                    gsegs if args.with_geom else [],
                    glayers if args.with_geom and args.with_geom_layer else [],
                    file_notes)
                cache_write_ms = (time.perf_counter() - cache_t0) * 1000.0
                if saved:
                    cache_file = str(saved)
                    notes.append(f"{f.name}: 证据缓存已写入")
                else:
                    notes.append(f"{f.name}: 缓存未写入（解码不完整或写入失败）")

        # 缓存内保存的是本文件局部图框编号；进入汇总前统一偏移。
        if cached is None:
            file_sheet_count = len(local_sheets)
        base = sheet_base
        file_sheets: list[dict] = []
        for s in local_sheets:
            row = dict(s)
            row["id"] = int(row.get("id") or 0) + base
            row["file"] = f.name
            file_sheets.append(row)
        for r in recs:
            r["file"] = len(fstats)
            sid = sheet_id(r)
            if sid is not None:
                r["sheet"] = sid + base

        partial = roi is not None or sheet is not None
        if roi is not None:
            file_sheets = sheets_in_roi(file_sheets, roi)
            recs = records_in_roi(recs, roi)
            gsegs, glayers = segments_in_roi(
                gsegs, roi, glayers if args.with_geom_layer else None)
            gents = [e for e in gents if _rc_in_roi(e[0], e[1], roi)]
        elif sheet is not None:
            file_sheets = [s for s in file_sheets if int(s.get("id") or 0) == sheet]
            recs = [r for r in recs if sheet_id(r) == sheet]
            bbox = sheet_bbox(file_sheets, sheet)
            if bbox is not None:
                gsegs, glayers = segments_in_roi(
                    gsegs, bbox, glayers if args.with_geom_layer else None)
                gents = [e for e in gents if _rc_in_roi(e[0], e[1], bbox)]
            else:
                gsegs, glayers = [], [] if args.with_geom_layer else None
                gents = []

        if partial:
            layers = sorted({str(r.get("layer") or "") for r in recs} - {""})
        all_meta.setdefault("sheets", []).extend(file_sheets)
        sheet_base += file_sheet_count
        all_recs += recs
        all_layers |= set(layers)
        if not partial:
            for k, v in (meta.get("block_refs") or {}).items():
                all_meta["block_refs"][k] = all_meta["block_refs"].get(k, 0) + v
            all_meta["insert_count"] = all_meta.get("insert_count", 0) + (meta.get("insert_count") or 0)
            blk_defs = meta.get("block_defs")
            if isinstance(blk_defs, list):
                cur: list = all_meta.setdefault("block_defs", [])
                for x in blk_defs:
                    if x not in cur:
                        cur.append(x)
                all_meta["block_defs"] = sorted(cur)
            bg = meta.get("block_geometries") or {}
            if isinstance(bg, dict) and bg:
                all_meta.setdefault("block_geometries", {}).update(bg)

        cache_bytes = 0
        if cache_file:
            try:
                cache_bytes = Path(cache_file).stat().st_size
            except OSError:
                cache_bytes = 0
        st = {"name": f.name, "path": str(f), "fmt": fmt,
              "texts": len(recs), "layers": len(layers), "secs": round(time.time() - t0, 1), "rss": rss_mb(),
              "cache": "hit" if cached is not None else "miss",
              "cache_read_ms": round(max(0.0, cache_read_ms), 3),
              "cache_write_ms": round(max(0.0, cache_write_ms), 3),
              "cache_bytes": cache_bytes,
              "cache_file": cache_file}
        fstats.append(st)
        if args.with_geom:
            st["segs"] = len(gsegs)
            st["ents"] = len(gents)
            seg_files.append(gsegs)
            gents_all.extend([list(e) + [len(fstats)] for e in gents])
            if args.with_geom_layer:
                seg_layers_files.append(glayers or [])
        log(f"完成 {round(time.time()-t0,1)}s / 峰值内存 {rss_mb()}MB")

    if sheet is not None and not all_recs:
        notes.append(f"--sheet {sheet} 未命中；已保留空结果，未编造图框内容")
    if partial:
        # 局部查询只输出命中范围内的证据；空块统计容器也不留在 JSON 中。
        all_meta.pop("block_refs", None)
        all_meta.pop("insert_count", None)
        all_meta.pop("block_defs", None)

    res = analyse(cluster_records(all_recs, args.cluster), sorted(all_layers), all_meta, keep,
                  dedupe=args.dedupe, count_by=args.count_by)
    res["spec_table"] = bool(args.spec_table)
    if args.with_geom and any(seg_files):
        try:
            estimate_beam_lengths(res, seg_files, args.geom_radius)
        except Exception as e:
            notes.append(f"梁长估算失败：{type(e).__name__}: {e}")
    if args.only:
        pick = {x.strip() for x in args.only.split(",") if x.strip()}
        res["members"] = {c: v for c, v in res["members"].items() if c in pick}
    res["notes"] = notes
    res["files"] = fstats
    if cache_dir is not None:
        cache_files = {
            x["cache_file"]: int(x.get("cache_bytes") or 0)
            for x in fstats if x.get("cache_file")
        }
        res["cache"] = {
            "dir": str(cache_dir),
            "hits": sum(1 for x in fstats if x.get("cache") == "hit"),
            "misses": sum(1 for x in fstats if x.get("cache") == "miss"),
            "read_ms": round(sum(float(x.get("cache_read_ms") or 0.0) for x in fstats), 3),
            "write_ms": round(sum(float(x.get("cache_write_ms") or 0.0) for x in fstats), 3),
            "db_files": len(cache_files),
            "db_bytes": sum(cache_files.values()),
        }
    all_meta.pop("segs", None)

    md = to_md(res, fstats)
    if args.out:
        base = Path(args.out)
        base.parent.mkdir(parents=True, exist_ok=True)
        written = []
        if args.format in ("md", "all"):
            base.with_suffix(".md").write_text(md, encoding="utf-8")
            written.append(str(base.with_suffix(".md")))
        if args.format in ("json", "all"):
            base.with_suffix(".json").write_text(json.dumps(jsonable(res), ensure_ascii=False, indent=1), encoding="utf-8")
            written.append(str(base.with_suffix(".json")))
        if args.format in ("csv", "all"):
            with base.with_suffix(".csv").open("w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh)
                w.writerow(CSV_HEAD)
                w.writerows(csv_rows(res))
            if args.spec_table and res.get("spec"):
                with base.with_name(base.name + "-spec.csv").open("w", newline="", encoding="utf-8-sig") as fh:
                    w = csv.writer(fh)
                    w.writerow(SPEC_CSV_HEAD)
                    w.writerows(spec_rows(res, fstats))
            if res.get("rebar_summary") and any(res["rebar_summary"].values()):
                with base.with_name(base.name + "-rebar.csv").open("w", newline="", encoding="utf-8-sig") as fh:
                    w = csv.writer(fh)
                    w.writerow(REBAR_CSV_HEAD)
                    for kind in ("箍筋", "纵筋"):
                        for row in res["rebar_summary"].get(kind) or []:
                            w.writerow([kind, row["型号"], row["构件型数"], row["估算根数"], row["构件编号"]])
            if res.get("practices"):
                with base.with_name(base.name + "-practices.csv").open("w", newline="", encoding="utf-8-sig") as fh:
                    w = csv.writer(fh)
                    w.writerow(PRACTICE_CSV_HEAD)
                    name_of = {i: f["name"] for i, f in enumerate(fstats)}
                    for row in res["practices"]:
                        w.writerow([row["part"], row["text"], name_of.get(row.get("file"), ""),
                                    row.get("sheet") or "", row.get("layer") or ""])
            written.append(str(base.with_suffix(".csv")))
        if args.format in ("xlsx", "all"):
            try:
                from cad_export import write_xlsx
                sections = [
                    ("构件候选", CSV_HEAD, csv_rows(res)),
                ]
                if args.spec_table and res.get("spec"):
                    sections.append(("规格表", SPEC_CSV_HEAD, spec_rows(res, fstats)))
                if res.get("rebar_summary") and any(res["rebar_summary"].values()):
                    rb = []
                    for kind in ("箍筋", "纵筋"):
                        for row in res["rebar_summary"].get(kind) or []:
                            rb.append([kind, row["型号"], row["构件型数"], row["估算根数"], row["构件编号"]])
                    sections.append(("钢筋汇总", REBAR_CSV_HEAD, rb))
                if res.get("practices"):
                    name_of = {i: f["name"] for i, f in enumerate(fstats)}
                    pr = [[row["part"], row["text"], name_of.get(row.get("file"), ""),
                           row.get("sheet") or "", row.get("layer") or ""] for row in res["practices"]]
                    sections.append(("建筑做法", PRACTICE_CSV_HEAD, pr))
                xlsx_path = write_xlsx(base.with_suffix(".xlsx"), sections)
                written.append(str(xlsx_path))
            except Exception as exc:
                print(f"xlsx 导出失败（跳过）：{exc}", file=sys.stderr)
        if args.format in ("docx", "all"):
            try:
                from cad_export import write_docx
                sections = [
                    ("构件候选", CSV_HEAD, csv_rows(res)),
                ]
                if args.spec_table and res.get("spec"):
                    sections.append(("规格表", SPEC_CSV_HEAD, spec_rows(res, fstats)))
                if res.get("rebar_summary") and any(res["rebar_summary"].values()):
                    rb = []
                    for kind in ("箍筋", "纵筋"):
                        for row in res["rebar_summary"].get(kind) or []:
                            rb.append([kind, row["型号"], row["构件型数"], row["估算根数"], row["构件编号"]])
                    sections.append(("钢筋汇总", REBAR_CSV_HEAD, rb))
                if res.get("practices"):
                    name_of = {i: f["name"] for i, f in enumerate(fstats)}
                    pr = [[row["part"], row["text"], name_of.get(row.get("file"), ""),
                           row.get("sheet") or "", row.get("layer") or ""] for row in res["practices"]]
                    sections.append(("建筑做法", PRACTICE_CSV_HEAD, pr))
                docx_path = write_docx(base.with_suffix(".docx"), "CAD 图纸解析结果", sections)
                written.append(str(docx_path))
            except Exception as exc:
                print(f"docx 导出失败（跳过）：{exc}", file=sys.stderr)
        print("已写出 " + "、".join(written), file=sys.stderr)
    else:
        if args.format in ("xlsx", "docx"):
            print("导出 xlsx/docx 需要 --out 参数（--format %s --out 输出前缀）" % args.format, file=sys.stderr)
            return 2
        if args.format == "json":
            print(json.dumps(jsonable(res), ensure_ascii=False, indent=1))
        elif args.format == "csv":
            w = csv.writer(sys.stdout)
            w.writerow(CSV_HEAD)
            w.writerows(csv_rows(res))
            if args.spec_table and res.get("spec"):
                print("", end="")
                w.writerow([])
                w.writerow(SPEC_CSV_HEAD)
                w.writerows(spec_rows(res, fstats))
        else:
            print(md)
    if notes:
        print("\n[提示] " + "；".join(notes), file=sys.stderr)
    if args.detail_json:
        detail = jsonable(res)
        # 产物必须能说出自己来自哪张图。只靠产物文件名不够：下游（图纸聚类、
        # 跨专业配对）拿到的路径是输出目录，会把整套多专业图纸挤进同一个簇，
        # 专业判定再准也没用。这里记源图绝对路径。
        detail["source_paths"] = [str(Path(p).resolve()) for p in (args.paths or [])]
        detail["text_records"] = all_recs
        detail["hits"] = res.get("hits") or []
        detail["geometry_segments"] = seg_files if args.with_geom else []
        detail["geometry_layers"] = seg_layers_files if args.with_geom_layer else []
        detail["geometry_entities"] = gents_all if args.with_geom else []
        detail["block_geometry"] = block_geometry_entries if args.with_block_expand else []
        detail_path = Path(args.detail_json)
        detail_path.parent.mkdir(parents=True, exist_ok=True)
        detail_path.write_text(
            json.dumps(detail, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写出详情 {detail_path}", file=sys.stderr)

    # 零产出不是成功。任何 DWG/DXF 的图层表至少有一个 "0" 图层，图层表为空、
    # 文字也为空，只能说明这张图没读出来，不是一张空图。返回 0 会让上游把它
    # 当成「图纸没内容」，而实际是「解析失败」——两者后续处理完全不同，
    # 静默成功会把能力边界藏起来（实测 5 张 AC1018/AC1027 大图即如此）。
    if not (res.get("layers") or []) and not all_recs:
        print("[错误] 解析结果为空：图层表 0 条、文字 0 条。"
              "这不是空图，是没读出来。常见原因：section map 变体（page info truncated）；"
              "可先用其它工具确认文件本身完整，再考虑降级到 DXF 路径。",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
