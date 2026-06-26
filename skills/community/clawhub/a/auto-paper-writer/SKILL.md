---
name: auto-paper-writer
description: 自动撰写科研论文的完整 AI pipeline。当用户说"撰写[方向]论文"、"自动写论文"、"生成论文"时触发。功能包括：(1) 搜索 ArXiv 最新论文并下载原始 PDF；(2) 总结现有工作局限性；(3) 设计创新模型框架；(4) 撰写双栏 LaTeX 论文（IEEEtran格式）；(5) 生成科研级 matplotlib 配图；(6) 编译 PDF 并保存到桌面。此技能仅生成学术论文框架和创新点思路，不保证内容创新性和实验真实性，用户需自行在 Overleaf/本地 LaTeX 中补充实验结果和细节调整。
---

# Auto Paper Writer

自动撰写科研论文的完整 pipeline。从文献调研到 PDF 输出的端到端自动化。

## 工作流程

### Step 1: 搜索最新论文
使用 ArXiv API 搜索相关方向的最新论文：

```powershell
# PowerShell 调用 ArXiv API
$query = "your search terms"
$url = "https://export.arxiv.org/api/query?search_query=all:$query&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
```

优先搜索 ICLR/NeurIPS/AAAI/ICML 等顶会论文，以及与用户方向相关的高引用工作。

### Step 1.5: 保存搜索论文
将搜索到的论文信息保存到文献文件夹：

```powershell
# 创建文献文件夹
$ref_dir = "$paper_dir\references"
New-Item -ItemType Directory -Path $ref_dir -Force

# 保存论文列表（Markdown 格式）
$ref_content = @"
# 文献调研

## 搜索时间：$(Get-Date -Format "yyyy-MM-dd HH:mm")
## 搜索方向：$direction
## 搜索关键词：$keywords

---

### 论文列表

| # | 论文标题 | 作者 | 日期 | arXiv ID |
|---|---------|------|------|----------|
"@

foreach ($entry in $xml.feed.entry) {
    $title = $entry.title -replace '\s+', ' '
    $authors = ($entry.author | ForEach-Object { $_.name }) -join ', '
    $published = $entry.published.Substring(0,10)
    $arxiv_id = $entry.id.Split('/')[-1]
    $ref_content += "`n| - | $title | $authors | $published | [$arxiv_id](https://arxiv.org/abs/$arxiv_id) |"
}

