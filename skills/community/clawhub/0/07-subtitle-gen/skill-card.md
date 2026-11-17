## Description:

Produces a local SRT-style subtitle response from optional dialogue text while accepting an audio URL input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and automation agents can use this skill to create a basic SRT subtitle response or link for short dramas, short videos, and batch audio-video workflows. This version should be reviewed with the understanding that the security evidence says it does not appear to analyze audio itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This version may not analyze audio despite accepting audio_url and describing automatic subtitle generation.

Mitigation: Treat the result as a basic SRT-style response from supplied dialogue and verify subtitle timing against the source audio before production use.

Risk: The available documentation is in Chinese, which may limit review by teams that require English operational documentation.

Mitigation: Have a Chinese-proficient reviewer validate the intended inputs, outputs, and behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/07-subtitle-gen)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing subtitle_url and SRT-style content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires audio_url and optionally dialogue; implementation evidence returns fixed 00:00:00 to 00:00:03 subtitle timing.]

## Skill Version(s):

1.0.3 (source: server release evidence; manifest reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
