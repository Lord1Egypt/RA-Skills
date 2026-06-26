## Description: <br>
Fixes OpenClaw's OpenRouter model prefix routing so free-model fallback switching works reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rongtianhua](https://clawhub.ai/user/rongtianhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to configure OpenRouter free models, rank fallback models, and repair fallback model prefixes so rate-limit fallback works reliably. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenRouter credentials from environment variables, OpenClaw config, and local agent auth profile files. <br>
Mitigation: Prefer an explicit OPENROUTER_API_KEY for the session, protect local credential files and shell history, and review the credential lookup behavior before use. <br>
Risk: The skill persistently rewrites OpenClaw model configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running it and verify the resulting primary and fallback model settings before restarting the gateway. <br>
Risk: The watcher can make OpenRouter chat completion checks while rotating models. <br>
Mitigation: Run watcher commands only with an intended OpenRouter account and key, and review external API usage before enabling daemon mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rongtianhua/free-ride-prefix-fix) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw model settings and local FreeRide cache or watcher state files.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence, skill.json, setup.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
