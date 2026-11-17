#!/usr/bin/env python3
"""生成可研报告专业排版 Word 模板（交付 Kit 用）。

用法: python3 gen_report_docx.py "项目名称" "编制单位" 输出路径.docx
规范: 封面+签署页+TOC域+样式体系(黑体标题/仿宋正文)+页眉页脚页码+三线表样式
"""
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PROJECT = sys.argv[1] if len(sys.argv) > 1 else "××××项目"
ORG     = sys.argv[2] if len(sys.argv) > 2 else "××××咨询有限公司"
OUT     = sys.argv[3] if len(sys.argv) > 3 else "可研报告模板.docx"

doc = Document()

# ---------- 页面 ----------
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.top_margin, sec.bottom_margin = Cm(2.54), Cm(2.54)
sec.left_margin, sec.right_margin = Cm(3.0), Cm(2.6)

def set_font(run, cn="仿宋_GB2312", en="Times New Roman", size=12, bold=False, color=None):
    run.font.name = en
    run.font.size = Pt(size)
    run.font.bold = bold
    r = run._element.rPr.rFonts
    r.set(qn("w:eastAsia"), cn)
    if color: run.font.color.rgb = RGBColor(*color)

def para(text="", cn="仿宋_GB2312", size=12, bold=False, align=None, before=0, after=6, line=None, color=None):
    p = doc.add_paragraph()
    if align is not None: p.alignment = align
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    if line: pf.line_spacing = Pt(line)
    if text:
        r = p.add_run(text); set_font(r, cn, size=size, bold=bold, color=color)
    return p

def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def field(par, instr):
    """插入域代码（目录 TOC / 页码 PAGE）"""
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = instr
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end")
    par._p.append(b); par._p.append(i); par._p.append(e)

# ---------- 样式体系 ----------
def style_heading(name, size, cn="黑体", color=(0,0,0), before=18, after=10):
    st = doc.styles[name]
    st.font.name = "Times New Roman"; st.font.size = Pt(size); st.font.bold = True
    st.font.color.rgb = RGBColor(*color)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), cn)
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    return st

style_heading("Heading 1", 16, "黑体", before=24, after=12)   # 章  二号~三号
style_heading("Heading 2", 14, "黑体")                         # 节
style_heading("Heading 3", 13, "楷体_GB2312")                  # 条

# 正文默认
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"; normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "仿宋_GB2312")
normal.paragraph_format.line_spacing = Pt(26)

# ---------- 封面 ----------
for _ in range(5): para("", after=0)
para(PROJECT, cn="黑体", size=26, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=0, line=40)
para("可 行 性 研 究 报 告", cn="黑体", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=0, line=36)
for _ in range(9): para("", after=0)
para(f"编制单位：{ORG}", cn="仿宋_GB2312", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
para("二〇二六年九月", cn="仿宋_GB2312", size=16, align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
page_break()

# ---------- 签署页 ----------
for _ in range(4): para("", after=0)
para("文件编号：KY-2026-×××", size=12, after=30)
para("报告密级：内部资料 · 注意保存", size=12, after=60)
tbl = doc.add_table(rows=6, cols=2)
tbl.style = "Table Grid"; tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
signs = [("编制人", ""), ("审核人", ""), ("审定人", ""), ("项目负责人", ""), ("编制单位（盖章）", ""), ("日    期", "")]
for i, (k, v) in enumerate(signs):
    c0, c1 = tbl.rows[i].cells
    c0.width, c1.width = Cm(4.5), Cm(9)
    p0 = c0.paragraphs[0]; r0 = p0.add_run(k); set_font(r0, "黑体", size=12)
    p1 = c1.paragraphs[0]
page_break()

# ---------- 目录 ----------
p = para("目  录", cn="黑体", size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
fld = doc.add_paragraph(); field(fld, 'TOC \\o "1-3" \\h \\z \\u')
page_break()

# ---------- 正文骨架（研判逻辑） ----------
def chapter(title):
    doc.add_paragraph(title, style="Heading 1")
def section(title):
    doc.add_paragraph(title, style="Heading 2")
def sub(title):
    doc.add_paragraph(title, style="Heading 3")
def body(t):
    return para(t)

# 企业级项目可行性研究 · 首版研判骨架（信息少、交付快、逻辑专业）
chapter("第一章  项目概述")
section("1.1 项目基本情况")
body("（一）项目名称：本项目建设单位为××，拟投资建设××项目，项目地点位于××，计划总投资约××亿元，资金来源为××。")
body("（二）建设内容：××。")
section("1.2 投资与实施主体")
body("（一）主体概况：××。")
body("（二）与本项目的匹配性：××。")
section("1.3 报告编制依据与范围")
body("本报告依据《企业投资项目可行性研究报告编写参考大纲（2023年版）》（发改投资规〔2023〕304号）编制。鉴于项目尚处前期论证阶段，部分建设与财务数据依据公开资料与行业基准进行初步测算，最终数据以投资决策阶段实测为准。")

chapter("第二章  项目建设背景与必要性")
section("2.1 政策与战略背景")
body("（一）国家层面：××。")
body("（二）区域层面：××。")
section("2.2 项目建设的必要性")
body("（一）战略必要性：××。")
body("（二）市场需求必要性：××。")

chapter("第三章  市场分析与需求预测")
section("3.1 行业市场总览")
body("（一）市场规模与增速：××（数据来源：××，××年）。")
body("（二）竞争格局：××。")
section("3.2 目标市场需求测算")
body("采用自上而下/自下而上方法测算，本项目达产年可服务市场约××。")

chapter("第四章  项目选址与要素保障")
section("4.1 选址方案与比选")
body("（一）备选方案：××。")
body("（二）选址结论：××。")
section("4.2 要素保障")
body("用地/用海/用能/环评等前置条件落实情况：××。")

chapter("第五章  建设方案与运营方案")
section("5.1 技术及建设方案")
section("5.2 运营与商业模式")
body("（一）收入结构：××。")
body("（二）盈利逻辑：××。")

chapter("第六章  投资估算与财务评价")
section("6.1 投资估算")
body("项目总投资约××亿元，其中建设投资××亿元、建设期利息××亿元、流动资金××亿元。投资测算详见《项目投资测算套表》。")
section("6.2 融资方案")
section("6.3 财务评价结论")
body("（一）盈利能力：全投资财务内部收益率约××%，财务净现值（ic=××%）××万元，静态投资回收期××年，详见配套测算套表。")
body("（二）偿债能力：××。")
body("（三）敏感性：××。")

chapter("第七章  风险分析与控制")
body("（一）主要风险：××。")
body("（二）应对措施：××。")

chapter("第八章  研究结论与建议")
section("8.1 研究结论")
body("综合判断：本项目××。")
section("8.2 后续工作建议")
body("（一）需进一步落实：××。")
body("（二）待补充资料清单：××。")

# ---------- 页眉页脚 ----------
hdr = sec.header
hp = hdr.paragraphs[0]; hp.text = f"{PROJECT} 可行性研究报告"
hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in hp.runs: set_font(r, "黑体", size=9)
ftr = sec.footer
fp = ftr.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("第 "); set_font(r, size=9)
fldp = fp.add_run(); field(fp, "PAGE")
set_font(fldp, size=9)
r = fp.add_run(" 页 共 "); set_font(r, size=9)
flds = fp.add_run(); field(fp, "NUMPAGES")
set_font(flds, size=9)
r = fp.add_run(" 页"); set_font(r, size=9)

doc.save(OUT)
print(f"OK -> {OUT}")
