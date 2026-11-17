#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从中文 PDF / 扫描件 / Excel / Word / CSV 中抽取结构化表格与字段。

用法::

    python scripts/extract_tables.py --input statement.pdf
    python scripts/extract_tables.py --input statement.pdf --profile bank_statement --out ./out
    python scripts/extract_tables.py --input payroll.xlsx --sheet 工资表 --out ./out
    python scripts/extract_tables.py --input doc.docx --out ./out
    python scripts/extract_tables.py --input data.csv --profile generic --out ./out
    python scripts/extract_tables.py --list-profiles
    python scripts/extract_tables.py --selftest

输出
----
``--out`` 目录中生成两个文件：

* ``records.json`` —— 完整记录集，含每字段的证据坐标（页/表/行/列）与原文串
* ``records.csv``  —— 扁平化后的记录表，便于人工快速查看

设计原则
--------
1. 只做"抽取"，不做"猜测"：读不到的字段保持缺失，原始字符串永远保留在 raw 里。
2. 每个字段都能指回原文位置（page / sheet / table_id / row / col）。
3. 缺少第三方库时给出明确的安装提示并以非零码退出，绝不 traceback 崩溃，
   也绝不静默返回空结果。
4. 归一化（金额转 float、日期转 ISO）只写入 value，raw 保持原样。
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
except Exception:  # pragma: no cover - 旧版本 Python
    pass

from field_library import (  # noqa: E402
    PROFILES,
    get_profile,
    is_null_token,
    label_for,
    match_header,
    normalize_header,
    normalize_text,
    parse_amount,
    parse_date,
)

SCHEMA_VERSION = "1.0"

# --------------------------------------------------------------------------
# 依赖探测：全部 try/except，缺库时给出安装提示
# --------------------------------------------------------------------------

MISSING = {}


def _require(module, pip_name, why):
    """尝试导入模块，失败时登记缺失信息（不抛异常）。"""
    try:
        return __import__(module)
    except ImportError:
        MISSING[module] = (pip_name, why)
        return None


def dependency_report():
    """返回 (是否全部可用, 可读提示文本)。"""
    if not MISSING:
        return True, "所有可选依赖均可用。"
    lines = ["缺少以下依赖，无法处理对应格式："]
    for module, (pip_name, why) in sorted(MISSING.items()):
        lines.append("  - %s（pip 包名：%s）—— %s" % (module, pip_name, why))
    lines.append("")
    lines.append("安装命令：")
    for module, (pip_name, _why) in sorted(MISSING.items()):
        lines.append("  pip install %s" % pip_name)
    return False, "\n".join(lines)


# --------------------------------------------------------------------------
# 通用工具
# --------------------------------------------------------------------------

def now_iso():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cell_text(value):
    if value is None:
        return ""
    if isinstance(value, _dt.datetime):
        return value.strftime("%Y-%m-%d") if not (value.hour or value.minute or value.second) \
            else value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, _dt.date):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, float):
        # 避免 1234.0 与 1234 在文本表头判定上的差异
        if value.is_integer():
            return str(int(value))
        return repr(value)
    return normalize_text(value)


def is_blank_row(row):
    return all(is_null_token(cell_text(c)) for c in row)


def detect_header(rows, max_scan=5):
    """在前 max_scan 行中挑选表头行。

    判定标准（全部满足才算表头候选）：
    * 至少 2 个非空单元格
    * 候选行的单元格不是全是数字（全是数字说明它是数据行，不是表头）
    * 下一行的非空单元格数量与候选行相当（>= 候选行的 60%），说明下面确实有数据
    返回 (表头行下标 或 None, 候选信息列表)
    """
    candidates = []
    for idx, row in enumerate(rows[:max_scan]):
        non_empty = [c for c in row if not is_null_token(cell_text(c))]
        if len(non_empty) < 2:
            candidates.append((idx, 0, False))
            continue
        all_numeric = True
        for c in non_empty:
            _v, status, _n = parse_amount(c)
            if status != "ok":
                all_numeric = False
                break
        nxt = rows[idx + 1] if idx + 1 < len(rows) else []
        nxt_count = len([c for c in nxt if not is_null_token(cell_text(c))])
        ratio_ok = nxt_count >= max(1, int(len(non_empty) * 0.6))
        candidates.append((idx, len(non_empty), (not all_numeric) and ratio_ok))
    best = None
    for idx, count, ok in candidates:
        if ok and count >= 2:
            if best is None or count > candidates[best][1]:
                best = idx
    return best, candidates


