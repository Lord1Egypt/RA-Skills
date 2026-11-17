# 中文论文排版与导出技术规范

## 1. 页面设置

| 项 | 值 |
|---|---|
| 纸张 | A4（21cm × 29.7cm） |
| 上下左右边距 | 2.54cm |
| 装订线 | 0（默认） |

## 2. 字体与字号规范

| 元素 | 中文 | 英文/数字 | 字号 | 字重 | 对齐 |
|---|---|---|---|---|---|
| 论文主标题 | 黑体 | Times New Roman | 二号 22pt | 加粗 | 居中 |
| 一级标题（第 N 章） | 黑体 | Times New Roman | 三号 16pt | 加粗 | 居中 |
| 二级标题（N.M 节） | 黑体 | Times New Roman | 小三 15pt | 加粗 | 左对齐 |
| 三级标题 | 黑体 | Times New Roman | 四号 14pt | 加粗 | 左对齐 |
| 正文 | 宋体 | Times New Roman | 小四 12pt | 正常 | 两端对齐 |
| 表格内容 | 宋体 | Times New Roman | 小四 12pt | 表头加粗 | 居中 |
| 参考文献 | 宋体 | Times New Roman | 五号 10.5pt | 正常 | 两端对齐 |

## 3. 行距与段落

| 元素 | 行距 | 段前/段后 | 首行缩进 |
|---|---|---|---|
| 正文 | 双倍（2.0） | 0 / 0 | 2 字符（Pt(24) for 12pt body） |
| 主标题 | 单倍 / 1.5 | 12 / 24 | 无 |
| 一级标题 | 1.5 | 18 / 12 | 无 |
| 二级标题 | 1.5 | 12 / 6 | 无 |
| 三级标题 | 1.5 | 6 / 3 | 无 |
| 参考文献 | 1.5 倍 | 0 / 3 | 悬挂缩进（`first_line_indent = -size*2`） |
| 表格内 | 1.3 | 2 / 2 | 无 |

## 4. 参考文献格式（GB/T 7714-2015）

### 期刊论文
```
[n] 作者1, 作者2, 作者3, 等. 题名[J]. 期刊名, 年, 卷(期): 起页-止页. DOI: xx.xxxx/xxx.
```

### 会议论文
```
[n] 作者1, 作者2. 题名[C]//Proceedings of 会议名. 地点: 出版者, 年: 起页-止页. DOI: xx.xxxx/xxx.
```

### 专著
```
[n] 作者1, 作者2. 书名[M]. 出版地: 出版者, 年: 页码. ISBN: xxx.
```

### 关键要点
- 编号 `[n]` 用半角方括号
- 文献类型标识：`[J]` 期刊 / `[C]` 会议 / `[M]` 专著 / `[D]` 学位论文
- 作者超过 3 人写「等」或「et al」
- DOI 大写、完整
- 参考文献悬挂缩进：除首行外每行向左凸出 2 字符

## 5. python-docx 关键代码片段

### 5.1 安装
```bash
pip install python-docx --break-system-packages
```

### 5.2 页面 + 默认样式
```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

section = doc.sections[0]
section.page_height = Cm(29.7)
section.page_width = Cm(21.0)
for attr in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
    setattr(section, attr, Cm(2.54))

# 默认正文样式
normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(12)
nrPr = normal.element.get_or_add_rPr()
nrFonts = nrPr.find(qn('w:rFonts'))
if nrFonts is None:
    nrFonts = OxmlElement('w:rFonts')
    nrPr.append(nrFonts)
nrFonts.set(qn('w:eastAsia'), '宋体')
nrFonts.set(qn('w:ascii'), 'Times New Roman')
nrFonts.set(qn('w:hAnsi'), 'Times New Roman')
```

### 5.3 字体设置核心函数（**关键**）

> **避坑**：单纯 `run.font.name = "宋体"` **不会**让中文渲染为宋体；要写到 OOXML `w:rFonts` 的 `eastAsia` 属性。

```python
def set_run_fonts(run, zh='宋体', en='Times New Roman', size=12, bold=False, italic=False):
    run.font.name = en
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), zh)
    rFonts.set(qn('w:ascii'), en)
    rFonts.set(qn('w:hAnsi'), en)
    rFonts.set(qn('w:cs'), en)
```

### 5.4 段落 / 标题 / 参考文献辅助函数

```python
def add_para(doc, text, *, zh='宋体', en='Times New Roman',
             size=12, bold=False, italic=False,
             align=None, indent_first=True, line_spacing=2.0,
             space_before=0, space_after=0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line_spacing
    if indent_first:
        pf.first_line_indent = Pt(size * 2)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    run = p.add_run(text)
    set_run_fonts(run, zh=zh, en=en, size=size, bold=bold, italic=italic)
    return p


def add_heading(doc, text, level=1):
    """level: 0=主标题, 1=一级(章), 2=二级(节), 3=三级."""
    sizes = {0: 22, 1: 16, 2: 15, 3: 14}
    aligns = {0: WD_ALIGN_PARAGRAPH.CENTER,
              1: WD_ALIGN_PARAGRAPH.CENTER,
              2: WD_ALIGN_PARAGRAPH.LEFT,
              3: WD_ALIGN_PARAGRAPH.LEFT}
    add_para(doc, text, zh='黑体', en='Times New Roman',
             size=sizes[level], bold=True,
             align=aligns[level], indent_first=False,
             line_spacing=1.5)


def add_reference(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.first_line_indent = Pt(-21)  # 悬挂缩进
    pf.space_after = Pt(3)
    run = p.add_run(text)
    set_run_fonts(run, size=10.5)
```

