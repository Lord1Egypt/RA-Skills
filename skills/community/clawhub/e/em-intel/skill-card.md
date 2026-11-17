## Description:

Engineering Manager Intelligence tracks team performance, engineer contributions, and project health across GitLab/GitHub and Jira/GitHub Issues, including briefings, reports, branch-to-ticket mapping, and optional Slack, Telegram, or email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larryfang](https://clawhub.ai/user/larryfang)

### License/Terms of Use:

MIT-0

## Use Case:

Engineering managers, team leads, and delivery stakeholders use this skill to generate morning briefs, end-of-day reviews, team performance reports, contribution maps, quiet-engineer alerts, epic health checks, and weekly newsletters from code and ticketing systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful service credentials for code, ticketing, and delivery systems.

Mitigation: Use dry-run or print mode first, keep the skill directory private, and use fine-grained least-privilege tokens with expirations.

Risk: Credential setup writes secrets to a local .env file and may prompt for tokens in a terminal.

Mitigation: Ensure .env is owner-readable only, avoid entering tokens in recorded or shared terminals, and verify GitLab and Jira URLs are HTTPS and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larryfang/skills/em-intel)
- [SETUP.md](artifact/SETUP.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text reports with console tables, shell command snippets, and optional HTML email rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run output with synthetic data; delivery can route to stdout, Slack, Telegram, or email.]

## Skill Version(s):

2.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