def map_headers(header_cells, profile):
    """表头 -> canonical key。返回 (映射列表, 未映射列名列表)。"""
    mapping = []
    unmapped = []
    used = set()
    for col, raw_header in enumerate(header_cells):
        text = cell_text(raw_header)
        if is_null_token(text):
            mapping.append((col, None, None))
            continue
        key, alias = match_header(text, profile)
        if key and key not in used:
            used.add(key)
            mapping.append((col, key, alias))
        elif key and key in used:
            # 同名重复列：加后缀避免覆盖
            suffix = 2
            new_key = "%s_%d" % (key, suffix)
            while new_key in used:
                suffix += 1
                new_key = "%s_%d" % (key, suffix)
            used.add(new_key)
            mapping.append((col, new_key, alias))
        else:
            unmapped.append(text)
            mapping.append((col, None, None))
    return mapping, unmapped


def build_record(fields, table_id, row_index, page=None, sheet=None, start_row=1):
    """组装一条带证据的记录。"""
    record = {
        "record_id": "",
        "table_id": table_id,
        "row": row_index,
        "fields": {},
        "issues": [],
    }
    for key, cell in fields.items():
        entry = {
            "value": cell.get("value"),
            "raw": cell.get("raw", ""),
            "evidence": {
                "table_id": table_id,
                "row": row_index,
                "col": cell.get("col"),
                "raw": cell.get("raw", ""),
            },
            "status": cell.get("status", "ok"),
        }
        if page is not None:
            entry["evidence"]["page"] = page
        if sheet is not None:
            entry["evidence"]["sheet"] = sheet
        if cell.get("note"):
            entry["note"] = cell["note"]
        record["fields"][key] = entry
    return record


def normalize_field_value(key, raw_text, profile, profile_def):
    """按字段类型归一化，返回 (value, status, note)。"""
    if is_null_token(raw_text):
        return None, "missing", None
    if key in profile_def.get("amount_fields", []):
        value, status, note = parse_amount(raw_text)
        if status == "missing":
            return None, "missing", None
        return value, ("ok" if status != "invalid" else "invalid"), note
    if key in profile_def.get("date_fields", []):
        value, status, note = parse_date(raw_text)
        return value, status, note
    # 通用：日期类字段名也尝试解析日期
    if "date" in key or "日期" in key:
        value, status, note = parse_date(raw_text)
        if status == "ok":
            return value, "ok", note
    return raw_text, "ok", None


def detect_key_value_form(rows, profile):
    """识别"标签-值"竖排表单（常见于 Word 保单、PDF 合同、发票票面）。

    判定标准：
    * 表只有 2 列（标签列 + 值列）
    * 至少 2 行
    * 标签列中至少 2 个单元格能命中字段别名表
    * 值列不命中别名（否则它更像普通数据表）

    返回 (字段映射字典 或 None, 命中标签数)
    字段映射字典的 key 是 canonical key，value 是 (原始标签, 单元格值, 行下标)
    """
    if len(rows) < 2:
        return None, 0
    width = max(len(r) for r in rows)
    if width != 2:
        return None, 0
    mapping = {}
    label_hits = 0
    for ridx, row in enumerate(rows):
        if len(row) < 2:
            continue
        label_text = cell_text(row[0])
        if is_null_token(label_text):
            continue
        key, _alias = match_header(label_text, profile)
        value_text = cell_text(row[1])
        if key and not is_null_token(value_text):
            vkey, _va = match_header(value_text, profile)
            if vkey and vkey != key:
                # 值列也命中别名 -> 这不是标签-值表单
                continue
            if key not in mapping:
                mapping[key] = (label_text, value_text, ridx)
                label_hits += 1
    if label_hits < 2:
        return None, label_hits
    return mapping, label_hits


def detect_footer_row(row, footer_keywords):
    """判断一行是否是合计/小计行。"""
    for cell in row[:3]:
        text = cell_text(cell)
        if not text:
            continue
        for kw in footer_keywords:
            if kw in text:
                return kw
    return None


# --------------------------------------------------------------------------
# 各格式的抽取器
# --------------------------------------------------------------------------

