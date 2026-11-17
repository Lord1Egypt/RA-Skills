## Description: <br>
Discord Chat 基础 helps agents send Discord channel messages, reply in threads, read recent history, and react with emojis through a configured Discord message channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small community operators use this skill to send notifications, answer simple Discord support questions, read recent channel context, and acknowledge messages with emoji reactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill requests broader local exec/write authority than its Discord examples appear to require. <br>
Mitigation: Install only when that authority is acceptable for the workspace, and review requested tool permissions before deployment. <br>
Risk: The security review notes under-disclosed credential and callback URL guidance. <br>
Mitigation: Use authorized Discord channels, keep history reads small, avoid sensitive channels unless participants consent, and provide callback URLs only for endpoints you control and trust. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/discord-chat-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline message command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Discord message actions for sending, replying, reading recent history, and reacting; examples assume an authorized Discord bot and configured channel routing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
