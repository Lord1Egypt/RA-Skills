"""
generate_mindmap.py — PPT结构脑图生成（v6.1 consulting-report-generator）
基于 reportlab 绘制层次化思维导图，从 Slide Config 数据生成 PDF 脑图
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white
import math, os

# Theme colors
NV = HexColor("#051C2C")
AB = HexColor("#006BA6")
AG = HexColor("#007A53")
AO = HexColor("#D46A00")
AR = HexColor("#C62828")
LG = HexColor("#CCCCCC")

def draw_rounded_rect(c, x, y, w, h, r=4, fill=NV, text="", text_color=white, font_size=10, bold=False):
    """绘制圆角矩形+文字"""
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
    c.drawCentredString(x + w/2, y + h/2 - font_size/3, text)


def generate_mindmap(slide_configs, output_path, title="报告结构脑图"):
    """
    从 Slide Config 数据生成脑图 PDF
    
    参数:
        slide_configs: [{"type":"section","label":"PART 01","title":"..."}, ...]
        output_path: 输出 .pdf 路径
        title: 脑图标题
    """
    w, h = landscape(A4)  # A4横向
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    
    # 标题
    c.setFillColor(NV)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, h - 35, title)
    c.setStrokeColor(AB)
    c.setLineWidth(2)
    c.line(30, h - 42, w - 30, h - 42)
    
    # 脑图布局参数
    root_x = 60
    root_y = h / 2
    level_gap = 150  # 层级间的水平间距
    vert_gap = 28     # 同级节点间的垂直间距
    
    # 绘制根节点
    draw_rounded_rect(c, root_x, root_y - 12, 100, 24, 5, NV, "PPT结构大纲", white, 10, True)
    
    # 从slide_configs中提取层级结构
    current_x = root_x + level_gap
    
    # 分组：章节与页面
    sections = []
    current_section = None
    
    for cfg in slide_configs:
        if cfg.get("type") == "section":
            current_section = {"title": cfg.get("title", ""), "pages": []}
            sections.append(current_section)
        elif cfg.get("type") in ("page", "content"):
            label = cfg.get("label", "")
            if current_section:
                current_section["pages"].append(label)
            else:
                # 封面/目录等特殊页
                sections.append({"title": label, "pages": []})
    
    if not sections:
        # 如果无分组，直接展平
        for cfg in slide_configs:
            if cfg.get("type") in ("page", "content"):
                sections.append({"title": cfg.get("label", ""), "pages": []})
    
    # 计算总高度（固定每节60px）
    max_pages = max((len(s.get("pages", [])) for s in sections), default=0)
    sec_height = 40 + max_pages * 22
    total_h = len(sections) * 60 + max_pages * 10
    start_y = min(h/2 + total_h/2, h - 80)
    
    # 绘制连接线和子节点
    for si, sec in enumerate(sections):
        sec_y = start_y - si * 45
        
        # 根节点到章节的连接线
        c.setStrokeColor(NV)
        c.setLineWidth(1.5)
        c.line(root_x + 100, root_y, current_x, sec_y)
        
        # 章节节点（Level 1）
        draw_rounded_rect(c, current_x, sec_y - 10, 130, 20, 4, AB, 
                          sec["title"][:20], white, 9, True)
        
        # 子页面（Level 2）
        pages = sec.get("pages", [])
        for pi, page_title in enumerate(pages[:5]):  # 最多5个子页
            page_y = sec_y - 14 - (pi + 1) * 22
            
            # 章节到页面的连接线
            c.setStrokeColor(LG)
            c.setLineWidth(0.8)
            c.line(current_x + 130, sec_y, current_x + level_gap, page_y)
            
            # 页面节点
            draw_rounded_rect(c, current_x + level_gap, page_y - 8, 120, 16, 3, 
                              AG if pi == 0 else HexColor("#88C0D0"),
                              page_title[:18], white, 7)
            
            # 如果还有更多页面用虚线...
            if pi == 4 and len(pages) > 5:
                c.setStrokeColor(LG)
                c.setDash(3, 3)
                c.line(current_x + level_gap, page_y - 12, 
                       current_x + level_gap + 60, page_y - 12)
                c.setDash()
                c.setFillColor(HexColor("#999999"))
                c.setFont("Helvetica", 7)
                c.drawString(current_x + level_gap + 5, page_y - 18, 
                            f"... 还有 {len(pages)-5} 页"[:15])
    
    # 底部信息
    c.setFillColor(HexColor("#999999"))
    c.setFont("Helvetica", 8)
    from datetime import datetime
    c.drawString(30, 20, f"共 {len(slide_configs)} 页幻灯片 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawRightString(w - 30, 20, "consulting-report-generator v6.1")
    
    c.save()
    print(f"✅ 脑图已生成: {output_path}")
    return output_path


# ============================================================
# 从 PPT Slide Config 数据生成脑图
# ============================================================

def build_slide_configs_from_ppt_structure(slides_data):
    """
    从PPT页面结构自动构建脑图配置
    
    参数:
        slides_data: [{"type":"cover|section|content|closing", "title":"...", "page":1}, ...]
    """
    configs = []
    for slide in slides_data:
        stype = slide.get("type", "content")
        if stype == "section":
            configs.append({
                "type": "section",
                "title": slide.get("title", ""),
                "label": slide.get("label", "")
            })
        elif stype in ("content", "cover", "toc"):
            configs.append({
                "type": "page",
                "label": slide.get("title", "")[:25]
            })
        elif stype == "closing":
            configs.append({
                "type": "page",
                "label": "总结与致谢"
            })
    return configs


def mindmap_from_ppt(pptx_path_or_slides, output_dir="/tmp"):
    """
    从PPT（或slides数据）生成脑图PDF
    
    用法:
        mindmap_from_ppt(slides_data, "/tmp/mindmap.pdf")
    """
    if isinstance(pptx_path_or_slides, list):
        configs = build_slide_configs_from_ppt_structure(pptx_path_or_slides)
        output_name = "ppt_structure_mindmap.pdf"
    else:
        # 未来可支持从pptx文件直接解析
        raise ValueError("请传入幻灯片数据列表")
    
    output_path = os.path.join(output_dir, output_name)
    generate_mindmap(configs, output_path)
    return output_path


if __name__ == "__main__":
    # 示例：精益生产PPT的Slide Config
    example_slides = [
        {"type": "cover", "title": "精益生产体系深度解析", "page": 1},
        {"type": "toc", "title": "内容目录", "page": 2},
        {"type": "section", "title": "精益生产概述", "label": "PART 01", "page": 3},
        {"type": "content", "title": "精益生产的起源与发展演进", "page": 4},
        {"type": "content", "title": "核心理念：一个目标、两大支柱", "page": 5},
        {"type": "content", "title": "精益屋是TPS经典结构", "page": 6},
        {"type": "section", "title": "七大浪费", "label": "PART 02", "page": 7},
        {"type": "content", "title": "TIMWOOD - 七种浪费总览", "page": 8},
        {"type": "content", "title": "生产过剩与等待浪费", "page": 9},
        {"type": "content", "title": "加工·库存·动作·不良浪费", "page": 10},
        {"type": "section", "title": "准时化JIT", "label": "PART 03", "page": 11},
        {"type": "content", "title": "JIT - 从推到拉", "page": 12},
        {"type": "content", "title": "看板管理实现JIT", "page": 13},
        {"type": "section", "title": "自働化Jidoka", "label": "PART 04", "page": 14},
        {"type": "content", "title": "人机最佳结合", "page": 15},
        {"type": "content", "title": "Poka-Yoke与Andon", "page": 16},
        {"type": "section", "title": "精益工具", "label": "PART 05", "page": 17},
        {"type": "content", "title": "5S现场管理", "page": 18},
        {"type": "content", "title": "标准化作业", "page": 19},
        {"type": "content", "title": "TPM全面生产维护", "page": 20},
        {"type": "content", "title": "SMED快速换模", "page": 21},
        {"type": "content", "title": "VSM价值流图", "page": 22},
        {"type": "section", "title": "OEE与绩效", "label": "PART 06", "page": 23},
        {"type": "content", "title": "全球OEE基准数据", "page": 24},
        {"type": "content", "title": "三大损失与OEE计算", "page": 25},
        {"type": "content", "title": "目标设定与改善案例", "page": 26},
        {"type": "section", "title": "持续改善Kaizen", "label": "PART 07", "page": 27},
        {"type": "content", "title": "Kaizen文化", "page": 28},
        {"type": "content", "title": "PDCA循环", "page": 29},
        {"type": "section", "title": "转型路线图", "label": "PART 08", "page": 30},
        {"type": "content", "title": "精益实施四阶段", "page": 31},
        {"type": "content", "title": "关键成功因素", "page": 32},
        {"type": "content", "title": "行动建议", "page": 33},
        {"type": "closing", "title": "结语", "page": 34},
    ]
    
    output = "/tmp/ppt_mindmap.pdf"
    mindmap_from_ppt(example_slides, output_dir="/tmp")
