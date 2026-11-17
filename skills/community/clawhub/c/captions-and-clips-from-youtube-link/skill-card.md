## Description:

Turns YouTube videos into short-form clips with captions and hook titles through the MakeAIClips API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nosselil](https://clawhub.ai/user/nosselil)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media teams, and developers use this skill to ask an agent to submit YouTube URLs or uploaded videos to MakeAIClips, monitor processing, and retrieve vertical clips with captions and hook titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube URLs, uploaded video files, processing preferences, transcripts, generated clip metadata, and the MakeAIClips API key to makeaiclips.live.

Mitigation: Use it only for videos appropriate for that external service, review the service's privacy and retention terms, and avoid private or sensitive videos unless those terms are acceptable.

Risk: The skill may surface signup, subscription, or upgrade prompts while handling clip limits or onboarding.

Mitigation: Review the skill's user-facing prompts before deployment so promotional messaging fits the intended environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nosselil/skills/captions-and-clips-from-youtube-link)
- [MakeAIClips web app](https://makeaiclips.live)
- [MakeAIClips API documentation](https://makeaiclips.live/docs)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, and downloaded MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAKEAICLIPS_API_KEY and sends video URLs or uploaded video files to MakeAIClips for processing.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
