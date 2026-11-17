## Description:

Exam paper OCR rebuilder with LLM audit that converts PDF or image exam papers into structured, editable outputs with OCR, question-type parsing, formula handling, and review notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, school operations teams, and education-technology developers use this skill to digitize exam papers from PDFs or images and rebuild them as editable exam content. It is intended to produce structured question data, review notes, and human-readable reports for downstream editing or import into question-bank workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute injected script content from untrusted exam inputs.

Mitigation: Review or sanitize generated HTML before opening it, especially when the original exam source is untrusted.

Risk: Exam content may be sent to external OCR or LLM providers during processing.

Mitigation: Use only exam files that the operator is allowed to share with the selected OCR and LLM services.

Risk: The skill relies on mutable external code or hosted assets for some report rendering behavior.

Mitigation: Prefer pinned dependencies and local or bundled report assets for deployment-sensitive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/exam-ocr-rebuilder)
- [Question type standards](references/question-types.md)
- [Output template](references/output-template.md)
- [LLM audit prompt template](references/llm-audit-prompt.md)
- [OCR tools comparison](references/ocr-tools-comparison.md)
- [HTML audit report template](references/html-template-audit.html)
- [Sample exam data](references/sample_exam_data.json)
- [Sample exam report](references/sample_exam_report.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, Markdown, and interactive HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OCR text, structured exam sections, answers, explanations, LaTeX formulas, audit logs, and optional report assets.]

## Skill Version(s):

1.0.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
