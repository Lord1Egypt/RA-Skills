## Description:

Deep Reading guides an agent to read source texts chapter by chapter or section by section and produce structured close-reading notes with quotations, sentence analysis, interpretive commentary, cross-text links, practical insights, and unresolved questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy-c8](https://clawhub.ai/user/yy-c8)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run a Chinese close-reading workflow for books and long-form texts, creating persistent chapter notes and reading plans. It is intended for careful comprehension and knowledge management rather than fast summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes persistent reading notes, plans, and optional memory entries that may contain sensitive source text or user annotations.

Mitigation: Use it only with texts and notes the user is comfortable storing locally, and review the reading/ and memory file behavior before enabling recurring use.

Risk: The cron template can update reading progress and memory notes automatically if configured.

Mitigation: Enable scheduled runs only for approved projects and review generated notes before relying on them for study or knowledge management.

## Reference(s):

- [Book Types and Reading Amount Configuration](references/book-types.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, reading-plan files, quality-check reports, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured chapter notes under reading/, may update reading plans and memory notes, and includes an optional quality-check script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
