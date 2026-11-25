---
name: exam-paper-options-align
version: 1.0.0
display_name: 试卷选项对齐与排版优化
display_name_en: Exam Paper Option Alignment & Formatting
slug: exam-paper-options-align
description: 对齐 Word 试卷中选择题的选项（A对A、B对B、C对C、D对D纵向对齐成列），并统一全卷版式（字号、字体、颜色、行距、缩进），使其可直接打印给学生考试使用。当用户要求"对齐选项""选项对齐""选项纵向对齐""试卷排版""优化试卷""美化试卷""试卷整理""正文字号不一致""行距不统一""字号字体统一"，或提供 .docx/.doc 试卷、练习题、测验卷、作业单要求排版规范化时使用。Trigger words: align options, exam paper formatting, Word test paper layout, 试卷, 选择题, 选项对齐。
---

# 试卷选项对齐与版式统一

把 Word 试卷的选择题选项用制表位对齐成列，并统一全卷字号、字体、行距。核心是 `scripts/exam_format.py`，**不要手写 XML 或直接用编辑器接口改**，制表符写入有硬性限制（见下）。

## 快速开始

先确认 Python 环境有 `python-docx` / `lxml`（脚本依赖这两个库）：

```bash
PY=$(command -v python3 || command -v python)
"$PY" -c "import docx, lxml" 2>/dev/null || "$PY" -m pip install python-docx lxml
SK="路径/到/本技能目录/scripts/exam_format.py"
```

```bash
# 1) 只读诊断：先看这份卷子有什么问题
$PY "$SK" 试卷.docx --inspect

# 2) 对齐选项 + 统一版式（自动备份后原地覆盖）
$PY "$SK" 试卷.docx

# 3) 只对齐选项，不动其它版式（最小干预）
$PY "$SK" 试卷.docx --align-only

# 4) 输出到新文件 / 四选项 / 正文 14pt
$PY "$SK" 试卷.docx -o 新卷.docx --letters ABCD --body-size 14
```

把上面 `SK` 换成你本机实际的技能目录路径即可。

诊断报告会列出：字号分布、西文/中文字体、表格字号、`sz≠szCs` 数量、行距分布、识别到的选项行与自适应列位。**先看报告再动手**，能避免误判标题层级。

## 标准工作流

1. **确认文件未被 Word 占用**。脚本直接改写 docx，若 Word 正打开该文件，改动会被 Word 覆盖。提醒用户先关闭。
2. **备份**：默认自动生成 `原名.bak-时间戳.docx`。用 `--no-backup` 可关闭（不建议）。
3. **诊断**：`--inspect`，重点看三处：
   - 识别到的选项行数是否与卷面一致（不对就调 `--letters`）
   - 表格字号是否与正文一致
   - `sz≠szCs` 是否 > 0（> 0 就是"看着字号不一致"的根因）
4. **执行**：默认模式（对齐 + 统一版式）。用户只想对齐时用 `--align-only`。
5. **看校验报告**：脚本结束会做去空白逐段比对，输出"内容校验：逐段零改动 ✓"。若有差异，逐条确认是空白规范化还是字词变化——**字词变化必须为零**。
6. **交付**：提醒用户在 Word 中**重新打开**文件（旧窗口保存会覆盖改动）。

## 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--letters` | `ABCD` | 选项字母集合。三选项卷用 `ABC` |
| `--body-size` | `12` | 正文字号 pt。小学卷常用 12，可提到 14 |
| `--line-spacing` | `1.5` | 正文行距。标题固定 1.0 |
| `--cols` | 自适应 | 手动指定列位 pt，如 `80,220,360` |
| `--gap` | `2` | 列间隙（字符数） |
| `--lat-font` / `--ea-font` | Times New Roman / 宋体 | 西文 / 中文字体 |
| `--align-only` | 关 | 只对齐选项，不动字号行距 |
| `--no-indent` | 关 | 长正文段落（完形短文）不首行缩进 |

## 脚本做了什么

**对齐**：把选项行中「题号前缀→A」「A内容→B」「B内容→C」之间的空格/制表符各自收敛为**一个**制表符，段落设统一左对齐制表位。列位按内容宽度自适应（西文≈0.52em、中文≈1.0em），默认留 2 字符间隙。

**版式**：字号按原层级映射为 正文 / +2pt / +4pt 三档（加粗），全卷统一字体、纯黑；正文行距统一；表格与正文同字号；修正 `Normal` 及自定义样式的字体与字号定义；按 OOXML schema 重排所有 `rPr`/`pPr`。

## 关键约束（踩过的坑）

- **制表符只能走 XML**。编辑器 SDK 的 `doc_insert_text` / `doc_replace_text` 会拒绝 `\t`（code=9 控制字符），HTML 通道把 `&#9;` 转成空格。必须 python-docx 改写（`run.text` 里的 `\t` 会自动转成 `<w:tab/>`）。
- **`sz` 与 `szCs` 必须同步**，否则部分字符回退到样式里的值 → 用户看到"字号不一致"。
- **清掉 theme 字体引用**（`asciiTheme`/`hAnsiTheme`/`cstheme`），否则西文可能渲染成 Calibri。字体名要精确，`Times New Roman Regular` 是无效的。
- **`rPr`/`pPr` 子元素顺序敏感**，append 会破坏 schema 顺序导致 Word 解析异常。脚本末尾统一重排。
- **表格、页眉页脚、空段落**都要处理，漏掉就会残留异字号。

更多细节见 [references/ooxml-pitfalls.md](references/ooxml-pitfalls.md)。

## 已知边界

- 题干与选项同行且选项多（如 4 选项 + 长题干）可能放不下。脚本会等分列位并警告，建议改排版为「题干一行、选项一行」或减小 `--body-size`（报告会给出建议值）。
- 选项行识别要求字母按序递增且后有内容。若卷面用 `① ② ③` 或 `A、B、C、` 之外的记号，需先转写或调整 `--letters`（顿号 `、` 与全角点 `．` 已支持）。
- 表格内的选项行不处理（罕见）。
