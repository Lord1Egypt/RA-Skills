#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: Only performs local operations. LLM calls go through adapter with user-provided API keys.

"""
Enhanced LLM HTML Generator - Forces SVG chart generation.

All rendering uses inline CSS + SVG. No external CDN, no Tailwind, no Chart.js.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import asyncio

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

from llm_adapter import LLMAdapter

# Dashboard prompt - uses inline CSS + SVG charts
DASHBOARD_PROMPT_WITH_CHART = """你是专业的PPT设计师。根据数据生成 Dashboard 风格的 HTML 页面。

## 硬性要求
1. **必须包含 SVG 图表**：使用纯 SVG 绘制柱状图/折线图（禁止 Chart.js、Canvas）
2. **必须包含 4 个 KPI 卡片**：大数字 + 单位 + 标签 + 进度条
3. **必须包含关键洞察列表**：带彩色圆点的要点
4. **只输出 HTML body 内容**（不要 <html>/<head>/<body> 标签）
5. **必须使用内联样式**（style="..."），禁止 Tailwind
6. **禁止使用任何外部 CDN 或 script 标签**

## 数据
```json
{data}
```

## 配色
- 红色：#dc2626
- 橙色：#ea580c
- 琥珀：#d97706
- 绿色：#059669
- 蓝色：#3b82f6
- 深蓝背景：#0f172a

## SVG 柱状图示例（必须使用 SVG）
```html
<svg viewBox="0 0 400 200" style="width:100%;">
  <rect x="50" y="80" width="40" height="100" fill="#dc2626" rx="4"/>
  <rect x="120" y="60" width="40" height="120" fill="#ea580c" rx="4"/>
  <rect x="190" y="40" width="40" height="140" fill="#d97706" rx="4"/>
  <rect x="260" y="20" width="40" height="160" fill="#059669" rx="4"/>
  <text x="70" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q1</text>
  <text x="140" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q2</text>
  <text x="210" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q3</text>
  <text x="280" y="195" text-anchor="middle" font-size="12" fill="#64748b">Q4</text>
</svg>
```

## KPI 卡片示例（inline style）
```html
<div style="background: #f8fafc; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0;">
  <div style="display: flex; align-items: baseline; gap: 4px;">
    <span style="font-size: 48px; font-weight: 900; color: #dc2626;">100</span>
    <span style="font-size: 18px; color: #64748b;">万+</span>
  </div>
  <div style="font-size: 14px; font-weight: 500; color: #64748b; margin-top: 8px;">服务客户数</div>
  <div style="height: 8px; background: #e2e8f0; border-radius: 4px; margin-top: 12px;">
    <div style="height: 100%; background: #ef4444; border-radius: 4px; width: 75%;"></div>
  </div>
</div>
```

现在生成 HTML：
"""

HTML_SCAFFOLD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; width: 1920px; height: 1080px; overflow: hidden; }}
  </style>
</head>
<body style="background: white;">
{content}
</body>
</html>'''


async def generate_dashboard_slide(slide_data: Dict[str, Any], model: str = None) -> str:
    """Generate a dashboard slide with SVG chart."""
    llm = LLMAdapter(model=model)
    
    # Extract data points for chart
    data_points = slide_data.get('data_points', [])
    
    # Add synthetic trend data if not present
    if len(data_points) >= 4:
        labels = [dp['label'] for dp in data_points[:4]]
        values = []
        for dp in data_points[:4]:
            val = dp.get('value', '0')
            import re
            match = re.search(r'[\d.]+', str(val))
            values.append(float(match.group()) if match else 0)
        
        slide_data['chart_data'] = {
            'labels': labels,
            'values': values,
            'title': '关键指标对比'
        }
    
    prompt = DASHBOARD_PROMPT_WITH_CHART.format(data=json.dumps(slide_data, ensure_ascii=False, indent=2))
    
    response = await llm.generate(prompt=prompt, max_tokens=4000, temperature=0.3)
    content = response.get('content', '')
    
    # Extract HTML if wrapped in code block
    if '```html' in content:
        content = content.split('```html')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    # Wrap in scaffold
    title = slide_data.get('title', 'Slide')
    return HTML_SCAFFOLD.format(title=title, content=content)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Slide data JSON file')
    parser.add_argument('--output', required=True, help='Output HTML file')
    parser.add_argument('--model', default='glm-4-flash', help='Model to use')
    args = parser.parse_args()
    
    with open(args.data) as f:
        slide_data = json.load(f)
    
    html = asyncio.run(generate_dashboard_slide(slide_data, args.model))
    
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"Generated: {args.output}")
