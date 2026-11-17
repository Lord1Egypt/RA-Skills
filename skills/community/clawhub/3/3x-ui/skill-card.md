## Description:

3X-UI代理面板 helps administrators use the 3x-ui REST API to manage Xray inbounds, outbounds, clients, nodes, subscriptions, backups, and server status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and server administrators use this skill to operate a 3x-ui panel through documented REST endpoints and helper shell scripts for user management, server monitoring, subscriptions, node administration, and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive administrative 3x-ui operations, including user changes, inbound and node management, backups, service restarts, and panel updates.

Mitigation: Grant only the narrowest available panel access and require explicit human review before destructive, service-affecting, or broad configuration changes.

Risk: Admin tokens, session cookies, subscription links, backups, logs, and configuration output may expose sensitive access or traffic information.

Mitigation: Require HTTPS panel URLs, avoid passing secrets on command lines, redact sensitive output before sharing, and store backups or logs only in approved locations.

## Reference(s):

- [3x-ui API 完整参考](artifact/references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/lanlan314/skills/3x-ui)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call 3x-ui panel APIs and JSON request or response examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
