# PDF Generation Fallback (ReportLab)

## When to Use
Use when LibreOffice is unavailable for DOCX→PDF conversion.
Install: `pip install reportlab --break-system-packages`

## Basic PDF with Charts

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register CJK font if available
def register_cjk_font():
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        'C:/Windows/Fonts/simhei.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont('CJK', path))
                return 'CJK'
            except:
                pass
    return 'Helvetica'  # Fallback (no CJK support)

BASE_FONT = register_cjk_font()

# Color definitions
COLOR_PRIMARY = HexColor('#2E86AB')
COLOR_ACCENT  = HexColor('#F18F01')
COLOR_DARK    = HexColor('#1A1A2E')
COLOR_LIGHT   = HexColor('#F0F7FB')
COLOR_TEXT    = HexColor('#333333')

def build_styles():
    styles = getSampleStyleSheet()
    custom = {
        'Title': ParagraphStyle('Title', fontName=BASE_FONT, fontSize=24,
                                 textColor=COLOR_PRIMARY, spaceAfter=12,
                                 alignment=TA_CENTER, leading=30),
        'Subtitle': ParagraphStyle('Subtitle', fontName=BASE_FONT, fontSize=14,
                                    textColor=COLOR_DARK, spaceAfter=6,
                                    alignment=TA_CENTER),
        'H1': ParagraphStyle('H1', fontName=BASE_FONT, fontSize=16,
                              textColor=COLOR_PRIMARY, spaceBefore=16,
                              spaceAfter=8, leading=20),
        'H2': ParagraphStyle('H2', fontName=BASE_FONT, fontSize=13,
                              textColor=COLOR_DARK, spaceBefore=12,
                              spaceAfter=6, leading=16),
        'Body': ParagraphStyle('Body', fontName=BASE_FONT, fontSize=10,
                                textColor=COLOR_TEXT, spaceAfter=6,
                                leading=15, alignment=TA_JUSTIFY),
        'Bullet': ParagraphStyle('Bullet', fontName=BASE_FONT, fontSize=10,
                                  textColor=COLOR_TEXT, spaceAfter=4,
                                  leftIndent=20, bulletIndent=10, leading=14),
        'Caption': ParagraphStyle('Caption', fontName=BASE_FONT, fontSize=8,
                                   textColor=HexColor('#666666'),
                                   alignment=TA_CENTER, spaceAfter=8),
    }
    return custom

# Table style helper
def make_table_style(header_color=COLOR_PRIMARY):
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), BASE_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), BASE_FONT),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_LIGHT, white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ])

# Build complete PDF
def build_pdf(output_path, title, subtitle, sections, chart_paths, stats_data=None):
    """
    sections: list of {'heading': str, 'body': str, 'chart': str or None}
    chart_paths: dict of section_name -> image_path
    stats_data: {'headers': [...], 'rows': [[...]]} for appendix table
    """
    styles = build_styles()
    story = []
    
    # Cover page
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph(title, styles['Title']))
    story.append(Paragraph(subtitle, styles['Subtitle']))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width='80%', thickness=2, color=COLOR_PRIMARY))
    story.append(PageBreak())
    
    # Body sections
    for sec in sections:
        story.append(Paragraph(sec['heading'], styles['H1']))
        story.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#CCCCCC')))
        story.append(Spacer(1, 4*mm))
        
        for para in sec['body'].split('\n\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), styles['Body']))
        
        if sec.get('chart') and os.path.exists(sec['chart']):
            story.append(Spacer(1, 4*mm))
            img = Image(sec['chart'], width=14*cm, height=8*cm)
            story.append(img)
            story.append(Paragraph(sec.get('caption', ''), styles['Caption']))
        
        story.append(Spacer(1, 6*mm))
    
    # Appendix: stats table
    if stats_data:
        story.append(PageBreak())
        story.append(Paragraph('附录：数据统计 / Appendix: Statistics', styles['H1']))
        table_data = [stats_data['headers']] + stats_data['rows']
        t = Table(table_data, repeatRows=1)
        t.setStyle(make_table_style())
        story.append(t)
    
    # Build
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2*cm)
    doc.build(story)
    print(f"✓ PDF saved: {output_path}")
```

## Usage Example

```python
build_pdf(
    output_path='/home/claude/report.pdf',
    title='Sales Analysis Report',
    subtitle='January 2025 | Auto-generated',
    sections=[
        {
            'heading': 'Executive Summary',
            'body': 'Total revenue grew 23% month-over-month...\n\nTop category: Electronics contributed 45% of revenue.',
            'chart': 'chart_trend.png',
            'caption': 'Figure 1: Monthly Revenue Trend'
        },
        {
            'heading': 'Category Performance',
            'body': 'Electronics led with $2.3M, followed by Apparel at $1.1M...',
            'chart': 'chart_top10.png',
            'caption': 'Figure 2: Top 10 Categories by Revenue'
        },
    ],
    stats_data={
        'headers': ['Metric', 'Revenue', 'Orders', 'AOV'],
        'rows': [
            ['Mean', '12,450', '234', '53.2'],
            ['Median', '11,200', '198', '51.8'],
            ['Std Dev', '3,200', '67', '12.1'],
        ]
    }
)
```
