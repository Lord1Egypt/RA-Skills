#!/usr/bin/env python3
"""
财务分析HTML可视化看板生成器（参考模板）

此脚本展示如何用Python f-string生成内嵌ECharts的HTML看板。
实际使用时，AI应根据具体数据进行修改和扩展。

核心模式：
1. 数据内嵌在<script>中（无外部JSON依赖）
2. ECharts 5.x CDN（多源回退）
3. IIFE封装
4. 每图表独立echarts.init()
"""

import json

# ── 看板HTML模板片段 ──────────────────────────

# CSS 样式框架（橙色主题）
CSS_FRAMEWORK = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #f0f4f8 0%, #e6edf3 100%);
  color: #1e293b; padding: 20px; line-height: 1.6;
}
.container { max-width: 1400px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #1e3a8a 0%, #0c4a6e 100%); color: white; padding: 30px 40px; border-radius: 16px; }
.chart-section { background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }
.chart-card { background: #f8fafc; border-radius: 10px; padding: 16px; border: 1px solid #e2e8f0; }
.chart-card .chart { height: 360px; }
"""

# ECharts CDN多重回退
ECHARTS_CDN = """
<script>
(function(){
  var urls = [
    "https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js",
    "https://cdn.staticfile.org/echarts/5.4.3/echarts.min.js",
    "https://lib.baomitu.com/echarts/5.4.3/echarts.min.js",
    "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js",
    "https://unpkg.com/echarts@5.4.3/dist/echarts.min.js"
  ];
  var s=document.createElement("script");
  s.src=urls[0];
  s.onerror=function(){ s.src=urls[1]; };
  document.head.appendChild(s);
})();
</script>
"""

# ── 辅助函数 ──────────────────────────────────

def yi(v, ndigits=2):
    """转亿元"""
    if v is None: return "N/A"
    return f"{v/1e8:.{ndigits}f}"

def pct(v, dec=2):
    if v is None: return "N/A"
    return f"{v:.{dec}f}%"

# ── 主入口 ────────────────────────────────────

def generate_html(core_data, metrics, years, stock_name, stock_code, output_path):
    """
    生成完整的HTML看板

    Args:
        core_data: dict[year][科目] = 数值(元)
        metrics: dict[year][指标] = 数值
        years: ["2022","2023","2024","2025"]
        stock_name: "贵州燃气"
        stock_code: "600903"
        output_path: 输出HTML路径
    """
    # 使用f-string框架构建HTML
    # 具体实现参考贵州燃气项目中的 generate_dashboard.py
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{stock_name}（{stock_code}）动态财务分析看板</title>
{ECHARTS_CDN}
<style>{CSS_FRAMEWORK}</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{stock_name}（{stock_code}）动态财务分析数据可视化看板</h1>
  </div>
  <!-- 图表区 -->
  <div class="chart-section">
    <div class="chart-grid">
      <div class="chart-card"><h3>资产负债趋势</h3><div class="chart" id="c1"></div></div>
      <div class="chart-card"><h3>营收与净利润趋势</h3><div class="chart" id="c2"></div></div>
      <!-- 更多图表... -->
    </div>
  </div>
</div>
<script>
(function(){{
  var R = {json.dumps(core_data, ensure_ascii=False)};
  var M = {json.dumps(metrics, ensure_ascii=False)};
  // 初始化ECharts图表...
}})();
</script>
</body>
</html>"""
    # f-string 中的 {{ }} 需要正确转义
    # 实际生成时参考贵州燃气项目完成版进行详细实现
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML看板已生成: {output_path}")


if __name__ == "__main__":
    print("此脚本为模板参考文件。")
    print("实际使用时，请根据具体数据在AI辅助下修改生成逻辑。")
    print("完整实现参考：贵州燃气项目/generate_dashboard.py")
