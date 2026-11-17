## Description:

Adds synchronized sound effects to silent video clips and routes narration or music requests to the appropriate sibling skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to decide whether a silent video needs synchronized sound effects, narration, or music, then run the SFX path for short clips using Mirelo SFX 1.5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected video clips and prompts are sent to an external model provider.

Mitigation: Use the skill only when provider processing is acceptable, and avoid sensitive or private footage unless that use is approved.

Risk: SFX coverage is limited and generated sound may be weak or poorly synchronized for some scenes.

Mitigation: Review the returned video for timing and sound fit, retry with a clearer prompt or seed, or regenerate the video with native audio when available.

## Reference(s):

- [Add Audio To Video on ClawHub](https://clawhub.ai/runware/skills/add-audio-to-video)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with model, routing, and parameter instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides video-input SFX jobs that return muxed video, and distinguishes them from prompt-only audio, narration, and music routes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
