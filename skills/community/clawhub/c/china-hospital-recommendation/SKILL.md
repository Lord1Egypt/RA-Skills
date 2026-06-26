---
name: China-hospital-recommendation-report
description: Generate English hospital recommendation reports for medical travel to China, hospital matching, and redo orders. Use when needs to turn user intake data into a premium deliverable with exactly 3 recommended hospitals by default, specialist-direction guidance, cost and logistics advice, evidence notes, and final Markdown/PDF export. Triggers on mentions of China hospital report, custom China medical travel report, China hospital matching deliverable, report redo, or premium PDF export.
---

# Hospital Recommendation Report

## Overview

Generate a self-contained premium report for paid users who need hospital matching guidance in China. The skill carries its own product brief, ranking snapshot, recommendation method, search policy, schema, and PDF rules; do not depend on repo-external references when using it.

## Resources To Read

- [references/product-brief.md](references/product-brief.md): report purpose, user promise, and scope boundaries
- [references/report-schema.md](references/report-schema.md): `ReportRequest`, `ReportResearchModel`, and `RenderedReportModel`
- [references/specialty-mapping.md](references/specialty-mapping.md): convert case descriptions into Fudan specialty keys
- [references/fudan-rankings-2025.md](references/fudan-rankings-2025.md): bundled static ranking baseline
- [references/recommendation-method.md](references/recommendation-method.md): hospital and specialist recommendation logic
- [references/search-policy.md](references/search-policy.md): what may be searched at generation time
- [references/pdf-spec.md](references/pdf-spec.md): premium PDF expectations
- [references/quality-checklist.md](references/quality-checklist.md): final QA gate

## Workflow

1. Confirm the task is a paid deliverable, not a casual answer.
2. Read the product brief and schema before drafting.
3. Map the condition to one or more specialties with `references/specialty-mapping.md`.
4. Use `references/fudan-rankings-2025.md` as the static ranking baseline. Do not search the web for Fudan rankings during generation.
5. Search only for dynamic facts allowed by `references/search-policy.md`, such as international services, department pages, specialist public profiles, JCI status, visa, transportation, and accommodation.
6. Build a `ReportResearchModel`, separating static facts, current search-backed facts, and recommendation judgments.
7. Produce a `RenderedReportModel` in English. Default to exactly 3 hospitals unless the payload includes a justified expansion reason. Prefer structured access-evidence and scenario-cost fields when the evidence is available.
8. Run `scripts/render_report.py` to export Markdown and PDF.
9. Review the output against `references/quality-checklist.md` before returning it.

## Output Rules

- Default delivery language is patient-facing English.
- Default hospital count is 3.
- Include specialist direction or department-lead guidance for the case; do not invent named doctors when public evidence is thin.
- When staging, pathology, receptor status, or treatment sequence are still unclear, default specialist guidance to evaluation-first or MDT-first rather than procedure-first.
- Keep hospital Chinese names as supporting labels only.
- Treat JCI as a positive recommendation factor when verified, but not as a hard requirement.
- Use evidence notes to explain what came from the bundled ranking baseline and what needs current verification.
- Separate administrative intake, record-review workflow, and doctor-led remote consultation. Do not imply teleconsult availability unless it is explicitly verified.
- Prefer scenario-based cost framing. If costs are high-uncertainty, say so directly instead of presenting a false sense of precision.
- Keep the report scoped to hospital matching, specialist direction, cost guidance, travel logistics, next steps, and disclaimer text.
- For PDF delivery, prefer the built-in `reportlab` premium renderer; keep Markdown as the editable intermediate artifact and use the `pandoc` path only as fallback.
- Follow the ChinaMed design-system palette for premium PDF styling instead of inventing a separate visual theme.
- Always append the ChinaMed Select consult-service sentence to the final Disclaimer in both Markdown and PDF output.

## Export

Generate Markdown and PDF:

```bash
python3 .agents/skills/hospital-recommendation-report/scripts/render_report.py input.json --output-dir output
```

Generate Markdown only:

```bash
python3 .agents/skills/hospital-recommendation-report/scripts/render_report.py input.json --output-dir output --skip-pdf
```
