## Description: <br>
Simple model router for OpenClaw. Switch between available models based on task type. No manual config needed - just use natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SiliconYahaha](https://clawhub.ai/user/SiliconYahaha) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to switch between validated OpenClaw models with natural-language commands or task descriptions, especially when routing image, file, PDF, screenshot, or multimodal work to Gemini 3 Flash and other work to OpenRouter Auto. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw's active model and restart the gateway from broad natural-language triggers, which may interrupt active work. <br>
Mitigation: Install only when always-available model routing is desired, and avoid enabling it during active work unless session interruption is acceptable. <br>
Risk: Model switches can affect provider cost and privacy expectations. <br>
Mitigation: Review approved providers, costs, and data-handling expectations before use. <br>


## Reference(s): <br>
- [Claw Switch package page](https://clawhub.ai/SiliconYahaha/claw-switch) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [catalog.json](artifact/catalog.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Plain text responses with OpenClaw shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May switch OpenClaw's active model and restart the gateway when routing or switching is triggered.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
