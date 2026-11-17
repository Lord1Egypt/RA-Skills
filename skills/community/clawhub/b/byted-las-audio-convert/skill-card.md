## Description:

Converts and transcodes audio files with Volcengine LAS, including format changes and adjustments to sample rate, bitrate, channels, compression, and ffmpeg parameters for TOS paths or local uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare or convert audio assets for downstream workflows, including changing container format, sample rate, bitrate, channels, and compression settings. It supports local file upload and TOS cloud storage paths through the Volcengine LAS audio conversion operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The environment setup can install a remote Volcengine LAS SDK wheel without pinned verification.

Mitigation: Review or pin the SDK package before use and install only in an isolated environment.

Risk: The workflow handles LAS and optional TOS cloud credentials.

Mitigation: Use narrowly scoped or temporary credentials and avoid broad long-lived keys where possible.

Risk: Audio conversion can upload local files or write outputs to TOS paths after price estimation.

Mitigation: Keep the required user confirmation pause before upload or conversion and confirm the target region and bucket path.

## Reference(s):

- [las_audio_convert API reference](references/api.md)
- [Pricing information](references/prices.md)
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-audio-convert)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and conversion result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated pricing guidance and a billing disclaimer before or after conversion execution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
