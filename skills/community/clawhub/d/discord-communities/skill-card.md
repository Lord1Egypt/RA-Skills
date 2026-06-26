## Description: <br>
Manage Discord guilds, channels, messages, members, roles, and application commands - powered by ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Discord through OpenClaw and ClawLink, including discovering guild data, resolving invites, checking entitlements, and managing channels, messages, members, roles, commands, and selected account settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration depends on ClawLink to broker the Discord OAuth connection and can access Discord account or server data according to granted scopes. <br>
Mitigation: Install only if ClawLink is trusted, review Discord scopes during OAuth, prefer read-only tools when possible, and revoke the ClawLink or Discord OAuth connection when no longer needed. <br>
Risk: Some tools can change Discord account or server state, including leaving guilds, editing command permissions, consuming or deleting entitlements, updating or deleting role connections, or modifying the current user's profile. <br>
Mitigation: Require explicit confirmation before write or destructive actions, and verify the target guild, application, entitlement, role connection, or user profile before execution. <br>


## Reference(s): <br>
- [ClawHub Discord Skill](https://clawhub.ai/hith3sh/discord-communities) <br>
- [ClawLink Integration Hub](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=discord-communities) <br>
- [ClawLink Discord Connection Dashboard](https://claw-link.dev/dashboard?add=discord) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Discord OAuth scopes and explicit confirmation for account or server state changes.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
