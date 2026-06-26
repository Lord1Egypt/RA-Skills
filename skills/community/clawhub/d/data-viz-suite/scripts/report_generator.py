"""
Report Generator - 报表生成器
支持 PDF、HTML、Excel 导出
"""

from typing import List, Optional, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os


class ReportGenerator:
    """报表生成器"""
    
    def __init__(self, title: str = '数据报表'):
        self.title = title
        self.sections: List[Dict] = []
        
        # 尝试注册中文字体
        self._register_fonts()
    
    def _register_fonts(self):
        """注册字体"""
        try:
            # 尝试常见中文字体
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/System/Library/Fonts/PingFang.ttc',
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    self.chinese_font = 'ChineseFont'
                    return
        except Exception:
            pass
        self.chinese_font = 'Helvetica'
    
    def add_section(self, title: str, charts: Optional[List] = None,
                   text: str = '', dataframe: Optional[pd.DataFrame] = None):
        """添加章节"""
        self.sections.append({
            'title': title,
            'charts': charts or [],
            'text': text,
            'dataframe': dataframe
        })
    
    def add_table(self, title: str, dataframe: pd.DataFrame):
        """添加表格章节"""
        self.add_section(title, dataframe=dataframe)
    
    def _export_pdf(self, path: str):
        """导出PDF"""
        doc = SimpleDocTemplate(path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # 标题
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName=self.chinese_font,
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph(self.title, title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # 章节
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontName=self.chinese_font,
            fontSize=16
        )
        
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['BodyText'],
            fontName=self.chinese_font,
            fontSize=10
        )
        
        for section in self.sections:
            story.append(Paragraph(section['title'], section_style))
            story.append(Spacer(1, 0.1 * inch))
            
            if section['text']:
                story.append(Paragraph(section['text'], body_style))
                story.append(Spacer(1, 0.1 * inch))
            
            if section['dataframe'] is not None:
                df = section['dataframe'].head(20)  # 最多20行
                data = [df.columns.tolist()] + df.values.tolist()
                table = Table(data)
                story.append(table)
                story.append(Spacer(1, 0.2 * inch))
        
        doc.build(story)
        print(f"PDF 报表已保存: {path}")
    
    def _export_html(self, path: str):
        """导出HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>{self.title}</h1>
"""
        for section in self.sections:
            html += f"    <h2>{section['title']}</h2>\n"
            if section['text']:
                html += f"    <p>{section['text']}</p>\n"
            if section['dataframe'] is not None:
                html += section['dataframe'].head(50).to_html(index=False)
        
        html += "</body>\n</html>"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML 报表已保存: {path}")
    
    def _export_excel(self, path: str):
        """导出Excel"""
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            for i, section in enumerate(self.sections):
                if section['dataframe'] is not None:
                    sheet_name = section['title'][:31]  # Excel sheet name limit
                    section['dataframe'].to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Excel 报表已保存: {path}")
    
    def export(self, path: str):
        """导出报表"""
        if path.endswith('.pdf'):
            self._export_pdf(path)
        elif path.endswith('.html'):
            self._export_html(path)
        elif path.endswith(('.xlsx', '.xls')):
            self._export_excel(path)
        else:
            # 默认导出HTML
            self._export_html(path + '.html')


if __name__ == '__main__':
    import pandas as pd
    
    report = ReportGenerator('销售报表')
    
    df = pd.DataFrame({
        '产品': ['A', 'B', 'C'],
        '销量': [100, 200, 150],
        '金额': [1000, 4000, 3000]
    })
    
    report.add_section('概览', text='本季度销售情况良好')
    report.add_table('销售明细', df)
    
    report.export('test_report.html')
