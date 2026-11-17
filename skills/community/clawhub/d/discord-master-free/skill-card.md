## Description: <br>
Discord Master Free is a Discord bot development guide for beginners and individual developers that covers bot creation, token handling, slash command registration, message handling, interaction responses, and basic permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and community operators use this skill to get practical Discord bot setup guidance, including command registration, Discord API request examples, credential handling, and basic permission configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Discord API examples can register commands or send messages if an agent runs them with real bot credentials. <br>
Mitigation: Use test guilds and placeholder credentials, and require explicit confirmation before registering commands or sending Discord channel messages. <br>
Risk: Discord bot tokens can grant control of a bot if exposed or mishandled. <br>
Mitigation: Keep bot tokens in environment variables, avoid hardcoding credentials, and rotate tokens immediately if exposure is suspected. <br>
Risk: The skill requests exec-capable behavior for HTTP calls, which can broaden operational impact when agents execute commands automatically. <br>
Mitigation: Review generated commands before execution and limit automatic command execution in production or shared Discord environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-master-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Discord API request templates and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
