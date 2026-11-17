## Description:

Creates reviewed, styled captions and subtitle files for videos, with optional translation and user-approved social posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use the skill to prepare accessible, platform-sized captions and subtitles, proofread translations, and optionally schedule approved video posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says transcription may use cloud services depending on available credentials, despite a stated local default.

Mitigation: Use local Whisper when audio must stay local; before cloud transcription, confirm the provider and what audio or vocabulary data it receives.

Risk: The partial security scan flags a possible unsafe file upload path and calls for review of API-key-in-URL guidance.

Mitigation: Review the upload destination and credential guidance before use; do not assume the partial scan establishes that the skill is safe.

## Reference(s):

- [Auto Captions Skill on ClawHub](https://clawhub.ai/social-media-skills/skills/auto-captions-skill)
- [Job File Format](artifact/references/job-file.md)
- [Proofreading Guide](artifact/references/proofreading.md)
- [Translation Guide](artifact/references/translation.md)
- [Caption Styles](artifact/references/styles.md)
- [Platform Guidance](artifact/references/platforms.md)
- [Posting Workflow](artifact/references/posting.md)
- [WoopSocial MCP Tools Reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Captioned video files, Subtitle files, Transcripts and translations, Posting plans]

**Output Format:** [MP4 video, SRT/VTT subtitles, plain-text transcripts, JSON job files, and Markdown plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by selected caption style, aspect ratio, language, and platform.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
