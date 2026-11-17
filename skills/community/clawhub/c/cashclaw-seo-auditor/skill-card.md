## Description:

Performs comprehensive SEO audits on websites covering technical SEO, on-page optimization, off-page signals, and performance metrics. Generates actionable reports with prioritized recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit websites for technical SEO, on-page SEO, off-page signals, and performance issues, then produce client-ready Markdown reports with prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch unrestricted URLs during website audits.

Mitigation: Use it only for domains the user is authorized to audit and run it in an isolated environment without access to internal networks or cloud metadata services.

Risk: The skill can write audit outputs to user-provided paths.

Mitigation: Direct outputs to a dedicated deliverables directory and check paths before execution to avoid overwriting unrelated files.

Risk: The install metadata references an unpinned npm package.

Mitigation: Prefer a pinned and reviewed CashClaw package version before trusting the installed cashclaw binary.

## Reference(s):

- [CashClaw SEO Auditor ClawHub skill page](https://clawhub.ai/andreataide86/skills/cashclaw-seo-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with supporting JSON audit data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown and JSON deliverables for audited domains when directed by the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
