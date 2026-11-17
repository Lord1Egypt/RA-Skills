## Description: <br>
Basic Discord message management guidance for sending messages, replies, reactions, and simple polls for personal users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, small Discord communities, and independent developers use this skill to guide an agent through routine Discord bot actions such as sending, editing, deleting, replying to, reacting to, pinning, searching, creating threads, and creating simple polls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact Discord actions such as editing or deleting messages, sending DMs, searching message history, pinning content, and uploading local files. <br>
Mitigation: Require explicit user confirmation before those actions and verify the target channel, user, message, and file path before execution. <br>
Risk: A Discord bot token with broad permissions can affect channels or messages beyond the user's intent. <br>
Mitigation: Store the token in an environment variable, never hard-code it, and grant the bot only the Discord permissions needed for the intended server and channels. <br>
Risk: Broad trigger wording could cause an agent to apply Discord actions in unrelated tasks. <br>
Mitigation: Invoke the skill only for Discord message-management requests and keep roles, moderation, and bulk operations disabled unless a reviewed paid or expanded version is installed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Text] <br>
**Output Format:** [Markdown guidance with JSON action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Discord bot token and Discord bot permissions for the target server, channel, or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
