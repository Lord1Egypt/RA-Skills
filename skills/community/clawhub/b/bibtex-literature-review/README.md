# BibTeX Literature Review

> 中文主文档。English version: [README.en.md](README.en.md)

`bibtex-literature-review` 是一个面向 Codex / AI coding agent 的文献综述生成 skill。它的目标不是简单把参考文献粘进 Word，而是从 Zotero/BibTeX/RIS/CSL JSON 等文献源出发，生成带有 **Word REF 交叉引用字段**、**正文上标数字引用**、**自动编号参考文献列表** 的 `.docx` 文献综述。

这个 skill 特别适合中文论文、课程报告、开题报告、毕业论文前期综述、管理学/社科类文献综述，也可以用于英文综述草稿。

## 核心能力

- 从 `.bib`、`.ris`、CSL JSON、CSV/TSV、普通参考文献列表中提取文献元数据。
- 支持 GB/T 7714、APA、MLA、Chicago、IEEE、Vancouver、Harvard 等参考文献文本格式。
- 生成 Word `.docx`，正文引用使用真正的 `REF` 字段，而不是普通文本或 `HYPERLINK`。
- 正文引用显示为上标，例如 `[1]`、`[3-5]`、`[10,11]`。
- 文末参考文献使用 Word 自动编号段落，XML 中包含 `w:numPr`。
- 每条参考文献带 `_RefBibNNN` bookmark，正文引用可以跳转到对应文献。
- 提供结构化校验脚本，检查 REF 字段、bookmark、自动编号、上标和 forbidden hyperlink。
- Markdown 草稿转换时默认只保留正文实际引用的文献，并按首次引用顺序重编号。

## 推荐最佳实践：Zotero + BibTeX + Codex

最稳的使用方式是：

1. 在 Zotero 中整理文献，补全作者、题名、期刊、年份、卷期、页码、DOI 等字段。
2. 使用 Zotero 的 Better BibTeX 导出 `.bib` 文件。
3. 把 `.bib` 文件、综述主题、目标字数、引用格式要求交给 Codex。
4. 让 Codex 使用本 skill 完成文献筛选、综述草稿、DOCX 构建和结构校验。
5. 最后人工检查参考文献格式、标题大小写、专有名词、机构格式要求。

推荐对 Codex 这样描述任务：

```text
请使用 bibtex-literature-review skill。
文献源是 /path/to/refs.bib，由 Zotero Better BibTeX 导出。
请围绕“{你的论文题目}”写一篇中文文献综述，约 3000 字。
参考文献格式使用 GB/T 7714，正文使用上标数字引用。
输出 Word DOCX，并运行 REF/自动编号/上标校验。
```

如果学校、期刊或机构对参考文献标点特别严格，也可以先在 Zotero 中直接导出指定样式的 formatted bibliography，再作为普通参考文献列表输入。本 skill 会继续负责正文综述、引用选择、Word REF 字段和 DOCX 校验。

## 输入格式

支持的文献源：

- `.bib` / `.bibtex`: 推荐使用 Zotero Better BibTeX 导出。
- `.ris`: Zotero、EndNote、Web of Science、CNKI 等常见工具导出。
- `.json` / `.csljson`: CSL JSON，适合更规范的结构化元数据。
- `.csv` / `.tsv`: Zotero、EndNote、Excel 风格表格。
- `.txt` / `.md`: 已经排好格式的参考文献列表。

支持的 Markdown 引用标记：

```markdown
这是单篇引用[cite:1]。
这是连续引用[cite:3-5]。
这是组合引用[cite:10,11]。
这是按 citekey 引用[@liu2025]。
这是多个 citekey 引用[@liu2025; @zhang2024]。
```

Markdown 转 review JSON 时，默认会过滤未引用文献：

```bash
python scripts/markdown_review_to_json.py draft.md --refs candidates.json --out review.json
```

只有在用户明确希望保留未引用文献时，才使用：

```bash
python scripts/markdown_review_to_json.py draft.md --refs candidates.json --out review.json --keep-unused
```

