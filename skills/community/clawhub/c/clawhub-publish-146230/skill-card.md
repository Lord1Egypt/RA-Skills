## Description:

Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). High quality, native generation without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxw975](https://clawhub.ai/user/gxw975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files from text prompts through a credentialed internal Google Antigravity image service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an external generate.js script that is not included in the artifact and can use local OAuth credentials.

Mitigation: Install only after confirming the script exists from a trusted source, is not writable by untrusted users, and is intended to use the configured Google Antigravity OAuth profile.

Risk: Image requests are routed through a credentialed internal service.

Mitigation: Use an appropriate OAuth profile and avoid sending prompts or output paths that disclose sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxw975/skills/clawhub-publish-146230)
- [Publisher profile](https://clawhub.ai/user/gxw975)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes an image file to a requested path and emits a MEDIA path for agent display.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
