## Description:

Connects agents to 100+ external APIs through Maton-managed OAuth connections, with examples for direct native API calls and connection management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmundi3210](https://clawhub.ai/user/tmundi3210)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to call third-party services such as Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot through authorized Maton connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad access to every Maton connection the user authorizes, including write and delete actions across connected services.

Mitigation: Use narrowly scoped service connections where possible, verify the target connection before writes or deletes, and require explicit confirmation for destructive or public-facing actions.

Risk: The Maton API key can expose account-level gateway access if printed, logged, screenshotted, or shared.

Mitigation: Do not print or share MATON_API_KEY, avoid commands that echo the key, and rotate it if it appears in logs or screenshots.

Risk: ClawHub security evidence marks this release as suspicious because of broad gateway access and unsafe API-key troubleshooting.

Mitigation: Review the skill before installation and deploy it only where the connected services, scopes, and allowed action types are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmundi3210/skills/api-gateway-disabled-20260401-113030)
- [Maton homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [Provider routing guides](artifact/references/)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; API actions depend on user-authorized Maton service connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
