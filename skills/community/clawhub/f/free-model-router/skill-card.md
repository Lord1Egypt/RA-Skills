## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking available free models, configuring fallbacks for rate-limit handling, and updating OpenClaw model configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find free OpenRouter models, configure primary and fallback models, and reduce model-serving costs in an OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marked suspicious because bundled jobs/ scripts are unrelated to the advertised free-model routing purpose. <br>
Mitigation: Remove or ignore the jobs/ directory if you only need model routing, and run only the documented freeride commands. <br>
Risk: The documented CLI can update ~/.openclaw/openclaw.json, and the watcher can run continuous OpenRouter probing and model rotation. <br>
Mitigation: Back up the OpenClaw config before use, and avoid freeride-watcher --daemon unless continuous automatic checks and config rotation are intended. <br>
Risk: The skill requires an OpenRouter API key and sends model-list or health-check requests to OpenRouter. <br>
Mitigation: Keep the API key in the environment or OpenClaw config, avoid hard-coding it in files, and review outbound API use before running watcher commands. <br>


## Reference(s): <br>
- [Free Model Router on ClawHub](https://clawhub.ai/ricksmartbrain-boop/free-model-router) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may modify ~/.openclaw/openclaw.json when executed by the user or agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact skill.json agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
