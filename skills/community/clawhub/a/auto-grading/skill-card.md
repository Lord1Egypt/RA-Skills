## Description:

智能批改作业 supports automated review of graduation design and thesis archives by extracting doc, docx, pdf, and pptx content, scoring documents, checking cross-document consistency, reviewing defense slides, and validating references against GB/T 7714.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, reviewers, and academic staff use this skill to review student graduation design or thesis archives, produce evidence-backed scoring, and summarize required revisions across documents and defense slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive student or institutional documents and writes extracted plaintext to local temporary storage.

Mitigation: Run it only in a restricted workspace, review the archive contents before processing, and clean /tmp/auto_grading after use.

Risk: The evidence guardrail may validate evidence against the wrong document when filenames or evidence overlap.

Mitigation: Manually check source filenames and quoted evidence for high-impact findings, and treat automatically verified findings as review aids rather than final determinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingsunzhang2026-oss/skills/auto-grading)
- [GB/T 7714-2015 Reference Guide](references/gbt7714.md)
- [Review Template](references/review_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured JSON for harness validation followed by Markdown review reports with scoring tables and issue lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issues are expected to include source file, evidence text, and confidence labels before final reporting.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
