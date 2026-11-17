# docx-writer

配置驱动的标准文档生成技能。基于 **bayoo-docx**（原生支持脚注的 python-docx 分支）+ **PyYAML**。

核心思路：**排版与内容解耦**。字体/字号/颜色/对齐/缩进/行距/页边距/背景/脚注全部写在模板 YAML 里；内容脚本只写文字与图片。换体例只换模板，不动代码。

## 文件结构

```
docx-writer/
├── SKILL.md                 # 完整排版规范 + 使用说明
├── template.docx            # 默认基底（承载原生脚注样式），被 academic 模板引用
├── templates/               # 模板 = 一份 YAML 配置
│   ├── academic.yaml        #   学术/论文体例（含脚注）
│   ├── push.yaml            #   微信公众号推送稿体例
│   ├── news.yaml            #   清华新闻网简讯体例
│   └── script.yaml          #   演讲稿/答辩稿体例
├── scripts/
│   ├── docx_engine.py       # 引擎：Template(读配置) + Builder(渲染)
│   ├── latex_formula.py     # LaTeX → 紧裁 PNG（XeLaTeX+PyMuPDF）
│   ├── build_from_content.py# 声明式渲染器：content.yaml/json → docx（CLI）
│   └── build_docx.py        # 内容脚本示例（Python API 写法）
├── README.md
└── log.md
```

## 前置条件

```powershell
pip install bayoo-docx lxml pyyaml pymupdf pillow
```

数学公式可输出 **Word 原生可编辑公式（OMML）**（需 `pandoc`）或 **XeLaTeX 渲染图**（需 `xelatex`）。

## 写法 A：声明式内容文件（推荐）

`content.yaml`：

```yaml
template: push            # 选模板：academic / push / news
image_base: ./imgs        # image 相对路径的基准（可选）
blocks:
  - { type: title,   text: "砥柱中流，骨干领航丨……纪实" }
  - { type: para,    style: body, text: "正文段落。" }
  - { type: image,   path: fig1.jpg, caption: "图1  示意" }
  - { type: heading, level: 1, text: "班委选举" }
  - { type: para,    style: body, text: "带脚注的正文{F1}。", fn: { F1: "注释文本" } }
  - { type: table,   caption: "表1", headers: [a, b], rows: [[1, 2]] }
  - { type: signature, lines: ["文案丨xx", "审核丨xx"] }
```

运行：

```powershell
python scripts/build_from_content.py --content content.yaml --out out.docx
```

## 写法 B：Python API（复杂逻辑）

```python
from docx_engine import Template, Builder
b = Builder(Template.load('academic'))
b.title('标题')
b.heading('一、引言', level=1)
b.para('正文{F1}。', fn_map={'F1': '注释文本'})
b.image('fig.jpg', caption='图1  示意')
b.table(['列1', '列2'], [['a', 'b']])
b.save('out.docx')
```

或复制 `scripts/build_docx.py`，改 `TEMPLATE_NAME/OUTPUT/FIG_DIR`，在 `build_content()` 里用
`B/Bs/H1/H2/H3/Tc/add_img/add_tbl` 写内容。

## 加一套新模板

复制 `templates/` 下任一 yaml → 改名 → 调 `page` / `styles` / `footnote` 字段即可。
引擎与内容脚本无需改动。字段说明见 `SKILL.md`。

## 排版函数（写法 B）

| 函数 | 用途 | 默认字体/字号 |
|------|------|-------------|
| `B(text)` | 正文 | 宋体/Times New Roman 五号(10.5pt) |
| `Bs(text)` | 小字（摘要等） | 宋体/Times New Roman 小五(9pt) |
| `H1(text)` | 一级标题 | 黑体/Arial 小四(12pt)，居中 |
| `H2(text)` | 二级标题 | 黑体/Arial 小四(12pt) |
| `H3(text)` | 三级标题 | 黑体/Arial 五号(10.5pt) |
| `Tc(text)` | 表题/图题 | 宋体/Times New Roman 小五(9pt)，居中 |
| `add_img(path, cap)` | 插入图片 + 图题 | 居中 |
| `Fx(latex, cap=None)` | 行间公式（XeLaTeX 渲染） | 居中 |
| `Lx(text, lx_map)` | 含行内公式 `{X1}` 的段落 | 同正文 |
| `add_tbl(headers, rows)` | 三线表 | 小五(9pt)，仅上下框线 |

## LaTeX 公式

- **行间**：`b.formula(r'\alpha_0=\arctan(p_x/p_y)', caption='式(1)')`，或 `content.yaml` 里 `{ type: formula, latex: "...", caption: "..." }`。
- **行内**：段落文本中写 `{X1}` 占位，传 `lx_map={'X1': r'...'}`（或 `Lx('由 {X1} 可得', {...})`）。
- **呈现方式**（模板 `formula` 样式 `mode`，或调用级 `mode=`）：
  - `omml`：**Word 原生公式**，在 Word 里可点选编辑（走 pandoc）；
  - `image`：XeLaTeX `preview`+`tightpage` 紧裁成 PNG 插入（任何环境可渲染，不可编辑）；
  - `auto`（默认）：有 pandoc 用 `omml`，否则 `image`。
- 渲染函数也可单独用：`python scripts/latex_formula.py --latex "E=mc^2" --omml`（原生）
  或 `... --outdir ./png`（图片）。

## 脚注语法

- **句号在前**：`句子内容。{F1}` ✅ ｜ **不可**：`句子内容{F1}。` ❌
- 字体/字号/编号方式/上标由模板 + 引擎自动处理。