def extract_csv(path, options):
    encodings = [options.encoding] if options.encoding else ["utf-8-sig", "utf-8", "gb18030", "gbk"]
    last_err = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc, newline="") as fh:
                rows = [list(r) for r in csv.reader(fh)]
            break
        except UnicodeDecodeError as exc:
            last_err = exc
            continue
    else:
        raise RuntimeError("CSV 解码失败（尝试过 %s）：%s" % (", ".join(encodings), last_err))

    tables = []
    if rows:
        tables.append({
            "table_id": "csv_t1",
            "sheet": None,
            "page": None,
            "rows": rows,
            "note": "csv 单表",
        })
    return {"source_type": "csv", "tables": tables, "pages": 1, "sheets": [], "extra": {}}


def extract_xlsx(path, options):
    openpyxl = _require("openpyxl", "openpyxl", "读取 .xlsx / .xlsm 工作簿")
    if openpyxl is None:
        return None
    import warnings
    warnings.filterwarnings("ignore")

    wb = openpyxl.load_workbook(path, data_only=True, read_only=False)
    tables = []
    sheet_names = list(wb.sheetnames)
    wanted = options.sheet
    if wanted and wanted not in sheet_names:
        raise RuntimeError("指定的工作表 %r 不存在，可用工作表：%s" % (wanted, ", ".join(sheet_names)))
    for sname in sheet_names:
        if wanted and sname != wanted:
            continue
        ws = wb[sname]
        rows = []
        for row in ws.iter_rows(values_only=True):
            rows.append(list(row))
        # 去掉尾部全空行
        while rows and is_blank_row(rows[-1]):
            rows.pop()
        if not rows:
            continue
        table_id = "sheet_%s" % re.sub(r"\W+", "_", sname)
        tables.append({
            "table_id": table_id,
            "sheet": sname,
            "page": None,
            "rows": rows,
            "note": "sheet %s (%d 行 x %d 列)" % (sname, len(rows), ws.max_column or 0),
        })
    try:
        wb.close()
    except Exception:
        pass
    return {"source_type": "xlsx", "tables": tables, "pages": None, "sheets": sheet_names, "extra": {}}


def extract_pdf(path, options):
    pdfplumber = _require("pdfplumber", "pdfplumber", "读取 PDF 文本层与表格线")
    if pdfplumber is None:
        return None
    tables = []
    page_count = 0
    low_confidence = []
    with pdfplumber.open(path) as pdf:
        page_count = len(pdf.pages)
        for pno, page in enumerate(pdf.pages, start=1):
            try:
                found = page.extract_tables()
            except Exception as exc:  # 单页失败不应中断整份文档
                low_confidence.append("p%d 抽取异常：%s" % (pno, exc))
                found = []
            for tidx, table in enumerate(found, start=1):
                rows = [list(r) for r in table]
                if not rows:
                    continue
                table_id = "p%d_t%d" % (pno, tidx)
                usable = sum(
                    1 for r in rows for c in r if not is_null_token(cell_text(c))
                )
                total = sum(len(r) for r in rows) or 1
                ratio = usable / float(total)
                lc = ratio < 0.5
                if lc:
                    low_confidence.append(
                        "%s 可用单元格比例 %.0f%%（疑似矢量文本无表格线或扫描件无框线）" % (table_id, ratio * 100)
                    )
                tables.append({
                    "table_id": table_id,
                    "sheet": None,
                    "page": pno,
                    "rows": rows,
                    "low_confidence": lc,
                    "note": "page %d table %d，%d 行 x %d 列" % (pno, tidx, len(rows), max(len(r) for r in rows)),
                })
    extra = {"low_confidence": low_confidence}
    return {"source_type": "pdf", "tables": tables, "pages": page_count, "sheets": [], "extra": extra}


def extract_docx(path, options):
    docx_mod = _require("docx", "python-docx", "读取 .docx 中的表格对象与文本框")
    if docx_mod is None:
        return None
    document = docx_mod.Document(path)
    tables = []
    for tidx, table in enumerate(document.tables, start=1):
        rows = []
        for row in table.rows:
            rows.append([c.text for c in row.cells])
        if not rows:
            continue
        tables.append({
            "table_id": "docx_t%d" % tidx,
            "sheet": None,
            "page": None,
            "rows": rows,
            "note": "Word 表格 %d，%d 行 x %d 列" % (tidx, len(rows), len(rows[0]) if rows else 0),
        })

    # 文本框内容：Word 常把票号/保单号放在文本框里
    text_blocks = []
    try:
        from docx.oxml.ns import qn
        body = document.element.body
        for i, txbx in enumerate(body.iter(qn("w:txbxContent")), start=1):
            lines = []
            for para in txbx.iter(qn("w:p")):
                txt = "".join(node.text or "" for node in para.iter(qn("w:t")))
                if txt.strip():
                    lines.append(normalize_text(txt))
            if lines:
                text_blocks.append({"index": i, "lines": lines})
    except Exception:
        text_blocks = []

    extra = {"text_blocks": text_blocks}
    return {"source_type": "docx", "tables": tables, "pages": None, "sheets": [], "extra": extra}


