## Description:

Uses the BizyAir API and Nano Banana 2 model to generate images, including text-to-image, reference-image, and meme-style generation, without a local GPU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin-chen2026](https://clawhub.ai/user/kevin-chen2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images through BizyAir from prompts and optional reference images. It is intended for workflows that need cloud-hosted image generation, aspect-ratio control, and optional JSON status output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid BizyAir API key and broad image-generation triggers may cause unintended paid use.

Mitigation: Confirm intent before running generation commands, set spending controls in the BizyAir account, and review generated-command parameters before execution.

Risk: Prompts and reference images are sent to BizyAir for processing.

Mitigation: Avoid submitting sensitive images or confidential prompts unless the user's BizyAir account and data-handling terms are acceptable.

Risk: API keys can be exposed through .env files, terminal output, logs, or screenshots.

Mitigation: Prefer environment variables or a secret manager, do not print .env files, never share terminal output containing secrets, and rotate any exposed key.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin-chen2026/skills/bizyair-banana2)
- [BizyAir Website](https://www.bizyair.cn)
- [BizyAir Documentation](https://docs.bizyair.cn)
- [BizyAir API Reference](https://docs.bizyair.cn/api/api-reference.html)
- [BizyAir Pricing](https://docs.bizyair.cn/pricing/introduce.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON]

**Output Format:** [Generated image files with terminal status output and optional JSON result metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BIZYAIR_API_KEY and may upload prompts and reference images to BizyAir.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
