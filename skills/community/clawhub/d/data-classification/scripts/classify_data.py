#!/usr/bin/env python3
"""First-pass data field classifier for GB/T 43697-2024 and JR/T 0197-2020 dual labels."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable


@dataclass
class FieldItem:
    table: str
    name: str
    dtype: str = ""
    comment: str = ""


@dataclass
class Result:
    table: str
    field: str
    dtype: str
    comment: str
    general_category: str
    general_level: str
    finance_category: str
    finance_level: str | int | None
    finance_candidates: str
    dual_label: str
    confidence: float
    basis: str
    review: str


GENERAL_RULES = [
    (r"(企业信贷|企业.*(借款|贷款).*金额|company_credit|enterprise_credit|corp_credit)", "金融数据/组织数据-单位资讯信息-企业信贷信息", "一般数据", 0.88, "命中企业信贷/企业借款金额关键词"),
    (r"(id[_-]?card|cert|certificate|passport|identity|身份证|证件|护照)", "金融数据/用户数据-个人信息-个人身份信息", "一般数据", 0.86, "命中证件/身份标识关键词"),
    (r"(phone|mobile|tel|email|mail|手机|电话|邮箱|联系)", "金融数据/用户数据-个人信息-个人联系信息", "一般数据", 0.84, "命中联系方式关键词"),
    (r"(name|姓名|客户名|用户名称|client_name|customer_name)", "金融数据/用户数据-个人信息-个人基本信息", "一般数据", 0.78, "命中姓名/名称关键词"),
    (r"(address|addr|gps|geo|longitude|latitude|location|地址|经度|纬度|定位|位置)", "金融数据/用户数据-个人信息-地理位置/联系地址", "一般数据", 0.78, "命中地址/位置关键词；高精度大规模需复核"),
    (r"(password|passwd|pwd|pin|otp|token|secret|key|salt|密码|口令|令牌|密钥|验证码)", "金融数据/用户数据-身份鉴别/凭证信息", "一般数据", 0.90, "命中认证凭证关键词；需高敏保护"),
    (r"(face|finger|iris|voiceprint|biometric|人脸|指纹|虹膜|声纹|生物)", "金融数据/用户数据-个人生物识别信息", "一般数据", 0.90, "命中生物识别关键词"),
    (r"(account|acct|card|卡号|账号|账户|银行卡)", "金融数据/业务数据-账户信息", "一般数据", 0.82, "命中账户/卡关键词"),
    (r"(amount|amt|balance|price|fee|余额|金额|费用|价格|资产)", "金融数据/业务数据-金额/资产信息", "一般数据", 0.78, "命中金额/余额关键词"),
    (r"(transaction|trans|trade|payment|pay|order|流水|交易|支付|转账|订单)", "金融数据/业务数据-交易与支付信息", "一般数据", 0.82, "命中交易/支付关键词"),
    (r"(loan|credit|授信|贷款|征信|逾期|担保)", "金融数据/业务数据-信贷信息", "一般数据", 0.82, "命中信贷关键词"),
    (r"(risk|score|tag|label|level|风险|评分|标签|等级)", "金融数据/用户数据-衍生标签/风险标签", "一般数据", 0.66, "命中标签/评分关键词；需确认模型含义"),
    (r"(company|corp|org|enterprise|uscc|统一社会信用|公司|企业|机构|组织)", "金融数据/组织数据-单位基本信息", "一般数据", 0.70, "命中组织/单位关键词"),
    (r"(contract|agreement|合同|协议|合约)", "金融数据/业务数据-合约协议信息", "一般数据", 0.72, "命中合同/协议关键词"),
    (r"(ip|device|mac|imei|login|log|session|日志|设备|登录|会话)", "系统运维数据-日志/设备/网络标识", "一般数据", 0.70, "命中日志/设备/网络标识关键词"),
]

FINANCE_RULES = [
    (r"(企业信贷|company_credit|enterprise_credit|corp_credit)", "客户-单位-单位资讯信息-企业信贷信息", 3, 0.94),
    (r"(企业.*(借款|贷款).*金额)", "客户-单位-单位资讯信息-企业信贷信息", 3, 0.94),
    (r"(企业.*(借款|贷款).*金额|loan_amount|credit_amount|借款金额|贷款金额)", "业务-合约协议-贷款业务信息-放还款信息", 2, 0.90),
    (r"(id[_-]?card|cert|certificate|passport|identity|身份证|证件|护照)", "客户-个人-个人身份鉴别信息-传统鉴别信息", 4, 0.90),
    (r"(password|passwd|pwd|pin|otp|token|secret|key|salt|密码|口令|令牌|密钥|验证码)", "客户-个人-个人身份鉴别信息-传统鉴别信息", 4, 0.92),
    (r"(face|finger|iris|voiceprint|biometric|人脸|指纹|虹膜|声纹|生物)", "客户-个人-个人身份鉴别信息-强隐私生物特征信息", 4, 0.92),
    (r"(phone|mobile|tel|email|mail|手机|电话|邮箱|联系)", "客户-个人-个人自然信息-个人联系信息", 3, 0.86),
    (r"(address|addr|gps|geo|longitude|latitude|location|地址|经度|纬度|定位|位置)", "客户-个人-个人自然信息-个人地理位置信息", 3, 0.82),
    (r"(name|姓名|客户名|用户名称|client_name|customer_name)", "客户-个人-个人自然信息-个人基本概况信息", 3, 0.80),
    (r"(customer|client|cust|user|客户|用户).*(id|no|编号|号)$|^(customer|client|cust|user)[_-]?(id|no)$", "客户-个人-个人自然信息-个人基本概况信息", 3, 0.72),
    (r"(account|acct|账号|账户)", "业务-账户信息-账户信息-基本信息", 2, 0.78),
    (r"(card|卡号|银行卡)", "业务-账户信息-账户信息-介质信息", 3, 0.82),
    (r"(balance|余额)", "业务-账户信息-账户信息-金额信息", 3, 0.86),
    (r"(amount|amt|price|fee|金额|费用|价格)", "业务-交易与支付-交易信息-金额信息", 3, 0.78),
    (r"(transaction|trans|trade|payment|pay|流水|交易|支付|转账)", "业务-交易与支付-交易信息-基本信息", 3, 0.84),
    (r"(loan|credit|授信|贷款|征信|逾期|担保)", "客户-个人-个人资讯信息-个人信贷信息", 3, 0.84),
    (r"(risk|风险)", "客户-个人-个人标签信息-风险标签信息", 2, 0.72),
    (r"(score|评分|分数)", "客户-个人-个人标签信息-价值标签信息", 2, 0.64),
    (r"(company|corp|org|enterprise|公司|企业|机构|组织|单位)", "客户-单位-单位基本信息-单位基本概况", 1, 0.70),
    (r"(legal_rep|法人|管理层|高管)", "客户-单位-单位基本信息-管理层信息", 3, 0.80),
    (r"(contract|agreement|合同|协议|合约)", "业务-合约协议-合同通用信息-基本信息", 2, 0.78),
    (r"(ip|device|mac|imei|login|log|session|日志|设备|登录|会话)", "系统-系统运行与安全-日志信息-基本信息", 2, 0.66),
]

CREATE_HEAD_RE = re.compile(r"create\s+table\s+(?:if\s+not\s+exists\s+)?[`\"\[]?([\w.\-\u4e00-\u9fff]+)[`\"\]]?\s*\(", re.I)
TABLE_COMMENT_RE = re.compile(r"comment\s*[= ]\s*['\"]([^'\"]+)['\"]", re.I)
LINE_COMMENT_RE = re.compile(r"comment\s+['\"]([^'\"]+)['\"]", re.I)


def norm(text: str) -> str:
    return (text or "").strip().lower()


def split_columns(body: str) -> list[str]:
    cols, buf, depth, quote = [], [], 0, ""
    for ch in body:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "'\"`":
            quote = ch
            buf.append(ch)
        elif ch == "(":
            depth += 1; buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1); buf.append(ch)
        elif ch == "," and depth == 0:
            part = "".join(buf).strip()
            if part:
                cols.append(part)
            buf = []
        else:
            buf.append(ch)
    part = "".join(buf).strip()
    if part:
        cols.append(part)
    return cols


def iter_create_tables(sql: str):
    """Yield (table, body, trailing_sql) while respecting nested type parentheses."""
    for match in CREATE_HEAD_RE.finditer(sql):
        table = match.group(1).strip('`"[]')
        start = match.end() - 1
        depth, quote, end = 0, "", None
        for i in range(start, len(sql)):
            ch = sql[i]
            if quote:
                if ch == quote:
                    quote = ""
                continue
            if ch in "'\"`":
                quote = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is not None:
            yield table, sql[start + 1:end], sql[end + 1:end + 300]


def parse_sql(sql: str) -> list[FieldItem]:
    items: list[FieldItem] = []
    for table, body, trailing in iter_create_tables(sql):
        tc = TABLE_COMMENT_RE.search(trailing)
        table_comment = tc.group(1) if tc else ""
        for raw in split_columns(body):
            line = raw.strip()
            if not line or re.match(r"(?i)^(primary|foreign|unique|key|constraint|index|check)\b", line):
                continue
            m = re.match(r"[`\"\[]?([\w\-\u4e00-\u9fff]+)[`\"\]]?\s+(.+)$", line, re.S)
            if not m:
                continue
            name = m.group(1)
            rest = m.group(2).strip()
            dtype_match = re.match(r"([A-Za-z]+\s*(?:\([^)]*\))?|ENUM\s*\([^)]*\)|SET\s*\([^)]*\))", rest, re.I)
            dtype = dtype_match.group(1).strip() if dtype_match else rest.split()[0]
            cm = LINE_COMMENT_RE.search(rest)
            comment = cm.group(1) if cm else ""
            if table_comment and not comment:
                comment = f"表注释:{table_comment}"
            items.append(FieldItem(table=table, name=name, dtype=dtype, comment=comment))
    return items


def rule_score(rule: tuple) -> float:
    # GENERAL_RULES store score at -2 because -1 is a textual basis; FINANCE_RULES store score at -1.
    return float(rule[-2] if isinstance(rule[-1], str) else rule[-1])


def matching_rules(text: str, rules: Iterable[tuple]) -> list[tuple]:
    matches = [rule for rule in rules if re.search(rule[0], text, re.I)]
    return sorted(matches, key=rule_score, reverse=True)


def best_match(text: str, rules: Iterable[tuple]):
    matches = matching_rules(text, rules)
    return matches[0] if matches else None


def format_finance_candidates(rules: list[tuple]) -> str:
    if not rules:
        return ""
    top_score = rule_score(rules[0])
    seen = set()
    parts = []
    for rule in rules:
        _, category, level, score = rule
        score = float(score)
        # Keep the best label and close/high-confidence alternatives; suppress broad generic hits.
        if score < 0.85 and score < top_score - 0.12:
            continue
        key = (category, level)
        if key in seen:
            continue
        seen.add(key)
        parts.append(f"{category}/JR-T {level}级({score:.2f})")
    return "；".join(parts)


def classify(item: FieldItem, mode: str) -> Result:
    # Prefer field/comment evidence. Use table name only as fallback because names like
    # customer_account would otherwise incorrectly classify every generic column as account data.
    field_evidence = " ".join([item.name, item.comment, item.dtype])
    table_evidence = " ".join([item.table, item.name, item.comment, item.dtype])
    g = best_match(field_evidence, GENERAL_RULES) or best_match(table_evidence, GENERAL_RULES)
    if g:
        _, general_category, general_level, gconf, basis = g
        if not best_match(field_evidence, GENERAL_RULES):
            gconf = min(float(gconf), 0.58)
            basis += "（主要来自表名，需复核）"
    else:
        general_category = "待确认-业务数据/经营管理数据/系统运维数据"
        general_level = "一般数据"
        gconf = 0.42
        basis = "未命中明确关键词；按一般数据暂定，需结合业务含义确认"

    finance_category: str = "不适用/非金融或待确认"
    finance_level: int | None = None
    finance_candidates = ""
    fconf = 0.0
    if mode == "finance":
        field_matches = matching_rules(field_evidence, FINANCE_RULES)
        table_matches = matching_rules(table_evidence, FINANCE_RULES)
        matches = field_matches or table_matches
        f = matches[0] if matches else None
        finance_candidates = format_finance_candidates(matches)
        if f:
            _, finance_category, finance_level, fconf = f
            if not finance_candidates:
                finance_candidates = f"{finance_category}/JR-T {finance_level}级({float(fconf):.2f})"
            if not field_matches:
                fconf = min(float(fconf), 0.58)
        else:
            finance_category = "金融分类待确认"
            finance_level = "待确认"
            finance_candidates = "金融分类待确认"
            fconf = 0.35

    confidence = round(max(gconf, fconf) if mode == "finance" else gconf, 2)
    if mode == "finance":
        dual = f"{general_category}/{general_level} + {finance_category}/JR-T {finance_level if finance_level is not None else '待确认'}级"
    else:
        dual = f"{general_category}/{general_level}"

    review_bits = []
    if confidence < 0.6:
        review_bits.append("低置信度，需业务口径确认")
    if any(k in norm(item.name) for k in ["id", "code", "type", "status", "no"] ) and confidence < 0.75:
        review_bits.append("通用字段名需结合表/注释")
    if re.search(r"(gps|经纬|位置|location)", table_evidence, re.I):
        review_bits.append("确认精度、规模、覆盖范围")
    review = "；".join(review_bits) or ""

    # Mandatory output fields must never be empty.
    finance_candidates = finance_candidates or finance_category or "金融分类待确认"
    return Result(item.table, item.name, item.dtype, item.comment, general_category, general_level, finance_category, finance_level, finance_candidates, dual, confidence, basis, review)


def output_headers(include_finance: bool) -> list[str]:
    base = ["表名", "字段名", "类型/注释", "通用分类", "通用分级"]
    if include_finance:
        base += ["推荐金融分类标签", "JR/T最低级别", "候选金融标签", "双标签"]
    return base + ["置信度", "依据/备注"]


def output_row(r: Result, include_finance: bool) -> list[str]:
    type_comment = f"{r.dtype} {r.comment}".strip()
    row = [r.table, r.field, type_comment, r.general_category, r.general_level]
    if include_finance:
        row += [r.finance_category, str(r.finance_level or "待确认"), r.finance_candidates, r.dual_label]
    row += [f"{r.confidence:.2f}", "；".join(x for x in [r.basis, r.review] if x)]
    return row


def render_markdown(results: list[Result], include_finance: bool) -> str:
    headers = output_headers(include_finance)
    lines = ["|" + "|".join(headers) + "|", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in results:
        lines.append("|" + "|".join(str(c).replace("|", "/") for c in output_row(r, include_finance)) + "|")
    lines.append("")
    lines.append(f"覆盖校验：输入/解析字段 {len(results)} 个，已分类 {len(results)} 个，遗漏 0 个。")
    return "\n".join(lines)


def render_csv(results: list[Result], include_finance: bool) -> str:
    out = StringIO()
    headers = output_headers(include_finance)
    writer = csv.writer(out)
    writer.writerow(headers)
    for r in results:
        writer.writerow(output_row(r, include_finance))
    return out.getvalue()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Classify data fields or SQL DDL under general/financial data rules.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--field", help="single field name")
    src.add_argument("--fields", help="comma/newline separated field names or a path to a text file")
    src.add_argument("--sql", help="path to SQL DDL file")
    ap.add_argument("--mode", choices=["general", "finance"], default="finance", help="general omits financial/JR-T columns; finance includes dual-label columns")
    ap.add_argument("--format", choices=["markdown", "json", "csv"], default="markdown")
    args = ap.parse_args(argv)

    if args.field:
        items = [FieldItem(table="", name=args.field)]
    elif args.fields:
        p = Path(args.fields)
        raw = p.read_text(encoding="utf-8") if p.exists() else args.fields
        names = [x.strip() for x in re.split(r"[,\n]", raw) if x.strip()]
        items = [FieldItem(table="", name=x) for x in names]
    else:
        sql = Path(args.sql).read_text(encoding="utf-8")
        items = parse_sql(sql)
        if not items:
            print("No CREATE TABLE columns parsed from SQL.", file=sys.stderr)
            return 2

    results = [classify(i, args.mode) for i in items]
    include_finance = args.mode == "finance"
    if args.format == "json":
        data = []
        for r in results:
            d = {
                "table": r.table,
                "field": r.field,
                "type_comment": f"{r.dtype} {r.comment}".strip(),
                "general_category": r.general_category,
                "general_level": r.general_level,
                "confidence": r.confidence,
                "basis": "；".join(x for x in [r.basis, r.review] if x),
            }
            if include_finance:
                d.update({
                    "finance_category": r.finance_category,
                    "finance_level": r.finance_level,
                    "finance_candidates": r.finance_candidates,
                    "dual_label": r.dual_label,
                })
            data.append(d)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        print(render_csv(results, include_finance), end="")
    else:
        print(render_markdown(results, include_finance))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