EXTRACTORS = {
    "csv": extract_csv,
    "xlsx": extract_xlsx,
    "pdf": extract_pdf,
    "docx": extract_docx,
}

EXT_BY_SUFFIX = {
    ".csv": "csv", ".tsv": "csv",
    ".xlsx": "xlsx", ".xlsm": "xlsx",
    ".pdf": "pdf",
    ".docx": "docx",
}


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------

def run_extraction(input_path, profile_key, options):
    suffix = os.path.splitext(input_path)[1].lower()
    source_type = options.type or EXT_BY_SUFFIX.get(suffix)
    if source_type is None:
        raise RuntimeError(
            "无法识别文件类型（扩展名 %s）。请用 --type 指定：pdf / xlsx / docx / csv" % (suffix or "<无>")
        )
    if source_type not in EXTRACTORS:
        raise RuntimeError("不支持的类型 %r，可选：pdf / xlsx / docx / csv" % source_type)

    profile_def = get_profile(profile_key)

    if source_type == "csv":
        raw = extract_csv(input_path, options)
    elif source_type == "xlsx":
        raw = extract_xlsx(input_path, options)
    elif source_type == "pdf":
        raw = extract_pdf(input_path, options)
    else:
        raw = extract_docx(input_path, options)

    if raw is None:
        ok, msg = dependency_report()
        raise RuntimeError(msg)

    records = []
    footer_rows = []
    rejected_tables = []
    unmapped_columns = []
    dropped_header_rows = 0
    seq = 0

    for tbl in raw["tables"]:
        rows = tbl["rows"]
        # 丢弃尾部空行
        while rows and is_blank_row(rows[-1]):
            rows.pop()
        if not rows:
            rejected_tables.append({
                "table_id": tbl["table_id"],
                "reason": "empty",
                "detail": tbl.get("note", ""),
            })
            continue
        if len(rows) < 2 or max(len(r) for r in rows) < 2:
            rejected_tables.append({
                "table_id": tbl["table_id"],
                "reason": "too_small",
                "detail": "%d 行 x %d 列" % (len(rows), max(len(r) for r in rows)),
            })
            continue

        kv_mapping, kv_hits = detect_key_value_form(rows, profile_key)
        if kv_mapping:
            # 标签-值竖排表单：整张表构成一条记录
            fields = {}
            for key, (label_text, value_text, ridx) in kv_mapping.items():
                value, status, note = normalize_field_value(key, value_text, profile_key, profile_def)
                fields[key] = {
                    "value": value,
                    "raw": value_text,
                    "col": 2,
                    "status": status,
                    "note": note,
                    "label": label_text,
                }
            if fields:
                seq += 1
                record = build_record(
                    fields,
                    tbl["table_id"],
                    1,
                    page=tbl.get("page"),
                    sheet=tbl.get("sheet"),
                )
                record["record_id"] = "r%03d" % seq
                record["form"] = "key_value"
                records.append(record)
            continue

        header_idx, _cands = detect_header(rows)
        header_detected = header_idx is not None
        if header_detected:
            header_cells = rows[header_idx]
            data_start = header_idx + 1
        else:
            width = max(len(r) for r in rows)
            header_cells = ["列%d" % (i + 1) for i in range(width)]
            data_start = 0
            unmapped_columns.append("%s: 未检测到表头，使用位置列名" % tbl["table_id"])

        mapping, unmapped = map_headers(header_cells, profile_key)
        for name in unmapped:
            unmapped_columns.append("%s: %s" % (tbl["table_id"], name))

        table_records = []
        for offset, row in enumerate(rows[data_start:], start=1):
            if is_blank_row(row):
                continue
            kw = detect_footer_row(row, profile_def["footer_keywords"])
            if kw:
                footer_fields = {}
                for col, key, _alias in mapping:
                    if key is None or col >= len(row):
                        continue
                    cell_raw = cell_text(row[col])
                    if kw in cell_raw and len(cell_raw) <= len(kw) + 2:
                        continue  # 合计字样本身不是字段值
                    footer_fields[key] = cell_raw
                footer_rows.append({
                    "table_id": tbl["table_id"],
                    "row": data_start + offset,
                    "keyword": kw,
                    "cells": [cell_text(c) for c in row],
                    "fields": footer_fields,
                    "page": tbl.get("page"),
                    "sheet": tbl.get("sheet"),
                })
                continue
            # 跳过重复表头
            non_empty = [cell_text(c) for c in row if not is_null_token(cell_text(c))]
            if non_empty and all(
                any(normalize_header(cell_text(c)) == normalize_header(cell_text(h))
                    for h in header_cells if not is_null_token(cell_text(h)))
                for c in non_empty
            ):
                dropped_header_rows += 1
                continue

            fields = {}
            for col, key, _alias in mapping:
                if key is None or col >= len(row):
                    continue
                raw_text = cell_text(row[col])
                value, status, note = normalize_field_value(key, raw_text, profile_key, profile_def)
                fields[key] = {
                    "value": value,
                    "raw": raw_text,
                    "col": col + 1,
                    "status": status,
                    "note": note,
                }
            if not fields:
                continue
            seq += 1
            record = build_record(
                fields,
                tbl["table_id"],
                data_start + offset,
                page=tbl.get("page"),
                sheet=tbl.get("sheet"),
            )
            record["record_id"] = "r%03d" % seq
            table_records.append(record)

        if not table_records and tbl["rows"]:
            rejected_tables.append({
                "table_id": tbl["table_id"],
                "reason": "no_data_rows",
                "detail": tbl.get("note", ""),
            })
        records.extend(table_records)

    result = {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "file": os.path.basename(input_path),
            "path": os.path.abspath(input_path),
            "type": raw["source_type"],
            "pages": raw.get("pages"),
            "sheets": raw.get("sheets") or [],
            "profile": profile_key,
            "profile_zh": profile_def["zh"],
            "extracted_at": now_iso(),
        },
        "summary": {
            "tables_detected": len([t for t in raw["tables"]]),
            "tables_rejected": len(rejected_tables),
            "records": len(records),
            "records_with_issues": 0,
            "validation_status": "not_run",
        },
        "records": records,
        "footer_rows": footer_rows,
        "unverified_fields": [],
        "rejected_tables": rejected_tables,
        "unmapped_columns": unmapped_columns,
        "dropped_header_rows": dropped_header_rows,
        "notes": raw.get("extra", {}).get("low_confidence", []),
        "text_blocks": raw.get("extra", {}).get("text_blocks", []),
    }
    return result


