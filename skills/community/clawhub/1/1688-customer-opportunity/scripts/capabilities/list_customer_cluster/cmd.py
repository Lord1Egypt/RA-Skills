import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.list_customer_cluster.service import list_customer_cluster

COMMAND_NAME = "list_customer_cluster"
COMMAND_DESC = "查询商家老客 AI 客群列表（含 buyerIdList，可衔接 customer_crowd_analysis）"


def _render_markdown(data: dict) -> str:
    cluster_list = data.get("list", [])
    cluster_count = data.get("cluster_count", 0)

    lines = [
        "# AI 客群列表",
        "",
        "<!-- MODULE: customer_cluster_list -->",
        f"<!-- CLUSTER_COUNT: {cluster_count} -->",
    ]

    if not cluster_list:
        lines += [
            "<!-- STATUS: EMPTY -->",
            "",
            "> 当前暂无客群数据，可能数据尚未更新（通常每周一更新）。",
            "",
            "<!-- /MODULE: customer_cluster_list -->",
        ]
        return "\n".join(lines)

    lines += [
        "<!-- STATUS: NORMAL -->",
        "",
        "> 根据店铺老客在平台上的行为表现，按不同维度智能划分客群，并针对不同客群提供完整运营方案提升复购；客群方案每周会根据买家最新数据刷新。",
        "",
        f"共 {cluster_count} 个老客客群。",
        "",
        "| # | 客群名称 | 买家数 | 特征描述 |",
        "|---|---------|-------|---------|",
    ]

    for i, cluster in enumerate(cluster_list, 1):
        plan_id = cluster.get("plan_id") or "—"
        cluster_name = cluster.get("cluster_name") or "—"
        feature = cluster.get("feature") or cluster.get("plan_reason") or "—"
        buyer_num = cluster.get("buyer_num")
        buyer_num_str = str(buyer_num) if buyer_num is not None else "—"

        lines.append(
            f"| {i} | {cluster_name} | {buyer_num_str} | {feature} |"
        )

    lines.append("")
    for i, cluster in enumerate(cluster_list, 1):
        plan_id = cluster.get("plan_id") or "—"
        cluster_main_tag = cluster.get("cluster_main_tag") or "—"
        lines.append(f"<!-- CLUSTER_{i}: PLAN_ID: {plan_id} | MAIN_TAG: {cluster_main_tag} -->")

    lines.append("<!-- /MODULE: customer_cluster_list -->")
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，请运行：`python cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    args = parser.parse_args()

    try:
        result = list_customer_cluster()
        print_output(True, _render_markdown(result), {"data": result})
    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
