## Description: <br>
Daily profession roleplay game engine with hidden kink guessing, AI-driven personality generation, achievement tracking, and multi-backend image generation (ComfyUI/SD WebUI/Midjourney/Nano Banana Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nannyu](https://clawhub.ai/user/nannyu) <br>

### License/Terms of Use: <br>
Private use; no redistribution without permission <br>


## Use Case: <br>
External users and OpenClaw developers use this skill to deploy and run a daily adult roleplay agent that creates daily character scenarios, manages hidden guessing-game state, posts scheduled messages, and archives roleplay progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled adult roleplay messages or generated intimate content may be posted to an unintended conversation or channel. <br>
Mitigation: Review heartbeat and cron settings before enabling the skill, use a dedicated private message channel, and avoid the "last" target unless routing to the most recent conversation is acceptable. <br>
Risk: Heartbeat configuration can affect agents beyond the roleplay agent when configured globally. <br>
Mitigation: Scope heartbeat behavior to the dedicated role-play agent where possible, and avoid agents.defaults unless global heartbeat behavior is intended. <br>
Risk: Calendar, reminder, or personal schedule data can influence roleplay personalization. <br>
Mitigation: Disable calendar and reminder personalization if private schedule data should not be used by the agent. <br>
Risk: Roleplay archives and generated images can retain intimate content over time. <br>
Mitigation: Use a private workspace and periodically delete archives or images that should not be retained. <br>
Risk: Messaging or image-service credentials can be exposed if bot tokens are stored in shared files. <br>
Mitigation: Keep bot tokens out of shared files and review channel configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nannyu/daily-roleplay-game) <br>
- [Project homepage](https://github.com/nannyu/openclaw-role-play-skill) <br>
- [OpenClaw setup guide](docs/OPENCLAW_SETUP.md) <br>
- [Cron configuration](docs/CRON_CONFIG.md) <br>
- [Daily roleplay design](docs/daily-roleplay-game.md) <br>
- [OpenClaw multi-agent documentation](https://docs.openclaw.ai/concepts/multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON/YAML configuration, shell commands, roleplay messages, and optional image-generation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local workspace files such as roleplay-active.md, guess-log.md, archives, tracker JSON, and image-generation configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
