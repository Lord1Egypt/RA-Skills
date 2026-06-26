#!/usr/bin/env python3
"""
validate_sms_template_params.py
对 Lisa 短信任务的 templateParamList 做硬约束校验（pre-flight gate）。

用法:
  python3 validate_sms_template_params.py '<templateParamList JSON>'

输入 JSON 形如:
  [
    {"variableLabel":"conference","variableAttribute":"unit_name","variableValue":"库阔科技"},
    {"variableLabel":"address",   "variableAttribute":"address",  "variableValue":"杭州萧山"},
    {"variableLabel":"time",      "variableAttribute":"time",     "variableValue":"2026年5月15日 14:00"}
  ]

输出（stdout，单行 JSON，便于 LLM 解析）:
  {
    "ok": false,
    "summary": "1/3 变量校验失败，禁止提交",
    "results": [
      {"label":"conference","attribute":"unit_name","value":"库阔科技","status":"PASS","reason":"OK"},
      {"label":"address",   "attribute":"address",  "value":"杭州萧山","status":"PASS","reason":"OK"},
      {"label":"time","attribute":"time","value":"2026年5月15日 14:00","status":"FAIL",
       "reason":"time 类变量不得包含中文「年/月/日」（运营商网关会拒绝）",
       "suggestion":"改写为 2026-05-15 14:00 或 5月15日 14:00 后重试"}
    ]
  }

退出码:
  0 — 全部 PASS（ok=true）
  1 — 至少一项 FAIL（ok=false）
  2 — 输入格式错误 / 解析失败
"""

import json
import re
import sys
from typing import Any


# ── 校验规则实现 ─────────────────────────────────────────────────────────────
# 每个 attribute 对应一个 (validator, hint)。validator 接收原始字符串值，
# 返回 (status, reason, suggestion) 三元组。status ∈ {"PASS","FAIL"}。

CN_HAN = re.compile(r"^[\u4e00-\u9fff]+$")
CN_HAN_ANY = re.compile(r"[\u4e00-\u9fff]")
URL_PAT = re.compile(r"https?://|www\.|\b\d{1,3}(?:\.\d{1,3}){3}\b", re.IGNORECASE)
QQ_WX_PAT = re.compile(r"(?:QQ|微信|wechat|weixin)\D{0,4}\d{5,}", re.IGNORECASE)
PHONE_LIKE = re.compile(r"\b1[3-9]\d{9}\b")
EMOJI_PAT = re.compile(
    "["                                  # rough emoji range
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "]"
)


def _len(s: str) -> int:
    """长度按字符计算（中文一字算一字，与运营商规则保持一致）。"""
    return len(s)


def v_number_captcha(v: str):
    if re.fullmatch(r"\d{4,6}", v):
        return ("PASS", "OK", None)
    return ("FAIL", "纯数字 4–6 位", "示例：123456")


def v_character_with_number2(v: str):
    if re.fullmatch(r"[A-Za-z0-9]{4,6}", v):
        return ("PASS", "OK", None)
    return ("FAIL", "数字+字母组合或仅字母，长度 4–6 位", "示例：A1b2C3")


def v_verify_time(v: str):
    if re.fullmatch(r"[1-9]\d?", v):
        return ("PASS", "OK", None)
    return ("FAIL", "1–99 的整数", "示例：5（表示 5 分钟）")


def v_time(v: str):
    # 高频事故：含中文「年月日」的时间字符串被运营商网关拒绝。
    if "年" in v:
        return (
            "FAIL",
            "time 类变量不得包含中文「年」（运营商网关会拒绝整批短信）",
            "改写为 2026-05-15 14:00 或 5月15日 14:00 后重试",
        )
    # 允许的形态：YYYY-MM-DD、YYYY/MM/DD、HH:mm、上午/下午X点、M月D日 等组合。
    accepted = [
        re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:[ T]\d{1,2}:\d{2})?"),
        re.compile(r"\d{1,2}:\d{2}"),
        re.compile(r"(上午|下午|早上|中午|晚上)\s*\d{1,2}\s*(点|:\d{2})?"),
        re.compile(r"\d{1,2}月\d{1,2}日(?:\s*\d{1,2}[:：]\d{2})?"),
    ]
    for pat in accepted:
        if pat.search(v):
            if _len(v) > 30:
                return ("FAIL", "time 字符串过长（>30 字符）", "示例：2026-05-15 14:00")
            return ("PASS", "OK", None)
    return (
        "FAIL",
        "未识别为合法时间/日期格式",
        "推荐 YYYY-MM-DD HH:mm，如 2026-05-15 14:00",
    )


