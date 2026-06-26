#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
SVG Chart Components - Static charts for PPT slides.
No JavaScript, no CDN, pure SVG.

Usage:
    from svg_charts import progress_ring, bar_chart, comparison_chart, timeline_chart
"""

import math
from typing import List, Dict, Any, Optional


def progress_ring(value: float, label: str, color: str = "#F59E0B", size: int = 80) -> str:
    """
    Generate a circular progress ring.
    
    Args:
        value: Progress value (0-100)
        label: Label text
        color: Ring color
        size: SVG size in pixels
    
    Returns:
        SVG string
    """
    radius = (size - 10) / 2
    circumference = 2 * math.pi * radius
    dashoffset = circumference * (1 - value / 100)
    
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#374151" stroke-width="6"/>
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="{color}" stroke-width="6"
          stroke-dasharray="{circumference:.0f}" stroke-dashoffset="{dashoffset:.0f}"
          style="transform: rotate(-90deg); transform-origin: center;"/>
  <text x="{size/2}" y="{size/2 - 5}" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{value}%</text>
  <text x="{size/2}" y="{size/2 + 12}" text-anchor="middle" fill="#94A3B8" font-size="8">{label}</text>
</svg>'''


def kpi_card(value: str, unit: str, label: str, color: str = "#F59E0B", show_ring: bool = False) -> str:
    """
    Generate a KPI card with large number.
    
    Args:
        value: Main value (string, can be number or range)
        unit: Unit text
        label: Label text
        color: Accent color
        show_ring: Whether to show progress ring
    
    Returns:
        HTML string with inline styles
    """
    ring_svg = progress_ring(75, "", color, 70) if show_ring else ""
    
    return f'''<div style="flex: 1; background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%);
                border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);
                display: flex; align-items: center; gap: 16px;">
  {ring_svg}
  <div>
    <div style="font-size: 32px; font-weight: 800; color: white;">{value}<span style="font-size: 18px; color: {color};">{unit}</span></div>
    <div style="font-size: 14px; color: #94A3B8; margin-top: 4px;">{label}</div>
  </div>
</div>'''


def bar_chart(data: List[Dict[str, Any]], title: str = "", height: int = 200, colors: List[str] = None) -> str:
    """
    Generate a horizontal or vertical bar chart.
    
    Args:
        data: List of {"label": str, "value": number}
        title: Chart title
        height: Chart height in pixels
        colors: List of bar colors
    
    Returns:
        SVG string
    """
    if not data:
        return ""
    
    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6"]
    
    max_value = max(d.get("value", 0) for d in data)
    if max_value == 0:
        max_value = 1
    
    bar_width = 60
    gap = 20
    total_width = len(data) * (bar_width + gap) + 40
    
    bars = []
    for i, item in enumerate(data):
        value = item.get("value", 0)
        label = item.get("label", "")
        bar_height = int((value / max_value) * (height - 60))
        color = colors[i % len(colors)]
        x = 40 + i * (bar_width + gap)
        y = height - 40 - bar_height
        
        bars.append(f'''<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="8"
                       fill="url(#barGrad{i})" opacity="0.9"/>
                     <text x="{x + bar_width/2}" y="{height - 20}" text-anchor="middle"
                           fill="#94A3B8" font-size="12">{label}</text>
                     <text x="{x + bar_width/2}" y="{y - 8}" text-anchor="middle"
                           fill="white" font-size="14" font-weight="bold">{value}</text>''')
        
        # Add gradient
        bars.append(f'''<defs>
          <linearGradient id="barGrad{i}" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" style="stop-color:{color};stop-opacity:0.6"/>
            <stop offset="100%" style="stop-color:{color};stop-opacity:1"/>
          </linearGradient>
        </defs>''')
    
    title_el = f'<text x="20" y="24" fill="white" font-size="16" font-weight="bold">{title}</text>' if title else ""
    
    return f'''<svg width="{total_width}" height="{height}" viewBox="0 0 {total_width} {height}">
  {title_el}
  {"".join(bars)}
</svg>'''


def comparison_chart(left_data: List[str], right_data: List[str], 
                    left_title: str = "方案 A", right_title: str = "方案 B",
                    left_color: str = "#F59E0B", right_color: str = "#10B981") -> str:
    """
    Generate a side-by-side comparison chart.
    
    Args:
        left_data: List of bullet points for left side
        right_data: List of bullet points for right side
        left_title: Left column title
        right_title: Right column title
        left_color: Left accent color
        right_color: Right accent color
    
    Returns:
        HTML string
    """
    left_items = "".join([f'''<div style="display: flex; align-items: start; gap: 12px; margin-bottom: 16px;">
      <div style="width: 8px; height: 8px; background: {left_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB; line-height: 1.5;">{item}</div>
    </div>''' for item in left_data])
    
    right_items = "".join([f'''<div style="display: flex; align-items: start; gap: 12px; margin-bottom: 16px;">
      <div style="width: 8px; height: 8px; background: {right_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB; line-height: 1.5;">{item}</div>
    </div>''' for item in right_data])
    
    return f'''<div style="display: flex; gap: 32px; padding: 32px;">
  <!-- Left Column -->
  <div style="flex: 1; background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%);
              border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.1);">
    <div style="font-size: 20px; font-weight: bold; color: {left_color}; margin-bottom: 20px;
                padding-bottom: 12px; border-bottom: 2px solid {left_color};">{left_title}</div>
    {left_items}
  </div>
  
  <!-- VS Circle -->
  <div style="display: flex; align-items: center;">
    <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%);
                border: 3px solid #374151; display: flex; align-items: center; justify-content: center;">
      <span style="font-size: 18px; font-weight: bold; color: white;">VS</span>
    </div>
  </div>
  
  <!-- Right Column -->
  <div style="flex: 1; background: linear-gradient(135deg, #1A2332 0%, #0B1221 100%);
              border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.1);">
    <div style="font-size: 20px; font-weight: bold; color: {right_color}; margin-bottom: 20px;
                padding-bottom: 12px; border-bottom: 2px solid {right_color};">{right_title}</div>
    {right_items}
  </div>
</div>'''


def timeline_chart(events: List[Dict[str, Any]], height: int = 300) -> str:
    """
    Generate a horizontal timeline.
    
    Args:
        data: List of {"year": str, "title": str, "desc": str}
        height: SVG height
    
    Returns:
        SVG string
    """
    if not events:
        return ""
    
    n = len(events)
    if n == 0:
        return ""
    
    width = 1200
    padding = 60
    line_y = 80
    usable_width = width - 2 * padding
    spacing = usable_width / (n + 1)
    
    nodes = []
    cards = []
    
    for i, event in enumerate(events):
        year = event.get("year", event.get("label", ""))
        title = event.get("title", "")
        desc = event.get("desc", event.get("detail", ""))
        
        x = padding + (i + 1) * spacing
        
        # Node circle
        nodes.append(f'''<circle cx="{x}" cy="{line_y}" r="12" fill="#F59E0B"/>
                        <circle cx="{x}" cy="{line_y}" r="6" fill="white"/>''')
        
        # Year label
        nodes.append(f'<text x="{x}" y="{line_y - 25}" text-anchor="middle" fill="#F59E0B" font-size="14" font-weight="bold">{year}</text>')
        
        # Card below timeline
        card_y = line_y + 40
        cards.append(f'''<g transform="translate({x - 80}, {card_y})">
          <rect width="160" height="{height - line_y - 60}" rx="12" fill="#1A2332" stroke="rgba(255,255,255,0.1)"/>
          <text x="80" y="30" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{title[:12]}{'...' if len(title) > 12 else ''}</text>
          <text x="80" y="60" text-anchor="middle" fill="#94A3B8" font-size="11">{desc[:20]}{'...' if len(desc) > 20 else ''}</text>
        </g>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Timeline line -->
  <line x1="{padding}" y1="{line_y}" x2="{width - padding}" y2="{line_y}" stroke="#374151" stroke-width="3"/>
  
  <!-- Nodes -->
  {"".join(nodes)}
  
  <!-- Event cards -->
  {"".join(cards)}
</svg>'''


def pyramid_chart(levels: List[Dict[str, Any]], colors: List[str] = None) -> str:
    """
    Generate a pyramid/hierarchy chart.
    
    Args:
        levels: List of {"label": str, "value": str, "desc": str} from top to bottom
        colors: List of colors from top to bottom
    
    Returns:
        SVG string
    """
    if not levels:
        return ""
    
    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6"]
    
    n = len(levels)
    width = 600
    height = 400
    center_x = width / 2
    
    trapezoids = []
    for i, level in enumerate(levels):
        label = level.get("label", "")
        value = level.get("value", "")
        desc = level.get("desc", "")
        
        # Trapezoid dimensions (wider at bottom)
        top_width = 100 + i * 60
        bottom_width = 100 + (i + 1) * 60
        y_top = i * (height / n)
        y_bottom = (i + 1) * (height / n)
        
        color = colors[i % len(colors)]
        
        # Trapezoid path
        trapezoids.append(f'''<path d="M {center_x - top_width/2} {y_top}
                                 L {center_x + top_width/2} {y_top}
                                 L {center_x + bottom_width/2} {y_bottom}
                                 L {center_x - bottom_width/2} {y_bottom} Z"
                               fill="{color}" opacity="0.85"/>''')
        
        # Text
        trapezoids.append(f'''<text x="{center_x}" y="{y_top + 30}" text-anchor="middle"
                               fill="white" font-size="16" font-weight="bold">{label}</text>''')
        
        if value:
            trapezoids.append(f'''<text x="{center_x}" y="{y_top + 55}" text-anchor="middle"
                                   fill="rgba(255,255,255,0.8)" font-size="13">{value}</text>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {"".join(trapezoids)}
</svg>'''


def data_cards(data_points: List[Dict[str, Any]], columns: int = 4) -> str:
    """
    Generate a row of data cards.
    
    Args:
        data_points: List of {"label": str, "value": str, "unit": str}
        columns: Number of columns
    
    Returns:
        HTML string
    """
    if not data_points:
        return ""
    
    colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
    
    cards = []
    for i, dp in enumerate(data_points):
        label = dp.get("label", "")
        value = dp.get("value", "")
        unit = dp.get("unit", "")
        color = colors[i % len(colors)]
        
        cards.append(kpi_card(str(value), unit, label, color))
    
    return f'''<div style="display: flex; gap: 16px; margin-bottom: 24px;">
  {"".join(cards)}
</div>'''


# Export all functions
__all__ = [
    "progress_ring",
    "kpi_card",
    "bar_chart",
    "comparison_chart",
    "timeline_chart",
    "pyramid_chart",
    "data_cards"
]
