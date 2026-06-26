## Description: <br>
Email Mail Master Rose helps an agent send email, send attachments, receive recent messages, check for new messages, and delete selected messages through configured Aliyun, QQ, 163, or enterprise mail accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roseknife520](https://clawhub.ai/user/roseknife520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent perform mailbox operations from a command-line workflow after configuring their own email address and authorization code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes plaintext mailbox authorization codes in its configuration file. <br>
Mitigation: Remove the bundled credentials, rotate any exposed authorization codes, and configure only user-owned mailbox credentials through a protected local secret mechanism. <br>
Risk: The skill can send attachments and delete mail, including permanent POP3 or explicit permanent-delete operations. <br>
Mitigation: Require explicit user confirmation before sending attachments or deleting messages, and review selected message IDs before executing deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roseknife520/email-mail-master-rose) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Command-line output or JSON for received and newly checked email summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send attachments and can delete one or more selected email IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
