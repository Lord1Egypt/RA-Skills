#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对抽取结果做字段完整性校验、格式校验、勾稽核对与异常标记，输出可读报告。

用法::

    python scripts/validate_fields.py --input out/records.json --profile bank_statement
    python scripts/validate_fields.py --input out/records.json --profile vat_invoice --report report.md
    python scripts/validate_fields.py --input records.csv --profile bank_statement --json
    python scripts/validate_fields.py --selftest
    python scripts/validate_fields.py --list-rules

输入格式
--------
1. ``extract_tables.py`` 产出的 ``records.json``（推荐，带证据坐标与 footer_rows）
2. 任意 CSV：第一行为表头，每行为一条记录；表头会按字段别名表映射到标准字段名；
   含有"合计/小计/总计"的行自动识别为合计行并参与勾稽核对。

校验规则
--------
R1  必填字段缺失            error    记录级
R2  互斥字段组全缺            error    记录级
R3  金额格式非法              error    字段级
R4  金额符号异常              warning  字段级
R5  金额非正（应正数而为 0/负）  error    字段级
R6  日期格式非法              error    字段级
R7  日期歧义（不自动判读）      warning  字段级
R8  日期区间倒置              warning  记录级
R9  日期超出单据声明期间        warning  字段级
R10 发票号码非法（长度或字符）    error    字段级
R11 发票号码长度异常（9/10/12 位）warning  字段级
R12 发票代码长度异常          warning  字段级
R13 编号含非法字符            error    字段级
R14 同一单据内编号重复        warning  字段级
R15 合计行与明细行求和不一致    warning  记录级
R16 明细行重复                warning  记录级
R17 字段无证据坐标（不可溯源）  warning  字段级
R18 单位换算（万元）未登记      warning  字段级
R19 金额分隔符写法存在歧义      warning  字段级
R20 归一化值与原文解析不一致    warning  字段级
R21 日期只写到月份（日按 1 补） info     字段级
R22 价税合计 ≠ 金额 + 税额     error    记录级
R23 实发工资 ≠ 应发 − 扣款合计  warning  记录级
R24 数量 × 单价 ≠ 金额        warning  记录级
R25 合计行存在但无明细可求和    info     记录级
R26 合计与明细求和一致        info     记录级

设计原则
--------
1. 信息不足时报告"缺什么"，绝不编造数字补齐。
2. 校验只读不写：不修改、不修复抽取结果。
3. 报告同时给出人类可读文本与可机读 JSON。
4. 仅依赖 Python 标准库，任何环境下都能跑。
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
except Exception:  # pragma: no cover
    pass

from field_library import (  # noqa: E402
    INVOICE_CODE_LENGTHS,
    INVOICE_NUMBER_LENGTHS,
    PROFILES,
    get_profile,
    is_null_token,
    label_for,
    match_header,
    normalize_header,
    normalize_text,
    normalize_value,
    parse_amount,
    parse_date,
)

SCHEMA_VERSION = "1.0"

#: 问题级别，从重到轻
LEVELS = ("error", "warning", "info")

#: 记录级元数据列，不参与字段校验
META_COLUMNS = {"record_id", "recordid", "table_id", "tableid", "row", "page",
                "sheet", "行号", "页码", "工作表"}


# --------------------------------------------------------------------------
# 载入输入
# --------------------------------------------------------------------------

