## Description: <br>
Connects agents to 100+ external APIs through Maton-managed gateway connections and documented request patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to route authenticated requests to supported SaaS and productivity APIs after the user has authorized the relevant Maton connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad API gateway access can reach high-impact external services, including write, delete, billing, admin, posting, scheduling, and webhook actions. <br>
Mitigation: Require explicit user confirmation before any high-impact action and connect only the services and scopes needed for the task. <br>
Risk: The MATON_API_KEY authenticates access to the gateway and should be treated as sensitive. <br>
Mitigation: Store the key in a secret manager or environment variable, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Authentication documentation is inconsistent across supported services, and some references indicate API-key based connections rather than OAuth. <br>
Mitigation: Verify each target service connection method and permission scope before use, especially for services that do not use OAuth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayakolin/api-gateway-tmp) <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Slack reference](artifact/references/slack/README.md) <br>
- [Google Drive reference](artifact/references/google-drive/README.md) <br>
- [Notion reference](artifact/references/notion/README.md) <br>
- [Stripe reference](artifact/references/stripe/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized service connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
