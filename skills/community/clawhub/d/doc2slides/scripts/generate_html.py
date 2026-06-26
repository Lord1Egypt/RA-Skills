#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

"""
Enhanced HTML Slide Generator with template support.
Generates consulting-style HTML slides from JSON data.

Usage:
  python generate_html.py --template <type> --output <file.html> --data <json>
  python generate_html.py --from slides.json --output-dir slides/
"""

import sys
import json
import argparse
import os
from pathlib import Path
from datetime import datetime

TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"


def load_template(template_name: str) -> str:
    """Load HTML template file."""
    template_path = TEMPLATES_DIR / f"{template_name.lower()}.html"
    if not template_path.exists():
        print(f"Warning: Template {template_name} not found, using CONTENT")
        template_path = TEMPLATES_DIR / "content.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def apply_style_to_html(html: str, style: dict) -> str:
    """Apply custom style to HTML template."""
    if not style or 'colors' not in style:
        return html
    
    colors = style.get('colors', {})
    
    # Replace default colors with user colors
    if colors.get('primary'):
        html = html.replace('#0f172a', f'#{colors["primary"]}')
    if colors.get('secondary'):
        html = html.replace('#1e293b', f'#{colors["secondary"]}')
    
    # Replace accent colors
    accent_colors = colors.get('accents', [])
    default_accents = ['#dc2626', '#ea580c', '#d97706', '#059669']
    for i, accent in enumerate(accent_colors[:4]):
        if i < len(default_accents):
            html = html.replace(default_accents[i], f'#{accent}')
    
    return html


def render_cover(data: dict) -> str:
    """Render COVER slide."""
    template = load_template('cover')
    html = template.replace('{{EYEBROW}}', data.get('eyebrow', 'PRESENTATION')) \
                   .replace('{{TITLE}}', data.get('title', 'Title')) \
                   .replace('{{SUBTITLE}}', data.get('subtitle', '')) \
                   .replace('{{AUTHOR}}', data.get('author', '')) \
                   .replace('{{DATE}}', data.get('date', datetime.now().strftime('%Y年%m月')))
    
    # Apply custom style
    if 'style' in data:
        html = apply_style_to_html(html, data['style'])
    
    return html


