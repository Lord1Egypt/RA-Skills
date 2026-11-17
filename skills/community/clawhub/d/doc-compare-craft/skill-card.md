## Description:

Compares two document versions and helps an agent generate interactive HTML views with side-by-side, inline, unified, word-level, legal redline, summary, and structural diff modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to compare old and new versions of contracts, technical plans, reports, standards, code-like text, and other documents. It guides the agent to summarize changes and produce visual diff outputs suited to review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source documents may contain secrets, personal data, confidential business terms, or regulated information.

Mitigation: Use only documents the user is authorized to share with the agent, and redact sensitive content before comparison when possible.

Risk: Legal redline or contract-change summaries may be incomplete or may miss business context.

Mitigation: Treat generated comparisons as review aids and require legal or subject-matter review before relying on them for decisions.

Risk: Bundled HTML template files are placeholders, so final visual output quality depends on the agent's generated implementation.

Mitigation: Review generated HTML before sharing it externally, especially for legal, customer-facing, or archival workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/doc-compare-craft)
- [Project homepage](https://github.com/wwbwin/clawhub-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and generated single-file HTML with inline CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports seven documented comparison modes and four color themes; generated HTML is intended to be self-contained with no external CDN, font, or icon dependencies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
