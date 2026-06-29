#!/usr/bin/env python3
"""
成本优化分析器 — Cost Optimizer
分析查询日志和账单数据，识别成本热点，生成优化建议和 HTML 报告。
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

# ── 优化规则引擎 ──────────────────────────────────────────────────

OPTIMIZATION_RULES = [
    {
        "id": "R001",
        "name": "全表扫描检测",
        "description": "查询未使用分区过滤或索引，导致全表扫描",
        "detect": lambda q: any(kw in q.get("query_text", "").upper() for kw in ["SELECT *", "SELECT COUNT(*)"])
                            and "WHERE" not in q.get("query_text", "").upper(),
        "severity": "CRITICAL",
        "fix": "添加分区过滤条件 (WHERE dt = 'YYYY-MM-DD') 或使用聚簇键过滤",
        "savings_estimate": "80-99%",
    },
    {
        "id": "R002",
        "name": "SELECT * 滥用",
        "description": "SELECT * 读取所有列，增加扫描量和成本",
        "detect": lambda q: "SELECT *" in q.get("query_text", "").upper(),
        "severity": "HIGH",
        "fix": "只 SELECT 需要的列，减少 50-90% 的数据传输量",
        "savings_estimate": "50-90%",
    },
    {
        "id": "R003",
        "name": "重复查询检测",
        "description": "相同查询多次执行，可考虑物化视图缓存",
        "detect": lambda q, patterns: q.get("query_hash") in patterns.get("repeated", set()),
        "severity": "HIGH",
        "fix": "创建物化视图 (MATERIALIZED VIEW) 或使用 BI 工具缓存",
        "savings_estimate": "70-95%",
    },
    {
        "id": "R004",
        "name": "低效 JOIN 检测",
        "description": "JOIN 条件缺少索引/聚簇键，笛卡尔积或大数据量 JOIN",
        "detect": lambda q: ("JOIN" in q.get("query_text", "").upper()
                            and "CROSS JOIN" in q.get("query_text", "").upper()),
        "severity": "CRITICAL",
        "fix": "避免 CROSS JOIN，确保 JOIN 条件使用正确的键，考虑预 JOIN 的宽表",
        "savings_estimate": "90-99%",
    },
    {
        "id": "R005",
        "name": "复杂子查询",
        "description": "多层嵌套子查询可优化为 CTE/WITH",
        "detect": lambda q: q.get("query_text", "").count("(SELECT") >= 3,
        "severity": "MEDIUM",
        "fix": "使用 WITH (CTE) 重写复杂子查询，提高可读性和执行效率",
        "savings_estimate": "10-50%",
    },
    {
        "id": "R006",
        "name": "小查询开销",
        "description": "大量小查询但数据量小，固定开销占比高",
        "detect": lambda q: q.get("bytes_processed", 0) < 10 * 1024 * 1024,  # < 10MB
        "severity": "LOW",
        "fix": "合并小查询为批量查询，或调整最小计费单位",
        "savings_estimate": "20-40%",
    },
    {
        "id": "R007",
        "name": "数据倾斜检测",
        "description": "某用户/团队的查询消耗远超平均值",
        "severity": "HIGH",
        "fix": "审查高消耗查询，设置配额限制，优化数据模型",
        "savings_estimate": "30-70%",
    },
    {
        "id": "R008",
        "name": "缺少 LIMIT",
        "description": "查询未指定 LIMIT，可能返回大量数据",
        "detect": lambda q: ("SELECT" in q.get("query_text", "").upper()
                            and "LIMIT" not in q.get("query_text", "").upper()
                            and q.get("bytes_processed", 0) > 100 * 1024 * 1024 * 1024),
        "severity": "MEDIUM",
        "fix": "添加 LIMIT 子句，或使用 TABLESAMPLE 抽样",
        "savings_estimate": "10-30%",
    },
]


def parse_args():
    parser = argparse.ArgumentParser(description="成本优化分析器")
    parser.add_argument("--query-log", type=str, required=True,
                        help="查询日志文件 (JSON)")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=["bigquery", "snowflake", "redshift", "starrocks", "clickhouse", "databricks"])
    parser.add_argument("--billing-data", type=str, default=None,
                        help="账单数据 (CSV)")
    parser.add_argument("--output", type=str, default="optimization_report/")
    parser.add_argument("--top-n", type=int, default=20,
                        help="分析 Top N 高成本查询")
    return parser.parse_args()


def load_query_log(file_path: str) -> list:
    """加载查询日志."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "queries" in data:
        return data["queries"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("查询日志格式错误，期望 JSON 数组或含 queries 键的对象")


def load_billing(file_path: str) -> list | None:
    """加载账单数据."""
    if not file_path or not os.path.exists(file_path):
        return None
    import csv
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def analyze_queries(queries: list, platform: str, top_n: int) -> dict:
    """分析查询并生成优化建议."""
    # 按字节处理量排序
    sorted_queries = sorted(
        queries,
        key=lambda q: q.get("bytes_processed", 0) or q.get("cost", 0) or 0,
        reverse=True,
    )
    top_queries = sorted_queries[:top_n]

    # 统计信息
    total_bytes = sum(q.get("bytes_processed", 0) or 0 for q in queries)
    total_queries = len(queries)
    avg_bytes = total_bytes / max(total_queries, 1)

    # 检测重复查询
    query_hashes = defaultdict(list)
    for q in queries:
        h = hash(q.get("query_text", "")[:200])
        query_hashes[h].append(q)

    repeated = set()
    for h, qs in query_hashes.items():
        if len(qs) > 5:
            repeated.add(h)

    patterns = {"repeated": repeated}

    # 应用优化规则
    findings = []
    for q in top_queries:
        for rule in OPTIMIZATION_RULES:
            if "detect" not in rule:
                continue
            try:
                if callable(rule["detect"]):
                    # 检查签名
                    import inspect
                    sig = inspect.signature(rule["detect"])
                    if len(sig.parameters) > 1:
                        matched = rule["detect"](q, patterns)
                    else:
                        matched = rule["detect"](q)
                    if matched:
                        findings.append({
                            "query": q.get("query_text", "")[:200],
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"],
                            "fix": rule["fix"],
                            "savings_estimate": rule.get("savings_estimate", "N/A"),
                            "bytes_processed": q.get("bytes_processed", 0),
                            "duration_sec": q.get("duration", 0),
                        })
            except Exception:
                continue

    # 按用户/团队统计
    user_stats = defaultdict(lambda: {"queries": 0, "total_bytes": 0, "total_cost": 0})
    for q in queries:
        user = q.get("user", q.get("user_email", "unknown"))
        user_stats[user]["queries"] += 1
        user_stats[user]["total_bytes"] += q.get("bytes_processed", 0) or 0
        user_stats[user]["total_cost"] += q.get("cost", 0) or 0

    # 识别数据倾斜
    skew_findings = []
    avg_per_user = total_bytes / max(len(user_stats), 1)
    for user, stats in user_stats.items():
        if stats["total_bytes"] > avg_per_user * 3:
            skew_findings.append({
                "user": user,
                "total_bytes": stats["total_bytes"],
                "avg_multiple": round(stats["total_bytes"] / max(avg_per_user, 1), 1),
                "queries": stats["queries"],
            })

    # 按表统计
    table_stats = defaultdict(lambda: {"bytes": 0, "queries": 0, "avg_bytes": 0})
    for q in queries:
        text = q.get("query_text", "")
        tables = extract_tables(text)
        for t in tables:
            table_stats[t]["bytes"] += q.get("bytes_processed", 0) or 0
            table_stats[t]["queries"] += 1
    for t in table_stats:
        table_stats[t]["avg_bytes"] = table_stats[t]["bytes"] / max(table_stats[t]["queries"], 1)

    top_tables = sorted(table_stats.items(), key=lambda x: x[1]["bytes"], reverse=True)[:10]

    return {
        "summary": {
            "total_queries": total_queries,
            "total_bytes_processed": total_bytes,
            "total_bytes_formatted": format_bytes(total_bytes),
            "avg_bytes_per_query": format_bytes(avg_bytes),
            "platform": platform,
        },
        "top_cost_queries": [
            {
                "query": q.get("query_text", "")[:300],
                "bytes_processed": q.get("bytes_processed", 0),
                "bytes_formatted": format_bytes(q.get("bytes_processed", 0) or 0),
                "duration_sec": q.get("duration", 0),
                "user": q.get("user", q.get("user_email", "unknown")),
            }
            for q in top_queries[:10]
        ],
        "findings": findings[:30],
        "skew_findings": skew_findings,
        "top_tables": [
            {"table": t, "bytes": format_bytes(s["bytes"]), "queries": s["queries"]}
            for t, s in top_tables
        ],
        "cost_breakdown": {
            "critical": len([f for f in findings if f["severity"] == "CRITICAL"]),
            "high": len([f for f in findings if f["severity"] == "HIGH"]),
            "medium": len([f for f in findings if f["severity"] == "MEDIUM"]),
            "low": len([f for f in findings if f["severity"] == "LOW"]),
        },
    }


def extract_tables(query_text: str) -> set:
    """从 SQL 中提取表名."""
    import re
    tables = set()
    # 匹配 FROM / JOIN 后的表名
    patterns = [
        r'(?:FROM|JOIN)\s+(?:`?\w+`?\.)?`?(\w+)`?',
        r'(?:FROM|JOIN)\s+`?(\w+\.\w+)`?',
    ]
    for p in patterns:
        for m in re.finditer(p, query_text, re.IGNORECASE):
            tables.add(m.group(1))
    return tables


def format_bytes(b: float) -> str:
    """格式化字节数为可读字符串."""
    if b is None or b == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while b >= 1024 and i < len(units) - 1:
        b /= 1024
        i += 1
    return f"{b:.2f} {units[i]}"


def generate_html_report(analysis: dict, output_dir: str) -> str:
    """生成交互式 HTML 成本优化报告."""
    summary = analysis["summary"]
    findings = analysis["findings"]
    cost_bd = analysis["cost_breakdown"]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据仓库成本优化报告 — {summary['platform']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; color: #1a1a2e; padding: 24px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 28px; margin-bottom: 8px; color: #0f0f23; }}
        .subtitle {{ color: #666; margin-bottom: 24px; font-size: 14px; }}
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .card {{ background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .card .label {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }}
        .card .value {{ font-size: 28px; font-weight: 700; color: #0f0f23; }}
        .card .unit {{ font-size: 14px; font-weight: 400; color: #888; }}
        .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .section h2 {{ font-size: 18px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e8ecf1; }}
        .finding {{ border-left: 4px solid #ddd; padding: 12px 16px; margin-bottom: 12px; background: #fafbfc; border-radius: 0 8px 8px 0; }}
        .finding.CRITICAL {{ border-color: #e74c3c; background: #fef2f2; }}
        .finding.HIGH {{ border-color: #f39c12; background: #fffbeb; }}
        .finding.MEDIUM {{ border-color: #3498db; background: #eff6ff; }}
        .finding.LOW {{ border-color: #95a5a6; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 8px; }}
        .badge.CRITICAL {{ background: #fef2f2; color: #e74c3c; }}
        .badge.HIGH {{ background: #fffbeb; color: #d97706; }}
        .badge.MEDIUM {{ background: #eff6ff; color: #2563eb; }}
        .badge.LOW {{ background: #f3f4f6; color: #6b7280; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e8ecf1; font-size: 13px; }}
        th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        tr:hover td {{ background: #f8fafc; }}
        .chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px; }}
        @media (max-width: 768px) {{ .chart-row {{ grid-template-columns: 1fr; }} }}
        canvas {{ max-height: 300px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据仓库成本优化报告</h1>
        <p class="subtitle">目标平台: {summary['platform']} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="cards">
            <div class="card">
                <div class="label">总查询数</div>
                <div class="value">{summary['total_queries']:,}<span class="unit"> 次</span></div>
            </div>
            <div class="card">
                <div class="label">总数据扫描量</div>
                <div class="value">{summary['total_bytes_formatted']}</div>
            </div>
            <div class="card">
                <div class="label">平均每次查询</div>
                <div class="value">{summary['avg_bytes_per_query']}</div>
            </div>
            <div class="card">
                <div class="label">优化建议</div>
                <div class="value">{len(findings)}<span class="unit"> 项</span></div>
            </div>
        </div>

        <div class="section">
            <h2>📈 问题严重度分布</h2>
            <div class="chart-row">
                <div><canvas id="severityChart"></canvas></div>
                <div>
                    <p style="font-size:14px; color:#666; margin-bottom:8px;">按严重度分组：</p>
                    <p>🔴 CRITICAL: <strong>{cost_bd['critical']}</strong> 项 — 需立即处理</p>
                    <p>🟠 HIGH: <strong>{cost_bd['high']}</strong> 项 — 本周内处理</p>
                    <p>🔵 MEDIUM: <strong>{cost_bd['medium']}</strong> 项 — 本月内优化</p>
                    <p>⚪ LOW: <strong>{cost_bd['low']}</strong> 项 — 可延后</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔍 优化建议清单</h2>
            <table>
                <thead>
                    <tr><th>规则</th><th>严重度</th><th>数据量</th><th>修复建议</th><th>预估节省</th></tr>
                </thead>
                <tbody>
"""
    for f in findings[:20]:
        html += f"""
                    <tr>
                        <td><strong>{f['rule_id']}</strong> {f['rule_name']}</td>
                        <td><span class="badge {f['severity']}">{f['severity']}</span></td>
                        <td>{format_bytes(f.get('bytes_processed', 0))}</td>
                        <td style="font-size:12px;">{f['fix']}</td>
                        <td>{f.get('savings_estimate', 'N/A')}</td>
                    </tr>
"""
    html += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🔥 Top 10 高成本查询</h2>
            <table>
                <thead>
                    <tr><th>#</th><th>查询</th><th>扫描量</th><th>耗时</th><th>用户</th></tr>
                </thead>
                <tbody>
"""
    for i, q in enumerate(analysis["top_cost_queries"], 1):
        text = q["query"][:150].replace("<", "&lt;").replace(">", "&gt;")
        html += f"""
                    <tr>
                        <td>{i}</td>
                        <td style="font-size:12px;max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{text}...</td>
                        <td>{q['bytes_formatted']}</td>
                        <td>{q.get('duration_sec', 'N/A')}s</td>
                        <td>{q['user']}</td>
                    </tr>
"""
    html += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🗄️ Top 10 高消耗表</h2>
            <table>
                <thead>
                    <tr><th>表名</th><th>扫描量</th><th>查询次数</th></tr>
                </thead>
                <tbody>
"""
    for t in analysis["top_tables"]:
        html += f"""
                    <tr><td>{t['table']}</td><td>{t['bytes']}</td><td>{t['queries']}</td></tr>
"""
    html += """
                </tbody>
            </table>
        </div>
    </div>

    <script>
        new Chart(document.getElementById('severityChart'), {
            type: 'doughnut',
            data: {
                labels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                datasets: [{
                    data: [
"""
    html += f"                        {cost_bd['critical']}, {cost_bd['high']}, {cost_bd['medium']}, {cost_bd['low']}"
    html += """
                    ],
                    backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#95a5a6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    </script>
</body>
</html>"""
    return html


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.query_log):
        print(f"❌ 查询日志文件不存在: {args.query_log}")
        sys.exit(1)

    print(f"📂 加载查询日志: {args.query_log}")
    queries = load_query_log(args.query_log)
    print(f"   {len(queries)} 条查询记录")

    print(f"🔍 分析中...")
    analysis = analyze_queries(queries, args.platform, args.top_n)

    # 保存 JSON
    json_file = os.path.join(args.output, "cost_analysis.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # 保存 HTML
    html_file = os.path.join(args.output, "cost_optimization_report.html")
    html = generate_html_report(analysis, args.output)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    summary = analysis["summary"]
    print(f"\n✅ 报告已生成")
    print(f"📄 JSON: {json_file}")
    print(f"🌐 HTML: {html_file}")
    print(f"\n📊 摘要:")
    print(f"   总查询数: {summary['total_queries']:,}")
    print(f"   总扫描量: {summary['total_bytes_formatted']}")
    print(f"   优化建议: {len(analysis['findings'])} 项")
    print(f"   CRITICAL: {analysis['cost_breakdown']['critical']}")
    print(f"   HIGH: {analysis['cost_breakdown']['high']}")
    print(f"   MEDIUM: {analysis['cost_breakdown']['medium']}")


if __name__ == "__main__":
    main()
