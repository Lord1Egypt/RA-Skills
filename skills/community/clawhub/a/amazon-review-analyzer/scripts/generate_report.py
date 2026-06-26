#!/usr/bin/env python3
"""
报告生成模块
生成交互式HTML报告
"""

import json
from typing import Dict, List
from datetime import datetime


def generate_html_report(
    product_info: Dict,
    tagged_reviews: List[Dict],
    output_path: str,
    debug: bool = False
):
    """
    生成交互式HTML报告
    
    Args:
        product_info: 产品信息 {"title", "price", "rating", "total_reviews", "image_url", "url"}
        tagged_reviews: 带打标结果的评论列表 [{"review": {...}, "tags": {...}}, ...]
        output_path: 输出HTML文件路径
        debug: 是否打印调试信息
    """
    
    if debug:
        print(f"正在生成HTML报告: {output_path}")
    
    # 1. 汇总分析
    summary = _analyze_tagged_reviews(tagged_reviews)
    
    if debug:
        print(f"  评论总数: {summary['total_reviews']}")
        print(f"  情感分布: {summary['sentiment_dist']}")
        print(f"  高频痛点: {len(summary['top_pain_points'])} 个")
        print(f"  高频卖点: {len(summary['top_selling_points'])} 个")
    
    # 2. 生成HTML
    html_content = _build_html_report(product_info, summary, tagged_reviews)
    
    # 3. 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ 报告已生成: {output_path}")
    
    return output_path


