## Description: <br>
Connects to 163/126/yeah.net (Coremail) email via IMAP and SMTP to read inboxes, search messages, and send email while handling the Coremail IMAP ID command requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanyuhh](https://clawhub.ai/user/hanyuhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to 163, 126, or yeah.net mailboxes for mailbox review, message search, inbox monitoring, and outbound email through the bundled client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private mailbox contents. <br>
Mitigation: Install only when the configured mailbox is trusted for agent access, and limit use to the intended 163/126/yeah.net account. <br>
Risk: The skill can send messages and attachments through the configured mailbox. <br>
Mitigation: Review the recipient, subject, body, CC list, and every attachment path before allowing any send command. <br>
Risk: Mailbox credentials stored in the environment file can expose account access if mishandled. <br>
Mitigation: Use a revocable mail authorization code instead of the login password and protect the .env file. <br>


## Reference(s): <br>
- [163 Email Monitor on ClawHub](https://clawhub.ai/hanyuhh/163-email-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output can be plain text or JSON for read and search operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads configuration from an environment file and can include limited message body previews when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
