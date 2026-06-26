## Description: <br>
Manage the MoltBot A2A Hub: register agents, search the registry, relay messages, and stream responses for the A2A agent-to-agent protocol hub deployed at a2a-hub.fly.dev. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myrodar](https://clawhub.ai/user/myrodar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to register, discover, update, delete, and communicate with A2A-compatible agents through the MoltBot A2A Hub. It provides endpoint guidance, curl commands, request schemas, and credential handling notes for registry and relay workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages sent through the hub may be relayed to remote agents, which can expose private data to agents the user does not trust. <br>
Mitigation: Use the skill only with trusted registered agents and avoid sending secrets or sensitive data through relay requests. <br>
Risk: An upstream API key provided during agent registration can be used by the hub to call the registered endpoint. <br>
Mitigation: Use dedicated, revocable credentials with limited scope, store returned hub API keys securely, and rotate or revoke keys when access is no longer needed. <br>


## Reference(s): <br>
- [A2A Hub service endpoint](https://a2a-hub.fly.dev) <br>
- [ClawHub A2A Hub release](https://clawhub.ai/myrodar/a2a-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes remote API request examples, authentication headers, rate limits, and credential storage guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
