import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.list_cluster_buyer_detail.service import list_cluster_buyer_detail

COMMAND_NAME = "list_cluster_buyer_detail"
COMMAND_DESC = "查询客群买家明细（加入时间），planId 来自 list_customer_cluster"


def _render_markdown(data: dict) -> str:
    plan_id = data.get("plan_id") or "—"
    buyer_count = data.get("buyer_count", 0)
    buyers = data.get("list") or []

    lines = [
        "# 客群买家明细",
        "",
        "<!-- MODULE: cluster_buyer_detail -->",
        f"<!-- PLAN_ID: {plan_id} -->",
        f"<!-- BUYER_COUNT: {buyer_count} -->",
    ]

    if not buyers:
        lines += [
            "<!-- STATUS: EMPTY -->",
            "",
            "> 该客群暂无买家明细数据。",
            "",
            "<!-- /MODULE: cluster_buyer_detail -->",
        ]
        return "\n".join(lines)

    display_buyers = buyers[:10]
    lines += [
        "<!-- STATUS: NORMAL -->",
        "",
        f"> 客群 `{plan_id}` 共 {buyer_count} 名买家，展示前 {len(display_buyers)} 名",
        "",
        "| # | 买家账号 | 加入时间 |",
        "|---|---------|---------|",
    ]

    login_ids = []
    for i, b in enumerate(display_buyers, 1):
        login_id = b.get("buyer_login_id") or "—"
        add_date = b.get("add_date") or "—"
        lines.append(f"| {i} | {login_id} | {add_date} |")
        login_ids.append(login_id)

    lines.append(f"<!-- BUYER_LOGIN_IDS: {json.dumps(login_ids, ensure_ascii=False)} -->")

    lines += [
        "",
        f"> 共 {buyer_count} 名买家。导出完整名单请从 `data` 字段提取 `list` 数组，生成 Excel 后使用 Excel/WPS 打开查看。",
    ]

    lines.append("<!-- /MODULE: cluster_buyer_detail -->")
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，请运行：`python cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--plan-id", required=True, help="客群计划 ID（来自 list_customer_cluster 返回）")
    args = parser.parse_args()

    try:
        result = list_cluster_buyer_detail(plan_id=args.plan_id)
        print_output(True, _render_markdown(result), {"data": result})
    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
