---
name: docx-chinese-baseline
slug: docx-chinese-baseline
displayName: Chinese DOCX Typesetting Baseline
version: "1.0.6"
description: "Locked design-token baseline for Chinese Word/DOCX documents and WeChat-native (公众号) article layouts: body 16px, section head 18px, title 23px, deep-blue #1a3a5c headings, no HTML tables/cards/backgrounds. Use when typesetting a Chinese DOCX or WeChat article, when html-to-docx output loses styles or fails on Windows, or when successive documents must stay visually consistent. Trigger keywords: 中文 docx 排版, Word 中文文档美化, html to docx 样式丢失, 16 18 23 px 基线, 深蓝标题, 公众号排版, 微信文章排版, WeChat article typesetting, 字号基线, font size baseline, Windows html-to-docx 失败, DOCX 样式. Baseline changes must update this skill first."
description_zh: "中文 Word 文档与公众号原生排版的锁定设计基线：正文 16px / 小标题 18px / 标题 23px、深蓝 #1a3a5c 标题色、禁 HTML 表格卡片背景、Windows html-to-docx 稳定转换路径。保证跨文档风格一致；基线变更必须先改本 skill。"
read_when: "Typesetting a Chinese DOCX or WeChat-native (公众号) article, aligning font/color tokens across documents, or when html-to-docx conversion loses styles or fails on Windows."
not_for:
  - English-language documents
  - PDF generation
  - Slides / PPT
  - Image-heavy poster design
agent_created: true
---

# Chinese DOCX Typesetting Baseline

Purpose: one locked baseline instead of per-task improvisation. Every Chinese DOCX produced from HTML follows the same token set, so successive documents look consistent and conversion failures have a known recovery path.

## Design Tokens (locked)

| Element | Token |
|---|---|
| Title (H1) | 23px, deep blue #1a3a5c, bold |
| Section head (H2) | 18px, deep blue #1a3a5c, bold |
| Body | 16px, dark gray/black |
| Heading color | #1a3a5c |
| WeChat-native layout | vertical info bars + plain editorial style; NO HTML tables, cards, backgrounds, popup grids |

## Workflow

1. [Deterministic] **Pick the target style**: WeChat-native article (strict no-table/no-card rules) or generic Word document (tables allowed, same font tokens).
2. [Deterministic] **Apply tokens**: set title 23px / section 18px / body 16px, heading color #1a3a5c in the source HTML or converter config before conversion.
3. [Deterministic] **Convert** with the html-to-docx pipeline.
4. [Deterministic] **Windows failure recovery**: if the bundled converter fails on Windows, follow the html-to-docx recovery skill: pre-process the HTML (strip unsupported CSS constructs), retry once; if still failing, rebuild the document programmatically (e.g. python-docx) applying the same tokens paragraph by paragraph.
5. [Deterministic] **Verify the output**: reopen the DOCX; confirm heading sizes 23/18/16 present, heading color #1a3a5c applied, CJK glyphs render correctly (no tofu), text remains editable (no flattened images); also confirm no HTML tables/cards/backgrounds and no converter-default spacing remain.

## Hard Rules

- Never flatten text to images; the DOCX must stay fully editable.
- WeChat-native layouts: no HTML tables, cards, background colors, or popup grids — vertical info bars only.
- Baseline changes (sizes, colors) must update this skill first, then the documents. No per-task deviation.
- Headings stay anchored to topic content (who / scene / problem), never filename-style titles.
- Line and paragraph spacing must be declared explicitly in the template; never inherit converter defaults, which differ between WPS and Word and silently produce inconsistent documents.
- Font names in the template must resolve to an installed CJK face on the target machine; an unresolved fallback is reported as a failure, not silently accepted from the converter.

## Failure Handling

- Converter crashes on Windows twice: switch to programmatic rebuild (python-docx) with the same tokens; do not debug the converter beyond two attempts.
- Styles lost after conversion: verify the HTML source carries inline styles or a converter-compatible stylesheet before blaming the converter; fix the source, reconvert once.
- CJK font issues: confirm the converter's font-fallback setting includes a Chinese font before changing the baseline.

## Output Format

Report: target style chosen → conversion path used (direct / recovery / programmatic) → verification checklist results (sizes, color, CJK glyph rendering, editability, no residual HTML tables/cards/backgrounds or converter-default spacing) → output file path.
