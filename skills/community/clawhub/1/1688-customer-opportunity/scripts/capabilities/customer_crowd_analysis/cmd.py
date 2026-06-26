import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.customer_crowd_analysis.service import (
    customer_crowd_analysis, batch_customer_crowd_analysis
)

COMMAND_NAME = "customer_crowd_analysis"
COMMAND_DESC = "客户机会跟进方案分析（支持单个或批量 loginId，线程池并发）"


def _render_no_data(data: dict) -> str:
    crowd_type = data.get("crowd_type", "")
    reason = data.get("no_data_reason", "近 30 天无该客户的算法分析数据")
    return (
        f"# 客户跟进方案 — {crowd_type}\n\n"
        "<!-- MODULE: crowd_analysis -->\n"
        "<!-- STATUS: NO_DATA -->\n\n"
        f"> {reason}\n\n"
        "建议调整日期（`--ds`）或人群类型（`--crowd-type`）后重试。\n\n"
        "<!-- /MODULE: crowd_analysis -->"
    )


def _render_normal(data: dict) -> str:
    crowd_type = data.get("crowd_type", "")
    profile = data.get("buyer_profile", {})
    analysis_reason = data.get("analysis_reason", "")
    recommend_strategy = data.get("recommend_strategy", [])
    recommend_offers = data.get("recommend_offers", [])
    recommend_coupons = data.get("recommend_coupons", [])
    chat_script = data.get("chat_script", "")
    buyer_login_id = profile.get("login_id", "")
    tags = profile.get("tags", [])

    lines = [
        f"# 客户跟进方案 — {crowd_type}",
        "",
        "<!-- MODULE: crowd_analysis -->",
        f"<!-- CROWD_TYPE: {crowd_type} -->",
        f"<!-- BUYER_LOGIN_ID: {buyer_login_id} -->",
        "<!-- STATUS: NORMAL -->",
        "",
        "## 一、买家画像",
        "",
        f"- **账号**：{buyer_login_id or '—'}",
        f"- **标签**：{', '.join(tags) if tags else '—'}",
        "",
        "## 二、分析原因",
        "",
        analysis_reason if analysis_reason else "_暂无分析数据_",
        "",
        "## 三、推荐运营策略",
        "",
    ]
    if recommend_strategy:
        for s in recommend_strategy:
            lines.append(f"- {s}")
    else:
        lines.append("_暂无推荐策略_")
    lines.append("")

    lines += ["## 四、推荐商品", ""]
    if recommend_offers:
        lines += ["| 商品 | 价格 |", "|------|------|"]
        for o in recommend_offers:
            title = o.get("title") or "—"
            price = o.get("price") or "—"
            lines.append(f"| {title} | {price} |")
    else:
        lines.append("_暂无推荐商品_")
    lines.append("")

    lines += ["## 五、推荐优惠券", ""]
    if recommend_coupons:
        for c in recommend_coupons:
            coupon_id = c.get("coupon_id") or "—"
            name = c.get("name") or "—"
            amount = c.get("amount") or "—"
            lines.append(f"- 券ID：{coupon_id}，{name}，面值：{amount}")
    else:
        lines.append("_暂无推荐优惠券_")
    lines.append("")

    lines += ["## 六、旺旺触达话术", ""]
    lines.append(f"> {chat_script}" if chat_script else "_暂无话术_")
    lines.append("")
    lines.append("<!-- /MODULE: crowd_analysis -->")
    return "\n".join(lines)


def render_markdown(data: dict) -> str:
    if not isinstance(data, dict):
        return _render_no_data({})
    if "no_data_reason" in data:
        return _render_no_data(data)
    return _render_normal(data)


def _render_batch(data: dict) -> str:
    crowd_type = data.get("crowd_type", "")
    total = data.get("total", 0)
    success = data.get("success", 0)
    failed = data.get("failed", 0)
    results = data.get("results") or []

    lines = [
        f"# 批量客户跟进方案 — {crowd_type}（共 {total} 人，成功 {success} 人，失败 {failed} 人）",
        "",
        "<!-- MODULE: batch_crowd_analysis -->",
        f"<!-- CROWD_TYPE: {crowd_type} -->",
        f"<!-- TOTAL: {total} --><!-- SUCCESS: {success} --><!-- FAILED: {failed} -->",
        "",
    ]

    for i, r in enumerate(results, 1):
        label = r.get("label") or "unknown"
        status = r.get("status", "FAILED")

        if status == "OK":
            analysis_data = r.get("data") or {}
            lines += [
                f"## {i}. {label}",
                "",
                f"<!-- BUYER_LABEL: {label} --><!-- BUYER_LOGIN_ID: {label} --><!-- STATUS: NORMAL -->",
                "",
            ]
            lines.append(render_markdown(analysis_data))
            lines += ["", "---", ""]
        else:
            reason = r.get("reason") or "未知错误"
            lines += [
                f"## {i}. {label}",
                "",
                f"<!-- BUYER_LOGIN_ID: {label} --><!-- STATUS: FAILED --><!-- REASON: {reason} -->",
                "",
                f"> ❌ {reason}，已跳过。",
                "",
                "---",
                "",
            ]

    lines.append("<!-- /MODULE: batch_crowd_analysis -->")
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，请运行：`python cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("-t", "--crowd-type", required=True,
                        help="人群类型：流失买家/周期采购/询盘未成交/老客促活")
    parser.add_argument("--ds", help="数据日期 YYYYMMDD（默认昨日）")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--buyer-login-id", help="单个买家 loginId")
    group.add_argument("--buyer-login-ids",
                       help='批量买家 loginId JSON 数组，例：\'["alice","bob"]\'')
    args = parser.parse_args()

    try:
        if args.buyer_login_id:
            result = customer_crowd_analysis(
                crowd_type=args.crowd_type,
                buyer_login_id=args.buyer_login_id,
                ds=args.ds,
            )
            print_output(True, render_markdown(result), {"data": result})
        else:
            try:
                lids = json.loads(args.buyer_login_ids)
                if not isinstance(lids, list) or not lids:
                    raise ValueError("--buyer-login-ids 必须是非空 JSON 数组")
            except json.JSONDecodeError as e:
                print_output(False, f"❌ --buyer-login-ids 参数 JSON 解析失败：{e}", {"data": {}})
                return

            result = batch_customer_crowd_analysis(
                crowd_type=args.crowd_type,
                buyer_login_ids=[str(x) for x in lids],
                ds=args.ds,
            )
            success_flag = result.get("failed", 0) < result.get("total", 1)
            print_output(success_flag, _render_batch(result), {"data": result})

    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
