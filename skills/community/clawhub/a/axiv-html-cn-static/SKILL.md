---
name: arxiv-html-cn-static
description: This skill should be used when an arXiv paper HTML page needs to be converted into a local Chinese static HTML webpage, preserving local figures, icons, CSS assets, paper metadata, and Chinese text produced from arxiv-paper-resolver-style section extraction.
---

# arXiv 中文静态 HTML 网页生成技能

## 目标

将 arXiv 英文论文 HTML 实验版转换为本地可打开的中文静态 HTML 网页。保留论文标题、元数据、章节结构、公式文本、图片、图表、图标和 CSS 资源。中文正文可复用 `arxiv-paper-resolver` 的章节提取与中文 Markdown 生成流程。

## 触发场景

在以下请求中使用本技能：

- 将 arXiv 英文论文 HTML 转为中文 HTML 网页。
- 将 arXiv 论文做成本地静态网页、离线网页或中文网页。
- 要求保留 arXiv HTML 中的图片、图表、图标、CSS 或版式资源。
- 已有 `arxiv-paper-resolver` 生成的中文 Markdown，希望进一步生成本地 `index.html`。

## 资源

- `scripts/arxiv_html_static_builder.py`：下载 arXiv HTML、PDF、图片、图标、CSS 等本地资源，并把中文 Markdown 包装为静态 HTML。
- `scripts/requirements.txt`：脚本依赖。
- `references/output_contract.md`：输出目录、文件命名和质量检查约定。

## 工作流程

### Step 1：确认 arXiv ID

若用户提供的是 arXiv URL 或裸 ID，直接使用。若只提供 PDF 路径或论文标题，先根据标题搜索 arXiv，确认 `abs` 页面与 ID。

### Step 2：优先复用 arxiv-paper-resolver 生成中文 Markdown

若当前目录已有 `{arxiv_id}_中文文档.md`，直接复用。

若没有中文 Markdown，先使用 `arxiv-paper-resolver`：

1. 运行其章节提取脚本，获得 `{arxiv_id}_raw_sections/`、`{arxiv_id}_metadata.json`、`{arxiv_id}_section_structure.txt`。
2. 读取原文章节，翻译为中文 Markdown。
3. 保持公式为 `$...$`，避免使用 `\(...\)` 或带反引号的公式定界符。
4. 去除参考文献引用标记和 References/Appendix 正文，除非用户明确要求保留。

### Step 3：准备本地 HTML 资源

安装依赖后运行：

```bash
python3 -m pip install -r /Users/nineve/.codebuddy/skills/arxiv-html-cn-static/scripts/requirements.txt
python3 /Users/nineve/.codebuddy/skills/arxiv-html-cn-static/scripts/arxiv_html_static_builder.py prepare <arxiv_id_or_url> -o <output_parent_dir>
```

该步骤会：

- 拉取 arXiv `abs` 元数据。
- 获取 arXiv HTML 实验版。
- 下载 PDF。
- 下载并本地化 HTML 中的图片、图表、图标、CSS、CSS 中引用的资源。
- 生成本地化英文 HTML 副本。
- 提取图表清单，记录图表所属章节。

### Step 4：构建中文静态 HTML

使用已有中文 Markdown 构建网页：

```bash
python3 /Users/nineve/.codebuddy/skills/arxiv-html-cn-static/scripts/arxiv_html_static_builder.py build <paper_dir> --md <arxiv_id>_中文文档.md
```

默认输出：

```text
<paper_dir>/index.html
```

构建时将：

- 将中文 Markdown 转为静态 HTML。
- 将 arXiv HTML 中的 `figure` 与 `table` 节点作为完整 HTML 块插入，因此表格不会只剩 caption。
- 清理 arXiv 表格中的固定 `height`、`width`、`transform` 与 LaTeXML 缩放包裹，改用 `.table-scroll` 横向滚动容器，确保宽表格横向可滚、纵向完整展开。
- 优先按正文中出现的 `Figure N` / `Table N` / `图N` / `表N` 引用插入图表；若中文 Markdown 中没有显式引用，则按原文图表在该章节中的顺序分布到章节内部，而不是统一放在章节开头。
- 使用本地 CSS 样式生成适合阅读的中文论文网页。
- 保持所有图片和图表引用为本地相对路径。
- 默认引入 MathJax CDN 渲染 `$...$`、`$$...$$`、`\(...\)`、`\[...\]` 公式；完全离线环境下可改为本地 MathJax/KaTeX 资源。

### Step 5：质量检查

完成后检查：

```bash
grep -nE 'https?://arxiv.org|https?://static' <paper_dir>/index.html | head
find <paper_dir>/assets -type f | head
```

要求：

- `index.html` 能通过浏览器本地打开。
- 论文中的图片、图表、图标资源存在于 `assets/`。
- HTML 正文为中文。
- 公式保持 `$...$` 文本形式，不改写 LaTeX 命令。
- 不依赖远程 arXiv 图片资源；若仍有远程链接，只允许作为论文链接、arXiv 链接或外部引用链接存在。

## 输出目录结构

标准输出结构：

```text
{output_parent_dir}/{paper-title-slug}/
├── index.html                         # 中文静态网页
├── {arxiv_id}.pdf                     # PDF
├── {arxiv_id}_original_local.html     # 本地化英文 HTML 副本
├── {arxiv_id}_static_metadata.json    # 静态网页元数据
├── {arxiv_id}_asset_manifest.json     # 资源下载清单
├── {arxiv_id}_figures.json            # 图表清单
├── {arxiv_id}_中文文档.md              # arxiv-paper-resolver 生成或复用的中文 Markdown
└── assets/                            # 本地图片、图标、CSS 等资源
```

## 注意事项

- 保持 `arxiv-paper-resolver` 与本技能职责分离：前者负责章节抽取和中文正文生成，后者负责 HTML 资源本地化与静态网页构建。
- 对图表采用“按章节插入”的保守策略；若用户要求与原文完全同位插图，需要人工/LLM 根据原文 HTML 进一步调整图表位置。
- 不把外部 CDN 作为必要依赖，确保 `index.html` 尽量可离线阅读。
- 若 arXiv HTML 实验版不存在，报告无法生成 HTML 静态页，并建议退回 PDF/LaTeX 解析路线。
