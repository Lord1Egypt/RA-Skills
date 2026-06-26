#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

"""
LLM-based HTML Slide Generator (Strict Version)
Uses AI to generate professional HTML slides with pure inline CSS + SVG.

NO CDN, NO JavaScript, NO external dependencies.

Usage:
  python llm_generate_html.py --data slide_data.json --output slide.html
  python llm_generate_html.py --from outline.json --output-dir ./html_slides
"""

import sys
import json
import argparse
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio

# Add parent to path
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

try:
    from llm_adapter import LLMAdapter
    HAS_LLM = True
except ImportError:
    HAS_LLM = False


def enforce_minimum_font_sizes(html: str) -> str:
    """
    强制放大所有字体，确保页面填满画布。
    
    容器尺寸修正：
    - 强制主容器为 1920x1080px
    
    字体放大规则：
    - < 18px → 18px（最小基础字号）
    - 18-23px → 24px（小标题放大）
    - 24-35px → 36px（副标题放大）
    - 36-47px → 48px（标题放大）
    - >= 48px → 保持不变（已经够大）
    
    同时放大 padding：
    - padding: < 24px → 32px
    """
    # Fix container size - force to 1920x1080
    def fix_container_size(match):
        style = match.group(0)
        # Replace width and height
        style = re.sub(r'width:\s*\d+px', 'width: 1920px', style)
        style = re.sub(r'height:\s*\d+px', 'height: 1080px', style)
        return style
    
    # Apply to first div (main container)
    html = re.sub(
        r'<div style="[^"]*?(?:width|height)[^"]*?"',
        fix_container_size,  # Pass match object directly, not m.group(0)
        html,
        count=1
    )
    
    # Font size mapping
    def enlarge_font(match):
        size = float(match.group(1))
        unit = match.group(2) or 'px'
        
        if size < 18:
            new_size = 18
        elif size < 24:
            new_size = 24
        elif size < 36:
            new_size = 36
        elif size < 48:
            new_size = 48
        else:
            new_size = size  # Already big enough
        
        return f'font-size: {int(new_size)}{unit}'
    
    # Apply font size enlargement
    html = re.sub(r'font-size:\s*(\d+(?:\.\d+)?)(px|em|rem)?', enlarge_font, html)
    
    # Enlarge padding (only if < 32px)
    def enlarge_padding(match):
        padding = match.group(0)
        # Extract all padding values
        values = re.findall(r'(\d+)(px)', padding)
        if values:
            # Find the smallest value
            min_val = min(int(v[0]) for v in values)
            if min_val < 32:
                # Scale up proportionally
                scale = 32 / min_val if min_val > 0 else 1
                def scale_value(m):
                    val = int(m.group(1))
                    new_val = int(val * scale)
                    return f'{new_val}px'
                padding = re.sub(r'(\d+)px', scale_value, padding)
        return padding
    
    html = re.sub(r'padding:\s*[^;]+', enlarge_padding, html)
    
    # Enlarge border-radius (if < 16px)
    def enlarge_radius(match):
        size = float(match.group(1))
        if size < 16:
            return f'border-radius: 16px'
        return match.group(0)
    
    html = re.sub(r'border-radius:\s*(\d+(?:\.\d+)?)px', enlarge_radius, html)
    
    return html
    print("Warning: llm_adapter not found, using fallback")

try:
    from smart_layout_matcher import SmartLayoutMatcher
    HAS_SMART_MATCHER = True
except ImportError:
    HAS_SMART_MATCHER = False
    print("Warning: smart_layout_matcher not found, using rule-based matching")

try:
    from color_schemes import get_color_scheme, apply_colors_to_prompt
    HAS_COLOR_SCHEMES = True
except ImportError:
    HAS_COLOR_SCHEMES = False
    print("Warning: color_schemes not found, using default colors")

try:
    from strict_image_text_prompt import STRICT_IMAGE_TEXT_PROMPT
    SLIDE_PROMPT = STRICT_IMAGE_TEXT_PROMPT
except ImportError:
    try:
        from enhanced_prompt_v2 import ENHANCED_PROMPT_V2
        SLIDE_PROMPT = ENHANCED_PROMPT_V2
    except ImportError:
        try:
            from strict_slide_prompt import STRICT_SLIDE_PROMPT
            SLIDE_PROMPT = STRICT_SLIDE_PROMPT
        except ImportError:
            SLIDE_PROMPT = "Generate HTML slide with inline styles only. No CDN, no JavaScript."

try:
    from svg_charts_enhanced import (
        progress_ring, bar_chart, kpi_card_big, 
        comparison_card, pyramid_with_cards, timeline_horizontal,
        area_chart, horizontal_bar_chart, funnel_chart, stacked_bar_chart, combo_chart,
        trend_arrow, kpi_card_gradient, kpi_card_glass, decorative_elements_v2,
        ICONS, decorative_elements
    )
    HAS_SVG_CHARTS = True
except ImportError:
    HAS_SVG_CHARTS = False

try:
    from layouts import dedup_layout, ALL_LAYOUTS, LAYOUT_CATEGORIES
    HAS_LAYOUT_DEDUP = True
except ImportError:
    HAS_LAYOUT_DEDUP = False