### 5.5 表格
```python
from docx.enum.table import WD_ALIGN_VERTICAL

tbl = doc.add_table(rows=1, cols=N)
tbl.style = 'Table Grid'

def add_table_row(table, row_data, *, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
    row = table.add_row()
    for i, cell_text in enumerate(row_data):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for para in cell.paragraphs:
            para.clear()
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(cell_text)
        set_run_fonts(run, size=12, bold=bold)
```

### 5.6 插图（含图注）

> **避坑**：必须用 **`run.add_picture()`**（不是 `paragraph.add_picture()`）才能正确嵌入并控制段落格式；图和图注分两个段落（图在前、图注居中在下），中间不要有换页。

```python
def add_figure(doc, image_path, caption, width_cm=13):
    # 图（居中）
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.2
    pf.space_before = Pt(6)
    pf.space_after = Pt(0)
    run = p.add_run()
    run.add_picture(image_path, width=Cm(width_cm))
    # 图注（黑体小五，居中）
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cpf = cp.paragraph_format
    cpf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    cpf.line_spacing = 1.5
    cpf.space_before = Pt(0)
    cpf.space_after = Pt(12)
    crun = cp.add_run(caption)
    set_run_fonts(crun, zh='黑体', en='Times New Roman',
                  size=10.5, bold=True)
```

> **生成图本身**的推荐路径：`matplotlib` 装不上就用 `Pillow`。常用中文字体路径 `/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc`，ImageFont.truetype 直接读。推荐图片尺寸 12-15cm 宽、300 DPI 保存 PNG。

### 5.7 数学公式

> **避坑**：`add_para()` 默认是**正体**；数学公式必须用 **斜体 + 居中 + 无首行缩进**，否则渲染出来像"代码块"。

```python
# 单行公式
add_para(doc, '   v_id(t+1) = w·v_id(t) + c1·r1·(p_id − x_id(t)) + c2·r2·(g_d − x_id(t))',
         italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent_first=False)

# 多行公式（按行调用多次即可）
add_para(doc, '   x_id(t+1) = x_id(t) + v_id(t+1)',
         italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent_first=False)
```

**进阶**：若学校要求 Word 原生公式对象（可在 Word 中双击编辑），用 OOXML 嵌入 OMML，比纯文本公式可访问性更好；实现见 `python-docx` 文档中 `OxmlElement('m:oMath')` 的用法（小众需求，常规论文用斜体文本即可）。

## 6. docx → PDF（Linux）

```bash
soffice --headless --convert-to pdf "input.docx"
```

输出 PDF 与 docx 同目录。

## 7. 验证

```bash
pdfinfo output.pdf | grep -E '(Pages|Page size)'
```

期望：`Pages: 26+`、`Page size: 595.304 x 841.89 pts (A4)`。

## 8. 中文字体 fallback 说明

Linux 服务器通常未装 SimSun（宋体）。脚本里写 `宋体` 是「期望字体」，docx 在 Windows / macOS Word/WPS 上打开会用本地宋体；用 Linux + libreoffice 转 PDF 时会 fallback 到本地可用的中文字体（如 Noto Serif CJK SC / AR PL UMing），效果接近宋体但不完全一致。如对字体一致性要求极高，可在 LibreOffice 中配置字体替换：

```bash
mkdir -p ~/.config/libreoffice/4/user/registrymodifications.xcu.d/
cat > ~/.config/libreoffice/4/user/registrymodifications.xcu << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <item oor:path="/org.openoffice.Office.Common/Font/Substitution"><prop oor:name="Replacement" oor:op="fuse"><value>true</value></prop>
  <node oor:name="Substitutions">
   <node oor:name="MSungStd" oor:op="replace"><prop oor:name="ReplaceFont" oor:op="fuse"><value>Noto Serif CJK SC</value></prop><prop oor:name="SubstituteFont" oor:op="fuse"><value>Noto Serif CJK SC</value></prop></node>
   <node oor:name="SimSun" oor:op="replace"><prop oor:name="ReplaceFont" oor:op="fuse"><value>Noto Serif CJK SC</value></prop><prop oor:name="SubstituteFont" oor:op="fuse"><value>Noto Serif CJK SC</value></prop></node>
  </node>
 </item>
</oor:items>
EOF
```

## 9. 完整工作模板

最小可用的端到端脚本流程：

1. `mkdir -p paper && cd paper`
2. 写 `generate.py`（使用上面 5.x 的辅助函数 + 实际正文内容）
3. `python3 generate.py` → 生成 `xxx.docx`
4. `soffice --headless --convert-to pdf xxx.docx` → 生成 `xxx.pdf`
5. `pdfinfo xxx.pdf | grep Pages` → 校验页数

整段流程通常 5-15 分钟（取决于章节数），远快于人工 Word 排版。
