## Description:

Track Claude.ai token usage and session costs by scraping the Claude.ai usage dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude.ai users use this skill to monitor token usage, session limits, extra spend, balance, and short-term usage projections from the Claude.ai usage dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the Python tracker script that the skill tells the agent to run.

Mitigation: Before use, confirm the exact local script path and review that script independently.

Risk: The tracker handles sensitive Claude.ai usage, spend, balance, and limit data.

Mitigation: Use it only where that account and billing data can be stored in the disclosed memory file with appropriate local access controls.

Risk: The skill performs outbound access to the Claude.ai web dashboard.

Mitigation: Confirm that dashboard access is expected for the environment and account before enabling the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/claude-usage-tracker)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference usage percentages, spend, balance, reset timing, and projection confidence when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
