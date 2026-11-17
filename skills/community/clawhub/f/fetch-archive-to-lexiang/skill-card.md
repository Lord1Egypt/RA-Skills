## Description:

Discovers and fetches articles, videos, podcasts, and PDFs into standardized source packages, then orchestrates deduplicated Lexiang archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajaxhe](https://clawhub.ai/user/ajaxhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-management users use this skill to collect source material, preserve original content and media, prepare Markdown work packages, and archive final pages or VOD media into Lexiang with directory deduplication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in browser session and Lexiang credentials while fetching and archiving content.

Mitigation: Run it only when that access is intentional, prefer an isolated browser profile, and avoid daily browser sessions or environments containing sensitive organizational data.

Risk: Local helper configuration under ~/.fetch_article can influence browser-session behavior.

Mitigation: Review helper configuration before use and confirm the selected browser profile and CDP port are appropriate for the archival task.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ajaxhe/skills/fetch-archive-to-lexiang)
- [README](README.md)
- [Lexiang upload reference](references/lexiang-upload.md)
- [YouTube video reference](references/youtube-video.md)
- [Podcast audio reference](references/podcast-audio.md)
- [PDF processing reference](references/pdf-processing.md)
- [Platform-specific reference](references/platform-specific.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown work packages, JSON metadata, media files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces immutable source.md plus meta.json and title-named Markdown; may preserve images and media files for Lexiang upload.]

## Skill Version(s):

4.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
