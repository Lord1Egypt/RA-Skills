## Description:

Clone Wizard guides users through preparing voice recordings, checking audio quality with SenseAudio, completing platform-based voice cloning, and generating a first playback preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare recordings, interpret SenseAudio audio-quality feedback, complete platform voice cloning, and create an initial cloned-voice preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends voice recordings and cloned-voice identifiers to SenseAudio using the user's configured API key.

Mitigation: Use the skill only when users understand and consent to those external uploads, and confirm before uploading audio or generating previews.

Risk: The security summary flags an unsafe shell pattern for user-provided voice_id values.

Mitigation: Validate or safely quote voice_id values before incorporating them into shell examples or API requests.

## Reference(s):

- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/clone-wizard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and generated audio-file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and uses curl, jq, and xxd for API-backed checks and preview generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