def write_outputs(result, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "records.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    csv_path = os.path.join(out_dir, "records.csv")
    keys = []
    for rec in result["records"]:
        for key in rec["fields"]:
            if key not in keys:
                keys.append(key)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["record_id", "table_id", "row", "page", "sheet"] + keys)
        for rec in result["records"]:
            base = [
                rec["record_id"], rec["table_id"], rec["row"],
                rec["fields"] and next((f["evidence"].get("page") for f in rec["fields"].values() if f["evidence"].get("page")), "") or "",
                next((f["evidence"].get("sheet") for f in rec["fields"].values() if f["evidence"].get("sheet")), "") or "",
            ]
            values = []
            for key in keys:
                entry = rec["fields"].get(key)
                values.append("" if entry is None else ("" if entry.get("value") is None else entry.get("value")))
            writer.writerow(base + values)
    return json_path, csv_path


def print_summary(result):
    src = result["source"]
    print("来源文件   : %s（%s）" % (src["file"], src["type"]))
    if src.get("pages"):
        print("页数       : %d" % src["pages"])
    if src.get("sheets"):
        print("工作表     : %s" % ", ".join(src["sheets"]))
    print("文档画像   : %s / %s" % (src["profile"], src["profile_zh"]))
    print("检出表格   : %d（丢弃 %d）" % (result["summary"]["tables_detected"], result["summary"]["tables_rejected"]))
    print("记录条数   : %d" % result["summary"]["records"])
    print("合计行     : %d" % len(result["footer_rows"]))
    print("丢弃重复表头: %d" % result["dropped_header_rows"])
    if result["unmapped_columns"]:
        print("未映射列   :")
        for item in result["unmapped_columns"][:20]:
            print("  - %s" % item)
    if result["notes"]:
        print("低置信提示 :")
        for item in result["notes"][:10]:
            print("  - %s" % item)


