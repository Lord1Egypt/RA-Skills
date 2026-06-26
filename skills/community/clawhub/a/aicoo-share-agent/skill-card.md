## Description: <br>
Creates and manages secure, shareable Aicoo agent links with scope, expiration, sign-in, permission, analytics, and revocation controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent create, update, review, and revoke Aicoo share links for selected folders or full-agent access. It is intended for controlled sharing with investors, prospects, partners, collaborators, or other recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Aicoo API credentials to create and manage share links. <br>
Mitigation: Install it only when the agent should manage Aicoo sharing, keep API keys scoped and protected, and confirm link creation or policy changes before execution. <br>
Risk: Share links can expose agent context, folders, calendars, notes, visitor identity data, or note-backed policies. <br>
Mitigation: Prefer folder-scoped, read-only links with sign-in required and short expirations; review exposed data before enabling anonymous, write, edit, calendar-write, or never-expiring access. <br>
Risk: Updating or revoking links and patching policy notes can change remote Aicoo access behavior. <br>
Mitigation: Review the target link, folder scope, notes permission, expiration, and policy note content before applying updates or revocations. <br>


## Reference(s): <br>
- [Share Agent API Reference](artifact/reference/API.md) <br>
- [Basic Share Example](artifact/examples/basic-share.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xisen-w/aicoo-share-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, JSON request payloads, and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include share URLs, scope, permissions, expiration, sign-in requirement, sandboxing status, visitor analytics, and revocation results.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
