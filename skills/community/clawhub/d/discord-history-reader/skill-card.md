## Description: <br>
Reads Discord channel and thread message history directly via the Discord Bot API when the agent cannot see it through an active OpenClaw session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to fetch historical Discord channel or thread context for an agent when the conversation is outside the current OpenClaw session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent bot-token access can let an agent read Discord history outside normal OpenClaw session visibility. <br>
Mitigation: Use a dedicated low-permission bot limited to specific channels and require explicit approval for each channel or thread read. <br>
Risk: A Discord bot token grants access to every channel where the bot has permissions and may be exposed if mishandled. <br>
Mitigation: Store the token outside the workspace with restrictive file permissions, avoid send or moderation permissions, and rotate the token if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EasonC13/discord-history-reader) <br>
- [Discord channel messages API endpoint](https://discord.com/api/v10/channels/{channel_or_thread_id}/messages?limit=50) <br>
- [Discord active threads API endpoint](https://discord.com/api/v10/channels/{parent_channel_id}/threads/active) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Discord API responses as JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Discord channel or thread IDs and a low-permission bot token with read history access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
