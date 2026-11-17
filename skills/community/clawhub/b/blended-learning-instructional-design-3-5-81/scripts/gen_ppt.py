# -*- coding: utf-8 -*-
"""生成说课 PPT（.pptx），图文并茂、与 HTML 课件风格一致，末尾新增一页插入页脚说明。

用法：
    python gen_ppt.py <design_data.json> [输出目录]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import ensure_deps, read_footer, strip_lines  # noqa: E402
from gen_html_courseware import auto_quizzes  # 复用自动兜底出题逻辑（前测/中测/后测）

PRIMARY = None
ACCENT = None
TEXT_C = None
WHITE = None
LIGHT = None

PRIMARY_RGB = (0x14, 0x3A, 0x6E)
ACCENT_RGB = (0xE8, 0xA3, 0x3D)
TEXT_RGB = (0x26, 0x30, 0x3E)
WHITE_RGB = (0xFF, 0xFF, 0xFF)
LIGHT_RGB = (0xEF, 0xF4, 0xFB)
GREEN_RGB = (0x2A, 0x9D, 0x6B)
RED_RGB = (0xC0, 0x43, 0x2F)

Inches = None
Pt = None
qn = None
MSO_SHAPE = None
PP_ALIGN = None


def _load_pptx():
    global Inches, Pt, qn, MSO_SHAPE, PP_ALIGN
    from pptx.util import Inches, Pt
    from pptx.oxml.ns import qn
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN


CAL_KEYS = ["seq", "date", "week", "lecture", "minutes", "location",
            "students", "content", "form", "activity"]


def _rgb(c):
    """将颜色统一为 RGBColor（兼容传入的 (r,g,b) 元组或 None）。"""
    from pptx.dml.color import RGBColor
    if c is None:
        return RGBColor(0x26, 0x30, 0x3E)
    if isinstance(c, RGBColor):
        return c
    return RGBColor(*c)


def set_run(run, size, color, bold=False, name="微软雅黑"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = _rgb(color)
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    ea = rPr.makeelement(qn("a:ea"), {})
    ea.set("typeface", name)
    if latin is not None:
        latin.addnext(ea)
    else:
        rPr.append(ea)


def add_text(slide, left, top, width, height, lines, align=None):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (txt, size, color, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if align is not None:
            p.alignment = align
        p.space_after = Pt(6)
        run = p.add_run()
        run.text = txt
        set_run(run, size, color, bold)
    return tb


def add_rect(slide, left, top, width, height, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = _rgb(color)
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def add_card(slide, left, top, width, height, fill=LIGHT, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = _rgb(fill)
    if line is not None:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(1.25)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def add_oval(slide, left, top, size, color, text="", txt_color=None, txt_size=16):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left), Inches(top),
                                 Inches(size), Inches(size))
    shp.fill.solid()
    shp.fill.fore_color.rgb = _rgb(color)
    shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    set_run(r, txt_size, txt_color or WHITE, True)
    return shp


def content_header(slide, kicker, title, icon="📖"):
    add_rect(slide, 0, 0, 13.333, 0.14, ACCENT)
    add_oval(slide, 11.55, 0.42, 1.15, PRIMARY, icon, WHITE, 30)
    add_text(slide, 0.7, 0.45, 10.6, 0.5, [(kicker, 14, PRIMARY, True)])
    add_text(slide, 0.7, 0.9, 10.6, 1.0, [(title, 30, PRIMARY, True)])


def textcard_slide(prs, kicker, title, text, icon="📖", accent=PRIMARY):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, kicker, title, icon)
    lines = strip_lines(text) or ["（待填写）"]
    add_card(s, 0.9, 1.95, 11.6, 4.95, fill=WHITE, line=accent)
    add_text(s, 1.15, 2.2, 11.1, 4.5,
             [(ln, 15, TEXT_C, False) for ln in lines])
    return s


def bullets_slide(prs, kicker, title, lines, icon="🎓", accent=PRIMARY):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, kicker, title, icon)
    lines = list(lines)
    top = 2.0
    gap = min(1.0, (6.7 - top) / max(len(lines), 1))
    for i, ln in enumerate(lines):
        y = top + i * gap
        add_card(s, 0.9, y, 11.6, gap - 0.14, fill=LIGHT)
        add_oval(s, 1.05, y + (gap - 0.14 - 0.5) / 2, 0.5, accent, str(i + 1), WHITE, 16)
        add_text(s, 1.75, y + 0.08, 10.5, gap - 0.3, [(ln, 15, TEXT_C, False)])
    return s


def cover_slide(prs, bi):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(s, 0, 0, 13.333, 7.5, PRIMARY)
    add_oval(s, 10.2, -1.2, 3.4, ACCENT)
    add_oval(s, 11.6, 5.0, 2.6, (0x1A, 0x4D, 0x8F))
    add_rect(s, 0.9, 1.5, 2.7, 0.62, ACCENT)
    add_text(s, 0.9, 1.5, 6, 0.62, [("混合式教学设计 · 说课", 18, WHITE, True)])
    add_text(s, 0.9, 2.3, 11.6, 1.6, [(bi.get("course_name", "（课程名称）"), 42, WHITE, True)])
    info = [
        ("授课内容：" + str(bi.get("content", "")), 20, WHITE, False),
        ("所属节次：" + str(bi.get("section", "")), 20, WHITE, False),
        ("面向专业：" + str(bi.get("major", "")), 20, WHITE, False),
        ("学时安排：" + str(bi.get("hours", "")) + " ｜ 授课人数：" + str(bi.get("students", "")), 20, WHITE, False),
    ]
    add_text(s, 0.9, 4.1, 11.6, 2.6, info)
    return s


def agenda_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "内容导航", "说课目录", "🗺️")
    items = ["一、基本信息", "二、整门课程的混合式教学设计方案",
             "三、一课次的混合式教学设计方案",
             "互动体验：前测 · 知识图谱 · 教学流程模拟 · 中测 · 后测",
             "四、课程教学日历", "总结与页脚说明"]
    colors = [PRIMARY, ACCENT, GREEN_RGB, RED_RGB, (0x6A, 0x5A, 0xCD), TEXT_C]
    for i, it in enumerate(items):
        col = colors[i % len(colors)]
        x = 0.9 + (i % 2) * 6.0
        y = 2.0 + (i // 2) * 1.55
        add_card(s, x, y, 5.7, 1.35, fill=WHITE, line=col)
        add_oval(s, x + 0.25, y + 0.42, 0.5, col, str(i + 1), WHITE, 16)
        add_text(s, x + 0.95, y + 0.2, 4.6, 1.0, [(it, 16, TEXT_C, True)])
    return s


def basic_slide(prs, bi):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "课程与课次概况", "一、基本信息", "📋")
    pairs = [("课程名称", bi.get("course_name", "")), ("面向专业", bi.get("major", "")),
             ("授课内容", bi.get("content", "")), ("所属课程节次", bi.get("section", "")),
             ("学时安排", bi.get("hours", "")), ("授课人数", bi.get("students", ""))]
    for i, (k, v) in enumerate(pairs):
        x = 0.9 + (i % 2) * 6.0
        y = 2.0 + (i // 2) * 1.5
        add_card(s, x, y, 5.7, 1.3, fill=WHITE, line=PRIMARY)
        add_text(s, x + 0.25, y + 0.15, 5.3, 0.4, [(k, 14, ACCENT, True)])
        add_text(s, x + 0.25, y + 0.55, 5.3, 0.65, [(str(v), 16, TEXT_C, False)])
    return s


def goals_slide(prs, lg):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "三、一课次 · 2", "学习目标（知识/技能/素养/思政 · 布卢姆）", "🏁")
    if not isinstance(lg, dict):
        lg = {}
    labels = [("knowledge", "知识目标", "📘", PRIMARY),
              ("skill", "技能目标", "🛠️", ACCENT),
              ("literacy", "素养目标", "🌱", GREEN_RGB),
              ("ideology", "思政目标", "🚩", RED_RGB)]
    positions = [(0.9, 2.0), (6.9, 2.0), (0.9, 4.55), (6.9, 4.55)]
    for (key, label, icon, col), (x, y) in zip(labels, positions):
        v = lg.get(key, "") or ""
        add_card(s, x, y, 5.6, 2.25, fill=WHITE, line=col)
        add_rect(s, x, y, 5.6, 0.14, col)
        add_text(s, x + 0.25, y + 0.25, 5.1, 0.5, [(icon + "  " + label, 18, col, True)])
        pts = strip_lines(v)[:4]
        add_text(s, x + 0.25, y + 0.85, 5.15, 1.3,
                 [("• " + p, 13, TEXT_C, False) for p in pts] or [("（待填写）", 13, TEXT_C, False)])
    return s


def process_slide(prs, sl):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "三、一课次 · 4", "过程与方法（混合式教学流程）", "🔄")
    phases = [("课前 · 线上自学", "📱", PRIMARY, "观看概念视频、完成前测、在知识图谱标注疑点"),
              ("课中 · 线下深化", "🧑‍🏫", ACCENT, "案例导入、小组推导算法、上机求解、课堂辩论"),
              ("课后 · 线上拓展", "💡", GREEN_RGB, "提交仿真实验报告、智能体答疑、拓展阅读")]
    w = 3.55
    for i, (t, icon, col, desc) in enumerate(phases):
        cx = 0.9 + i * (w + 0.55)
        add_card(s, cx, 2.1, w, 3.4, fill=WHITE, line=col)
        add_rect(s, cx, 2.1, w, 0.14, col)
        add_oval(s, cx + w / 2 - 0.5, 2.4, 1.0, col, icon, WHITE, 26)
        add_text(s, cx + 0.15, 3.55, w - 0.3, 0.5, [(t, 17, col, True)], align=PP_ALIGN.CENTER)
        add_text(s, cx + 0.2, 4.15, w - 0.4, 1.3, [(desc, 13, TEXT_C, False)])
        if i < 2:
            add_text(s, cx + w + 0.02, 3.5, 0.55, 0.6, [("➜", 26, ACCENT, True)], align=PP_ALIGN.CENTER)
    det = "。".join(strip_lines(sl.get("process_method", ""))[:2])
    add_card(s, 0.9, 5.75, 11.6, 1.05, fill=LIGHT)
    add_text(s, 1.1, 5.9, 11.2, 0.8, [("实施要点：" + det, 13, TEXT_C, False)])
    return s


def parse_scores(text):
    m1 = re.search(r"前测[^\d]*?([\d.]+)", text or "")
    m2 = re.search(r"后测[^\d]*?([\d.]+)", text or "")
    if m1 and m2:
        try:
            return float(m1.group(1)), float(m2.group(1))
        except ValueError:
            return None
    return None


def effect_slide(prs, kicker, title, text, icon="📈"):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, kicker, title, icon)
    scores = parse_scores(text)
    if scores:
        pre, post = scores
        add_card(s, 0.9, 2.0, 3.5, 1.7, fill=LIGHT)
        add_text(s, 0.9, 2.15, 3.5, 0.5, [("前测平均分", 15, PRIMARY, True)], align=PP_ALIGN.CENTER)
        add_text(s, 0.9, 2.65, 3.5, 0.9, [("%.1f" % pre, 40, ACCENT, True)], align=PP_ALIGN.CENTER)
        add_card(s, 4.7, 2.0, 3.5, 1.7, fill=LIGHT)
        add_text(s, 4.7, 2.15, 3.5, 0.5, [("后测平均分", 15, PRIMARY, True)], align=PP_ALIGN.CENTER)
        add_text(s, 4.7, 2.65, 3.5, 0.9, [("%.1f" % post, 40, GREEN_RGB, True)], align=PP_ALIGN.CENTER)
        add_text(s, 8.6, 2.1, 4.0, 0.5, [("成绩提升对比", 15, PRIMARY, True)])
        add_rect(s, 8.6, 2.75, (pre / 100.0) * 3.9, 0.42, ACCENT)
        add_rect(s, 8.6, 3.35, (post / 100.0) * 3.9, 0.42, GREEN_RGB)
        add_text(s, 8.6 + (pre / 100.0) * 3.9 + 0.05, 2.7, 1.2, 0.35,
                 [("%.1f" % pre, 11, TEXT_C, False)])
        add_text(s, 8.6 + (post / 100.0) * 3.9 + 0.05, 3.3, 1.2, 0.35,
                 [("%.1f" % post, 11, TEXT_C, False)])
        add_card(s, 0.9, 4.0, 11.6, 2.9, fill=WHITE, line=PRIMARY)
        add_text(s, 1.15, 4.2, 11.1, 2.5, [(ln, 14, TEXT_C, False) for ln in strip_lines(text)])
    else:
        add_card(s, 0.9, 1.95, 11.6, 4.95, fill=WHITE, line=PRIMARY)
        add_text(s, 1.15, 2.2, 11.1, 4.5, [(ln, 15, TEXT_C, False) for ln in strip_lines(text) or ["（待填写）"]])
    return s


def calendar_slide(prs, rows):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "四、课程教学日历", "混合式教学教学日历（节选）", "🗓️")
    rows = rows[:12]
    n_rows = len(rows) + 1
    from pptx.util import Inches as In
    tbl_shape = s.shapes.add_table(n_rows, 10, In(0.55), In(1.9), In(12.25), In(4.6))
    tbl = tbl_shape.table
    widths = [0.7, 1.3, 1.0, 1.0, 0.8, 1.2, 0.9, 2.6, 0.9, 1.85]
    for ci, w in enumerate(widths):
        tbl.columns[ci].width = In(w)
    headers = ["序号", "日期", "周次", "讲次", "学时", "地点", "人数", "教学内容", "形式", "活动"]
    for ci, h in enumerate(headers):
        c = tbl.cell(0, ci)
        c.text = h
        for p in c.text_frame.paragraphs:
            for r in p.runs:
                set_run(r, 12, WHITE, True)
        c.fill.solid()
        c.fill.fore_color.rgb = PRIMARY
    for ri, item in enumerate(rows, start=1):
        for ci, k in enumerate(CAL_KEYS):
            c = tbl.cell(ri, ci)
            c.text = str(item.get(k, "") or "")
            for p in c.text_frame.paragraphs:
                for r in p.runs:
                    set_run(r, 11, TEXT_C, False)
            c.fill.solid()
            c.fill.fore_color.rgb = LIGHT if ri % 2 == 0 else WHITE
    add_text(s, 0.55, 6.75, 12, 0.5, [("完整日历见 Word 文档《混合式教学教学日历》。", 12, TEXT_C, False)])
    return s


def footer_slide(prs):
    lines = read_footer()
    title = lines[0] if lines else "Skill 说明与使用提示"
    body = [ln for ln in lines[1:] if ln.strip()]
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "页脚说明", title, "ℹ️")
    add_card(s, 0.9, 1.95, 11.6, 4.95, fill=WHITE, line=ACCENT)
    add_text(s, 1.15, 2.2, 11.1, 4.5, [(ln, 15, TEXT_C, False) for ln in body] or ["（待填写）"])
    return s


def quiz_slide(prs, data):
    """面向学生的前测/中测/后测（题目与参考答案）静态展示页。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    content_header(s, "面向学生的形成性测评", "前测 · 中测 · 后测（题目与参考答案）", "📝")
    quizzes = (data.get("interactions", {}) or {}).get("quizzes")
    if not quizzes:
        try:
            quizzes = auto_quizzes(data)
        except Exception:
            quizzes = []
    if not quizzes:
        add_text(s, 0.9, 2.4, 11.6, 4.0,
                 [("（未提供测试题，交互版题目与反馈见 HTML 课件）", 15, TEXT_C, False)])
        return s
    col_w = 3.75
    gap = 0.32
    xs = [0.7, 0.7 + col_w + gap, 0.7 + 2 * (col_w + gap)]
    icons = ["📝", "⚡", "🏆"]
    cols = [PRIMARY, ACCENT, GREEN_RGB]
    for ci, qz in enumerate(quizzes[:3]):
        x = xs[ci]
        add_card(s, x, 1.95, col_w, 4.95, fill=WHITE, line=cols[ci % 3])
        add_text(s, x + 0.2, 2.05, col_w - 0.4, 0.5,
                 [(icons[ci] + " " + qz.get("title", ""), 13, cols[ci % 3], True)])
        qs = qz.get("questions", [])[:2]
        y = 2.65
        for qi, q in enumerate(qs):
            opts = q.get("options") or []
            a = q.get("answer", 0)
            ans = opts[a] if 0 <= a < len(opts) else ""
            fb = q.get("explain", "") or ""
            if len(fb) > 64:
                fb = fb[:64] + "…"
            add_text(s, x + 0.2, y, col_w - 0.4, 0.55,
                     [("Q%d. %s" % (qi + 1, q.get("q", "")), 10.5, TEXT_C, True)])
            add_text(s, x + 0.2, y + 0.5, col_w - 0.4, 0.5,
                     [("✅ " + ans, 9.5, GREEN_RGB, False)])
            add_text(s, x + 0.2, y + 0.92, col_w - 0.4, 0.9,
                     [("💡 " + fb, 9, TEXT_C, False)])
            y += 1.95
    add_text(s, 0.7, 6.95, 12, 0.4,
             [("（每测示例 2 题；完整题库与作答反馈见 HTML 交互课件）", 10, TEXT_C, False)])
    return s


