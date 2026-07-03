"""
外卖评价监控 - HTML报告生成器
生成交互式可视化报告，包含评分趋势、差评分析、异常告警等
"""
import json
import os
from datetime import datetime
from pathlib import Path


def generate_html_report(analysis_result: dict, df_info: dict = None, output_path: str = None) -> str:
    """生成HTML可视化报告"""

    # 准备数据
    summary = analysis_result.get("summary", {})
    sentiment = analysis_result.get("sentiment", {})
    dimensions = analysis_result.get("dimensions", {})
    trends = analysis_result.get("trends", {})
    anomalies = analysis_result.get("anomalies", [])
    keywords = analysis_result.get("keywords", [])
    negative_reviews = analysis_result.get("negative_reviews", [])

    total = summary.get("total", 0)
    if total == 0:
        return "<html><body><h2>暂无评价数据</h2></body></html>"

    # 评分分布数据
    rating_dist = summary.get("rating_distribution", {})
    rating_labels = list(rating_dist.keys())
    rating_values = list(rating_dist.values())
    rating_colors = ["#52c41a", "#73d13d", "#fadb14", "#ffa940", "#ff4d4f"]

    # 情感分布
    pos = sentiment.get("positive", 0)
    neu = sentiment.get("neutral", 0)
    neg = sentiment.get("negative", 0)

    # 维度分析数据
    dim_labels = list(dimensions.keys())
    dim_neg_ratios = [dimensions[d].get("negative_ratio", 0) for d in dim_labels]
    dim_pos_ratios = [dimensions[d].get("positive_ratio", 0) for d in dim_labels]

    # 趋势数据
    daily_data = trends.get("daily", [])
    trend_dates = [d.get("date_str", "") for d in daily_data]
    trend_ratings = [d.get("avg_rating", 0) for d in daily_data]
    trend_neg = [d.get("negative_ratio", 0) for d in daily_data]

    # 关键词
    top_keywords = keywords[:30]
    kw_labels = [k[0] for k in top_keywords]
    kw_counts = [k[1] for k in top_keywords]

    # 异常严重程度颜色
    severity_colors = {"high": "#ff4d4f", "medium": "#faad14", "low": "#52c41a"}

    # 时间范围
    time_range = summary.get("time_range", {})
    time_str = f"{time_range.get('start', '')} ~ {time_range.get('end', '')}"

    # 平台信息
    platforms = summary.get("platforms", {})
    platform_str = ", ".join(platforms.keys()) if platforms else "未识别"

    # 生成HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>外卖评价监控报告</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px; }}
.header h1 {{ font-size: 28px; margin-bottom: 10px; }}
.header .meta {{ opacity: 0.9; font-size: 14px; }}

