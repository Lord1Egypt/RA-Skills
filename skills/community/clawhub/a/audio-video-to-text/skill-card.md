## Description: <br>
Audio Video To Text transcribes audio and video files with Whisper and can produce plain text, SRT/VTT subtitles, or JSON for meeting notes, subtitles, interviews, and podcasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan830826](https://clawhub.ai/user/ivan830826) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to turn local audio or video files into transcripts, subtitle files, or structured JSON for meetings, interviews, podcasts, and video captioning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing confidential or unauthorized recordings can expose sensitive speech in local transcript files and temporary extracted audio. <br>
Mitigation: Process only recordings the user is authorized to transcribe, store outputs in approved locations, and delete generated transcripts or temporary audio when no longer needed. <br>
Risk: Concurrent video transcriptions can collide because the script uses a shared temporary audio filename. <br>
Mitigation: Run video transcriptions one at a time or update the temporary audio path to a unique per-run filename before batch or parallel use. <br>
Risk: Installing or running transcription dependencies from untrusted sources can introduce supply-chain or execution risk. <br>
Mitigation: Install dependencies from trusted package sources, avoid elevated privileges, and review the script before deployment. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) <br>
- [ISO 639-1 Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) <br>
- [ClawHub Skill Page](https://clawhub.ai/ivan830826/audio-video-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated transcript files in TXT, SRT, VTT, or JSON formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output content depends on the selected Whisper model, input media quality, language option, output format, and CPU or CUDA device choice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
