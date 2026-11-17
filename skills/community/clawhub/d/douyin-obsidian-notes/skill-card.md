## Description:

Saves Douyin video or image-post content into Obsidian notes by extracting page content, transcribing audio with Groq Whisper, summarizing it, and writing structured Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpf](https://clawhub.ai/user/charles-lpf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Douyin links into structured Obsidian notes with summaries, key points, transcripts, and source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a live-looking Groq API key in config.json.

Mitigation: Remove the bundled key, revoke it if it was ever valid, and require each installer to provide their own user-owned key.

Risk: Audio or extracted page text may be sent to Groq for transcription.

Mitigation: Confirm that the user is allowed to send the selected Douyin content to Groq before transcription.

Risk: Shell commands consume user-provided Douyin URLs and page-derived titles, transcripts, and generated Markdown.

Mitigation: Quote and sanitize URLs, titles, file paths, transcripts, and Markdown before use in shell commands or Obsidian writes.

Risk: The workflow writes generated notes and properties into an Obsidian vault.

Mitigation: Confirm the target vault and folder before writing, and avoid silent writes until configuration is user-owned.

Risk: The workflow depends on external tools and services including agent-browser, ffmpeg, Obsidian CLI, Douyin, and Groq.

Mitigation: Install trusted versions from known sources, prefer pinned or locally reviewed dependencies, and verify tool availability before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charles-lpf/skills/douyin-obsidian-notes)
- [Publisher profile](https://clawhub.ai/user/charles-lpf)
- [Groq Console](https://console.groq.com)
- [Groq audio transcription endpoint](https://api.groq.com/openai/v1/audio/transcriptions)
- [Douyin](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and shell/API command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Obsidian Markdown notes with frontmatter, summary, key points, transcript, and source link; may use temporary local audio files during transcription.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
