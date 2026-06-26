## Description: <br>
Use when someone wants to install, configure, onboard, script, or troubleshoot the ricebowl.ai-first ai-media CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchanzis](https://clawhub.ai/user/jinchanzis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to install and configure the ai-media CLI, onboard to ricebowl.ai, inspect available models, and script image or video generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through API key setup for a hosted service. <br>
Mitigation: Use a dedicated revocable API key and avoid exposing keys or configuration output in chats, logs, screenshots, or CI. <br>
Risk: Generation and recharge commands can spend credits and send prompts, images, or metadata to ricebowl.ai. <br>
Mitigation: Review and approve recharge, image generation, video generation, and task submission commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jinchanzis/ai-media-generator-ai-media-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/jinchanzis) <br>
- [ai-media-generator Homepage](https://github.com/214140846/ai-media-generator) <br>
- [ricebowl.ai](https://ricebowl.ai) <br>
- [ricebowl.ai Pricing](https://ricebowl.ai/pricing) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Platform Onboarding Reference](references/platform-onboarding.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI commands for model discovery and task polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
