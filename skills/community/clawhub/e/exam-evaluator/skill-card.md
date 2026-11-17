## Description:

Extracts questions from XLSX, XLS, DOCX, and PDF exam materials, evaluates item-writing quality across content validity, structural validity, difficulty control, discrimination potential, and standardization, and produces an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, assessment designers, and training teams use this skill to review exam or question-bank quality, compare papers, and produce visual reports with targeted improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include confidential exam or question-bank content and may load Chart.js from a CDN.

Mitigation: Use a local or integrity-pinned Chart.js copy and avoid opening generated HTML with network access when working with confidential materials.

Risk: The workflow references helper scripts for parsing, metrics, duplicate detection, validation, and report generation that are not included in the provided artifact evidence.

Mitigation: Confirm the required helper scripts are supplied and reviewed before relying on the workflow for full report generation.

Risk: The skill evaluates educational assessment quality, so parsing errors or subjective scoring can produce misleading recommendations.

Mitigation: Review low-confidence parsing, suspicious answers, content-alignment flags, and final reports before using recommendations for exam decisions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/flyboat403/exam-evaluator)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/exam-evaluator)
- [Evaluation criteria](references/evaluation_criteria.md)
- [Bloom taxonomy](references/bloom_taxonomy.md)
- [Question types](references/question_types.md)
- [Vocational standards](references/vocational_standards.md)
- [Chart.js distribution used by generated reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON structures, shell commands, and generated HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary artifact behavior produces output/report.html; optional per-question CSV export may be available from the report.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
