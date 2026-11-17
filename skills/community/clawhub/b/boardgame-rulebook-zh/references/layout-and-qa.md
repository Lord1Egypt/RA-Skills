# 版式安全与自动 QA（实现说明）

## 总流程

```text
PDF
 ├─ extract.py
 │   ├─ 逐页读取文字 dict（行/span/bbox/字号/粗体/颜色）
 │   ├─ find_tables() 识别表格单元
 │   ├─ 合并行段落；在行首项目符号处切分列表
 │   ├─ XY-cut 推断阅读顺序（左栏→右栏；页眉/页脚带）
 │   ├─ 识别标题/图注/正文/表格/内嵌图标
 │   ├─ 位图摘要、矢量图摘要、页面几何
 │   ├─ 术语命中 + 译文模板
 │   └─ 扫描页/大面积图片/旋转文字警告
 ├─ translations.tsv（人/agent 翻译）
 └─ render.py
     ├─ 只擦文字行 bbox（fill=False，images=NONE，graphics=NONE）
     ├─ 按原 bbox 写回译文；自动缩放/安全扩框/表格夹取
     ├─ 内嵌图标绕图排版
     ├─ 重新打开输出，与 before 摘要比对
     └─ report.md / report.json / 预览图
```

## 坐标与页面

- 单位是 PDF point（1/72 inch）；原点左上。`bbox = [x0, y0, x1, y1]`。
- PyMuPDF 的 `page.rect` 已考虑 `/Rotate`；`get_text` bbox 与写回坐标在同一空间。旋转页可以处理，但要目检。
- 不改变页面尺寸、CropBox、旋转、页数。QA 的 `geometry-changed` 会拦。

## 提取策略

### 行与段落

- 用 `page.get_text("dict")` 取 block/line/span；保留每行 bbox，用于精确擦除。
- 同一 block 内按垂直间距、字号/粗体变化、水平不重叠切分 run；跨 block 的断行在阅读顺序确定后合并（`merge_fragments`）。
- 行首项目符号（`• - – 1. (a)` 等）会把列表逐条切开；避免把整页配件清单合成一大段。
- 文本重建：英文连字符断行合并；中文不加空格；项目符号保留。
- 单字母 `E.` 不再当作列表标记，避免把 “Robert E. Howard” 切断。

### 表格

- `page.find_tables()` 给 cell bbox；按行中心/重叠把 line 分给单元。
- 每个 cell 单独成段，译文框夹在 cell 内（左右各 2pt 安全边）；表格线是矢量图，渲染时不动。
- 无边框表格不一定被 `find_tables` 识别；此时靠水平不重叠 + `flat` 标记拆成单行，渲染时只向右借用安全空白。

### 阅读顺序

- 递归 XY-cut：横向/纵向全宽空白决定切分；优先保证左栏→右栏。
- 页面顶部/底部的短页眉/页脚可先抽出（最多 4 项、非项目符号）；避免把右栏顶部的配件清单误当页眉。
- 阅读顺序只影响 `source.md` 的翻译顺序，不影响最终文字位置；译文按 id 写回原 bbox。

### 标题与对齐

- 正文字号取全文档加权中位数；字号 ≥ 正文 1.18 倍、或短粗体全大写，判为标题。
- 多行标题按中心/右边缘判断对齐；单行标题用同栏正文的列边界判断是否居中。
- 图注若与图片中心对齐则居中；页脚按页宽判断居中/右对齐。
- 颜色取 span 加权众数；粗体按 flags/font name；斜体不强制。

### 内嵌图标

- 位图：与段落 bbox 相交、面积小、位于文字区域内 → 内嵌图。
- 矢量图：`get_drawings()` 中小尺寸填充路径（≤ 4×字号）且与文字行相交 → 图标。
- `source.md` 标 `inline_art`；渲染时用 `layout_around_obstacles` 逐行绕开，并向右借用安全空白。
- 满页背景图（面积 > 页面 50%）不作为障碍；文字本来就在它上面。
- 图标顺序可能需要人工判断：图标是句子成分（资源符号）时，译文顺序要对照原页。

## 擦除（关键）

对每一行：

```python
page.add_redact_annot(line_bbox_expanded, fill=False)
page.apply_redactions(
    images=fitz.PDF_REDACT_IMAGE_NONE,
    graphics=fitz.PDF_REDACT_LINE_ART_NONE,
    text=0,
)
```

- `fill=False`：不填白，保留羊皮纸/彩色底/背景图。
- `images=NONE`：不删位图。
- `graphics=NONE`：不删线条、表格框、矢量插画。
- 只擦**文字行 bbox**，不擦整页、不擦单元格整块。
- 表格线、图标、插图、装饰边框都被保留；QA 再用摘要证明。

## 写回

### 普通段落

- 用 `fitz.TextWriter.fill_textbox` 先试排；溢出会抛异常/返回剩余行。
- 成功后再 `write_text` 到页面；不会留下半截文字。
- 自动从原字号向下缩（0.25pt），直到放得下；最低 5.5pt（表格 5.0，标题 6.5）。
- 对齐沿用左/中/右；颜色沿用原色；粗体用粗体字体。
- 字号低于 7pt 警告；低于原字号 70% 警告。

