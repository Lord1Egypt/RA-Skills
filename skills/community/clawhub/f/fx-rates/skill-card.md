## Description:

Check exchange rates, currency tips, and money-saving strategies for international travel, including ATM fees, card acceptance, local payment methods, and related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to retrieve exchange-rate, money-exchange, and payment-method guidance from flyai CLI results and present concise travel-facing answers with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt automatic global installation of the flyai CLI.

Mitigation: Require user approval before installing software and review the flyai CLI package provenance before use.

Risk: Returned booking links are third-party commercial links.

Mitigation: Validate URLs from CLI output and clearly treat booking links as third-party destinations.

Risk: Execution logging can persist raw user queries.

Mitigation: Disable or redact local logs before use, especially when queries may contain personal travel or payment context.

## Reference(s):

- [ClawHub Fx Rates Listing](https://clawhub.ai/dingtom336-gif/skills/fx-rates)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with tables, booking links, concise tips, and inline shell commands when setup or retry steps are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to be based on flyai CLI output, include detailUrl booking links when results are shown, and follow the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
