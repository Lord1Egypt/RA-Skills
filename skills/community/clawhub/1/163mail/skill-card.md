## Description: <br>
163mail lets an agent send, receive, search, read, reply to, forward, and delete 163.com email through IMAP and SMTP authorization-code credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxy1503](https://clawhub.ai/user/lxy1503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a 163.com mailbox from an agent workflow, including inbox review, message search, sending, replying, forwarding, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled config.json contains live-looking mailbox credentials. <br>
Mitigation: Remove bundled credentials before installation, use environment variables or a locally created config.json, and rotate the exposed authorization code. <br>
Risk: Undocumented helper scripts can send fixed outbound emails to a hard-coded recipient. <br>
Mitigation: Review or delete send-email.js and send-word-email.js before use, and require explicit user confirmation for outbound mail actions. <br>
Risk: Mailbox commands can send, forward, reply to, or permanently delete email. <br>
Mitigation: Run with least-privilege mailbox credentials where possible and confirm destructive or outbound actions before execution. <br>
Risk: IMAP TLS certificate verification is disabled in the implementation. <br>
Mitigation: Restore TLS certificate verification before using the skill with sensitive mailbox data. <br>


## Reference(s): <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/lxy1503/163mail) <br>
- [Publisher profile](https://clawhub.ai/user/lxy1503) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text command responses with setup shell snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform IMAP and SMTP mailbox side effects; documented commands do not support attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