def load_records(path, profile_key="generic"):
    """载入抽取结果，返回 (records, footer_rows, meta)。"""
    if not os.path.exists(path):
        raise RuntimeError("文件不存在：%s" % path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return _load_json(path)
    if ext in (".csv", ".tsv"):
        return _load_csv(path, profile_key)
    raise RuntimeError("不支持的输入格式 %r，可选 .json / .csv" % ext)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    records = payload.get("records", [])
    footer_rows = payload.get("footer_rows", [])
    meta = {
        "source": payload.get("source", {}),
        "summary": payload.get("summary", {}),
        "dropped_header_rows": payload.get("dropped_header_rows", 0),
        "unmapped_columns": payload.get("unmapped_columns", []),
        "notes": payload.get("notes", []),
    }
    return records, footer_rows, meta


def _load_csv(path, profile_key="generic"):
    encoding = "utf-8-sig"
    try:
        with open(path, "r", encoding=encoding, newline="") as fh:
            rows = [list(r) for r in csv.reader(fh)]
    except UnicodeDecodeError:
        encoding = "gb18030"
        with open(path, "r", encoding=encoding, newline="") as fh:
            rows = [list(r) for r in csv.reader(fh)]
    if not rows:
        return [], [], {"source": {"file": os.path.basename(path), "encoding": encoding}}

    header = rows[0]
    body = rows[1:]
    footer_keywords = PROFILES[profile_key]["footer_keywords"] \
        if profile_key in PROFILES else PROFILES["generic"]["footer_keywords"]

    # 表头映射
    header_keys = []
    for col, head in enumerate(header):
        text = normalize_text(head)
        key, _alias = match_header(text, profile_key)
        if not key:
            norm = normalize_header(text)
            key = None if (not norm or norm in META_COLUMNS) else norm
        header_keys.append((col, key))

    profile_def = get_profile(profile_key) if profile_key in PROFILES \
        else get_profile("generic")

    records = []
    footer_rows = []
    seq = 0
    for ridx, row in enumerate(body, start=2):
        if all(is_null_token(c) for c in row):
            continue
        first = normalize_text(row[0]) if row else ""
        hit = next((kw for kw in footer_keywords
                    if kw in first or any(kw in normalize_text(row[i])
                                          for i in range(min(2, len(row))))), None)
        if hit:
            footer_fields = {}
            for col, key in header_keys:
                if key and col < len(row):
                    footer_fields[key] = normalize_text(row[col])
            footer_rows.append({
                "table_id": "csv_t1",
                "row": ridx,
                "keyword": hit,
                "cells": [normalize_text(c) for c in row],
                "fields": footer_fields,
                "page": None,
                "sheet": None,
            })
            continue
        seq += 1
        fields = {}
        for col, key in header_keys:
            if not key or col >= len(row):
                continue
            raw = normalize_text(row[col])
            value, status, note = normalize_value(key, raw, profile_def)
            fields[key] = {
                "value": value,
                "raw": raw,
                "evidence": {"table_id": "csv_t1", "row": ridx, "col": col + 1, "raw": raw},
                "status": status,
            }
            if note:
                fields[key]["note"] = note
        records.append({
            "record_id": "r%03d" % seq,
            "table_id": "csv_t1",
            "row": ridx,
            "fields": fields,
            "issues": [],
        })
    return records, footer_rows, {"source": {"file": os.path.basename(path), "encoding": encoding}}


# --------------------------------------------------------------------------
# 校验器
# --------------------------------------------------------------------------

class Issue(object):
    __slots__ = ("issue_id", "level", "rule", "record_id", "field", "raw", "message", "fix_hint")

    def __init__(self, level, rule, message, record_id="", field="", raw="", fix_hint=""):
        self.level = level
        self.rule = rule
        self.message = message
        self.record_id = record_id
        self.field = field
        self.raw = raw
        self.fix_hint = fix_hint
        self.issue_id = ""

    def to_dict(self):
        return {
            "issue_id": self.issue_id,
            "level": self.level,
            "rule": self.rule,
            "record_id": self.record_id,
            "field": self.field,
            "raw": self.raw,
            "message": self.message,
            "fix_hint": self.fix_hint,
        }


class Validator(object):
    def __init__(self, profile_key, tolerance=0.01, statement_period=None):
        if profile_key not in PROFILES:
            raise KeyError(profile_key)
        self.profile_key = profile_key
        self.profile = get_profile(profile_key)
        self.tolerance = tolerance
        self.statement_period = statement_period  # (start, end) ISO 字符串
        self.issues = []
        self.unverified = []
        self.stats = {}

    # -- issue helper ----------------------------------------------------
    def add(self, level, rule, message, record_id="", field="", raw="", fix_hint=""):
        if level not in LEVELS:
            level = "warning"
        self.issues.append(Issue(level, rule, message, record_id, field, raw, fix_hint))

    # -- main ------------------------------------------------------------
    def validate(self, records, footer_rows):
        self._check_required(records)
        self._check_amounts(records)
        self._check_dates(records)
        self._check_identifiers(records)
        self._check_evidence(records)
        self._check_reconciliation(records, footer_rows)
        self._check_arithmetic(records)
        self._check_duplicates(records)
        for idx, issue in enumerate(self.issues, start=1):
            issue.issue_id = "i%03d" % idx
        self.stats = {
            "records": len(records),
            "error": sum(1 for i in self.issues if i.level == "error"),
            "warning": sum(1 for i in self.issues if i.level == "warning"),
            "info": sum(1 for i in self.issues if i.level == "info"),
            "unverified_fields": len(self.unverified),
        }
        return self.result(records)

    # -- R1 / R2 / R18 ----------------------------------------------------
    def _check_required(self, records):
        req = self.profile["required"]
        for rec in records:
            present = set(rec.get("fields", {}).keys())
            for field in req:
                entry = rec["fields"].get(field)
                # 只有"原文里根本没有这个值"才算缺失。
                # 原文有值但解析不出来（非法/歧义日期等）由字段级规则负责，不重复报缺失。
                raw = (entry or {}).get("raw", "")
                if entry is None or is_null_token(raw):
                    self.add("error", "required_field_missing",
                             "必填字段缺失：%s" % label_for(field),
                             record_id=rec.get("record_id", ""), field=field,
                             raw=raw,
                             fix_hint="回到原文对应页/行补取该字段；确认原文是否真的没有此字段")
            for group in self.profile.get("one_of", []):
                hit = False
                for g in group:
                    entry = rec["fields"].get(g)
                    if entry is not None and not is_null_token(entry.get("raw", "")):
                        hit = True
                        break
                if not hit:
                    pretty = " / ".join(label_for(g) for g in group)
                    self.add("error", "required_group_missing",
                             "互斥字段组全部缺失：%s（至少要有其一）" % pretty,
                             record_id=rec.get("record_id", ""), field=",".join(group),
                             fix_hint="确认该单据类型是否用词不同，或原文该列确实不存在")

    # -- R3 / R4 / R5 / R17 ------------------------------------------------
    def _check_amounts(self, records):
        amount_fields = self.profile.get("amount_fields", [])
        for rec in records:
            for field in amount_fields:
                entry = rec["fields"].get(field)
                if entry is None:
                    continue
                raw = entry.get("raw", "")
                value = entry.get("value")
                if value is None and is_null_token(raw):
                    continue  # 占位符视为缺失，不重复报
                parsed, status, note = parse_amount(raw)
                if status == "invalid":
                    self.add("error", "invalid_amount",
                             "金额无法解析：%s" % (raw or "<空>"),
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="核对原文该单元格；全角字符/千分位/小数点错位都会导致此问题")
                    continue
                if status == "ambiguous":
                    self.add("warning", "ambiguous_amount_format",
                             "金额分隔符写法存在歧义（既可能读作千分位也可能读作小数点）：%s" % raw,
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="对照同页合计行判断量级，勿直接采信")
                if parsed is not None:
                    if field in ("sum_insured", "premium", "gross_pay", "net_pay") and parsed <= 0:
                        self.add("error", "non_positive_amount",
                                 "%s 应为正数，实际为 %s" % (label_for(field), parsed),
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="占位符请按缺失处理，不要读作 0")
                    if parsed < 0 and field in ("balance", "amount", "sum_insured", "premium"):
                        self.add("warning", "unexpected_sign",
                                 "%s 出现负值：%s" % (label_for(field), parsed),
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="中文单据常用单独的方向列表示借贷，请核对方向列")
                if note == "unit_wan_yuan":
                    self.add("warning", "unit_not_registered",
                             "金额单位疑似万元（原文含「万元」），换算系数未登记：%s" % raw,
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="换算需在 notes 中显式登记倍数，否则合计会错 10000 倍")
                # 值与原文解析结果不一致 -> 归一化环节出错
                if parsed is not None and isinstance(value, (int, float)) and abs(float(value) - parsed) > 1e-9:
                    self.add("warning", "value_raw_mismatch",
                             "归一化值与原文解析结果不一致：value=%s, 原文解析=%s" % (value, parsed),
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="重新运行抽取，确认归一化未覆盖原值")

    # -- R6 / R7 / R8 / R9 -------------------------------------------------
    def _check_dates(self, records):
        date_fields = self.profile.get("date_fields", [])
        for rec in records:
            values = {}
            for field in date_fields:
                entry = rec["fields"].get(field)
                if entry is None:
                    continue
                raw = entry.get("raw", "")
                if is_null_token(raw):
                    continue
                iso, status, note = parse_date(raw)
                if status == "invalid":
                    self.add("error", "invalid_date",
                             "日期非法或格式无法识别：%s" % raw,
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="核对原文；2024年2月30日 这类日期必须回原文确认")
                elif status == "ambiguous":
                    self.add("warning", "ambiguous_date",
                             "日期存在日/月顺序歧义，未自动判读：%s" % raw,
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="由人工确认后写回，不要自动取一种解释")
                elif status == "ok":
                    values[field] = iso
                    if note == "day_defaulted":
                        self.add("info", "date_day_defaulted",
                                 "日期只写到月份，日期部分按 1 号补齐：%s" % raw,
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="如原文确无具体日，保留补齐说明即可")
                if self.statement_period and iso:
                    start, end = self.statement_period
                    if (start and iso < start) or (end and iso > end):
                        self.add("warning", "date_out_of_period",
                                 "日期 %s 超出单据声明期间 %s ~ %s" % (iso, start or "?", end or "?"),
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="确认是否混入其他账期的记录")
            if "effective_date" in values and "expiry_date" in values:
                if values["expiry_date"] <= values["effective_date"]:
                    self.add("warning", "date_range_inverted",
                             "保险期间倒置：生效 %s 不早于到期 %s" % (
                                 values["effective_date"], values["expiry_date"]),
                             record_id=rec.get("record_id", ""), field="effective_date/expiry_date",
                             raw="",
                             fix_hint="核对原文的起止日期录入")

# -- R10 / R11 / R12 / R13 ---------------------------------------------
    def _check_identifiers(self, records):
        id_fields = self.profile.get("id_fields", [])
        unique_fields = set(self.profile.get("unique_id_fields", []))
        seen = {}
        for rec in records:
            for field in id_fields:
                entry = rec["fields"].get(field)
                if entry is None:
                    continue
                raw = normalize_text(entry.get("raw", ""))
                if is_null_token(raw):
                    continue
                if field == "invoice_number":
                    digits = raw.replace(" ", "")
                    if not digits.isdigit():
                        self.add("error", "invalid_invoice_number",
                                 "发票号码含非数字字符：%s" % raw,
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="发票号码必须全为数字；疑似 O/0 混淆请回原文核对")
                    elif len(digits) not in INVOICE_NUMBER_LENGTHS:
                        if len(digits) in (9, 10, 12):
                            self.add("warning", "invoice_number_length_unusual",
                                     "发票号码长度为 %d 位（常见为 %s 位）：%s" % (
                                         len(digits), "/".join(str(x) for x in sorted(INVOICE_NUMBER_LENGTHS)), raw),
                                     record_id=rec.get("record_id", ""), field=field, raw=raw,
                                     fix_hint="可能把发票代码填进了号码列，请核对表头")
                        else:
                            self.add("error", "invalid_invoice_number",
                                     "发票号码长度为 %d 位（合法为 %s 位）：%s" % (
                                         len(digits), "/".join(str(x) for x in sorted(INVOICE_NUMBER_LENGTHS)), raw),
                                     record_id=rec.get("record_id", ""), field=field, raw=raw,
                                     fix_hint="不要补零或截断，回原文重新读取")
                elif field == "invoice_code":
                    digits = raw.replace(" ", "")
                    if digits.isdigit() and len(digits) not in INVOICE_CODE_LENGTHS:
                        self.add("warning", "invoice_code_length_unusual",
                                 "发票代码长度为 %d 位（常见 %s 位）：%s" % (
                                     len(digits), "/".join(str(x) for x in sorted(INVOICE_CODE_LENGTHS)), raw),
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="全电发票通常无发票代码；纸质发票为 10 或 12 位")
                if field in ("invoice_number", "invoice_code", "policy_no", "employee_no",
                             "waybill_no", "declaration_no") and not re.match(r"^[0-9A-Za-z\-/]+$", raw):
                    self.add("error", "invalid_identifier_chars",
                             "编号含非法字符（只允许数字、字母、-、/）：%s" % raw,
                             record_id=rec.get("record_id", ""), field=field, raw=raw,
                             fix_hint="检查是否混入了说明文字或标点")
                # 只有"文档内唯一"的编号才做重复检查（发票代码、税号可跨行重复）
                if field in unique_fields:
                    key = (field, raw.replace(" ", "").upper())
                    if key in seen:
                        self.add("warning", "duplicate_identifier",
                                 "同一单据内 %s 重复：%s（首次出现在 %s）" % (
                                     label_for(field), raw, seen[key]),
                                 record_id=rec.get("record_id", ""), field=field, raw=raw,
                                 fix_hint="重复编号可能是录入错误，也可能是合法的多明细共用单号，请人工判定")
                    else:
                        seen[key] = rec.get("record_id", "")

    # -- R16 ---------------------------------------------------------------
    def _check_evidence(self, records):
        for rec in records:
            for field, entry in rec.get("fields", {}).items():
                ev = entry.get("evidence") or {}
                has_coord = any(ev.get(k) for k in ("page", "sheet", "table_id")) and ev.get("row")
                if not has_coord:
                    self.add("warning", "missing_evidence",
                             "字段缺少可溯源坐标，按 unverified 处理：%s" % label_for(field),
                             record_id=rec.get("record_id", ""), field=field,
                             raw=entry.get("raw", ""),
                             fix_hint="补上页/表/行/列坐标，或标记为 unverified 并说明原因")
                    self.unverified.append({
                        "record_id": rec.get("record_id", ""),
                        "field": field,
                        "raw": entry.get("raw", ""),
                        "reason": "missing_evidence",
                    })
                if entry.get("status") in ("invalid", "unverified"):
                    self.unverified.append({
                        "record_id": rec.get("record_id", ""),
                        "field": field,
                        "raw": entry.get("raw", ""),
                        "reason": entry.get("status"),
                    })

    # -- R14 ---------------------------------------------------------------
    def _check_reconciliation(self, records, footer_rows):
        """合计行与明细行求和一致性（按列分别核对）。"""
        if not footer_rows:
            return
        amount_fields = [f for f in self.profile.get("amount_fields", [])]

        # 逐列求和
        sums = {}
        counts = {}
        for rec in records:
            for field in amount_fields:
                entry = rec.get("fields", {}).get(field)
                if entry is None:
                    continue
                parsed, status, _note = parse_amount(entry.get("raw", ""))
                if status == "ok" and parsed is not None:
                    sums[field] = sums.get(field, 0.0) + parsed
                    counts[field] = counts.get(field, 0) + 1

        for foot in footer_rows:
            foot_fields = foot.get("fields") or {}
            candidates = []
            if foot_fields:
                for field, raw in foot_fields.items():
                    if field not in amount_fields:
                        continue
                    parsed, status, _note = parse_amount(raw)
                    if status == "ok" and parsed is not None:
                        candidates.append((field, parsed, raw))
            else:
                # 无列映射时退回"整行最后一个可解析金额"
                for raw in foot.get("cells", []):
                    parsed, status, _note = parse_amount(raw)
                    if status == "ok" and parsed is not None:
                        candidates.append((self.profile.get("amount_fields", ["amount"])[0]
                                           if self.profile.get("amount_fields") else "amount",
                                           parsed, raw))

            for field, stated, raw in candidates:
                if counts.get(field, 0) == 0:
                    self.add("info", "reconciliation_not_possible",
                             "合计行有 %s 金额，但明细中没有该列的可求和数据" % label_for(field),
                             field=field, raw=raw,
                             fix_hint="确认明细是否被整体丢弃，或合计属于另一张表")
                    continue
                detail = sums[field]
                diff = abs(stated - detail)
                if diff > self.tolerance:
                    self.add("warning", "total_mismatch",
                             "合计 %s 与 %s 明细求和 %s（%d 行）不一致，差额 %s" % (
                                 stated, label_for(field), round(detail, 2),
                                 counts[field], round(diff, 2)),
                             record_id="", field=field, raw=raw,
                             fix_hint="先查跨页续行、退款行、手续费行，再查本页小计还是全表合计")
                else:
                    self.add("info", "total_matched",
                             "合计 %s 与 %s 明细求和一致（%d 行）" % (
                                 stated, label_for(field), counts[field]),
                             field=field, raw=raw,
                             fix_hint="")

    # -- R14b 单条记录内的勾稽（价税合计 / 实发工资 / 数量×单价） ----------
    def _check_arithmetic(self, records):
        specs = self.profile.get("arithmetic", [])
        if not specs:
            return
        for rec in records:
            fields = rec.get("fields", {})
            for spec in specs:
                operands = []
                missing = False
                for field in spec.get("add", []) + spec.get("subtract", []) + \
                        spec.get("multiply", []) + [spec["equals"]]:
                    entry = fields.get(field)
                    if entry is None:
                        missing = True
                        break
                    parsed, status, _note = parse_amount(entry.get("raw", ""))
                    if status != "ok":
                        missing = True
                        break
                    operands.append((field, parsed))
                if missing:
                    continue
                lookup = dict(operands)
                expected = 1.0 if spec.get("multiply") else 0.0
                for field in spec.get("add", []):
                    expected += lookup[field]
                for field in spec.get("subtract", []):
                    expected -= lookup[field]
                for field in spec.get("multiply", []):
                    expected *= lookup[field]
                actual = lookup[spec["equals"]]
                diff = abs(expected - actual)
                tol = max(self.tolerance, abs(expected) * 0.005)
                if diff > tol:
                    self.add(spec.get("level", "warning"), spec["rule"],
                             "%s 不成立：按原文计算应为 %s，实际为 %s，差额 %s" % (
                                 label_for(spec["equals"]), round(expected, 2),
                                 actual, round(diff, 2)),
                             record_id=rec.get("record_id", ""), field=spec["equals"],
                             raw=fields.get(spec["equals"], {}).get("raw", ""),
                             fix_hint=spec.get("hint", ""))

    # -- R15 ---------------------------------------------------------------
    def _check_duplicates(self, records):
        key_fields = self.profile.get("key_fields", [])
        if not key_fields:
            return
        seen = {}
        for rec in records:
            parts = []
            for field in key_fields:
                entry = rec.get("fields", {}).get(field)
                if entry is None:
                    parts.append("")
                    continue
                value = entry.get("value")
                parts.append("" if value is None else str(value))
            if not any(p for p in parts):
                continue
            key = "|".join(parts)
            if key in seen:
                self.add("warning", "duplicate_detail_row",
                         "明细行重复（键：%s）：与 %s 完全一致" % (
                             " + ".join(label_for(f) for f in key_fields), seen[key]),
                         record_id=rec.get("record_id", ""), field=",".join(key_fields),
                         fix_hint="冲正/退款成对出现属正常；工具不会自动删除任何一行")
            else:
                seen[key] = rec.get("record_id", "")

    # -- 汇总 --------------------------------------------------------------
    def result(self, records):
        errors = sum(1 for i in self.issues if i.level == "error")
        warnings = sum(1 for i in self.issues if i.level == "warning")
        if errors:
            status = "blocked"
        elif warnings:
            status = "pass_with_warnings"
        else:
            status = "pass"
        return {
            "schema_version": SCHEMA_VERSION,
            "validation_status": status,
            "profile": self.profile_key,
            "profile_zh": self.profile["zh"],
            "tolerance": self.tolerance,
            "summary": {
                "records": len(records),
                "errors": errors,
                "warnings": warnings,
                "info": sum(1 for i in self.issues if i.level == "info"),
                "unverified_fields": len(self.unverified),
            },
            "issues": [i.to_dict() for i in self.issues],
            "unverified_fields": self.unverified,
        }


# --------------------------------------------------------------------------
# 报告输出
# --------------------------------------------------------------------------

def render_report(result, meta):
    lines = []
    src = meta.get("source", {}) or {}
    lines.append("# 字段校验报告 / Field Validation Report")
    lines.append("")
    lines.append("- 来源文件 / source file : %s" % (src.get("file", "(unknown)")))
    if src.get("type"):
        lines.append("- 文件类型 / source type : %s" % src["type"])
    if src.get("profile_zh"):
        lines.append("- 文档画像 / profile    : %s / %s" % (result["profile"], result["profile_zh"]))
    lines.append("- 校验结论 / status     : %s" % result["validation_status"])
    lines.append("- 容差 / tolerance      : %s" % result["tolerance"])
    lines.append("")
    s = result["summary"]
    lines.append("## 概览 / Summary")
    lines.append("")
    lines.append("| 记录数 records | error | warning | info | unverified |")
    lines.append("|---|---|---|---|---|")
    lines.append("| %d | %d | %d | %d | %d |" % (
        s["records"], s["errors"], s["warnings"], s["info"], s["unverified_fields"]))
    lines.append("")

    if result["validation_status"] == "blocked":
        lines.append("> **结论：BLOCKED — 存在 error 级问题，结果不可直接交付。**")
        lines.append("")

    lines.append("## 问题明细 / Issues")
    lines.append("")
    if not result["issues"]:
        lines.append("无问题检出。")
        lines.append("")
    else:
        lines.append("| issue_id | level | rule | record_id | field | raw | message | fix_hint |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for issue in result["issues"]:
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                issue["issue_id"], issue["level"], issue["rule"],
                issue["record_id"] or "-",
                issue["field"] or "-",
                _cell(issue["raw"]),
                _cell(issue["message"]),
                _cell(issue["fix_hint"]),
            ))
        lines.append("")

    lines.append("## 不可溯源字段 / Unverified fields")
    lines.append("")
    if not result["unverified_fields"]:
        lines.append("所有字段均可溯源。")
        lines.append("")
    else:
        lines.append("| record_id | field | raw | reason |")
        lines.append("|---|---|---|---|")
        for item in result["unverified_fields"]:
            lines.append("| %s | %s | %s | %s |" % (
                item.get("record_id", "-"), item.get("field", "-"),
                _cell(item.get("raw", "")), item.get("reason", "")))
        lines.append("")

    if meta.get("unmapped_columns"):
        lines.append("## 未映射列 / Unmapped columns")
        lines.append("")
        for item in meta["unmapped_columns"]:
            lines.append("- %s" % item)
        lines.append("")

    if meta.get("notes"):
        lines.append("## 抽取阶段提示 / Extraction notes")
        lines.append("")
        for item in meta["notes"]:
            lines.append("- %s" % item)
        lines.append("")

    lines.append("## 交付前请确认 / Before delivery")
    lines.append("")
    lines.append("1. 逐条处理 error 级问题，或明确说明为何可以接受。")
    lines.append("2. 打开 `references/delivery-acceptance-checklist.md` 走完验收清单。")
    lines.append("3. 在交付说明中保留 validation_status 与 issue 计数。")
    lines.append("")
    return "\n".join(lines)


