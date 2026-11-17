## Description:

Helps agents guide users through Azure-based batch speech-to-text transcription for audio files, including basic transcript and timestamp output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, independent creators, and workflow developers use this skill to prepare Azure Speech transcription jobs for podcasts, meetings, and video subtitle workflows. It helps configure Azure endpoints, keys, Blob audio URLs, language settings, and timestamped transcript handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for unrelated translation or localization tasks because its activation guidance is broader than its Azure transcription purpose.

Mitigation: Use it only for Azure-based audio transcription workflows and route translation, localization, or creative-writing requests to a more appropriate skill.

Risk: Audio recordings, Blob URLs, Azure endpoints, and subscription keys are sensitive and may be exposed during setup or generated command execution.

Mitigation: Confirm the target Azure resource, storage URL, output path, and credential handling before running generated Python or shell commands; keep keys in environment variables or a secret manager.

Risk: The skill relies on command execution and cloud audio processing, which can cause unintended actions if commands are run without review.

Mitigation: Review generated code and shell commands before execution, especially dependency installation, network access, and output file writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-transcription-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Azure transcription setup guidance, executable examples, and transcript or subtitle file handling instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
