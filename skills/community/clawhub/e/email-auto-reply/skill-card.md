## Description: <br>
Email Auto Reply helps users maintain local keyword-based reply templates and test matching replies for common email inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support staff and individual users use this skill to manage local keyword-to-reply templates and test draft responses from the command line. It is suited for organizing common replies, not for automatically accessing mailboxes or sending email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect the skill to send email, manage multiple accounts, or perform automatic CC behavior. <br>
Mitigation: Treat it as a local reply-template manager unless additional reviewed code is added for mailbox access or message sending. <br>
Risk: Reply templates may contain secrets or sensitive customer information. <br>
Mitigation: Avoid storing credentials, private customer data, or regulated information in local reply templates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SxLiuYu/email-auto-reply) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON rule data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores reply rules in ~/.email_auto_reply.json; the provided code does not access email accounts, send messages, or copy recipients.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
