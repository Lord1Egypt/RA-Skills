## Description:

Automatically extracts audio from video or audio files, transcribes it with qwen3-asr-flash, and writes a segmented text summary next to the source file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanoo7](https://clawhub.ai/user/alanoo7)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to turn short audio or video files into transcribed summaries for review, note-taking, or content triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships with an exposed API key.

Mitigation: Revoke the embedded key and require users to provide their own secret through a secure environment or configuration mechanism before use.

Risk: Unsafe command execution could allow crafted filenames to run local commands.

Mitigation: Call ffmpeg through a subprocess argument list and validate input paths before execution.

Risk: Audio or video-derived content is uploaded to a third-party ASR provider.

Mitigation: Warn users before upload and require consent for files that may contain private, confidential, or regulated content.

Risk: Temporary audio output uses a predictable shared filename.

Mitigation: Use unique private temporary files and clean them up reliably after processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alanoo7/skills/audio-summary)
- [Publisher profile](https://clawhub.ai/user/alanoo7)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript and segmented summary saved as a .txt file, with progress messages printed to the shell.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes a single input audio or video path and may create a temporary compressed audio file during execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
