## Description: <br>
Bingo Email lets an agent read, send, reply to, forward, draft, move, and delete email across IMAP/SMTP mailboxes through a local Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soulcoolzzz](https://clawhub.ai/user/soulcoolzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users with configured mailbox access use this skill to let an agent manage routine email workflows, including reading messages, preparing drafts, sending replies, forwarding messages, and organizing mailbox folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, forward, or reply-all to email using the configured mailbox. <br>
Mitigation: Review recipients, subject, body text, and reply-all behavior before allowing any send, forward, or reply command to run. <br>
Risk: The skill requires an app password or mailbox authorization code stored in a local configuration file. <br>
Mitigation: Use a dedicated app password where possible, keep the configuration file private with restrictive permissions, and rotate credentials if exposure is suspected. <br>
Risk: The delete command can permanently remove mailbox data because it marks a message deleted and expunges it. <br>
Mitigation: Avoid delete unless permanent removal is intended, and prefer reviewing or moving messages before deleting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soulcoolzzz/bingo-email) <br>
- [Project homepage](https://github.com/soulcoolzzz/bingo-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read mailbox content and may create, send, move, or delete email when invoked with the corresponding command.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
