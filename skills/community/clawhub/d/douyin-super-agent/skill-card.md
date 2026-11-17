## Description:

Processes Douyin video links or audio files to download media, extract audio, transcribe speech, correct common ASR errors, and save transcript and result files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pry520okgpt](https://clawhub.ai/user/pry520okgpt)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn Douyin video links or local audio files into cleaned transcripts and structured result files. It is useful for social video review, transcription, and content extraction workflows where users can control whether optional remote/cloud ASR integrations are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio or video content may be processed by optional remote/cloud ASR integrations when qwen-asr or Tencent Cloud ASR are available.

Mitigation: Avoid sensitive, private, credential-bearing, or regulated media unless remote ASR integrations are disabled or removed and local Whisper processing is used.

Risk: Transcript excerpts may be stored in a persistent local memory-manager skill.

Mitigation: Disable or remove the memory-manager integration, and review or clear local memory storage before handling private or regulated content.

Risk: Setup installs unpinned Python dependencies and relies on external tools.

Mitigation: Install in an isolated environment and pin or review dependencies and tool versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pry520okgpt/skills/douyin-super-agent)
- [Publisher profile](https://clawhub.ai/user/pry520okgpt)
- [Project homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Plain text transcripts, Markdown reports, JSON result files, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes media and transcript outputs under ~/Desktop/douyin-super-agent/ and may cache Whisper models under ~/.cache/whisper/.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