def v_money(v: str):
    if re.fullmatch(r"\d+(?:\.\d{1,2})?", v):
        return ("PASS", "OK", None)
    return ("FAIL", "纯数字或小数，不含单位符号（¥/$/元 等一律去掉）", "示例：99.00")


def v_user_nick(v: str):
    if _len(v) > 20:
        return ("FAIL", "user_nick 不超过 20 字符", None)
    if EMOJI_PAT.search(v):
        return ("FAIL", "user_nick 不得含 emoji", None)
    if QQ_WX_PAT.search(v) or PHONE_LIKE.search(v):
        return ("FAIL", "user_nick 不得含 QQ/微信号/手机号", None)
    return ("PASS", "OK", None)


def v_name(v: str):
    if not CN_HAN.fullmatch(v):
        return ("FAIL", "name 必须是简体中文", "示例：张三")
    if not (2 <= _len(v) <= 5):
        return ("FAIL", "name 长度 2–5 个汉字", None)
    return ("PASS", "OK", None)


def v_unit_name(v: str):
    if not CN_HAN.fullmatch(v):
        return (
            "FAIL",
            "unit_name 必须仅中文（不得含英文/数字/空格/符号）",
            "示例：库阔数字科技",
        )
    if _len(v) > 20:
        return ("FAIL", "unit_name 不超过 20 字符", None)
    return ("PASS", "OK", None)


def v_address(v: str):
    if _len(v) > 30:
        return ("FAIL", "address 不超过 30 字符", None)
    if QQ_WX_PAT.search(v):
        return ("FAIL", "address 不得含 QQ/微信号", None)
    if URL_PAT.search(v):
        return ("FAIL", "address 不得含 URL/IP", None)
    return ("PASS", "OK", None)


def v_license_plate(v: str):
    if not (1 <= _len(v) <= 10):
        return ("FAIL", "车牌号长度需 ≤ 10", None)
    return ("PASS", "OK", None)


def v_tracking_number(v: str):
    if re.fullmatch(r"\d{8,16}", v) or re.fullmatch(r"[A-Za-z][A-Za-z0-9]{7,15}", v):
        return ("PASS", "OK", None)
    return ("FAIL", "8–16 位数字，或字母开头+字母数字", "示例：SF1234567890")


def v_pick_up_code(v: str):
    if re.fullmatch(r"[\d\-_]{4,8}", v):
        return ("PASS", "OK", None)
    return ("FAIL", "4–8 位数字/短横线/下划线", "示例：12-34")


def v_other_number2(v: str):
    if not (1 <= _len(v) <= 35):
        return ("FAIL", "长度需 1–35 字符", None)
    if not re.fullmatch(r"[A-Za-z0-9]+", v):
        return ("FAIL", "仅允许字母/数字", None)
    return ("PASS", "OK", None)


def v_phone_number2(v: str):
    if re.fullmatch(r"\d{3,12}", v):
        return ("PASS", "OK", None)
    return (
        "FAIL",
        "phone_number2 需 3–12 位纯数字（去掉 +、空格、横杠）",
        "示例：13812345678",
    )


def v_link_param(v: str):
    if URL_PAT.search(v):
        return ("FAIL", "link_param 不得含完整链接/IP", None)
    if re.fullmatch(r"[A-Za-z0-9]{1,8}", v):
        return ("PASS", "OK", None)
    return ("FAIL", "1–8 位英文数字", "示例：abc123")


def v_email_address(v: str):
    if not (7 <= _len(v) <= 30):
        return ("FAIL", "邮箱长度 7–30 字符", None)
    if "@" not in v:
        return ("FAIL", "邮箱必须包含 @", None)
    return ("PASS", "OK", None)


