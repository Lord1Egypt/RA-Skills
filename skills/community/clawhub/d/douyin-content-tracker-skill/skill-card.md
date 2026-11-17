## Description:

This skill helps an agent guide setup and operation of a Douyin creator-tracking pipeline that scrapes creator video metadata, extracts audio, and transcribes speech with Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpttang](https://clawhub.ai/user/gpttang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run recurring Douyin creator monitoring, including account lists, MediaCrawler setup, cookie refresh, audio extraction, and Whisper transcription. It is intended for workflows that need local CSV metadata, audio files, and Markdown transcripts from tracked Douyin profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an authenticated Douyin session and stores cookies locally, which could expose the session if copied, synced, or committed.

Mitigation: Use a dedicated Douyin account, keep cookie files out of shared folders and source control, and refresh cookies only through the documented login flow.

Risk: Downloaded media, transcripts, model files, and CSV outputs are written persistently to the configured output directory.

Mitigation: Set OUTPUT_BASE_DIR to a dedicated local folder, review retention needs, and avoid storing sensitive outputs in synced or public directories.

Risk: Server security guidance flags blogger-name path sanitization as needing a fix before running on untrusted creator data.

Mitigation: Patch and review path sanitization before using untrusted account lists or creator names, then test output paths stay under the intended output directory.

Risk: The skill depends on MediaCrawler, Playwright, ffmpeg, and Whisper, which can fail or change behavior across environments.

Mitigation: Pin dependencies and MediaCrawler to reviewed versions, install browser and ffmpeg prerequisites explicitly, and follow the troubleshooting guide when scraping, audio extraction, or transcription fails.

## Reference(s):

- [Pipeline Reference](artifact/references/pipeline.md)
- [Troubleshooting Reference](artifact/references/troubleshooting.md)
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [ClawHub Skill Page](https://clawhub.ai/gpttang/skills/douyin-content-tracker-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The pipeline can produce local CSV metadata, M4A audio files, Markdown transcript files, and per-creator transcript summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
