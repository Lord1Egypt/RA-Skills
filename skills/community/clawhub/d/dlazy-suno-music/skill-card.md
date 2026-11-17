## Description:

Suno music generation model. Supports inspiration mode (auto lyrics) and custom mode (manual lyrics), generating music with or without vocals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate songs from prompts, with optional custom lyrics, style, and vocal or instrumental settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that `dlazy login` has an unclear relationship to music generation, and some referenced material was unavailable for review.

Mitigation: Review the CLI install details and accessible references, and decide whether to authorize the login flow before using the skill.

Risk: The skill documentation says prompts and optional local media are sent to dLazy's hosted API and media storage.

Mitigation: Avoid submitting prompts or media that you are not comfortable sending to the hosted service.

## Reference(s):

- [CLI project homepage listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio files, JSON]

**Output Format:** [JSON result envelope with generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-based music generation; optional custom lyrics, style, title, vocal or instrumental settings, and asynchronous task status.]

## Skill Version(s):

1.3.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
