## Description:

Extracts Douyin video transcripts and converts them into structured Obsidian Markdown notes, using local Whisper transcription when subtitles are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scutlhp](https://clawhub.ai/user/scutlhp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users can use this skill to turn Douyin video links or share text into local Markdown notes with video metadata and transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags platform-protection bypass, broad network access, and installation of an unverified executable dependency.

Mitigation: Run in a dedicated virtual environment or sandbox, use only Douyin links you trust, prefer a manually installed and verified FFmpeg, and test output in a non-synced vault before using important Obsidian notes.

## Reference(s):

- [Architecture Documentation](reference/architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/scutlhp/skills/douyin-to-obsidian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown notes with YAML frontmatter, plus console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript notes to a configured Obsidian directory and may create diagnostic files when extraction fails.]

## Skill Version(s):

1.0.0 (source: server release metadata and CLAWHUB.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
