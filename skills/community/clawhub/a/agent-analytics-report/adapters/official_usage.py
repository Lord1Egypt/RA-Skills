# -*- coding: utf-8 -*-
"""adapters/official_usage.py — 官方用量导出（xlsx）只读适配器（F17 · P0）

为什么需要它
------------
本地 trace 只有「generation 粒度」的模型调用，而且存在两类系统性偏差：

  1. **盲区**：图像模型（hunyuan-image-*）、minimax-m3 等**根本不进 trace**，
     实测 30 日窗口漏记 ¥251.74（占 WorkBuddy 成本 8.7%）。
  2. **标签不分免费/收费**：`hy4-preview` 夜间免费、白天收费，但 trace 的
     `model` 字段**两者都写 `hy4-preview`**。静态价表在数学上无法表达
     「服务端时段减免 / 用户免费额度」，只能按单价 × token 硬算 → 严重高估。

官方用量导出（官网下载的 `request-usage-*.xlsx`）里的「积分消耗」字段是
**服务端实际计费结果**，是唯一真值。本适配器把它读进来，作为 L1 成本口径。

设计约束
--------
  - **纯只读**：只打开用户自己下载的本地文件，不写不传，符合 ADR-4 / ADR-6。
  - **零新增依赖**：xlsx 本质是 zip + XML，用标准库 `zipfile` + `xml` 直接解析，
    不引入 openpyxl（技能要能在任意用户机器上跑）。
  - **按表头名映射，禁止硬编码列位**：官方导出 2026-09-13 起新增 `User Prompt` 列，
    按固定列位解析会把 Prompt 当成模型名（已在调试脚本里踩过）。

导出格式（实测两版）
--------------------
  - 旧版（~2026-09-12）：RequestID / 积分消耗 / 模型 / 客户端 / 时间
  - 新版（2026-09-13 起）：RequestID / 积分消耗 / **User Prompt** / 模型 / 客户端 / 时间
  - 所有单元格均为明文字符串（含积分与时间），无共享字符串、无日期序列值。
  - 图像模型「客户端」列为空字符串。
  - 时间为**北京时间**（trace 是 UTC，对账时需先归一，见 `beijing_date_of`）。
"""

import datetime
import re
import zipfile
from collections import defaultdict
from xml.etree import ElementTree

__all__ = [
    "OfficialUsageError",
    "OFFICIAL_SOURCE",
    "REQUIRED_COLUMNS",
    "HEADER_ALIASES",
    "read_sheet",
    "map_headers",
    "parse_credits",
    "parse_timestamp",
    "load_official_usage",
    "collect_official_usage",
    "reconcile_with_trace",
]

OFFICIAL_SOURCE = "workbuddy-official"

# 工作表默认名（官方导出固定）
DEFAULT_SHEET = "Usage Details"

# 必须有这些列，否则无法解析（缺一列即报错，不做猜测）
REQUIRED_COLUMNS = ("model", "credits", "time")

# 表头别名 → 内部字段名。官方是中文表头，英文别名用于兼容可能的国际版导出。
HEADER_ALIASES = {
    "requestid": "request_id",
    "request_id": "request_id",
    "请求id": "request_id",
    "积分消耗": "credits",
    "积分": "credits",
    "credits": "credits",
    "credit": "credits",
    "模型": "model",
    "model": "model",
    "客户端": "client",
    "client": "client",
    "时间": "time",
    "time": "time",
    "日期": "time",
    "date": "time",
    "user prompt": "prompt",
    "userprompt": "prompt",
    "prompt": "prompt",
    "提示词": "prompt",
}

_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

# 内置日期格式号（不含 0=General）。用于把日期序列值还原成 datetime。
_BUILTIN_DATE_FMTS = set(range(14, 23)) | {27, 30, 36, 45, 46, 47, 50, 57, 58}
_DATE_TOKEN_RE = re.compile(r"(\[[^\]]*\])|(\"[^\"]*\")|('[^']*')")
_EXCEL_EPOCH = datetime.datetime(1899, 12, 30)  # 含 1900 闰年 bug 的补偿值


class OfficialUsageError(Exception):
    """官方用量导出解析失败（文件缺失 / 不是 xlsx / 缺列 / 表头不识别）。"""


