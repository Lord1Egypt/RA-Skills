## Description:

Extracts key points, methods, results, conclusions, and simplified explanations from Chinese and English academic paper PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric060](https://clawhub.ai/user/eric060)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and developers use this skill to turn academic paper PDFs into structured summaries covering paper metadata, core questions, methods, findings, limitations, and plain-language explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF parsing dependencies could be installed from untrusted package sources.

Mitigation: Install only the stated PDF libraries from trusted package indexes and review dependency provenance before use.

Risk: Generated summaries could overwrite existing files when output paths are reused.

Mitigation: Choose output filenames or directories that do not conflict with existing summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric060/skills/academic-paper-summarizer)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-paper and batch workflows for Chinese and English academic papers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