def render_problem(data: dict) -> str:
    """Render PROBLEM slide with enhanced stats visualization."""
    template = load_template('problem')
    
    # Support both 'description'/'insight' and 'key_points' fields
    key_points = data.get('key_points', [])
    description = data.get('description', '')
    insight = data.get('insight', '')
    
    # Generate key points HTML (left side)
    key_points_html = ""
    for i, point in enumerate(key_points[:5], 1):
        icon = ['🔹', '📈', '🎯', '💡', '✨'][min(i-1, 4)]
        key_points_html += f'''
        <div class="flex items-start gap-3 bg-slate-50 rounded-lg px-4 py-3 border-l-4 border-navy-800">
          <span class="text-lg">{icon}</span>
          <span class="text-base text-navy-800 leading-snug">{point}</span>
        </div>
        '''
    
    # If no key_points, use description
    if not key_points_html:
        key_points_html = f'<div class="text-lg text-slate-600">{description}</div>'
    
    # Generate stats cards HTML (right side)
    # Support both 'stats' and 'data_points' field names
    stats = data.get('stats', data.get('data_points', []))
    
    color_map = {
        'red': ('bg-red-500', 'text-red-600'),
        'orange': ('bg-orange-500', 'text-orange-500'),
        'amber': ('bg-amber-500', 'text-amber-500'),
        'green': ('bg-emerald-500', 'text-emerald-500'),
        'blue': ('bg-blue-500', 'text-blue-500')
    }
    
    stats_cards_html = ""
    for i, stat in enumerate(stats[:4], 1):
        value = stat.get('value', 0)
        unit = stat.get('unit', '%')
        label = stat.get('label', f'指标{i}')
        color_name = stat.get('color', list(color_map.keys())[(i-1) % len(color_map)])
        bg_class, text_class = color_map.get(color_name, color_map['red'])
        
        # Extract numeric value from string (e.g., "近100" -> 100)
        import re
        if isinstance(value, str):
            numeric_match = re.search(r'[\d.]+', value)
            numeric_value = float(numeric_match.group()) if numeric_match else 0
        else:
            numeric_value = float(value) if value else 0
        
        # Handle different units
        if unit in ['万亿$', '万亿', '亿']:
            display_value = f"{value}{unit}"
            bar_width = min(numeric_value * 10, 100)  # Scale for visualization
        elif unit == '+':
            display_value = f"{value}+"
            bar_width = min(numeric_value, 100)
        elif unit == '%':
            display_value = f"{value}%"
            bar_width = numeric_value
        elif unit == '万+':
            display_value = f"{value}万+"
            bar_width = min(numeric_value / 50, 100)
        else:
            display_value = f"{value}{unit}"
            bar_width = min(numeric_value, 100)
        
        stats_cards_html += f'''
        <div class="bg-slate-50 rounded-xl p-5 border border-slate-100">
          <div class="flex items-baseline gap-1 mb-2">
            <span class="text-4xl font-black {text_class}">{display_value}</span>
          </div>
          <div class="text-sm font-medium text-slate-600 mb-3">{label}</div>
          <div class="h-2 bg-slate-200 rounded-full overflow-hidden">
            <div class="h-full {bg_class} rounded-full stat-bar" style="width: {bar_width}%"></div>
          </div>
        </div>
        '''
    
    # If no stats, show placeholder
    if not stats_cards_html:
        stats_cards_html = '''
        <div class="col-span-2 text-center text-slate-400 py-12">
          暂无关键数据
        </div>
        '''
    
    # Generate SVG chart data
    chart_labels = []
    chart_values = []
    for stat in stats:
        value = stat.get('value', 0)
        unit = stat.get('unit', '')
        label = stat.get('label', '指标')
        
        # Extract numeric value from string (e.g., "近100" -> 100)
        if isinstance(value, str):
            numeric_match = re.search(r'[\d.]+', value)
            numeric_value = float(numeric_match.group()) if numeric_match else 0
        else:
            numeric_value = float(value) if value else 0
        
        # Extract numeric value for chart
        if unit in ['万亿$', '万亿', '亿']:
            chart_values.append(numeric_value)
        elif unit == '+':
            chart_values.append(numeric_value)
        elif unit == '%':
            chart_values.append(numeric_value)
        elif unit == '万+':
            chart_values.append(numeric_value / 10)  # Scale down
        else:
            chart_values.append(numeric_value if numeric_value else 0)
        
        chart_labels.append(label[:10])  # Truncate label
    
    chart_labels_json = json.dumps(chart_labels, ensure_ascii=False)
    chart_values_json = json.dumps(chart_values)
    
    # Determine insight
    if not insight and len(key_points) > 2:
        insight = key_points[-1]
    
    return template.replace('{{EYEBROW}}', data.get('eyebrow', 'Analysis')) \
                   .replace('{{TITLE}}', data.get('title', 'Key Finding')) \
                   .replace('{{KEY_POINTS}}', key_points_html) \
                   .replace('{{INSIGHT}}', insight or '暂无关键洞察') \
                   .replace('{{CHART_LABELS}}', chart_labels_json) \
                   .replace('{{CHART_VALUES}}', chart_values_json)


def render_solution(data: dict) -> str:
    """Render SOLUTION slide with enhanced step cards."""
    template = load_template('solution')
    
    # Support both 'steps' and 'key_points' fields
    steps = data.get('steps', [])
    key_points = data.get('key_points', [])
    
    # If no steps but has key_points, convert key_points to steps
    if not steps and key_points:
        steps = []
        for i, kp in enumerate(key_points, 1):
            # Try to split by ':' or '：' to get title and detail
            if '：' in kp:
                title, detail = kp.split('：', 1)
            elif ':' in kp:
                title, detail = kp.split(':', 1)
            else:
                title, detail = kp[:15], '' if len(kp) <= 15 else kp[15:]
            
            steps.append({
                "number": f"{i:02d}",
                "title": title.strip()[:12],
                "detail": detail.strip()[:40] if detail else ''
            })
    
    if not steps:
        steps = [
            {"number": "01", "title": "分析", "detail": "深入分析现状"},
            {"number": "02", "title": "设计", "detail": "制定解决方案"},
            {"number": "03", "title": "实施", "detail": "分阶段推进"},
            {"number": "04", "title": "验证", "detail": "测试与优化"}
        ]
    
    step_colors = [
        ('bg-navy-900', 'border-slate-700'),
        ('bg-navy-800', 'border-slate-600'),
        ('bg-emerald-700', 'border-emerald-500'),
        ('bg-emerald-600', 'border-emerald-400')
    ]
    
    steps_html = ""
    for i, step in enumerate(steps[:4]):
        bg_class, border_class = step_colors[i % len(step_colors)]
        steps_html += f'''
        <div class="{bg_class} text-white rounded-xl p-6 border-l-4 {border_class}">
          <div class="text-xs font-bold text-slate-400 mb-2">STEP {step["number"]}</div>
          <div class="text-xl font-bold mb-3">{step["title"]}</div>
          <div class="text-sm text-slate-300 leading-relaxed">{step["detail"]}</div>
        </div>
        '''
    
    # Generate benefits HTML
    benefits = data.get('benefits', [])
    if not benefits:
        # Extract from key_points if available
        if len(key_points) > 4:
            benefits = [
                {"number": "1", "title": "核心价值", "detail": key_points[4] if len(key_points) > 4 else ""},
            ]
        else:
            benefits = [
                {"number": "✓", "title": "可落地", "detail": "方案成熟"},
                {"number": "✓", "title": "见效快", "detail": "周期短"},
                {"number": "✓", "title": "风险低", "detail": "经验丰富"}
            ]
    
    benefits_html = ""
    for benefit in benefits[:3]:
        benefits_html += f'''
      <div class="flex items-center gap-3 bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
        <div class="w-8 h-8 bg-emerald-500 rounded-full flex items-center justify-center text-white font-bold">{benefit["number"]}</div>
        <div>
          <div class="font-bold text-emerald-800">{benefit["title"]}</div>
          <div class="text-sm text-emerald-600">{benefit["detail"]}</div>
        </div>
      </div>
      '''
    
    return template.replace('{{EYEBROW}}', data.get('eyebrow', 'Solution')) \
                   .replace('{{TITLE}}', data.get('title', 'Implementation Path')) \
                   .replace('{{STEPS}}', steps_html) \
                   .replace('{{BENEFITS}}', benefits_html)


