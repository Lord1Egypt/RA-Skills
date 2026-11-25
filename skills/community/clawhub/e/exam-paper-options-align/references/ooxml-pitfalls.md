# OOXML 排版坑位清单

处理 .docx 试卷排版时的非显性陷阱，按"踩中频率"排序。

## 1. 制表符写不进去

| 通道 | 结果 |
|---|---|
| 编辑器 SDK `doc_insert_text` / `doc_replace_text` | 拒绝，`code=9`（控制字符） |
| 编辑器 SDK `doc_insert_html_content` + `&#9;` | 被转成普通空格 |
| **python-docx `run.text = "...\t..."`** | ✅ 自动转成真正的 `<w:tab/>` |

结论：写制表符只能改 XML。改前 `save_file` + `close_file`，改后重新 `open_file`，否则编辑器缓存会覆盖磁盘改动。

## 2. 字号「看着不一致」的四个真凶

`w:sz` 全都是同一个值时，视觉上仍可能不一致：

1. **`w:szCs` 与 `w:sz` 不同步**：run 没有 `szCs` 时回退到样式定义（如 `_Style 0` 的 `szCs=22`）。必须显式写 `sz == szCs`。
2. **表格字号独立**：表格常用 10.5pt 而正文 12pt，最容易被用户一眼看出。
3. **theme 字体继承**：`asciiTheme` / `hAnsiTheme` / `cstheme` 未清除时，西文可能渲染成 Calibri 而非 Times New Roman，视觉大小差异明显。
4. **字体名无效**：`Times New Roman Regular`（多后缀）找不到字体 → 回退。正确写法 `Times New Roman`。

另查：残留 `w:i` 斜体、`w:position` 上下标、`w:w` 字符缩放。

## 3. rPr / pPr 子元素顺序敏感

Word 按 schema 顺序解析，`append` 新增元素常插到末尾而破坏顺序（尤其 `w:sz` 落在 `w:lang` 之后）。

`CT_RPr` 顺序（节选，完整顺序见脚本内 `RPR_ORDER`）：

```
rStyle → rFonts → b → bCs → i → iCs → ... → color → spacing → w → kern
→ position → sz → szCs → highlight → u → effect → bdr → shd → ... → lang
```

`w:tabs` 在 `CT_PPr` 中必须位于 `spacing` / `ind` **之前**。

稳妥做法：新增元素后，对整个 docx（`document.xml`、`styles.xml`、`header*.xml`、`footer*.xml`）做一次统一重排，脚本的 `sort_docx_xml()` 已实现。

## 4. 首行缩进会叠加到制表位

制表位是相对「左缩进 + 左边距」的绝对位置，但**首行缩进会推后文本起点**。若 `首行缩进 + 题号前缀宽度 > 第一个制表位`，制表符会跳到**下一个**制表位，整列错位。

对策：选项行首行缩进清零（`Pt(0)`），列位按「最长前缀 + 间隙」自适应计算。

## 5. 逐 run 改写时的制表符重复

把一段区间收敛为一个制表符时，若区间跨 run 边界，判定条件用 `gs >= rs` 会让相邻两个 run **各插入一个 tab**，结果变成 `\t\t` → 跳到下一列。

正确判定：`rs <= gs < re`（起点严格落在本 run 内）。零长度区间（纯插入）需把不相交判定写成 `ge < rs or gs > re`，否则会被跳过。

## 6. 选项内容被误删

区间取「标记结束 → 下一标记开始」会把选项正文一起替换掉。必须取「**内容结束**（去尾空白后）→ 下一标记开始」。

同理，前缀区间要取「前缀有效内容结束 → 第一个标记开始」，否则 `(    ) 1.` 这类题号会被删掉。

## 7. 空段落行高

没有 run 的段落继承 `Normal` 样式字号，行高与正文不同 → 间距看着不均。给空段落设 `w:pPr/w:rPr/w:sz`。

## 8. 内容校验不可省

改动后用「去空白归一化」逐段比对：

```python
norm = lambda s: re.sub(r"\s+", " ", s).strip()
```

差异应为空，或仅为空白规范化（如 `B.busy` → `B. busy`、段尾空格）。出现字词变化即为 bug。
