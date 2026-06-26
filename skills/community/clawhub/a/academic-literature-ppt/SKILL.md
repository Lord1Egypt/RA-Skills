---
name: academic-literature-ppt
description: Create academic literature review presentation slides (PPTX) from research papers or articles. Use when the user wants to summarize academic literature into a presentation, create a literature report PPT/slides, convert research papers into presentation format, make an academic paper summary presentation, produce a journal club or paper review slide deck, or summarize a scientific article for group meeting presentation. The skill produces blue-themed academic style slides with Chinese translations of original literature content. Triggers on requests involving literature summary presentations, paper report PPTs, academic review slides, journal club slides, group meeting literature reports, or any task requiring conversion of research articles into structured presentation format.
---

# Academic Literature Presentation Skill

Create professional academic presentation slides (PPTX) summarizing research literature. Content is translated into Chinese while strictly preserving original citations and all figures/tables from the source paper.

## Reference Source

- **Reference type**: Uploaded artifact (PPTX)
- **Reference artifact type**: PPTX
- **Reference File Type**: PPTX
- **Primary language**: Chinese (translated from English literature)

## Supported Outputs

- PPTX (default)

## Default Output Selection

- When user does not specify format, produce PPTX

## Workflow

1. **Read and understand the source literature** (PDF or other format)
   - Extract the full structure: introduction, literature review, hypotheses, theoretical model, methods, results (all figures and tables), discussion, conclusions
   - Identify all figures, tables, and charts to preserve
   - Note all citation formats (Author, Year) to preserve exactly

2. **Translate content to Chinese** following strict rules:
   - Translate only from the original literature text
   - Do NOT fabricate, invent, or modify content beyond translation
   - Preserve all citation formats exactly as (Author, Year) or (Author1 & Author2, Year)
   - Keep all statistical values, p-values, effect sizes exactly as reported

3. **Structure the presentation** according to `references/structure_contract.md`

4. **Apply the visual style** according to `references/style_contract.md`

## Critical Content Rules

1. **Translation fidelity**: Only translate what exists in the original literature. Never invent hypotheses, results, or conclusions not present in the source.
2. **Citation preservation**: Keep all citations in original (Author, Year) format. Do not translate author names.
3. **Figure/table preservation**: Include ALL figures and tables from the original paper. None should be omitted.
4. **Statistical accuracy**: Report exact statistical values (F, p, t, Cohen's d, R-squared, etc.) without rounding or modification.
5. **Model diagrams**: Recreate theoretical model/hypothesis diagrams from the literature, preserving all variable names and arrow relationships.

## Style and Structure Contracts

- **Style contract**: Read `references/style_contract.md` for complete visual style specification including color palette, typography, layout patterns, and critical anti-patterns to avoid.
- **Structure contract**: Read `references/structure_contract.md` for complete content structure specification including required sections, content rules, and citation handling.

## Font Strategy

- **Primary font**: Microsoft YaHei (微软雅黑) for all text
- **Fallback CJK fonts**: PingFang SC, Noto Sans CJK SC, Source Han Sans SC
- All text paths (headings, body, tables, captions, cover) use the same font family for consistency

## Notes on Implementation

This skill produces PPTX-format artifacts but does not prescribe any specific implementation library or tool for slide creation. The style and structure contracts are artifact-level specifications that guide any compliant implementation approach.
