---
name: gbt-47041-autism-rehab
description: "Apply GB/T 47041-2026, the Chinese national standard for service quality and assessment of rehabilitation institutions for children with autism. Use when asked about GB/T 47041, 孤独症儿童康复机构服务质量及评价规范, autism rehabilitation institution compliance, service quality requirements, scoring, evaluation reports, checklists, parent satisfaction surveys, service流程, staffing ratios, facilities, rehabilitation training content, family support, or quality improvement."
---

# GB/T 47041 Autism Rehab

## Operating Rule

Treat `assets/GBT-47041-2026.md` as the authoritative source. Use the reference files for fast orientation, then verify exact clause text, page context, or scoring details from the PDF before making high-stakes claims.

Use this skill to:

- Interpret requirements in GB/T 47041-2026 for autism rehabilitation institutions.
- Build compliance checklists, evidence matrices, gap analyses, scoring sheets,整改建议, and evaluation report outlines.
- Explain service流程, staff配置, facility/equipment requirements, rehabilitation content, family support, satisfaction surveys, and evaluation implementation.
- Map institution evidence to the standard's 100-point evaluation structure.

## Fast Path

1. Read `references/gbt-47041-2026-operational-guide.md` for the summarized requirements and scoring framework.
2. Read `references/clause-map.md` when you need the section/page map.
3. Read `assets/GBT-47041-2026.md` directly for exact wording, or search it with the script:

```bash
python scripts/search_standard.py --query "家长满意度" --context 120
python scripts/search_standard.py --section "6.2"
python scripts/search_standard.py --list-sections
```

## Answering Style

- Cite the standard as `GB/T 47041-2026` and include clause numbers whenever practical.
- Distinguish normative clauses from informative appendices. Appendix A and Appendix B are informative references, not mandatory scoring rules by themselves unless used through a cited requirement.
- Quote sparingly. Prefer concise paraphrase plus clause/page reference; use exact quotation only when the user needs wording.
- Do not present the answer as legal, medical, licensing, or government certification advice. For official filing, accreditation, or dispute use, tell the user to verify against the source PDF and the competent authority.

## Evaluation Pattern

For compliance or scoring tasks, structure the work as:

1. Institution facts and evidence received.
2. Score by the three first-level indicators: service conditions 20, service norms 20, service effects 60.
3. Evidence gaps, risk notes, and required补充材料.
4. Grade: excellent >=90, good 80-89, qualified 60-79, unqualified <60.
5.整改建议 tied to the relevant clause or scoring item.

When evidence is missing, mark it as `待核验` rather than assuming compliance.
