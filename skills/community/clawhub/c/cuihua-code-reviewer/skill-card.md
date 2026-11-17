## Description:

AI-powered code review assistant for OpenClaw agent developers that analyzes code quality, detects security and performance issues, and provides actionable improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review OpenClaw agent code for security vulnerabilities, performance issues, code quality problems, and best-practice gaps before committing or sharing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may copy detected passwords or API keys into plain Markdown files or shared summaries.

Mitigation: Review and redact reports before sharing or committing them, and add redaction, access controls, cleanup, and pinned dependencies before using the Slack, email, CI summary, cron, or API server examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-code-reviewer)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal summaries, Markdown reports, JSON reports, and code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a local code-review-report.md for detailed findings.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
