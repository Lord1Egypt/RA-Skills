---
name: arxiv-paper-resolver
description: 接收 arXiv 论文链接，自动提取章节结构、下载 PDF、解析 HTML 全文，生成按论文自身章节结构编排的中文文档
tags: [Research, Papers, Documentation, Automation]
---

# arXiv 论文解析与归档技能

## 触发条件
- 用户提供 arXiv 论文链接（如 `https://arxiv.org/abs/2604.25836`）
- 用户要求查找、解析并生成某篇论文的中文文档

## 核心功能
1. **章节提取**：从 arXiv HTML 实验版解析论文的完整章节结构（h2 主节 + h3 子节）
2. **自动下载**：从 abs 页面获取 Access Paper 三个链接，下载 PDF
3. **目录归档**：按论文标题创建子目录，保存 PDF、章节文件、元数据
4. **中文翻译**：将各章节翻译为中文，生成按论文自身章节结构编排的 MD 文档（不包含参考文献/引用内容）

## 工作流程

### 完整流程概览
```
用户提供 arXiv 链接
  ↓
Step 1: 运行提取脚本（自动完成）
  ├── 获取 abs 页面 → 提取标题 + Access Paper 三链接
  ├── 创建论文标题命名的子目录
  ├── 下载 PDF
  ├── 获取 HTML 实验版全文
  ├── 解析 h2/h3 章节结构
  └── 保存章节文件 + 元数据 JSON
  ↓
Step 2: 读取章节文件（人工/LLM 完成）
  ├── 读取章节结构总览
  └── 逐章读取原始内容
  ↓
Step 3: 翻译并组装中文文档（LLM 完成）
  ├── 按章节依次翻译为中文
  ├── 保持数学符号和 LaTeX 公式不变
  └── 生成完整 MD 文档
  ↓
完成：PDF + 中文文档 已归档到目录
```

### 安装与依赖

```bash
pip install -r scripts/requirements.txt
```

### 步骤 1: 运行提取脚本

调用 `scripts/arxiv_section_extractor.py`，传入 arXiv ID（支持 URL 或裸 ID）：

```bash
python3 scripts/arxiv_section_extractor.py 2604.25836
# 或指定输出目录
python3 scripts/arxiv_section_extractor.py 2604.25836 -o ~/papers
# 或通过环境变量
export ARXIV_PAPERS_DIR=~/papers
python3 scripts/arxiv_section_extractor.py 2604.25836
```

脚本自动完成：
- 从 abs 页面获取论文标题和三个 Access Paper 链接
- 创建 `{output_dir}/{论文标题slug}/` 目录
- 下载 PDF
- 获取 HTML 实验版全文
- 解析所有 h2 章节（含 h3 子节），跳过 References / Appendix 等附录
- 保存元数据 JSON、章节结构总览

### 步骤 2: 读取章节结构

先读章节结构总览了解论文组织：

```bash
cat {output_dir}/{slug}/{arxiv_id}_section_structure.txt
```

### 步骤 3: 依次读取各章节原文

```bash
ls {output_dir}/{slug}/{arxiv_id}_raw_sections/
```

按编号顺序读取 `01_*.txt`、`02_*.txt`……每个文件包含该章的完整原文。

### 步骤 4: 翻译并生成中文 MD 文档

对每个章节：
1. 读取原始英文内容
2. 翻译为中文（保持数学符号/LaTeX 不变）
3. 按论文自身章节结构组装

**⚠️ 格式要求（严格执行）：**

