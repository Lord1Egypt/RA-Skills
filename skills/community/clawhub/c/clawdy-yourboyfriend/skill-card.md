## Description: <br>
Generate and send selfies of Clawdy across messaging platforms using xAI Grok Imagine via fal.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users install this skill to generate context-aware Clawdy selfies with xAI Grok Imagine via fal.ai and send them through connected messaging platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can persistently change the OpenClaw agent's identity and persona. <br>
Mitigation: Back up ~/.openclaw/workspace first and review SOUL.md and IDENTITY.md changes before using the skill. <br>
Risk: The skill stores a fal.ai API key in OpenClaw configuration. <br>
Mitigation: Use a dedicated key with appropriate account limits, protect ~/.openclaw/openclaw.json, and rotate the key if it is exposed. <br>
Risk: Prompts, reference imagery, and generated media can be uploaded to fal.ai/xAI and sent through connected messaging platforms. <br>
Mitigation: Use explicit recipient confirmation before sending media and avoid including sensitive personal content in prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawdy-yourboyfriend) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [fal.ai API keys](https://fal.ai/dashboard/keys) <br>
- [Grok Imagine edit endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, TypeScript and Bash examples, OpenClaw configuration, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates image URLs and local image files through fal.ai, then sends media through OpenClaw messaging channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
