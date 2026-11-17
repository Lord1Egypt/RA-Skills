## Description:

Generate images, videos, and audio via fal.ai API (FLUX, SDXL, Whisper, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[agmmnn](https://clawhub.ai/user/agmmnn)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to call fal.ai queue endpoints for image generation, video generation, and audio transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a fal.ai API key that may incur usage charges if exposed or misused.

Mitigation: Use FAL_KEY or a protected config entry, avoid passing keys on the command line, rotate any key previously passed as --api-key, and restrict use to trusted model endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agmmnn/skills/fal-ai)
- [fal.ai API key dashboard](https://fal.ai/dashboard/keys)
- [fal.ai queue API endpoint](https://queue.fal.run)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated media URLs, queue request identifiers, model lists, and transcription results from fal.ai.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