# ──────────────────────────────────────────────────────────────
# 1. 极简 xlsx 读取（标准库实现，无第三方依赖）
# ──────────────────────────────────────────────────────────────

def _col_index(cell_ref):
    """'B7' → 1（0-based 列号）；'AA3' → 26。"""
    n = 0
    for ch in cell_ref:
        if not ch.isalpha():
            break
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def _is_date_format(fmt_code):
    """判断一个 numFmt 的 formatCode 是否表示日期/时间。"""
    if not fmt_code:
        return False
    code = _DATE_TOKEN_RE.sub("", fmt_code)
    # 去掉转义与颜色段后仍含日期关键字即为日期格式
    return bool(re.search(r"[ymdhs]", code, re.IGNORECASE))


def _load_shared_strings(zf):
    """读取 xl/sharedStrings.xml（官方导出目前不使用，但通用解析必须支持）。"""
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ElementTree.fromstring(zf.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall(f"{_NS}si"):
        # 拼接所有 t 节点（富文本会把一个字符串拆成多个 run）
        out.append("".join(t.text or "" for t in si.iter(f"{_NS}t")))
    return out


def _load_date_style_ids(zf):
    """返回「样式 id → 是否日期格式」的映射。"""
    if "xl/styles.xml" not in zf.namelist():
        return {}
    root = ElementTree.fromstring(zf.read("xl/styles.xml"))
    custom = {}
    for nf in root.iter(f"{_NS}numFmt"):
        try:
            fid = int(nf.get("numFmtId", "-1"))
        except (TypeError, ValueError):
            continue
        custom[fid] = _is_date_format(nf.get("formatCode"))
    cell_xfs = root.find(f"{_NS}cellXfs")
    out = {}
    if cell_xfs is None:
        return out
    for idx, xf in enumerate(cell_xfs.findall(f"{_NS}xf")):
        try:
            fid = int(xf.get("numFmtId", "0"))
        except (TypeError, ValueError):
            fid = 0
        out[idx] = custom[fid] if fid in custom else (fid in _BUILTIN_DATE_FMTS)
    return out


def _sheet_names(zf):
    """返回 [(sheet_name, zip内路径)]，按 workbook.xml 顺序。"""
    names = {}
    rels = {}
    try:
        rel_root = ElementTree.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        for rel in rel_root:
            rels[rel.get("Id")] = rel.get("Target")
    except (KeyError, ElementTree.ParseError):
        rels = {}
    root = ElementTree.fromstring(zf.read("xl/workbook.xml"))
    out = []
    for sh in root.iter(f"{_NS}sheet"):
        name = sh.get("name") or ""
        target = rels.get(sh.get(f"{_REL_NS}id"), "")
        if target:
            target = target.lstrip("/")
            path = target if target.startswith("xl/") else "xl/" + target
        else:
            path = ""
        if name not in names:
            names[name] = True
            out.append((name, path))
    return out


def read_sheet(path, sheet=None):
    """读取 xlsx 的某个工作表，返回二维字符串列表（缺失单元格补 ''）。

    :param path: xlsx 文件路径
    :param sheet: 工作表名；None 时取第一个工作表
    :raises OfficialUsageError: 文件不存在 / 不是合法 xlsx / 找不到指定工作表
    """
    try:
        zf = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as e:
        raise OfficialUsageError(f"无法打开 xlsx（{path}）：{e}") from e

    with zf:
        try:
            shared = _load_shared_strings(zf)
            date_styles = _load_date_style_ids(zf)
            sheets = _sheet_names(zf)
        except (KeyError, ElementTree.ParseError) as e:
            raise OfficialUsageError(f"xlsx 结构无法解析（{path}）：{e}") from e

        if not sheets:
            raise OfficialUsageError(f"xlsx 中未找到任何工作表：{path}")
        if sheet:
            target = next((p for n, p in sheets if n == sheet), None)
            if target is None:
                avail = "、".join(n for n, _ in sheets)
                raise OfficialUsageError(
                    f"xlsx 中找不到工作表「{sheet}」（可用：{avail}）")
        else:
            target = sheets[0][1] or "xl/worksheets/sheet1.xml"
        if target not in zf.namelist():
            target = "xl/worksheets/sheet1.xml"
        if target not in zf.namelist():
            raise OfficialUsageError(f"xlsx 中找不到工作表数据文件：{path}")

        try:
            ws = ElementTree.fromstring(zf.read(target))
        except (KeyError, ElementTree.ParseError) as e:
            raise OfficialUsageError(f"工作表 XML 解析失败（{path}）：{e}") from e

        rows = []
        for row in ws.iter(f"{_NS}row"):
            cells = []
            for c in row.findall(f"{_NS}c"):
                idx = _col_index(c.get("r", "") or "")
                if idx < 0:
                    continue
                while len(cells) <= idx:
                    cells.append("")
                cells[idx] = _cell_text(c, shared, date_styles)
            rows.append(cells)
        return rows


def _cell_text(cell, shared, date_styles):
    """把一个 <c> 节点转成字符串。"""
    ctype = cell.get("t") or "n"
    if ctype == "inlineStr":
        is_node = cell.find(f"{_NS}is")
        if is_node is None:
            return ""
        return "".join(t.text or "" for t in is_node.iter(f"{_NS}t"))

    v = cell.find(f"{_NS}v")
    raw = v.text if v is not None and v.text is not None else ""
    if ctype == "s":
        try:
            return shared[int(raw)]
        except (ValueError, IndexError):
            return ""
    if ctype == "b":
        return "TRUE" if raw == "1" else "FALSE"
    if ctype in ("str", "e"):
        return raw
    # 数值：若样式是日期格式则还原为 "YYYY-MM-DD HH:MM:SS"
    if raw == "":
        return ""
    try:
        num = float(raw)
    except ValueError:
        return raw
    try:
        style_id = int(cell.get("s", "-1"))
    except (TypeError, ValueError):
        style_id = -1
    if date_styles.get(style_id):
        try:
            return (_EXCEL_EPOCH + datetime.timedelta(days=num)).strftime("%Y-%m-%d %H:%M:%S")
        except (OverflowError, ValueError):
            return raw
    if num == int(num):
        return str(int(num))
    return repr(round(num, 6))


# ──────────────────────────────────────────────────────────────
# 2. 表头映射与字段解析
# ──────────────────────────────────────────────────────────────

def map_headers(header_row):
    """表头行 → {内部字段名: 列索引}。

    按**表头名**匹配（大小写/空格不敏感），不认列位——官方导出会加列。
    """
    idx = {}
    for i, raw in enumerate(header_row):
        key = re.sub(r"\s+", "", str(raw or "")).strip().lower()
        field = HEADER_ALIASES.get(key)
        if field and field not in idx:
            idx[field] = i
    return idx


def _require_columns(cols):
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    if missing:
        zh = {"model": "模型", "credits": "积分消耗", "time": "时间"}
        raise OfficialUsageError(
            "官方导出缺少必需列：" + "、".join(zh[m] for m in missing)
            + f"（实际识别到的表头字段：{sorted(cols)}）")


def parse_credits(raw):
    """积分字符串 → float。空/非数字 → 0.0（官方空值等同未计费）。"""
    if raw is None:
        return 0.0
    s = str(raw).strip().replace(",", "")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        return float(m.group(0)) if m else 0.0


def parse_timestamp(raw):
    """时间字符串 → "YYYY-MM-DD HH:MM:SS"；无法解析时原样返回（不静默丢行）。"""
    s = str(raw or "").strip()
    if not s:
        return ""
    s = s.replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
                "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y/%m/%d"):
        try:
            return datetime.datetime.strptime(s, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return s


def beijing_date_of(ts_text):
    """时间文本 → 北京日期 "YYYY-MM-DD"。官方导出已是北京时间，直接取前 10 位。"""
    s = parse_timestamp(ts_text)
    return s[:10] if len(s) >= 10 else ""


# ──────────────────────────────────────────────────────────────
# 3. 载入与聚合
# ──────────────────────────────────────────────────────────────

def load_official_usage(path, sheet=None):
    """读取官方导出，返回 (rows, meta)。

    rows: [{request_id, credits, model, client, ts, date, hour, is_free, prompt}]
    meta: {file, sheet, columns, total_rows, skipped, window}
    """
    rows_raw = read_sheet(path, sheet=sheet)
    if not rows_raw:
        raise OfficialUsageError(f"官方导出为空（无表头行）：{path}")

    cols = map_headers(rows_raw[0])
    _require_columns(cols)

    out = []
    skipped = 0
    for r in rows_raw[1:]:
        model = str(r[cols["model"]] if cols["model"] < len(r) else "").strip()
        if not model:
            skipped += 1
            continue
        ts = parse_timestamp(r[cols["time"]] if cols["time"] < len(r) else "")
        credits = parse_credits(r[cols["credits"]] if cols["credits"] < len(r) else "")
        out.append({
            "request_id": str(r[cols["request_id"]] if cols.get("request_id", -1) < len(r)
                              and cols.get("request_id", -1) >= 0 else "").strip(),
            "credits": credits,
            "model": model,
            "client": str(r[cols["client"]] if cols.get("client", -1) < len(r)
                          and cols.get("client", -1) >= 0 else "").strip(),
            "ts": ts,
            "date": ts[:10],
            "hour": int(ts[11:13]) if len(ts) >= 13 and ts[11:13].isdigit() else -1,
            "is_free": credits <= 0,
            "prompt": str(r[cols["prompt"]] if cols.get("prompt", -1) < len(r)
                          and cols.get("prompt", -1) >= 0 else "").strip(),
        })

    dates = sorted(d["date"] for d in out if d["date"])
    meta = {
        "file": str(path),
        "sheet": sheet or DEFAULT_SHEET,
        "columns": dict(cols),
        "total_rows": len(rows_raw) - 1,
        "parsed_rows": len(out),
        "skipped_rows": skipped,
        "window": {"first": dates[0] if dates else "", "last": dates[-1] if dates else ""},
    }
    return out, meta


def collect_official_usage(path, start_date=None, end_date=None, sheet=None):
    """官方导出 → canonical 结构（供报告渲染与双源对账）。

    :param path: xlsx 路径
    :param start_date / end_date: 可选 "YYYY-MM-DD"，按**北京日期**过滤（含端点）
    :return: dict（source / rows / by_model / by_client / by_day / totals / meta）
    """
    rows, meta = load_official_usage(path, sheet=sheet)

    if start_date or end_date:
        rows = [r for r in rows
                if r["date"] and (not start_date or r["date"] >= start_date)
                and (not end_date or r["date"] <= end_date)]

    by_model = _group(rows, lambda r: r["model"])
    by_client = _group(rows, lambda r: r["client"] or "(空)")
    by_day = _group(rows, lambda r: r["date"] or "(未知)")

    totals = {
        "requests": len(rows),
        "credits": round(sum(r["credits"] for r in rows), 2),
        "free_requests": sum(1 for r in rows if r["is_free"]),
        "paid_requests": sum(1 for r in rows if not r["is_free"]),
        "models": len(by_model),
        "clients": len(by_client),
    }
    dates = sorted(r["date"] for r in rows if r["date"])
    return {
        "source": OFFICIAL_SOURCE,
        "rows": rows,
        "by_model": by_model,
        "by_client": by_client,
        "by_day": by_day,
        "totals": totals,
        "filter": {"start_date": start_date, "end_date": end_date},
        "meta": dict(meta, window={
            "first": dates[0] if dates else "", "last": dates[-1] if dates else ""}),
    }


def _group(rows, keyfn):
    """按 keyfn 聚合，返回按 credits 降序的列表。"""
    agg = defaultdict(lambda: {"requests": 0, "credits": 0.0,
                               "free_requests": 0, "paid_requests": 0})
    for r in rows:
        g = agg[keyfn(r)]
        g["requests"] += 1
        g["credits"] += r["credits"]
        if r["is_free"]:
            g["free_requests"] += 1
        else:
            g["paid_requests"] += 1
    out = []
    for name, g in agg.items():
        out.append({
            "name": name,
            "requests": g["requests"],
            "credits": round(g["credits"], 2),
            "free_requests": g["free_requests"],
            "paid_requests": g["paid_requests"],
            "avg_credits": round(g["credits"] / g["requests"], 2) if g["requests"] else 0.0,
        })
    out.sort(key=lambda x: (-x["credits"], -x["requests"], x["name"]))
    return out


# ──────────────────────────────────────────────────────────────
# 4. 双源对账
# ──────────────────────────────────────────────────────────────

def collapse_display_aliases(by_model, alias_map):
    """把官方模型名按 `display_merge` 归拢到基础名，与 trace 侧的显示口径对齐。

    为什么必须做：trace 侧已把「收费版变体」合并显示为基名（如 `hy3-x` → `hy3`，
    见 `ca_core.merge_display_key`）。若官方侧不过同一层映射，`hy3-x` 会因精确匹配
    不上而被**误判成 trace 盲区**。

    实测（2026-08-13~09-12，30 日）：不归拢时 `hy3-x`(97 请求 / 397.43 积分) 与
    `hy4-preview-x`(1 / 13.52) 被误报为盲区，虚报 410.95 积分 —— 占 missing_credits
    的 75.7%，而真实盲区（图像模型）只有 131.35。

    :return: ({基础名: {requests, credits, variants}}, {变体名: 基础名})
    """
    if not alias_map:
        return ({m["name"]: dict(m, variants=[]) for m in by_model}, {})

    # 键按小写索引（与 ca_core.merge_display_key 的 normalize_model 口径一致），
    # 官方导出里的大小写差异不影响归并；值是**原始写法**的基础名，保证显示一致。
    lookup = {str(k).strip().lower(): v for k, v in alias_map.items()}

    merged = {}
    alias_of = {}
    for m in by_model:
        base = lookup.get(m["name"].strip().lower(), m["name"])
        alias_of[m["name"]] = base
        slot = merged.setdefault(base, {"name": base, "requests": 0, "credits": 0.0,
                                        "variants": []})
        slot["requests"] += m["requests"]
        slot["credits"] = round(slot["credits"] + m["credits"], 2)
        if base != m["name"]:
            slot["variants"].append(m["name"])
    return merged, alias_of


def reconcile_with_trace(official, trace_model_stats, trace_total_calls=0, alias_map=None):
    """官方导出（请求/积分真值）与本地 trace（generation 粒度）对账。

    :param official: collect_official_usage() 的产物
    :param trace_model_stats: model_stats（aggregate_by_exec_model 输出，含 model/calls/total_cost）
    :param trace_total_calls: trace generation 总数
    :param alias_map: `display_merge` 映射（变体名 -> 基础名）。传入后官方侧先归拢，
        与 trace 侧显示口径对齐，避免把 `hy3-x` 这类变体误判成 trace 盲区。
    :return: {
        official_requests, trace_generations, ratio,
        missing_in_trace: [...],   # 官方有、trace 无 → 成本被低估
        trace_only: [...],         # trace 有、官方无 → 本地/免费/路由
        both: [...],               # 两边都有，给倍数
    }
    """
    off_by_model, _ = collapse_display_aliases(
        (official or {}).get("by_model", []), alias_map)
    trace_by_model = {}
    for m in trace_model_stats or []:
        name = (m.get("model") or "").strip()
        if not name:
            continue
        cur = trace_by_model.setdefault(name, {"calls": 0, "cost": 0.0})
        cur["calls"] += int(m.get("calls", 0) or 0)
        cur["cost"] += float(m.get("total_cost", 0.0) or 0.0)

    off_total = int((official or {}).get("totals", {}).get("requests", 0) or 0)
    trace_total = int(trace_total_calls or sum(v["calls"] for v in trace_by_model.values()))

    missing, trace_only, both = [], [], []
    for name in sorted(set(off_by_model) | set(trace_by_model)):
        o = off_by_model.get(name)
        t = trace_by_model.get(name)
        if o and not t:
            missing.append({
                "model": name, "official_requests": o["requests"],
                "official_credits": o["credits"],
                "variants": o.get("variants") or [],
            })
        elif t and not o:
            trace_only.append({
                "model": name, "trace_generations": t["calls"],
                "trace_est_cost": round(t["cost"], 2),
            })
        elif o and t:
            both.append({
                "model": name, "official_requests": o["requests"],
                "trace_generations": t["calls"],
                "official_credits": o["credits"],
                "trace_est_cost": round(t["cost"], 2),
                "variants": o.get("variants") or [],
            })

    missing.sort(key=lambda x: -x["official_credits"])
    trace_only.sort(key=lambda x: -x["trace_generations"])
    both.sort(key=lambda x: -x["official_credits"])

    return {
        "official_requests": off_total,
        "trace_generations": trace_total,
        "ratio": round(trace_total / off_total, 1) if off_total else 0.0,
        "missing_in_trace": missing,
        "missing_credits": round(sum(m["official_credits"] for m in missing), 2),
        "trace_only": trace_only,
        "both": both,
    }
