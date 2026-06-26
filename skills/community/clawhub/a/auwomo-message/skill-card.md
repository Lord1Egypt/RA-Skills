## Description: <br>
Sends Feishu/Lark private messages to exact-match organization members through the auwomo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyqqj0](https://clawhub.ai/user/tyqqj0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and operators use this skill to ask an agent to send Feishu/Lark private messages to known organization members through auwomo. It is for exact-recipient messaging and reminders, not task management or agent inbox delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A message could be sent to the wrong organization member or with unintended text. <br>
Mitigation: Use the skill's dry-run flow first and confirm the exact recipient and message text before sending. <br>
Risk: The skill depends on local auwomo and lark-cli tools and the configured bot account. <br>
Mitigation: Install only in environments where those tools and the bot account are trusted and configured for the intended organization. <br>


## Reference(s): <br>
- [message-send](references/message-send.md) <br>
- [ClawHub skill page](https://clawhub.ai/tyqqj0/auwomo-message) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional text or JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may recommend dry-run before sending and should confirm the exact recipient and message text before real delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
