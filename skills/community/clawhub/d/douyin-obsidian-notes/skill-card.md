## Description: <br>
Saves Douyin video and image-post content into Obsidian notes by extracting or transcribing the content, summarizing it, and writing structured Markdown to a configured vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpf](https://clawhub.ai/user/charles-lpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Obsidian vaults use this skill to archive Douyin links as structured notes with summaries, key points, source links, and original transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a real-looking Groq API key in config.json. <br>
Mitigation: Revoke or replace the bundled key before use, store credentials through a safer secret mechanism when possible, and avoid publishing configured secrets with the skill. <br>
Risk: Douyin audio or text may be sent to Groq for transcription and then saved into an Obsidian vault. <br>
Mitigation: Process only content the user is comfortable sharing with Groq and storing locally, and disclose this data flow before running the workflow. <br>
Risk: The skill runs browser automation, downloads media, converts audio, calls an external API, and writes files to an Obsidian vault. <br>
Mitigation: Review generated commands and configured vault paths before execution, and confirm dependencies are installed from trusted sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charles-lpf/douyin-obsidian-notes) <br>
- [Groq Console](https://console.groq.com) <br>
- [Groq Audio Transcriptions API Endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>
- [Douyin Web](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, inline shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Obsidian notes containing an AI summary, key points, optional quotes or action items, original transcript or extracted post text, and the source link.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