$ref_content += "@"
$ref_content | Out-File -FilePath "$ref_dir\paper_references.md" -Encoding UTF8
```

保存内容：
- `references/paper_references.md` — 论文列表（标题/作者/日期/链接）
- `references/*.pdf` — 原始论文 PDF 文件

### Step 1.5: 下载论文原文 PDF
从 ArXiv 下载每篇论文的原始 PDF，**文件用论文标题命名**：

```powershell
# ArXiv PDF 下载地址格式
# https://arxiv.org/pdf/{arxiv_id}.pdf

foreach ($entry in $xml.feed.entry) {
    $arxiv_id = $entry.id.Split('/')[-1] -replace 'v\d+$', ''
    $title = $entry.title -replace '\s+', ' ' -replace '[^\w\s-]', '' -replace '\s', '_'
    $pdf_url = "https://arxiv.org/pdf/$arxiv_id.pdf"
    $pdf_path = "$ref_dir\$title.pdf"

    # 截断过长文件名，保留前 50 字符
    if ($title.Length -gt 50) {
        $title = $title.Substring(0, 50)
        $pdf_path = "$ref_dir\$title.pdf"
    }

    try {
        Invoke-WebRequest -Uri $pdf_url -OutFile $pdf_path -UseBasicParsing
        Write-Host "Downloaded: $title.pdf"
    } catch {
        Write-Host "Failed to download: $arxiv_id"
    }
}
```

**文件命名规则**：
- 用论文标题命名，不是 arXiv ID
- 空格替换为下划线
- 特殊字符清理
- 过长截断前 50 字符

下载结果示例：
- `references/Bidirectional_Cross-Modal_Prompting_for_Event-Frame.pdf`
- `references/MM-WebAgent_A_Hierarchical_Multimodal_Web_Agent.pdf`
- ...

**重要**：此步骤是标准工作流程的必要环节，必须执行！

### Step 2: 分析局限性
阅读摘要和核心方法，总结现有工作的**局限性**：
- 计算开销大 / 参数量过大
- 需要海量标注数据
- 模态对齐/融合不完善
- 泛化能力有限
- 推理速度慢

### Step 3: 设计创新模型框架
- 起一个简洁有力的模型名字
- 提出 **3-5 个核心创新点**
- 画整体架构框图（模块化设计）

### Step 4: 撰写论文
按标准科研论文结构，使用 **IEEEtran 双栏格式**：

```latex
\documentclass[conference]{IEEEtran}
```

论文结构：
1. **Abstract** - 简明扼要，150-250 词
2. **Introduction** - 研究背景、动机、贡献（列出 3-5 条贡献）
3. **Related Work** - 梳理相关工作，对比分析
4. **Proposed Method** - 详细介绍方法
5. **Experiments** - 实验设置、基线对比
6. **Conclusion** - 总结与未来工作
7. **References** - 格式规范的参考文献

使用标准 LaTeX 公式、表格、`\ref{}` 交叉引用。

### Step 5: 生成科研级配图
使用 matplotlib 生成 300dpi 高质量图片：

```python
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# 图1: 模型框架图 - 整体架构，模块化，箭头标注
# 图2: 方法细节图 - 核心创新机制
# 图3: 实验结果图 - 对比曲线、柱状图
```

### Step 6: 编译 PDF
使用 **TeX Live**（不是 Tectonic）编译：

```powershell
$texlive = "D:\texlive\2026\bin\windows\pdflatex.exe"
$paper_dir = "C:\Users\29064\Desktop\PaperName"

# 必须运行两次！第一次生成 .aux，第二次解析交叉引用
& $texlive "$paper_dir\paper.tex" -interaction=nonstopmode -output-directory="$paper_dir"
& $texlive "$paper_dir\paper.tex" -interaction=nonstopmode -output-directory="$paper_dir"
```

**关键规则**：
- 编译失败时**绝不简化 .tex 内容**，保留完整让用户在 Overleaf 自行处理
- 编译时**必须在 tex 文件所在目录运行**（否则图片相对路径找不到）
- **不要用 Tectonic**（与 IEEEtran 不兼容）

### Step 7: 保存到桌面
输出路径：`C:\Users\29064\Desktop\[论文名字]\`
包含文件：
- `paper.tex` - 主论文文件
- `paper.pdf` - 编译后的 PDF
- `figure1.png` / `figure2.png` / `figure3.png` - 配图
- `references/paper_references.md` - 文献调研列表
- `references/*.pdf` - 原始论文 PDF

### Step 8: 清理临时文件
论文撰写完成后，**删除所有临时脚本文件**：
- 搜索脚本（`search_*.ps1`）
- 下载脚本（`download_*.ps1`）
- 配图生成脚本（`generate_*.py`）
- 其他中间文件

```powershell
Remove-Item "$env:USERPROFILE\Desktop\*.ps1" -Force
Remove-Item "$env:USERPROFILE\Desktop\*.py" -Force
Remove-Item "$env:USERPROFILE\Desktop\*_v*.pptx" -Force
```

## 核心原则

1. **生成后立即编译**：.tex 完成后立刻用 TeX Live 编译
2. **保留完整性**：不简化内容，编译失败时输出完整 .tex
3. **双栏 IEEEtran**：标准学术论文格式
4. **科研级配图**：300dpi，清晰标注

## 参考文件

- **论文模板**：[references/ieee_template.md](references/ieee_template.md)
- **LaTeX 写作指南**：[references/latex_guide.md](references/latex_guide.md)
- **配图规范**：[references/figure_guide.md](references/figure_guide.md)
