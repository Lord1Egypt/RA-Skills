## Description:

Converts text or Markdown files into speech audio using Volcengine V3 async long-text synthesis, with voice, emotion, SSML, and subtitle timestamp options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyphper](https://clawhub.ai/user/happyphper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synthesize spoken audio from direct text, Markdown, or text files for audiobooks, bedtime stories, and batch audio production. It is useful when an agent needs to prepare Volcengine TTS commands, configure required credentials, and generate audio or subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text or file contents are sent to Volcengine for processing.

Mitigation: Use the skill only with content approved for Volcengine processing and avoid submitting sensitive or restricted text.

Risk: Passing the Volcengine access token on the command line can expose it through shell history or process inspection.

Mitigation: Set credentials through a protected environment or credential manager and rotate any token previously entered in shell history.

Risk: The installer installs unpinned Python packages into the active environment.

Mitigation: Use a virtual environment and pin or review package versions before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/happyphper/skills/doubao-tts-cn)
- [Volcengine console](https://console.volcengine.com/)
- [Volcengine TTS submit endpoint](https://openspeech.bytedance.com/api/v3/tts/submit)
- [Volcengine TTS query endpoint](https://openspeech.bytedance.com/api/v3/tts/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and generated audio or subtitle file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3, WAV, PCM, OGG Opus, subtitle JSON, and SRT files through Volcengine API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
