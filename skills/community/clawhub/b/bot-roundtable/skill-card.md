## Description: <br>
Enables an agent to coordinate multiple Feishu bot identities that present expert perspectives in a group discussion, either automatically from trigger phrases or through manual calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu workspace operators use this skill to let several configured bot personas contribute short expert-style responses to a group chat for analysis, debate, and multi-perspective discussion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically post to Feishu chats as several bot identities using stored credentials. <br>
Mitigation: Install it only in Feishu groups and bot applications you control, restrict approved chats and users, and store Feishu secrets outside committed files with least privilege. <br>
Risk: Vague trigger phrases such as discussion prompts can cause unintended automated posts. <br>
Mitigation: Replace vague triggers with an explicit command or bot mention and require confirmation before posting. <br>
Risk: Multiple bot personas may make automated responses look like independent human participants. <br>
Mitigation: Clearly label automated bot responses and the bot identity used for each message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/bot-roundtable) <br>
- [Publisher profile](https://clawhub.ai/user/linbo405) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and JSON snippets; runtime behavior may send Feishu chat messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes 0.5 second spacing between messages and messages limited to 300 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