def v_others(v: str):
    if _len(v) > 35:
        return ("FAIL", "others 不超过 35 字符", None)
    if QQ_WX_PAT.search(v) or PHONE_LIKE.search(v) or URL_PAT.search(v):
        return ("FAIL", "others 不得含 QQ/微信/手机/网址", None)
    return ("PASS", "OK", None)


# attribute → validator 映射（与 SKILL.md 表保持一致）
VALIDATORS = {
    "numberCaptcha": v_number_captcha,
    "characterWithNumber2": v_character_with_number2,
    "verifyTime": v_verify_time,
    "time": v_time,
    "money": v_money,
    "user_nick": v_user_nick,
    "name": v_name,
    "unit_name": v_unit_name,
    "address": v_address,
    "license_plate_number": v_license_plate,
    "tracking_number": v_tracking_number,
    "pick_up_code": v_pick_up_code,
    "other_number2": v_other_number2,
    "phone_number2": v_phone_number2,
    "link_param": v_link_param,
    "email_address": v_email_address,
    "others": v_others,
}


def validate_one(item: dict[str, Any]) -> dict[str, Any]:
    label = item.get("variableLabel")
    attr = item.get("variableAttribute")
    value = item.get("variableValue")

    if not isinstance(label, str) or not label:
        return {
            "label": label,
            "attribute": attr,
            "value": value,
            "status": "FAIL",
            "reason": "variableLabel 必须是非空字符串",
        }
    if not isinstance(attr, str) or not attr:
        return {
            "label": label,
            "attribute": attr,
            "value": value,
            "status": "FAIL",
            "reason": "variableAttribute 必须是非空字符串（参照 SKILL.md 变量规则表的 code 列）",
        }
    if not isinstance(value, str):
        return {
            "label": label,
            "attribute": attr,
            "value": value,
            "status": "FAIL",
            "reason": "variableValue 必须是字符串（数字/布尔需先转字符串）",
        }
    if value.strip() == "":
        return {
            "label": label,
            "attribute": attr,
            "value": value,
            "status": "FAIL",
            "reason": "variableValue 不能为空",
        }

    validator = VALIDATORS.get(attr)
    if validator is None:
        # 未知 attribute 一律按 others 兜底，并提示 LLM 应使用合法 code。
        status, reason, suggestion = v_others(value)
        out = {
            "label": label,
            "attribute": attr,
            "value": value,
            "status": status,
            "reason": (
                f"未识别的 variableAttribute={attr!r}，已按 others 规则校验：{reason}"
            ),
        }
        if suggestion:
            out["suggestion"] = suggestion
        return out

    status, reason, suggestion = validator(value)
    out = {
        "label": label,
        "attribute": attr,
        "value": value,
        "status": status,
        "reason": reason,
    }
    if suggestion:
        out["suggestion"] = suggestion
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"ok": False, "summary": "缺少参数：需传入 templateParamList JSON 字符串"},
                ensure_ascii=False,
            )
        )
        return 2

    raw = sys.argv[1]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {"ok": False, "summary": f"JSON 解析失败：{exc}"},
                ensure_ascii=False,
            )
        )
        return 2

    if not isinstance(data, list):
        print(
            json.dumps(
                {"ok": False, "summary": "templateParamList 必须是数组"},
                ensure_ascii=False,
            )
        )
        return 2

    if len(data) == 0:
        # 模板无变量是合法情形
        print(
            json.dumps(
                {"ok": True, "summary": "模板无变量，跳过校验", "results": []},
                ensure_ascii=False,
            )
        )
        return 0

    results = [validate_one(item) for item in data]
    fail_count = sum(1 for r in results if r.get("status") == "FAIL")
    ok = fail_count == 0
    summary = (
        f"{len(results)}/{len(results)} 变量校验通过，可继续提交"
        if ok
        else f"{fail_count}/{len(results)} 变量校验失败，禁止提交"
    )
    print(json.dumps({"ok": ok, "summary": summary, "results": results}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
