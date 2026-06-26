#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
专业 SVG 图表组件库
- 真实数据可视化
- 渐变装饰
- 多种图表类型
"""

def progress_ring(value: float, size: int = 100, color: str = "#F59E0B", label: str = "") -> str:
    """真实进度环"""
    import math
    radius = (size - 10) / 2
    circumference = 2 * math.pi * radius
    progress = value / 100 * circumference
    offset = circumference - progress
    
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <defs>
    <linearGradient id="grad_{value}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color};stop-opacity:0.6" />
    </linearGradient>
  </defs>
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#1A2332" stroke-width="6"/>
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="url(#grad_{value})" stroke-width="6"
    stroke-linecap="round"
    stroke-dasharray="{circumference}"
    stroke-dashoffset="{offset}"
    transform="rotate(-90 {size/2} {size/2})"/>
  <text x="{size/2}" y="{size/2}" text-anchor="middle" fill="white" font-size="18" font-weight="bold" dy=".3em">{int(value)}%</text>
</svg>'''

def bar_chart(data: list, width: int = 500, height: int = 300, colors: list = None) -> str:
    """柱状图 - data: [{'label': str, 'value': float, 'unit': str}]"""
    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
    
    bars = []
    max_val = max(d['value'] for d in data) if data else 1
    bar_width = (width - 100) / len(data) - 20
    
    for i, item in enumerate(data):
        bar_height = (item['value'] / max_val) * (height - 80)
        x = 50 + i * (bar_width + 20)
        y = height - 50 - bar_height
        color = colors[i % len(colors)]
        
        bars.append(f'''
    <defs>
      <linearGradient id="bar_{i}" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" style="stop-color:{color};stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:{color};stop-opacity:1" />
      </linearGradient>
    </defs>
    <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="8" fill="url(#bar_{i})"/>
    <text x="{x + bar_width/2}" y="{y - 10}" text-anchor="middle" fill="white" font-size="12" font-weight="bold">{item['value']}{item.get('unit', '')}</text>
    <text x="{x + bar_width/2}" y="{height - 25}" text-anchor="middle" fill="#94A3B8" font-size="11">{item['label']}</text>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {''.join(bars)}
</svg>'''

def kpi_card_big(number: str, unit: str, label: str, color: str = "#F59E0B", icon: str = None) -> str:
    """大数字 KPI 卡片"""
    icon_svg = ""
    if icon:
        icon_svg = f'''<svg width="32" height="32" viewBox="0 0 24 24" style="position: absolute; top: 20px; right: 20px; opacity: 0.3;">
    <path fill="{color}" d="{icon}"/>
  </svg>'''
    
    return f'''<div style="background: #1A2332; border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.1); position: relative;">
  {icon_svg}
  <div style="font-size: 48px; font-weight: 800; color: {color};">{number}<span style="font-size: 20px;">{unit}</span></div>
  <div style="font-size: 14px; color: #94A3B8; margin-top: 8px;">{label}</div>
</div>'''

def comparison_card(left_title: str, left_points: list, left_color: str, 
                   right_title: str, right_points: list, right_color: str) -> str:
    """左右对比卡片"""
    left_items = '\n'.join([f'''<div style="display: flex; align-items: start; gap: 12px;">
      <div style="width: 8px; height: 8px; background: {left_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB;">{point}</div>
    </div>''' for point in left_points])
    
    right_items = '\n'.join([f'''<div style="display: flex; align-items: start; gap: 12px;">
      <div style="width: 8px; height: 8px; background: {right_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB;">{point}</div>
    </div>''' for point in right_points])
    
    return f'''<div style="display: flex; gap: 40px;">
  <div style="flex: 1; background: #1A2332; border-radius: 16px; padding: 32px; border-top: 4px solid {left_color};">
    <h3 style="font-size: 24px; color: {left_color}; margin: 0 0 24px 0;">{left_title}</h3>
    <div style="display: flex; flex-direction: column; gap: 16px;">
      {left_items}
    </div>
  </div>
  
  <div style="display: flex; align-items: center;">
    <div style="width: 60px; height: 60px; border-radius: 50%; background: #1A2332; border: 3px solid #374151; display: flex; align-items: center; justify-content: center;">
      <span style="font-size: 20px; font-weight: bold; color: white;">VS</span>
    </div>
  </div>
  
  <div style="flex: 1; background: #1A2332; border-radius: 16px; padding: 32px; border-top: 4px solid {right_color};">
    <h3 style="font-size: 24px; color: {right_color}; margin: 0 0 24px 0;">{right_title}</h3>
    <div style="display: flex; flex-direction: column; gap: 16px;">
      {right_items}
    </div>
  </div>
</div>'''

def pyramid_with_cards(layers: list, card_color: str = "#F59E0B") -> str:
    """金字塔 + 右侧卡片
    layers: [{'title': str, 'desc': str, 'color': str}]
    """
    colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6"]
    
    # 金字塔 SVG
    pyramid_parts = []
    for i, layer in enumerate(layers):
        # 从上到下，宽度逐渐增加
        top_y = 30 + i * 90
        bottom_y = top_y + 60
        top_width = 80 + i * 60
        bottom_width = 140 + i * 60
        
        pyramid_parts.append(f'''<path d="M 200 {top_y} L {200 + top_width/2} {bottom_y} L {200 - top_width/2} {bottom_y} Z" fill="{layer.get('color', colors[i % len(colors)])}"/>''')
        pyramid_parts.append(f'''<text x="200" y="{(top_y + bottom_y)/2}" text-anchor="middle" fill="white" font-size="16" font-weight="bold">{i+1}</text>''')
    
    pyramid_svg = f'''<svg width="400" height="400" viewBox="0 0 400 400">
  {''.join(pyramid_parts)}
</svg>'''
    
    # 右侧卡片
    cards = []
    for i, layer in enumerate(layers):
        color = layer.get('color', colors[i % len(colors)])
        cards.append(f'''<div style="background: #1A2332; border-radius: 12px; padding: 20px; border-left: 4px solid {color};">
      <div style="font-size: 16px; font-weight: bold; color: white;">{layer['title']}</div>
      <div style="font-size: 13px; color: #94A3B8; margin-top: 8px;">{layer['desc']}</div>
    </div>''')
    
    return f'''<div style="display: flex; gap: 40px; align-items: start;">
  <div style="flex-shrink: 0;">
    {pyramid_svg}
  </div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
    {''.join(cards)}
  </div>
</div>'''

def timeline_horizontal(events: list, width: int = 1100, height: int = 200) -> str:
    """横向时间线
    events: [{'year': str, 'title': str, 'desc': str}]
    """
    if not events:
        return ""
    
    spacing = (width - 100) / (len(events) - 1) if len(events) > 1 else 0
    colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6"]
    
    # 时间线主线
    timeline = [f'<line x1="50" y1="60" x2="{width-50}" y2="60" stroke="#374151" stroke-width="3"/>']
    
    # 事件节点
    for i, event in enumerate(events):
        x = 50 + i * spacing
        color = colors[i % len(colors)]
        
        timeline.append(f'''
    <circle cx="{x}" cy="60" r="15" fill="{color}"/>
    <text x="{x}" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="bold">{event['year']}</text>
    <text x="{x}" y="100" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{event['title']}</text>
    <text x="{x}" y="120" text-anchor="middle" fill="#94A3B8" font-size="11">{event.get('desc', '')}</text>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {''.join(timeline)}
</svg>'''

def decorative_elements() -> str:
    """装饰性背景元素"""
    return '''
  <!-- 背景网格 -->
  <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.03; pointer-events: none;">
    <defs>
      <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
        <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#4B5563" stroke-width="0.5"/>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)"/>
  </svg>
  
  <!-- 渐变圆形装饰 -->
  <svg style="position: absolute; top: -100px; right: -100px; width: 400px; height: 400px; pointer-events: none;">
    <defs>
      <radialGradient id="glow">
        <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:0.15" />
        <stop offset="100%" style="stop-color:#F59E0B;stop-opacity:0" />
      </radialGradient>
    </defs>
    <circle cx="200" cy="200" r="200" fill="url(#glow)"/>
  </svg>
'''

def pie_chart(data: list, size: int = 300, center_text: str = None) -> str:
    """饼图/环形图 - data: [{'label': str, 'value': float, 'color': str}]
    
    使用 SVG arc 路径绘制饼图，支持中心文字（环形图模式）
    """
    if not data:
        return ""
    
    import math
    
    # 默认配色
    default_colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
    
    # 计算总和
    total = sum(d['value'] for d in data)
    if total == 0:
        total = 1
    
    # 圆心坐标
    cx, cy = size / 2, size / 2
    radius = size / 2 - 20
    
    # 内圆半径（环形图模式）
    inner_radius = radius * 0.6 if center_text else 0
    
    # 计算每个扇形的角度
    paths = []
    start_angle = -90  # 从12点钟方向开始
    
    for i, item in enumerate(data):
        color = item.get('color', default_colors[i % len(default_colors)])
        value = item['value']
        angle = (value / total) * 360
        
        # 计算扇形路径
        end_angle = start_angle + angle
        
        # 转换为弧度
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # 计算外圆弧的起止点
        x1 = cx + radius * math.cos(start_rad)
        y1 = cy + radius * math.sin(start_rad)
        x2 = cx + radius * math.cos(end_rad)
        y2 = cy + radius * math.sin(end_rad)
        
        # 判断是否为大角度弧
        large_arc = 1 if angle > 180 else 0
        
        if inner_radius > 0:
            # 环形图：计算内圆弧
            ix1 = cx + inner_radius * math.cos(end_rad)
            iy1 = cy + inner_radius * math.sin(end_rad)
            ix2 = cx + inner_radius * math.cos(start_rad)
            iy2 = cy + inner_radius * math.sin(start_rad)
            
            # 环形路径：外弧 -> 内弧（反向）
            path = f'''<path d="M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} L {ix1} {iy1} A {inner_radius} {inner_radius} 0 {large_arc} 0 {ix2} {iy2} Z" 
            fill="{color}" opacity="0.9">
            <title>{item['label']}: {value} ({value/total*100:.1f}%)</title>
          </path>'''
        else:
            # 饼图：从圆心开始
            path = f'''<path d="M {cx} {cy} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z" 
            fill="{color}" opacity="0.9">
            <title>{item['label']}: {value} ({value/total*100:.1f}%)</title>
          </path>'''
        
        paths.append(path)
        start_angle = end_angle
    
    # 中心文字（环形图模式）
    center_svg = ""
    if center_text:
        center_svg = f'''<text x="{cx}" y="{cy}" text-anchor="middle" fill="white" font-size="24" font-weight="bold" dy=".3em">{center_text}</text>'''
    
    # 图例
    legends = []
    for i, item in enumerate(data):
        color = item.get('color', default_colors[i % len(default_colors)])
        legends.append(f'''<div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
        <div style="width: 12px; height: 12px; background: {color}; border-radius: 2px;"></div>
        <span style="font-size: 13px; color: #94A3B8;">{item['label']}</span>
        <span style="font-size: 13px; color: white; font-weight: bold;">{item['value']}</span>
      </div>''')
    
    return f'''<div style="display: flex; gap: 40px; align-items: center;">
  <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
    {''.join(paths)}
    {center_svg}
  </svg>
  <div style="flex: 1;">
    {''.join(legends)}
  </div>
</div>'''


def radar_chart(data: list, size: int = 400, title: str = None) -> str:
    """雷达图 - data: [{'label': str, 'value': float, 'max': float}]
    
    多维度能力对比，自动绘制网格和数值区域
    """
    if not data or len(data) < 3:
        return ""
    
    import math
    
    n = len(data)
    cx, cy = size / 2, size / 2
    radius = size / 2 - 60
    
    # 计算每个维度的角度
    angle_step = 360 / n
    
    # 绘制网格（3层）
    grid_levels = [0.33, 0.66, 1.0]
    grid_paths = []
    
    for level in grid_levels:
        points = []
        for i in range(n):
            angle = math.radians(i * angle_step - 90)
            r = radius * level
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        grid_paths.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#374151" stroke-width="1" opacity="0.5"/>')
    
    # 绘制轴线
    axis_lines = []
    for i in range(n):
        angle = math.radians(i * angle_step - 90)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        axis_lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#374151" stroke-width="1" opacity="0.3"/>')
    
    # 绘制数据区域
    data_points = []
    for i, item in enumerate(data):
        max_val = item.get('max', 100)
        value = min(item['value'], max_val)  # 不超过最大值
        ratio = value / max_val if max_val > 0 else 0
        
        angle = math.radians(i * angle_step - 90)
        r = radius * ratio
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        data_points.append(f"{x:.1f},{y:.1f}")
    
    data_area = f'<polygon points="{" ".join(data_points)}" fill="#F59E0B" fill-opacity="0.3" stroke="#F59E0B" stroke-width="2"/>'
    
    # 绘制数据点
    data_dots = []
    for i, item in enumerate(data):
        max_val = item.get('max', 100)
        value = min(item['value'], max_val)
        ratio = value / max_val if max_val > 0 else 0
        
        angle = math.radians(i * angle_step - 90)
        r = radius * ratio
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        data_dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#F59E0B"/>')
    
    # 绘制标签
    labels = []
    for i, item in enumerate(data):
        angle = math.radians(i * angle_step - 90)
        label_r = radius + 30
        x = cx + label_r * math.cos(angle)
        y = cy + label_r * math.sin(angle)
        labels.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" fill="#94A3B8" font-size="12">{item["label"]}</text>')
        
        # 数值标签
        value_r = radius * (item['value'] / item.get('max', 100)) + 15
        vx = cx + value_r * math.cos(angle)
        vy = cy + value_r * math.sin(angle)
        labels.append(f'<text x="{vx:.1f}" y="{vy:.1f}" text-anchor="middle" fill="white" font-size="11" font-weight="bold">{item["value"]}</text>')
    
    title_svg = f'<text x="{cx}" y="30" text-anchor="middle" fill="white" font-size="16" font-weight="bold">{title}</text>' if title else ""
    
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  {title_svg}
  {''.join(grid_paths)}
  {''.join(axis_lines)}
  {data_area}
  {''.join(data_dots)}
  {''.join(labels)}
</svg>'''


def data_table(headers: list, rows: list, column_widths: list = None) -> str:
    """数据表格 - 适合大量数据展示
    
    Args:
        headers: ['列1', '列2', '列3']
        rows: [['值1', '值2', '值3'], ...]
        column_widths: [200, 150, 150] (可选)
    """
    if not headers or not rows:
        return ""
    
    n_cols = len(headers)
    
    # 默认等宽
    if not column_widths:
        total_width = 800
        col_width = total_width // n_cols
        column_widths = [col_width] * n_cols
    
    # 表头
    header_cells = []
    for i, h in enumerate(headers):
        header_cells.append(f'''<th style="background: #1A2332; padding: 16px; text-align: left; font-size: 14px; font-weight: bold; color: #F59E0B; border-bottom: 2px solid #F59E0B;">
          {h}
        </th>''')
    
    # 表体
    body_rows = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            # 最后一列右对齐（通常是数值）
            align = "right" if i == n_cols - 1 else "left"
            cells.append(f'''<td style="padding: 14px 16px; font-size: 13px; color: white; border-bottom: 1px solid #374151; text-align: {align};">
              {cell}
            </td>''')
        
        body_rows.append(f'''<tr style="background: rgba(26, 35, 50, 0.5);">
          {''.join(cells)}
        </tr>''')
    
    return f'''<div style="background: #0B1221; border-radius: 12px; overflow: hidden; border: 1px solid #374151;">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr>
        {''.join(header_cells)}
      </tr>
    </thead>
    <tbody>
      {''.join(body_rows)}
    </tbody>
  </table>
</div>'''


def gauge_chart(value: float, max_value: float = 100, size: int = 200, 
                label: str = "", color: str = "#F59E0B") -> str:
    """仪表盘图表 - 半圆仪表
    
    适合展示进度、完成率等单一指标
    """
    import math
    
    cx, cy = size / 2, size * 0.65
    radius = size / 2 - 20
    
    # 计算角度（半圆：-180度到0度）
    ratio = min(value / max_value, 1.0) if max_value > 0 else 0
    angle = -180 + (ratio * 180)  # 从左边开始
    
    # 背景弧
    bg_arc = f'''<path d="M {cx - radius} {cy} A {radius} {radius} 0 0 1 {cx + radius} {cy}" 
      fill="none" stroke="#374151" stroke-width="12" stroke-linecap="round"/>'''
    
    # 数值弧
    end_rad = math.radians(angle)
    end_x = cx + radius * math.cos(end_rad)
    end_y = cy + radius * math.sin(end_rad)
    
    large_arc = 1 if ratio > 0.5 else 0
    value_arc = f'''<path d="M {cx - radius} {cy} A {radius} {radius} 0 {large_arc} 1 {end_x:.1f} {end_y:.1f}" 
      fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'''
    
    # 指针
    pointer_rad = math.radians(-180 + ratio * 180)
    pointer_len = radius * 0.7
    pointer_x = cx + pointer_len * math.cos(pointer_rad)
    pointer_y = cy + pointer_len * math.sin(pointer_rad)
    pointer = f'''<line x1="{cx}" y1="{cy}" x2="{pointer_x:.1f}" y2="{pointer_y:.1f}" 
      stroke="white" stroke-width="3" stroke-linecap="round"/>
      <circle cx="{cx}" cy="{cy}" r="8" fill="white"/>'''
    
    # 数值文字
    value_text = f'''<text x="{cx}" y="{cy + 50}" text-anchor="middle" fill="white" font-size="32" font-weight="bold">{int(value)}</text>'''
    label_text = f'''<text x="{cx}" y="{cy + 75}" text-anchor="middle" fill="#94A3B8" font-size="14">{label}</text>''' if label else ""
    
    return f'''<svg width="{size}" height="{size * 0.7}" viewBox="0 0 {size} {size * 0.7}">
  {bg_arc}
  {value_arc}
  {pointer}
  {value_text}
  {label_text}
</svg>'''


def area_chart(data: list, width: int = 600, height: int = 350, colors: list = None) -> str:
    """面积图 - data: [{'label': str, 'value': float}, ...]
    
    支持多系列：每条 data 中可用 'series' 字段区分不同系列
    单系列直接生成；多系列自动分组配色
    """
    import math

    if not data:
        return ""

    if not colors:
        colors = ["#F59E0B", "#3B82F6", "#10B981", "#EA580C", "#8B5CF6"]

    # 检查是否多系列
    series_keys = list(dict.fromkeys(d.get('series', 'default') for d in data))
    is_multi = len(series_keys) > 1

    pad_left, pad_right, pad_top, pad_bottom = 60, 30, 30, 50
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    # 构建多系列数据
    series_data = {}
    all_labels = []
    all_values = []
    for d in data:
        sk = d.get('series', 'default')
        series_data.setdefault(sk, []).append(d)
        all_values.append(d['value'])
        if d['label'] not in all_labels:
            all_labels.append(d['label'])

    max_val = max(all_values) if all_values else 1
    if max_val == 0:
        max_val = 1
    n_labels = max(len(all_labels), 2)

    svg_parts = []

    # X 轴标签
    for i, label in enumerate(all_labels):
        x = pad_left + (i / max(n_labels - 1, 1)) * chart_w
        svg_parts.append(f'<text x="{x:.1f}" y="{height - 10}" text-anchor="middle" fill="#94A3B8" font-size="11">{label}</text>')

    # Y 轴网格线 (5 条)
    for i in range(5):
        y = pad_top + (i / 4) * chart_h
        val = max_val * (1 - i / 4)
        svg_parts.append(f'<line x1="{pad_left}" y1="{y:.1f}" x2="{width - pad_right}" y2="{y:.1f}" stroke="#374151" stroke-width="1" opacity="0.3"/>')
        svg_parts.append(f'<text x="{pad_left - 10}" y="{y + 4}" text-anchor="end" fill="#94A3B8" font-size="10">{val:.0f}</text>')

    # 绘制每个系列
    for si, sk in enumerate(series_keys):
        series_items = series_data[sk]
        color = colors[si % len(colors)]
        n = len(series_items)

        # 计算点坐标
        points = []
        for i, item in enumerate(series_items):
            x = pad_left + (i / max(n - 1, 1)) * chart_w
            y = pad_top + chart_h - (item['value'] / max_val) * chart_h
            points.append((x, y))

        # 面积路径：从左下 → 数据点 → 右下 → 闭合
        area_path = f"M {points[0][0]} {pad_top + chart_h}"
        for px, py in points:
            area_path += f" L {px:.1f} {py:.1f}"
        area_path += f" L {points[-1][0]} {pad_top + chart_h} Z"

        # 线条路径
        line_path = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for px, py in points[1:]:
            line_path += f" L {px:.1f} {py:.1f}"

        svg_parts.append(f'<defs><linearGradient id="area_fill_{si}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:{color};stop-opacity:0.4"/><stop offset="100%" style="stop-color:{color};stop-opacity:0.05"/></linearGradient></defs>')
        svg_parts.append(f'<path d="{area_path}" fill="url(#area_fill_{si})"/>')
        svg_parts.append(f'<path d="{line_path}" fill="none" stroke="{color}" stroke-width="2.5"/>')

        # 数据点
        for px, py in points:
            svg_parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{color}"/>')
            svg_parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2" fill="white"/>')

    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(svg_parts)}</svg>'


def horizontal_bar_chart(data: list, width: int = 700, height: int = 350, colors: list = None) -> str:
    """水平条形图 - data: [{'label': str, 'value': float, 'unit': str}]"""
    if not data:
        return ""

    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]

    pad_left, pad_right = 120, 80
    pad_top, pad_bottom = 20, 30
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    max_val = max(d['value'] for d in data) if data else 1
    if max_val == 0:
        max_val = 1

    bar_height = min(40, (chart_h - (len(data) - 1) * 8) / len(data))
    gap = 8
    total_bars_h = len(data) * bar_height + (len(data) - 1) * gap
    start_y = pad_top + (chart_h - total_bars_h) / 2

    bars = []

    for i, item in enumerate(data):
        y = start_y + i * (bar_height + gap)
        bar_w = (item['value'] / max_val) * chart_w
        color = colors[i % len(colors)]

        bars.append(f'<defs><linearGradient id="hbar_{i}" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:{color};stop-opacity:0.85"/><stop offset="100%" style="stop-color:{color};stop-opacity:1"/></linearGradient></defs>')
        bars.append(f'<rect x="{pad_left}" y="{y:.1f}" width="0" height="{bar_height}" rx="6" fill="url(#hbar_{i})">')
        bars.append(f'  <animate attributeName="width" from="0" to="{bar_w:.1f}" dur="0.8s" fill="freeze"/></rect>')
        # 背景条
        bars.append(f'<rect x="{pad_left}" y="{y:.1f}" width="{chart_w}" height="{bar_height}" rx="6" fill="#1A2332" opacity="0.5"/>')
        # 前景条（覆盖）
        bars.append(f'<rect x="{pad_left}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_height}" rx="6" fill="url(#hbar_{i})"/>')
        # 标签
        bars.append(f'<text x="{pad_left - 12}" y="{y + bar_height / 2 + 5}" text-anchor="end" fill="#E5E7EB" font-size="13">{item["label"]}</text>')
        # 数值
        bars.append(f'<text x="{pad_left + bar_w + 10}" y="{y + bar_height / 2 + 5}" fill="white" font-size="13" font-weight="bold">{item["value"]}{item.get("unit", "")}</text>')

    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(bars)}</svg>'


def funnel_chart(data: list, width: int = 600, height: int = 450, colors: list = None) -> str:
    """漏斗图 - data: [{'label': str, 'value': float}, ...]
    
    从上到下递减的漏斗形状，展示转化率/流程
    """
    import math

    if not data:
        return ""

    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]

    max_val = max(d['value'] for d in data) if data else 1
    if max_val == 0:
        max_val = 1

    pad_top, pad_bottom = 30, 30
    pad_x = 40
    usable_h = height - pad_top - pad_bottom
    step_h = usable_h / len(data)
    cx = width / 2
    max_half_w = (width - pad_x * 2) / 2

    parts = []

    for i, item in enumerate(data):
        ratio = item['value'] / max_val
        next_ratio = data[i + 1]['value'] / max_val if i < len(data) - 1 else ratio * 0.6
        curr_ratio = ratio

        y_top = pad_top + i * step_h
        y_bottom = y_top + step_h

        top_half_w = max_half_w * curr_ratio
        bottom_half_w = max_half_w * next_ratio

        # 计算百分比标签
        pct = item['value'] / data[0]['value'] * 100 if data[0]['value'] > 0 else 100
        color = colors[i % len(colors)]

        # 梯形路径
        path = (f"M {cx - top_half_w} {y_top} "
                f"L {cx + top_half_w} {y_top} "
                f"L {cx + bottom_half_w} {y_bottom} "
                f"L {cx - bottom_half_w} {y_bottom} Z")

        parts.append(f'<defs><linearGradient id="funnel_{i}" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:{color};stop-opacity:0.9"/><stop offset="100%" style="stop-color:{color};stop-opacity:0.7"/></linearGradient></defs>')
        parts.append(f'<path d="{path}" fill="url(#funnel_{i})"/>')
        # 标签
        text_y = (y_top + y_bottom) / 2 + 5
        parts.append(f'<text x="{cx}" y="{text_y}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{item["label"]}</text>')
        parts.append(f'<text x="{cx}" y="{text_y + 18}" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="12">{item["value"]}{item.get("unit", "")} ({pct:.1f}%)</text>')

    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(parts)}</svg>'


def stacked_bar_chart(data: list, width: int = 600, height: int = 350, colors: list = None) -> str:
    """堆叠柱状图 - data: [{'label': str, 'values': [{'name': str, 'value': float}, ...]}, ...]"""
    import math

    if not data:
        return ""

    if not colors:
        colors = ["#F59E0B", "#3B82F6", "#10B981", "#EA580C", "#8B5CF6"]

    # 收集所有系列名
    all_series = list(dict.fromkeys(
        v['name'] for d in data for v in d.get('values', [])
    ))

    pad_left, pad_right, pad_top, pad_bottom = 60, 30, 30, 60
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    # 计算每列的堆叠总值
    max_total = 0
    for d in data:
        total = sum(v['value'] for v in d.get('values', []))
        if total > max_total:
            max_total = total
    if max_total == 0:
        max_total = 1

    n = len(data)
    bar_w = min(80, (chart_w / n) * 0.6)
    spacing = chart_w / n

    bars = []

    for i, d in enumerate(data):
        x = pad_left + spacing * i + spacing / 2 - bar_w / 2
        cumulative = 0

        for si, series_name in enumerate(all_series):
            # 找到当前系列在当前柱子中的值
            val = 0
            for v in d.get('values', []):
                if v['name'] == series_name:
                    val = v['value']
                    break

            seg_h = (val / max_total) * chart_h
            y = pad_top + chart_h - cumulative - seg_h
            color = colors[si % len(colors)]

            if val > 0:
                bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{seg_h:.1f}" fill="{color}" opacity="0.9"/>')
                if seg_h > 25:
                    bars.append(f'<text x="{x + bar_w / 2}" y="{y + seg_h / 2 + 4}" text-anchor="middle" fill="white" font-size="11" font-weight="bold">{val}</text>')

            cumulative += seg_h

        # X 轴标签
        bars.append(f'<text x="{x + bar_w / 2}" y="{height - 15}" text-anchor="middle" fill="#94A3B8" font-size="11">{d["label"]}</text>')

    # 图例
    legend_parts = []
    legend_x = pad_left
    for si, name in enumerate(all_series):
        color = colors[si % len(colors)]
        legend_parts.append(f'<rect x="{legend_x}" y="4" width="12" height="12" rx="2" fill="{color}"/>')
        legend_parts.append(f'<text x="{legend_x + 16}" y="14" fill="#94A3B8" font-size="11">{name}</text>')
        legend_x += len(name) * 12 + 36

    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(legend_parts)}{"".join(bars)}</svg>'


def combo_chart(bar_data: list, line_data: list = None, width: int = 700, height: int = 400,
                bar_colors: list = None, line_color: str = "#EF4444") -> str:
    """组合图（柱状 + 折线）- 双 Y 轴
    
    Args:
        bar_data: [{'label': str, 'value': float, 'unit': str}]
        line_data: [{'label': str, 'value': float, 'unit': str}] (可选，用同一 label 匹配)
    """
    if not bar_data:
        return ""

    if not bar_colors:
        bar_colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6"]

    pad_left, pad_right = 70, 70
    pad_top, pad_bottom = 30, 60
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    n = len(bar_data)
    spacing = chart_w / n
    bar_w = min(50, spacing * 0.5)

    max_bar = max(d['value'] for d in bar_data) if bar_data else 1
    if max_bar == 0:
        max_bar = 1

    parts = []

    # Y 轴（左）网格线
    for i in range(5):
        y = pad_top + (i / 4) * chart_h
        val = max_bar * (1 - i / 4)
        parts.append(f'<line x1="{pad_left}" y1="{y:.1f}" x2="{width - pad_right}" y2="{y:.1f}" stroke="#374151" stroke-width="1" opacity="0.3"/>')
        parts.append(f'<text x="{pad_left - 8}" y="{y + 4}" text-anchor="end" fill="#94A3B8" font-size="10">{val:.0f}</text>')

    # 柱状图
    for i, item in enumerate(bar_data):
        x = pad_left + spacing * i + spacing / 2 - bar_w / 2
        bar_h = (item['value'] / max_bar) * chart_h
        y = pad_top + chart_h - bar_h
        color = bar_colors[i % len(bar_colors)]

        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" rx="4" fill="{color}" opacity="0.85"/>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{y - 6}" text-anchor="middle" fill="white" font-size="11" font-weight="bold">{item["value"]}{item.get("unit", "")}</text>')
        # X 标签
        parts.append(f'<text x="{x + bar_w / 2}" y="{height - 15}" text-anchor="middle" fill="#94A3B8" font-size="11">{item["label"]}</text>')

    # 折线图（右 Y 轴）
    if line_data and len(line_data) >= 2:
        max_line = max(d['value'] for d in line_data)
        if max_line == 0:
            max_line = 1

        # 右 Y 轴
        for i in range(5):
            y = pad_top + (i / 4) * chart_h
            val = max_line * (1 - i / 4)
            parts.append(f'<text x="{width - pad_right + 8}" y="{y + 4}" text-anchor="start" fill="#94A3B8" font-size="10">{val:.0f}</text>')

        line_points = []
        for d in line_data:
            # 找对应的 x 位置
            idx = next((i for i, bd in enumerate(bar_data) if bd['label'] == d['label']), None)
            if idx is not None:
                x = pad_left + spacing * idx + spacing / 2
                y = pad_top + chart_h - (d['value'] / max_line) * chart_h
                line_points.append((x, y))
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{line_color}"/>')
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="white"/>')
                parts.append(f'<text x="{x:.1f}" y="{y - 10}" text-anchor="middle" fill="{line_color}" font-size="11" font-weight="bold">{d["value"]}{d.get("unit", "")}</text>')

        if len(line_points) >= 2:
            line_path = f"M {line_points[0][0]:.1f} {line_points[0][1]:.1f}"
            for px, py in line_points[1:]:
                line_path += f" L {px:.1f} {py:.1f}"
            parts.append(f'<path d="{line_path}" fill="none" stroke="{line_color}" stroke-width="2.5" stroke-linecap="round"/>')

    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">{"".join(parts)}</svg>'


def trend_arrow(direction: str = "up", value: str = "+12%", color: str = None) -> str:
    """趋势箭头 SVG - 用于 KPI 卡片
    
    Args:
        direction: 'up' / 'down' / 'flat'
        value: 显示的值如 '+12%', '-5%'
        color: 箭头颜色，默认 up=绿, down=红, flat=灰
    """
    if color is None:
        color = "#10B981" if direction == "up" else "#EF4444" if direction == "down" else "#94A3B8"

    if direction == "up":
        path_d = "M12 19V5M5 12l7-7 7 7"
    elif direction == "down":
        path_d = "M12 5v14M5 12l7 7 7-7"
    else:
        path_d = "M5 12h14"

    return f'''<div style="display: inline-flex; align-items: center; gap: 4px; background: {"rgba(16,185,129,0.15)" if direction == "up" else "rgba(239,68,68,0.15)" if direction == "down" else "rgba(148,163,184,0.15)"}; padding: 4px 10px; border-radius: 20px;">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="{path_d}"/>
  </svg>
  <span style="font-size: 13px; color: {color}; font-weight: 600;">{value}</span>
</div>'''


def kpi_card_gradient(number: str, unit: str, label: str, color: str = "#F59E0B",
                      gradient_dir: str = "left", icon: str = None, trend: str = None) -> str:
    """渐变边框 KPI 卡片
    
    Args:
        gradient_dir: 'left' / 'top' / 'bottom' / 'right' - 渐变条方向
        trend: 'up' / 'down' / 'flat' - 趋势箭头
    """
    border_map = {
        "left": f"border-left: 5px solid {color};",
        "top": f"border-top: 5px solid {color};",
        "bottom": f"border-bottom: 5px solid {color};",
        "right": f"border-right: 5px solid {color};",
    }

    icon_svg = ""
    if icon:
        icon_svg = f'''<div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="{icon}"/>
    </svg>
  </div>'''

    trend_html = ""
    if trend:
        trend_html = trend_arrow(direction=trend.get('direction', 'up'), value=trend.get('value', ''))

    return f'''<div style="background: #1A2332; border-radius: 16px; padding: 28px 32px; {border_map.get(gradient_dir, border_map['left'])} box-shadow: 0 4px 24px rgba(0,0,0,0.3);">
  <div style="display: flex; justify-content: space-between; align-items: flex-start;">
    <div>
      <div style="font-size: 52px; font-weight: 800; color: {color}; line-height: 1.1;">{number}<span style="font-size: 22px; color: #94A3B8;">{unit}</span></div>
      <div style="font-size: 16px; color: #94A3B8; margin-top: 8px;">{label}</div>
    </div>
    {icon_svg}
  </div>
  {f'<div style="margin-top: 12px;">{trend_html}</div>' if trend else ''}
</div>'''


def kpi_card_glass(number: str, unit: str, label: str, color: str = "#F59E0B",
                   trend: str = None) -> str:
    """毛玻璃 KPI 卡片 - 用于深色背景上的半透明效果
    
    注意: 需要 backdrop-filter 支持，在某些截图环境可能降级为普通半透明
    """
    trend_html = ""
    if trend:
        trend_html = trend_arrow(direction=trend.get('direction', 'up'), value=trend.get('value', ''))

    return f'''<div style="background: rgba(255,255,255,0.06); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 20px; padding: 28px 32px; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
  <div style="font-size: 52px; font-weight: 800; color: {color}; line-height: 1.1;">{number}<span style="font-size: 22px; color: #94A3B8;">{unit}</span></div>
  <div style="font-size: 16px; color: #94A3B8; margin-top: 8px;">{label}</div>
  {f'<div style="margin-top: 12px;">{trend_html}</div>' if trend else ''}
</div>'''


def decorative_elements_v2(scheme: dict = None) -> str:
    """增强版装饰元素 - 支持动态配色
    
    Args:
        scheme: color scheme dict (from color_schemes.py)
    """
    bg = scheme.get('background', '#0B1221') if scheme else '#0B1221'
    grid_color = scheme.get('grid_stroke', '#4B5563') if scheme else '#4B5563'
    accent1 = scheme.get('accent', ['#F59E0B'])[0] if scheme else '#F59E0B'

    # 判断浅色/深色主题
    def is_light(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 299 + g * 587 + b * 114) / 1000 > 128

    light = is_light(bg)
    opacity = "0.04" if light else "0.03"

    return f'''
  <!-- 背景网格 -->
  <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: {opacity}; pointer-events: none;">
    <defs>
      <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
        <path d="M 60 0 L 0 0 0 60" fill="none" stroke="{grid_color}" stroke-width="0.5"/>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)"/>
  </svg>
  
  <!-- 点阵图案 -->
  <svg style="position: absolute; bottom: 0; left: 0; width: 600px; height: 400px; pointer-events: none; opacity: 0.02;">
    <defs>
      <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
        <circle cx="15" cy="15" r="1.5" fill="{grid_color}"/>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#dots)"/>
  </svg>

  <!-- 渐变圆形装饰 -->
  <svg style="position: absolute; top: -100px; right: -100px; width: 500px; height: 500px; pointer-events: none;">
    <defs>
      <radialGradient id="glow1">
        <stop offset="0%" style="stop-color:{accent1};stop-opacity:0.12" />
        <stop offset="100%" style="stop-color:{accent1};stop-opacity:0" />
      </radialGradient>
    </defs>
    <circle cx="250" cy="250" r="250" fill="url(#glow1)"/>
  </svg>

  <!-- 渐变圆形装饰2 -->
  <svg style="position: absolute; bottom: -150px; left: -80px; width: 400px; height: 400px; pointer-events: none;">
    <defs>
      <radialGradient id="glow2">
        <stop offset="0%" style="stop-color:{accent1};stop-opacity:0.08" />
        <stop offset="100%" style="stop-color:{accent1};stop-opacity:0" />
      </radialGradient>
    </defs>
    <circle cx="200" cy="200" r="200" fill="url(#glow2)"/>
  </svg>
'''


# ============================================================
# 图标库 - 25+ 常用 SVG 图标 (stroke-based, 兼容内联使用)
# ============================================================
ICONS = {
    # 团队/人力
    "users": "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z",
    "user": "M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 3a4 4 0 110 8 4 4 0 010-8z",
    
    # 数据/分析
    "chart": "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
    "trending_up": "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
    "trending_down": "M13 17h8m0 0V9m0 8l-8-8-4 4-6-6",
    "analytics": "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
    
    # 财务
    "dollar": "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    "bank": "M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11m16-11v11M8 14v3m4-3v3m4-3v3",
    
    # 安全/合规
    "shield": "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z",
    "lock": "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z",
    
    # 增长/效率
    "rocket": "M13 10V3L4 14h7v7l9-11h-7z",
    "zap": "M13 10V3L4 14h7v7l9-11h-7z",
    "target": "M12 8a4 4 0 100 8 4 4 0 000-8zM12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41",
    "clock": "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    
    # 创新科技
    "lightbulb": "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
    "cpu": "M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z",
    "code": "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4",
    
    # 状态/结果
    "check": "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    "check_circle": "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    "star": "M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z",
    "flag": "M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9",
    
    # 沟通/协作
    "chat": "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z",
    "globe": "M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9",
    
    # 文档/任务
    "document": "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    "clipboard": "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4",
    
    # 其他常用
    "heart": "M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z",
    "award": "M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z",
    "layers": "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
}
