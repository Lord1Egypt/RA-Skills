#!/usr/bin/env python3
"""
综合HTML报告生成模块
8阶段全链路分析报告，交互式HTML + Chart.js可视化
"""

import json
import os
from datetime import datetime
from typing import Dict, List


def generate_html_report(
    query: str,
    market: str,
    products: List[Dict],
    tagged_reviews: Dict[str, List[Dict]],
    keyword_data: Dict,
    voc_data: Dict,
    competitor_data: Dict,
    opportunity_data: Dict,
    output_path: str,
    debug: bool = False
):
    """
    生成综合HTML报告

    Args:
        query: 原始搜索词
        market: 市场代码
        products: 产品列表
        tagged_reviews: {asin: [{review, tags}, ...]}
        keyword_data: 关键词扩展结果
        voc_data: VOC聚类结果
        competitor_data: 竞品分析结果
        opportunity_data: 机会分析结果
        output_path: 输出路径
        debug: 调试模式
    """
    if debug:
        print(f"  Generating report: {output_path}")

    # 统计数据
    total_reviews = sum(len(r) for r in tagged_reviews.values())
    total_products = len(products)

    # 评分统计
    ratings = []
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    for reviews in tagged_reviews.values():
        for item in reviews:
            rating = item.get("review", {}).get("rating", 0)
            if rating:
                ratings.append(rating)
            sentiments[item.get("tags", {}).get("sentiment", "neutral")] = sentiments.get(
                item.get("tags", {}).get("sentiment", "neutral"), 0
            ) + 1

    avg_rating = round(sum(ratings) / max(len(ratings), 1), 1) if ratings else 0

    # 准备JSON数据
    data_json = json.dumps({
        "query": query,
        "products": products[:10],
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "rating_dist": _rating_distribution(ratings),
        "sentiment_dist": sentiments,
        "keyword_data": keyword_data,
        "voc_data": _simplify_voc(voc_data),
        "competitor_data": _simplify_competitor(competitor_data),
        "opportunity_data": opportunity_data,
    }, ensure_ascii=False)

    # 生成HTML
    html = _build_html(query, market, total_products, total_reviews, avg_rating, data_json)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 报告已生成: {output_path}")
    return output_path


def _rating_distribution(ratings: List) -> Dict:
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in ratings:
        bucket = int(r)
        if bucket in dist:
            dist[bucket] += 1
    return dist


def _simplify_voc(voc_data: Dict) -> Dict:
    """简化VOC数据用于JSON序列化"""
    if not voc_data:
        return {"clusters": [], "overall_summary": ""}
    return {
        "clusters": voc_data.get("clusters", [])[:10],
        "severity_summary": voc_data.get("severity_summary", {}),
        "overall_summary": voc_data.get("overall_summary", "")
    }


def _simplify_competitor(competitor_data: Dict) -> Dict:
    """简化竞品数据"""
    if not competitor_data:
        return {"comparison_matrix": [], "radar_dimensions": [], "market_gaps": [], "overall_summary": ""}
    return {
        "comparison_matrix": competitor_data.get("comparison_matrix", [])[:6],
        "radar_dimensions": competitor_data.get("radar_dimensions", []),
        "market_gaps": competitor_data.get("market_gaps", [])[:5],
        "overall_summary": competitor_data.get("overall_summary", "")
    }


