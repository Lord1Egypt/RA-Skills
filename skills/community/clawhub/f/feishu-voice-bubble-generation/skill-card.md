## Description:

This skill guides a Feishu agent to generate voice-bubble messages by converting text to MP3, transcoding it to Opus, and sending the Opus file through Feishu messaging tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lens-lzy](https://clawhub.ai/user/lens-lzy)

### License/Terms of Use:

MIT-0

## Use Case:

Feishu bot developers and operators use this skill to send text as native voice-bubble messages and manage Chinese voice selections. The skill helps agents keep MP3 audio as an intermediate artifact and send Opus output as the default voice-bubble format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can modify the host environment by installing Python and system packages.

Mitigation: Install and review the skill in an isolated virtual environment or container, and manually approve any ffmpeg system-package installation.

Risk: The installer pulls edge-tts without a pinned version.

Mitigation: Pin and verify the edge-tts package version before installing in shared, production, or privileged environments.

Risk: Broad voice-related trigger words may activate the skill outside Feishu voice-bubble requests.

Mitigation: Narrow triggers to Feishu-specific voice-bubble requests before deployment where accidental activation matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lens-lzy/skills/feishu-voice-bubble-generation)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu voice-bubble workflow instructions, including text-to-speech voice selection and MP3-to-Opus conversion steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
