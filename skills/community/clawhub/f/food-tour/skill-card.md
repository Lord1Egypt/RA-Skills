## Description:

Plan culinary travel experiences including local food tours, street food crawls, cooking classes, food markets, regional tasting routes, and restaurant discovery using flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find culinary travel options from live flyai CLI searches and present user-facing Markdown summaries with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and execute a third-party flyai CLI.

Mitigation: Require user confirmation before installation or command execution, review the CLI package separately, and avoid elevated privileges for global npm installs.

Risk: Travel searches and booking links may involve sensitive trip, identity, or preference details.

Mitigation: Avoid entering sensitive details unless logs are disabled or redacted, and require explicit confirmation before opening or acting on booking links.

Risk: The artifact behavior can persist raw user queries locally.

Mitigation: Treat execution logs as sensitive, minimize stored query content, and redact personal or travel details before persistence.

## Reference(s):

- [food-tour ClawHub page](https://clawhub.ai/xiejinsong/skills/food-tour)
- [Publisher profile](https://clawhub.ai/user/xiejinsong)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for travel data; expected user-facing output includes a brand tag and booking links when results are available.]

## Skill Version(s):

v3.2.3 (source: server release evidence; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
