## Description:

Processes inbound audio files by converting non-WAV inputs to WAV, transcribing them, and answering the resulting text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirkovz](https://clawhub.ai/user/sirkovz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn trusted local inbound audio into German text instructions or questions that the agent can answer like normal chat input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound audio can influence agent behavior after transcription, and unsafe local command templates may mishandle untrusted file paths.

Mitigation: Process only trusted audio from the specified inbound directory, validate and canonicalize filenames, use safe argument-array execution for ffmpeg and whisper, write conversions to a controlled temporary location, and require user confirmation before broader agent actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirkovz/skills/audio-command-executor)
- [Publisher profile](https://clawhub.ai/user/sirkovz)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell command snippets and clear error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German-language responses; audio paths should be trusted and validated before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
