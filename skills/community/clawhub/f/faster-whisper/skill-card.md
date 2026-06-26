## Description: <br>
Local speech-to-text using faster-whisper. 4-6x faster than OpenAI Whisper with identical accuracy; GPU acceleration enables ~20x realtime transcription. SRT/VTT/TTML/CSV subtitles, speaker diarization, URL/YouTube input, batch processing with ETA, transcript search, chapter detection, per-file language map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThePlasmak](https://clawhub.ai/user/ThePlasmak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to transcribe local audio or video, generate subtitle files, search transcripts, translate speech to English, and process batches of recordings without relying on a hosted transcription API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL and RSS inputs can download remote media through yt-dlp. <br>
Mitigation: Use URL or RSS transcription only for media the user intends to fetch, and verify optional download tooling before running the command. <br>
Risk: Optional Hugging Face tokens may be used for private or gated models and diarization. <br>
Mitigation: Prefer cached tokens and avoid pasting tokens into shared logs, transcripts, or command histories. <br>
Risk: Transcript outputs can overwrite files, and generated HTML reports from untrusted audio or filenames carry the HTML escaping concern noted by the security evidence. <br>
Mitigation: Choose output paths carefully and avoid opening HTML transcript reports generated from untrusted inputs until the escaping issue is fixed. <br>


## Reference(s): <br>
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper) <br>
- [Distil-Whisper Paper](https://arxiv.org/abs/2311.00430) <br>
- [Hugging Face faster-whisper Models](https://huggingface.co/collections/Systran/faster-whisper) <br>
- [pyannote.audio](https://github.com/pyannote/pyannote-audio) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file path summaries, and concise transcript or result text when appropriate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can direct an agent to create transcript, subtitle, CSV, JSON, HTML, speaker-audio, chapter, and stats files; long structured outputs should be written to files and summarized for the user.] <br>

## Skill Version(s): <br>
1.5.1 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
