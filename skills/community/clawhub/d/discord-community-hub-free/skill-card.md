## Description: <br>
Discord Community Hub Free helps agents perform read-only Discord account, server, member, role, widget, invite, and integration discovery lookups through an integration gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External community managers and developers use this skill to connect a Discord account and inspect user, guild, member, role, widget, invite, and available integration information. It is intended for lightweight, read-only Discord community overview workflows rather than administrative write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording or generic write-like examples may steer an agent beyond the free read-only Discord scope. <br>
Mitigation: Use the skill only for read-only account, server, member, role, widget, invite, and tool discovery lookups; route Discord administration or write workflows to a separately reviewed tool. <br>
Risk: Connecting a Discord account through the integration gateway can expose account and server data if OAuth scopes are broader than intended. <br>
Mitigation: Review requested OAuth scopes before authorizing, avoid write scopes for this free release, and grant only the scopes needed for the intended lookup workflow. <br>


## Reference(s): <br>
- [Discord Community Hub Free ClawHub page](https://clawhub.ai/thcjp/skills/discord-community-hub-free) <br>
- [thcjp ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell command examples; agent responses may include text or structured Discord lookup results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Discord lookup posture; requires a paired integration gateway and Discord OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
