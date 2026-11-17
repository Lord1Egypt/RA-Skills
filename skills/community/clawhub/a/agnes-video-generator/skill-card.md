## Description:

Generates AI videos from text prompts or image URLs using Agnes-Video-V2.0, with configurable frames, frame rate, resolution, seed, negative prompts, and asynchronous polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lg0219](https://clawhub.ai/user/lg0219)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to ask an agent to generate short videos from prompts or animate image URLs through Agnes, then receive a direct video URL and generation metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and generation parameters are sent to the Agnes API for processing.

Mitigation: Avoid sensitive or private media unless external processing by Agnes is acceptable.

Risk: Video generation may incur Agnes API costs.

Mitigation: Review Agnes pricing and usage limits before running large or repeated generations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lg0219/skills/agnes-video-generator)
- [Agnes Video API Endpoint](https://apihub.agnes-ai.com/v1/videos)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON containing success status, generated video URL, size, duration, video ID, and generation status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGNES_API_KEY and sends prompts, image URLs, and generation parameters to Agnes for asynchronous processing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
