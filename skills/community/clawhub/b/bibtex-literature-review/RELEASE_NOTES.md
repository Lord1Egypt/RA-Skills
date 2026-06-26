# Release Notes

## v0.1.0

`bibtex-literature-review` 首个版本发布。这是一个面向 Codex / AI coding agent 的文献综述生成 skill，用于从结构化文献源生成可校验的 Word `.docx` 文献综述。

### 主要能力

- 支持从 BibTeX、RIS、CSL JSON、CSV/TSV 和普通参考文献列表中规范化文献元数据。
- 支持 GB/T 7714、APA、MLA、Chicago、IEEE、Vancouver、Harvard 等参考文献文本格式。
- 生成真正的 Word `REF` 交叉引用字段，而不是普通文本引用或 `HYPERLINK` 字段。
- 正文引用显示为上标数字标记，例如 `[1]`、`[3-5]`、`[10,11]`。
- 文末参考文献使用 Word 自动编号段落，XML 中包含 `w:numPr`。
- 为参考文献段落添加 `_RefBibNNN` bookmark，使正文引用可以跳转到对应文献。
- 支持将带 `[cite:1]`、`[cite:3-5]`、`[@citekey]` 标记的 Markdown 草稿转换为结构化 review JSON。
- Markdown 转换默认只保留正文实际引用的文献，并按首次引用顺序重编号。
- 提供 DOCX OOXML 校验脚本，检查 REF 字段、bookmark、正文上标、自动编号和 forbidden hyperlink。

### 推荐工作流

推荐使用 Zotero 整理文献元数据，通过 Better BibTeX 导出 `.bib` 文件，再让 Codex 使用本 skill 完成文献筛选、综述草稿、DOCX 构建和结构校验。

### 发布前验证

本版本已完成 release preflight 和端到端自检：

- BibTeX fixture 规范化为候选文献 JSON。
- review JSON 构建为 Word DOCX。
- 校验通过 6 个 Word REF 字段。
- 校验通过 5 个 `_RefBibNNN` bibliography bookmarks。
- 校验通过文末参考文献自动编号。
- 校验确认正文引用为上标。
- 校验确认未使用 `HYPERLINK` 字段冒充交叉引用。
- 包目录无 `__pycache__`、`.pyc`、临时 DOCX/PDF/PNG 等发布污染物。

### License

MIT
