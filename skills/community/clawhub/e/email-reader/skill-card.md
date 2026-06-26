## Description: <br>
Email Reader helps an agent read, summarize, search, classify, and send email through IMAP/SMTP accounts using the himalaya CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackeven02](https://clawhub.ai/user/Jackeven02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect configured mailboxes, summarize unread or important messages, and draft or send email through supported IMAP/SMTP providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive mailbox contents to an agent. <br>
Mitigation: Use the least-privileged email account practical for the task, prefer OAuth or app-specific passwords, and avoid storing real passwords in shell history or logs. <br>
Risk: The skill enables outbound email actions and mailbox changes. <br>
Mitigation: Require explicit user approval before sending, deleting, marking messages, or setting up recurring checks. <br>
Risk: The skill relies on the himalaya CLI for mailbox operations. <br>
Mitigation: Verify the himalaya package source before installation and confirm configuration against the intended email provider. <br>


## Reference(s): <br>
- [Email management reference resources](references/resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and concise email summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Presents sender, subject, summary, and suggested actions for relevant messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
