## Description: <br>
Access Gmail, Slack, Google Calendar, GitHub, and custom Auth0 connections on behalf of authenticated users through the auth0-tv CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepu105](https://clawhub.ai/user/deepu105) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to help authenticated users search, read, send, post, update, and manage data in connected third-party services through structured auth0-tv CLI calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive OAuth-protected accounts and data through auth0-tv. <br>
Mitigation: Install only if the external auth0-token-vault-cli package is trusted, connect only needed services and scopes, and review requested access before use. <br>
Risk: Destructive actions can send or delete email, post Slack messages, update calendars, change GitHub resources, or make authenticated non-GET requests. <br>
Mitigation: Require explicit user approval before destructive commands, authenticated fetch calls with non-GET methods, or requests with bodies. <br>
Risk: Custom Auth0 connections can broaden authenticated API access if scopes or allowed domains are too broad. <br>
Mitigation: Use minimum required scopes and exact trusted allowed domains for custom connections. <br>


## Reference(s): <br>
- [auth0-tv Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deepu105/auth0-token-vault) <br>
- [auth0-token-vault-cli npm package](https://www.npmjs.com/package/auth0-token-vault-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, the auth0-tv CLI, human OAuth setup for login/connect flows, and JSON mode for agent use.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
