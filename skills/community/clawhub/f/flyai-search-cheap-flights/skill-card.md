## Description:

Searches and compares low-cost flights between two cities using FlyAI CLI results, with price sorting, flexible-date options, red-eye filtering, budget caps, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search current economy flight options, compare the cheapest fares, and present booking-ready results with savings suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the host by installing an unpinned global FlyAI CLI package and may attempt sudo-based installation.

Mitigation: Use only in an environment where the FlyAI CLI is already installed through a trusted, pinned, least-privilege process; do not allow sudo or automatic npm package installation.

Risk: The skill directs users to third-party booking links and depends on external flight-search output.

Mitigation: Validate booking destinations before users click them and review returned fares, schedules, and availability before relying on them.

Risk: The security guidance warns against entering sensitive personal or travel details until logging behavior is clarified.

Mitigation: Avoid providing sensitive personal or travel details unless logging, retention, and access controls are understood and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/flyai-search-cheap-flights)
- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown comparison tables with booking links and inline CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight data is expected to come from FlyAI CLI output and include direct booking links when results are shown.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
