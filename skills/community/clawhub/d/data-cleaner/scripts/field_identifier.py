"""
F2 · Intelligent field type identification.
Uses regex patterns + optional AI (MiniMax / DeepSeek) for ambiguous fields.

Supported types:
  name, phone, email, address, amount, date, sku, order_no,
  id_card, gender, url, ip_address, bank_account, custom

Usage:
    from field_identifier import identify_fields, FieldType

    types = identify_fields(df)           # dict: col_name -> FieldType
    types = identify_fields(df, ai_model="deepseek")   # use AI for uncertain cols
    types = identify_fields(df, custom_rules={"姓名": "name"})
"""

import os
import re
import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd

# ─── Field type enum ───────────────────────────────────────────────────────────

class FieldType(str, Enum):
    NAME       = "name"
    PHONE      = "phone"
    EMAIL      = "email"
    ADDRESS    = "address"
    AMOUNT     = "amount"
    DATE       = "date"
    SKU        = "sku"
    ORDER_NO   = "order_no"
    ID_CARD    = "id_card"
    GENDER     = "gender"
    URL        = "url"
    IP_ADDRESS = "ip_address"
    BANK_ACCOUNT = "bank_account"
    TEXT       = "text"
    NUMBER     = "number"
    UNKNOWN    = "unknown"

FIELD_TYPE_LABELS: Dict[FieldType, str] = {
    FieldType.NAME:       "姓名",
    FieldType.PHONE:      "手机号",
    FieldType.EMAIL:     "邮箱",
    FieldType.ADDRESS:    "地址",
    FieldType.AMOUNT:     "金额",
    FieldType.DATE:       "日期",
    FieldType.SKU:        "SKU",
    FieldType.ORDER_NO:   "订单号",
    FieldType.ID_CARD:    "身份证",
    FieldType.GENDER:     "性别",
    FieldType.URL:        "网址",
    FieldType.IP_ADDRESS: "IP地址",
    FieldType.BANK_ACCOUNT: "银行账号",
    FieldType.TEXT:       "文本",
    FieldType.NUMBER:     "数字",
    FieldType.UNKNOWN:    "未知",
}

# ─── Regex patterns ────────────────────────────────────────────────────────────

_PATTERNS: Dict[FieldType, re.Pattern] = {
    FieldType.EMAIL: re.compile(
        r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    ),
    FieldType.PHONE: re.compile(
        r"^1[3-9]\d[\s\-]?\d{4}[\s\-]?\d{4}$"   # Chinese mobile
    ),
    FieldType.ID_CARD: re.compile(
        r"^\d{15}$|^\d{17}[\dXx]$"
    ),
    FieldType.DATE: re.compile(
        r"^(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)"
        r"|(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
        r"|^\d{8}$"
        r"|^\d{10}$|^\d{13}$"
    ),
    # AMOUNT: must have decimal point or currency symbol (not pure digits)
    FieldType.AMOUNT: re.compile(
        r"^[¥$€£]\s*[\d，,]+\.\d+$"
        r"|^[¥$€£]\s*[\d，,]+\$"
        r"|^[\d，,]+\.\d+\s*[¥$€£]?$"
    ),
    # SKU: letter prefix or specific formats, NOT bare 11-digit phone-like numbers
    FieldType.SKU: re.compile(
        r"^[A-Za-z]+[\-]?\d{4,10}$"
        r"|^SKU[\-_]?\d{4,12}$"
        r"|^[A-Z0-9]{6,12}$"
    ),
    FieldType.ORDER_NO: re.compile(
        r"^(DD|ORDER|PO|SO|BM)[\-_]?\d{4,16}$"
        r"|^[A-Z]{2,}\d{6,16}$"
        r"|^\d{16,24}$"
    ),
    FieldType.URL: re.compile(
        r"^https?://[^\s]+$"
    ),
    FieldType.IP_ADDRESS: re.compile(
        r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    ),
    FieldType.GENDER: re.compile(
        r"^(男|女|男性|女性|M|m|F|f)$"
    ),
}

# Chinese province / city / district keywords for address detection
_ADDRESS_KEYWORDS = [
    "省", "市", "区", "县", "镇", "乡", "村", "路", "街", "号",
    "栋", "单元", "室", "弄", "巷", "楼", "广场", "大厦", "小区",
    "北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安",
]

_GENDER_VALUES = {"男", "女", "男性", "女性", "M", "F", "m", "f", "0", "1"}

# ─── Scoring helpers ───────────────────────────────────────────────────────────