**A. 行内公式必须使用 `$...$`（Typora 兼容）**
- ✅ 正确：`$S_{\text{TC}} = \frac{1}{N_{\text{valid}}}$`
- ❌ 错误：`\(S_{\text{TC}} = \frac{1}{N_{\text{valid}}}\)`（不渲染）
- ❌ 错误：``$`S_{\text{TC}} = \frac{1}{N_{\text{valid}}}`$``（带反引号乱码）
- 生成后必须验证：文件中所有公式定界符都是纯 `$`，不能有反引号 `` ` `` 或 `\(`/`\)`

**B. 禁止使用 HTML 锚点标签**
- ❌ 错误：`<a id="section-1"></a>`（在 Typora 中显示为多余字段）
- 目录链接（如 `[1. 章节名](#section-1)`）也应一并省略，Typora 不支持此类锚点跳转

**C. 文档结构（最终 MD 格式）：**
```markdown
# 论文标题（原文+中文译名）

## 基本信息
- **论文标题**：...
- **arXiv ID**：...
- **链接**：...
- **PDF**：`{output_dir}/{slug}/{arxiv_id}.pdf`

---

## 摘要
（翻译后的中文摘要，无公式则直接写文字）

---

## 目录
- [1. 章节名](#)
- [2. 章节名](#)
- ...

---

## 1. 章节名（翻译后的中文名）
（翻译后的完整内容，含 h3 子节。公式必须用 `$...$` 包裹。）

---

## 2. 章节名
...
```

### 步骤 5: 保存

保存为 `{output_dir}/{slug}/{arxiv_id}_中文文档.md`

### 步骤 6（可选）：基于文档生成技术演示 PPT

当用户要求"做成 PPT"、"生成演示文稿"、"做 slides"时，在完成中文文档后，使用 HTML 幻灯片技能生成演示文稿。

## 脚本说明

### `scripts/arxiv_section_extractor.py`

唯一的核心脚本，封装了所有自动化操作。

**用法：**
```bash
python3 arxiv_section_extractor.py <arxiv_id>
# 或
python3 arxiv_section_extractor.py https://arxiv.org/abs/2604.25836
# 指定输出目录
python3 arxiv_section_extractor.py 2604.25836 -o ~/papers
```

**依赖：** `requests`, `beautifulsoup4`

**功能：**
1. `extract_arxiv_id()` — 从 URL 或裸 ID 中提取 arxiv_id
2. `get_paper_info_from_abs()` — 从 abs 页面获取标题和三个 Access Paper 链接
3. `fetch_html_content()` — 获取 HTML 实验版全文（自动尝试 v1 和无后缀）
4. `extract_sections_from_html()` — 解析 h2 章节结构和 h3 子节
5. `save_section_files()` — 将各章节保存为独立文件，生成章节结构总览
6. `sanitize_title()` — 将标题转为安全目录名

**输出目录结构：**
```
{output_dir}/{title-slug}/
├── {arxiv_id}.pdf                    ← 原始 PDF
├── {arxiv_id}_中文文档.md            ← 最终中文文档（由 LLM 生成）
├── {arxiv_id}_metadata.json          ← 论文元数据
├── {arxiv_id}_section_structure.txt  ← 章节结构总览
└── {arxiv_id}_raw_sections/          ← 各章节原文
    ├── 00_abstract.txt
    ├── 01_Introduction.txt
    ├── 02_Section_Name.txt
    └── ...
```

## 输出示例

```
{output_dir}/strongly-quasi-pseudometric-aggregation-functions/
├── 2604.25836.pdf                    ← PDF
├── 2604.25836_中文文档.md            ← 中文文档
├── 2604.25836_metadata.json          ← 元数据
├── 2604.25836_section_structure.txt  ← 章节结构
└── 2604.25836_raw_sections/          ← 原文章节
    ├── 00_abstract.txt
    ├── 01_Introduction.txt
    ├── 02_Quasi-pseudometric_aggregation_functions.txt
    ├── 03_Strongly...on_products.txt
    └── 04_Strongly...on_sets.txt
```

## 注意事项

1. **公式定界符（关键！）**：翻译生成的中文文档中，所有 LaTeX 行内公式必须使用 **`$...$`** 作为定界符。**禁止使用** `\(...\)`（Typora 不渲染），也**禁止使用** ``$`...`$``（带反引号导致乱码）。生成后需用 `grep '$' 文档.md | head` 验证定界符正确。
2. **禁止 HTML 标签**：文档中**不得出现**任何 HTML 标签，包括 `<a id="...">` 锚点、`<br>` 换行等。目录无需带锚点链接，直接写 `- [章节名](#)` 或纯文本列表即可。
3. **翻译约定**：数学符号和 LaTeX 命令（如 `\mathcal`, `\text`, `\sum`）保留原样不翻译。技术术语（如 LLM, MLLM, DV, Agent 等）首字母缩写保留原文，可在其后括号加中文注释。不包含参考文献/引用内容（如 [1], [2] 等引用标记应删除）。
4. **章节跳过**：脚本自动跳过 References、Appendix、Supplementary 等附录章节。
5. **HTML 地址**：脚本自动尝试 `{id}v1` 和 `{id}` 两种地址格式。
6. **输出目录**：默认 `~/papers/`，可通过 `-o` 参数或 `ARXIV_PAPERS_DIR` 环境变量自定义。
7. **错误处理**：PDF 下载失败不影响章节提取；HTML 获取失败则终止流程。
