## Description:

Transcribes Brazilian Portuguese audio locally with wav2vec2, generates a short OpenClaw or optional Anthropic response, and synthesizes a Portuguese voice reply with Piper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrique-simoes](https://clawhub.ai/user/henrique-simoes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to process Brazilian Portuguese voice messages in OpenClaw, returning a short agent response as synthesized speech. It is suited to accessibility, mobile, Telegram-style, and hands-busy reply workflows where local transcription and synthesis are preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a malformed shell-templated /voz trigger.

Mitigation: Replace the shell-string action with structured argument passing or remove the trigger before shared or sensitive deployment.

Risk: The installer downloads executable and model assets without integrity checks.

Mitigation: Add integrity verification for downloaded Piper assets and review the resolved download sources before installation.

Risk: Python dependencies are version-pinned but not hash-locked.

Mitigation: Use locked dependency hashes for reproducible installs.

Risk: Optional external response generation can send transcript text to Anthropic when ANTHROPIC_API_KEY is set.

Mitigation: Leave ANTHROPIC_API_KEY unset for local-only response generation, and use a trusted private WORKSPACE path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henrique-simoes/skills/audio-ptbr-autoreply)
- [wav2vec2 Portuguese ASR model](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese)
- [Piper releases](https://github.com/rhasspy/piper/releases)
- [Piper PT-BR voice models](https://huggingface.co/rhasspy/piper-voices)

## Skill Output:

**Output Type(s):** [text, audio, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON from helper scripts, shell command output, and a MEDIA directive pointing to the generated audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local mode is the default; transcript text may be sent to Anthropic only when ANTHROPIC_API_KEY is configured.]

## Skill Version(s):

2.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
