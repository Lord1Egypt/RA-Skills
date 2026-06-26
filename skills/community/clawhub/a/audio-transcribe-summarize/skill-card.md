## Description: <br>
Transcribe audio/video files to text and generate structured summaries using SenseAudio ASR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q1lin570](https://clawhub.ai/user/q1lin570) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to transcribe user-selected recordings, meetings, lectures, podcasts, interviews, or video files with SenseAudio and then turn the transcript into structured notes, key points, action items, quotes, and a full transcript section. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio or video is uploaded to SenseAudio for transcription. <br>
Mitigation: Use the skill only for recordings approved for that provider, and avoid confidential or regulated content unless organizational policy allows it. <br>
Risk: The skill requires a SenseAudio API key. <br>
Mitigation: Use a revocable API key stored in the SENSEAUDIO_API_KEY environment variable and rotate it if exposure is suspected. <br>
Risk: Transcript text and raw JSON files are written locally next to the source file or selected output path. <br>
Mitigation: Choose output locations deliberately and clean up local transcript artifacts when they contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q1lin570/audio-transcribe-summarize) <br>
- [SenseASR API reference](artifact/api-reference.md) <br>
- [SenseAudio API keys](https://senseaudio.cn/platform/api-key) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the helper script writes transcript text and raw JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports model selection, language hints, speaker diarization, timestamps, sentiment, translation, hotwords, output path, and response format options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
