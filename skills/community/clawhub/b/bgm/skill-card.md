## Description:

Generate original background music for short videos from a natural language description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn a short video scene, mood, style, and duration into three original instrumental background music options using SenseAudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell examples handle user-derived style text unsafely when building request JSON.

Mitigation: Build request payloads with a JSON-aware tool such as jq before executing API calls.

Risk: Polling the external API can run indefinitely.

Mitigation: Add explicit timeouts, retry limits, or maximum polling duration before routine use.

Risk: The skill calls an external music-generation API and requires a SenseAudio API key.

Mitigation: Review API privacy terms and disclose external API use before sending user prompts or project details.

## Reference(s):

- [SenseAudio](https://senseaudio.cn)
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/bgm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with generated audio links and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three instrumental BGM variations with duration and audio URL fields when the external API succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
