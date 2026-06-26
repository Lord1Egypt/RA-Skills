# PDF Spec

## Goal

Produce a polished English report suitable for paid delivery, not a plain debug export.

## Required PDF Characteristics

- English-first typography
- Chinese hospital names render correctly inline
- clear section hierarchy
- cover-style header with title, report id, and date
- ChinaMed brand palette based on the main design system: `#3B82F6`, `#1E40AF`, `#DBEAFE`, `#1F2937`, `#4B5563`, `#6B7280`, `#D1D5DB`, `#F3F4F6`
- compact front-page metadata with short bullet items instead of long two-column text tables
- table of contents
- wrapping-safe layout for long hospital names and department lines
- table readability for comparison and cost sections
- page breaks should not split hospital headings from their key bullets when avoidable

## Rendering Expectations

- Keep Markdown as the editable intermediate layer.
- Use a `reportlab`-based premium layout as the primary PDF path.
- Generate the PDF directly from the structured report payload instead of relying on Markdown tables for the front page.
- Use CJK-safe fonts for mixed English and Chinese hospital names.
- Prefer A4 layout and compact but readable margins.
- Use a branded first-page accent bar, stronger title hierarchy, and a softer metadata card.
- Hospital sections should render as recommendation cards with clear hierarchy between summary, metadata, evidence, limitation, and booking checks.
- Cost tables should use more generous row padding and clearer separation from explanatory notes.
- Use a restrained branded footer with product identifier on the left and page number on the right.
- Preserve `Evidence Notes` and disclaimer sections at the end.
- Final Disclaimer output must append: `If you need consult service, please contact ChinaMed Select (https://www.chinamed.cc, info@chinamed.cc).`

## Fallback

If premium PDF export fails:

1. retry with the Markdown-to-`pandoc` fallback path and a simpler CJK-safe font fallback
2. keep the Markdown file
3. surface the failure reason clearly