.alert-bar {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
.alert-item {{ flex: 1; min-width: 200px; padding: 16px; border-radius: 10px; border-left: 4px solid; }}
.alert-item.high {{ background: #fff1f0; border-color: #ff4d4f; }}
.alert-item.medium {{ background: #fffbe6; border-color: #faad14; }}
.alert-item.low {{ background: #f6ffed; border-color: #52c41a; }}
.alert-item .type {{ font-weight: 700; font-size: 15px; margin-bottom: 4px; }}
.alert-item .msg {{ font-size: 13px; color: #666; }}

.stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }}
.stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; }}
.stat-card .value {{ font-size: 36px; font-weight: 700; color: #667eea; }}
.stat-card .label {{ font-size: 13px; color: #999; margin-top: 4px; }}
.stat-card.warning .value {{ color: #ff4d4f; }}
.stat-card.success .value {{ color: #52c41a; }}

.chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
.chart-box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.chart-box h3 {{ font-size: 16px; margin-bottom: 12px; color: #333; }}
.chart-box.full {{ grid-column: 1 / -1; }}
.chart-container {{ width: 100%; height: 350px; }}

.dim-chart {{ width: 100%; height: 400px; }}

.keyword-cloud {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 16px; justify-content: center; }}
.keyword-tag {{ padding: 4px 12px; border-radius: 16px; font-size: 13px; cursor: default; }}
.keyword-tag.hot {{ background: #fff1f0; color: #cf1322; }}
.keyword-tag.warm {{ background: #fff7e6; color: #d46b08; }}
.keyword-tag.normal {{ background: #e6f7ff; color: #096dd9; }}

.review-list {{ max-height: 500px; overflow-y: auto; }}
.review-item {{ padding: 12px 16px; border-bottom: 1px solid #f0f0f0; }}
.review-item:last-child {{ border-bottom: none; }}
.review-item .text {{ font-size: 14px; color: #333; margin-bottom: 4px; }}
.review-item .meta-row {{ font-size: 12px; color: #999; display: flex; gap: 16px; }}

.footer {{ text-align: center; padding: 20px; color: #999; font-size: 12px; }}

@media (max-width: 768px) {{
  .chart-row {{ grid-template-columns: 1fr; }}
  .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>🍔 外卖评价监控报告</h1>
  <div class="meta">
    生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} &nbsp;|&nbsp;
    评价总数：{total} 条 &nbsp;|&nbsp;
    数据时间：{time_str} &nbsp;|&nbsp;
    平台：{platform_str}
  </div>
</div>

<!-- 异常告警 -->
{"".join(f'''
<div class="alert-item {a.get("severity","low")}">
  <div class="type">{a.get("type","")}</div>
  <div class="msg">{a.get("message","")} · {a.get("details","")}</div>
</div>
''' for a in anomalies) if anomalies else '<div class="alert-item low"><div class="type">✅ 一切正常</div><div class="msg">当前评价数据无明显异常</div></div>'}
"""

    # 统计卡片
    avg_rating = summary.get("avg_rating", 0)
    neg_ratio = sentiment.get("negative_ratio", 0)

    html += f"""
<div class="stats-row">
  <div class="stat-card {'warning' if avg_rating < 4 else 'success'}">
    <div class="value">{avg_rating}</div>
    <div class="label">平均评分</div>
  </div>
  <div class="stat-card {'warning' if neg_ratio > 20 else ''}">
    <div class="value">{neg_ratio}%</div>
    <div class="label">差评率</div>
  </div>
  <div class="stat-card">
    <div class="value">{sentiment.get('positive', 0)}</div>
    <div class="label">好评数</div>
  </div>
  <div class="stat-card">
    <div class="value">{sentiment.get('negative', 0)}</div>
    <div class="label">差评数</div>
  </div>
</div>
"""

    # 图表行1: 评分分布 + 情感分布
    html += f"""
<div class="chart-row">
  <div class="chart-box">
    <h3>📊 评分分布</h3>
    <div class="chart-container" id="ratingChart"></div>
  </div>
  <div class="chart-box">
    <h3>😊 情感分析分布</h3>
    <div class="chart-container" id="sentimentChart"></div>
  </div>
</div>
"""

    # 图表行2: 评分趋势 + 差评趋势
    html += f"""
<div class="chart-row">
  <div class="chart-box full">
    <h3>📈 评分趋势与差评率变化</h3>
    <div class="chart-container" id="trendChart"></div>
  </div>
</div>
"""

    # 图表行3: 维度分析
    html += f"""
<div class="chart-row">
  <div class="chart-box full">
    <h3>🎯 各维度评价分析</h3>
    <div class="dim-chart" id="dimensionChart"></div>
  </div>
</div>
"""

    # 图表行4: 关键词云 + 差评列表
    html += f"""
<div class="chart-row">
  <div class="chart-box">
    <h3>🏷️ 高频关键词 (TOP 30)</h3>
    <div class="keyword-cloud">
      {"".join(f'<span class="keyword-tag {"hot" if c >= 10 else ("warm" if c >= 5 else "normal")}" style="font-size:{min(24, 12 + c)}px">{w}({c})</span>' for w, c in top_keywords)}
    </div>
    {f'<div class="chart-container" id="keywordChart" style="height:300px"></div>' if len(top_keywords) > 5 else ''}
  </div>
  <div class="chart-box">
    <h3>⚠️ 最新差评列表</h3>
    <div class="review-list">
      {"".join(f'''
      <div class="review-item">
        <div class="text">{r["content"]}</div>
        <div class="meta-row">
          <span>评分：{r.get("rating","-")}</span>
          <span>情感：{r.get("score","-")}</span>
          <span>{r.get("time","-")}</span>
        </div>
      </div>
      ''' for r in negative_reviews[:15]) if negative_reviews else '<div class="review-item"><div class="text">暂无差评 🎉</div></div>'}
    </div>
  </div>
</div>
"""

    # JavaScript 图表
    html += f"""
<script>
// 评分分布
(function() {{
  var chart = echarts.init(document.getElementById('ratingChart'));
  chart.setOption({{
    tooltip: {{ trigger: 'item' }},
    series: [{{
      type: 'pie',
      radius: ['45%', '75%'],
      avoidLabelOverlap: false,
      itemStyle: {{ borderRadius: 8, borderColor: '#fff', borderWidth: 2 }},
      label: {{ show: true, formatter: '{{b}}: {{c}}条 ({{d}}%)' }},
      data: [
        {{ value: {rating_dist.get("5星", 0)}, name: '5星 ⭐⭐⭐⭐⭐', itemStyle: {{ color: '#52c41a' }} }},
        {{ value: {rating_dist.get("4星", 0)}, name: '4星 ⭐⭐⭐⭐', itemStyle: {{ color: '#73d13d' }} }},
        {{ value: {rating_dist.get("3星", 0)}, name: '3星 ⭐⭐⭐', itemStyle: {{ color: '#fadb14' }} }},
        {{ value: {rating_dist.get("2星", 0)}, name: '2星 ⭐⭐', itemStyle: {{ color: '#ffa940' }} }},
        {{ value: {rating_dist.get("1星", 0)}, name: '1星 ⭐', itemStyle: {{ color: '#ff4d4f' }} }}
      ]
    }}]
  }});
}})();

// 情感分布
(function() {{
  var chart = echarts.init(document.getElementById('sentimentChart'));
  chart.setOption({{
    tooltip: {{ trigger: 'item' }},
    series: [{{
      type: 'pie',
      radius: '70%',
      data: [
        {{ value: {pos}, name: '好评 😊', itemStyle: {{ color: '#52c41a' }} }},
        {{ value: {neu}, name: '中性 😐', itemStyle: {{ color: '#faad14' }} }},
        {{ value: {neg}, name: '差评 😞', itemStyle: {{ color: '#ff4d4f' }} }}
      ],
      label: {{ formatter: '{{b}}\\n{{c}}条 ({{d}}%)' }}
    }}]
  }});
}})();

// 趋势图
(function() {{
  var chart = echarts.init(document.getElementById('trendChart'));
  chart.setOption({{
    tooltip: {{ trigger: 'axis' }},
    legend: {{ data: ['日均评分', '差评率%'] }},
    grid: {{ left: '3%', right: '4%', bottom: '3%', containLabel: true }},
    xAxis: {{
      type: 'category',
      data: {json.dumps(trend_dates)},
      axisLabel: {{ rotate: 30 }}
    }},
    yAxis: [
      {{ type: 'value', name: '评分', min: 0, max: 5, splitLine: {{ lineStyle: {{ type: 'dashed' }} }} }},
      {{ type: 'value', name: '差评率%', splitLine: {{ show: false }} }}
    ],
    series: [
      {{
        name: '日均评分',
        type: 'line',
        data: {json.dumps(trend_ratings)},
        smooth: true,
        itemStyle: {{ color: '#667eea' }},
        markLine: {{
          silent: true,
          data: [{{ yAxis: 4.0, label: {{ formatter: '告警线 4.0' }}, lineStyle: {{ color: '#ff4d4f', type: 'dashed' }} }}]
        }}
      }},
      {{
        name: '差评率%',
        type: 'bar',
        yAxisIndex: 1,
        data: {json.dumps(trend_neg)},
        itemStyle: {{ color: '#ffa940', opacity: 0.6 }}
      }}
    ]
  }});
}})();

// 维度分析
(function() {{
  var chart = echarts.init(document.getElementById('dimensionChart'));
  chart.setOption({{
    tooltip: {{ trigger: 'axis' }},
    legend: {{ data: ['好评占比%', '差评占比%'] }},
    grid: {{ left: '3%', right: '4%', bottom: '3%', containLabel: true }},
    xAxis: {{ type: 'category', data: {json.dumps(dim_labels)} }},
    yAxis: {{ type: 'value', name: '占比%', max: 100 }},
    series: [
      {{
        name: '好评占比%',
        type: 'bar',
        stack: 'total',
        data: {json.dumps(dim_pos_ratios)},
        itemStyle: {{ color: '#52c41a' }},
        label: {{ show: true, position: 'inside', formatter: '{{c}}%' }}
      }},
      {{
        name: '差评占比%',
        type: 'bar',
        stack: 'total',
        data: {json.dumps(dim_neg_ratios)},
        itemStyle: {{ color: '#ff4d4f' }},
        label: {{ show: true, position: 'inside', formatter: '{{c}}%' }}
      }}
    ]
  }});
}})();

// 关键词条形图
{"(function() { var chart = echarts.init(document.getElementById('keywordChart')); chart.setOption({ tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } }, grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true }, xAxis: { type: 'value' }, yAxis: { type: 'category', data: " + json.dumps(kw_labels[::-1]) + ", inverse: true }, series: [{ type: 'bar', data: " + json.dumps(kw_counts[::-1]) + ", itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: '#667eea' }, { offset: 1, color: '#764ba2' }]) } }] }); })();" if len(top_keywords) > 5 else ""}

// 响应式
window.addEventListener('resize', function() {{
  var charts = document.querySelectorAll('.chart-container, .dim-chart');
  charts.forEach(function(el) {{
    var instance = echarts.getInstanceByDom(el);
    if (instance) instance.resize();
  }});
}});
</script>

<div class="footer">
  外卖评价监控系统 · 自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} · 数据来源：各外卖平台商家后台
</div>

</div>
</body>
</html>"""

    # 保存文件
    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 报告已生成: {output_path}")

    return html


def generate_summary_text(analysis_result: dict) -> str:
    """生成文本摘要"""
    summary = analysis_result.get("summary", {})
    sentiment = analysis_result.get("sentiment", {})
    anomalies = analysis_result.get("anomalies", [])
    dimensions = analysis_result.get("dimensions", {})

    total = summary.get("total", 0)
    avg_rating = summary.get("avg_rating", "N/A")
    neg_ratio = sentiment.get("negative_ratio", 0)

    lines = [
        "📊 外卖评价监控摘要",
        "=" * 40,
        f"评价总数：{total} 条",
        f"平均评分：{avg_rating}",
        f"差评率：{neg_ratio}%",
        f"好评：{sentiment.get('positive', 0)} 条 | 中性：{sentiment.get('neutral', 0)} 条 | 差评：{sentiment.get('negative', 0)} 条",
        "",
    ]

    # 维度分析
    lines.append("📋 各维度分析：")
    for dim, data in dimensions.items():
        emoji = {"口味": "👅", "配送": "🚀", "服务": "💁", "价格": "💰"}.get(dim, "📌")
        lines.append(
            f"  {emoji} {dim}：提及率 {data.get('mention_ratio', 0)}%，"
            f"好评 {data.get('positive_ratio', 0)}% / 差评 {data.get('negative_ratio', 0)}%"
        )

    # 异常告警
    if anomalies:
        lines.append("")
        lines.append("⚠️ 异常告警：")
        for a in anomalies:
            sev = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(a.get("severity"), "⚪")
            lines.append(f"  {sev} [{a.get('type', '')}] {a.get('message', '')}")
            lines.append(f"     {a.get('details', '')}")
    else:
        lines.append("")
        lines.append("✅ 当前评价数据正常，暂无异常告警")

    return "\n".join(lines)
