## Description:

Provides local ASR transcription with speaker diarization using FunASR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwanai](https://clawhub.ai/user/lgwanai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and media teams use this skill to transcribe audio or video files, identify speakers, and generate timestamped text, subtitle, JSON, or Markdown outputs with local processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the package is not self-contained and relies on a missing local asr_skill Python package resolved from a broad ancestor path.

Mitigation: Install and run it only in an isolated environment where the asr_skill dependency is pinned, reviewed, and trusted before processing media.

Risk: Asynchronous runs store task metadata in a weakly scoped persistent file, which may retain media paths and processing status.

Mitigation: Avoid sensitive media until task-state storage and cleanup are tightened, and remove task metadata after use when appropriate.

## Reference(s):

- [Output Format Specifications](references/output-formats.md)
- [ClawHub skill page](https://clawhub.ai/lgwanai/skills/asr-skills)
- [Publisher profile](https://clawhub.ai/user/lgwanai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, SRT, ASS/SSA, Markdown, Python snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include timestamps, speaker labels, confidence scores, word-level details, overlap markers, styled subtitle metadata, and task status JSON for asynchronous runs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
