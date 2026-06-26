## Description: <br>
Extracts Douyin video transcripts and saves them as structured Obsidian Markdown notes, using local Whisper transcription when subtitles are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scutlhp](https://clawhub.ai/user/scutlhp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to turn public Douyin video links or share text into Obsidian-ready Markdown notes with transcript text and video metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Douyin access in ways intended to bypass platform protections. <br>
Mitigation: Install only if that behavior is acceptable for the intended use, pass explicit public Douyin URLs, and avoid logged-in or private content. <br>
Risk: The skill includes unverified runtime binary downloads for FFmpeg. <br>
Mitigation: Use a virtual environment and manually install or verify FFmpeg instead of relying on the automatic download. <br>
Risk: The skill writes Markdown files automatically to the configured Obsidian path. <br>
Mitigation: Review and adjust the target Obsidian directory before running the extraction script. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/scutlhp/douyin-to-obsidian) <br>
- [Architecture documentation](reference/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, console status text, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown files to a configured Obsidian directory and may download local transcription or media-processing dependencies during setup or first run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and CLAWHUB.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