def render_matrix(data: dict) -> str:
    """Render MATRIX slide (2x2 strategic matrix)."""
    template = load_template('matrix')
    
    # Support both 'Q1/Q2/Q3/Q4' dict format and 'quadrants' array format
    position_map = {
        'top-left': 'Q1',
        'top-right': 'Q2', 
        'bottom-left': 'Q3',
        'bottom-right': 'Q4'
    }
    
    defaults = {
        'Q1': {'priority': '高优先级', 'title': '快速行动', 'content': '高价值、易执行'},
        'Q2': {'priority': '中优先级', 'title': '计划推进', 'content': '高价值、需投入'},
        'Q3': {'priority': '低优先级', 'title': '可选优化', 'content': '低价值、易执行'},
        'Q4': {'priority': '暂缓', 'title': '避免投入', 'content': '低价值、难执行'}
    }
    
    # Convert quadrants array to Q1/Q2/Q3/Q4 format
    quadrants = data.get('quadrants', [])
    if quadrants:
        for q in quadrants:
            pos = q.get('position', '')
            q_key = position_map.get(pos)
            if q_key:
                points = q.get('points', [])
                content = '<br>'.join(points) if points else q.get('content', '')
                data[q_key] = {
                    'priority': q.get('priority', defaults[q_key]['priority']),
                    'title': q.get('title', defaults[q_key]['title']),
                    'content': content
                }
    
    replacements = {
        '{{EYEBROW}}': data.get('eyebrow', 'Strategic Matrix'),
        '{{TITLE}}': data.get('title', 'Priority Matrix')
    }
    
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        q_data = data.get(q, {})
        default = defaults[q]
        replacements[f'{{{{{q}_PRIORITY}}}}'] = q_data.get('priority', default['priority'])
        replacements[f'{{{{{q}_TITLE}}}}'] = q_data.get('title', default['title'])
        replacements[f'{{{{{q}_CONTENT}}}}'] = q_data.get('content', default['content'])
    
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return result


def render_compare(data: dict) -> str:
    """Render COMPARE slide (Do/Don't)."""
    template = load_template('compare')
    
    # Generate Do items
    do_items = data.get('do', [])
    if not do_items:
        do_items = ['建议行动一', '建议行动二', '建议行动三']
    
    do_html = ""
    for item in do_items:
        do_html += f'''<div class="bg-emerald-50 border border-emerald-200 rounded-lg px-5 py-4 text-emerald-800">✓ {item}</div>\n'''
    
    # Generate Don't items
    dont_items = data.get('dont', [])
    if not dont_items:
        dont_items = ['避免行动一', '避免行动二', '避免行动三']
    
    dont_html = ""
    for item in dont_items:
        dont_html += f'''<div class="bg-red-50 border border-red-200 rounded-lg px-5 py-4 text-red-800">✗ {item}</div>\n'''
    
    return template.replace('{{EYEBROW}}', data.get('eyebrow', 'Comparison')) \
                   .replace('{{TITLE}}', data.get('title', 'Do / Don\'t')) \
                   .replace('{{DO_TITLE}}', data.get('do_title', '建议')) \
                   .replace('{{DONT_TITLE}}', data.get('dont_title', '避免')) \
                   .replace('{{DO_ITEMS}}', do_html) \
                   .replace('{{DONT_ITEMS}}', dont_html)