## 基本工作流

### 1. 规范化文献源

```bash
python scripts/sources_to_json.py refs.bib --style gbt7714 --out candidates.json
```

常见样式：

```bash
python scripts/sources_to_json.py refs.bib --style apa --out candidates_apa.json
python scripts/sources_to_json.py refs.bib --style ieee --out candidates_ieee.json
python scripts/sources_to_json.py refs.ris --style vancouver --out candidates_vancouver.json
```

可以用关键词快速缩小范围：

```bash
python scripts/sources_to_json.py refs.bib --contains 激励 --contains satisfaction --out candidates.json
```

### 2. 选择实际使用的文献

最终参考文献列表应该只包含正文实际引用的文献。默认建议：

- 先由 Codex 根据综述主题从 `candidates.json` 中选择相关文献。
- 写作时只引用被选中的文献。
- 若从 Markdown 草稿转换，使用默认过滤行为自动移除未引用条目。
- 编号按照正文首次引用顺序排列，除非用户明确要求其他排序方式。

### 3. 编写 review JSON

DOCX 构建器使用结构化 JSON，而不是普通纯文本引用：

```json
{
  "title": "Mock 文献综述",
  "references": [
    {
      "gbt": "张三. 示例研究主题的理论基础与发展趋势[J]. 示例期刊, 2025, 12(3): 45-56."
    },
    {
      "gbt": "Li Ming. Mock evidence on organizational practice and technology adoption[J]. Journal of Example Studies, 2024, 8(2): 101-118."
    }
  ],
  "paragraphs": [
    [
      "已有研究表明，示例研究主题可以从理论基础、实践机制与情境因素三个层面展开分析",
      {"cite": 1},
      "；同时，组织实践与技术采纳之间的关系也为后续研究提供了经验参照",
      {"cite": 2},
      "。"
    ]
  ]
}
```

引用对象规则：

- `{"cite": 1}` -> `[1]`
- `{"cite": [3, 4, 5]}` -> `[3-5]`
- `{"cite": [10, 11], "collapse": false}` -> `[10,11]`

完整 JSON 规范见 [references/review-json-spec.md](references/review-json-spec.md)。

### 4. 构建 DOCX

```bash
python scripts/build_docx_from_review_json.py review.json --out output.docx
```

### 5. 校验 DOCX

```bash
python scripts/validate_docx_crossrefs.py output.docx \
  --expect-bib-count 12 \
  --forbid-hyperlinks \
  --require-ref \
  --require-superscript \
  --require-auto-numbered-bib
```

验收重点：

- 正文引用必须是 Word `REF` 字段，不是 `HYPERLINK`。
- 正文引用必须是上标。
- 文末参考文献必须是 Word 自动编号段落。
- 每个正文引用都能对应 `_RefBibNNN` bookmark。
- 文献列表只包含正文实际引用的文献。
- 如果环境支持渲染和多模态检查，应该检查 PNG 页面，确认没有双括号、字段代码泄露、文本重叠或引用丢失。

详细验收标准见 [references/acceptance.md](references/acceptance.md)。

## 引用风格说明

这个 skill 区分两层：

- 正文引用机制：默认使用 Word `REF` 字段，显示为数字上标。
- 参考文献文本格式：GB/T 7714、APA、MLA、Chicago、IEEE、Vancouver、Harvard 等。

需要注意：

- APA、MLA、Chicago author-date 等风格通常不是数字上标引用。如果用户要求保留 Word REF 跳转能力，本 skill 默认只把这些风格应用到文末参考文献文本。
- IEEE、Vancouver、GB/T 7714 更适合默认数字引用流程。
- 内置 formatter 是确定性 baseline，不是完整 CSL 引擎。出版级格式应人工复核，或优先使用 Zotero/CSL 生成 formatted references。

大小写规范：

