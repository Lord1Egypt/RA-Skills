## Description:

clawdess helps an agent generate persona-based photos, image-to-video clips, and short voice messages through configured third-party AI media providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwings](https://clawhub.ai/user/xwings)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a conversation should produce a generated photo, a short image-based video, or a voice note for the Clawdess persona. The skill requires the user or runtime to provide provider API credentials and, for visual generation, reference or source image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and voice text may be sent to selected third-party AI providers.

Mitigation: Use the skill only when the user understands and accepts provider data sharing, and avoid sensitive personal data in prompts, images, or voice text.

Risk: Broad conversational triggers may initiate media generation without sufficiently explicit consent and may incur provider costs.

Mitigation: Require confirmation for each generation request and keep API credentials scoped to the intended photo, video, or voice provider.

Risk: Generated photo and video files may be cached locally under ~/.openclaw/media/clawdess.

Mitigation: Review local retention needs and clear the cache when generated media should not remain on disk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwings/skills/clawdess)
- [xwings publisher profile](https://clawhub.ai/user/xwings)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Media URLs, Files, Guidance]

**Output Format:** [CLI-oriented Markdown guidance and text output containing MEDIA URLs; generated photo and video files may also be cached locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWDESS_PHOTO_API, CLAWDESS_VIDEO_API, or CLAWDESS_VOICE_API depending on the selected subcommand.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
