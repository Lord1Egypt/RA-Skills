## Description:

Turns tagged scripts or existing audio and video into multi-speaker voiceovers and timed subtitles through Miragea’s API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghhu](https://clawhub.ai/user/yanghhu)

### License/Terms of Use:

MIT

## Use Case:

Video creators and editors use the skill to turn scripts into multi-speaker narration with timed captions, or to transcribe existing audio and video into subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio, video, transcripts, or reference recordings may be sent to the third-party Miragea service.

Mitigation: Review Miragea’s privacy terms and submit only material you are authorized to share; use --dry-run to check scripts without sending content to the API.

Risk: Voice cloning can reproduce a speaker’s voice.

Mitigation: Clone only your own voice or a voice for which you have explicit permission.

Risk: API usage is subject to account quotas, rate limits, and charges.

Mitigation: Check current limits and pricing with the API capabilities command before generating at scale.

Risk: An exposed MIRAGEA_API_KEY could allow unauthorized use of the account.

Mitigation: Keep the key in an environment variable and do not paste it into chats or save it in files.

## Reference(s):

- [Miragea](https://miragea.ai)
- [Miragea API](https://miragea.ai/v1)
- [ClawHub skill release](https://clawhub.ai/yanghhu/skills/ai-video-voiceover-subtitles)

## Skill Output:

**Output Type(s):** [Audio files, Subtitle files, JSON]

**Output Format:** [WAV audio, SRT subtitles, and a JSON timing manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voiceover and recognition use Miragea’s API; --dry-run checks a script offline without an API call.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
