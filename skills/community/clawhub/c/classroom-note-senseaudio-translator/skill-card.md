## Description: <br>
Transcribes English classroom audio, lecture videos, meeting recordings, or page-linked media with SenseAudio ASR, then produces Chinese study notes with summaries, key concepts, timelines, review questions, and optional Notion or Obsidian export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KLilyZ](https://clawhub.ai/user/KLilyZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and knowledge workers use this skill to turn English classes, lectures, group meetings, or learning media into structured Chinese Markdown notes for review. It is most useful when the user wants transcription plus summarized study material rather than a raw transcript only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected recordings are uploaded to SenseAudio for transcription. <br>
Mitigation: Use the skill only with recordings the user is allowed to process, avoid confidential or unauthorized content, and review SenseAudio handling requirements before use. <br>
Risk: Optional OpenAI-compatible summarization, Notion export, and page-media download can send transcripts, notes, tokens, or media URLs to additional services. <br>
Mitigation: Use scoped tokens, enable only the exports needed for the task, and set OPENAI_BASE_URL only to an endpoint the user fully trusts. <br>
Risk: Generated transcripts, translations, and summaries may contain recognition or summarization errors. <br>
Mitigation: Review the generated Markdown, bilingual text, and transcript JSON before relying on the notes for study, publication, or operational decisions. <br>


## Reference(s): <br>
- [SenseAudio Speech Recognition HTTP API](https://senseaudio.cn/docs/speech_recognition/http_api) <br>
- [Skill Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/KLilyZ/classroom-note-senseaudio-translator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, bilingual text, transcript JSON, and optional Notion or Obsidian exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; OPENAI_API_KEY, OPENAI_BASE_URL, NOTION_TOKEN, ffmpeg, Notion export, and Obsidian export are optional depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
