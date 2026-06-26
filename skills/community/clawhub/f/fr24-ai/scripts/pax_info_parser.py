"""从自然语言解析乘客与联系人（供 flight_parse_passengers / 预订核对）。"""
from __future__ import annotations

import re
from typing import Any

# 日期：1990-01-15 / 1990年1月15日
_DATE_RE = re.compile(r"(?P<y>\d{4})[年/\-.](?P<m>\d{1,2})[月/\-.](?P<d>\d{1,2})日?")
_EXPIRY_RE = re.compile(
    r"(?P<y>\d{4})[年/\-.](?P<m>\d{1,2})[月/\-.](?P<d>\d{1,2})日?\s*(?:到期|失效|有效期)"
)
_PASSPORT_RE = re.compile(
    r"(?:护照|证件号?|passport)\s*[:：]?\s*([A-Za-z0-9]{3,12})",
    re.I,
)
_MOBILE_RE = re.compile(
    r"(?:手机|电话|mobile|tel)\s*[:：]?\s*(?:\+?86[-\s]?)?(1[3-9]\d{9})",
    re.I,
)
_EMAIL_RE = re.compile(
    r"(?:邮箱|email)\s*[:：]?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    re.I,
)
_GENDER_RE = re.compile(r"(男|女|male|female|\b[MF]\b)", re.I)
_NAME_SLASH_RE = re.compile(r"([A-Za-z]{2,12}/[A-Za-z]{2,12})")
_PAX_LINE_RE = re.compile(
    r"(?:乘客|成人|儿童|婴儿|pax)\s*[:：]?\s*([^，,。\n]+)",
    re.I,
)
# 无「乘客：」前缀时，行首中文名 + 性别
_INLINE_PAX_RE = re.compile(
    r"^[\s]*([\u4e00-\u9fffA-Za-z]{2,20})\s+(男|女)\s+",
    re.M,
)
_CONTACT_NAME_RE = re.compile(r"联系人\s*[:：]?\s*([^，,。\n]+)", re.I)
_CHILD_MARK = re.compile(r"儿童|CHD|child", re.I)
_INFANT_MARK = re.compile(r"婴儿|INF|infant", re.I)
_CHINESE_RE = re.compile(r"^[\u4e00-\u9fff]{2,8}$")


def _fmt_date(y: str, m: str, d: str) -> str:
    return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"


def _first_date(text: str) -> str | None:
    m = _DATE_RE.search(text)
    if not m:
        return None
    return _fmt_date(m.group("y"), m.group("m"), m.group("d"))


def _expiry_date(text: str) -> str | None:
    m = _EXPIRY_RE.search(text)
    if m:
        return _fmt_date(m.group("y"), m.group("m"), m.group("d"))
    dates = list(_DATE_RE.finditer(text))
    if len(dates) >= 2:
        last = dates[-1]
        return _fmt_date(last.group("y"), last.group("m"), last.group("d"))
    return None


def _gender_raw_and_code(text: str) -> tuple[str, str]:
    m = _GENDER_RE.search(text)
    if not m:
        return "男", "M"
    g = m.group(1)
    if g.upper() in ("M", "MALE", "男"):
        return "男", "M"
    return "女", "F"


def chinese_to_ticket_name(name: str) -> tuple[str, str]:
    """
    中文或拼音 → 机票姓名 TICKET/NAME 与展示用拼音（如 weiwei）。

    Returns:
        (apiName, displayPinyin)
    """
    name = name.strip()
    m = _NAME_SLASH_RE.search(name)
    if m:
        ticket = m.group(1).upper()
        return ticket, ticket.replace("/", "").lower()

    clean = re.sub(r"[（(].*?[）)]", "", name)
    clean = re.sub(r"[，,].*$", "", clean).strip()
    if not clean:
        return name.upper(), name.lower()

    if not _CHINESE_RE.match(clean):
        parts = clean.split()
        if len(parts) >= 2:
            return f"{parts[0].upper()}/{parts[1].upper()}", clean.lower()
        return clean.upper(), clean.lower()

    try:
        from pypinyin import Style, lazy_pinyin

        py = lazy_pinyin(clean, style=Style.NORMAL)
        if not py:
            return clean, clean
        surname = py[0].upper()
        given = "".join(x.capitalize() for x in py[1:]).upper() if len(py) > 1 else surname
        if len(py) == 1 and len(clean) >= 2:
            # 两字名：张三 → ZHANG/SAN
            given = py[0].upper()
        ticket = f"{surname}/{given}"
        display_py = "".join(py)
        return ticket, display_py
    except ImportError:
        pass

    # 无 pypinyin：双字名每字取首字母占位（建议安装 pypinyin）
    if len(clean) == 2:
        syl = "WEI"  # 占位，Agent 应提示用户确认拼音
        ticket = f"{syl}/{syl}"
        return ticket, clean
    return clean, clean


