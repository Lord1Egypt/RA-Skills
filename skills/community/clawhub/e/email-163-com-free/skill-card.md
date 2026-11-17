## Description: <br>
163邮箱基础版 helps agents guide users through basic 163.com email CLI workflows for sending plain-text mail with one attachment, reading mail, searching by sender or subject, and managing JSON configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill when they need an agent to prepare basic 163.com mailbox actions such as sending work email, reviewing recent unread messages, or searching mail by sender or subject. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that access a real 163.com mailbox and expose email contents or credentials if used carelessly. <br>
Mitigation: Use a 163 client authorization code instead of the mailbox login password, restrict local config file permissions, and avoid including unnecessary email content in prompts or logs. <br>
Risk: Incorrect recipient, subject, body, or attachment details could cause unintended email disclosure. <br>
Mitigation: Review all recipient and attachment details before executing send commands, especially when attaching local files. <br>
Risk: The artifact stores mailbox configuration in a local JSON file, including an authorization code. <br>
Mitigation: Keep the configuration file outside version control, limit filesystem permissions, and rotate the authorization code if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-163-com-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include mailbox configuration values, command examples, validation steps, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
