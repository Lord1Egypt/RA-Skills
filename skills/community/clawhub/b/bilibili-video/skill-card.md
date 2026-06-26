## Description: <br>
Bilibili Video extracts Bilibili video subtitles or audio transcripts using a fallback flow from creator-provided captions to AI subtitles to local audio download and ASR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a Bilibili URL or BV/AV identifier and needs video information, subtitles, downloaded audio, or transcript text for summarization and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and refresh reusable Bilibili session cookies. <br>
Mitigation: Prefer unauthenticated use when possible, avoid pasting raw cookies into chat, and delete the saved cookie file when no longer needed. <br>
Risk: The skill can download or save video-derived transcript and audio files locally. <br>
Mitigation: Review the target video before use and delete /tmp/openclaw/bilibili/ outputs after they are no longer needed. <br>
Risk: ASR fallback may run additional local transcription tooling after audio download. <br>
Mitigation: Disable ASR fallback when only subtitle retrieval is required or when local transcription tooling is not approved. <br>


## Reference(s): <br>
- [Bilibili API Notes](references/api-notes.md) <br>
- [Bilibili Video on ClawHub](https://clawhub.ai/guoqunabc/bilibili-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript files with video metadata and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes transcript and optional audio-derived files under /tmp/openclaw/bilibili/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
