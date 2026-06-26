## Description: <br>
Manages AI models from SkillBoss API Hub for OpenClaw, ranks models by quality, configures fallbacks for rate-limit handling, and updates openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure free AI model routing, ranked fallback models, and model status checks when they want to reduce model costs or recover from rate limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw default and fallback model routing. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running setup commands, review the resulting model configuration, and verify the active model after restarting OpenClaw. <br>
Risk: Provider and API-key instructions are inconsistent between SkillBoss/HeyBossAI and OpenRouter. <br>
Mitigation: Confirm the intended provider for this release and use only the matching API key. <br>
Risk: Watcher commands are documented, but the provided watcher artifact has no implementation content. <br>
Mitigation: Avoid watcher or daemon commands until the maintainer clarifies the implementation and stop behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-freeride) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide edits to OpenClaw model routing and API-key configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
