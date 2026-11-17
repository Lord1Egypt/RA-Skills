## Description:

Generate AI images using MiniMax or fal.ai (Grok Imagine) and send them to messaging channels through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate character selfie images from a fixed reference image, choose mirror or direct selfie modes, and send the generated image to channels through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can persistently change OpenClaw workspace files and agent identity/persona content.

Mitigation: Prefer manual installation or a pinned package version, and back up existing OpenClaw workspace files before installing.

Risk: API keys and gateway tokens may be exposed if stored in plaintext configuration.

Mitigation: Use environment variables or a secret manager where possible, and avoid committing or sharing local OpenClaw configuration files containing credentials.

Risk: The TypeScript sender uses shell command execution for OpenClaw message sending.

Mitigation: Do not use the TypeScript sender until it uses a non-shell argument API for OpenClaw command execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honestqiao/skills/clawra-selfie-minimax)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [fal.ai](https://fal.ai)
- [MiniMax platform](https://platform.minimaxi.com)
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation)
- [fal.ai Grok Imagine image edit endpoint](https://fal.run/xai/grok-imagine-image/edit)
- [Reference image](https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and TypeScript examples; runtime scripts produce image URLs and OpenClaw message-send actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider API keys and an OpenClaw gateway to generate and send images.]

## Skill Version(s):

1.2.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
