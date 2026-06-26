## Description: <br>
This skill provides script-based email operations for an agent, including mailbox management, email reading and search, sending, replies, forwarding, and attachment handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyxiang](https://clawhub.ai/user/tyxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent read, search, organize, send, reply to, and forward email through configured IMAP and SMTP accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-authority mailbox actions, including sending, forwarding, deleting, expunging, folder deletion, and bulk moves. <br>
Mitigation: Install only when real mailbox authority is intended and require explicit human approval before send, reply-all, forward, delete, expunge, folder delete, or bulk move actions. <br>
Risk: Mailbox credentials and OAuth tokens can expose account access if stored or logged improperly. <br>
Mitigation: Use app passwords or least-privilege OAuth where available, store secrets only in environment variables, and keep secrets out of checked-in files and logs. <br>
Risk: Incorrect or untrusted IMAP, SMTP, or OAuth endpoints can route mail or credentials through unintended services. <br>
Mitigation: Verify IMAP, SMTP, and OAuth endpoint configuration before use, and keep TLS certificate verification enabled except for controlled local testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tyxiang/ai-agent-email-skill) <br>
- [Publisher profile](https://clawhub.ai/user/tyxiang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts exchange JSON over stdin and stdout; diagnostics are written to stderr.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
