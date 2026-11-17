## Description:

Free, instant access to verified LinkedIn profiles and business emails for ecommerce stores by querying EcCompass AI data for a specific store domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger52027](https://clawhub.ai/user/roger52027)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, ecommerce analysts, and developers use this skill to retrieve decision-maker LinkedIn profiles and business email contacts for individual ecommerce store domains. It can also support broader ecommerce research when the bundled CLI commands are available to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves contact details, including business emails and LinkedIn profiles, which can create privacy, compliance, or outreach-law risk if used for bulk harvesting.

Mitigation: Use it only for permitted business purposes, avoid bulk personal-data collection, and confirm compliance with applicable privacy and outreach rules before acting on results.

Risk: The bundled CLI exposes broader ecommerce search, analytics, historical revenue/traffic, installed-app, and raw JSON capabilities beyond narrow contact lookup.

Mitigation: Review intended commands before use and restrict agent instructions or execution permissions when only contact lookup is needed.

Risk: The skill requires an ECcompass API token for network calls.

Mitigation: Use a scoped or disposable token when available and avoid sharing command outputs that may expose account-specific data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roger52027/skills/ecommerce-lead-contacts)
- [EcCompass AI](https://eccompass.ai)
- [API Schema](references/schema.md)
- [Usage Examples](references/examples.md)
- [Ecommerce Website Data](https://clawhub.ai/roger52027/ecommerce-website-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown and terminal text, with optional formatted JSON from CLI calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.eccompass.ai and an APEX_TOKEN credential.]

## Skill Version(s):

1.0.9 (source: frontmatter, claw.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
