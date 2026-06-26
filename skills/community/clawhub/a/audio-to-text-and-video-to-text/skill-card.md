## Description: <br>
Transcribes audio and video files into text using OpenAI's Whisper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to convert uploaded or local media files into transcripts, subtitles, captions, or structured transcription output. It supports audio extraction from video, chunked processing for larger files, and optional transcript cleanup or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio or video content is sent to OpenAI for transcription. <br>
Mitigation: Use only with media the user is comfortable processing through OpenAI, and consider privacy or data-handling requirements before running transcription. <br>
Risk: The skill requires an OpenAI API key and may expose the key if handled carelessly. <br>
Mitigation: Provide OPENAI_API_KEY through a secure environment variable or secret manager, and avoid pasting long-lived keys into chat. <br>
Risk: The transcription script may install Python dependencies at runtime. <br>
Mitigation: Preinstall or pin dependencies on shared, production, or sensitive machines instead of allowing runtime package installation. <br>


## Reference(s): <br>
- [OpenAI API Keys](https://platform.openai.com/api-keys) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated transcript files in TXT, SRT, VTT, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include timestamps, subtitle cues, segment metadata, language selection, model selection, chunk size, and prompt context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
