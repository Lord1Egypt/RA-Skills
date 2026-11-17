## Description:

Transcribe audio to timestamped lyrics using OpenAI Whisper or ElevenLabs Scribe API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dumoedss](https://clawhub.ai/user/dumoedss)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to transcribe songs or other audio into timestamped lyric files for editing, synchronization, or downstream media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports serious implementation weaknesses that could expose API keys or run unintended local code with crafted inputs.

Mitigation: Review before installing, use only non-sensitive audio, use disposable or tightly scoped API keys, and avoid custom output paths with special characters until the reported issues are fixed.

Risk: Local configuration may contain provider credentials.

Mitigation: Keep the generated config file protected, use masked config listing for review, and do not use config --get for secret fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dumoedss/skills/acestep-lyrics-transcription)
- [OpenAI API key setup](https://platform.openai.com/api-keys)
- [ElevenLabs API key setup](https://elevenlabs.io/app/settings/api-keys)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Bash commands; generated LRC, SRT, or JSON transcription files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3 or python, and a configured OpenAI or ElevenLabs API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
