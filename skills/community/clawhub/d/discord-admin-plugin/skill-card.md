## Description: <br>
Full Discord server administration suite for OpenClaw covering roles, moderation, channels, invites, webhooks, audit logs, and member management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendrag-git](https://clawhub.ai/user/rendrag-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent administer Discord servers through a configured Discord bot. It is suited for role, moderation, channel, invite, webhook, audit-log, and member-management workflows where the bot has deliberately granted permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Discord server-control actions such as bans, message deletion, role changes, channel changes, invites, and webhooks without built-in confirmation or scope limits. <br>
Mitigation: Use a dedicated least-privilege bot, restrict it to intended servers and permissions, and require external human approval for bans, deletes, role or channel changes, invites, and webhooks. <br>
Risk: Tool output or administrative capabilities could be exposed to users who should not control the Discord server. <br>
Mitigation: Limit which agents and users can invoke the skill, avoid exposing tool output to untrusted users, and monitor Discord audit logs for administrative actions. <br>
Risk: The required Discord bot token is a sensitive credential. <br>
Mitigation: Store the token only in the OpenClaw configuration path described by the artifact, treat it as secret, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rendrag-git/discord-admin-plugin) <br>
- [Publisher Profile](https://clawhub.ai/user/rendrag-git) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text] <br>
**Output Format:** [Structured JSON responses returned as text after Discord administration actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Discord bot token, Node.js, network access, and Discord permissions scoped to the intended servers and actions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
