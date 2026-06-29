#!/usr/bin/env python3
"""
SLA 监控仪表板生成器 — SLA Monitor
基于管道运行历史和 SLA 配置，生成交互式 HTML 监控仪表板。
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_args():
    parser = argparse.ArgumentParser(description="SLA 监控仪表板生成器")
    parser.add_argument("--config", type=str, default=None,
                        help="SLA 配置文件 (YAML)")
    parser.add_argument("--pipeline-runs", type=str, required=True,
                        help="管道运行历史数据 (CSV)")
    parser.add_argument("--output", type=str, default="sla_dashboard/",
                        help="输出目录")
    parser.add_argument("--days", type=int, default=30,
                        help="分析数据范围（天）")
    return parser.parse_args()


DEFAULT_SLA_CONFIG = {
    "sla_tiers": {
        "tier_1_critical": {
            "name": "Tier 1 — 核心管道",
            "freshness_hours": 4,
            "uptime_pct": 99.9,
            "max_failure_rate_pct": 1.0,
            "notification_channels": ["pagerduty", "slack"],
            "description": "直接影响核心业务指标的管道",
        },
        "tier_2_important": {
            "name": "Tier 2 — 重要管道",
            "freshness_hours": 8,
            "uptime_pct": 99.5,
            "max_failure_rate_pct": 3.0,
            "notification_channels": ["slack", "email"],
            "description": "影响内部报表和分析的管道",
        },
        "tier_3_normal": {
            "name": "Tier 3 — 常规管道",
            "freshness_hours": 24,
            "uptime_pct": 99.0,
            "max_failure_rate_pct": 5.0,
            "notification_channels": ["email"],
            "description": "非关键数据管道",
        },
    },
    "alert_rules": {
        "freshness_violation": "数据新鲜度超过 SLA 阈值",
        "failure_rate_spike": "失败率较前 7 天均值上升 > 200%",
        "volume_anomaly": "数据量变化超过 50%",
        "consecutive_failures": "连续失败超过 3 次",
    },
}


def load_config(file_path: str | None) -> dict:
    """加载 SLA 配置."""
    if file_path and os.path.exists(file_path):
        if not HAS_YAML:
            print("⚠️  PyYAML 未安装，使用默认配置")
            return DEFAULT_SLA_CONFIG
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or DEFAULT_SLA_CONFIG
    return DEFAULT_SLA_CONFIG


def load_pipeline_runs(file_path: str) -> list:
    """加载管道运行历史."""
    runs = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            runs.append(row)
    return runs


def analyze_pipeline_runs(runs: list, config: dict, days: int) -> dict:
    """分析管道运行数据."""
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    # 按管道分组
    pipeline_stats = defaultdict(lambda: {
        "runs": [],
        "total": 0,
        "success": 0,
        "failed": 0,
        "running": 0,
        "durations": [],
        "latest_run": None,
        "daily_runs": defaultdict(int),
    })

    for run in runs:
        pipeline = run.get("pipeline_name", run.get("dag_id", "unknown"))
        status = run.get("status", run.get("state", "unknown")).lower()
        start_time_str = run.get("start_time", run.get("execution_date", ""))
        duration_str = run.get("duration_sec", run.get("duration", 0))

        try:
            duration = float(duration_str)
        except (ValueError, TypeError):
            duration = 0

        stats = pipeline_stats[pipeline]
        stats["total"] += 1

        if status in ("success", "succeeded", "completed"):
            stats["success"] += 1
            stats["durations"].append(duration)
        elif status in ("failed", "error", "failure"):
            stats["failed"] += 1
        elif status in ("running", "queued"):
            stats["running"] += 1

        # 解析时间
        try:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    start_dt = datetime.strptime(start_time_str[:19], fmt)
                    break
                except ValueError:
                    continue
            else:
                start_dt = None
        except Exception:
            start_dt = None

        if start_dt and start_dt >= cutoff:
            stats["daily_runs"][start_dt.strftime("%Y-%m-%d")] += 1
            if stats["latest_run"] is None or start_dt > stats["latest_run"]:
                stats["latest_run"] = start_dt

    # 计算每管道 SLA 指标
    sla_results = {}
    for pipeline, stats in pipeline_stats.items():
        if stats["total"] == 0:
            continue

        success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
        failure_rate = (stats["failed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        avg_duration = sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else 0

        # 判断满足哪个 SLA 级别
        sla_level = "tier_3_normal"
        tiers = config.get("sla_tiers", DEFAULT_SLA_CONFIG["sla_tiers"])
        if success_rate >= tiers.get("tier_1_critical", {}).get("uptime_pct", 99.9):
            sla_level = "tier_1_critical"
        elif success_rate >= tiers.get("tier_2_important", {}).get("uptime_pct", 99.5):
            sla_level = "tier_2_important"

        # 检测异常
        alerts = detect_anomalies(pipeline, stats, config, days)

        sla_results[pipeline] = {
            "total_runs": stats["total"],
            "success": stats["success"],
            "failed": stats["failed"],
            "success_rate": round(success_rate, 2),
            "failure_rate": round(failure_rate, 2),
            "avg_duration_sec": round(avg_duration, 1),
            "latest_run": stats["latest_run"].isoformat() if stats["latest_run"] else None,
            "sla_level": sla_level,
            "sla_status": "COMPLIANT" if success_rate >= tiers.get(sla_level, {}).get("uptime_pct", 99) else "VIOLATED",
            "alerts": alerts,
        }

    # 全局统计
    global_stats = {
        "total_pipelines": len(sla_results),
        "compiant_pipelines": sum(1 for p in sla_results.values() if p["sla_status"] == "COMPLIANT"),
        "violated_pipelines": sum(1 for p in sla_results.values() if p["sla_status"] == "VIOLATED"),
        "total_runs": sum(p["total_runs"] for p in sla_results.values()),
        "total_failures": sum(p["failed"] for p in sla_results.values()),
        "overall_success_rate": round(
            sum(p["success"] for p in sla_results.values()) /
            max(sum(p["total_runs"] for p in sla_results.values()), 1) * 100, 2
        ),
        "total_alerts": sum(len(p["alerts"]) for p in sla_results.values()),
    }

    return {
        "global": global_stats,
        "pipelines": sla_results,
        "config": config,
        "analysis_period_days": days,
        "generated_at": datetime.now().isoformat(),
    }


def detect_anomalies(pipeline: str, stats: dict, config: dict, days: int) -> list:
    """检测异常."""
    alerts = []

    tiers = config.get("sla_tiers", DEFAULT_SLA_CONFIG["sla_tiers"])
    tier = tiers.get("tier_2_important", {})

    # 失败率过高
    failure_rate = (stats["failed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    if failure_rate > tier.get("max_failure_rate_pct", 3.0):
        alerts.append({
            "type": "high_failure_rate",
            "severity": "CRITICAL" if failure_rate > 10 else "HIGH",
            "message": f"失败率 {failure_rate:.1f}% 超过阈值 {tier.get('max_failure_rate_pct', 3.0)}%",
            "metric": f"{failure_rate:.1f}%",
            "threshold": f"{tier.get('max_failure_rate_pct', 3.0)}%",
        })

    # 数据新鲜度
    if stats["latest_run"]:
        hours_since = (datetime.now() - stats["latest_run"]).total_seconds() / 3600
        freshness_threshold = tier.get("freshness_hours", 8)
        if hours_since > freshness_threshold:
            alerts.append({
                "type": "freshness_violation",
                "severity": "HIGH" if hours_since > freshness_threshold * 2 else "MEDIUM",
                "message": f"最后一次成功运行在 {hours_since:.1f} 小时前，超过 SLA {freshness_threshold}h",
                "metric": f"{hours_since:.1f}h",
                "threshold": f"{freshness_threshold}h",
            })

    # 平均时长异常
    if stats["durations"] and len(stats["durations"]) > 5:
        avg = sum(stats["durations"]) / len(stats["durations"])
        recent_avg = sum(stats["durations"][-5:]) / min(len(stats["durations"]), 5)
        if avg > 0 and recent_avg > avg * 2:
            alerts.append({
                "type": "duration_spike",
                "severity": "MEDIUM",
                "message": f"最近运行时长 {recent_avg:.0f}s 远超平均值 {avg:.0f}s",
                "metric": f"{recent_avg:.0f}s",
                "threshold": f"{avg:.0f}s (avg)",
            })

    return alerts


def generate_html_dashboard(analysis: dict) -> str:
    """生成交互式 HTML SLA 监控仪表板."""
    g = analysis["global"]
    pipelines = analysis["pipelines"]

    # 管道数据 JSON
    pipe_names = list(pipelines.keys())
    pipe_json = json.dumps([
        {
            "name": name,
            "success_rate": p["success_rate"],
            "failure_rate": p["failure_rate"],
            "total_runs": p["total_runs"],
            "sla_level": p["sla_level"],
            "sla_status": p["sla_status"],
            "alerts": len(p["alerts"]),
        }
        for name, p in pipelines.items()
    ], ensure_ascii=False)

    # 按 tier 分类
    tier_counts = defaultdict(int)
    for p in pipelines.values():
        tier_counts[p["sla_level"]] += 1

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SLA 监控仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; padding: 24px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ font-size: 28px; color: #0f0f23; margin-bottom: 4px; }}
        .subtitle {{ color: #666; font-size: 13px; margin-bottom: 24px; }}
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px; }}
        .card {{ background: #fff; border-radius: 10px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .card .lbl {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }}
        .card .val {{ font-size: 26px; font-weight: 700; }}
        .card.green .val {{ color: #059669; }}
        .card.red .val {{ color: #dc2626; }}
        .card.amber .val {{ color: #d97706; }}
        .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .section h2 {{ font-size: 18px; margin-bottom: 16px; border-bottom: 2px solid #e8ecf1; padding-bottom: 8px; }}
        .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        @media (max-width: 768px) {{ .charts {{ grid-template-columns: 1fr; }} }}
        canvas {{ max-height: 300px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 10px 12px; border-bottom: 1px solid #e8ecf1; text-align: left; }}
        th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        .badge.pass {{ background: #ecfdf5; color: #059669; }}
        .badge.fail {{ background: #fef2f2; color: #dc2626; }}
        .badge.t1 {{ background: #ede9fe; color: #7c3aed; }}
        .badge.t2 {{ background: #dbeafe; color: #2563eb; }}
        .badge.t3 {{ background: #f3f4f6; color: #6b7280; }}
        tr:hover td {{ background: #f8fafc; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 数据管道 SLA 监控仪表板</h1>
        <p class="subtitle">分析周期: 最近 {analysis['analysis_period_days']} 天 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="cards">
            <div class="card green">
                <div class="lbl">管道总数</div>
                <div class="val">{g['total_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> 个</span></div>
            </div>
            <div class="card green">
                <div class="lbl">总体成功率</div>
                <div class="val">{g['overall_success_rate']}<span style="font-size:14px;font-weight:400;color:#666;">%</span></div>
            </div>
            <div class="card green">
                <div class="lbl">SLA 合规</div>
                <div class="val">{g['compiant_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> / {g['total_pipelines']}</span></div>
            </div>
            <div class="card {'red' if g['violated_pipelines'] > 0 else 'green'}">
                <div class="lbl">SLA 违规</div>
                <div class="val">{g['violated_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> 个</span></div>
            </div>
            <div class="card {'amber' if g['total_alerts'] > 0 else 'green'}">
                <div class="lbl">活跃告警</div>
                <div class="val">{g['total_alerts']}<span style="font-size:14px;font-weight:400;color:#666;"> 条</span></div>
            </div>
            <div class="card">
                <div class="lbl">总运行次数</div>
                <div class="val">{g['total_runs']:,}</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 管道成功率分布</h2>
            <div class="charts">
                <div><canvas id="successChart"></canvas></div>
                <div><canvas id="tierChart"></canvas></div>
            </div>
        </div>

        <div class="section">
            <h2>📋 管道 SLA 明细</h2>
            <table id="pipelineTable">
                <thead>
                    <tr>
                        <th>管道名称</th>
                        <th>SLA 级别</th>
                        <th>成功率</th>
                        <th>失败率</th>
                        <th>总运行</th>
                        <th>SLA 状态</th>
                        <th>告警</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <script>
        const pipes = {pipe_json};

        // 填充表格
        const tb = document.querySelector('#pipelineTable tbody');
        pipes.forEach(p => {{
            const statusClass = p.sla_status === 'COMPLIANT' ? 'pass' : 'fail';
            const tierClass = p.sla_level === 'tier_1_critical' ? 't1' : p.sla_level === 'tier_2_important' ? 't2' : 't3';
            const tierLabel = p.sla_level === 'tier_1_critical' ? 'T1 核心' : p.sla_level === 'tier_2_important' ? 'T2 重要' : 'T3 常规';
            const alertCell = p.alerts > 0 ? `<span style="color:#dc2626;font-weight:600;">${{p.alerts}}</span>` : '0';
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${{p.name}}</strong></td>
                <td><span class="badge ${{tierClass}}">${{tierLabel}}</span></td>
                <td>${{p.success_rate}}%</td>
                <td style="color:${{p.failure_rate > 5 ? '#dc2626' : '#666'}}">${{p.failure_rate}}%</td>
                <td>${{p.total_runs}}</td>
                <td><span class="badge ${{statusClass}}">${{p.sla_status === 'COMPLIANT' ? '✅ COMPLIANT' : '❌ VIOLATED'}}</span></td>
                <td>${{alertCell}}</td>
            `;
            tb.appendChild(tr);
        }});

        // 成功率图表
        new Chart(document.getElementById('successChart'), {{
            type: 'bar',
            data: {{
                labels: pipes.map(p => p.name),
                datasets: [{{
                    label: '成功率 (%)',
                    data: pipes.map(p => p.success_rate),
                    backgroundColor: pipes.map(p => p.success_rate >= 99 ? '#059669' : p.success_rate >= 95 ? '#d97706' : '#dc2626'),
                    borderRadius: 4,
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{ y: {{ min: 80, max: 100 }} }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});

        // Tier 分布
        const tierCounts = {{
            tier_1_critical: {tier_counts.get('tier_1_critical', 0)},
            tier_2_important: {tier_counts.get('tier_2_important', 0)},
            tier_3_normal: {tier_counts.get('tier_3_normal', 0)},
        }};
        new Chart(document.getElementById('tierChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['T1 核心', 'T2 重要', 'T3 常规'],
                datasets: [{{
                    data: [tierCounts.tier_1_critical, tierCounts.tier_2_important, tierCounts.tier_3_normal],
                    backgroundColor: ['#7c3aed', '#2563eb', '#6b7280'],
                    borderWidth: 0,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ position: 'bottom' }} }}
            }}
        }});
    </script>
</body>
</html>"""
    return html


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.pipeline_runs):
        print(f"❌ 管道运行数据不存在: {args.pipeline_runs}")
        sys.exit(1)

    config = load_config(args.config)
    runs = load_pipeline_runs(args.pipeline_runs)

    print(f"📂 加载 {len(runs)} 条管道运行记录")
    print(f"📅 分析范围: 最近 {args.days} 天")

    analysis = analyze_pipeline_runs(runs, config, args.days)

    # 保存 JSON
    json_file = os.path.join(args.output, "sla_analysis.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # 保存 HTML 仪表板
    html_file = os.path.join(args.output, "sla_dashboard.html")
    html = generate_html_dashboard(analysis)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    g = analysis["global"]
    print(f"\n✅ SLA 监控仪表板已生成")
    print(f"📄 JSON: {json_file}")
    print(f"🌐 HTML: {html_file}")
    print(f"\n📊 摘要:")
    print(f"   管道总数: {g['total_pipelines']}")
    print(f"   总体成功率: {g['overall_success_rate']}%")
    print(f"   SLA 合规: {g['compiant_pipelines']}/{g['total_pipelines']}")
    print(f"   SLA 违规: {g['violated_pipelines']}")
    print(f"   活跃告警: {g['total_alerts']}")


if __name__ == "__main__":
    main()