def _is_empty(val: str) -> bool:
    return val in ("", "nan", "NaN", "None", "null", "NULL", "undefined")

def _match_score(pat: re.Pattern, val: str) -> float:
    """Fraction of non-empty values matching the pattern (0.0–1.0)."""
    if _is_empty(val):
        return 0.0
    return 1.0 if pat.match(str(val).strip()) else 0.0

def _avg_match_score(series: pd.Series, pat: re.Pattern) -> float:
    vals = [str(v) for v in series if not _is_empty(str(v))]
    if not vals:
        return 0.0
    return sum(1 for v in vals if pat.match(v.strip())) / len(vals)

def _numeric_score(series: pd.Series) -> float:
    vals = [str(v).strip() for v in series if not _is_empty(str(v))]
    if not vals:
        return 0.0
    count = 0
    for v in vals:
        # Remove currency symbols and commas
        cleaned = re.sub(r"[¥$€£,\s]", "", v)
        try:
            float(cleaned)
            count += 1
        except ValueError:
            pass
    return count / len(vals)

def _date_score(series: pd.Series) -> float:
    """Higher score if values look like dates."""
    vals = [str(v).strip() for v in series if not _is_empty(str(v))]
    if not vals:
        return 0.0
    date_forms = [
        (r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}", 0.9),
        (r"\d{8}", 0.8),
        (r"\d{10}", 0.8),
        (r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", 0.7),
    ]
    total = 0.0
    for v in vals:
        for pat, w in date_forms:
            if re.match(pat, v):
                total += w
                break
    return total / len(vals)

def _address_score(series: pd.Series) -> float:
    vals = [str(v) for v in series if not _is_empty(str(v))]
    if not vals:
        return 0.0
    hits = sum(1 for v in vals if any(k in v for k in _ADDRESS_KEYWORDS))
    avg_len = sum(len(v) for v in vals) / len(vals)
    # Longish strings with address keywords → high score
    len_bonus = min(avg_len / 20, 1.0) * 0.3
    return hits / len(vals) * 0.7 + len_bonus

def _gender_score(series: pd.Series) -> float:
    vals = {str(v).strip() for v in series if not _is_empty(str(v))}
    if not vals:
        return 0.0
    intersection = vals & _GENDER_VALUES
    return min(len(intersection) / 2, 1.0)  # just 1-2 distinct values matters

def _name_score(series: pd.Series) -> float:
    """
    Detect Chinese / common personal names.
    Chinese names: 2-4 chars, often with common surname characters,
    no digits, no special chars beyond hyphen/·.
    """
    # Common Chinese surname characters (top 100)
    COMMON_SURNAMES = set(
        "李王张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段雷钱汤尹黎易常武乔贺赖龚文"
    )
    vals = [str(v).strip() for v in series if not _is_empty(str(v))]
    if not vals:
        return 0.0

    hits = 0
    for v in vals:
        # Length check: 2-4 chars typical for Chinese full name
        if 2 <= len(v) <= 4:
            # No digits
            if re.match(r"^[\u4e00-\u9fa5·\-']+$", v):  # All Chinese + hyphen/apostrophe
                # Check for surname character at start
                if v[0] in COMMON_SURNAMES:
                    hits += 1
                elif re.match(r"^[A-Z][a-z]+$", v):  # English name "John Smith"
                    hits += 0.8
                elif re.match(r"^[A-Za-z]+$", v) and 3 <= len(v) <= 15:  # Single-word English name
                    hits += 0.5
        # English name formats
        elif re.match(r"^[A-Z][a-z]+(\s+[A-Z][a-z]+)+$", v):
            hits += 1

    return hits / len(vals)

# ─── Column name heuristics ────────────────────────────────────────────────────

_COL_NAME_WEIGHTS: Dict[str, Dict[FieldType, float]] = {
    # Name → FieldType hints
    "name": {FieldType.NAME: 0.9},
    "姓名": {FieldType.NAME: 0.9},
    "客户姓名": {FieldType.NAME: 0.9},
    "phone": {FieldType.PHONE: 0.9},
    "tel": {FieldType.PHONE: 0.8},
    "mobile": {FieldType.PHONE: 0.9},
    "电话": {FieldType.PHONE: 0.9},
    "手机": {FieldType.PHONE: 0.9},
    "手机号": {FieldType.PHONE: 0.9},
    "email": {FieldType.EMAIL: 0.9},
    "mail": {FieldType.EMAIL: 0.8},
    "邮箱": {FieldType.EMAIL: 0.9},
    "电子邮件": {FieldType.EMAIL: 0.9},
    "address": {FieldType.ADDRESS: 0.9},
    "地址": {FieldType.ADDRESS: 0.9},
    "收货地址": {FieldType.ADDRESS: 0.9},
    "amount": {FieldType.AMOUNT: 0.9},
    "金额": {FieldType.AMOUNT: 0.9},
    "总价": {FieldType.AMOUNT: 0.9},
    "单价": {FieldType.AMOUNT: 0.9},
    "price": {FieldType.AMOUNT: 0.9},
    "销售额": {FieldType.AMOUNT: 0.9},
    "date": {FieldType.DATE: 0.9},
    "日期": {FieldType.DATE: 0.9},
    "成交日期": {FieldType.DATE: 0.9},
    "订单日期": {FieldType.DATE: 0.9},
    "下单时间": {FieldType.DATE: 0.9},
    "创建时间": {FieldType.DATE: 0.9},
    "sku": {FieldType.SKU: 0.9},
    "SKU": {FieldType.SKU: 0.9},
    "商品编号": {FieldType.SKU: 0.9},
    "order": {FieldType.ORDER_NO: 0.9},
    "订单": {FieldType.ORDER_NO: 0.9},
    "订单号": {FieldType.ORDER_NO: 0.9},
    "order_no": {FieldType.ORDER_NO: 0.9},
    "订单编号": {FieldType.ORDER_NO: 0.9},
    "id_card": {FieldType.ID_CARD: 0.9},
    "身份证": {FieldType.ID_CARD: 0.9},
    "gender": {FieldType.GENDER: 0.9},
    "性别": {FieldType.GENDER: 0.9},
    "url": {FieldType.URL: 0.9},
    "网址": {FieldType.URL: 0.9},
    "ip": {FieldType.IP_ADDRESS: 0.9},
    "ip地址": {FieldType.IP_ADDRESS: 0.9},
    "银行账号": {FieldType.BANK_ACCOUNT: 0.9},
    "账号": {FieldType.BANK_ACCOUNT: 0.5},
}

def _col_name_score(col: str, ftype: FieldType) -> float:
    col_lower = col.lower()
    hints = _COL_NAME_WEIGHTS.get(col, {})
    hints.update(_COL_NAME_WEIGHTS.get(col_lower, {}))
    return hints.get(ftype, 0.0)

# ─── Main identification function ─────────────────────────────────────────────

@dataclass
class FieldInfo:
    field_type: FieldType
    confidence: float          # 0.0–1.0
    samples: List[str] = field(default_factory=list)

    def label(self) -> str:
        return FIELD_TYPE_LABELS.get(self.field_type, str(self.field_type))


def identify_fields(
    df: pd.DataFrame,
    *,
    custom_rules: Optional[Dict[str, str]] = None,
    ai_model: Optional[str] = None,
    ai_api_key: Optional[str] = None,
) -> Dict[str, FieldInfo]:
    """
    Identify field types for all columns in a DataFrame.

    Parameters
    ----------
    df           : input DataFrame
    custom_rules : {column_name: FieldType.value} user-defined overrides
    ai_model     : "minimax" or "deepseek" — use AI for uncertain columns
    ai_api_key   : API key (defaults to env DATA_CLEANER_API_KEY)

    Returns
    -------
    Dict[col_name -> FieldInfo]
    """
    custom_rules = custom_rules or {}
    results: Dict[str, FieldInfo] = {}
    uncertain_cols: List[str] = []

    for col in df.columns:
        col_str = str(col).strip()

        # 1. User override
        if col_str in custom_rules:
            try:
                ft = FieldType(custom_rules[col_str])
                results[col] = FieldInfo(ft, 1.0, [])
                continue
            except ValueError:
                pass

        # 2. Compute pattern scores
        scores: Dict[FieldType, float] = {}
        series = df[col].astype(str)

        for ftype, pat in _PATTERNS.items():
            pattern_score  = _avg_match_score(series, pat)
            name_score     = _col_name_score(col_str, ftype)
            # Combine: pattern is primary, name hints are bonus
            combined = pattern_score * 0.7 + name_score * 0.3
            if combined > 0:
                scores[ftype] = min(combined, 1.0)

        # Special fast-path scorers — add to scores only if the best
        # type-specific pattern score is low (NUMBER is a generic fallback,
        # not a competitor to clear type signals like phone/email/ID).
        num_score    = _numeric_score(series)
        date_s       = _date_score(series)
        addr_s       = _address_score(series)
        gender_s     = _gender_score(series)
        name_s       = _name_score(series)           # Chinese / common name pattern

        best_type_score = max(scores.values()) if scores else 0.0

        # NUMBER only wins when no specific type has scored clearly (below 0.7)
        if num_score > 0.5 and best_type_score < 0.7:
            scores[FieldType.NUMBER] = num_score

        if date_s > best_type_score:
            scores[FieldType.DATE] = date_s

        if addr_s > 0.5:
            scores[FieldType.ADDRESS] = addr_s

        if gender_s > 0.5:
            scores[FieldType.GENDER] = gender_s

        if name_s > best_type_score:
            scores[FieldType.NAME] = name_s

        # 3. Pick best match
        if not scores:
            results[col] = FieldInfo(FieldType.UNKNOWN, 0.0, _samples(series, 3))
            uncertain_cols.append(col)
            continue

        best_ftype = max(scores, key=lambda k: scores[k])
        confidence = scores[best_ftype]

        # Low confidence → mark uncertain
        if confidence < 0.6:
            uncertain_cols.append(col)

        results[col] = FieldInfo(
            field_type=best_ftype,
            confidence=confidence,
            samples=_samples(series, 3),
        )

    # 4. AI assist for uncertain columns
    if uncertain_cols and ai_model:
        _fill_with_ai(results, uncertain_cols, df, ai_model, ai_api_key)

    return results


def _samples(series: pd.Series, n: int = 3) -> List[str]:
    vals = [str(v) for v in series if str(v) not in ("", "nan", "NaN")]
    return list(dict.fromkeys(vals))[:n]  # unique, preserve order


# ─── AI-assisted identification ───────────────────────────────────────────────

def _fill_with_ai(
    results: Dict[str, FieldInfo],
    uncertain_cols: List[str],
    df: pd.DataFrame,
    model: str,
    api_key: Optional[str],
) -> None:
    api_key = api_key or os.environ.get("DATA_CLEANER_API_KEY", "")
    if not api_key:
        return

    import urllib.request
    import urllib.parse

    col_samples = {
        col: _samples(df[col].astype(str), 5)
        for col in uncertain_cols
    }

    prompt = (
        "你是一个数据分析师。请根据以下列名和样本值，判断每列的字段类型。\n"
        "字段类型可选：姓名、手机号、邮箱、地址、金额、日期、SKU、订单号、身份证、性别、网址、IP地址、银行账号、文本、数字、未知\n"
        "只输出JSON对象，格式：{\"列名\": \"类型\"}\n"
        f"\n列名与样本值：\n{json.dumps(col_samples, ensure_ascii=False)}\n"
    )

    try:
        if model in ("deepseek", "minimax"):
            # Unified MiniMax/DeepSeek compatible API
            url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
            if model == "deepseek":
                url = "https://api.deepseek.com/v1/chat/completions"

            payload = json.dumps({
                "model": "MiniMax-Text-01" if model == "minimax" else "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
                "temperature": 0.1,
            }).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"]

            # Parse JSON from response
            match = re.search(r"\{[^{}]*\}", content, re.DOTALL)
            if match:
                ai_result = json.loads(match.group())
                for col, type_str in ai_result.items():
                    if col in results:
                        try:
                            ft = FieldType(type_str)
                            results[col] = FieldInfo(ft, 0.8, results[col].samples)
                        except ValueError:
                            pass
    except Exception:
        pass  # AI fallback: keep regex result


# ─── User-defined field mapping ───────────────────────────────────────────────

def apply_custom_mapping(
    field_info: Dict[str, FieldInfo],
    mapping: Dict[str, str],
) -> Dict[str, FieldInfo]:
    """
    Apply user-defined column → field_type overrides.
    mapping = {"姓名": "name", "电话": "phone"}
    """
    for col, type_str in mapping.items():
        if col in field_info:
            try:
                ft = FieldType(type_str)
                field_info[col] = FieldInfo(ft, 1.0, field_info[col].samples)
            except ValueError:
                pass
    return field_info


# ─── Summary ──────────────────────────────────────────────────────────────────

def field_summary(field_info: Dict[str, FieldInfo]) -> str:
    lines = ["### 字段识别结果"]
    for col, info in field_info.items():
        conf_pct = f"{info.confidence:.0%}"
        lines.append(f"- **{col}** → {info.label()}（置信度 {conf_pct}）")
    return "\n".join(lines)
