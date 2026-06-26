## Description: <br>
Interact with Forgejo using the `tea` CLI for issues, pull requests, Actions, and advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[razzeee](https://clawhub.ai/user/razzeee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use this skill to ask an agent for Forgejo `tea` CLI commands that inspect and manage issues, pull requests, Actions configuration, logins, and raw API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to use broad Forgejo CLI and raw API access. <br>
Mitigation: Use a dedicated least-privilege Forgejo token and require explicit confirmation before write, merge, delete, Actions, raw API, or administrative commands. <br>
Risk: The artifact includes examples for listing Actions secrets and adding token-based logins. <br>
Mitigation: Do not expose token values, secret names, or secret-related output in chats or logs, and avoid admin or organization-wide scopes where possible. <br>


## Reference(s): <br>
- [Forgejo skill release on ClawHub](https://clawhub.ai/razzeee/forgejo) <br>
- [razzeee publisher profile on ClawHub](https://clawhub.ai/user/razzeee) <br>
- [Tea CLI Go module](https://code.gitea.io/tea) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Forgejo CLI commands that require a configured `tea` login and a least-privilege token.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
