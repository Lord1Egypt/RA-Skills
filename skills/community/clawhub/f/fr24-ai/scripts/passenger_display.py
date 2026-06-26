"""乘客字段展示：用户输入 ↔ 接口参数对照。"""
from __future__ import annotations

from typing import Any

GENDER_LABEL = {"M": "男", "F": "女"}
PAX_TYPE_LABEL = {"ADT": "成人", "CHD": "儿童", "INF": "婴儿"}


def _field(label: str, user_input: str, api_value: str, *, extra: str | None = None) -> dict[str, str]:
    row: dict[str, str] = {
        "label": label,
        "userInput": user_input,
        "apiValue": api_value,
    }
    if extra:
        row["note"] = extra
    return row


def build_passenger_display(
    passengers: list[dict[str, Any]],
    *,
    raw_mappings: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """生成供用户核对的乘客字段表。"""
    displays: list[dict[str, Any]] = []
    for i, pax in enumerate(passengers):
        raw = (raw_mappings or [{}])[i] if raw_mappings else {}
        py = raw.get("namePinyin")
        py_note = f"拼音 {py}" if py else None
        fields: list[dict[str, str]] = [
            _field(
                "姓名",
                raw.get("nameRaw", pax.get("name", "")),
                pax.get("name", ""),
                extra=py_note,
            ),
            _field("性别", raw.get("genderRaw", GENDER_LABEL.get(pax.get("gender", "M"), "")), pax.get("gender", "")),
            _field("出生日期", raw.get("birthdayRaw", pax.get("birthday", "")), pax.get("birthday", "")),
            _field("证件类型", "护照", pax.get("cardType", "PP")),
            _field("证件号", raw.get("cardNumRaw", pax.get("cardNum", "")), pax.get("cardNum", "")),
            _field(
                "证件有效期",
                raw.get("expiryRaw", pax.get("cardExpiryDate", "")),
                pax.get("cardExpiryDate", ""),
            ),
            _field("国籍", raw.get("nationalityRaw", pax.get("nationality", "CN")), pax.get("nationality", "CN")),
            _field(
                "乘客类型",
                PAX_TYPE_LABEL.get(pax.get("paxType", "ADT"), pax.get("paxType", "")),
                pax.get("paxType", "ADT"),
            ),
        ]
        if raw.get("cardNumWarning"):
            fields[4]["note"] = raw["cardNumWarning"]
        displays.append(
            {
                "paxId": pax.get("paxId"),
                "summaryLine": _summary_line(pax, raw),
                "fields": fields,
            }
        )
    return displays


def build_contact_display(
    contact: dict[str, str],
    *,
    raw: dict[str, Any] | None = None,
) -> dict[str, Any]:
    r = raw or {}
    fields = [
        _field("联系人姓名", r.get("nameRaw", contact.get("agentName", "")), contact.get("agentName", "")),
        _field("手机", r.get("mobileRaw", contact.get("mobile", "")), contact.get("mobile", "")),
        _field("邮箱", r.get("emailRaw", contact.get("agentEmail", "")), contact.get("agentEmail", "")),
        _field("区号", "86", contact.get("areaCode", "86")),
    ]
    return {
        "summaryLine": (
            f"联系人 {contact.get('agentName')} "
            f"{contact.get('mobile')} {contact.get('agentEmail')}"
        ),
        "fields": fields,
    }


def _summary_line(pax: dict[str, Any], raw: dict[str, Any]) -> str:
    name_ui = raw.get("nameRaw", pax.get("name", ""))
    py = raw.get("namePinyin", "")
    py_part = f" {py}" if py else ""
    g = raw.get("genderRaw") or GENDER_LABEL.get(pax.get("gender", "M"), "")
    return (
        f"{name_ui}{py_part} {g} {pax.get('birthday')} "
        f"护照{pax.get('cardNum')} {pax.get('cardExpiryDate')}到期"
    )


def format_display_message(passenger_display: list[dict], contact_display: dict) -> str:
    lines = ["请核对乘客与联系人（左侧为您输入，apiValue 为将提交接口的值）：", ""]
    for p in passenger_display:
        lines.append(p.get("summaryLine", ""))
        for f in p.get("fields") or []:
            note = f" ({f['note']})" if f.get("note") else ""
            py = ""
            if f["label"] == "姓名" and f.get("note") and "拼音" not in f.get("note", ""):
                py = f" [{f['note']}]"
            elif f["label"] == "姓名" and f.get("note"):
                py = f" [{f['note']}]"
            lines.append(f"  - {f['label']}：{f['userInput']} → {f['apiValue']}{note}")
    lines.append("")
    lines.append(contact_display.get("summaryLine", ""))
    for f in contact_display.get("fields") or []:
        lines.append(f"  - {f['label']}：{f['userInput']} → {f['apiValue']}")
    lines.append("")
    lines.append("若无误请回复「乘客信息确认无误」，再为您校验报价。")
    return "\n".join(lines)
