import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.customer_reception_advice.service import customer_reception_advice

COMMAND_NAME = "customer_reception_advice"
COMMAND_DESC = "实时客户接待画像 + 跟进建议(基于近 4 天旺旺聊天 + TPP 推理)。统一入参 --buyers，对象数组 JSON，每个对象含 login_id 或 phone 字段，如 '[{\"login_id\":\"alice\"},{\"phone\":\"138...\"}]'"


def _truncate(text: str, max_len: int = 20) -> str:
    text = text.strip()
    return text[:max_len] + "…" if len(text) > max_len else text


def _render_batch(results: list) -> str:
    total = len(results)
    lines = [
        "# 买家画像与跟进建议",
        "",
        "<!-- MODULE: reception_advice_batch -->",
        f"<!-- TOTAL: {total} -->",
        "",
    ]

    if not results:
        lines += [
            "<!-- STATUS: EMPTY -->",
            "",
            "> 无处理结果。",
            "",
            "<!-- /MODULE: reception_advice_batch -->",
        ]
        return "\n".join(lines)

    for i, r in enumerate(results, 1):
        if not isinstance(r, dict):
            continue
        login_id = (r.get("buyer_login_id") or "").strip() or "—"
        profile = _truncate(r.get("buyer_profile") or "")
        suggestion = _truncate(r.get("follow_suggestion") or "")

        profile_text = profile if profile else "_暂无画像_"
        suggestion_text = suggestion if suggestion else "_暂无建议_"

        lines += [
            f"**{i}. {login_id}**",
            f"画像：{profile_text}",
            f"建议：{suggestion_text}",
            "",
        ]
        chat_count = r.get("chat_history_count", 0)
        lines.append(f"<!-- BUYER_{i}: LOGIN_ID: {login_id} | CHAT_COUNT: {chat_count} -->")
        lines.append("")

    lines.append("<!-- /MODULE: reception_advice_batch -->")
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置,请运行:`python cli.py configure YOUR_AK`", {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--buyers", required=True,
                        help="买家对象数组 JSON,每个对象含 login_id 或 phone 字段。"
                             "示例: '[{\"login_id\":\"alice\"},{\"phone\":\"13800138000\"},{\"login_id\":\"bob\"}]'。"
                             "单买家也用此参数: '[{\"login_id\":\"alice\"}]'")
    args = parser.parse_args()

    try:
        buyers = json.loads(args.buyers)
        if not isinstance(buyers, list) or not buyers:
            print_output(False, "❌ 参数错误:--buyers 必须是非空 JSON 数组", {"data": {}})
            return
    except json.JSONDecodeError:
        print_output(False, "❌ 参数错误:--buyers 必须是合法 JSON 数组,如 '[{\"login_id\":\"alice\"}]'", {"data": {}})
        return

    try:
        resp = customer_reception_advice(buyers=buyers)
        results = resp.get("results", [])
        print_output(True, _render_batch(results), {"data": resp})
    except ValueError as e:
        print_output(False, f"❌ 参数错误:{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
