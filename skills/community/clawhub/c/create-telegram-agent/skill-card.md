## Description: <br>
Create a new Telegram agent in OpenClaw with proper configuration, including workspace setup, Telegram binding, and bot token configuration after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4T-Shirt](https://clawhub.ai/user/4T-Shirt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create a Telegram-connected agent, prepare the required OpenClaw configuration, and generate initial AGENTS.md and SOUL.md files after confirming the proposed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Telegram bot token may be exposed if the agent repeats the full token in chat or configuration previews. <br>
Mitigation: Mask bot tokens in previews and confirmations, avoid logging full tokens, and rotate the token with BotFather if it has already been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4T-Shirt/create-telegram-agent) <br>
- [Publisher profile](https://clawhub.ai/user/4T-Shirt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed OpenClaw configuration, directory creation commands, and starter agent files for review before changes are applied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