def _build_html(query: str, market: str, total_products: int, total_reviews: int, avg_rating: float, data_json: str) -> str:
    """构建完整HTML"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Amazon产品研究报告: {query}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}

/* Hero */
.hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 50px 0 40px; margin-bottom: 30px; }}
.hero h1 {{ font-size: 28px; margin-bottom: 8px; }}
.hero .query {{ font-size: 16px; opacity: 0.9; margin-bottom: 20px; }}
.stats-row {{ display: flex; gap: 20px; flex-wrap: wrap; }}
.stat-card {{ background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 12px; padding: 16px 24px; min-width: 140px; }}
.stat-card .value {{ font-size: 28px; font-weight: 700; }}
.stat-card .label {{ font-size: 12px; opacity: 0.8; }}

/* Sections */
.section {{ background: white; border-radius: 16px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 22px; margin-bottom: 20px; color: #1a1a2e; border-bottom: 3px solid #667eea; padding-bottom: 10px; display: inline-block; }}
.section h3 {{ font-size: 16px; color: #555; margin: 16px 0 10px; }}

/* Product Cards */
.product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }}
.product-card {{ border: 1px solid #e8ecf1; border-radius: 12px; padding: 16px; text-align: center; transition: transform 0.2s, box-shadow 0.2s; }}
.product-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
.product-card img {{ width: 120px; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; background: #f0f0f0; }}
.product-card .title {{ font-size: 13px; font-weight: 600; margin-bottom: 6px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
.product-card .meta {{ font-size: 12px; color: #888; }}
.product-card .price {{ font-size: 18px; font-weight: 700; color: #e74c3c; margin: 6px 0; }}
.product-card .stars {{ color: #f39c12; }}
.product-card a {{ display: inline-block; margin-top: 8px; font-size: 12px; color: #667eea; text-decoration: none; }}

/* Charts */
.chart-container {{ position: relative; margin: 20px 0; }}
.chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
@media (max-width: 768px) {{ .chart-row {{ grid-template-columns: 1fr; }} }}

/* Keyword */
.keyword-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.keyword-table th {{ background: #f0f2f5; padding: 10px 12px; text-align: left; font-weight: 600; }}
.keyword-table td {{ padding: 10px 12px; border-bottom: 1px solid #e8ecf1; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
.tag-high {{ background: #e8f5e9; color: #2e7d32; }}
.tag-medium {{ background: #fff3e0; color: #e65100; }}
.tag-low {{ background: #fce4ec; color: #c62828; }}

/* VOC */
.voc-cluster {{ border-left: 4px solid #667eea; padding: 12px 16px; margin-bottom: 12px; background: #f8f9fc; border-radius: 0 8px 8px 0; }}
.voc-cluster.critical {{ border-left-color: #e74c3c; }}
.voc-cluster.major {{ border-left-color: #f39c12; }}
.voc-cluster.minor {{ border-left-color: #3498db; }}
.voc-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
.voc-category {{ font-weight: 700; font-size: 15px; }}
.voc-severity {{ padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; color: white; }}
.sev-critical {{ background: #e74c3c; }}
.sev-major {{ background: #f39c12; }}
.sev-minor {{ background: #3498db; }}

/* Competitor Table */
.comp-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.comp-table th {{ background: #f0f2f5; padding: 10px; text-align: left; }}
.comp-table td {{ padding: 10px; border-bottom: 1px solid #e8ecf1; }}
.score-bar {{ display: inline-block; height: 8px; border-radius: 4px; background: linear-gradient(90deg, #667eea, #764ba2); }}

/* Opportunity */
.opp-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}
.opp-card {{ border: 1px solid #e8ecf1; border-radius: 12px; padding: 20px; }}
.opp-score {{ display: inline-block; width: 40px; height: 40px; line-height: 40px; text-align: center; border-radius: 50%; font-weight: 700; color: white; font-size: 18px; }}
.score-high {{ background: #27ae60; }}
.score-mid {{ background: #f39c12; }}
.opp-title {{ font-size: 16px; font-weight: 700; margin: 10px 0 6px; }}
.opp-desc {{ font-size: 13px; color: #666; margin-bottom: 10px; }}
.opp-meta {{ display: flex; gap: 8px; flex-wrap: wrap; font-size: 12px; }}

/* Summary Box */
.summary-box {{ background: linear-gradient(135deg, #f0f2ff 0%, #f5f0ff 100%); border-radius: 12px; padding: 20px 24px; margin: 16px 0; font-size: 15px; }}

/* TOC / Nav */
.toc {{ position: sticky; top: 0; background: white; z-index: 100; padding: 12px 0; border-bottom: 1px solid #e8ecf1; margin-bottom: 24px; }}
.toc-inner {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; }}
.toc a {{ color: #667eea; text-decoration: none; padding: 4px 8px; border-radius: 6px; }}
.toc a:hover {{ background: #f0f2ff; }}

/* Responsive */
@media (max-width: 768px) {{
  .stats-row {{ gap: 10px; }}
  .stat-card {{ min-width: 100px; padding: 12px 16px; }}
  .stat-card .value {{ font-size: 22px; }}
  .section {{ padding: 20px; }}
  .product-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .opp-grid {{ grid-template-columns: 1fr; }}
}}

/* Print */
@media print {{
  body {{ background: white; }}
  .hero {{ background: #667eea !important; -webkit-print-color-adjust: exact; }}
  .section {{ box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }}
}}
</style>
</head>
<body>

<div class="hero">
  <div class="container">
    <h1>Amazon产品研究报告</h1>
    <div class="query">搜索词: <strong>{query}</strong> | 市场: {market}</div>
    <div class="stats-row">
      <div class="stat-card"><div class="value">{total_products}</div><div class="label">分析产品</div></div>
      <div class="stat-card"><div class="value">{total_reviews}</div><div class="label">分析评论</div></div>
      <div class="stat-card"><div class="value">{avg_rating}</div><div class="label">平均评分</div></div>
      <div class="stat-card"><div class="value">{datetime.now().strftime('%Y-%m-%d')}</div><div class="label">生成日期</div></div>
    </div>
  </div>
</div>

<div class="container">

<div class="toc"><div class="toc-inner container">
  <a href="#products">产品一览</a>
  <a href="#reviews">评论分析</a>
  <a href="#keywords">关键词扩展</a>
  <a href="#voc">VOC痛点聚类</a>
  <a href="#competitors">竞品对比</a>
  <a href="#opportunities">新品机会</a>
  <a href="#summary">综合总结</a>
</div></div>

<div id="products" class="section">
  <h2>产品一览</h2>
  <div class="product-grid" id="productGrid"></div>
</div>

<div id="reviews" class="section">
  <h2>评论与评分概览</h2>
  <div class="chart-row">
    <div><h3>评分分布</h3><div class="chart-container"><canvas id="ratingChart"></canvas></div></div>
    <div><h3>情感分布</h3><div class="chart-container"><canvas id="sentimentChart"></canvas></div></div>
  </div>
  <div class="summary-box" id="reviewSummary"></div>
</div>

<div id="keywords" class="section">
  <h2>关键词扩展</h2>
  <h3>高频搜索词</h3>
  <table class="keyword-table"><thead><tr><th>关键词</th><th>搜索频度</th><th>来源</th><th>预估月搜索量</th></tr></thead><tbody id="kwHighFreq"></tbody></table>
  <h3>长尾关键词</h3>
  <table class="keyword-table"><thead><tr><th>长尾词</th><th>搜索量</th><th>竞争度</th><th>转化潜力</th></tr></thead><tbody id="kwLongTail"></tbody></table>
  <h3>关联词汇</h3>
  <table class="keyword-table"><thead><tr><th>词汇</th><th>关联类型</th><th>权重</th></tr></thead><tbody id="kwRelated"></tbody></table>
  <div class="summary-box" id="kwSummary"></div>
</div>

<div id="voc" class="section">
  <h2>VOC痛点聚类</h2>
  <div id="vocClusters"></div>
  <div class="summary-box" id="vocSummary"></div>
</div>

<div id="competitors" class="section">
  <h2>竞品对比矩阵</h2>
  <div class="chart-row">
    <div><h3>多维度雷达图对比</h3><div class="chart-container"><canvas id="radarChart"></canvas></div></div>
    <div><h3>市场空白</h3><div id="marketGaps"></div></div>
  </div>
  <h3>竞品详细对比</h3>
  <div style="overflow-x:auto;">
    <table class="comp-table"><thead><tr><th>产品</th><th>价格</th><th>质量</th><th>性价比</th><th>功能</th><th>满意度</th><th>品牌力</th><th>定位</th></tr></thead><tbody id="compTable"></tbody></table>
  </div>
  <div class="summary-box" id="compSummary"></div>
</div>

<div id="opportunities" class="section">
  <h2>新品机会分析</h2>
  <div class="opp-grid" id="oppGrid"></div>
  <div style="margin-top:16px;">
    <h3>最推荐方向</h3>
    <div class="summary-box" id="topRec"></div>
  </div>
  <div class="summary-box" id="oppSummary"></div>
</div>

<div id="summary" class="section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
  <h2 style="color: white; border-bottom-color: rgba(255,255,255,0.4);">综合总结</h2>
  <div id="finalSummary" style="font-size: 16px; line-height: 1.8;"></div>
</div>

<div style="text-align:center; padding: 40px 20px; color: #999; font-size: 13px;">
  <p>Powered by WorkBuddy Amazon Product Research | 数据来源: Amazon (via RapidAPI)</p>
  <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>

</div>

<script>
// ========== DATA ==========
const RAW_DATA = {data_json};

// ========== PRODUCT GRID ==========
(function() {{
  const grid = document.getElementById('productGrid');
  const products = RAW_DATA.products || [];
  products.forEach(p => {{
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${{p.image_url || 'https://via.placeholder.com/300x300/EEE/999'}}" alt="${{p.title}}" onerror="this.src='https://via.placeholder.com/300x300/EEE/999?text=No+Image'">
      <div class="title">${{p.title}}</div>
      <div class="stars">${{'⭐'.repeat(Math.round(p.rating || 0))}} ${{p.rating}}</div>
      <div class="price">${{p.price || 'N/A'}}</div>
      <div class="meta">${{(p.total_reviews || 0).toLocaleString()}} 条评论</div>
      <a href="${{p.url}}" target="_blank">查看详情 →</a>
    `;
    grid.appendChild(card);
  }});
}})();

// ========== RATING CHART ==========
(function() {{
  const dist = RAW_DATA.rating_dist || {{}};
  const ctx = document.getElementById('ratingChart').getContext('2d');
  new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels: ['1星','2星','3星','4星','5星'],
      datasets: [{{
        label: '评论数',
        data: [dist[1]||0, dist[2]||0, dist[3]||0, dist[4]||0, dist[5]||0],
        backgroundColor: ['#e74c3c','#e67e22','#f1c40f','#2ecc71','#27ae60'],
        borderRadius: 6
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
    }}
  }});
}})();

// ========== SENTIMENT CHART ==========
(function() {{
  const sent = RAW_DATA.sentiment_dist || {{}};
  const ctx = document.getElementById('sentimentChart').getContext('2d');
  new Chart(ctx, {{
    type: 'doughnut',
    data: {{
      labels: ['正面','负面','中性'],
      datasets: [{{
        data: [sent.positive||0, sent.negative||0, sent.neutral||0],
        backgroundColor: ['#27ae60','#e74c3c','#95a5a6'],
        borderWidth: 2,
        borderColor: '#fff'
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{
        legend: {{ position: 'bottom' }}
      }}
    }}
  }});
  // Summary
  const total = (sent.positive||0)+(sent.negative||0)+(sent.neutral||0);
  const posPct = total > 0 ? Math.round((sent.positive||0)/total*100) : 0;
  document.getElementById('reviewSummary').innerHTML = `共分析 ${{total.toLocaleString()}} 条评论，好评率 ${{posPct}}%，平均评分 ${{RAW_DATA.avg_rating}}。`;
}})();

// ========== KEYWORD TABLES ==========
(function() {{
  const kd = RAW_DATA.keyword_data || {{}};

  // High frequency
  const hfBody = document.getElementById('kwHighFreq');
  (kd.high_frequency_keywords || []).forEach(kw => {{
    const freqClass = kw.frequency === 'very_high' ? 'tag-high' : kw.frequency === 'high' ? 'tag-high' : 'tag-medium';
    hfBody.innerHTML += `<tr>
      <td><strong>${{kw.keyword}}</strong></td>
      <td><span class="tag ${{freqClass}}">${{kw.frequency || 'medium'}}</span></td>
      <td>${{kw.source || '-'}}</td>
      <td>${{(kw.monthly_searches_estimate || '-').toLocaleString()}}</td>
    </tr>`;
  }});

  // Long tail
  const ltBody = document.getElementById('kwLongTail');
  (kd.long_tail_keywords || []).forEach(kw => {{
    ltBody.innerHTML += `<tr>
      <td><strong>${{kw.keyword}}</strong></td>
      <td><span class="tag tag-${{kw.volume === 'high' ? 'high' : 'medium'}}">${{kw.volume}}</span></td>
      <td><span class="tag tag-${{kw.competition === 'low' ? 'high' : 'medium'}}">${{kw.competition}}</span></td>
      <td>${{kw.conversion_potential || '-'}}</td>
    </tr>`;
  }});

  // Related
  const relBody = document.getElementById('kwRelated');
  (kd.related_terms || []).forEach(t => {{
    relBody.innerHTML += `<tr>
      <td>${{t.term}}</td>
      <td>${{t.relation}}</td>
      <td>${{t.weight ? (t.weight*100).toFixed(0)+'%' : '-'}}</td>
    </tr>`;
  }});

  document.getElementById('kwSummary').innerHTML = kd.summary || '';
}})();

// ========== VOC CLUSTERS ==========
(function() {{
  const voc = RAW_DATA.voc_data || {{}};
  const container = document.getElementById('vocClusters');
  const clusters = voc.clusters || [];

  clusters.forEach(c => {{
    const sevClass = c.severity >= 8 ? 'critical' : c.severity >= 5 ? 'major' : 'minor';
    const sevLabel = c.severity >= 8 ? 'critical' : c.severity >= 5 ? 'major' : 'minor';
    const sevTag = c.severity >= 8 ? 'sev-critical' : c.severity >= 5 ? 'sev-major' : 'sev-minor';

    const pains = (c.pain_points || []).map(p => `<span style="display:inline-block;background:#f0f0f0;padding:2px 8px;border-radius:4px;margin:2px;font-size:12px;">${{p}}</span>`).join(' ');
    const quotes = (c.typical_reviews || []).slice(0, 2).map(q => `<blockquote style="border-left:3px solid #ddd;margin:6px 0;padding:4px 12px;font-size:12px;color:#666;">"${{q}}"</blockquote>`).join('');

    container.innerHTML += `
    <div class="voc-cluster ${{sevClass}}">
      <div class="voc-header">
        <span class="voc-category">${{c.category}}</span>
        <span class="voc-severity ${{sevTag}}">严重度: ${{c.severity}}/10 | 出现 ${{c.frequency || 0}}次</span>
      </div>
      <div>${{pains}}</div>
      ${{quotes}}
      <div style="font-size:12px;color:#888;margin-top:4px;">改进方向: ${{c.improvement_direction || '-'}}</div>
    </div>`;
  }});

  document.getElementById('vocSummary').innerHTML = voc.overall_summary || '';
}})();

// ========== COMPETITOR RADAR ==========
(function() {{
  const comp = RAW_DATA.competitor_data || {{}};
  const matrix = comp.comparison_matrix || [];
  const dims = comp.radar_dimensions || ['quality','value_for_money','features','customer_satisfaction','brand_power'];

  if (matrix.length === 0) return;

  const colors = ['#667eea','#e74c3c','#27ae60','#f39c12','#3498db','#9b59b6'];
  const datasets = matrix.map((m, i) => ({{
    label: m.title ? m.title.substring(0, 25) : 'Product '+(i+1),
    data: dims.map(d => (m.scores || {{}})[d] || 5),
    borderColor: colors[i % colors.length],
    backgroundColor: colors[i % colors.length] + '20',
    borderWidth: 2
  }}));

  const ctx = document.getElementById('radarChart').getContext('2d');
  new Chart(ctx, {{
    type: 'radar',
    data: {{ labels: dims.map(d => d.replace(/_/g,' ').replace(/\\b\\w/g, c=>c.toUpperCase())), datasets: datasets }},
    options: {{
      responsive: true,
      scales: {{ r: {{ beginAtZero: true, max: 10, ticks: {{ stepSize: 2 }} }} }},
      plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }} }} }} }}
    }}
  }});

  // Comparison table
  const tbody = document.getElementById('compTable');
  matrix.forEach(m => {{
    const scores = m.scores || {{}};
    tbody.innerHTML += `<tr>
      <td style="font-size:12px;">${{(m.title||'').substring(0, 40)}}</td>
      <td>${{m.price || '-'}}</td>
      <td><span class="score-bar" style="width:${{(scores.quality||0)*12}}px;"></span> ${{scores.quality||'-'}}</td>
      <td><span class="score-bar" style="width:${{(scores.value_for_money||0)*12}}px;"></span> ${{scores.value_for_money||'-'}}</td>
      <td><span class="score-bar" style="width:${{(scores.features||0)*12}}px;"></span> ${{scores.features||'-'}}</td>
      <td><span class="score-bar" style="width:${{(scores.customer_satisfaction||0)*12}}px;"></span> ${{scores.customer_satisfaction||'-'}}</td>
      <td><span class="score-bar" style="width:${{(scores.brand_power||0)*12}}px;"></span> ${{scores.brand_power||'-'}}</td>
      <td><span class="tag tag-${{m.positioning === '高端旗舰' ? 'low' : 'high'}}">${{m.positioning || '-'}}</span></td>
    </tr>`;
  }});

  // Market gaps
  const gapsDiv = document.getElementById('marketGaps');
  (comp.market_gaps || []).forEach(g => {{
    gapsDiv.innerHTML += `<div style="padding:8px;margin-bottom:8px;background:#f8f9fc;border-radius:8px;font-size:13px;">
      <strong>${{g.description || g}}</strong>
      ${{g.opportunity_score ? '<span style="float:right;color:#667eea;">机会评分: '+g.opportunity_score+'/10</span>' : ''}}
    </div>`;
  }});

  document.getElementById('compSummary').innerHTML = comp.overall_summary || '';
}})();

// ========== OPPORTUNITIES ==========
(function() {{
  const opp = RAW_DATA.opportunity_data || {{}};
  const grid = document.getElementById('oppGrid');
  const opportunities = opp.opportunities || [];

  opportunities.forEach(o => {{
    const scoreClass = o.opportunity_score >= 8 ? 'score-high' : o.opportunity_score >= 6 ? 'score-mid' : 'score-high';
    grid.innerHTML += `
    <div class="opp-card">
      <div class="opp-score ${{scoreClass}}">${{o.opportunity_score || '?'}}</div>
      <div class="opp-title">${{o.title}}</div>
      <div class="opp-desc">${{o.description}}</div>
      <div class="opp-meta">
        <span class="tag tag-high">市场: ${{o.target_market || '-'}}</span>
        <span class="tag tag-medium">需求: ${{o.estimated_demand || '-'}}</span>
        <span class="tag tag-low">竞争: ${{o.competitive_intensity || '-'}}</span>
        <span class="tag">价位: ${{o.price_range || '-'}}</span>
        <span class="tag">难度: ${{o.entry_difficulty || '-'}}</span>
      </div>
      <div style="font-size:12px;margin-top:8px;color:#666;">
        <strong>差异化:</strong> ${{o.key_differentiator || '-'}}<br>
        <strong>风险:</strong> ${{(o.risks || []).join(', ')}}
      </div>
    </div>`;
  }});

  // Top recommendation
  const rec = opp.top_recommendation || {{}};
  let recHtml = `<p><strong>推荐方向:</strong> ${{rec.direction || '-'}}</p>`;
  recHtml += `<p><strong>理由:</strong> ${{rec.reasoning || '-'}}</p>`;
  if (rec.action_items) {{
    recHtml += '<p><strong>行动项:</strong></p><ul style="font-size:14px;margin-left:20px;">';
    rec.action_items.forEach(a => {{ recHtml += `<li>${{a}}</li>`; }});
    recHtml += '</ul>';
  }}
  document.getElementById('topRec').innerHTML = recHtml;

  document.getElementById('oppSummary').innerHTML = `
    <p><strong>风险评估:</strong> ${{opp.risk_assessment || '-'}}</p>
    <p>${{opp.summary || ''}}</p>
  `;
}})();

// ========== FINAL SUMMARY ==========
(function() {{
  const voc = RAW_DATA.voc_data || {{}};
  const comp = RAW_DATA.competitor_data || {{}};
  const opp = RAW_DATA.opportunity_data || {{}};
  const kd = RAW_DATA.keyword_data || {{}};

  let summary = `<p>基于对 <strong>${{RAW_DATA.total_reviews.toLocaleString()}}</strong> 条评论的AI深度分析，我们发现了以下关键洞察：</p>`;

  if (voc.overall_summary) {{
    summary += `<p>🔴 <strong>VOC核心发现:</strong> ${{voc.overall_summary}}</p>`;
  }}

  if (comp.overall_summary) {{
    summary += `<p>📊 <strong>竞争格局:</strong> ${{comp.overall_summary}}</p>`;
  }}

  if (opp.summary) {{
    summary += `<p>💡 <strong>机会建议:</strong> ${{opp.summary}}</p>`;
  }}

  if (kd.summary) {{
    summary += `<p>🔑 <strong>关键词策略:</strong> ${{kd.summary}}</p>`;
  }}

  document.getElementById('finalSummary').innerHTML = summary;
}})();
</script>

</body>
</html>"""


if __name__ == "__main__":
    print("报告生成模块已加载")
