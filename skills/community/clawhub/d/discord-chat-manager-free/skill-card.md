## Description: <br>
Discord Chat Manager Free helps agents send, reply to, search, read, react to, edit, and delete Discord channel messages for personal and small-team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and small teams use this skill to manage Discord channel conversations through an agent, including sending announcements, replying by message ID, reading recent messages, adding reactions, editing or deleting messages, and basic keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger text points to unrelated SEO tasks, which may cause the skill to activate outside its Discord chat-management purpose. <br>
Mitigation: Correct the trigger text before use and limit activation to Discord chat workflows. <br>
Risk: The skill can read, post, edit, and delete Discord messages, including potentially sensitive channel history. <br>
Mitigation: Grant only the minimum Discord bot permissions needed and require explicit confirmation before editing or deleting messages or searching private history. <br>
Risk: A Discord bot token is required for operation. <br>
Mitigation: Store the bot token in a secret manager or environment variable and avoid exposing it in prompts, logs, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-chat-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Discord message command examples and tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operation status, Discord message content, channel or message metadata, summaries, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
