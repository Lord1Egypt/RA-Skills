#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.
# Security: Only performs local operations. No external network calls.

"""
Dashboard-specific prompts and templates for LLM HTML generation.

All rendering uses inline CSS + SVG. No external CDN, no Tailwind, no Chart.js.
"""

import json

# Dashboard layout prompt - uses inline CSS + SVG charts only
DASHBOARD_PROMPT = """你是一个专业的前端工程师，正在生成一个 DASHBOARD 风格的幻灯片。

## 数据
```json
{data}
```

## 布局要求

### 顶部：标题区域
- 左上角：eyebrow（小标签，如"业绩概览"）
- 主标题：大字加粗
- 可选：右侧放 logo 或日期

### 中部上：KPI 卡片区域（4个）
使用 CSS Grid 布局 `display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;`

每个 KPI 卡片结构（inline style）：
```html
<div style="background: #f8fafc; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0;">
  <div style="display: flex; align-items: baseline; gap: 4px; margin-bottom: 8px;">
    <span style="font-size: 36px; font-weight: 900; color: #dc2626;">100</span>
    <span style="font-size: 18px; color: #64748b;">万+</span>
  </div>
  <div style="font-size: 14px; font-weight: 500; color: #64748b; margin-bottom: 12px;">服务客户数</div>
  <div style="height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
    <div style="height: 100%; background: #ef4444; border-radius: 4px; width: 75%;"></div>
  </div>
</div>
```

### 中部下：图表 + 洞察区域
使用 CSS Grid 布局 `display: grid; grid-template-columns: 2fr 1fr; gap: 24px;`

左侧 2 列：SVG 图表（柱状图/折线图，纯 SVG 绘制）
```html
<div style="background: #f8fafc; border-radius: 12px; padding: 24px; border: 1px solid #e2e8f0;">
  <div style="font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 16px;">趋势分析</div>
  <svg viewBox="0 0 400 200" style="width: 100%;">
    <!-- 用 SVG rect 绘制柱状图，或 SVG polyline 绘制折线图 -->
    <rect x="50" y="60" width="40" height="120" fill="#dc2626" rx="4"/>
    <rect x="120" y="40" width="40" height="140" fill="#ea580c" rx="4"/>
    <rect x="190" y="20" width="40" height="160" fill="#d97706" rx="4"/>
    <rect x="260" y="0" width="40" height="180" fill="#059669" rx="4"/>
    <!-- 轴标签 -->
    <text x="70" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q1</text>
    <text x="140" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q2</text>
    <text x="210" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q3</text>
    <text x="280" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q4</text>
  </svg>
</div>
```

右侧 1 列：洞察列表
```html
<div style="background: #0f172a; border-radius: 12px; padding: 24px; color: white;">
  <div style="font-size: 18px; font-weight: 700; margin-bottom: 16px;">关键洞察</div>
  <div style="display: flex; flex-direction: column; gap: 12px;">
    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <span style="color: #f87171;">●</span>
      <span style="font-size: 14px; color: #e2e8f0;">洞察要点一</span>
    </div>
    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <span style="color: #fb923c;">●</span>
      <span style="font-size: 14px; color: #e2e8f0;">洞察要点二</span>
    </div>
  </div>
</div>
```

## 配色指南
- 红色系：#dc2626, #ef4444
- 橙色系：#ea580c, #f97316
- 琥珀系：#d97706, #f59e0b
- 绿色系：#059669, #10b981
- 蓝色系：#2563eb, #3b82f6

## 重要规则
1. 所有数据必须从输入数据中提取，不要编造
2. 进度条宽度应根据数据计算（如：数据值/最大值*100）
3. 图表必须使用 SVG 绘制，禁止使用 Chart.js 或 Canvas
4. 必须使用内联样式（style="..."），禁止使用 Tailwind
5. 禁止使用任何外部 CDN 或 script 标签

现在请生成完整的 HTML body 内容：
"""

# Big Number layout prompt
BIG_NUMBER_PROMPT = """生成一个大数字展示幻灯片。

## 数据
```json
{data}
```

## 布局
左侧：超大数字 + 单位 + 标签 + 进度条
右侧：背景说明文字 + 辅助图形

## 示例结构（inline CSS）
```html
<div style="height: 100vh; display: flex; align-items: center; padding: 48px;">
  <div style="width: 50%; display: flex; flex-direction: column; justify-content: center;">
    <div style="font-size: 72px; font-weight: 900; color: #dc2626;">100<span style="font-size: 36px; color: #64748b;">万+</span></div>
    <div style="font-size: 20px; color: #64748b; margin-top: 16px;">服务客户数</div>
    <div style="height: 12px; background: #e2e8f0; border-radius: 6px; margin-top: 24px; width: 75%;">
      <div style="height: 100%; background: #ef4444; border-radius: 6px; width: 75%;"></div>
    </div>
  </div>
  <div style="width: 50%; background: #f8fafc; border-radius: 16px; padding: 32px;">
    <div style="font-size: 18px; color: #64748b; line-height: 1.6;">
      说明文字...
    </div>
  </div>
</div>
```

## 规则
- 使用内联样式，禁止 Tailwind
- 图表使用 SVG，禁止 Chart.js
- 禁止外部 CDN 或 script 标签

请生成 HTML：
"""

