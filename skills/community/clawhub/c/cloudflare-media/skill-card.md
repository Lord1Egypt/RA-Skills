## Description:

Generates images and text-to-speech audio with Cloudflare Workers AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nsense11](https://clawhub.ai/user/n0nsense11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to select Cloudflare Workers AI image or TTS models, configure credentials, and generate image or audio outputs from prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Cloudflare credentials from local config or general agent memory and requests broad local tool access.

Mitigation: Review before installing, use a narrowly scoped Cloudflare Workers AI token, avoid storing the token in MEMORY.md, and narrow allowed tools where possible.

Risk: Prompts, private images, or confidential text may be sent to Cloudflare Workers AI.

Mitigation: Do not submit sensitive content unless approved, and add an explicit confirmation or disclosure step before external requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n0nsense11/skills/cloudflare-media)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with curl examples and generated image or audio file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG/JPEG images or MP3/WAV audio through Cloudflare Workers AI.]

## Skill Version(s):

2.2.0 (source: frontmatter; server release metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
