#!/usr/bin/env python3
"""扫描安装图纸 DWG：管线分段、设备、文本、块计数、属性组、楼层锚点。"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import math
import re
import os
import sys

import i18n
from collections import defaultdict
from pathlib import Path

try:
    import resource  # type: ignore
except ImportError:
    resource = None


def _base_dir():
    """只探测、不下载：找不到 cad-file-reader 时返回 None，由入口给安装命令。"""
    sandbox = os.environ.get("CODEX_SKILLS_ROOT", "").strip()
    if sandbox:
        cands = [Path(sandbox).expanduser() / "cad-file-reader"]
    else:
        override = os.environ.get("CAD_SKILL_DIR", "").strip()
        cands = [Path(override).expanduser()] if override else []
        cands += [
            Path.home() / ".codex" / "skills" / "cad-file-reader",
            Path.home() / ".claude" / "skills" / "cad-file-reader",
        ]
    for candidate in cands:
        if (candidate / "scripts").is_dir():
            return candidate.resolve()
    return None


CAD_SKILL_DIR = _base_dir()
VENDOR = (CAD_SKILL_DIR / "vendor") if CAD_SKILL_DIR else None
SCRIPTS = (CAD_SKILL_DIR / "scripts") if CAD_SKILL_DIR else None


def cad_reader_info() -> dict:
    """记录识图底座版本和测量候选兼容状态，便于扫描结果追溯。"""
    version = ""
    if CAD_SKILL_DIR:
        try:
            version = str(json.loads((CAD_SKILL_DIR / "manifest.json").read_text(encoding="utf-8")).get("version") or "")
        except Exception:
            pass
    parts = []
    for piece in version.split("."):
        try:
            parts.append(int(piece))
        except ValueError:
            parts.append(0)
    compatible = len(parts) >= 2 and (parts[0], parts[1]) >= (0, 41)
    return {"version": version, "measurement_candidates_compatible": compatible}


if SCRIPTS:
    sys.path.insert(0, str(SCRIPTS))
if VENDOR and VENDOR.is_dir():
    sys.path.insert(0, str(VENDOR))
try:
    from cad_common import start_mem_guard  # noqa: E402
except Exception:  # 底座缺失时内存闸降级，不影响契约消费
    def start_mem_guard(**kwargs):
        return {"ok": True, "skipped": "cad_common 不可用（仅内存闸）"}

import contract_support as cs  # noqa: E402
from contract_guard import GuardError, guard_contract  # noqa: E402
import entry_gate as eg  # noqa: E402

SEG_LAYER_RE = re.compile(r"(WIRE|PIPE|CABLETRAY|BUSB|LGT|E-WIRE|E-CABLETRAY)", re.I)
OUTDOOR_LAYER_RE = re.compile(
    r"(强电|弱电|电缆|排管|电缆沟|管网|综合管网|室外管网|雨水|污水|废水|给水|中水|消防|喷淋|燃气|热力|暖通|采暖|供热|通信|照明|景观|路灯|SITE[_-]?PIPE|OUTDOOR|DIM_|EQUIP_|管线-|HEATER|HEATING)",
    re.I,
)
# 不是管线的图层：标注、图框、设备符号、建筑底图。
# `OUTDOOR_LAYER_RE` 里有 `照明`/`DIM_`/`EQUIP_`，室内电气图的标注层会因此被当成路由，
# 实测 J-5 电气图 `DIM-照明` 白扫出 11329.9m 线段，拖慢出表还污染「图层分档」。
NON_ROUTE_RE = re.compile(
    r"^(?:DIM|DIMENSION)|标注|尺寸|图框|标题|会签|PUB[_-]?TITLE|^WALL$|墙体|^STAIR|楼梯"
    r"|^AXIS|轴网|^DOTE$|^TEXT|文字|^HATCH|填充|图例|^EQUIP[_-]|设备图"
    # 块展开后图层名带 `外层块$0$` 前缀，`^DIM` 锚不上；尺寸/引出/标高线不是管线，
    # 实测sample-site图里 DIM_LEAD/DIM_MODI/DIM_ELEV 占掉近万段，必须无锚点再挡一道。
    r"|DIM[_-]",
    re.I,
)
# 图签/标题栏属性不是设备：图号、子项名称、设计单位、绘图人、比例、专业类别……
# 实测sample-site图里 devices 开头全是「张工/绘图」「10号楼/子项名称_001」「暖施01/图号」，
# 会把人名单层当成设备点位，必须按 tag 剔除（tag 常带 `_001` 匿名副本后缀）。
TITLE_ATTRIB_TAG_RE = re.compile(
    r"(图\s*号|图\s*名|图别|图签|标题|子项|工程名|项目名称|建设单位|设计单位|施工单位|监理单位|勘察单位|"
    r"设计|制图|绘\s*图|描图|描校|校对|审核|审定|批准|项目负责人|专业负责人|设计人|制图人|会签|签字|"
    r"专业类别|专业|比例|日期|阶段|版本|张次|页码|共\s*张|第\s*张|出图|联系|电话|地址|"
    r"编\s*号|序号|项目号|合同号|档案号|工程编号|工程代号|工程名)",
    re.I,
)
TITLE_ATTRIB_TAG_SUFFIX_RE = re.compile(r"[_\-]\d+$")
TITLE_ATTRIB_TEXT_RE = re.compile(r"^\s*(1\s*:\s*\d+|[A-Za-z]{0,4}\d{1,3}([-.]\d+)*|"
                                  r"\d{4}[-/年.]\d{1,2}([-/月.]\d{1,2})?|—+|—+|/+|N/?A|无)\s*$", re.I)


def is_titleblock_attrib(tag: str, text: str) -> bool:
    """判断 ATTRIB 是否来自图签（标题栏），是则不计入设备点位。"""
    base = TITLE_ATTRIB_TAG_SUFFIX_RE.sub("", (tag or "").strip())
    if base and TITLE_ATTRIB_TAG_RE.search(base):
        return True
    if TITLE_ATTRIB_TAG_RE.search((tag or "").strip()):
        return True
    # 无 tag 时退化为文本形态：纯比例/编号/日期/占位线都不是设备。
    return bool(not base and text and TITLE_ATTRIB_TEXT_RE.match(text))


def is_non_route_layer(layer: str) -> bool:
    return bool(NON_ROUTE_RE.search(layer or ""))


def route_layer(layer: str, domain: str = "auto") -> bool:
    """判断图层是否可作为安装路由；auto 兼容室内，outdoor 扩展室外管网。"""
    if is_non_route_layer(layer):
        return False
    if domain == "indoor":
        return bool(SEG_LAYER_RE.search(layer))
    if domain == "outdoor":
        return bool(SEG_LAYER_RE.search(layer) or OUTDOOR_LAYER_RE.search(layer))
    return bool(SEG_LAYER_RE.search(layer) or OUTDOOR_LAYER_RE.search(layer))


def pipe_layer(layer: str) -> bool:
    """判断图层是否属于给排水/管网管段，供管径标注匹配使用。

    电气优先：`WIRE-消防` 是消防联动线路，不是消防水管；两条判据不互斥时
    同一批管长既进电线电缆又进水专业，全楼量凭空翻倍。
    """
    if is_non_route_layer(layer):
        return False
    if re.search(r"WIRE|BUSB|LGT", layer, re.I):
        return False
    return layer.upper().startswith("PIPE-") or bool(re.search(r"(管网|室外管网|雨水|污水|废水|给水|中水|消防|喷淋|燃气|热力|暖通|采暖|供热|SITE[_-]?PIPE|管线-|HEATER|HEATING)", layer, re.I))
FLOOR_RE = re.compile(r"^(JF|[1-9]F|ROOF|RF|B1|B2)$")
UNICODE_ESCAPE_RE = re.compile(r"(?:\\U\+|U\+)([0-9A-Fa-f]{4})")


def decode_cad_text(text: str) -> str:
    """补齐 ezdwg 保留在部分属性文本中的 \\U+ 转义。"""
    return UNICODE_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), text)


def peak_rss_mb() -> int:
    if resource is None:
        return 0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(rss / 1048576) if sys.platform == "darwin" else int(rss / 1024)


def sane(*vals) -> bool:
    for v in vals:
        try:
            f = float(v)
        except (TypeError, ValueError):
            return False
        if not (math.isfinite(f) and abs(f) < 1e12):
            return False
    return True


def poly_len(points, bulges, closed) -> float:
    n = len(points)
    if n < 2:
        return 0.0
    total = 0.0
    segs = n if closed else n - 1
    for i in range(segs):
        a, b = points[i], points[(i + 1) % n]
        chord = math.hypot(b[0] - a[0], b[1] - a[1])
        bulge = 0.0
        if bulges and i < len(bulges):
            try:
                bulge = float(bulges[i] or 0.0)
            except (TypeError, ValueError):
                pass
        if abs(bulge) > 1e-9 and chord > 1e-9:
            theta = 4.0 * math.atan(abs(bulge))
            total += chord / (2.0 * math.sin(theta / 2.0)) * theta
        else:
            total += chord
    return total


def infer_unit_from_doc(doc: object, max_segments: int = 5000) -> dict:
    """在 INSUNITS=0 时用图面线段长度中位数给出保守单位候选。

    室外总图常用米作坐标、但 INSUNITS 仍为 0；如果中位数远小于常见毫米
    构件长度，则判为 m。推断结果仍标记为 auto_inferred，不是人工确认。
    """
    lengths: list[float] = []
    try:
        for entity in doc.modelspace().iter_entities():
            dxftype = str(getattr(entity, "dxftype", ""))
            dxf = getattr(entity, "dxf", {}) or {}
            if dxftype == "LINE":
                start, end = dxf.get("start") or (), dxf.get("end") or ()
                if len(start) >= 2 and len(end) >= 2 and sane(start[0], start[1], end[0], end[1]):
                    length = math.hypot(float(end[0]) - float(start[0]), float(end[1]) - float(start[1]))
                    if length > 0:
                        lengths.append(length)
            elif dxftype == "LWPOLYLINE":
                points = [(float(p[0]), float(p[1])) for p in (dxf.get("points") or []) if sane(p[0], p[1])]
                for a, b in zip(points, points[1:]):
                    length = math.hypot(b[0] - a[0], b[1] - a[1])
                    if length > 0:
                        lengths.append(length)
            if len(lengths) >= max_segments:
                break
    except Exception:
        return {"unit": "unknown", "median": None, "sample_count": 0, "reason": "无法读取几何"}
    if len(lengths) < 20:
        return {"unit": "unknown", "median": None, "sample_count": len(lengths),
                "reason": "有效线段不足20条，无法保守推断"}
    lengths.sort()
    median = lengths[len(lengths) // 2]
    # 毫米建筑图常见分段远大于 100 mm；米制总图常见分段小于 100。
    if 0.1 <= median <= 100.0:
        return {"unit": "m", "median": round(median, 4), "sample_count": len(lengths),
                "reason": f"线段长度中位数 {median:.3g}，按室外米制总图推断；请用原图尺寸复核"}
    if median >= 500.0:
        return {"unit": "mm", "median": round(median, 4), "sample_count": len(lengths),
                "reason": f"线段长度中位数 {median:.3g}，按毫米图推断"}
    return {"unit": "unknown", "median": round(median, 4), "sample_count": len(lengths),
            "reason": "单位推断落在灰区，需人工确认"}


def drawing_unit_info(doc: object, requested: str = "auto") -> dict:
    """读取 $INSUNITS，必要时按调用方声明归一化到毫米。

    INSUNITS=0/None 在旧图里很常见；可用图面线段中位数做保守推断，
    但仍把结果标成 auto_inferred，并提示用原图尺寸人工复核。
    """
    header: dict = {}
    try:
        header = doc.header_variables() or {}
    except Exception:
        header = {}
    code = header.get("insunits")
    detected = "unknown"
    # 默认口径：单位来自 $INSUNITS 或用户显式声明，不是推断出来的。
    # 早期版本这里不设默认值，图面线段不足 20 条（纯说明图）或 INSUNITS 直接给了 4/6 时，
    # 走到下面 elif 分支读 status 会 UnboundLocalError 直接崩，整张图扫不出来。
    status = "auto"
    if code == 4:
        detected = "mm"
    elif code == 6:
        detected = "m"
    inference = {"unit": "unknown", "median": None, "sample_count": 0, "reason": ""}
    if requested == "auto" and detected == "unknown":
        inference = infer_unit_from_doc(doc)
        if inference["unit"] in {"m", "mm"}:
            detected = inference["unit"]
            status = "auto_inferred"
    effective = requested if requested != "auto" else detected
    if effective not in {"mm", "m"}:
        effective = "unknown"
    factor = 1000.0 if effective == "m" else (1.0 if effective == "mm" else 1.0)
    if requested != "auto" and effective != "unknown":
        status = "confirmed_by_user"
    elif detected != "unknown":
        status = status if status == "auto_inferred" else "auto"
    else:
        status = "review"
    return {
        "insunits": code,
        "ltscale": header.get("ltscale"),
        "textsize": header.get("textsize"),
        "detected": detected,
        "effective": effective,
        "coord_scale_to_mm": factor,
        "length_scale_to_mm": factor,
        "status": status,
        "unit_inference": inference,
        "review_reason": "" if status != "review" else "INSUNITS=0/未知，图面坐标单位未确认；如已知则用 --unit mm 或 --unit m 重扫",
    }


def _contract_num(value, fallback):
    try:
        f = float(value)
    except (TypeError, ValueError):
        return float(fallback)
    return f if math.isfinite(f) else float(fallback)


def _contract_text(row):
    for key in ("text", "name", "raw", "id", "code"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:240]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
    return ""


def _contract_xy(row):
    x = y = None
    try:
        if row.get("x") is not None:
            x = float(row["x"])
    except (TypeError, ValueError):
        x = None
    try:
        if row.get("y") is not None:
            y = float(row["y"])
    except (TypeError, ValueError):
        y = None
    if x is not None and y is not None:
        return x, y
    for key in ("geometry", "bbox"):
        raw = row.get(key)
        if isinstance(raw, (list, tuple)) and len(raw) >= 2:
            try:
                return float(raw[0]), float(raw[1])
            except (TypeError, ValueError):
                continue
    return x, y


def _contract_geom(row):
    for key in ("geometry", "bbox"):
        raw = row.get(key)
        if isinstance(raw, (list, tuple)) and len(raw) >= 4:
            try:
                out = [float(v) for v in raw[:4]]
                if all(math.isfinite(v) for v in out):
                    return out
            except (TypeError, ValueError):
                continue
    x, y = _contract_xy(row)
    if x is not None and y is not None:
        return [x, y, x, y]
    return []


def contract_unit_info(payload, requested="auto"):
    """契约消费模式不再次打开 DWG：单位优先取契约自带审计，否则按调用方声明。"""
    if requested in ("mm", "m"):
        effective, status = requested, "confirmed_by_user"
    else:
        audit = payload.get("scale_unit_audit") or {}
        detected = ""
        if isinstance(audit, dict):
            detected = str(audit.get("unit") or audit.get("effective") or audit.get("detected") or "").strip()
        elif isinstance(audit, list):
            for rec in audit:
                if isinstance(rec, dict):
                    candidate = str(rec.get("unit") or rec.get("effective") or rec.get("detected") or "").strip()
                    if candidate:
                        detected = candidate
                        break
                    units = rec.get("units")
                    if isinstance(units, (list, tuple)) and units:
                        detected = str(units[0]).strip()
                        break
        detected = detected.strip()
        if detected in ("mm", "m"):
            effective, status = detected, "auto_inferred"
        else:
            effective, status = "unknown", "review"
    factor = 1000.0 if effective == "m" else (1.0 if effective == "mm" else 1.0)
    return {
        "insunits": None,
        "ltscale": None,
        "textsize": None,
        "detected": effective if effective != "unknown" else None,
        "effective": effective,
        "coord_scale_to_mm": factor,
        "length_scale_to_mm": factor,
        "status": status,
        "unit_inference": {
            "unit": effective,
            "median": None,
            "sample_count": 0,
            "reason": "契约消费模式未打开 DWG；单位取自契约审计或调用方显式 --unit 声明。",
        },
        "review_reason": "" if status != "review" else "契约未带单位信息且未指定 --unit mm/m，请回原图核对单位。",
    }


def scan_contract(contract_path, max_text=40000, left_boundary_mm=None, domain="auto", unit="auto",
                  allow_manual=False):
    """识别契约消费模式：只读 cad-file-reader 产出的 MEP 契约 JSON，不直接打开 DWG。

    这是 lis-skill-bus 识图契约红线的算量入口：cad-file-reader 负责识图并产契约，
    本函数只把契约候选转成完整 mep-scan 输出（segments/pipe_segments/devices/texts）。
    契约里的识图/测量候选一律 final_quantity=false，本函数不新增工程量。
    """
    guard = start_mem_guard(name="mep_scan契约闸")
    path = Path(contract_path)
    # 识图契约准入闸：provenance=reader/bus 才是正式；manual 必须显式 allow_manual。
    # 统一映射 contract_guard 1-5 → 入口码 22/24。
    cguard = eg.require_contract(path, allow_manual=bool(allow_manual))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "status": "error", "error": f"{type(exc).__name__}: {exc}",
                "path": str(path), "schema": "anzhuang-suanliang/mep-scan-contract/v0",
                "peak_rss_mb": peak_rss_mb(), "mem_guard": guard}
    if not isinstance(payload, dict):
        return {"ok": False, "status": "error", "error": "契约 JSON 根节点必须是对象",
                "path": str(path), "schema": "anzhuang-suanliang/mep-scan-contract/v0",
                "peak_rss_mb": peak_rss_mb(), "mem_guard": guard}
    contract = payload.get("contract") if isinstance(payload.get("contract"), dict) else {}
    # bus 拉回的是 cad-contract/v1 外壳：{"contract": v0payload, "contract": v0payload["contract"]}；
    # 候选列表在第二层 contract 里，这里统一解包，兼容手工契约与外壳两种形态。
    inner = contract.get("contract") if isinstance(contract.get("contract"), dict) else None
    # 只有内层真的带候选时才下沉；空 candidates 的元数据层会吞掉 text_records/route_segments。
    if isinstance(inner, dict) and isinstance(inner.get("candidates"), list) and inner.get("candidates"):
        contract = inner
    contract_schema = str(contract.get("schema") or payload.get("schema") or "unknown")
    source_file = str(contract.get("source") or payload.get("source_file") or path.name) or path.name
    unit_info = contract_unit_info(payload, unit)
    coord_scale = float(unit_info["coord_scale_to_mm"])
    length_scale = float(unit_info["length_scale_to_mm"])

    def rows(*sections):
        out = []
        for section in sections:
            # bus 外壳下候选段落在解包后的 contract 内；直传契约仍回退到根节点，两种形态都兼容。
            raw = contract.get(section)
            if not isinstance(raw, list):
                raw = payload.get(section)
            if isinstance(raw, list):
                out.extend([r for r in raw if isinstance(r, dict)])
        return out

    route_rows = rows("route_segments", "risers", "vertical_routes", "circuits")
    if not route_rows:
        # 契约里几何候选的 kind 是 line（bbox=线段包框），文本/系统候选才是 route；
        # 两者都收，后面按图层过滤并用 bbox 长度兜底，避免“有几何却识别成 0 段”。
        route_rows = [
            c for c in (contract.get("candidates") or [])
            if isinstance(c, dict) and c.get("kind") in ("route", "line")
        ]
    equip_rows = rows("equipment", "lightning", "fire_protection", "weak_current", "intelligent_building")
    if not equip_rows:
        equip_rows = [c for c in (contract.get("candidates") or []) if isinstance(c, dict) and c.get("kind") == "device"]
    text_rows = rows("labels", "drawing_types", "systems", "notes", "specs", "text_records", "texts", "views")
    if not text_rows:
        text_rows = [c for c in (contract.get("candidates") or []) if isinstance(c, dict) and c.get("kind") in ("text", "block") and _contract_text(c)]

    wire = defaultdict(lambda: {"entities": 0, "length_mm": 0.0})
    segments = []
    pipe_segments = []
    devices = []
    texts = []
    floor_labels = {}
    titleblock_attribs = 0
    contract_counts = defaultdict(int)
    contract_counts["route_rows"] = len(route_rows)
    contract_counts["equipment_rows"] = len(equip_rows)
    contract_counts["text_rows"] = len(text_rows)
    contract_counts["outlier_segments"] = 0
    outlier_rows = []

    for row in route_rows:
        layer = str(row.get("layer") or "")
        geom = _contract_geom(row)
        if len(geom) < 4 or not route_layer(layer, domain):
            continue
        try:
            x1, y1, x2, y2 = float(geom[0]), float(geom[1]), float(geom[2]), float(geom[3])
        except (TypeError, ValueError):
            continue
        if not sane(x1, y1, x2, y2):
            continue
        fallback_len = math.hypot(x2 - x1, y2 - y1)
        seg_len = _contract_num(row.get("length_drawing_units", fallback_len), fallback_len) * length_scale
        if seg_len <= 0:
            continue
        # 单段超长多为块基点/坐标偏移造成的坏几何（实测出现 66 km 单段）；
        # 不静默剔除，计入 outlier_segments 交给复核。
        cap_mm = 200000.0 if domain == "indoor" else 2000000.0
        if seg_len > cap_mm:
            contract_counts["outlier_segments"] += 1
            outlier_rows.append({"layer": layer, "length_mm": round(seg_len, 1),
                                 "geometry": [round(v, 1) for v in (x1, y1, x2, y2)]})
            continue
        wire[layer]["entities"] += 1
        wire[layer]["length_mm"] += seg_len
        segments.append([layer, round(seg_len, 1),
                         round((x1 + x2) / 2 * coord_scale, 1), round((y1 + y2) / 2 * coord_scale, 1),
                         round(x1 * coord_scale, 1), round(y1 * coord_scale, 1),
                         round(x2 * coord_scale, 1), round(y2 * coord_scale, 1)])
        if pipe_layer(layer):
            pipe_segments.append([layer, round(seg_len, 1),
                                  round(x1 * coord_scale, 1), round(y1 * coord_scale, 1), 0.0,
                                  round(x2 * coord_scale, 1), round(y2 * coord_scale, 1), 0.0])

    for row in equip_rows:
        text = _contract_text(row)
        if not text:
            continue
        x, y = _contract_xy(row)
        if x is None or y is None:
            continue
        zone_tag = str(row.get("category") or row.get("tag") or row.get("kind") or "")
        if is_titleblock_attrib(zone_tag, text):
            titleblock_attribs += 1
            continue
        devices.append({"text": text, "tag": zone_tag,
                        "x": round(x * coord_scale, 1), "y": round(y * coord_scale, 1)})

    for row in text_rows:
        text = _contract_text(row)
        x, y = _contract_xy(row)
        if not text or x is None or y is None or len(texts) >= max_text:
            continue
        layer = str(row.get("layer") or "")
        texts.append({"layer": layer, "text": text,
                      "x": round(x * coord_scale, 1), "y": round(y * coord_scale, 1),
                      "h": _contract_num(row.get("height", 0.0), 0.0) * length_scale})
        if FLOOR_RE.match(text):
            floor_labels.setdefault(text, [round(x * coord_scale, 1), round(y * coord_scale, 1)])

    zones = sorted(floor_labels, key=lambda k: floor_labels[k][0])
    xs = [floor_labels[z][0] for z in zones]
    bounds = [0.0] + [(a + b) / 2 for a, b in zip(xs, xs[1:])] + [float("inf")]

    def zone_of(x):
        if left_boundary_mm is not None and x < left_boundary_mm:
            return "左图区"
        for i, z in enumerate(zones):
            if bounds[i] <= x < bounds[i + 1]:
                return z
        return zones[0] if zones else "全图"

    dev_by_zone = defaultdict(lambda: defaultdict(int))
    seg_by_zone = defaultdict(lambda: defaultdict(float))
    for seg in segments:
        seg_by_zone[zone_of(seg[2])][seg[0]] += seg[1]
    for rec in devices:
        dev_by_zone[zone_of(rec["x"])][rec["text"]] += 1

    block_stats = {"ok": True, "scheme": "contract", "expanded": 0, "inserts": 0,
                   "blocks": 0, "note": "契约消费模式不展开块；块内路由已由 cad-file-reader 摊平进 route_segments/equipment/labels。"}
    return {
        "ok": True,
        "schema": "anzhuang-suanliang/mep-scan-contract/v0",
        "contract_schema": contract_schema,
        "contract_file": str(path),
        "recognized_by": "cad-file-reader",
        "file": source_file,
        "path": str(path),
        "entity_counts": {},
        "contract_counts": dict(sorted(contract_counts.items(), key=lambda kv: -kv[1])),
        "outlier_segments": outlier_rows,
        "wire_layers": {k: {"entities": v["entities"], "length_mm": round(v["length_mm"], 1)}
                        for k, v in sorted(wire.items(), key=lambda kv: -kv[1]["length_mm"])},
        "segments": segments,
        "pipe_segments": pipe_segments,
        "inserts": {},
        "attrib_groups": {},
        "devices": devices,
        "texts": texts,
        "floor_labels": floor_labels,
        "wire_by_zone": {z: {k: round(v / 1000, 1) for k, v in sorted(ls.items(), key=lambda kv: -kv[1])}
                         for z, ls in seg_by_zone.items()},
        "devices_by_zone": {z: dict(sorted(d.items(), key=lambda kv: -kv[1]))
                            for z, d in dev_by_zone.items()},
        "domain": domain,
        "drawing_unit": unit_info,
        "geometry_scope": "cad-file-reader_contract",
        "block_reference_count": 0,
        "block_expansion": block_stats,
        "titleblock_attribs_filtered": titleblock_attribs,
        "block_geometry_review": "契约模式不直接读 DWG：识图与块展开均由 cad-file-reader 完成，本输出只消费其契约候选。",
        "cad_reader": cad_reader_info(),
        "peak_rss_mb": peak_rss_mb(),
        "mem_guard": guard,
        **cs.provenance_fields(cguard),
        "contract_warnings": list(cguard.get("warnings") or []),
        "run_manifest": cs.run_manifest("anzhuang-suanliang", _skill_version(), cguard,
                                        argv=_argv_snapshot()),
    }


def _skill_version() -> str:
    try:
        return str(json.loads((Path(__file__).resolve().parents[1] / "manifest.json")
                              .read_text(encoding="utf-8")).get("version") or "")
    except Exception:
        return ""


def _argv_snapshot():
    import sys as _sys
    return list(_sys.argv[1:])


def main() -> None:
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    desc = (__doc__ if lang == "zh" else
            "Consume a cad-file-reader cad-contract/v1 JSON: pipe segments, devices, text, attributes, floor anchors.")
    ap = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("path", nargs="?",
                    help="输入 cad-file-reader 契约 JSON（配 --contract）；直读 DWG 已停用" if lang == "en"
                    else "输入 cad-file-reader 契约 JSON（配合 --contract）；直读 DWG 已停用")
    ap.add_argument("--contract", action="store_true",
                    help="consume cad-file-reader contract JSON, do not open DWG" if lang == "en" else "消费 cad-file-reader 契约 JSON，不直接打开 DWG（正式入口）")
    ap.add_argument("--allow-manual", action="store_true",
                    help="allow manual contract; result is forced final_quantity=false" if lang == "en"
                    else "允许消费手工契约；结果强制 final_quantity=false、formal_ledger_eligible=false")
    ap.add_argument("--check-deps", action="store_true",
                    help="only check cad-file-reader / lis-skill-bus / Python; exit 20/21 when missing" if lang == "en"
                    else "只检查 cad-file-reader / lis-skill-bus / Python 前置；缺 reader=20、缺 bus=21，不读图纸")
    ap.add_argument("--out", help="output JSON path" if lang == "en" else "输出 JSON 路径")
    ap.add_argument("--max-text", type=int, default=40000,
                    help="max text records to keep (default 40000)" if lang == "en" else "最大文本数")
    ap.add_argument("--left-boundary-mm", type=float, default=None,
                    help="x split of an independent drawing zone on the left (e.g. emergency / trunk), in mm" if lang == "en" else "同文件左侧独立图区（应急/桥架等）的 x 分界，单位 mm")
    ap.add_argument("--domain", choices=("auto", "indoor", "outdoor"), default="auto",
                    help="interpretation domain; outdoor for external pipe networks / landscape electric" if lang == "en" else "识图域；室外综合管网/景观电气用 outdoor")
    ap.add_argument("--unit", choices=("auto", "mm", "m"), default="auto",
                    help="drawing coordinate unit; use --unit mm/m when INSUNITS=0" if lang == "en" else "图面坐标单位；INSUNITS=0 时可用 --unit mm/m 显式确认")
    args = ap.parse_args(raw)

    if args.check_deps:
        status = cs.check_deps()
        print(cs.format_deps(status))
        sys.exit(eg.dependency_exit_code())

    # 入口闸门：直接传图纸一律 23；缺 reader=20、缺 bus=21，不自行解图。
    try:
        eg.reject_drawing_input(args.path)
        eg.require_reader()
        eg.require_bus()
    except eg.GateError as exc:
        sys.exit(eg.print_gate_error(exc))

    if not args.path or not args.out:
        sys.stderr.write("[mep_scan] 需要输入契约 JSON 与 --out。\n"
                         "正式链路：cad-file-reader 产出 cad-contract/v1 → 本入口 --contract 消费。\n")
        sys.exit(2)

    if not args.contract:
        sys.stderr.write(
            "[mep_scan] 本入口只消费 cad-file-reader 的 cad-contract/v1 契约，不再直接打开 DWG。\n"
            "请先用 cad-file-reader 生成契约，再用 --contract 指定契约 JSON；直接传图纸返回 23。\n")
        sys.exit(2)

    try:
        result = scan_contract(args.path, args.max_text, args.left_boundary_mm,
                               args.domain, args.unit, allow_manual=args.allow_manual)
    except eg.GateError as exc:
        sys.exit(eg.print_gate_error(exc))
    except GuardError as exc:
        sys.stderr.write("[GuardError %d] %s\n" % (exc.code, exc.message))
        if exc.hint:
            sys.stderr.write("修复: %s\n" % exc.hint)
        sys.exit(exc.code)

    out_doc = {
        "status": "ok" if result.get("ok") else "error",
        "message": ("contract scan completed" if lang == "en" else "契约识别完成") if result.get("ok") else str(result.get("error") or "识别失败"),
        "schema": result.get("schema", "anzhuang-suanliang/mep-scan/v0"),
    }
    result.setdefault("meta", {}).update(out_doc)
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    if not result.get("ok"):
        sys.stderr.write(f"[mep_scan] 识别失败：{result.get('error')}\n")
        sys.exit(1)
    if lang == "en":
        print(f"OK {result['file']} segments={len(result['segments'])} "
              f"texts={len(result['texts'])} peak_rss={result['peak_rss_mb']}MB")
    else:
        print(f"OK {result['file']} 段数={len(result['segments'])} "
              f"文本={len(result['texts'])} 峰值RSS={result['peak_rss_mb']}MB")


if __name__ == "__main__":
    main()
