## Description:

Full project audit that launches five parallel AI agents for security, bugs, dead code, architecture, and performance, then compiles a unified report with health grading and actionable fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atobones](https://clawhub.ai/user/atobones)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill in Claude Code to review a project for security, correctness, dead code, architecture, and performance issues. It produces a prioritized audit report and can guide or apply targeted fixes after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer fetches mutable remote command files into persistent Claude command locations.

Mitigation: Review the packaged audit.md and install.sh before installation; prefer project-local installation from the packaged artifact or a pinned, verified release instead of curl-to-shell or mutable main downloads.

Risk: Auto-fix mode can rewrite project files without a final confirmation.

Mitigation: Run audits in report-only mode first; use fix commands only on a clean branch after reviewing the proposed changes and preparing tests or rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atobones/skills/claude-audit)
- [claude-audit homepage](https://github.com/atobones/claude-audit)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with structured findings, health grade, action plan, and optional fix guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can filter by audit area, changed files, severity, and top-N findings; auto-fix mode may apply code changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