def _cell(text):
    if text is None:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ")


# --------------------------------------------------------------------------
# 自检
# --------------------------------------------------------------------------

SELFTEST_CSV = (
    "record_id,交易日期,摘要,借方发生额,贷方发生额,余额,对方户名,流水号\n"
    'r001,2024-01-05,货款汇入,,"12,345.60","150,000.00",示例制造有限公司,TX20240105001\n'
    'r002,2024-01-06,手续费,"25.00",,"149,975.00",示例制造有限公司,TX20240106002\n'
    'r003,2024-01-08,货款汇入,,"8,000.00","157,975.00",示例贸易有限公司,TX20240108003\n'
    'r004,2024-01-08,货款汇入,,"8,000.00","157,975.00",示例贸易有限公司,TX20240108003\n'
    'r005,01/02/2024,退款,"15.00",,"149,960.00",示例制造有限公司,TX20240108004\n'
    'r006,2024-01-09,货款汇入,,"1,000.00","160,960.00",示例制造有限公司,TX20240108005\n'
    '合计,,,"40.00","29,345.60",,,\n'
)


def selftest():
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="cn_doc_validate_selftest_")
    csv_path = os.path.join(tmpdir, "sample.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(SELFTEST_CSV)

    records, footer_rows, meta = load_records(csv_path, "bank_statement")
    validator = Validator("bank_statement", tolerance=0.01)
    result = validator.validate(records, footer_rows)

    print("自检数据：%s" % csv_path)
    print("记录数：%d，合计行：%d" % (len(records), len(footer_rows)))
    print("结论：%s" % result["validation_status"])
    print("")
    for issue in result["issues"]:
        print("  [%-7s] %-26s %-12s %s" % (
            issue["level"], issue["rule"], issue["record_id"] or "-", issue["message"]))
    print("")

    fired = set(i["rule"] for i in result["issues"])
    expected = {"duplicate_detail_row", "ambiguous_date", "duplicate_identifier",
                "total_matched"}
    ok = (
        result["validation_status"] == "pass_with_warnings"
        and expected.issubset(fired)
        and not any(i["rule"] == "total_mismatch" for i in result["issues"])
    )
    print("命中规则：%s" % ", ".join(sorted(fired)))
    print("SELFTEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def build_parser():
    p = argparse.ArgumentParser(
        prog="validate_fields.py",
        description="对抽取结果做必填/金额/日期/编号/合计勾稽/重复行校验，输出可读报告与 JSON。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python scripts/validate_fields.py --input out/records.json --profile bank_statement
  python scripts/validate_fields.py --input out/records.json --profile vat_invoice --report report.md
  python scripts/validate_fields.py --input records.csv --profile vat_invoice --json
  python scripts/validate_fields.py --list-rules
  python scripts/validate_fields.py --selftest

退出码：0 = 通过（含警告）1 = 存在 error 级问题（BLOCKED）；2 = 参数或输入错误。
""",
    )
    p.add_argument("--input", "-i", help="抽取结果文件（extract_tables.py 产出的 records.json，或任意 CSV）")
    p.add_argument("--profile", "-p", default="generic",
                   help="文档画像：%s（默认 generic）" % "、".join(PROFILES.keys()))
    p.add_argument("--report", "-r", help="把可读报告写到指定文件（Markdown）")
    p.add_argument("--json", dest="json_out", help="把机器可读结果写到指定文件（JSON）")
    p.add_argument("--tolerance", type=float, default=0.01, help="合计勾稽容差，默认 0.01")
    p.add_argument("--period", help="单据声明期间，形如 2024-01-01,2024-01-31，用于日期越界检查")
    p.add_argument("--list-rules", action="store_true", help="列出所有校验规则")
    p.add_argument("--selftest", action="store_true", help="用内置样例 CSV 自检规则是否触发")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_rules:
        for line in __doc__.splitlines():
            if re.match(r"^R\d+\s", line):
                print(line.strip())
        return 0

    if args.selftest:
        return selftest()

    if not args.input:
        parser.print_usage()
        print("错误：缺少 --input。示例：python scripts/validate_fields.py --input out/records.json")
        return 2

    if args.profile not in PROFILES:
        print("错误：未知的画像 %r，可选：%s" % (args.profile, ", ".join(PROFILES.keys())))
        return 2

    period = None
    if args.period:
        parts = [p.strip() for p in args.period.split(",")]
        if len(parts) != 2:
            print("错误：--period 需要两个 ISO 日期，如 2024-01-01,2024-01-31")
            return 2
        period = (parts[0] or None, parts[1] or None)

    try:
        records, footer_rows, meta = load_records(args.input, args.profile)
    except RuntimeError as exc:
        print("读取失败：%s" % exc)
        return 2

    validator = Validator(args.profile, tolerance=args.tolerance, statement_period=period)
    result = validator.validate(records, footer_rows)
    report = render_report(result, meta)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(report)
        print("报告已写入：%s" % args.report)
    else:
        print(report)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
        print("JSON 已写入：%s" % args.json_out)

    return 1 if result["validation_status"] == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())
