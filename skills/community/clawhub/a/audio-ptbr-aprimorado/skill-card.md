## Description:

Audio PTBR provides a Brazilian Portuguese voice interface that transcribes audio, generates responses through Claude API or OpenClaw fallback, and synthesizes replies with Piper TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrique-simoes](https://clawhub.ai/user/henrique-simoes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this ClawHub skill to add Brazilian Portuguese voice interaction to OpenClaw, Claude Desktop, or standalone workflows by transcribing speech, generating a concise response, and returning speech or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and shell hook have broad execution authority on the host.

Mitigation: Review before installing, prefer a container or dedicated virtual environment, and avoid elevated privileges unless host package changes are acceptable.

Risk: Piper binaries and voice models are downloaded during setup without enough verification.

Mitigation: Verify or pin downloaded Piper and model artifacts before deployment.

Risk: The shell hook can pass user-controlled values into shell execution.

Mitigation: Fix the hook to pass arguments without shell interpolation and keep input validation enabled.

Risk: When ANTHROPIC_API_KEY is set, transcribed speech may be sent to Anthropic for response generation.

Mitigation: Set ANTHROPIC_API_KEY only when external processing of transcripts is acceptable; otherwise use the OpenClaw fallback.

## Reference(s):

- [Audio PTBR ClawHub listing](https://clawhub.ai/henrique-simoes/skills/audio-ptbr-aprimorado)
- [wav2vec2-large-xlsr-53-portuguese model card](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese)
- [Piper TTS project](https://github.com/rhasspy/piper)
- [Anthropic Claude](https://www.anthropic.com/claude)

## Skill Output:

**Output Type(s):** [Audio, Text, JSON, Shell commands, Configuration]

**Output Format:** [OGG/Opus audio, plain text, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Silent audio-only replies are the default; explicit text mode can return text instead of audio.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
