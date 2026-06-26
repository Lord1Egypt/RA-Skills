## Description: <br>
Connects agents to 100+ third-party APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton's managed OAuth API gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmundi3210](https://clawhub.ai/user/tmundi3210) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call native third-party API endpoints through Maton's gateway and to manage user-authorized service connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway can perform write, delete, messaging, publishing, billing, sharing, webhook, and sensitive-document actions across connected services. <br>
Mitigation: Use least-privilege service connections and require explicit user confirmation before any destructive, external-facing, financial, sharing, or sensitive-data action. <br>
Risk: MATON_API_KEY authenticates to Maton and enables access to services that the user has connected. <br>
Mitigation: Store the key as a secret, avoid logging it, rotate it if exposed, and authorize only the services and scopes needed for the task. <br>
Risk: Some integrations may use API keys or non-OAuth credentials with different safety boundaries from OAuth connections. <br>
Mitigation: Treat API-key-based integrations as higher risk and verify the credential model and service permissions before use. <br>


## Reference(s): <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API reference](https://www.maton.ai/docs/api-reference) <br>
- [Slack routing guide](references/slack/README.md) <br>
- [Google Mail routing guide](references/google-mail/README.md) <br>
- [Notion routing guide](references/notion/README.md) <br>
- [Stripe routing guide](references/stripe/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, shell, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and user-authorized service connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
