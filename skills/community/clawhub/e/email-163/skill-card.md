## Description: <br>
email-163 helps agents operate a 163 mailbox for bulk sending, advanced search, scheduled mail handling, archiving, audit logging, templates, and multi-account workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operations teams, and agent users can use this skill to draft and run 163 mailbox workflows such as bulk notices, filtered search, scheduled cleanup, archiving, and audit exports. It is intended for normal ClawHub release use, with review required before connecting it to real mailboxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send bulk email, delete or archive messages, schedule mailbox actions, and manage multiple accounts. <br>
Mitigation: Review planned actions before execution, use dry-run for bulk sends, require explicit approval for large sends and deletes, and avoid broad scheduled delete rules. <br>
Risk: 163 authorization codes and mailbox credentials could be exposed if stored in plaintext configuration. <br>
Mitigation: Store authorization codes in environment variables, a keychain, or a managed secret store, and avoid committing or logging secrets. <br>
Risk: The security verdict is suspicious because destructive mailbox operations have weak guardrails. <br>
Mitigation: Install first with a test account, limit permissions where possible, and scan or review the skill before using it with real mailbox data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-163) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, CSV examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run instructions, mailbox command examples, schedule expressions, and audit or export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
