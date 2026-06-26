# 标准商务幻灯片模板

## Table of Contents
- [整体结构](#structure)
- [标题页](#title-slide)
- [目录页](#agenda)
- [内容页（文字+要点）](#content)
- [内容页（图文并排）](#split)
- [数据页（图表+说明）](#data)
- [过渡页（章节分隔）](#section)
- [结尾页](#end)
- [通用设计规范](#design)

---

## 整体结构 {#structure}

标准商务 PPT 通常包含：

```
1. 标题页      — 主题、副标题、日期/公司
2. 目录页      — 章节概览
3. 过渡页      — 章节分隔（可选）
4. 内容页 × N  — 文字要点 / 图文 / 数据图表
5. 结尾页      — Thank You / 联系方式 / Q&A
```

---

## 标题页 {#title-slide}

```python
def title_slide(prs, title, subtitle, date='', company=''):
    """深色渐变背景的封面页。"""
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x0A, 0x14, 0x2E)
    bg.line.fill.background()

    # 左侧强调色竖条
    bar = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(80000), Emu(SH))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(0x00, 0x7A, 0xFF)
    bar.line.fill.background()

    # 主标题
    txb = slide.shapes.add_textbox(Emu(300000), Emu(SH//2 - 700000),
                                   Emu(SW - 500000), Emu(600000))
    tf = txb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 副标题
    txb2 = slide.shapes.add_textbox(Emu(300000), Emu(SH//2 - 50000),
                                    Emu(SW - 500000), Emu(400000))
    tf2 = txb2.text_frame
    p2 = tf2.paragraphs[0]
    run2 = p2.add_run()
    run2.text = subtitle
    run2.font.size = Pt(18)
    run2.font.color.rgb = RGBColor(0x88, 0xBB, 0xFF)

    # 日期 / 公司（右下角）
    if date or company:
        info = f'{company}  {date}'.strip()
        txb3 = slide.shapes.add_textbox(Emu(SW - 2500000), Emu(SH - 400000),
                                        Emu(2300000), Emu(280000))
        tf3 = txb3.text_frame
        p3 = tf3.paragraphs[0]
        from pptx.enum.text import PP_ALIGN
        p3.alignment = PP_ALIGN.RIGHT
        run3 = p3.add_run()
        run3.text = info
        run3.font.size = Pt(10)
        run3.font.color.rgb = RGBColor(0x66, 0x88, 0xAA)

    add_fade_transition(slide)
    return slide
```

---

## 目录页 {#agenda}

```python
def agenda_slide(prs, sections: list[str], highlight_index: int = -1):
    """
    目录页，sections 为章节标题列表。
    highlight_index：当前章节（-1 = 无高亮，用于总目录）。
    """
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x0A, 0x14, 0x2E)
    bg.line.fill.background()

    # 页面标题
    txb = slide.shapes.add_textbox(Emu(500000), Emu(300000),
                                   Emu(SW - 1000000), Emu(500000))
    tf = txb.text_frame
    run = tf.paragraphs[0].add_run()
    run.text = 'AGENDA'
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 分割线
    sep = slide.shapes.add_shape(1, Emu(500000), Emu(880000),
                                 Emu(SW - 1000000), Emu(18000))
    sep.fill.solid()
    sep.fill.fore_color.rgb = RGBColor(0x00, 0x7A, 0xFF)
    sep.line.fill.background()

    # 章节列表
    item_h = 600000
    start_y = 1100000
    for i, sec in enumerate(sections):
        is_active = (i == highlight_index)
        y = start_y + i * item_h

        # 序号圆圈
        dot_clr = RGBColor(0x00,0x7A,0xFF) if is_active else RGBColor(0x33,0x44,0x55)
        dot = slide.shapes.add_shape(9, Emu(500000), Emu(y + 50000),
                                     Emu(280000), Emu(280000))
        dot.fill.solid()
        dot.fill.fore_color.rgb = dot_clr
        dot.line.fill.background()

        # 序号文字
        num_txb = slide.shapes.add_textbox(Emu(500000), Emu(y + 30000),
                                           Emu(280000), Emu(320000))
        from pptx.enum.text import PP_ALIGN
        num_p = num_txb.text_frame.paragraphs[0]
        num_p.alignment = PP_ALIGN.CENTER
        num_run = num_p.add_run()
        num_run.text = str(i + 1)
        num_run.font.size = Pt(11)
        num_run.font.bold = True
        num_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # 章节标题
        txt_clr = RGBColor(0xFF,0xFF,0xFF) if is_active else RGBColor(0x88,0x99,0xAA)
        txt_txb = slide.shapes.add_textbox(Emu(850000), Emu(y + 20000),
                                           Emu(SW - 1400000), Emu(350000))
        txt_run = txt_txb.text_frame.paragraphs[0].add_run()
        txt_run.text = sec
        txt_run.font.size = Pt(14 if is_active else 13)
        txt_run.font.bold = is_active
        txt_run.font.color.rgb = txt_clr

    add_fade_transition(slide)
    return slide
```

---

## 内容页（文字+要点） {#content}

```python
def bullet_slide(prs, title: str, bullets: list[str],
                 subtitle: str = '', accent_color=None):
    """
    标准要点页。bullets 支持两级缩进：以 '  ' 开头为二级要点。
    """
    from pptx.enum.text import PP_ALIGN
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    accent = accent_color or RGBColor(0x00, 0x7A, 0xFF)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x0A, 0x14, 0x2E)
    bg.line.fill.background()

    # 顶部色条
    top_bar = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(120000))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = accent
    top_bar.line.fill.background()

    # 页面标题
    t_txb = slide.shapes.add_textbox(Emu(400000), Emu(150000),
                                     Emu(SW - 800000), Emu(480000))
    t_run = t_txb.text_frame.paragraphs[0].add_run()
    t_run.text = title
    t_run.font.size = Pt(24)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 副标题（可选）
    content_top = 820000
    if subtitle:
        s_txb = slide.shapes.add_textbox(Emu(400000), Emu(680000),
                                         Emu(SW - 800000), Emu(300000))
        s_run = s_txb.text_frame.paragraphs[0].add_run()
        s_run.text = subtitle
        s_run.font.size = Pt(12)
        s_run.font.color.rgb = RGBColor(0x88, 0x99, 0xAA)
        content_top = 1050000

    # 要点列表
    item_h = 550000
    for i, bullet in enumerate(bullets):
        is_sub = bullet.startswith('  ')
        text = bullet.strip()
        y = content_top + i * item_h
        indent = 800000 if is_sub else 400000

        # 项目符号
        if not is_sub:
            dot = slide.shapes.add_shape(9, Emu(indent - 200000), Emu(y + 130000),
                                         Emu(120000), Emu(120000))
            dot.fill.solid()
            dot.fill.fore_color.rgb = accent
            dot.line.fill.background()

        # 文字
        b_txb = slide.shapes.add_textbox(Emu(indent + 50000), Emu(y),
                                         Emu(SW - indent - 500000), Emu(item_h - 50000))
        b_tf = b_txb.text_frame
        b_tf.word_wrap = True
        b_run = b_tf.paragraphs[0].add_run()
        b_run.text = text
        b_run.font.size = Pt(11 if is_sub else 13)
        b_run.font.color.rgb = (RGBColor(0x88,0x99,0xAA) if is_sub
                                else RGBColor(0xDD, 0xEE, 0xFF))

    add_fade_transition(slide)
    return slide
```

---

## 内容页（图文并排） {#split}

```python
def split_slide(prs, title: str, left_content_fn, right_content_fn):
    """
    左右分栏页。left_content_fn(slide, area) 和 right_content_fn(slide, area)
    接收 slide 和区域 dict {x, y, w, h}（EMU），负责在该区域内绘制内容。
    """
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x0A, 0x14, 0x2E)
    bg.line.fill.background()

    # 标题
    t_txb = slide.shapes.add_textbox(Emu(400000), Emu(150000),
                                     Emu(SW - 800000), Emu(480000))
    t_run = t_txb.text_frame.paragraphs[0].add_run()
    t_run.text = title
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 分割线
    mid_x = SW // 2
    div = slide.shapes.add_shape(1, Emu(mid_x - 9000), Emu(780000),
                                 Emu(18000), Emu(SH - 1000000))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(0x22, 0x33, 0x55)
    div.line.fill.background()

    # 回调绘制左右内容
    padding = 200000
    left_area  = {'x': padding, 'y': 820000,
                  'w': mid_x - padding * 2, 'h': SH - 1000000}
    right_area = {'x': mid_x + padding, 'y': 820000,
                  'w': mid_x - padding * 2, 'h': SH - 1000000}
    left_content_fn(slide, left_area)
    right_content_fn(slide, right_area)

    add_fade_transition(slide)
    return slide
```

---

## 数据页（图表+说明） {#data}

```python
def chart_slide(prs, title: str, chart_type, chart_data,
                insight: str = '', notes: list[str] = None):
    """图表页：左侧大图表，右侧关键洞察。"""
    from pptx.util import Inches
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x0A, 0x14, 0x2E)
    bg.line.fill.background()

    # 标题
    t_txb = slide.shapes.add_textbox(Emu(400000), Emu(150000),
                                     Emu(SW - 800000), Emu(480000))
    t_run = t_txb.text_frame.paragraphs[0].add_run()
    t_run.text = title
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 图表（占左侧 65%）
    chart_w = int(SW * 0.62)
    gf = slide.shapes.add_chart(
        chart_type,
        Emu(300000), Emu(820000),
        Emu(chart_w), Emu(SH - 1100000),
        chart_data,
    )
    ch = gf.chart
    ch.plot_area.format.fill.background()
    ch.chart_area.format.fill.background()
    if ch.has_legend:
        ch.legend.font.size = Pt(9)

    # 右侧洞察文字
    right_x = chart_w + 500000
    right_w = SW - right_x - 200000
    if insight:
        ins_txb = slide.shapes.add_textbox(Emu(right_x), Emu(900000),
                                           Emu(right_w), Emu(500000))
        ins_tf = ins_txb.text_frame
        ins_tf.word_wrap = True
        ins_run = ins_tf.paragraphs[0].add_run()
        ins_run.text = insight
        ins_run.font.size = Pt(13)
        ins_run.font.bold = True
        ins_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    if notes:
        for i, note in enumerate(notes):
            ny = 1500000 + i * 500000
            n_txb = slide.shapes.add_textbox(Emu(right_x), Emu(ny),
                                             Emu(right_w), Emu(420000))
            n_tf = n_txb.text_frame
            n_tf.word_wrap = True
            n_run = n_tf.paragraphs[0].add_run()
            n_run.text = f'• {note}'
            n_run.font.size = Pt(11)
            n_run.font.color.rgb = RGBColor(0xAA, 0xBB, 0xCC)

    add_fade_transition(slide)
    return slide
```

---

## 过渡页（章节分隔） {#section}

```python
def section_slide(prs, section_num: int, section_title: str,
                  accent_color=None):
    """章节分隔页，大号数字 + 标题，视觉节奏感强。"""
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    accent = accent_color or RGBColor(0x00, 0x7A, 0xFF)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x06, 0x0E, 0x22)
    bg.line.fill.background()

    # 大号序号（水印风格，右下角）
    num_txb = slide.shapes.add_textbox(Emu(SW - 2500000), Emu(SH - 2800000),
                                       Emu(2200000), Emu(2500000))
    num_p = num_txb.text_frame.paragraphs[0]
    from pptx.enum.text import PP_ALIGN
    num_p.alignment = PP_ALIGN.RIGHT
    num_run = num_p.add_run()
    num_run.text = f'{section_num:02d}'
    num_run.font.size = Pt(200)
    num_run.font.bold = True
    num_run.font.color.rgb = RGBColor(0x15, 0x25, 0x45)

    # 章节标题（居中偏左）
    t_txb = slide.shapes.add_textbox(Emu(500000), Emu(SH//2 - 400000),
                                     Emu(SW - 1000000), Emu(600000))
    t_run = t_txb.text_frame.paragraphs[0].add_run()
    t_run.text = section_title
    t_run.font.size = Pt(40)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 强调线
    line = slide.shapes.add_shape(1, Emu(500000), Emu(SH//2 + 260000),
                                  Emu(600000), Emu(25000))
    line.fill.solid()
    line.fill.fore_color.rgb = accent
    line.line.fill.background()

    add_fade_transition(slide)
    return slide
```

---

## 结尾页 {#end}

```python
def end_slide(prs, message: str = 'Thank You',
              contact: str = '', logo_path: str = ''):
    """结尾页。"""
    from pptx.enum.text import PP_ALIGN
    SW, SH = int(prs.slide_width), int(prs.slide_height)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(SW), Emu(SH))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0x00, 0x5A, 0xCC)
    bg.line.fill.background()

    # 主文字
    m_txb = slide.shapes.add_textbox(Emu(0), Emu(SH//2 - 700000),
                                     Emu(SW), Emu(700000))
    m_p = m_txb.text_frame.paragraphs[0]
    m_p.alignment = PP_ALIGN.CENTER
    m_run = m_p.add_run()
    m_run.text = message
    m_run.font.size = Pt(48)
    m_run.font.bold = True
    m_run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # 联系方式
    if contact:
        c_txb = slide.shapes.add_textbox(Emu(0), Emu(SH//2 + 100000),
                                         Emu(SW), Emu(400000))
        c_p = c_txb.text_frame.paragraphs[0]
        c_p.alignment = PP_ALIGN.CENTER
        c_run = c_p.add_run()
        c_run.text = contact
        c_run.font.size = Pt(14)
        c_run.font.color.rgb = RGBColor(0xCC, 0xDD, 0xFF)

    # Logo（如果提供路径）
    if logo_path:
        from pptx.util import Inches
        slide.shapes.add_picture(logo_path,
                                 Emu(SW - 1500000), Emu(SH - 600000),
                                 Emu(1200000), Emu(400000))

    add_fade_transition(slide)
    return slide
```

---

## 通用设计规范 {#design}

**字体大小体系**

| 用途 | 大小 |
|------|------|
| 封面主标题 | 36–48pt |
| 页面标题 | 22–28pt |
| 正文要点 | 13–15pt |
| 次要文字 | 10–12pt |
| 注释/标签 | 8–10pt |

**颜色体系**

| 用途 | 建议 |
|------|------|
| 背景 | 深蓝黑（深色）或白色（浅色） |
| 强调色 | 1–2 个品牌色，保持一致 |
| 正文文字 | 接近白/黑，对比度 > 4.5:1 |
| 次要文字 | 60–70% 亮度的正文色 |

**完整演示构建示例**

```python
from pptx import Presentation
from pptx.util import Emu
from pptx_helpers import add_fade_transition
# import the functions above

prs = Presentation()
prs.slide_width  = Emu(12192000)
prs.slide_height = Emu(6858000)

title_slide(prs, 'Q1 Business Review', '2025 January – March',
            date='2025-04-10', company='Acme Corp')

agenda_slide(prs, ['Market Overview', 'Financial Results',
                    'Product Updates', 'Outlook'])

section_slide(prs, 1, 'Market Overview')
bullet_slide(prs, 'Market Overview',
             ['Total addressable market grew 18% YoY',
              '  Asia-Pacific leads with 32% growth',
              '  North America stable at +8%',
              'Competitive landscape remains fragmented',
              'New regulations creating entry barriers'])

section_slide(prs, 2, 'Financial Results')
# ... more slides

end_slide(prs, 'Thank You', contact='contact@acme.com')

prs.save('q1-review.pptx')
```
