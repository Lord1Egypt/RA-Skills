## Description:

Searches and analyzes ecommerce websites through EcCompass data, including store discovery, domain analytics, GMV and traffic trends, tech stack, installed apps, and contact lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger52027](https://clawhub.ai/user/roger52027)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research ecommerce stores, analyze competitors, inspect store technologies, review estimated revenue and traffic trends, and retrieve business contact data for lawful outreach or research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can lead users to expose an APEX_TOKEN in chat or persistent agent history.

Mitigation: Configure APEX_TOKEN through a protected environment variable or credential store and avoid pasting real tokens into conversational prompts.

Risk: The skill can retrieve emails, phone numbers, and LinkedIn contact data that may be personal or sensitive business data.

Mitigation: Use returned contact data only for lawful, appropriate outreach or research, and apply privacy and consent requirements for the relevant jurisdiction and use case.

Risk: GMV, traffic, and revenue values are estimates rather than verified financial records.

Mitigation: Treat analytics as directional market intelligence and verify material business decisions against authoritative sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roger52027/skills/ecommerce-website-data)
- [EcCompass AI](https://eccompass.ai)
- [AI Instructions](artifact/SKILL.md)
- [API Schema](artifact/references/schema.md)
- [Usage Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional formatted JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.eccompass.ai and an APEX_TOKEN credential. CLI responses include ecommerce analytics, search result tables, historical metrics, installed-app summaries, or contact records depending on the command.]

## Skill Version(s):

1.2.18 (source: server release metadata, SKILL.md frontmatter, claw.json, query.py, CHANGELOG released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
