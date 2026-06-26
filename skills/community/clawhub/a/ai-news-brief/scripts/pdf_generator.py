#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 报告生成模块 - FPDF2 版本
支持中文，样式更智能
"""

import os
import sys

# 尝试导入 fpdf2
try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
    FPDF2_AVAILABLE = True
except ImportError:
    FPDF2_AVAILABLE = False
    print("Note: fpdf2 not installed. PDF generation disabled.")
    print("Install with: pip install fpdf2")


class PDFReport(FPDF):
    """自定义 PDF 报告类"""
    
    def __init__(self):
        super().__init__()
        # 设置中文字体支持
        self.add_font('SimSun', '', 'C:/Windows/Fonts/simsun.ttc', uni=True)
        self.add_font('SimHei', '', 'C:/Windows/Fonts/simhei.ttf', uni=True)
        self.set_font('SimSun', '', 12)
        
    def header(self):
        # 可在子类中重写
        pass
        
    def footer(self):
        self.set_y(-15)
        self.set_font('SimSun', '', 9)
        self.set_text_color(128)
        self.cell(0, 10, f'— 第 {self.page_no()} 页 —', align='C')


class AIReportPDF(PDFReport):
    """AI 资讯简报 PDF"""
    
    def __init__(self):
        super().__init__()
        self.chapter_title_font = ('SimHei', '', 16)
        self.chapter_font = ('SimSun', '', 11)
        self.title_color = (26, 115, 232)  # Google Blue
        self.heading_color = (33, 33, 33)
        self.text_color = (51, 51, 51)
        self.gray_color = (95, 99, 104)
        
    def create_title_page(self, date_range):
        """创建封面页"""
        self.add_page()
        
        # 标题
        self.set_font('SimHei', '', 32)
        self.set_text_color(*self.title_color)
        self.cell(0, 40, '[AI] AI 资讯简报', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # 日期
        self.set_font('SimSun', '', 16)
        self.set_text_color(*self.gray_color)
        self.cell(0, 20, f'日期: {date_range}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # 分隔线
        self.ln(15)
        self.set_draw_color(*self.title_color)
        self.set_line_width(1)
        self.line(50, self.get_y(), 160, self.get_y())
        
        # 底部信息
        self.ln(30)
        self.set_font('SimSun', '', 10)
        self.set_text_color(*self.gray_color)
        self.cell(0, 10, '[AI] 由 AI 资讯简报自动生成', align='C')
        
    def chapter_title(self, title):
        """章节标题"""
        self.set_font('SimHei', '', 14)
        self.set_text_color(*self.title_color)
        self.cell(0, 12, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
    def chapter_body(self, text):
        """正文内容"""
        self.set_font('SimSun', '', 10)
        self.set_text_color(*self.text_color)
        self.multi_cell(0, 6, text)
        self.ln()


def generate_pdf_report(articles, date_range, output_path):
    """
    使用 FPDF2 生成 PDF 报告
    """
    if not FPDF2_AVAILABLE:
        print("PDF generation requires: pip install fpdf2")
        return None
    
    try:
        # 创建 PDF
        pdf = AIReportPDF()
        
        # 封面
        pdf.create_title_page(date_range)
        
        # 导入分类模块
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from categorizer import categorize_articles, get_module_order
            categorized = categorize_articles(articles)
            module_order = get_module_order()
        except Exception:
            categorized = {"热点资讯": articles[:15]}
            module_order = [("热点资讯", "🔥")]
        
        # 按模块生成
        for module_name, icon in module_order:
            module_articles = categorized.get(module_name, [])
            if not module_articles:
                continue
            
            # 新页面
            pdf.add_page()
            
            # 模块标题
            pdf.chapter_title(f"[{module_name}] {module_name} ({len(module_articles)}条)")
            
            # 文章列表
            for i, article in enumerate(module_articles[:10], 1):
                title = article.get('title', '')[:60]
                source = article.get('source', '未知来源')
                hot_score = article.get('hot_score', 0)
                summary = article.get('summary', '')[:100]
                level = article.get('credibility', {}).get('level', 'D')
                
                # 标题
                pdf.set_font('SimHei', '', 11)
                pdf.set_text_color(26, 115, 232)
                pdf.cell(0, 8, f"{i}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                
                # 元信息
                pdf.set_font('SimSun', '', 9)
                pdf.set_text_color(95, 99, 104)
                meta = f"来源: {source}  |  可信度: {level}  |  热度: {hot_score}"
                pdf.cell(0, 6, meta, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                
                # 摘要
                if summary and len(summary) > 10:
                    pdf.set_font('SimSun', '', 9)
                    pdf.set_text_color(51, 51, 51)
                    pdf.cell(0, 6, f"摘要: {summary}...", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                
                pdf.ln(8)
        
        # 保存
        pdf.output(output_path)
        return output_path
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_pdf_with_attachment(articles, date_range, config=None):
    """
    生成PDF并作为附件发送
    """
    if not FPDF2_AVAILABLE:
        return None, "请先安装: pip install fpdf2"
    
    # 确保目录存在
    output_dir = config.get('config', {}).get('output_dir', './reports') if config else './reports'
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    from datetime import datetime
    filename = f"ai_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # 生成PDF
    try:
        pdf_path = generate_pdf_report(articles, date_range, output_path)
        return pdf_path, "success"
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    # 测试
    if FPDF2_AVAILABLE:
        print("[OK] FPDF2 PDF module ready!")
        
        # 测试数据
        test_articles = [
            {'title': '测试文章1：OpenAI发布新模型GPT-5震撼发布', 'source': '36kr', 'hot_score': 95, 
             'summary': '这是测试摘要内容，OpenAI发布了最新的GPT-5模型，性能大幅提升...', 
             'credibility': {'level': 'A'}, 'url': 'https://example.com/1'},
            {'title': '测试文章2：英伟达发布5090新显卡', 'source': '量子位', 'hot_score': 88, 
             'summary': '英伟达发布5090显卡，性能提升显著，AI计算能力大幅增强...', 
             'credibility': {'level': 'A'}, 'url': 'https://example.com/2'},
            {'title': '测试文章3：AI创业公司完成亿元融资', 'source': '爱范儿', 'hot_score': 75, 
             'summary': '某AI创业公司完成亿元融资，估值达到10亿美元...', 
             'credibility': {'level': 'B'}, 'url': 'https://example.com/3'},
            {'title': '测试文章4：国产大模型发布性能接近GPT-4', 'source': '机器之心', 'hot_score': 82, 
             'summary': '国产大模型发布，性能接近GPT-4水平...', 
             'credibility': {'level': 'A'}, 'url': 'https://example.com/4'},
        ]
        
        output_path = 'test_fpdf2.pdf'
        result = generate_pdf_report(test_articles, '2026-04-07', output_path)
        
        if result and os.path.exists(result):
            print(f"[OK] PDF generated: {result}")
            print(f"     File size: {os.path.getsize(result)} bytes")
        else:
            print("[ERROR] PDF generation failed")
    else:
        print("Please install fpdf2: pip install fpdf2")