def build_ppt(data):
    from pptx import Presentation
    from pptx.dml.color import RGBColor

    global PRIMARY, ACCENT, TEXT_C, WHITE, LIGHT
    PRIMARY = RGBColor(*PRIMARY_RGB)
    ACCENT = RGBColor(*ACCENT_RGB)
    TEXT_C = RGBColor(*TEXT_RGB)
    WHITE = RGBColor(*WHITE_RGB)
    LIGHT = RGBColor(*LIGHT_RGB)

    bi = data.get("basic_info", {}) or {}
    wc = data.get("whole_course", {}) or {}
    sl = data.get("single_lesson", {}) or {}
    cal = data.get("calendar", []) or []

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    cover_slide(prs, bi)                                                  # 1
    agenda_slide(prs)                                                     # 2
    basic_slide(prs, bi)                                                  # 3
    textcard_slide(prs, "二、整门课程 · 1", "混合式教学设计思路",
                   wc.get("design_idea", ""), "🎯")                       # 4
    textcard_slide(prs, "二、整门课程 · 2", "创新举措",
                   wc.get("innovation", ""), "💡", ACCENT)                # 5
    effect_slide(prs, "二、整门课程 · 3", "效果达成情况",
                 wc.get("effect", ""), "📈")                             # 6
    textcard_slide(prs, "三、一课次 · 1", "学情分析",
                   sl.get("learning_analysis", ""), "🧭")                 # 7
    goals_slide(prs, sl.get("learning_goals", {}))                        # 8
    textcard_slide(prs, "三、一课次 · 3", "内容与资源",
                   sl.get("content_resources", ""), "📚")                 # 9
    process_slide(prs, sl)                                                # 10
    textcard_slide(prs, "三、一课次 · 5", "评价与反馈",
                   sl.get("evaluation", ""), "✅", GREEN_RGB)             # 11
    quiz_slide(prs, data)                                                # 12
    effect_slide(prs, "三、一课次 · 6", "教学效果达成情况",
                 sl.get("effect", ""), "🌟")                             # 12
    calendar_slide(prs, cal)                                             # 13
    bullets_slide(prs, "总结", "本课次混合式教学设计要点回顾",
                  ["围绕课程目标设计线上线下融合的学习路径",
                   "以学生发展为中心组织内容与资源",
                   "过程性评价贯穿课前、课中、课后",
                   "用数据持续改进教学，达成教学效果"], "🎓")              # 14
    footer_slide(prs)                                                    # 15

    return prs


def main():
    if not ensure_deps():
        print("依赖未就绪，请先运行 scripts/_bootstrap_deps.py 或请 AI 工具协助。")
        return 1
    _load_pptx()

    if len(sys.argv) < 2:
        print("用法：python gen_ppt.py <design_data.json> [输出目录]")
        return 1

    import json
    with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(sys.argv[1]))
    os.makedirs(out_dir, exist_ok=True)

    prs = build_ppt(data)
    out = os.path.join(out_dir, "混合式教学设计说课.pptx")
    prs.save(out)
    print("已生成：%s（共 %d 页）" % (out, len(prs.slides)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