def render_content(data: dict) -> str:
    """Render CONTENT slide with enhanced layout."""
    template = load_template('content')
    
    # Support both 'content' and 'key_points' fields
    content_items = data.get('content', []) or data.get('key_points', [])
    if isinstance(content_items, str):
        content_items = [content_items]
    
    # Generate content HTML with better layout
    content_html = ""
    
    # Determine layout based on number of items
    num_items = len(content_items)
    
    if num_items <= 3:
        # Single column layout
        col_span = 12
        for i, item in enumerate(content_items, 1):
            icon = ['01', '02', '03', '04', '05'][min(i-1, 4)]
            content_html += f'''
          <div class="col-span-{col_span} flex items-start gap-6 bg-gradient-to-r from-slate-50 to-white rounded-xl p-6 border border-slate-100">
            <div class="w-14 h-14 bg-navy-900 rounded-xl flex items-center justify-center text-white text-xl font-bold flex-shrink-0">{icon}</div>
            <div class="flex-1">
              <div class="text-xl font-bold text-navy-900 leading-relaxed">{item}</div>
            </div>
          </div>
            '''
    else:
        # Two column layout for 4+ items
        for i, item in enumerate(content_items[:6], 1):
            icon = ['01', '02', '03', '04', '05', '06'][i-1]
            col_span = 6 if i <= 4 else 12
            content_html += f'''
          <div class="col-span-{col_span} flex items-start gap-4 bg-gradient-to-r from-slate-50 to-white rounded-xl p-5 border border-slate-100">
            <div class="w-12 h-12 bg-navy-900 rounded-xl flex items-center justify-center text-white text-lg font-bold flex-shrink-0">{icon}</div>
            <div class="flex-1">
              <div class="text-lg font-medium text-navy-800 leading-relaxed">{item}</div>
            </div>
          </div>
            '''
    
    return template.replace('{{EYEBROW}}', data.get('eyebrow', '')) \
                   .replace('{{TITLE}}', data.get('title', 'Content')) \
                   .replace('{{CONTENT}}', content_html)


def render_closing(data: dict) -> str:
    """Render CLOSING slide."""
    template = load_template('closing')
    return template.replace('{{TITLE}}', data.get('title', 'Thank You')) \
                   .replace('{{CTA}}', data.get('cta', 'Let\'s Connect')) \
                   .replace('{{CONTACT_NAME}}', data.get('contact_name', '')) \
                   .replace('{{CONTACT_EMAIL}}', data.get('contact_email', ''))


def render_slide(template_type: str, data: dict) -> str:
    """Route to appropriate renderer based on template type."""
    renderers = {
        'COVER': render_cover,
        'PROBLEM': render_problem,
        'SOLUTION': render_solution,
        'MATRIX': render_matrix,
        'COMPARE': render_compare,
        'CONTENT': render_content,
        'CLOSING': render_closing
    }
    
    # Map layout_suggestion to template types
    layout_map = {
        'cover': 'COVER',
        'dashboard': 'PROBLEM',  # Dashboard uses PROBLEM template (has charts)
        'big_number': 'PROBLEM',  # Big numbers use PROBLEM template
        'comparison': 'COMPARE',
        'card': 'CONTENT',
        'pyramid': 'SOLUTION',
        'action_plan': 'SOLUTION',
        'summary': 'CONTENT',
        'timeline': 'SOLUTION'
    }
    
    # Normalize template type
    template_upper = template_type.upper()
    
    # Check if it's a layout_suggestion that needs mapping
    if template_upper not in renderers:
        template_upper = layout_map.get(template_type.lower(), 'CONTENT')
    
    renderer = renderers.get(template_upper, render_content)
    return renderer(data)


def main():
    parser = argparse.ArgumentParser(description='Generate HTML slides')
    parser.add_argument('--template', help='Template type (COVER/PROBLEM/SOLUTION/MATRIX/COMPARE/CONTENT/CLOSING)')
    parser.add_argument('--output', help='Output HTML file')
    parser.add_argument('--data', help='JSON data for slide')
    parser.add_argument('--from', dest='from_file', help='Input JSON file with multiple slides')
    parser.add_argument('--output-dir', help='Output directory for multiple slides')
    
    args = parser.parse_args()
    
    # Single slide mode
    if args.template and args.output:
        if args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON data")
                sys.exit(1)
        else:
            data = {}
        
        html = render_slide(args.template, data)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ Generated {args.output}")
    
    # Multiple slides mode
    elif args.from_file and args.output_dir:
        with open(args.from_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        slides = content.get('slides', [])
        if not slides:
            print("Error: No slides found in input file")
            sys.exit(1)
        
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, slide in enumerate(slides, 1):
            # Use layout_suggestion if available, otherwise template
            template_type = slide.get('layout_suggestion', slide.get('template', 'CONTENT'))
            html = render_slide(template_type, slide)
            
            output_file = output_dir / f"slide_{i:02d}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"✓ Generated {output_file.name}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
