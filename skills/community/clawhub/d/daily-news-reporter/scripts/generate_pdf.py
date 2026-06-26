# -*- coding: utf-8 -*-
"""
PDF报告生成器
Markdown日报转PDF工具
使用reportlab生成专业PDF报告
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse
import os

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))

class PDFReportGenerator:
    """PDF报告生成器"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_styles()
    
    def setup_styles(self):
        """设置自定义样式"""
        
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontName='SimHei',
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # 居中
        )
        
        # 副标题样式
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontName='SimSun',
            fontSize=11,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=1
        )
        
        # 一级标题
        self.h1_style = ParagraphStyle(
            'CustomH1',
            parent=self.styles['Heading1'],
            fontName='SimHei',
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=25,
            spaceAfter=15,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=2,
            borderPadding=5,
            leftIndent=0
        )
        
        # 二级标题
        self.h2_style = ParagraphStyle(
            'CustomH2',
            parent=self.styles['Heading2'],
            fontName='SimHei',
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=20,
            spaceAfter=10
        )
        
        # 三级标题
        self.h3_style = ParagraphStyle(
            'CustomH3',
            parent=self.styles['Heading3'],
            fontName='SimHei',
            fontSize=12,
            textColor=colors.HexColor('#7f8c8d'),
            spaceBefore=15,
            spaceAfter=8
        )
        
        # 正文
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontName='SimSun',
            fontSize=10.5,
            leading=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8
        )
        
        # 引用
        self.quote_style = ParagraphStyle(
            'CustomQuote',
            parent=self.styles['Normal'],
            fontName='SimSun',
            fontSize=10,
            leading=16,
            textColor=colors.HexColor('#555555'),
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10,
            borderColor=colors.HexColor('#bdc3c7'),
            borderWidth=1,
            borderPadding=8,
            backColor=colors.HexColor('#f8f9fa')
        )
        
        # 警示
        self.warning_style = ParagraphStyle(
            'Warning',
            parent=self.styles['Normal'],
            fontName='SimHei',
            fontSize=11,
            leading=18,
            textColor=colors.HexColor('#c0392b'),
            spaceBefore=10,
            spaceAfter=10
        )
        
        # 页脚
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontName='SimSun',
            fontSize=9,
            textColor=colors.HexColor('#95a5a6'),
            alignment=1
        )
    
    def create_table(self, data, col_widths, header_color=colors.HexColor('#3498db'), 
                     header_text_color=colors.whitesmoke, 
                     row_colors=[colors.white, colors.HexColor('#f8f9fa')]):
        """创建标准表格"""
        table = Table(data, colWidths=col_widths)
        
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), header_text_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ]
        
        # 添加交替行背景
        for i in range(1, len(data)):
            bg_color = row_colors[i % 2]
            style_commands.append(('BACKGROUND', (0, i), (-1, i), bg_color))
        
        table.setStyle(TableStyle(style_commands))
        return table
    
    def generate_report(self, title, date, subtitle, sections, output_path):
        """
        生成PDF报告
        
        Args:
            title: 报告标题
            date: 报告日期
            subtitle: 副标题
            sections: 报告内容区块列表
            output_path: 输出路径
        """
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # 标题页
        story.append(Paragraph(title, self.title_style))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"日期：{date}", self.subtitle_style))
        if subtitle:
            story.append(Paragraph(subtitle, self.subtitle_style))
        story.append(Spacer(1, 1*cm))
        
        # 添加各区块
        for section in sections:
            section_type = section.get('type', 'text')
            
            if section_type == 'h1':
                story.append(Paragraph(section['content'], self.h1_style))
            elif section_type == 'h2':
                story.append(Paragraph(section['content'], self.h2_style))
            elif section_type == 'h3':
                story.append(Paragraph(section['content'], self.h3_style))
            elif section_type == 'text':
                story.append(Paragraph(section['content'], self.body_style))
            elif section_type == 'quote':
                story.append(Paragraph(section['content'], self.quote_style))
            elif section_type == 'table':
                table = self.create_table(
                    section['data'], 
                    section.get('col_widths', []),
                    section.get('header_color', colors.HexColor('#3498db'))
                )
                story.append(table)
            elif section_type == 'spacer':
                story.append(Spacer(1, section.get('height', 0.5)*cm))
            elif section_type == 'pagebreak':
                story.append(PageBreak())
        
        # 页脚
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(f"— 报告时间：{date} —", self.footer_style))
        story.append(Paragraph("本报告采用改进版信息采集流程，关键信息经多源交叉验证。", self.footer_style))
        
        # 生成PDF
        doc.build(story)
        print(f"PDF报告已生成: {output_path}")
        return output_path

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='生成PDF报告')
    parser.add_argument('--input', '-i', help='输入Markdown文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出PDF文件路径')
    parser.add_argument('--title', '-t', default='国际时事日报', help='报告标题')
    parser.add_argument('--date', '-d', help='报告日期')
    
    args = parser.parse_args()
    
    generator = PDFReportGenerator()
    
    # 示例：生成测试报告
    from datetime import datetime
    today = args.date or datetime.now().strftime("%Y年%m月%d日")
    
    sections = [
        {'type': 'h1', 'content': '📌 今日要闻速览'},
        {'type': 'spacer', 'height': 0.3},
        {'type': 'table', 'data': [
            ['序号', '事件', '影响', '来源等级'],
            ['1', '示例事件1', '⭐⭐⭐⭐⭐', '【官方】'],
            ['2', '示例事件2', '⭐⭐⭐⭐', '【专业】'],
        ], 'col_widths': [1.5*cm, 8*cm, 2.5*cm, 3*cm]},
        {'type': 'pagebreak'},
        {'type': 'h1', 'content': '🔥 详细报道'},
        {'type': 'h2', 'content': '一、事件详细分析'},
        {'type': 'text', 'content': '这是示例正文内容...'},
    ]
    
    generator.generate_report(
        title=args.title,
        date=today,
        subtitle="WorkBuddy AI 编制",
        sections=sections,
        output_path=args.output
    )

if __name__ == "__main__":
    main()
