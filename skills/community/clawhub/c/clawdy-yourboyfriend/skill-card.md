## Description:

Generate and send selfies of Clawdy across messaging platforms using xAI Grok Imagine via fal.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users install this skill to generate persona-consistent Clawdy selfies from a user prompt and send them to configured messaging channels. It supports companion-agent workflows that need image generation and message delivery through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently change the broader OpenClaw agent persona by writing IDENTITY.md and appending to SOUL.md.

Mitigation: Back up IDENTITY.md and SOUL.md before installation, review the proposed persona changes, and install only when a companion persona is intended.

Risk: The installer stores the fal.ai API key in the local OpenClaw configuration.

Mitigation: Use a limited, rotatable fal.ai key and review openclaw.json after setup.

Risk: The skill can send generated media to messaging channels through OpenClaw.

Mitigation: Review the destination channel, caption, and generated image before sending, especially in shared or external channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawdy-yourboyfriend)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [fal.ai](https://fal.ai)
- [fal.ai Grok Imagine edit endpoint](https://fal.run/xai/grok-imagine-image/edit)
- [Clawdy reference image](https://cdn.jsdelivr.net/gh/X-RayLuan/Clawdy-YourBoyfriend@main/assets/clawdy.png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and code examples; scripts may output JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates image-edit requests through fal.ai and sends resulting media through OpenClaw; destination and caption are supplied by the user or agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
