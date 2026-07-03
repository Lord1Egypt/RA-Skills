#!/usr/bin/env python3
"""
电商商品兴趣度分析 HTML 报告生成器
- 读取分析结果 JSON
- 生成交互式可视化 HTML 报告
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def color_for_score(score: float) -> str:
    """根据分数返回颜色"""
    if score >= 70:
        return "#22c55e"  # green
    elif score >= 40:
        return "#f59e0b"  # amber
    else:
        return "#ef4444"  # red


def level_label_cn(level: str) -> str:
    return {"high": "高兴趣", "medium": "中等兴趣", "low": "低兴趣"}.get(level, level)


def issue_label_cn(issue: str) -> str:
    return {
        "price": "💰 价格问题",
        "copy": "📝 文案问题",
        "both": "🔧 综合问题",
        "none": "✅ 表现优秀",
    }.get(issue, issue)


def priority_label_cn(p: str) -> str:
    return {
        "price_first": "优先调整价格",
        "copy_first": "优先优化文案",
        "both": "价格+文案同步优化",
        "none": "无需操作",
    }.get(p, p)


def generate_radar_chart_data(product: Dict) -> str:
    """生成雷达图 JS 数据"""
    scores = product["sub_scores"]
    labels = ["浏览", "停留时长", "详情页", "浏览深度", "点赞", "评论", "分享", "加购", "收藏", "复访"]
    keys = ["view", "duration", "detail", "scroll", "like", "comment", "share", "cart", "favorite", "revisit"]
    values = [scores.get(k, 0) for k in keys]
    return json.dumps({"labels": labels, "values": values})


def generate_html(results: Dict, title: str = "电商商品兴趣度分析报告") -> str:
    """生成完整 HTML 报告"""
    products = results["products"]
    summary = results["summary"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 产品卡片 HTML
    product_cards = []
    for idx, p in enumerate(products):
        score = p["interest_score"]
        color = color_for_score(score)
        d = p["diagnosis"]
        c = p["copy_analysis"]
        radar_data = generate_radar_chart_data(p)

        # 置信度条颜色
        conf_color = color_for_score(d["confidence"] * 100)

        # 文案建议列表
        copy_tips = "".join(f'<li>{s}</li>' for s in c["suggestions"]) if c["suggestions"] else "<li>文案基本OK</li>"

        # 诊断发现列表
        findings_items = "".join(f'<li>{f}</li>' for f in d["detailed_findings"])

        card = f"""
        <div class="product-card" id="product-{idx}">
            <div class="product-header">
                <div class="product-rank">#{idx + 1}</div>
                <div class="product-info">
                    <h3>{p['product_name']}</h3>
                    <span class="product-meta">
                        价格: ¥{p['product_price']:.2f} | 
                        品类: {p.get('category', '通用')} | 
                        样本: {p['total_users']}人
                    </span>
                </div>
                <div class="interest-badge" style="background: {color}">
                    <span class="score-num">{score:.0f}</span>
                    <span class="score-label">兴趣分</span>
                </div>
            </div>

            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-value" style="color: {color}">{score:.1f}</div>
                    <div class="metric-label">兴趣度 ({level_label_cn(p['interest_level'])})</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color: #3b82f6">{p['conversion_rate']:.1f}%</div>
                    <div class="metric-label">转化率</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color: #8b5cf6">{c['word_count']}</div>
                    <div class="metric-label">文案字数</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color: {conf_color}">{d['confidence'] * 100:.0f}%</div>
                    <div class="metric-label">置信度</div>
                </div>
            </div>

            <div class="diagnosis-section">
                <div class="issue-tag issue-{d['primary_issue']}">
                    {issue_label_cn(d['primary_issue'])}
                </div>
                <div class="action-tag">
                    行动建议: {priority_label_cn(d['action_priority'])}
                </div>
            </div>

            <div class="analysis-grid">
                <div class="analysis-col">
                    <h4>📊 兴趣度雷达图</h4>
                    <canvas id="radar-{idx}" width="280" height="280"></canvas>
                    <script>
                        new Chart(document.getElementById('radar-{idx}').getContext('2d'), {{
                            type: 'radar',
                            data: {{
                                labels: {json.dumps(json.loads(radar_data)['labels'])},
                                datasets: [{{
                                    label: '{p['product_name']}',
                                    data: {json.dumps(json.loads(radar_data)['values'])},
                                    backgroundColor: '{color}33',
                                    borderColor: '{color}',
                                    borderWidth: 2,
                                    pointBackgroundColor: '{color}',
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                scales: {{ r: {{ min: 0, max: 100, ticks: {{ stepSize: 25 }} }} }},
                                plugins: {{ legend: {{ display: false }} }}
                            }}
                        }});
                    </script>
                </div>
                <div class="analysis-col">
                    <h4>💰 价格诊断</h4>
                    <p>{d['price_suggestion']}</p>

                    <h4 style="margin-top: 12px;">📝 文案诊断</h4>
                    <p>{d['copy_suggestion']}</p>

                    <h4 style="margin-top: 12px;">🔍 文案指标</h4>
                    <div class="copy-metrics">
                        <span class="copy-tag {'good' if c['has_cta'] else 'bad'}">
                            {'✅ 有CTA' if c['has_cta'] else '❌ 无CTA'}
                        </span>
                        <span class="copy-tag {'good' if c['has_selling_point'] else 'bad'}">
                            {'✅ 有卖点' if c['has_selling_point'] else '❌ 缺卖点'}
                        </span>
                        <span class="copy-tag {'good' if c['sentiment_score'] > 0.1 else 'bad'}">
                            情感: {c['sentiment_score']:.2f}
                        </span>
                        <span class="copy-tag {'good' if c['readability_score'] >= 60 else 'bad'}">
                            可读性: {c['readability_score']:.0f}
                        </span>
                    </div>

                    <h4 style="margin-top: 12px;">💡 优化建议</h4>
                    <ul class="suggestions-list">{copy_tips}</ul>
                </div>
            </div>

            <details class="findings-details">
                <summary>📋 详细诊断发现 ({len(d['detailed_findings'])}条)</summary>
                <ul class="findings-list">{findings_items}</ul>
            </details>
        </div>
        """
        product_cards.append(card)

    # 汇总统计
    summary_stats = f"""
    <div class="summary-grid">
        <div class="summary-card total">
            <div class="summary-num">{summary['total_products']}</div>
            <div class="summary-label">分析商品数</div>
        </div>
        <div class="summary-card price">
            <div class="summary-num">{summary['price_issues']}</div>
            <div class="summary-label">价格问题</div>
        </div>
        <div class="summary-card copy">
            <div class="summary-num">{summary['copy_issues']}</div>
            <div class="summary-label">文案问题</div>
        </div>
        <div class="summary-card both">
            <div class="summary-num">{summary['both_issues']}</div>
            <div class="summary-label">综合问题</div>
        </div>
        <div class="summary-card good">
            <div class="summary-num">{summary['no_issues']}</div>
            <div class="summary-label">表现优秀</div>
        </div>
    </div>
    """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                         "Microsoft YaHei", sans-serif;
            background: #f5f7fa; color: #1a1a2e; line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

        /* Header */
        .report-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 32px 40px; border-radius: 16px;
            margin-bottom: 24px; text-align: center;
        }}
        .report-header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .report-header .timestamp {{ opacity: 0.8; font-size: 14px; }}

        /* Summary */
        .summary-grid {{
            display: grid; grid-template-columns: repeat(5, 1fr);
            gap: 16px; margin-bottom: 24px;
        }}
        .summary-card {{
            background: white; border-radius: 12px; padding: 20px;
            text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-top: 4px solid #e5e7eb;
        }}
        .summary-card.total {{ border-top-color: #667eea; }}
        .summary-card.price {{ border-top-color: #f59e0b; }}
        .summary-card.copy {{ border-top-color: #3b82f6; }}
        .summary-card.both {{ border-top-color: #ef4444; }}
        .summary-card.good {{ border-top-color: #22c55e; }}
        .summary-num {{ font-size: 36px; font-weight: 700; color: #1a1a2e; }}
        .summary-label {{ font-size: 13px; color: #6b7280; margin-top: 4px; }}

        /* Product Card */
        .product-card {{
            background: white; border-radius: 16px; padding: 24px;
            margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .product-header {{
            display: flex; align-items: center; gap: 16px;
            margin-bottom: 16px; padding-bottom: 16px;
            border-bottom: 1px solid #f3f4f6;
        }}
        .product-rank {{
            width: 40px; height: 40px; border-radius: 10px;
            background: #f3f4f6; display: flex; align-items: center;
            justify-content: center; font-weight: 700; font-size: 16px;
            color: #6b7280; flex-shrink: 0;
        }}
        .product-info {{ flex: 1; }}
        .product-info h3 {{ font-size: 18px; margin-bottom: 4px; }}
        .product-meta {{ font-size: 13px; color: #6b7280; }}
        .interest-badge {{
            width: 72px; height: 72px; border-radius: 50%;
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; color: white; flex-shrink: 0;
        }}
        .score-num {{ font-size: 24px; font-weight: 800; line-height: 1; }}
        .score-label {{ font-size: 11px; opacity: 0.9; }}

        /* Metrics */
        .metrics-row {{
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 12px; margin-bottom: 16px;
        }}
        .metric-box {{
            background: #f9fafb; border-radius: 10px;
            padding: 12px; text-align: center;
        }}
        .metric-value {{ font-size: 22px; font-weight: 700; }}
        .metric-label {{ font-size: 12px; color: #6b7280; margin-top: 2px; }}

        /* Diagnosis */
        .diagnosis-section {{
            display: flex; gap: 10px; margin-bottom: 16px;
        }}
        .issue-tag, .action-tag {{
            padding: 6px 14px; border-radius: 20px;
            font-size: 13px; font-weight: 600;
        }}
        .issue-tag {{ color: white; }}
        .issue-price {{ background: #f59e0b; }}
        .issue-copy {{ background: #3b82f6; }}
        .issue-both {{ background: #ef4444; }}
        .issue-none {{ background: #22c55e; }}
        .action-tag {{
            background: #f3f4f6; color: #374151;
        }}

        /* Analysis Grid */
        .analysis-grid {{
            display: grid; grid-template-columns: 300px 1fr;
            gap: 24px; margin-top: 16px;
        }}
        .analysis-col h4 {{
            font-size: 14px; color: #374151; margin-bottom: 8px;
        }}
        .analysis-col p {{
            font-size: 14px; color: #4b5563; margin-bottom: 8px;
        }}
        .copy-metrics {{
            display: flex; flex-wrap: wrap; gap: 6px;
        }}
        .copy-tag {{
            padding: 3px 10px; border-radius: 12px;
            font-size: 12px; font-weight: 500;
        }}
        .copy-tag.good {{ background: #dcfce7; color: #166534; }}
        .copy-tag.bad {{ background: #fee2e2; color: #991b1b; }}

        .suggestions-list {{
            list-style: none; padding: 0;
        }}
        .suggestions-list li {{
            padding: 6px 0; font-size: 13px; color: #4b5563;
            border-bottom: 1px solid #f3f4f6;
        }}
        .suggestions-list li::before {{
            content: "▸ "; color: #667eea; font-weight: bold;
        }}

        .findings-details {{
            margin-top: 16px; padding-top: 16px;
            border-top: 1px solid #f3f4f6;
        }}
        .findings-details summary {{
            cursor: pointer; font-weight: 600; font-size: 14px;
            color: #667eea;
        }}
        .findings-list {{
            margin-top: 8px; padding-left: 20px;
        }}
        .findings-list li {{
            font-size: 13px; color: #4b5563; padding: 3px 0;
        }}

        /* Footer */
        .report-footer {{
            text-align: center; padding: 24px; color: #9ca3af;
            font-size: 12px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .summary-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .metrics-row {{ grid-template-columns: repeat(2, 1fr); }}
            .analysis-grid {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 480px) {{
            .summary-grid {{ grid-template-columns: 1fr; }}
            .product-header {{ flex-direction: column; text-align: center; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="report-header">
            <h1>🛍️ {title}</h1>
            <p class="timestamp">生成时间: {now} | 分析引擎 v1.0</p>
        </div>

        {summary_stats}

        {"".join(product_cards)}

        <div class="report-footer">
            <p>📊 电商商品兴趣度分析报告 | 基于多维度行为数据 + NLP文案分析</p>
            <p>算法版本: 加权兴趣度模型 v1.0 | 诊断矩阵: 3×3 兴趣-转化交叉分析</p>
        </div>
    </div>
</body>
</html>"""

    return html


# ============================================================
# CLI入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="电商兴趣度分析 HTML 报告生成器")
    parser.add_argument("--data", "-d", required=True,
                        help="分析结果 JSON 文件路径")
    parser.add_argument("--output", "-o", default="interest_report.html",
                        help="输出 HTML 报告路径 (默认: interest_report.html)")
    parser.add_argument("--title", "-t", default="电商商品兴趣度分析报告",
                        help="报告标题")
    args = parser.parse_args()

    # 加载分析结果
    with open(args.data, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # 生成报告
    html = generate_html(results, args.title)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML 报告已生成: {args.output}")
