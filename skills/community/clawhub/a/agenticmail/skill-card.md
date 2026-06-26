## Description: <br>
AgenticMail gives AI agents email, SMS, persistent storage, and multi-agent coordination tools with setup and security guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ope-olatunji](https://clawhub.ai/user/ope-olatunji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use AgenticMail to give agents managed mailboxes, SMS access, persistent storage, and task delegation for workflows that need communication or coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and SMS, read mailboxes, coordinate agents, and manage persistent storage. <br>
Mitigation: Install only for workflows that need real communication and storage capabilities, and require explicit human approval before sending messages or deleting data. <br>
Risk: Master-key operations can create or delete accounts, change gateway or domain settings, and support payment-related setup. <br>
Mitigation: Use an agent-scoped key for routine work, avoid exposing the master key to agents, and protect ~/.agenticmail/config.json. <br>
Risk: Database storage actions, including raw SQL and destructive table operations, can expose or alter persistent data. <br>
Mitigation: Review raw SQL, import/export, drop, truncate, and deletion operations before execution and limit access to approved data. <br>
Risk: SMS and OTP access can expose verification codes or other sensitive account messages. <br>
Mitigation: Require explicit human approval before retrieving, using, or forwarding SMS verification codes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ope-olatunji/agenticmail) <br>
- [AgenticMail API Reference](references/api-reference.md) <br>
- [AgenticMail Configuration](references/configuration.md) <br>
- [AgenticMail Project Homepage](https://github.com/agenticmail/agenticmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool-call outputs, JSON status/results, and shell/config snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some operations require an agent-scoped API key; administrative operations require a master key.] <br>

## Skill Version(s): <br>
0.5.50 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
