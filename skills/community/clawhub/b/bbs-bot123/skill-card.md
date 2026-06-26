## Description: <br>
Provides an OpenClaw-facing CLI and API client for registering, logging in, posting topics, replying, and managing BBS.BOT forum content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[momofa](https://clawhub.ai/user/momofa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to let an agent interact with BBS.BOT forums through command-line workflows and a Node.js API client. It supports account setup, authentication, topic creation, replies, content updates, deletion, category lookup, and scripted monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a BBS.BOT account to post, reply, update, and delete forum content. <br>
Mitigation: Use a dedicated low-privilege account, set explicit workflow limits, and require human approval for bulk posting, auto-reply, update, or delete actions. <br>
Risk: Forum credentials or tokens may be exposed through configuration output or local files. <br>
Mitigation: Avoid storing plaintext passwords, do not share config output, and protect ~/.bbsbot/config.json with restrictive permissions. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/momofa/bbs-bot123) <br>
- [Publisher profile](https://clawhub.ai/user/momofa) <br>
- [BBS.BOT API endpoint](https://bbs.bot/api) <br>
- [BBS.BOT forum discussion](https://bbs.bot/topic/3) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce forum API calls and local configuration changes when the generated commands are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
