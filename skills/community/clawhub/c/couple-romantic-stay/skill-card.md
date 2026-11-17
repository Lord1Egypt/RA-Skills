## Description:

Find romantic hotels for couples, including king-size beds, scenic views, intimate atmosphere, and couple amenities such as champagne and spa packages, using FlyAI CLI search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Travel-focused agents use this skill to help external users find and compare romantic hotel options for honeymoons, anniversaries, date nights, and couple trips. It collects destination and date parameters, runs FlyAI CLI hotel searches, and formats results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install a global third-party FlyAI CLI before running travel searches.

Mitigation: Install and review the CLI manually in an isolated environment before enabling the skill for routine use.

Risk: Travel searches are routed through a third-party provider and may expose trip details to that provider.

Mitigation: Avoid entering sensitive personal details and disclose provider use where required by policy.

Risk: The artifact includes instructions to persist raw user queries to a local execution log when file writes are available.

Mitigation: Disable or remove query log persistence unless local policy permits retaining that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/couple-romantic-stay)
- [fallbacks.md](references/fallbacks.md)
- [playbooks.md](references/playbooks.md)
- [runbook.md](references/runbook.md)
- [templates.md](references/templates.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown comparison tables with booking links, concise guidance, and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must come from FlyAI CLI output, include booking links when hotels are shown, and avoid raw JSON in user-facing responses.]

## Skill Version(s):

3.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