# Timeline layout prompt
TIMELINE_PROMPT = """生成一个时间线幻灯片。

## 数据
```json
{data}
```

## 布局
横向时间线 + 事件卡片

## 示例结构（inline CSS）
```html
<div style="height: 100vh; display: flex; flex-direction: column; padding: 48px;">
  <div style="font-size: 36px; font-weight: 700; color: #1e293b; margin-bottom: 32px;">发展历程</div>
  <div style="flex: 1; position: relative;">
    <div style="position: absolute; top: 50%; left: 0; right: 0; height: 4px; background: #cbd5e1;"></div>
    <div style="display: flex; justify-content: space-between; align-items: center; height: 100%;">
      <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="width: 64px; height: 64px; background: #ef4444; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 18px; z-index: 1;">2020</div>
        <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-top: 32px; width: 160px; text-align: center;">
          <div style="font-weight: 700; color: #1e293b;">公司成立</div>
          <div style="font-size: 14px; color: #64748b; margin-top: 8px;">描述文字</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 规则
- 使用内联样式，禁止 Tailwind
- 图表使用 SVG，禁止 Chart.js
- 禁止外部 CDN 或 script 标签

请生成 HTML：
"""


# Chart type recommendations (for SVG rendering)
CHART_TYPE_GUIDE = {
    "数值对比": "bar",
    "趋势展示": "line",
    "占比分析": "donut",
    "分布情况": "bar",
    "对比变化": "bar_grouped",
    "累计数据": "area"
}


def get_chart_type(data_points: list) -> str:
    """Determine best chart type based on data characteristics."""
    if not data_points:
        return "bar"
    
    units = set(dp.get('unit', '') for dp in data_points)
    
    if len(units) == 1 and len(data_points) <= 6:
        return "bar"
    
    if '%' in units:
        return "donut"
    
    return "bar"


def generate_svg_bar_chart(labels: list, values: list, width: int = 400, height: int = 200) -> str:
    """Generate SVG bar chart (no external dependencies)."""
    if not labels or not values:
        return ""
    
    max_val = max(values) if values else 1
    bar_width = max(20, (width - 80) // len(labels) - 20)
    chart_height = height - 40
    colors = ['#dc2626', '#ea580c', '#d97706', '#059669', '#2563eb', '#7c3aed']
    
    bars = []
    for i, (label, val) in enumerate(zip(labels, values)):
        x = 40 + i * (bar_width + 20)
        bar_h = (val / max_val) * (chart_height - 20) if max_val > 0 else 0
        y = chart_height - bar_h
        color = colors[i % len(colors)]
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" fill="{color}" rx="4"/>')
        bars.append(f'<text x="{x + bar_width//2}" y="{chart_height + 20}" text-anchor="middle" font-size="12" fill="#64748b">{label}</text>')
    
    return f'<svg viewBox="0 0 {width} {height}" style="width:100%;">{"".join(bars)}</svg>'


def generate_svg_line_chart(labels: list, values: list, width: int = 400, height: int = 200) -> str:
    """Generate SVG line chart (no external dependencies)."""
    if not labels or not values:
        return ""
    
    max_val = max(values) if values else 1
    chart_height = height - 40
    step_x = (width - 80) / max(len(labels) - 1, 1)
    
    points = []
    label_texts = []
    for i, (label, val) in enumerate(zip(labels, values)):
        x = 40 + i * step_x
        y = chart_height - (val / max_val) * (chart_height - 20) if max_val > 0 else chart_height
        points.append(f"{x},{y}")
        label_texts.append(f'<text x="{x}" y="{chart_height + 20}" text-anchor="middle" font-size="12" fill="#64748b">{label}</text>')
    
    return (
        f'<svg viewBox="0 0 {width} {height}" style="width:100%;">'
        f'<polyline points="{" ".join(points)}" fill="none" stroke="#dc2626" stroke-width="3"/>'
        f'{" ".join(label_texts)}'
        f'</svg>'
    )


# Example slide data
EXAMPLE_DASHBOARD_DATA = {
    "template": "DASHBOARD",
    "layout_suggestion": "dashboard",
    "title": "业绩概览",
    "eyebrow": "2024年度报告",
    "data_points": [
        {"value": 100, "unit": "万+", "label": "服务客户数", "color": "red"},
        {"value": 2500, "unit": "万", "label": "年收入", "color": "orange"},
        {"value": 3, "unit": "亿", "label": "累计融资", "color": "amber"},
        {"value": 14, "unit": "亿", "label": "前轮估值", "color": "green"}
    ],
    "key_points": [
        "年度营收同比增长 150%",
        "企业客户占比提升至 70%",
        "产品矩阵覆盖 10+ 行业",
        "客户续费率保持 95% 以上"
    ],
    "chart_data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [500, 800, 1200, 2500],
        "title": "季度营收趋势"
    }
}

EXAMPLE_BIG_NUMBER_DATA = {
    "template": "BIG_NUMBER",
    "layout_suggestion": "big_number",
    "title": "市场表现",
    "eyebrow": "关键指标",
    "data_points": [
        {"value": 100, "unit": "万+", "label": "服务客户数"}
    ],
    "description": "公司自成立以来，已累计服务超过 100 万客户，覆盖金融、零售、制造等多个行业。"
}


if __name__ == "__main__":
    import json
    print("Dashboard prompt example:")
    print(DASHBOARD_PROMPT.format(data=json.dumps(EXAMPLE_DASHBOARD_DATA, ensure_ascii=False, indent=2)))
