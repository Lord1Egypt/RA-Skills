## Description: <br>
Discord社区免费 helps agents use Discord OAuth read-only capabilities to check user identity, guild membership, invite details, gateway information, and OAuth2 public keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and community operators use this skill to perform basic read-only Discord identity, guild, member, and invite checks through an agent workflow. It is intended for basic verification and community-management lookup tasks, not commercial entitlement checks or role-connection synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Discord OAuth profile and guild information, which may include personal or community data. <br>
Mitigation: Install only when that access is appropriate, and limit OAuth scopes to the read-only Discord data needed for the task. <br>
Risk: The optional callback_url may send completion data to an external destination. <br>
Mitigation: Omit callback_url unless the destination is controlled and the data being sent is understood. <br>
Risk: The skill declares broad local read, write, and exec tools without explaining why all are needed. <br>
Mitigation: Run it with the narrowest practical local permissions and review any proposed commands or file changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-communities-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and JSON result structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Discord OAuth profile, guild, member, invite, gateway, and public-key data when the connected Discord integration authorizes access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