SELFTEST_CSV = (
    "交易日期,摘要,借方发生额,贷方发生额,余额,对方户名,流水号\n"
    '2024-01-05,货款汇入,,"12,345.60","150,000.00",示例制造有限公司,TX20240105001\n'
    '2024-01-06,手续费,"25.00",,"149,975.00",示例制造有限公司,TX20240106002\n'
    '2024年1月8日,货款汇入,,"8,000.00","157,975.00",示例贸易有限公司,TX20240108003\n'
)


def selftest():
    """用内置样例 CSV 跑通整条链路。"""
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="cn_doc_extract_selftest_")
    csv_path = os.path.join(tmpdir, "sample_statement.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(SELFTEST_CSV)
    out_dir = os.path.join(tmpdir, "out")
    result = run_extraction(csv_path, "bank_statement", argparse.Namespace(
        encoding="utf-8", type=None, sheet=None))
    json_path, csv_path_out = write_outputs(result, out_dir)
    print_summary(result)
    rec = result["records"][0]
    print("")
    print("首条记录示例：")
    for key, entry in list(rec["fields"].items()):
        print("  %-22s value=%-14r raw=%-14r %s" % (
            label_for(key), entry.get("value"), entry.get("raw"), entry.get("status")))
    ok = (
        result["summary"]["records"] == 3
        and rec["fields"]["credit_amount"]["value"] == 12345.60
        and rec["fields"]["balance"]["value"] == 150000.00
    )
    print("")
    print("输出文件：%s / %s" % (json_path, csv_path_out))
    print("SELFTEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def build_parser():
    p = argparse.ArgumentParser(
        prog="extract_tables.py",
        description="从中文 PDF / Excel / Word / CSV 抽取结构化表格与字段，输出带溯源证据的 JSON + CSV。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python scripts/extract_tables.py --input statement.pdf --profile bank_statement --out ./out
  python scripts/extract_tables.py --input payroll.xlsx --sheet 工资表 --out ./out
  python scripts/extract_tables.py --input doc.docx --out ./out
  python scripts/extract_tables.py --list-profiles
  python scripts/extract_tables.py --selftest
""",
    )
    p.add_argument("--input", "-i", help="源文件路径（.pdf/.png 走 OCR 预处理后的 PDF，.xlsx/.docx/.csv）")
    p.add_argument("--out", "-o", help="输出目录，默认 ./out_extracted")
    p.add_argument("--profile", "-p", default="generic",
                   help="文档画像：%s（默认 generic）" % "、".join(PROFILES.keys()))
    p.add_argument("--type", choices=["pdf", "xlsx", "docx", "csv"],
                   help="强制指定文件类型，默认按扩展名判断")
    p.add_argument("--sheet", help="仅处理指定工作表（xlsx）")
    p.add_argument("--encoding", default="utf-8-sig", help="CSV 编码，默认 utf-8-sig（gb18030 亦可）")
    p.add_argument("--list-profiles", action="store_true", help="列出所有文档画像及其必填字段")
    p.add_argument("--selftest", action="store_true", help="用内置样例 CSV 自检整条链路")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_profiles:
        for key, prof in PROFILES.items():
            req = "、".join(prof["required"]) or "（无必填）"
            print("%-16s %s" % (key, prof["zh"]))
            print("%-16s 必填字段：%s" % ("", req))
        return 0

    if args.selftest:
        return selftest()

    if not args.input:
        parser.print_usage()
        print("错误：缺少 --input。示例：python scripts/extract_tables.py --input statement.pdf --out ./out")
        return 2

    if not os.path.exists(args.input):
        print("错误：文件不存在：%s" % args.input)
        return 2

    if args.profile not in PROFILES:
        print("错误：未知的画像 %r，可选：%s" % (args.profile, ", ".join(PROFILES.keys())))
        return 2

    try:
        result = run_extraction(args.input, args.profile, args)
    except RuntimeError as exc:
        print("抽取失败：%s" % exc)
        return 3

    out_dir = args.out or os.path.join(os.getcwd(), "out_extracted")
    json_path, csv_path = write_outputs(result, out_dir)
    print_summary(result)
    print("")
    print("输出文件：%s" % json_path)
    print("输出文件：%s" % csv_path)
    print("")
    print("下一步：python scripts/validate_fields.py --input %s --profile %s" % (json_path, args.profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
