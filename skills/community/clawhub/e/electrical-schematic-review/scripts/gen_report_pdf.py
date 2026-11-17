#!/usr/bin/env python3
"""
电气原理图审图报告PDF生成器
从审图结果数据生成格式化的PDF报告。

Usage:
    python gen_report_pdf.py --input=review_results.json --output=report.pdf
    python gen_report_pdf.py --input=review_results.json --output=report.pdf --title="XX项目审图报告"
"""
import argparse
import json
import os
import sys
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab required. Install: pip install reportlab")
    sys.exit(1)


# 严重程度颜色
SEVERITY_COLORS = {
    'critical': '#FF0000',  # 红色
    'major': '#FF6600',     # 橙色
    'minor': '#FFCC00',     # 黄色
    'info': '#0066CC',      # 蓝色
}


def register_chinese_font():
    """注册中文字体"""
    font_paths = [
        'C:\\Windows\\Fonts\\msyh.ttc',  # 微软雅黑
        'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', fp))
                return 'ChineseFont'
            except Exception:
                continue
    return 'Helvetica'


def generate_report(input_file, output_file, title=None):
    """生成PDF审图报告"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    font_name = register_chinese_font()
    
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=25*mm,
        bottomMargin=20*mm,
    )
    
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'ChineseTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=18,
        spaceAfter=12,
    )
    
    heading_style = ParagraphStyle(
        'ChineseHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        spaceAfter=8,
        textColor=HexColor('#0066CC'),
    )
    
    body_style = ParagraphStyle(
        'ChineseBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
    )
    
    story = []
    
    # 标题
    report_title = title or data.get('project_name', '电气审图报告')
    story.append(Paragraph(report_title, title_style))
    story.append(Paragraph(f"生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style))
    story.append(Spacer(1, 10*mm))
    
    # 项目信息
    story.append(Paragraph('项目信息', heading_style))
    project_info = data.get('project_info', {})
    info_data = [[k, str(v)] for k, v in project_info.items()]
    if info_data:
        info_table = Table(info_data, colWidths=[40*mm, 120*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#F0F0F0')),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 8*mm))
    
    # 审图结果汇总
    story.append(Paragraph('审图结果汇总', heading_style))
    issues = data.get('issues', [])
    
    summary = {'critical': 0, 'major': 0, 'minor': 0, 'info': 0}
    for issue in issues:
        sev = issue.get('severity', 'info')
        summary[sev] = summary.get(sev, 0) + 1
    
    summary_data = [['严重程度', '数量']]
    for sev, count in summary.items():
        summary_data.append([sev.upper(), str(count)])
    summary_data.append(['总计', str(len(issues))])
    
    summary_table = Table(summary_data, colWidths=[40*mm, 30*mm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), font_name),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8*mm))
    
    # 详细问题列表
    if issues:
        story.append(Paragraph('详细问题列表', heading_style))
        
        detail_data = [['序号', '模块', '严重程度', '问题描述', '建议']]
        for idx, issue in enumerate(issues, 1):
            detail_data.append([
                str(idx),
                issue.get('module', ''),
                issue.get('severity', ''),
                issue.get('description', '')[:80],
                issue.get('suggestion', '')[:60],
            ])
        
        detail_table = Table(detail_data, colWidths=[10*mm, 25*mm, 20*mm, 55*mm, 50*mm])
        detail_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0066CC')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(detail_table)
    
    doc.build(story)
    print(f"Report generated: {output_file}")
    print(f"Total issues: {len(issues)}")


def main():
    parser = argparse.ArgumentParser(description='电气审图报告PDF生成')
    parser.add_argument('--input', required=True, help='审图结果JSON文件')
    parser.add_argument('--output', default='review_report.pdf', help='输出PDF文件')
    parser.add_argument('--title', help='报告标题')
    
    args = parser.parse_args()
    generate_report(args.input, args.output, args.title)


if __name__ == '__main__':
    main()
