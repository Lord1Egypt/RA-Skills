#!/usr/bin/env python3

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from alert_data import (
    CLASSIFICATION_LABELS,
    PRIORITY_LABELS,
    analyze_inventory,
    build_abnormal_host_params,
    build_normal_host_params,
    build_problem_params,
    fetch_all_pages,
    load_env,
    read_json_rows,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate alert inspection report and Excel workbook")
    parser.add_argument("--output", default="reports", help="Output directory")
    parser.add_argument("--report-name", help="Report markdown filename")
    parser.add_argument("--problems-file", help="Read problem data from local JSON file")
    parser.add_argument("--hosts-file", help="Read host data from local JSON file")
    parser.add_argument("--page-size", type=int, default=200)
    parser.add_argument("--problem-page-size", type=int)
    parser.add_argument("--host-page-size", type=int)
    parser.add_argument("--status", type=int, default=1)
    parser.add_argument("--searchtype", default="history")
    parser.add_argument("--clock-begin", dest="clock_begin")
    parser.add_argument("--clock-end", dest="clock_end")
    parser.add_argument("--ip")
    parser.add_argument("--is-ip", dest="is_ip")
    parser.add_argument("--keyword")
    parser.add_argument("--is-maintenanced", dest="is_maintenanced")
    parser.add_argument("--is-acked", dest="is_acked")
    parser.add_argument("--classification", type=int)
    parser.add_argument("--subtype", type=int)
    parser.add_argument("--groupid", type=int)
    parser.add_argument("--priority")
    parser.add_argument("--sort-order", dest="sort_order")
    parser.add_argument("--sort-name", dest="sort_name")
    parser.add_argument("--hostid", type=int)
    parser.add_argument("--hostids")
    parser.add_argument("--true-ip", dest="true_ip", type=int)
    return parser.parse_args()


def load_rows(args):
    if args.problems_file or args.hosts_file:
        if not (args.problems_file and args.hosts_file):
            raise SystemExit("--problems-file 和 --hosts-file 必须同时提供")
        return read_json_rows(args.hosts_file), read_json_rows(args.problems_file)

    skill_dir = Path(__file__).resolve().parent
    load_env(skill_dir / ".env")
    load_env(skill_dir.parent / "alert-inspection" / ".env")

    api_url = Path
    del api_url
    import os

    api_url = os.environ.get("LWJK_API_URL", "")
    api_secret = os.environ.get("LWJK_API_SECRET", "")
    if not api_url or not api_secret:
        raise SystemExit("LWJK_API_URL 和 LWJK_API_SECRET 未配置，请检查 skills/alert-inspection/.env")

    problems = fetch_all_pages(
        api_url,
        api_secret,
        "/api/v6/alert/problem-list",
        build_problem_params(args),
        args.problem_page_size or args.page_size,
        "problem-list",
    )
    normal_hosts = fetch_all_pages(
        api_url,
        api_secret,
        "/api/v6/monitor/host-list",
        build_normal_host_params(args),
        args.host_page_size or args.page_size,
        "host-list-normal",
    )
    abnormal_hosts = fetch_all_pages(
        api_url,
        api_secret,
        "/api/v6/monitor/host-list",
        build_abnormal_host_params(args),
        args.host_page_size or args.page_size,
        "host-list-abnormal",
    )
    return normal_hosts + abnormal_hosts, problems


def build_summary(host_rows, problem_rows):
    analyzed = analyze_inventory(host_rows, problem_rows)
    hosts = analyzed["hosts"]
    problems = analyzed["problems"]
    normal_hosts = analyzed["normal_hosts"]
    abnormal_hosts = analyzed["abnormal_hosts"]
    priority_counts = Counter(analyzed["priority_counts"])
    host_problem_counts = defaultdict(lambda: {"count": 0, "max_priority": 0, "name": "", "ip": ""})

    for item in problems:
        key = item["hostid"] or item["ip"] or item["name"]
        entry = host_problem_counts[key]
        entry["count"] += 1
        entry["max_priority"] = max(entry["max_priority"], item["priority"])
        entry["name"] = item["name"]
        entry["ip"] = item["ip"]

    top_hosts = sorted(
        host_problem_counts.values(),
        key=lambda item: (-item["max_priority"], -item["count"], item["name"], item["ip"]),
    )[:20]
    top_problems = problems[:20]
    export_hosts = []
    for host in hosts:
        problem_entry = host_problem_counts.get(host["hostid"] or host["ip"] or host["name"], {})
        max_priority = problem_entry.get("max_priority", 0)
        export_hosts.append(
            {
                **host,
                "has_problem": host["active_status"] != 0,
                "is_normal": host["active_status"] == 0,
                "problem_count": problem_entry.get("count", 0),
                "max_priority": max_priority,
                "max_priority_label": PRIORITY_LABELS.get(max_priority, ""),
            }
        )

    return {
        "hosts": export_hosts,
        "problems": problems,
        "normal_hosts": normal_hosts,
        "abnormal_hosts": abnormal_hosts,
        "priority_counts": priority_counts,
        "top_hosts": top_hosts,
        "top_problems": top_problems,
    }


def render_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def build_report_markdown(summary: dict[str, Any], classification: int | None) -> str:
    environment = CLASSIFICATION_LABELS.get(classification, "全部设备")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    problems = summary["problems"]
    normal_hosts = summary["normal_hosts"]
    priority_counts = summary["priority_counts"]

    priority_rows = []
    for level in [5, 4, 3, 2, 1]:
        count = priority_counts.get(level, 0)
        ratio = f"{(count / len(problems) * 100):.2f}%" if problems else "0.00%"
        priority_rows.append((PRIORITY_LABELS[level], count, ratio))
    priority_rows.append(("合计", len(problems), "100.00%" if problems else "0.00%"))

    host_rows = []
    for item in summary["top_hosts"]:
        status_icon = "🔴" if item["max_priority"] >= 4 else "🟡" if item["max_priority"] >= 2 else "🔵"
        host_rows.append(
            (
                item["name"] or "-",
                item["ip"] or "-",
                item["count"],
                PRIORITY_LABELS.get(item["max_priority"], item["max_priority"]),
                status_icon,
            )
        )

    detail_rows = []
    for item in summary["top_problems"]:
        detail_rows.append(
            (
                item["name"] or "-",
                item["ip"] or "-",
                item["description"] or "-",
                PRIORITY_LABELS.get(item["priority"], item["priority"]),
                item["duration"] or "-",
            )
        )

    lines = [
        f"🚨 设备健康巡检报告 · {environment}",
        f"巡检时间：{now}",
        "报告生成: lerwee运维智能体",
        "",
        "📊 告警概览",
        *render_table(["告警等级", "数量", "占比"], priority_rows),
        "",
        "📋 告警主机列表",
    ]
    lines.extend(render_table(["主机", "IP", "告警数", "最高等级", "状态"], host_rows or [("-", "-", 0, "-", "🔵")]))
    lines.extend(
        [
            "",
            "⚠️ 告警详情（按等级从高到低）",
        ]
    )
    lines.extend(
        render_table(
            ["主机名", "IP", "告警描述", "等级", "持续时长"],
            detail_rows or [("-", "-", "-", "-", "-")],
        )
    )
    lines.extend(["", "📌 巡检结论"])

    severe_count = priority_counts.get(5, 0) + priority_counts.get(4, 0)
    attention_count = priority_counts.get(3, 0) + priority_counts.get(2, 0)
    lines.append(f"● 🔴 {severe_count}条高危告警需立即处理")
    lines.append(f"● ⚠️ {attention_count}条告警需关注")
    lines.append(f"● ✅ {len(normal_hosts)}台主机无告警")
    return "\n".join(lines) + "\n"


def resolve_paths(args):
    output_dir = Path(args.output).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = args.report_name or f"设备健康巡检报告_{stamp}.md"
    return output_dir / report_name


def main():
    args = parse_args()
    host_rows, problem_rows = load_rows(args)
    summary = build_summary(host_rows, problem_rows)
    report_path = resolve_paths(args)

    report_markdown = build_report_markdown(summary, args.classification)
    report_path.write_text(report_markdown, encoding="utf-8")
    normalized_hosts_path = report_path.with_name(report_path.stem + ".hosts.json")
    normalized_problems_path = report_path.with_name(report_path.stem + ".problems.json")
    normalized_hosts_path.write_text(json.dumps(summary["hosts"], ensure_ascii=False, indent=2), encoding="utf-8")
    normalized_problems_path.write_text(json.dumps(summary["problems"], ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {
        "report_file": str(report_path),
        "excel_file": None,
        "sheet_names": [],
        "hosts_file": str(normalized_hosts_path),
        "problems_file": str(normalized_problems_path),
        "total_hosts": len(summary["hosts"]),
        "normal_hosts": len(summary["normal_hosts"]),
        "abnormal_hosts": len(summary["abnormal_hosts"]),
        "total_problems": len(summary["problems"]),
        "environment_name": CLASSIFICATION_LABELS.get(args.classification, "全部设备"),
        "export_template": str(Path(__file__).resolve().parent / "references" / "export_excel_template.py"),
        "report_markdown": report_markdown,
        "next_step": "基于 references/export_excel_template.py 生成临时导出脚本，再导出 Excel",
        "host_query_strategy": {
            "normal": {"active_status": 0},
            "abnormal": {
                "active_status[0]": 1,
                "active_status[1]": 5,
                "active_status[2]": 4,
                "active_status[3]": 3,
                "active_status[4]": 2,
                "active_status[5]": -1,
            },
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
