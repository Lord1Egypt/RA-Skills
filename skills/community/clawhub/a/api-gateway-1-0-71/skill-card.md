## Description:

Connects agents to 100+ third-party APIs through Maton-managed OAuth and a unified gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaopei123](https://clawhub.ai/user/gaopei123)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent call authorized external services such as Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot. It is useful for workflows that need native API calls, connection management, and provider-specific routing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway can give an agent broad power over connected services, including write or delete operations.

Mitigation: Use least-privilege service accounts and OAuth scopes, and require explicit review before write or delete calls.

Risk: MATON_API_KEY exposure could let another party use the gateway account.

Mitigation: Store the key as an environment variable, never print or share it, and rotate it if it appears in logs or screenshots.

Risk: When multiple accounts are connected for the same app, requests may target the wrong account.

Mitigation: Specify the Maton-Connection header for workflows that require a particular connected account.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gaopei123/skills/api-gateway-1-0-71)
- [Maton homepage](https://maton.ai)
- [Maton API reference](https://www.maton.ai/docs/api-reference)
- [Provider routing guides](references/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint examples and inline Python, JavaScript, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; target service permissions depend on user-authorized OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
