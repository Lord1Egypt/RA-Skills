## Description: <br>
Provides an unofficial third-party 139 Mail IMAP/POP3 workflow for configuring mailbox access, reading and searching messages, sending mail, and managing or moving messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FANJIABO-529](https://clawhub.ai/user/FANJIABO-529) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to operate a 139.com mailbox after configuring an email address and authorization code. It supports mailbox review, unread checks, message search, sending mail, status changes, deletion, restoration, and folder moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials for an unofficial third-party 139.com mail integration. <br>
Mitigation: Use a dedicated authorization code, keep the generated config file local, revoke the authorization code when no longer needed, and delete config/139mail.conf after use. <br>
Risk: The skill can send, delete, restore, and move mailbox messages. <br>
Mitigation: Require explicit user confirmation before executing commands that mutate mailbox state. <br>
Risk: The artifact documents compatibility mode for older TLS behavior, which weakens transport safety controls. <br>
Mitigation: Use the skill only on trusted networks and avoid running mailbox operations over untrusted connections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FANJIABO-529/139mail) <br>
- [139 Mail web portal](https://mail.10086.cn/) <br>
- [Server and credential reference](references/credentials.md) <br>
- [IMAP operation guide](references/imap_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local mailbox configuration with a 139.com address and authorization code; commands that send, delete, restore, or move mail should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
