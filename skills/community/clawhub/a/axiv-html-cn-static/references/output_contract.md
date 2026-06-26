# 输出契约：arXiv 中文静态 HTML

## 必需文件

- `index.html`：中文静态网页入口。
- `assets/`：本地化图片、图表、图标、CSS 资源。
- `{arxiv_id}_static_metadata.json`：论文标题、arXiv ID、链接、输出目录等。
- `{arxiv_id}_asset_manifest.json`：远程资源到本地文件的映射。
- `{arxiv_id}_figures.json`：图表、图片、标题与章节归属。

## 内容要求

- 中文正文应来自 arxiv-paper-resolver 风格的章节翻译文档。
- 保留论文自身章节结构。
- 公式保留 LaTeX 源文本，行内公式使用 `$...$`。
- 图表资源必须使用本地相对路径，例如 `assets/xxx.svg`、`assets/xxx.png`。
- 表格应作为 HTML `<table>` 节点出现在 `index.html` 中，而不是只保存 caption。
- 表格外层应使用 `.table-scroll` 横向滚动容器；不得保留 arXiv `ltx_transformed_outer` 中会裁切表格的固定 `height` 或 `transform: translate(...) scale(...)`。
- 宽表格允许横向滚动，但纵向必须完整展开，不应在表格内部出现很小的上下滚动窗口。
- 图表优先插入到中文正文中的显式引用附近；无显式引用时，按原文顺序分布在对应章节内部。
- 公式使用 MathJax 渲染。默认允许 `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js` 作为公式渲染脚本；若要求完全离线，需要将 MathJax 或 KaTeX 资源下载到 `assets/` 并改写脚本引用。
- 若仍出现远程 URL，应只作为论文链接、外部引用或 MathJax CDN；不应作为图片/CSS 必需资源。

## 推荐检查命令

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/arxiv_html_static_builder.py prepare 2604.27955 -o ./out
python3 scripts/arxiv_html_static_builder.py build ./out/gui-agents-with-reinforcement-learning-toward-digital-inhabitants --md ./out/gui-agents-with-reinforcement-learning-toward-digital-inhabitants/2604.27955_中文文档.md
find ./out/gui-agents-with-reinforcement-learning-toward-digital-inhabitants/assets -type f | head
grep -nE 'src="https?://|href="https?://arxiv.org/html' ./out/gui-agents-with-reinforcement-learning-toward-digital-inhabitants/index.html | head
```
