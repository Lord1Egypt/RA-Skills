# reference.docx 制作指南

## 什么是 reference.docx

`reference.docx` 是一个**样式模板**，Pandoc 转换时会读取它的样式定义，套用到生成的 docx 上。

本 skill **不提供默认模板**，你必须自己准备一份。

## 制作步骤

### 方法一：从已有文档开始（推荐）

1. 找一个已经调好样式的 Word 文档
2. 用 Word 打开
3. 在「开始 → 样式」里逐个检查并修改样式（见下文"改哪些样式"）
4. **另存为** `reference.docx`

### 方法二：用 pandoc 导出空白模板再改

```powershell
# 导出 pandoc 默认样式模板到当前目录
pandoc --print-default-data-file reference.docx > my_reference.docx
```

然后用 Word 打开 `my_reference.docx`，改好样式后另存为 `reference.docx`。

### 方法三：完全从空白 docx 开始

用 Word 新建空白文档，先在「样式」里设定 Normal / Heading 1-6 等样式，另存为 `reference.docx`。

## 改哪些样式最有用

| 样式名 | 影响 |
|--------|------|
| **Normal**（正文） | 全局字体、字号、行距、段间距 |
| **Heading 1** ~ **Heading 6** | 各级标题样式 |
| **Title** | 文档主标题 |
| **Subtitle** | 副标题 |
| **Quote** / **Block Text** | 引用块 |
| **Code** / **Verbatim Char** | 行内代码 |
| **Code Block** | 代码块 |
| **List Paragraph** | 列表 |
| **Caption** | 图表标题 |
| **Table Text** / **Table Caption** | 表格 |
| **Hyperlink** | 超链接颜色/下划线 |

## 关键技巧

1. **用"样式"面板改，不要直接选中文字改格式**
   - 直接改格式 = 局部覆盖，Pandoc 不识别
   - 改"样式" = 全局生效，Pandoc 会读取

2. **中文用户注意**
   - 在 Normal 样式里把中文字体设为宋体/微软雅黑，西文设为 Times New Roman / Calibri
   - 字号建议：正文小四（12pt），标题适当加大

3. **页面设置**
   - 页边距、纸张大小、页眉页脚：在"布局"里改，Pandoc 会保留

4. **不要删除默认样式**
   - Pandoc 按样式名匹配，删了会导致对应元素用回默认样式

## 验证方法

转换一个测试文档，检查：
- 标题层级是否正确对应 Heading 1-6
- 字体/字号是否符合预期
- 代码块是否有边框/背景色
- 列表缩进是否正确

## 常见问题

**Q: 改了样式但转换后没生效？**
A: 检查是否改了"样式"本身（开始 → 样式 → 右键 → 修改），而不是直接改文字格式。

**Q: 中文显示为方框？**
A: Normal 样式里中文字体没设置，或者 pandoc 不支持该字体。换宋体/微软雅黑试试。

**Q: 如何改页边距？**
A: 在 Word 的"布局"→"页边距"里改，保存到 reference.docx 即可。
