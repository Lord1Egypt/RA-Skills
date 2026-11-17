## Description:

Extracts speech from Douyin video links or local audio and video files, transcribes it with a local Whisper medium model, and helps the agent produce readable Chinese transcript Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuzheng60](https://clawhub.ai/user/liuzheng60)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Douyin videos or local media files into readable Chinese transcripts for review, caption extraction, or content understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Douyin fetcher can open and request arbitrary user-supplied URLs because Douyin-only domains are not enforced.

Mitigation: Run it only on trusted public Douyin links, avoid private or internal URLs, and review the link before execution.

Risk: Setup and first transcription can download large third-party dependencies, Chromium, and the Whisper model.

Mitigation: Run setup in a low-privilege isolated environment with enough disk space, and review network access expectations before installation.

Risk: Generated videos, transcripts, JSON output, and terminal logs may contain sensitive user media or speech content.

Mitigation: Store outputs in an appropriate workspace, restrict access to generated files, and remove local artifacts when they are no longer needed.

## Reference(s):

- [Whisper usage reference](references/whisper_usage.md)
- [ClawHub skill page](https://clawhub.ai/liuzheng60/skills/douyin-transcribe-lz)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown transcript plus raw TXT and JSON transcript files, with shell command guidance for setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are timestamped; Douyin mode may also save the downloaded MP4, and local mode reads the original media file in place.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
