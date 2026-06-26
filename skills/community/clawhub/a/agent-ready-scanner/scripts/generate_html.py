#!/usr/bin/env python3
"""
将 JSON 报告转换为 HTML
"""

import argparse
import json
import re
from pathlib import Path


def generate_html(report_json: dict, template_path: str) -> str:
    """生成 HTML 报告"""
    
    # 读取模板
    template = Path(template_path).read_text(encoding='utf-8')
    
    # 计算百分比和颜色
    total = report_json['total_score']
    max_score = report_json['max_score']
    percentage = int((total / max_score) * 100) if max_score > 0 else 0
    
    # 圆环进度: dash_offset = 377 * (1 - percentage/100)
    dash_offset = 377 * (1 - percentage / 100)
    
    # 颜色
    if percentage >= 80:
        score_color = '#10b981'
    elif percentage >= 50:
        score_color = '#f59e0b'
    else:
        score_color = '#ef4444'
    
    # 图标映射
    icon_map = {'pass': '✓', 'warning': '⚠', 'fail': '✗'}
    
    # 构建类别 HTML
    categories_html = []
    for cat_name, cat_data in report_json['categories'].items():
        checks_html = []
        for i, check in enumerate(cat_data['checks']):
            status = check['status']
            icon = icon_map.get(status, '?')
            
            # 详情
            has_details = bool(check.get('details'))
            details_json = json.dumps(check.get('details', {}), ensure_ascii=False, indent=2) if has_details else ''
            
            # 修复建议
            fix_suggestion = check.get('fix_suggestion', '')
            
            check_html = f'''
            <div class="check">
                <div class="check-header">
                    <span class="check-icon {status}">{icon}</span>
                    <span class="check-name">{check['name']}</span>
                </div>
                <div class="check-message">{check['message']}</div>'''
            
            if has_details:
                check_html += f'''
                <div class="check-details">
                    <pre>{details_json}</pre>
                </div>'''
            
            if fix_suggestion:
                check_id = f"{cat_name}-{check['name']}-{i}".replace(' ', '-').lower()
                check_html += f'''
                <div class="fix-suggestion">
                    <h4>💡 修复建议</h4>
                    <pre id="fix-{check_id}">{fix_suggestion}</pre>
                    <button class="copy-btn" onclick="copyFix('fix-{check_id}', this)">📋 复制</button>
                </div>'''
            
            check_html += '\n            </div>'
            checks_html.append(check_html)
        
        cat_html = f'''
        <div class="category">
            <div class="category-header">
                <h2>{cat_name}</h2>
                <span class="category-score">{cat_data['score']}/{cat_data['max_score']}</span>
            </div>
            {''.join(checks_html)}
        </div>'''
        
        categories_html.append(cat_html)
    
    # 替换模板变量
    html = template
    html = html.replace('{{url}}', report_json['url'])
    html = html.replace('{{timestamp}}', report_json['timestamp'])
    html = html.replace('{{total_score}}', str(total))
    html = html.replace('{{max_score}}', str(max_score))
    html = html.replace('{{percentage}}', str(percentage))
    html = html.replace('{{dash_offset}}', str(dash_offset))
    html = html.replace('{{score_color}}', score_color)
    html = html.replace('{{summary}}', report_json['summary'])
    
    # 处理 {{#categories}}...{{/categories}} 块
    # 找到块并替换
    pattern = r'\{\{#categories\}\}.*?\{\{/categories\}\}'
    html = re.sub(pattern, ''.join(categories_html), html, flags=re.DOTALL)
    
    return html


def main():
    parser = argparse.ArgumentParser(description="生成 HTML 报告")
    parser.add_argument("json_file", help="JSON 报告文件")
    parser.add_argument("--template", default=None, help="HTML 模板路径")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 文件路径")
    
    args = parser.parse_args()
    
    # 读取 JSON
    with open(args.json_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # 模板路径
    if args.template:
        template_path = args.template
    else:
        # 默认模板位置
        template_path = Path(__file__).parent.parent / 'assets' / 'report_template.html'
    
    # 生成 HTML
    html = generate_html(report, template_path)
    
    # 写入输出
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"✅ HTML 报告已生成: {args.output}")


if __name__ == "__main__":
    main()
