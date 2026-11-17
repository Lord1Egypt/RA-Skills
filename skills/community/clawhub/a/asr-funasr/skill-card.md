## Description:

Automatic Speech Recognition using OpenAI Whisper (local GPU). Supports Chinese, English, and 90+ languages. Auto-detects language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe audio files into text with either the default FunASR SenseVoice engine for Chinese, Japanese, Korean, and Cantonese speech or Whisper for multilingual transcription and translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default FunASR engine executes unpinned remote model code.

Mitigation: Review before installing, run only in an isolated environment without sensitive files or credentials, prefer Whisper when acceptable, and require pinned dependencies/model revisions or removal of trust_remote_code=True before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/asr-funasr)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Plain text transcript printed to stdout or written to a requested output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected language metadata in console output; Whisper mode can translate speech to English text.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
