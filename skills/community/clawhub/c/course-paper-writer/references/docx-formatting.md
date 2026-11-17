# DOCX 排版与自检

排版只占 10% 的分，但它是一票否决项：格式错了，前 90% 的内容分也会被打折。

---

## 一、字号对照

| 中文字号 | pt | 常见用途 |
|---|---|---|
| 二号 | 22 | 封面大标题 |
| 三号 | 16 | 论文标题、一级标题 |
| 四号 | 14 | 作者姓名、二级标题 |
| 小四 | 12 | 正文、三级标题 |
| 五号 | 10.5 | 摘要、关键词、参考文献 |

字体对应：黑体（标题）、宋体（正文）、楷体（姓名/学号）、仿宋（摘要/关键词）。**以用户的要求文件为准，不要套用你见过的模板。**

---

## 二、四个必设项（缺一个就出错）

### 1. 中文字体必须设 eastAsia

python-docx 的 `run.font.name = "宋体"` 只设 ascii/hAnsi，**不会设 eastAsia**，结果 Word 用西文字体渲染汉字，字距和字形都不对。

```python
from docx.oxml.ns import qn

def set_font(run, cn_font, size_pt, bold=False):
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.font.name = "Times New Roman"
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = rPr.makeelement(qn('w:rFonts'), {})
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:ascii'), "Times New Roman")
    rFonts.set(qn('w:hAnsi'), "Times New Roman")
```

### 2. 行距分两种，别混

```python
# 固定值（如"20 磅"）
pf.line_spacing = Pt(20)
pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY

# 倍数（如"1.5 倍行距"）—— 直接给浮点数
pf.line_spacing = 1.5
```

### 3. 首行缩进"2 字符" = 2 × 正文字号

小四（12pt）→ `pf.first_line_indent = Pt(24)`

### 4. 标题层级全文一致

一级/二级/三级标题的字体、字号、是否顶格，全文必须统一。**三级标题通常顶格不缩进**，但要用与正文不同的字体（如黑体）区分出来。

---

## 三、上标引用：占位符方案

正文写作时用 `⟦n⟧`，渲染时替换成上标 `[n]`：

```python
import re
CITE = re.compile(r"⟦(\d+)⟧")

def rich(par, text, cn, size):
    pos = 0
    for m in CITE.finditer(text):
        if m.start() > pos:
            set_font(par.add_run(text[pos:m.start()]), cn, size)
        r = par.add_run("[%s]" % m.group(1))
        set_font(r, cn, size)
        r.font.superscript = True
        pos = m.end()
    if pos < len(text):
        set_font(par.add_run(text[pos:]), cn, size)
```

好处：改序号只改占位符，不用手工找上标。

**编号必须按正文首次出现顺序**，生成后要做一次交叉核对：

```python
# 扫描正文，取首次出现顺序，必须等于 1..N
seen = []
for _, t in body:
    for m in CITE.finditer(t):
        v = int(m.group(1))
        if v not in seen:
            seen.append(v)
assert seen == list(range(1, len(refs) + 1))
```

---

## 四、字数怎么数

**必须报三档**，因为不同老师的算法不同：

| 档位 | 算法 | 用途 |
|---|---|---|
| 含小标题 | 正文全部字符（去空白、去上标） | 最严格 |
| 不含小标题 | 只算正文段落 | 常见 |
| 不含标点 | 剔除中文标点再数 | 宽松 |

摘要单独报两档（含标点/不含标点），因为摘要上限常常卡得很死（如 250–300 字）。

```python
PUNCT = "，。；：、！？“”‘’（）——…《》"

def count(s, keep_punct=True):
    s = re.sub(r"\[\d+\]", "", s)          # 上标不算字
    return len([c for c in s
                if not c.isspace() and (keep_punct or c not in PUNCT)])
```

**统计"近 N 年文献占比"时，必须先剔除 URL 里的访问日期**，否则 `[2026-11-10]` 会被当成出版年，占比虚高：

```python
def pub_year(ref):
    s = re.sub(r"\[\d{4}-\d{2}-\d{2}\]", "", ref)   # 先删访问日期
    ys = re.findall(r"(?<!\d)(20\d{2})(?!\d)", s)
    return int(ys[-1]) if ys else 0
```

---

## 五、页数估算（无 LibreOffice 时）

```
行宽pt   = (页宽 - 左 - 右)cm ÷ 2.54 × 72
每行字数 = floor(行宽pt ÷ 正文字号)
每页行数 = floor((页高 - 上 - 下)cm ÷ 2.54 × 72 ÷ 行高pt)
```

A4 + 常规页边距 + 小四 12pt：
- 20 磅固定行距 ≈ 35 行 × 37 字 ≈ 1000 字/页
- 1.5 倍行距 ≈ 30 行 ≈ 800–900 字/页

---

## 六、必查清单

生成后逐项跑一遍，不要靠肉眼：

```
□ 标题字体字号居中
□ 姓名、学院、学号 字体字号居中
□ 摘要、关键词 字体字号
□ 一级/二级/三级标题 字体字号 + 是否顶格
□ 正文 字体字号行距首行缩进
□ 参考文献 字体字号行距
□ 上标数量 = 引文处数
□ 引用序号 1..N 连续
□ 无残留占位符 ⟦ ⟧
□ 字体名确实是"宋体/黑体"，不是 None（继承了 Normal 样式也算合格，但要确认 Normal 样式设对了）
```

用脚本断言，不要看终端输出——**Windows 终端常把中文显示成乱码，看着像出错其实是对的，反之亦然**（见 pitfalls 第 2 条）。
