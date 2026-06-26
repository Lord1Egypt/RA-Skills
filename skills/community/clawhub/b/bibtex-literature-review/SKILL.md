---
name: bibtex-literature-review
description: Build Word literature reviews from BibTeX, RIS, CSL JSON, CSV/TSV, or plain reference lists with GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, or Harvard bibliography formatting and clickable Word REF citations. Use when Codex must parse literature source files, write Chinese or English reviews, generate .docx documents with superscript numeric citations, avoid HYPERLINK fields, enforce Word automatic numbered bibliography paragraphs, or validate REF/bookmark/numbering OOXML behavior.
---

# BibTeX Literature Review

## Purpose

Create `.docx` literature reviews from literature-source metadata with Chinese thesis-style numeric citations, clickable Word `REF` fields, superscript citation markers, and a bibliography that uses real Word automatic numbering paragraphs.

This skill is intentionally strict because Word cross-reference OOXML is fragile. Do not hand-wave the citation layer: generate, inspect, render, and validate.

## Boundaries and Isolation

- Treat sample Word files as read-only style/behavior references unless the user explicitly asks to edit them.
- Do not perform external metadata lookup unless the user asks for web/library enrichment; format only from provided metadata by default.
- Keep source normalization, review drafting, DOCX building, and DOCX validation as separate steps. Do not hide malformed reference data by silently fabricating missing fields.
- Keep generated task artifacts outside the skill directory unless they are deliberate reusable resources. Do not leave `__pycache__`, test DOCX files, temporary JSON, or rendered pages inside the skill package.
- Default APA/MLA/Chicago/Harvard support applies to bibliography text. Keep numeric clickable Word `REF` body citations unless the user explicitly asks for a non-numeric in-text citation system.
- Use bundled scripts through explicit input/output paths. Scripts may write the requested output file and temporary working directories, but should not modify source files in place.

## Core Workflow

1. Inspect the user inputs:
   - Literature source file path (`.bib`, `.ris`, `.json`, `.csv`, `.tsv`, `.txt`, `.md`) or curated reference JSON.
   - Sample Word file, if provided, for style and field behavior only.
   - Topic, word count, target language, and output path.
2. Normalize the source structurally. Do not rely on ad hoc string slicing for authors, titles, journals, years, volume/issue, or pages.
3. Select only the references actually used in the review. Keep numbering in first-citation order unless the user asks for another order.
4. Draft the review text with explicit citation markers as data, not as plain text.
5. Convert references to the requested bibliography style from available metadata. Default to GB/T 7714 for Chinese thesis tasks. Do not invent missing volume, issue, page, DOI, publisher, or place fields.
6. Build the DOCX with `scripts/build_docx_from_review_json.py` or an equivalent OOXML implementation.
7. Validate the DOCX with `scripts/validate_docx_crossrefs.py`.
8. Prefer code-level DOCX validation first. Render the DOCX when a renderer is available; if the active AI environment supports multimodal inspection, inspect PNG pages and iterate until clean.

## Required REF Pattern

Use this default pattern unless the user explicitly asks for a different field-code variant:

- Body citations are complex Word fields whose instruction text contains `REF _RefBibNNN \h`.
- Body citation display is superscript, including brackets, commas, and ranges.
- Bibliography paragraphs use real Word automatic numbering (`w:numPr`) with visible marker format `[%1]`.
- Each bibliography paragraph also contains a hidden bookmarked digit run (`_RefBibNNN`) so body REF fields return a clean digit. This avoids the double-bracket bug produced when `REF ... \n` reads an already bracketed list marker.

Read [references/ooxml-ref-fields.md](references/ooxml-ref-fields.md) before changing the citation implementation, especially if the user asks for exact `REF ... \n \h` field codes.

## JSON Build Contract

For repeatable generation, create a review JSON object and pass it to the builder:

```json
{
  "title": "文献综述",
  "references": [
    {"gbt": "刘颖. 数字化转型背景下企业人力资源管理模式创新研究[J]. 知识经济, 2025(33): 157-159, 163."}
  ],
  "paragraphs": [
    [
      "数字化转型正在重塑企业人力资源管理的逻辑。刘颖认为，数据驱动和员工体验重构成为提升人才竞争优势的重要路径",
      {"cite": 1},
      "。"
    ]
  ]
}
```

Citation values:

- `{"cite": 1}` creates superscript `[1]`.
- `{"cite": [3, 4, 5]}` creates superscript `[3-5]` by default.
- `{"cite": [10, 11], "collapse": false}` creates superscript `[10,11]`.

Read [references/review-json-spec.md](references/review-json-spec.md) for the full JSON schema and examples.

## Resource Routing

- For BibTeX selection and GB/T 7714 formatting rules, read [references/gbt7714-bibtex.md](references/gbt7714-bibtex.md).
- For APA, MLA, Chicago, IEEE, Vancouver, Harvard, and the distinction between bibliography style and Word REF body citations, read [references/citation-styles.md](references/citation-styles.md).
- For RIS, CSL JSON, CSV/TSV, plain references, or Markdown drafts, read [references/input-formats.md](references/input-formats.md).
- For Word REF fields, bookmarks, automatic numbering, hidden anchors, and known failure modes, read [references/ooxml-ref-fields.md](references/ooxml-ref-fields.md).
- For a step-by-step production checklist, read [references/workflow.md](references/workflow.md).
- For acceptance criteria and command-line checks, read [references/acceptance.md](references/acceptance.md).

## Non-Negotiable Acceptance Gate

Before delivering a `.docx`, confirm all of the following:

- 正文引用是 Word `REF` 字段，不是 `HYPERLINK`。
- 正文引用显示为上标。
- 文末参考文献是 Word 自动编号段落，XML 中有 `w:numPr`。
- 每条正文引用都有可跳转到参考文献位置的 `_RefBibNNN` 锚点。
- 组合引用能正常显示，例如 `[3-5]`、`[4,5]` 或 `[10,11]`。
- 参考文献列表只包含正文实际引用的文献。
- 渲染后的页面没有引用丢失、双括号、字段占位符、重叠或明显排版问题。

Use:

```bash
python scripts/validate_docx_crossrefs.py output.docx --expect-bib-count 12 --forbid-hyperlinks --require-ref --require-superscript --require-auto-numbered-bib
```

Then render and visually inspect with the available DOCX renderer.

## Helpful Scripts

- `scripts/sources_to_json.py`: normalize `.bib`, `.ris`, CSL JSON, CSV/TSV, or plain reference lists into JSON candidates.
- `scripts/bibtex_to_json.py`: backwards-compatible BibTeX-only parser.
- `scripts/markdown_review_to_json.py`: convert Markdown review drafts with `[cite:1]` or `[@key]` markers into review JSON.
- `scripts/build_docx_from_review_json.py`: build the final `.docx` from curated review JSON.
- `scripts/validate_docx_crossrefs.py`: inspect DOCX OOXML for REF fields, superscript results, forbidden hyperlinks, bookmarks, and bibliography numbering.
- `scripts/self_check.py`: run an isolated end-to-end regression check against a real BibTeX fixture; fails on package pollution, invalid frontmatter, malformed scripts, or DOCX cross-reference regressions.