- 优先保留 Zotero / BibTeX / CSL JSON 中的原始大小写。
- 不要全局强制小写，避免破坏 AI、HRM、ESG、DNA、OECD 等缩写和专有名词。
- APA/Harvard 的 sentence case、MLA/Chicago 的 title case 如果要求严格，应由人工或专门 CSL 工具复核。
- 中文题名一般不做大小写处理，只清理明显空格和标点问题。

详细规则见 [references/citation-styles.md](references/citation-styles.md)。

## 使用规范

### 应该做

- 使用 Zotero 或其他文献管理工具维护干净元数据。
- 优先使用 Zotero Better BibTeX 导出的 `.bib`。
- 明确告诉 Codex：主题、语言、目标字数、引用格式、输出路径。
- 只引用实际支撑正文观点的文献。
- 生成 DOCX 后必须运行结构校验。
- 严格场景下，人工复核参考文献标点、大小写、作者名、DOI、页码。

### 不应该做

- 不要把正文引用写成普通文本 `[1]` 后直接交付。
- 不要用 `HYPERLINK` 字段冒充 Word 交叉引用。
- 不要让未引用文献留在文末参考文献列表。
- 不要凭空补 DOI、页码、卷期、出版社、出版地。
- 不要默认联网补全文献元数据，除非用户明确要求。
- 不要直接修改用户提供的样例 Word 文件，除非用户明确要求。

## 脚本说明

- [scripts/sources_to_json.py](scripts/sources_to_json.py): 将 BibTeX、RIS、CSL JSON、CSV/TSV、普通参考文献列表转换为候选 JSON。
- [scripts/bibtex_to_json.py](scripts/bibtex_to_json.py): 兼容旧流程的 BibTeX-only parser，适合常见 Zotero/Better BibTeX 输出。
- [scripts/markdown_review_to_json.py](scripts/markdown_review_to_json.py): 将带 `[cite:1]` 或 `[@key]` 的 Markdown 草稿转换为 review JSON。
- [scripts/build_docx_from_review_json.py](scripts/build_docx_from_review_json.py): 从 review JSON 构建带 REF 字段的 DOCX。
- [scripts/validate_docx_crossrefs.py](scripts/validate_docx_crossrefs.py): 检查 DOCX OOXML 中的 REF、bookmark、上标、自动编号和 hyperlink。
- [scripts/self_check.py](scripts/self_check.py): 端到端自检，检查 skill 包卫生、脚本语法、DOCX 交叉引用回归。

## 自检

使用真实 BibTeX fixture 运行：

```bash
python scripts/self_check.py --bib /path/to/refs.bib
```

自检会在临时目录中完成：

- 解析 BibTeX。
- 生成候选文献 JSON。
- 构建 review JSON。
- 生成 DOCX。
- 校验 REF 字段、自动编号、bookmark、上标。
- 检查 skill 目录没有 `__pycache__`、临时 DOCX/PDF/PNG 等污染物。

## 适用边界

适合：

- 中文论文/报告文献综述。
- 需要 Word 可点击交叉引用的 DOCX。
- 使用 Zotero 管理文献，并希望 Codex 自动完成初稿和结构校验。
- GB/T 7714、IEEE、Vancouver 等数字引用工作流。

不适合直接承诺：

- 完全出版级 APA/MLA/Chicago 格式，无人工复核。
- 复杂 BibTeX 宏、`@string`、大量自定义 LaTeX 命令的完整解析。
- 替代 Zotero、EndNote、CSL 引擎或学校官方格式模板。

## 参考文档

- 工作流：[references/workflow.md](references/workflow.md)
- 输入格式：[references/input-formats.md](references/input-formats.md)
- 引用风格：[references/citation-styles.md](references/citation-styles.md)
- GB/T 7714：[references/gbt7714-bibtex.md](references/gbt7714-bibtex.md)
- Review JSON：[references/review-json-spec.md](references/review-json-spec.md)
- Word REF / OOXML：[references/ooxml-ref-fields.md](references/ooxml-ref-fields.md)
- 验收标准：[references/acceptance.md](references/acceptance.md)

## License

MIT License. See [LICENSE](LICENSE).
