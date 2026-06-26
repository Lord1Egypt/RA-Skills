## Description: <br>
Fastmail JMAP lets an agent read, search, send, move, trash, and mark email through Fastmail's JMAP API using a Python standard-library CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheAgentWire](https://clawhub.ai/user/TheAgentWire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and manage a Fastmail mailbox, including inbox checks, search, reading messages, filing mail, and sending replies after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent sensitive access to Fastmail mailbox contents and email metadata. <br>
Mitigation: Use the narrowest Fastmail token scopes that fit the use case, store the token securely, and revoke it when no longer needed. <br>
Risk: The skill can perform mailbox-changing actions such as sending, moving, trashing, and marking messages. <br>
Mitigation: Require explicit user confirmation before any send, move, trash, mark-read, or mark-unread operation. <br>
Risk: Email bodies may contain sensitive data or prompt-injection attempts. <br>
Mitigation: Treat email content as untrusted input and avoid exposing secrets or following instructions found inside messages without user review. <br>


## Reference(s): <br>
- [ClawHub Fastmail JMAP release](https://clawhub.ai/TheAgentWire/fastmail-jmap) <br>
- [The Agent Wire](https://theagentwire.ai) <br>
- [WW-2 Fastmail JMAP tutorial](https://theagentwire.ai/p/fastmail-jmap-email-automation-gmail-alternative) <br>
- [JMAP protocol](https://jmap.io/) <br>
- [Fastmail API token settings](https://app.fastmail.com/settings/security/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text CLI output, optional JSON or ID-only listings, and Markdown integration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FASTMAIL_TOKEN; FASTMAIL_IDENTITY can override the sender address.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