try:
    from enhanced_prompt_v2 import build_prompt
    HAS_BUILD_PROMPT = True
except ImportError:
    HAS_BUILD_PROMPT = False


# HTML scaffold - minimal, no CDN
HTML_SCAFFOLD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>'''


def fix_broken_data_labels(data_points: List[Dict]) -> List[Dict]:
    """
    Fix broken data labels that are truncated text fragments.
    
    Examples of broken labels:
    - "，已完成B轮融资" → should be "融资状态"
    - "元，同比增长" → should be "增长率"
    - "人，覆盖" → should be "团队规模"
    
    Detection: label starts with punctuation, contains broken patterns, or has no semantic meaning.
    """
    if not data_points:
        return data_points
    
    fixed_points = []
    
    # Common meaningful label patterns based on unit
    label_keywords = {
        '亿': ['营收规模', '融资金额', '估值', '市值', 'GMV'],
        '万': ['服务客户数', '用户数', '团队规模', '企业数'],
        '%': ['增长率', '占比', '覆盖率', '满意度', '市场份额'],
        '+': ['服务客户数', '企业数', '用户数'],
        '人': ['团队规模', '员工数', '服务人数'],
        '元': ['营收', '融资金额', '合同金额'],
    }
    
    for i, dp in enumerate(data_points):
        label = dp.get('label', '')
        value = dp.get('value', '')
        unit = dp.get('unit', '')
        
        # Check if label is broken (more comprehensive patterns)
        is_broken = (
            label.startswith('，') or 
            label.startswith('、') or
            label.startswith(',') or
            label.startswith('元') or  # "元，同比增长"
            label.startswith('人') or  # "人，覆盖"
            len(label) < 2 or
            label.endswith('，') or
            label.endswith('、') or
            '，' in label[1:] or  # Has comma in the middle (fragment)
            not re.search(r'[\u4e00-\u9fff]', label)  # No Chinese chars
        )
        
        if is_broken:
            # Infer label from unit and context
            inferred_label = f'指标{i+1}'
            
            # Try to infer from unit
            for unit_key, suggestions in label_keywords.items():
                if unit_key in str(unit) or unit_key in str(value):
                    inferred_label = suggestions[0]
                    break
            
            # Create fixed data point
            fixed_dp = {
                'label': inferred_label,
                'value': value,
                'unit': unit
            }
            fixed_points.append(fixed_dp)
        else:
            fixed_points.append(dp)
    
    return fixed_points


def parse_numbers_from_text(text: str) -> List[Dict]:
    """
    Extract numeric data points from text as a fallback.
    
    Patterns:
    - 3亿元、2500万、14亿
    - 33%、60-70%、100%+
    - 100家、40人、110多个国家
    - 2020年、2023年
    - 排名第一
    """
    if not text:
        return []
    
    data_points = []
    
    # Unit label mapping
    unit_labels = {
        '亿': ['金额', '估值', '市值', '规模', '融资'],
        '万': ['金额', '客户数', '用户数', '营收'],
        '%': ['增长率', '占比', '覆盖率', '满意度'],
        '家': ['客户数', '企业数', '门店数'],
        '人': ['团队规模', '员工数', '用户数'],
        '年': ['成立时间', '发展年份'],
        '名': ['排名', '位置'],
        '个': ['数量', '产品数', '项目数'],
        '国家': ['覆盖国家', '服务地区'],
        '+': ['数量'],  # 100+、1000+
    }
    
    # Pattern: 数字+单位
    patterns = [
        # 金额：3亿元、2500万（最优先）
        (r'(\d+(?:\.\d+)?)\s*(亿|万)(?:\s*元)?', '金额'),
        # 百分比：33%、60-70%
        (r'(\d+(?:\.\d+)?)\s*%', '占比'),
        # 国家/地区：110多个国家
        (r'(\d+)\s*多?\s*个?\s*国家', '覆盖国家'),
        # 数量：100家、40人、110个
        (r'(\d+)\s*(家|人|个|名)\b', '数量'),
        # 年份：2020年
        (r'(20\d{2})\s*年', '年份'),
        # 范围：100+、1000+
        (r'(\d+)\s*\+', '数量'),
        # 排名：排名第一、排名第1
        (r'排名\s*第\s*(一|二|三|1|2|3|4|5)', '排名'),
    ]
    
    for pattern, default_label in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            value = match.group(1)
            unit = match.group(2) if len(match.groups()) > 1 else ''
            
            # Handle Chinese numbers
            if value == '一':
                value = '1'
            elif value == '二':
                value = '2'
            elif value == '三':
                value = '3'
            
            # Infer label from unit
            label = default_label
            if unit in unit_labels:
                # Search for context keywords in nearby text
                context_start = max(0, match.start() - 30)
                context = text[context_start:match.end() + 20]
                for kw in unit_labels[unit]:
                    if kw in context:
                        label = kw
                        break
            
            # Deduplication
            dp_str = f"{label}:{value}{unit}"
            if not any(f"{d.get('label')}:{d.get('value')}{d.get('unit')}" == dp_str for d in data_points):
                data_points.append({
                    'label': label,
                    'value': value,
                    'unit': unit
                })
    
    return data_points[:6]  # Limit to 6 data points per slide


async def preprocess_slide_data_async(
    slide_data: Dict[str, Any], 
    smart_matcher: 'SmartLayoutMatcher' = None
) -> Dict[str, Any]:
    """
    Preprocess slide data with LLM-based smart layout matching.
    
    Args:
        slide_data: Slide data dict
        smart_matcher: SmartLayoutMatcher instance (optional)
    
    Returns:
        Enhanced slide data with layout and chart hints
    """
    data_points = slide_data.get('data_points', [])
    key_points = slide_data.get('key_points', [])
    
    # Extract data points if missing
    if not data_points:
        content_detail = slide_data.get('content_detail', '')
        key_points_text = ' '.join(key_points) if key_points else ''
        combined_text = f"{content_detail} {key_points_text}"
        
        extracted = parse_numbers_from_text(combined_text)
        if extracted:
            data_points = extracted
            slide_data['data_points'] = data_points
            print(f"  ✓ Extracted {len(data_points)} data points from text")
    
    # Use LLM smart matcher ONLY (no rule-based fallback)
    if HAS_SMART_MATCHER and smart_matcher:
        try:
            match_result = await smart_matcher.match(slide_data)
            
            # Apply smart match result
            slide_data['layout_suggestion'] = match_result.layout
            slide_data['_smart_match'] = {
                'chart_type': match_result.chart_type,
                'confidence': match_result.confidence,
                'reason': match_result.reason,
                'visual_elements': match_result.visual_elements
            }
            
            print(f"  🤖 LLM match: {match_result.layout} ({match_result.confidence:.0%}) - {match_result.reason}")
            
        except Exception as e:
            print(f"  ⚠️ LLM match failed: {e}, using default layout")
            # Use default layout (no rule-based fallback)
            if not slide_data.get('layout_suggestion'):
                slide_data['layout_suggestion'] = 'CONTENT'
    else:
        # No smart matcher available, use default layout
        if not slide_data.get('layout_suggestion'):
            slide_data['layout_suggestion'] = 'CONTENT'
        print(f"  ℹ️ No LLM matcher, using layout: {slide_data['layout_suggestion']}")
    
    # Precompute progress ring values
    data_points = slide_data.get('data_points', [])
    for dp in data_points:
        value = dp.get('value', '0')
        unit = dp.get('unit', '')
        
        try:
            numeric_value = float(str(value).replace('+', '').replace(',', ''))
        except (ValueError, TypeError):
            numeric_value = 0
        
        if '%' in unit:
            progress = numeric_value
        elif numeric_value > 100:
            progress = 100
        elif numeric_value > 1:
            progress = numeric_value
        else:
            progress = numeric_value * 100
        
        progress = min(100, max(0, progress))
        stroke_dashoffset = 251.2 * (1 - progress / 100)
        
        dp['_progress'] = round(progress, 1)
        dp['_stroke_dashoffset'] = round(stroke_dashoffset, 2)
    
    # Fix broken data labels
    data_points = fix_broken_data_labels(data_points)
    slide_data['data_points'] = data_points
    
    # Generate chart hint
    slide_data = _generate_chart_hint(slide_data)
    
    return slide_data


def _generate_chart_hint(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate chart-specific hints based on layout and data characteristics.
    
    This function analyzes the data and layout to provide specific
    visualization hints for HTML generation.
    """
    layout = slide_data.get('layout_suggestion', 'CONTENT').upper()
    data_points = slide_data.get('data_points', [])
    smart_match = slide_data.get('_smart_match', {})
    
    # Default chart configuration
    chart_config = {
        'chart_type': 'auto',
        'show_legend': False,
        'show_grid': True,
        'color_by_category': False,
        'animation_type': 'fade',
        'emphasis_style': 'highlight'
    }
    
    # Layout-specific chart hints
    if layout == 'DASHBOARD':
        chart_config.update({
            'chart_type': smart_match.get('chart_type', 'kpi_cards'),
            'layout_mode': 'grid',
            'card_style': 'metric_card',
            'show_progress': any('%' in dp.get('unit', '') for dp in data_points),
            'columns': min(3, len(data_points))
        })
        
        # Suggest progress rings for percentage data
        if any('%' in dp.get('unit', '') for dp in data_points):
            chart_config['visual_hints'] = ['progress_rings', 'color_coded']
        
    elif layout == 'BIG_NUMBER':
        chart_config.update({
            'chart_type': 'hero_number',
            'layout_mode': 'centered',
            'font_scale': 'hero',
            'show_unit': True,
            'supporting_visual': 'trend_arrow' if len(data_points) > 1 else None
        })
        
    elif layout == 'COMPARISON':
        chart_config.update({
            'chart_type': smart_match.get('chart_type', 'two_column'),
            'layout_mode': 'split',
            'show_vs_badge': True,
            'color_scheme': 'contrast',
            'bar_style': 'horizontal'
        })
        
    elif layout == 'PYRAMID':
        chart_config.update({
            'chart_type': 'svg_pyramid',
            'layout_mode': 'vertical',
            'show_numbers': True,
            'gradient_style': 'top_down',
            'connection_lines': True
        })
        
    elif layout == 'TIMELINE':
        chart_config.update({
            'chart_type': smart_match.get('chart_type', 'horizontal_timeline'),
            'layout_mode': 'horizontal',
            'show_dates': True,
            'connection_style': 'dotted',
            'milestone_markers': True
        })
        
    elif layout == 'PIE_CHART':
        chart_config.update({
            'chart_type': 'donut_chart',
            'layout_mode': 'centered',
            'show_labels': True,
            'show_percentages': True,
            'inner_radius': 0.6
        })
        
    elif layout == 'RADAR_CHART':
        chart_config.update({
            'chart_type': 'hexagon_radar',
            'layout_mode': 'centered',
            'show_axis_labels': True,
            'fill_opacity': 0.3,
            'grid_lines': 5
        })
        
    elif layout == 'TABLE':
        chart_config.update({
            'chart_type': 'styled_table',
            'layout_mode': 'full_width',
            'header_style': 'bold',
            'zebra_stripes': True,
            'row_hover': True
        })
        
    elif layout == 'PROCESS_FLOW':
        chart_config.update({
            'chart_type': 'step_cards',
            'layout_mode': 'horizontal',
            'show_arrows': True,
            'step_numbers': True,
            'connection_style': 'gradient'
        })
        
    elif layout == 'ACTION_PLAN':
        chart_config.update({
            'chart_type': 'action_cards',
            'layout_mode': 'vertical',
            'priority_indicators': True,
            'timeline_hints': True
        })
    
    # Add visual elements from smart match
    if smart_match.get('visual_elements'):
        chart_config['visual_elements'] = smart_match['visual_elements']
    
    # Data-driven enhancements
    if data_points:
        # Detect if data has trends
        values = []
        for dp in data_points:
            try:
                v = float(str(dp.get('value', '0')).replace('+', '').replace(',', ''))
                values.append(v)
            except:
                pass
        
        if len(values) >= 3:
            # Check for increasing/decreasing trend
            if all(values[i] <= values[i+1] for i in range(len(values)-1)):
                chart_config['trend'] = 'increasing'
            elif all(values[i] >= values[i+1] for i in range(len(values)-1)):
                chart_config['trend'] = 'decreasing'
        
        # Detect if all values are percentages
        if all('%' in dp.get('unit', '') for dp in data_points):
            chart_config['all_percentages'] = True
            chart_config['total_hint'] = '100%'
    
    # Store chart config in slide_data
    slide_data['_chart_config'] = chart_config
    
    return slide_data


def preprocess_slide_data(slide_data: Dict[str, Any], smart_matcher=None) -> Dict[str, Any]:
    """
    Synchronous wrapper for preprocess_slide_data_async.
    
    This function provides a sync interface for the async preprocessing logic.
    Uses LLM-based smart matching (no rule-based fallback).
    """
    try:
        # Try to run async version
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, we need to use a different approach
            # For now, just do basic preprocessing without LLM
            data_points = slide_data.get('data_points', [])
            key_points = slide_data.get('key_points', [])
            
            # Extract data points if missing
            if not data_points:
                content_detail = slide_data.get('content_detail', '')
                key_points_text = ' '.join(key_points) if key_points else ''
                combined_text = f"{content_detail} {key_points_text}"
                extracted = parse_numbers_from_text(combined_text)
                if extracted:
                    data_points = extracted
                    slide_data['data_points'] = data_points
            
            # Precompute progress ring values
            for dp in data_points:
                value = dp.get('value', '0')
                unit = dp.get('unit', '')
                try:
                    numeric_value = float(str(value).replace('+', '').replace(',', ''))
                except (ValueError, TypeError):
                    numeric_value = 0
                
                if '%' in unit:
                    progress = numeric_value
                elif numeric_value > 100:
                    progress = 100
                elif numeric_value > 1:
                    progress = numeric_value
                else:
                    progress = numeric_value * 100
                
                progress = min(100, max(0, progress))
                stroke_dashoffset = 251.2 * (1 - progress / 100)
                
                dp['_progress'] = round(progress, 1)
                dp['_stroke_dashoffset'] = round(stroke_dashoffset, 2)
            
            # Generate chart hint
            slide_data = _generate_chart_hint(slide_data)
            return slide_data
        else:
            # Run async version
            return asyncio.run(preprocess_slide_data_async(slide_data, smart_matcher))
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(preprocess_slide_data_async(slide_data, smart_matcher))


def _preprocess_slide_data_rules(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based layout matching (fallback).
    """
    layout = slide_data.get('layout_suggestion', 'CONTENT').upper()
    data_points = slide_data.get('data_points', [])
    
    # Auto-adjust layout based on data point count
    if data_points:
        if layout == 'CONTENT':
            if len(data_points) >= 8:
                slide_data['layout_suggestion'] = 'TABLE'
            elif len(data_points) >= 5:
                has_percent = any('%' in dp.get('unit', '') for dp in data_points)
                slide_data['layout_suggestion'] = 'PIE_CHART' if has_percent else 'DASHBOARD'
            elif len(data_points) >= 3:
                slide_data['layout_suggestion'] = 'DASHBOARD'
            elif len(data_points) >= 1:
                slide_data['layout_suggestion'] = 'BIG_NUMBER'
        
        # Detect pie chart data (percentages that sum to ~100%)
        if all('%' in dp.get('unit', '') for dp in data_points):
            try:
                total = sum(float(dp.get('value', 0)) for dp in data_points)
                if 80 <= total <= 120:  # Allow some margin
                    slide_data['layout_suggestion'] = 'PIE_CHART'
            except:
                pass
        
        # Radar chart for multi-dimension evaluation (not percentage composition)
        # Keywords: 能力、维度、评估、评分
        title = slide_data.get('title', '').lower()
        content = slide_data.get('content_detail', '').lower()
        all_text = f"{title} {content}"
        radar_keywords = ['能力', '维度', '评估', '评分', '雷达', '综合', 'competency', 'evaluation']
        if any(kw in all_text for kw in radar_keywords):
            if 3 <= len(data_points) <= 8:
                slide_data['layout_suggestion'] = 'RADAR_CHART'
    
    return slide_data
    
    # Fix broken data labels
    data_points = fix_broken_data_labels(data_points)
    slide_data['data_points'] = data_points
    
    # Add chart hint based on layout
    chart_hint = ""
    
    if layout == 'DASHBOARD':
        if data_points:
            # Build data points info with precomputed stroke-dashoffset
            dp_info = []
            for dp in data_points:
                dp_info.append(f"""- {dp.get('label', '指标')}: {dp.get('value', '')}{dp.get('unit', '')}
  进度环 stroke-dashoffset="{dp.get('_stroke_dashoffset', 251.2)}" (进度 {dp.get('_progress', 100)}%)""")
            
            chart_hint = f"""
【数据可视化要求 - 重要！】
必须展示以下数据点，使用 KPI 卡片 + SVG 进度环：

数据点（已预计算 stroke-dashoffset）：
{chr(10).join(dp_info)}

生成要求：
1. 每个 data_point 生成一个 KPI 卡片（3列布局）
2. 卡片包含：图标 + 大数字 + 单位 + 标签

3. **进度环直接使用预计算值**（不要自己计算！）：
   示例：stroke-dashoffset="{data_points[0].get('_stroke_dashoffset', 251.2) if data_points else 251.2}"

正确示例：
<svg width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="none" stroke="#1A2332" stroke-width="6"/>
  <circle cx="50" cy="50" r="40" fill="none" stroke="#F59E0B" stroke-width="6"
    stroke-linecap="round"
    stroke-dasharray="251.2"
    stroke-dashoffset="25.12"
    transform="rotate(-90 50 50)"/>
  <text x="50" y="50" text-anchor="middle" fill="white" font-size="16" font-weight="bold" dy=".3em">90%</text>
</svg>

4. 如果数据超过 4 个，分成两行展示
5. 使用不同的强调色：#F59E0B, #EA580C, #10B981, #3B82F6, #8B5CF6
"""
    
    elif layout == 'COMPARISON':
        chart_hint = f"""
【对比布局要求】
必须使用左右分栏对比布局：
- 左栏：传统方案/现状（标题颜色 #F59E0B）
- 中间：VS 圆形标志
- 右栏：创新方案/改进（标题颜色 #10B981）

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

生成要求：
1. 左右两栏用不同强调色
2. 每个要点用圆点标记
3. VS 圆形居中对齐
"""
    
    elif layout == 'TIMELINE':
        chart_hint = f"""
【时间线布局要求】
必须使用横向 SVG 时间线：
- 横向线条连接节点
- 每个节点用圆形标记
- 节点下方放事件卡片

关键要点（按时间顺序）：
{json.dumps(key_points, ensure_ascii=False, indent=2)}
"""
    
    elif layout in ['BIG_NUMBER', 'big_number']:
        if data_points:
            chart_hint = f"""
【大数字布局要求 - 重要！】
必须展示所有数据点，采用以下布局：

1. 左侧：超大数字展示核心指标
   - 数字大小：150-200px
   - 颜色：#F59E0B（琥珀色）
   - 下方：指标说明文字

2. 右侧：SVG柱状图或其他数据点
   - 用柱状图展示其余数据点
   - 每个柱子上方标注数值
   - 底部标注标签

数据点（必须全部展示）：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

⚠️ 注意：不能只显示文字，必须用大数字+图表展示数据！
"""
    
    elif layout == 'PYRAMID':
        chart_hint = f"""
【金字塔布局要求 - 重要！】
必须使用以下完整结构（注意外层容器！）：

<div style="display: flex; gap: 40px; align-items: start;">
  <!-- 左侧：SVG金字塔（只放编号） -->
  <div style="flex-shrink: 0;">
    <svg width="400" height="400" viewBox="0 0 400 400">
      <!-- 4层金字塔路径 -->
      <path d="M 200 30 L 240 90 L 160 90 Z" fill="#F59E0B"/>
      <path d="M 160 90 L 240 90 L 280 180 L 120 180 Z" fill="#EA580C"/>
      <path d="M 120 180 L 280 180 L 330 290 L 70 290 Z" fill="#10B981"/>
      <path d="M 70 290 L 330 290 L 380 390 L 20 390 Z" fill="#3B82F6"/>
      <!-- 层级编号 -->
      <text x="200" y="65" text-anchor="middle" fill="white" font-size="16" font-weight="bold">1</text>
      <text x="200" y="140" text-anchor="middle" fill="white" font-size="16" font-weight="bold">2</text>
      <text x="200" y="240" text-anchor="middle" fill="white" font-size="16" font-weight="bold">3</text>
      <text x="200" y="345" text-anchor="middle" fill="white" font-size="16" font-weight="bold">4</text>
    </svg>
  </div>
  
  <!-- 右侧：文字卡片 -->
  <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
    <div style="background: #1A2332; border-radius: 12px; padding: 20px; border-left: 4px solid #F59E0B;">
      <div style="font-size: 16px; font-weight: bold; color: white;">第一层标题</div>
      <div style="font-size: 13px; color: #94A3B8; margin-top: 8px;">第一层描述</div>
    </div>
    <!-- 其他卡片... -->
  </div>
</div>

关键要点（按层级顺序）：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

数据点：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

⚠️ 注意：
1. 外层必须用 display: flex 容器包裹
2. 金字塔和卡片是并列的两个子元素
3. 不要在金字塔内部放长文字！
"""
    
    elif layout in ['CONTENT', 'CARD']:
        if data_points:
            chart_hint = f"""
【内容布局要求】
使用编号卡片列表展示要点：
- 每个要点一个卡片
- 左侧圆形编号
- 卡片有渐变背景和边框

数据点：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}
"""
    
    elif layout == 'LEFT-RIGHT' or layout == 'LEFT_RIGHT':
        chart_hint = f"""
【左右布局要求】
左侧：可视化图表（SVG）
右侧：要点说明

数据点：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}
"""
    
    elif layout == 'ACTION_PLAN':
        chart_hint = f"""
【行动计划布局要求】
使用步骤卡片展示：
- 横向或纵向排列
- 每个步骤有编号、标题、描述
- 用箭头或线条连接步骤

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

数据点：
{json.dumps(data_points, ensure_ascii=False, indent=2)}
"""
    
    elif layout == 'PIE_CHART':
        if data_points:
            chart_hint = f"""
【饼图布局要求 - 重要！】
必须使用 SVG arc 路径绘制扇形：

数据点（占比数据）：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

生成要求：
1. 使用 SVG <path> 绘制扇形弧
2. 弧路径公式：M cx cy L x1 y1 A r r 0 large_arc 1 x2 y2 Z
3. 计算每个扇形的角度：angle = (value / total) * 360
4. 添加图例说明
5. 中心可放置总数值文字
"""
    
    elif layout == 'RADAR_CHART':
        chart_hint = f"""
【雷达图布局要求 - 重要！】
展示多维度能力对比，至少3个维度：

数据点：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

生成要求：
1. 绘制3层六边形网格
2. 从中心向外绘制轴线
3. 数据区域用半透明多边形
4. 每个维度标注标签和数值
"""
    
    elif layout == 'TABLE':
        chart_hint = f"""
【表格布局要求 - 重要！】
适合大量数据展示：

数据点（超过6个）：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

关键要点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

生成要求：
1. 使用 <table> 标签
2. 表头用琥珀色 #F59E0B
3. 奇偶行交替背景色
4. 数值列右对齐
5. 表格有圆角边框
"""
    
    elif layout == 'GAUGE':
        if data_points:
            chart_hint = f"""
【仪表盘布局要求 - 重要！】
展示单一关键指标：

数据点：
{json.dumps(data_points[0] if data_points else {}, ensure_ascii=False, indent=2)}

生成要求：
1. 绘制半圆背景弧
2. 数值弧用强调色
3. 添加指针
4. 中心显示数值和标签
"""
    
    # Add chart hint to slide_data
    if chart_hint:
        slide_data['_chart_hint'] = chart_hint
    
    return slide_data


def validate_html(html: str, min_content_chars: int = 200) -> tuple[bool, str]:
    """
    Validate generated HTML.
    
    Args:
        html: HTML string to validate
        min_content_chars: Minimum character count for slide content (rejects empty shells)
    
    Returns:
        (is_valid, error_message)
    """
    # Check for forbidden patterns
    forbidden_patterns = [
        (r'<script[^>]*>', "禁止使用 <script> 标签"),
        (r'src=["\']https?://', "禁止使用外部资源链接（CDN）"),
        (r'href=["\']https?://cdn\.', "禁止使用 CDN 链接"),
        (r'class=["\'][^"\']*["\']', "禁止使用 class 样式类，必须用内联 style"),
        (r'tailwindcss\.com', "禁止使用 Tailwind CDN"),
        (r'chartjs\.org', "禁止使用 Chart.js CDN"),
        (r'fontawesome\.com', "禁止使用 FontAwesome CDN"),
    ]
    
    for pattern, error in forbidden_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            return False, error
    
    # Check for required patterns
    if 'style="' not in html:
        return False, "缺少内联样式 style=\"...\""
    
    # Check content density — reject empty shells
    # Strip tags to get text content only
    text_only = re.sub(r'<[^>]+>', '', html)
    text_only = re.sub(r'\s+', '', text_only)
    
    if len(text_only) < min_content_chars:
        return False, f"内容过少（仅 {len(text_only)} 字符，要求至少 {min_content_chars}）。请填充更多实质性内容。"
    
    return True, ""


class LLMHTMLGenerator:
    """LLM-based HTML slide generator with strict validation."""
    
    def __init__(self, model: str = None, style: str = None, theme: str = None, instruction: str = None):
        """Initialize with LLM adapter and color scheme.
        
        Args:
            model: LLM model name (e.g., "glm-4-flash", "gpt-4o")
            style: Color scheme name (e.g., "corporate", "tech", "nature")
            theme: Document theme for auto color selection (e.g., "AI", "finance")
            instruction: User instruction to guide HTML generation (highest priority)
        """
        if not HAS_LLM:
            raise RuntimeError("llm_adapter not available")
        
        self.llm = LLMAdapter(model=model)
        self.instruction = instruction  # User instruction
        self.prev_layouts = []  # Track previous layouts for dedup
        
        # Get color scheme
        if HAS_COLOR_SCHEMES:
            self.color_scheme = get_color_scheme(style=style, theme=theme)
        else:
            # Fallback to default
            self.color_scheme = {
                "name": "默认",
                "background": "#0B1221",
                "card": "#1A2332",
                "text_primary": "#FFFFFF",
                "text_secondary": "#94A3B8",
                "accent": ["#F59E0B", "#EA580C", "#10B981", "#3B82F6"],
                "grid_stroke": "#4B5563",
            }
    
    async def generate_slide_html(self, slide_data: Dict[str, Any], max_retries: int = 3) -> str:
        """
        Generate HTML for a single slide using LLM.
        
        Args:
            slide_data: Slide data including title, content, stats, etc.
            max_retries: Maximum number of retries on validation failure
        
        Returns:
            Complete HTML string
        """
        # Preprocess slide data
        slide_data = preprocess_slide_data(slide_data)
        
        # --- Layout dedup: ensure adjacent slides use different layouts ---
        suggested_layout = slide_data.get('layout', slide_data.get('template', slide_data.get('layout_suggestion', 'CONTENT')))
        if HAS_LAYOUT_DEDUP and self.prev_layouts:
            deduped_layout = dedup_layout(suggested_layout, self.prev_layouts)
            if deduped_layout != suggested_layout:
                print(f"  🔄 Layout dedup: {suggested_layout} → {deduped_layout}")
                slide_data['layout'] = deduped_layout
                slide_data['layout_suggestion'] = deduped_layout
        
        self.prev_layouts.append(slide_data.get('layout', suggested_layout))
        
        # Prepare prompt with color scheme
        slide_json = json.dumps(slide_data, ensure_ascii=False, indent=2)
        
        # --- Use build_prompt for dynamic color scheme + prev_layout insertion ---
        if HAS_BUILD_PROMPT:
            base_prompt = build_prompt(
                scheme=self.color_scheme, 
                prev_layout=self.prev_layouts[-2] if len(self.prev_layouts) >= 2 else None
            )
        elif HAS_COLOR_SCHEMES:
            base_prompt = apply_colors_to_prompt(SLIDE_PROMPT, self.color_scheme)
        else:
            base_prompt = SLIDE_PROMPT
        
        # Add chart hint if available
        chart_hint = slide_data.pop('_chart_hint', '')
        
        # Get colors from scheme
        bg = self.color_scheme['background']
        text_primary = self.color_scheme['text_primary']
        accent1 = self.color_scheme['accent'][0]
        
        prompt = base_prompt + f"""

---

## 输入数据
```json
{slide_json}
```

{chart_hint}

---

【通用规则 - 所有页面必须遵守】
1. ⚠️ **必须有可见的页面标题**：<h2 style="font-size: 36px; color: {text_primary}; margin: 0 0 40px 0;">标题文字</h2>
2. 标题必须在内容的最上方，不能省略
3. 标题文字取自 slide_data.title 字段

---

现在，请生成这页幻灯片的 HTML 代码：
- 只输出 <div>...</div> 内容（不要 <html><head><body>）
- 使用内联样式 style="..."
- 用 SVG 绘制图表（不要用 Chart.js）
- 背景色 {bg}
- 强调色 {accent1}
"""
        
        # Apply user instruction (highest priority)
        if self.instruction:
            prompt += f"""

---

## 【用户自定义指令 — 最高优先级】
以下用户指令**覆盖**上述所有默认规则，必须严格遵守：
{self.instruction}
"""
        
        # Try generation with validation
        for attempt in range(max_retries):
            # Call LLM
            response = await self.llm.generate(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.3,
                timeout=240.0  # 4 minutes timeout for each slide
            )
            
            # Extract content
            content = response.get('content', '')
            
            # If response is wrapped in ```html, extract it
            if '```html' in content:
                content = content.split('```html')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            # Validate
            is_valid, error = validate_html(content)
            
            if is_valid:
                # Enforce minimum font sizes
                content = enforce_minimum_font_sizes(content)
                # Wrap in HTML scaffold
                title = slide_data.get('title', 'Slide')
                html = HTML_SCAFFOLD.format(title=title, content=content)
                return html
            
            # Validation failed, add error to prompt and retry
            print(f"  ⚠️ Validation failed (attempt {attempt + 1}/{max_retries}): {error}")
            
            if attempt < max_retries - 1:
                # Count current text length for context
                text_len = len(re.sub(r'<[^>]+>', '', content).replace(' ', ''))
                prompt += f"""

【⚠️ 严重错误 - 必须修正】
上次生成的 HTML 未通过验证：
- 错误：{error}
- 当前纯文字仅 {text_len} 字符，要求至少 500 字符

【修正要求】：
1. 展开每个要点：每个卡片/要点至少写 2-3 句话的详细说明
2. 写出具体数据：不要只说"增长"，要写"从 X 增长到 Y，增幅 Z%"
3. 填满画布：1920×1080 不应有大片空白
4. 绝对禁止用省略号、等号、重复句子来凑字数
5. 从 slide_data 中提取所有可用内容，不要省略

请重新生成一个内容充实的完整页面。
"""
        
        # All retries failed — check if content is valid HTML before falling back
        if '<div' not in content and '<svg' not in content and '<table' not in content:
            print(f"  ⚠️ LLM returned non-HTML content (thinking/process text), falling back to template mode")
            html = self._fallback_template_html(slide_data)
            if html:
                return html
            # If template fallback also fails, return empty scaffold
            title = slide_data.get('title', 'Slide')
            return HTML_SCAFFOLD.format(title=title, content=f'<div style="padding:80px;"><h2>{title}</h2><p style="color:#999;font-size:24px;">（LLM生成失败，请手动编辑此页）</p></div>')
        
        print(f"  ❌ All {max_retries} attempts failed, returning last result")
        content = enforce_minimum_font_sizes(content)
        title = slide_data.get('title', 'Slide')
        return HTML_SCAFFOLD.format(title=title, content=content)
    
    async def generate_slides_batch(
        self, 
        slides: List[Dict[str, Any]], 
        output_dir: str
    ) -> List[str]:
        """
        Generate HTML for multiple slides.
        
        Args:
            slides: List of slide data
            output_dir: Output directory
        
        Returns:
            List of output file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        html_files = []
        
        for i, slide_data in enumerate(slides, 1):
            title = slide_data.get('title', 'Untitled')
            print(f"Generating slide {i}/{len(slides)}: {title}")
            
            html = await self.generate_slide_html(slide_data)
            
            output_file = output_dir / f"slide_{i:02d}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            html_files.append(str(output_file))
            print(f"  ✓ Saved {output_file.name}")
        
        return html_files

    @staticmethod
    def _fallback_template_html(slide_data: Dict[str, Any]) -> str:
        """
        Fallback: generate a basic HTML slide using template logic when LLM fails.
        Produces a clean, content-filled slide based on slide_data without AI.
        """
        from subprocess import run as _run; import os, json as _json, tempfile

        script_path = os.path.join(os.path.dirname(__file__), 'generate_html.py')
        if not os.path.exists(script_path):
            print("  ⚠️ Template script not found, cannot fallback")
            return None

        title = slide_data.get('title', 'Untitled Slide')
        layout = slide_data.get('layout', slide_data.get('template', slide_data.get('layout_suggestion', 'CONTENT')))
        key_points = slide_data.get('key_points', [])
        data_points = slide_data.get('data_points', slide_data.get('stats', []))

        # Build template data
        tpl_data = {
            'template': layout,
            'title': title,
            'content': key_points,
            'stats': data_points,
            **slide_data
        }

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
                tmp_path = tmp.name

            result = _run(
                ['python3', script_path,
                 '--template', layout,
                 '--output', tmp_path,
                 '--data', _json.dumps(tpl_data, ensure_ascii=False)],
                capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0 and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 200:
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                os.unlink(tmp_path)
                if '<div' in html or '<svg' in html:
                    print(f"  ✓ Template fallback succeeded for: {title}")
                    return html
            else:
                print(f"  ⚠️ Template fallback script failed: {result.stderr[:200] if result.stderr else 'empty output'}")
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        except Exception as e:
            print(f"  ⚠️ Template fallback error: {e}")
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return None


async def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='LLM-based HTML slide generator')
    parser.add_argument('--data', help='Slide data JSON file')
    parser.add_argument('--output', help='Output HTML file')
    parser.add_argument('--from', dest='from_file', help='Outline JSON with multiple slides')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    parser.add_argument('--model', help='LLM model name')
    
    args = parser.parse_args()
    
    # Single slide mode
    if args.data and args.output:
        with open(args.data, 'r', encoding='utf-8') as f:
            slide_data = json.load(f)
        
        generator = LLMHTMLGenerator(model=args.model)
        html = await generator.generate_slide_html(slide_data)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ Generated {args.output}")
    
    # Batch mode
    elif args.from_file and args.output_dir:
        with open(args.from_file, 'r', encoding='utf-8') as f:
            outline = json.load(f)
        
        slides = outline.get('slides', outline.get('slide_structure', []))
        
        generator = LLMHTMLGenerator(model=args.model)
        await generator.generate_slides_batch(slides, args.output_dir)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

