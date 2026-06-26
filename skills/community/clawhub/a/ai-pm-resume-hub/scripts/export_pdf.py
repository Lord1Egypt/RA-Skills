#!/usr/bin/env python3
"""
AI PM Resume Hub - PDF导出脚本
支持两种输出：
1. HR投递版：A4标准大小，重点突出实习经历
2. 手机预览版：竖屏长图，适配手机屏幕
"""
import os
import sys
from pathlib import Path
from fpdf import FPDF

# 配置路径
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
RESUME_ROOT = WORKSPACE_ROOT / "career" / "ai-pm-campus"
INPUT_MD = RESUME_ROOT / "outputs" / "resume-onepage.md"
INPUT_HTML = RESUME_ROOT / "outputs" / "resume-dashboard.html"
OUTPUT_HR_PDF = RESUME_ROOT / "outputs" / "resume-hr.pdf"
OUTPUT_MOBILE_PDF = RESUME_ROOT / "outputs" / "resume-mobile.pdf"

def load_resume_content():
    """加载简历Markdown内容"""
    if not INPUT_MD.exists():
        print(f"❌ 找不到简历文件：{INPUT_MD}")
        print("请先运行 /ai-pm-resume-hub build 生成简历")
        sys.exit(1)
    
    with open(INPUT_MD, "r", encoding="utf-8") as f:
        return f.read()

def parse_markdown(md_content):
    """简单解析Markdown内容"""
    lines = md_content.split("\n")
    parsed = []
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        if line.startswith("# "):
            parsed.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            parsed.append(("h2", line[3:].strip()))
        elif line.startswith("### "):
            parsed.append(("h3", line[4:].strip()))
        elif line.startswith("- "):
            parsed.append(("bullet", line[2:].strip()))
        elif line == "---":
            parsed.append(("divider", None))
        else:
            parsed.append(("text", line.strip()))
    
    return parsed

def export_hr_pdf(content):
    """导出HR投递版PDF：A4标准，突出实习经历"""
    print("📄 正在生成HR投递版PDF...")
    
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 配置字体
    pdf.add_font("Songti", "", "/System/Library/Fonts/Supplemental/Songti.ttc")
    pdf.add_font("Songti", "B", "/System/Library/Fonts/Supplemental/Songti.ttc")
    
    # 设置边距
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    
    # 渲染内容
    for item_type, text in content:
        if item_type == "h1":
            pdf.set_font("Songti", "B", 22)
            pdf.set_text_color(29, 29, 31)
            pdf.cell(0, 15, txt=text, ln=True, align="C")
            pdf.ln(5)
            
        elif item_type == "h2":
            pdf.set_font("Songti", "B", 16)
            pdf.set_text_color(0, 113, 227)
            pdf.cell(0, 10, txt=text, ln=True, align="L")
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(3)
            
            # 实习经历标题添加特殊标记，突出显示
            if "实习" in text:
                pdf.set_fill_color(240, 248, 255)
                pdf.rect(15, pdf.get_y() - 8, 180, 8, style="F")
            
        elif item_type == "h3":
            pdf.set_font("Songti", "B", 14)
            pdf.set_text_color(29, 29, 31)
            pdf.cell(0, 8, txt=text, ln=True, align="L")
            
        elif item_type == "bullet":
            pdf.set_font("Songti", "", 12)
            pdf.set_text_color(66, 66, 69)
            pdf.cell(10)
            pdf.multi_cell(160, 6, txt="• " + text)
            pdf.ln(1)
            
        elif item_type == "divider":
            pdf.ln(3)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)
            
        elif item_type == "text":
            if "[待补" in text or "待补:" in text:
                pdf.set_text_color(255, 59, 48)
                pdf.set_font("Songti", "", 11)
            else:
                pdf.set_text_color(66, 66, 69)
                pdf.set_font("Songti", "", 12)
            pdf.multi_cell(170, 6, txt=text)
            pdf.ln(2)
    
    # 保存PDF
    pdf.output(OUTPUT_HR_PDF)
    print(f"✅ HR投递版PDF已生成：{OUTPUT_HR_PDF}")

def export_mobile_pdf():
    """导出手机预览版PDF：竖屏长图，基于可视化仪表盘"""
    print("📱 正在生成手机预览版PDF...")
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 缺少依赖 playwright，请先安装：pip3 install playwright")
        print("   安装后还需要运行：playwright install chromium")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 430, "height": 932})  # iPhone 14 Pro尺寸
        
        # 打开本地HTML文件
        html_path = f"file://{INPUT_HTML.resolve()}"
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        
        # 获取完整页面高度
        page_height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": 430, "height": page_height})
        
        # 生成PDF
        page.pdf(
            path=OUTPUT_MOBILE_PDF,
            width="430px",
            height=f"{page_height}px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        browser.close()
    
    print(f"✅ 手机预览版PDF已生成：{OUTPUT_MOBILE_PDF}")

def main():
    print("🚀 开始导出PDF...")
    
    # 1. 生成HR投递版
    md_content = load_resume_content()
    parsed_content = parse_markdown(md_content)
    export_hr_pdf(parsed_content)
    
    # 2. 生成手机预览版
    if INPUT_HTML.exists():
        export_mobile_pdf()
    else:
        print("⚠️  未找到可视化HTML文件，跳过手机预览版生成")
        print("   请先运行 /ai-pm-resume-hub visualize 生成仪表盘")
    
    # 输出统计
    hr_size = os.path.getsize(OUTPUT_HR_PDF) / 1024 if OUTPUT_HR_PDF.exists() else 0
    mobile_size = os.path.getsize(OUTPUT_MOBILE_PDF) / 1024 if OUTPUT_MOBILE_PDF.exists() else 0
    
    print("\n📊 导出完成：")
    if hr_size > 0:
        print(f"   - HR投递版：{hr_size:.1f} KB")
    if mobile_size > 0:
        print(f"   - 手机预览版：{mobile_size:.1f} KB")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
