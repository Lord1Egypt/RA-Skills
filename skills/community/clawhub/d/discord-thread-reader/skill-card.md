## Description: <br>
Discord Context helps agents read Discord channel and thread message history via the Discord Bot API when conversation history is outside the current OpenClaw session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13-agent](https://clawhub.ai/user/EasonC13-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve historical Discord context from channels or threads by ID when the active session does not include those messages. It is intended for cases where the operator deliberately grants an agent access to a Discord bot token and the bot has appropriate read permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent ongoing access to a Discord bot token that can read history in every channel the bot can access. <br>
Mitigation: Use a dedicated bot with the minimum channel permissions needed, avoid write permissions, store the token outside the workspace with restrictive file permissions, and rotate the token after use. <br>
Risk: The skill can read Discord history outside normal OpenClaw session visibility. <br>
Mitigation: Require explicit channel or thread IDs and use it only for conversations the operator is authorized to inspect. <br>
Risk: A persistent token pointer can remain available to future agent sessions. <br>
Mitigation: Remove the persistent token reference when the task is complete and update or rotate the token if access should end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EasonC13-agent/discord-thread-reader) <br>
- [Discord channel messages API endpoint](https://discord.com/api/v10/channels/{channel_or_thread_id}/messages?limit=50) <br>
- [Discord active threads API endpoint](https://discord.com/api/v10/channels/{parent_channel_id}/threads/active) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Executed commands return Discord API JSON responses; the skill itself provides setup and request guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
