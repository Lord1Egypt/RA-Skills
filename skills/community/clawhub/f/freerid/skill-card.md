## Description: <br>
Manages free AI models from OpenRouter for OpenClaw, automatically ranks models by quality, configures fallbacks for rate-limit handling, and updates openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goozdx-eng](https://clawhub.ai/user/goozdx-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenClaw with OpenRouter free models, ranked fallbacks, and optional model rotation when rate limits occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw's default model and fallback list. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before first use and review the changed model settings after running FreeRide. <br>
Risk: The skill requires an OpenRouter API key that could be exposed through shared or committed configuration. <br>
Mitigation: Use a dedicated OpenRouter key and avoid storing it in shared files or committed config. <br>
Risk: The optional watcher can run ongoing background checks and automatically rotate models. <br>
Mitigation: Run freeride-watcher --daemon only when continuous monitoring and automatic rotation are desired. <br>


## Reference(s): <br>
- [ClawHub FreeRide skill page](https://clawhub.ai/goozdx-eng/freerid) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend updates to ~/.openclaw/openclaw.json and optional background model-rotation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
