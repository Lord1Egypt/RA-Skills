## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking available free models, configuring fallbacks for rate-limit handling, and updating OpenClaw model settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find free OpenRouter models, set a primary model, configure fallback models, and recover from rate limits with less manual model switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the release has inconsistent install identity and can persistently change OpenClaw global model settings. <br>
Mitigation: Verify that the ClawHub slug, install command, local path, and version refer to the same package, then back up ~/.openclaw/openclaw.json before running configuration-changing commands. <br>
Risk: The skill requires an OpenRouter API key that may appear in local configuration or terminal output. <br>
Mitigation: Use a dedicated OpenRouter key, avoid sharing config or command output that contains it, and rotate the key if it is exposed. <br>
Risk: The optional watcher can keep running and automatically rotate models after rate-limit checks. <br>
Mitigation: Run freeride-watcher --daemon only when ongoing automatic rotation is intended, and use watcher status or process controls to confirm it is running only as expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tigertamvip/free-ride-1) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json model defaults and fallback lists when the CLI is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
