---
name: formula-pdf
description: 将包含数学公式的内容渲染为PDF文档。使用HTML+MathJax渲染公式，通过Edge无头模式转为PDF。当用户要求整理文档、生成报告、制作笔记且内容含有公式时触发。不要用Word导出（公式会变成代码），必须用此方法。
---

# Formula-PDF: 公式PDF文档生成

## 触发条件

当用户说 "整理成文档"、"发给我"、"弄成PDF" 且内容含有**数学公式**时触发。
**必须优先使用此方法**，不要使用Word导出。

## 工作流程

### Step 1: 编写HTML

内容优先写中文（文件名用英文），公式用MathJax语法。

**写文件的正确方式（重要！）：**
- 不要用 `write` 工具直接写HTML（含大量引号和反斜杠时参数会解析失败）
- 用PowerShell here-string写：

```powershell
@'
<html>
<head>
    <meta charset="UTF-8">
    <script>MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]}};</script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head>
<body>
    <!-- 内容 -->
</body>
</html>
'@ | Out-File -FilePath filename.html -Encoding UTF8
```

**公式写法：**
- 行内公式 `$E = mc^2$`
- 块级公式 `$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$`
- 表格中可以放公式
- 支持所有标准LaTeX数学命令
- **注意写斜杠：** `\frac` 不是 `frac`

### Step 2: 转换为PDF

使用Edge无头模式打印为PDF。**不要杀Edge进程，可直接共存运行。**

```powershell
& 'edge' `
    --headless=new `
    --virtual-time-budget=30000 `
    --print-to-pdf="output.pdf" `
    --no-margins `
    "file:///C:/path/to/input.html"
```

**关键参数解释：**
- `--headless=new`：无界面模式
- `--virtual-time-budget=30000`：等待MathJax加载和渲染的时间（毫秒）
- `--print-to-pdf`：输出PDF路径
- `--no-margins`：无边距
- `"file:///"`：必须用文件协议，**路径用双引号包起来**

### Step 3: 验证公式已渲染

用pymupdf检查PDF文本中是否含有原始LaTeX代码：

```python
import fitz
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()

# 如果含有这些关键词，说明公式没渲染
latex_patterns = [r'\frac', r'\sqrt', r'\lim', r'\sum', r'\int', r'\dfrac', r'$$']
for p in latex_patterns:
    if p in text:
        print("警告: 公式未渲染，含LaTeX原始代码")

print("验证完成")
```

### Step 4: 发送文件

用`message`工具将PDF发送给用户：

```python
message(action="send", filePath="PDF路径", message="公式已渲染")
```

## 参考脚本

- `scripts/html_to_pdf.py`：一键转换脚本，支持参数
- `assets/template.html`：HTML模板，可直接用作起点

## 常见问题

### 公式显示为LaTeX代码
- 增加 `--virtual-time-budget` 的值（如50000）
- 检查MathJax CDN地址是否可达
- 验证HTML中MathJax script标签是否正确

### PDF没生成
- Edge可能在进程冲突，先重试一次
- 确保文件路径用正斜杠

### 中文乱码
- CSS中设置 `font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;`

## 目录结构

```
formula-pdf/
├── SKILL.md
├── scripts/
│   └── html_to_pdf.py    # 一键转换工具
├── references/            # （可选）更多使用参考
└── assets/
    └── template.html      # HTML模板
```