def _extract_name_raw(chunk: str, pm: re.Match[str] | None) -> str:
    if pm:
        return pm.group(1).strip()
    im = _INLINE_PAX_RE.search(chunk)
    if im:
        return im.group(1).strip()
    return chunk[:40].strip()


def _pax_type(text: str) -> str:
    if _INFANT_MARK.search(text):
        return "INF"
    if _CHILD_MARK.search(text):
        return "CHD"
    return "ADT"


def parse_passengers_and_contact(
    text: str,
) -> tuple[list[dict[str, Any]], dict[str, str] | None, list[dict[str, Any]], dict[str, Any] | None, str | None]:
    """
    解析自然语言。

    Returns:
        (passengers, agent_contact, raw_mappings, contact_raw, error)
    """
    if not text or not text.strip():
        return [], None, [], None, "内容为空"

    body = text.strip()
    passengers: list[dict[str, Any]] = []
    raw_mappings: list[dict[str, Any]] = []
    pax_id = 1

    chunks = re.split(r"(?=(?:乘客|成人|儿童|婴儿)\s*[:：])", body, flags=re.I)
    if len(chunks) <= 1:
        chunks = [body]

    for chunk in chunks:
        if not chunk.strip():
            continue
        if re.search(r"联系人\s*[:：]", chunk, re.I) and not _PAX_LINE_RE.search(chunk) and not _INLINE_PAX_RE.search(chunk):
            continue
        pm = _PAX_LINE_RE.search(chunk)
        if not pm and not _NAME_SLASH_RE.search(chunk) and not _INLINE_PAX_RE.search(chunk):
            continue

        name_raw = _extract_name_raw(chunk, pm)
        birthday = _first_date(chunk)
        if not birthday:
            return [], None, [], None, f"无法解析出生日期：{name_raw[:20]}"

        passport = _PASSPORT_RE.search(chunk)
        if not passport:
            return [], None, [], None, f"无法解析护照/证件号：{name_raw[:20]}"

        expiry = _expiry_date(chunk)
        if not expiry:
            return [], None, [], None, f"无法解析证件有效期：{name_raw[:20]}"

        ticket_name, display_py = chinese_to_ticket_name(name_raw)
        gender_raw, gender_code = _gender_raw_and_code(chunk)
        card_num = passport.group(1).upper()
        card_warn = None
        if len(card_num) < 6:
            card_warn = "证件号较短，请确认是否为完整护照号"

        nationality_raw = "CN"
        if re.search(r"国籍\s*[:：]?\s*([A-Za-z]{2})", chunk, re.I):
            nationality_raw = re.search(r"国籍\s*[:：]?\s*([A-Za-z]{2})", chunk, re.I).group(1).upper()

        pax: dict[str, Any] = {
            "paxId": pax_id,
            "name": ticket_name,
            "paxType": _pax_type(chunk),
            "birthday": birthday,
            "gender": gender_code,
            "cardNum": card_num,
            "cardType": "PP",
            "cardIssuedPlace": "CN",
            "cardExpiryDate": expiry,
            "nationality": nationality_raw,
        }
        if pax["paxType"] in ("CHD", "INF") and pax_id > 1:
            pax["accompaniedPaxId"] = "1"

        raw_mappings.append(
            {
                "nameRaw": name_raw,
                "namePinyin": display_py,
                "genderRaw": gender_raw,
                "birthdayRaw": birthday,
                "cardNumRaw": card_num,
                "expiryRaw": expiry,
                "nationalityRaw": nationality_raw,
                "cardNumWarning": card_warn,
            }
        )
        passengers.append(pax)
        pax_id += 1

    if not passengers:
        return [], None, [], None, "未识别到乘客信息"

    contact_raw: dict[str, Any] = {}
    cm = _CONTACT_NAME_RE.search(body)
    mobile = _MOBILE_RE.search(body)
    email = _EMAIL_RE.search(body)
    contact: dict[str, str] | None = None
    if cm or mobile or email:
        cname_raw = cm.group(1).strip() if cm else passengers[0]["name"]
        c_ticket, c_py = chinese_to_ticket_name(cname_raw)
        contact_raw = {
            "nameRaw": cname_raw,
            "namePinyin": c_py,
            "mobileRaw": mobile.group(1) if mobile else "",
            "emailRaw": email.group(1) if email else "",
        }
        contact = {
            "agentName": c_ticket if "/" in c_ticket else passengers[0]["name"],
            "agentEmail": email.group(1) if email else "booking@example.com",
            "mobile": mobile.group(1) if mobile else "13800138000",
            "areaCode": "86",
        }

    return passengers, contact, raw_mappings, contact_raw, None
