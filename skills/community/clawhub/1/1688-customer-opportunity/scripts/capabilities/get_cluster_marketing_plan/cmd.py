import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.get_cluster_marketing_plan.service import get_cluster_marketing_plan

COMMAND_NAME = "get_cluster_marketing_plan"
COMMAND_DESC = "查询客群运营方案（商品/文案/海报），planId 来自 list_customer_cluster"


def _render_markdown(data: dict) -> str:
    if not data:
        return "<!-- MODULE: cluster_marketing_plan -->\n> 该客群暂无运营方案。\n<!-- /MODULE: cluster_marketing_plan -->"

    plan_id = data.get("plan_id") or "—"
    sale_desc = data.get("sale_desc") or ""

    lines = [
        "# 客群智能运营方案",
        "",
        "<!-- MODULE: cluster_marketing_plan -->",
        f"<!-- PLAN_ID: {plan_id} -->",
        "",
    ]

    if sale_desc:
        lines += [f"> {sale_desc}", ""]
    else:
        lines += ["> 该客群暂无推荐文案。", ""]

    lines.append("<!-- /MODULE: cluster_marketing_plan -->")

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
        result = get_cluster_marketing_plan(plan_id=args.plan_id)
        print_output(True, _render_markdown(result), {"data": result})
    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