### 安全扩框

- 纵向：从原 bbox 向下扩展，直到下一个文字/图片/图标或页底安全线；有上限（正文约 2.8×行高，标题 1.6×行高）。
- 横向：列表项、页眉页脚、疑似无边框表格标签、内嵌图标段可以向右借用空白（上限 60pt 或 0.8×原宽），不进入同 y 带的其它文字/图片。
- 表格单元：不允许越出 cell；只能缩字号。
- 任何扩框都不会覆盖其它文字/图片；QA 会再次检查实际写入 bbox。

### 内嵌图标

- `layout_around_obstacles` 逐行计算可用横向区间，绕开图标。
- 一行放不下时向下移；不覆盖图标。
- 如果实在放不下，渲染器会用最小字号强制写出并报 `overflow`；必须改写译文/override。

### 字体

- 自动顺序：Microsoft YaHei → SimHei → SimSun（Windows）；PingFang/STHeiti（macOS）；Noto Sans CJK/WQY（Linux）；最后 PyMuPDF 内置 CJK。
- `--font` / `--bold-font` 可指定；羊皮纸/奇幻规则书可试 SimSun（衬线）。
- 渲染后 `doc.subset_fonts()` 子集化，输出通常只增加几十 KB 到几 MB。
- 缺字（emoji、生僻字）会报 `missing-glyphs`；换字体或删符号。
- 输出字体应嵌入且文字可选中；QA 检查 Type0 字体。

## QA 检查项

### 资产完整性

| 检查 | 方法 | 失败级别 |
| --- | --- | --- |
| 页数 | `page_count` | error |
| 页面几何 | `page.rect` / mediabox / cropbox / rotation | error |
| 位图 | `get_image_info(hashes=True)` 的 digest + bbox + 尺寸，排序后比较 | error |
| 矢量图 | `get_drawings()` 规范化为 JSON 后 SHA1 | error |

位图/矢量图摘要不变 = 插图、表格线、图标、装饰没有移动/删除/重编码。  
满页背景图也算位图；它不变说明底图完好。

### 文本完整性

| 检查 | 说明 |
| --- | --- |
| `missing-translation` | 有 id 无译文；默认 error |
| `text-not-found` | 输出页找不到完整译文（缺字/裁剪/编码） |
| `source-residue` | 原英文仍残留在该段 bbox |
| `number-missing` | 原文数字未出现在译文（warning） |
| `glossary-wrong` | 命中术语表的明确错译（error） |
| `termbase-mismatch` | 项目术语库建议（info） |
| `line-start-punctuation` | 中文标点出现在行首（warning） |

### 版面完整性

| 检查 | 说明 |
| --- | --- |
| `overflow` | 最小字号仍放不下；已强制写出，必须修 |
| `table-cell-overflow` | 译文越出表格单元 |
| `placement-outside-page` | 写入位置越出页面 |
| `art-covered` | 覆盖内嵌位图/图标 |
| `vector-covered` | 覆盖矢量图标 |
| `text-overlap` | 两段译文互相重叠 |
| `text-overlap-source` | 译文压到保留/未翻译原文 |
| `small-font` / `font-shrunk` | 字号过小（warning） |

重叠判定用面积比（>25% 较小框面积，且 >8pt²），避免紧行距列表的 1–2pt 框重叠误报。

## `layout_overrides.json`

路径默认 `work/layout_overrides.json`（也可 `--overrides`）。

```json
{
  "p003_s008": {
    "box": [28.0, 423.0, 292.0, 540.0],
    "font_size": 10.0,
    "align": "left"
  }
}
```

- `box`：PDF point，`[x0,y0,x1,y1]`；必须落在页面内。
- 表格单元会被夹到 cell；越界 QA 报错。
- `font_size`：起始字号，仍会自动缩小以适配。
- `align`：`left` / `center` / `right`。
- 用途：内嵌图标造成语义顺序别扭、行首标点、窄栏长词、特殊标题。
- 修改后重跑 render；不要手动改输出 PDF。

## 已知边界

- 扫描版/纯图 PDF：不覆盖；见 `scanned-pdfs.md`。
- 矢量描边文字：无文字层，不处理。
- 逐行竖排/旋转文字：保留原文并警告；整页 `/Rotate` 可处理。
- 复杂嵌套表格、表单字段、批注：未完全覆盖，需目检。
- PDF 中的文字如果本身被裁剪/重叠（设计如此），bbox 可能不完美；以视觉为准。
- 不重排页面：译文只使用原位置和安全空白；版面设计不会变。
- “满页图片覆盖 100%” 可能是正常底图（如羊皮纸），也可能是扫描；必须看预览确认文字是独立层。
- 字体只保证系统 CJK 覆盖；特殊符号/emoji 会报缺字。
- 版权：只处理用户有权翻译的文档；不要把原 PDF/整页译文发到公开仓库。
