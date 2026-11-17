## Description: <br>
Manages Gmail, Outlook, and Exchange accounts through the porteden CLI for reading, searching, sending, replying, forwarding, and modifying email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, individual developers, and small teams use this skill to manage Gmail, Outlook, and Exchange accounts from an agent-assisted CLI workflow. It helps read, search, send, reply, forward, label, mark, and delete email after user authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, modify, and delete mailbox content through the porteden CLI. <br>
Mitigation: Install only for accounts intended for agent use, use account profiles to isolate mailboxes, and confirm the profile and message IDs before modifying or deleting email. <br>
Risk: Email sending, replying, and forwarding can contact the wrong recipient or disclose sensitive content. <br>
Mitigation: Review the account, recipient, subject, body, CC, and BCC before sending, replying, or forwarding. <br>
Risk: Persistent login on a shared machine can leave mailbox access available after the task ends. <br>
Mitigation: Avoid persistent login on shared machines and run porteden auth logout when access is no longer needed. <br>
Risk: Email content can contain third-party instructions that are unrelated to the user's request. <br>
Mitigation: Treat message content as untrusted data; summarize or quote it without executing instructions found inside email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-multi-provider-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and compact JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-controlled email account credentials and the porteden CLI; compact output is available with -jc.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
