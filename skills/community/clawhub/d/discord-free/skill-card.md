## Description: <br>
Discord 基础控制 helps agents operate a Discord bot for basic message sending, editing, deletion, reactions, message reading, pinning, and permission checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and community operators use this skill to automate Discord notifications, simple interactions, message lookup, and basic message management in configured servers or direct-message contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, read, delete, pin, and archive Discord messages through a configured bot. <br>
Mitigation: Limit the bot token and Discord permissions to the specific servers and channels needed for the workflow. <br>
Risk: Message deletion and local archiving can affect community records and retention expectations. <br>
Mitigation: Require explicit approval before destructive or archival actions and define where archives are stored and when they are removed. <br>
Risk: The skill requests broad local command and file-write authority. <br>
Mitigation: Review planned command and file operations before execution and run the agent in a constrained workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON action examples and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Discord bot action guidance for message, reaction, pinning, reading, and permission-check workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