def _analyze_tagged_reviews(tagged_reviews: List[Dict]) -> Dict:
    """汇总分析所有打标结果"""
    
    total = len(tagged_reviews)
    
    # 情感分布
    sentiment_dist = {"positive": 0, "negative": 0, "neutral": 0}
    for item in tagged_reviews:
        sentiment = item["tags"].get("sentiment", "neutral")
        if sentiment in sentiment_dist:
            sentiment_dist[sentiment] += 1
    
    # 评分分布
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for item in tagged_reviews:
        rating = item["review"].get("rating", 0)
        if rating in rating_dist:
            rating_dist[rating] += 1
    
    # 高频痛点
    pain_point_counts = {}
    for item in tagged_reviews:
        for point in item["tags"].get("pain_points", []):
            pain_point_counts[point] = pain_point_counts.get(point, 0) + 1
    
    top_pain_points = sorted(pain_point_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 高频卖点
    selling_point_counts = {}
    for item in tagged_reviews:
        for point in item["tags"].get("selling_points", []):
            selling_point_counts[point] = selling_point_counts.get(point, 0) + 1
    
    top_selling_points = sorted(selling_point_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 使用场景
    use_case_counts = {}
    for item in tagged_reviews:
        for case in item["tags"].get("use_cases", []):
            use_case_counts[case] = use_case_counts.get(case, 0) + 1
    
    top_use_cases = sorted(use_case_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # 用户画像（去重）
    user_profiles = list(set([item["tags"].get("user_profile", "") for item in tagged_reviews if item["tags"].get("user_profile", "")]))
    
    # Listing优化建议（基于痛点反向推导）
    listing_suggestions = []
    for point, count in top_pain_points[:5]:
        suggestion = f"在Listing中主动说明如何解决'{point}'问题"
        listing_suggestions.append(suggestion)
    
    return {
        "total_reviews": total,
        "sentiment_dist": sentiment_dist,
        "rating_dist": rating_dist,
        "top_pain_points": top_pain_points,
        "top_selling_points": top_selling_points,
        "top_use_cases": top_use_cases,
        "user_profiles": user_profiles[:5],  # 最多取5个
        "listing_suggestions": listing_suggestions,
        "tagged_reviews": tagged_reviews  # 保留原始数据，用于报告中的详细展示
    }


def _build_html_report(product_info: Dict, summary: Dict, tagged_reviews: List[Dict]) -> str:
    """构建HTML报告内容"""
    
    # 生成唯一ID（用于图表）
    report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 准备图表数据（JSON格式）
    sentiment_data = json.dumps(summary["sentiment_dist"])
    rating_data = json.dumps(summary["rating_dist"])
    pain_points_data = json.dumps([{"name": p[0], "value": p[1]} for p in summary["top_pain_points"]])
    selling_points_data = json.dumps([{"name": p[0], "value": p[1]} for p in summary["top_selling_points"]])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon评论深度分析报告 - {product_info['title'][:50]}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .product-info {{
            display: flex;
            gap: 30px;
            align-items: center;
            margin-top: 20px;
        }}
        
        .product-image {{
            width: 150px;
            height: 150px;
            object-fit: contain;
            background: white;
            border-radius: 8px;
            padding: 10px;
        }}
        
        .product-details {{
            flex: 1;
        }}
        
        .product-details p {{
            margin: 5px 0;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card h3 {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            margin: 20px 0;
        }}
        
        .insight-list {{
            list-style: none;
        }}
        
        .insight-list li {{
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        
        .pain-point {{
            border-left-color: #e74c3c !important;
        }}
        
        .selling-point {{
            border-left-color: #2ecc71 !important;
        }}
        
        .tag {{
            display: inline-block;
            padding: 5px 10px;
            margin: 5px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .pain-tag {{
            background: #e74c3c;
        }}
        
        .selling-tag {{
            background: #2ecc71;
        }}
        
        footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .product-info {{
                flex-direction: column;
                text-align: center;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛍️ Amazon评论深度分析报告</h1>
            <div class="product-info">
                <img src="{product_info.get('image_url', '')}" alt="产品图片" class="product-image" onerror="this.style.display='none'">
                <div class="product-details">
                    <h2>{product_info.get('title', 'Unknown Product')}</h2>
                    <p><strong>ASIN:</strong> {product_info.get('asin', 'N/A')}</p>
                    <p><strong>价格:</strong> {product_info.get('price', 'N/A')}</p>
                    <p><strong>评分:</strong> {'⭐' * int(product_info.get('rating', 0))} ({product_info.get('rating', 0)}/5)</p>
                    <p><strong>评论数:</strong> {product_info.get('total_reviews', 0)}</p>
                    <p><a href="{product_info.get('url', '#')}" style="color: white;" target="_blank">在Amazon查看产品 →</a></p>
                </div>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>{summary['total_reviews']}</h3>
                <p>分析评论数</p>
            </div>
            <div class="stat-card">
                <h3>{summary['sentiment_dist']['positive']}</h3>
                <p>正面评论</p>
            </div>
            <div class="stat-card">
                <h3>{summary['sentiment_dist']['negative']}</h3>
                <p>负面评论</p>
            </div>
            <div class="stat-card">
                <h3>{len(summary['top_pain_points'])}</h3>
                <p>识别痛点数</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 评论概览</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h3>情感分布</h3>
                    <div class="chart-container">
                        <canvas id="sentimentChart"></canvas>
                    </div>
                </div>
                <div>
                    <h3>评分分布</h3>
                    <div class="chart-container">
                        <canvas id="ratingChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔴 痛点分析 (TOP 10)</h2>
            <div class="chart-container">
                <canvas id="painChart"></canvas>
            </div>
            <h3 style="margin-top: 30px;">详细痛点列表</h3>
            <ul class="insight-list">
"""
    
    # 添加痛点列表
    for i, (point, count) in enumerate(summary['top_pain_points'], 1):
        html += f'                <li class="pain-point"><strong>{i}. {point}</strong> <span style="color: #e74c3c;">(提及 {count} 次)</span></li>\n'
    
    html += f"""            </ul>
        </div>
        
        <div class="section">
            <h2>🟢 卖点分析 (TOP 10)</h2>
            <div class="chart-container">
                <canvas id="sellingChart"></canvas>
            </div>
            <h3 style="margin-top: 30px;">详细卖点列表</h3>
            <ul class="insight-list">
"""
    
    # 添加卖点列表
    for i, (point, count) in enumerate(summary['top_selling_points'], 1):
        html += f'                <li class="selling-point"><strong>{i}. {point}</strong> <span style="color: #2ecc71;">(提及 {count} 次)</span></li>\n'
    
    html += f"""            </ul>
        </div>
        
        <div class="section">
            <h2>👤 用户画像 & 使用场景</h2>
            <h3>典型用户画像</h3>
            <div style="margin: 15px 0;">
"""
    
    # 添加用户画像
    for profile in summary['user_profiles']:
        html += f'                <span class="tag">{profile}</span>\n'
    
    html += f"""            </div>
            <h3 style="margin-top: 30px;">主要使用场景</h3>
            <div style="margin: 15px 0;">
"""
    
    # 添加使用场景
    for case, count in summary['top_use_cases']:
        html += f'                <span class="tag selling-tag">{case} ({count}次)</span>\n'
    
    html += f"""            </div>
        </div>
        
        <div class="section">
            <h2>📝 Listing优化建议</h2>
            <ul class="insight-list">
"""
    
    # 添加Listing优化建议
    for i, suggestion in enumerate(summary['listing_suggestions'], 1):
        html += f'                <li><strong>{i}.</strong> {suggestion}</li>\n'
    
    html += f"""            </ul>
            <p style="margin-top: 20px; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                💡 <strong>提示：</strong> 基于用户痛点，建议在Listing中主动解答用户疑虑，将痛点转化为卖点。
            </p>
        </div>
        
        <div class="section">
            <h2>📋 典型评论摘录</h2>
"""
    
    # 添加典型评论（取前5条）
    for i, item in enumerate(tagged_reviews[:5], 1):
        review = item['review']
        tags = item['tags']
        sentiment_color = "#2ecc71" if tags['sentiment'] == 'positive' else "#e74c3c" if tags['sentiment'] == 'negative' else "#f39c12"
        
        html += f"""            <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid {sentiment_color};">
                <p><strong>评分:</strong> {'⭐' * review.get('rating', 0)}</p>
                <p><strong>标题:</strong> {review.get('title', '')}</p>
                <p><strong>内容:</strong> {review.get('body', '')[:200]}...</p>
                <p><strong>AI摘要:</strong> {tags.get('summary', '')}</p>
                <p><strong>痛点:</strong> {', '.join(tags.get('pain_points', [])) if tags.get('pain_points') else '无'}</p>
                <p><strong>卖点:</strong> {', '.join(tags.get('selling_points', [])) if tags.get('selling_points') else '无'}</p>
            </div>
"""
    
    html += """        </div>
    </div>
    
    <footer>
        <p>Generated by Amazon评论深度分析助手 | Powered by AI</p>
        <p style="margin-top: 10px; color: #999; font-size: 0.8em;">本报告基于真实用户评论分析生成，仅供参考</p>
    </footer>
    
    <script>
        // 情感分布图
        new Chart(document.getElementById('sentimentChart'), {
            type: 'pie',
            data: {
                labels: ['正面', '负面', '中性'],
                datasets: [{
                    data: """ + f"[{summary['sentiment_dist']['positive']}, {summary['sentiment_dist']['negative']}, {summary['sentiment_dist']['neutral']}]" + """,
                    backgroundColor: ['#2ecc71', '#e74c3c', '#f39c12']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        
        // 评分分布图
        new Chart(document.getElementById('ratingChart'), {
            type: 'bar',
            data: {
                labels: ['1星', '2星', '3星', '4星', '5星'],
                datasets: [{
                    label: '评论数',
                    data: """ + f"[{summary['rating_dist'][1]}, {summary['rating_dist'][2]}, {summary['rating_dist'][3]}, {summary['rating_dist'][4]}, {summary['rating_dist'][5]}]" + """,
                    backgroundColor: ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#27ae60']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // 痛点词云图（用横向柱状图代替）
        new Chart(document.getElementById('painChart'), {
            type: 'bar',
            data: {
                labels: """ + json.dumps([p[0] for p in summary['top_pain_points']]) + """,
                datasets: [{
                    label: '提及次数',
                    data: """ + json.dumps([p[1] for p in summary['top_pain_points']]) + """,
                    backgroundColor: '#e74c3c'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true }
                }
            }
        });
        
        // 卖点词云图
        new Chart(document.getElementById('sellingChart'), {
            type: 'bar',
            data: {
                labels: """ + json.dumps([p[0] for p in summary['top_selling_points']]) + """,
                datasets: [{
                    label: '提及次数',
                    data: """ + json.dumps([p[1] for p in summary['top_selling_points']]) + """,
                    backgroundColor: '#2ecc71'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true }
                }
            }
        });
    </script>
</body>
</html>"""
    
    return html


if __name__ == "__main__":
    # 测试代码
    test_product = {
        "asin": "B08N5WRWNW",
        "title": "Test Product",
        "price": "$99.99",
        "rating": 4.5,
        "total_reviews": 100,
        "image_url": "",
        "url": "https://www.amazon.com/dp/B08N5WRWNW"
    }
    
    test_tagged_reviews = [
        {
            "review": {"rating": 5, "title": "Great!", "body": "Love it"},
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["good quality"],
                "use_cases": ["daily use"],
                "user_profile": "regular user",
                "improvement_suggestions": [],
                "summary": "Good product"
            }
        }
    ]
    
    generate_html_report(test_product, test_tagged_reviews, "test_report.html", debug=True)
    print("测试报告已生成: test_report.html")
