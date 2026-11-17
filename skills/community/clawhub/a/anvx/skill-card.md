## Description:

Track and optimize AI API spending across 19 providers with live pricing and 6 optimization modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tje8x](https://clawhub.ai/user/tje8x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect AI, cloud, payments, communications, monitoring, search, and crypto spending, then receive read-only optimization recommendations. It is intended for financial visibility and cost analysis, not account modification or financial transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests many sensitive provider credentials.

Mitigation: Use dedicated least-privilege read-only credentials for every provider and avoid production administrator or write-capable keys.

Risk: Local financial history and query history are persisted on the user's machine.

Mitigation: Review local storage before installation and run the skill only on systems where local financial data can be protected.

Risk: The security review flags packaging and credential-scope issues.

Mitigation: Confirm the package includes a real lockfile and supports restricted Stripe credentials before treating the release as low risk.

## Reference(s):

- [ANVX homepage](https://anvx.io)
- [ClawHub skill page](https://clawhub.ai/tje8x/skills/anvx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, financial summaries, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dollar amounts, percentages, provider names, and crypto informational disclaimers.]

## Skill Version(s):

1.4.6 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
