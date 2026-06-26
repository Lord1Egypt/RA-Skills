## Description: <br>
Download audio from Bilibili or b23.tv links and transcribe it into txt, srt, and segment JSON with yt-dlp, ffmpeg, and faster-whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yizh4ng](https://clawhub.ai/user/yizh4ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn Bilibili or b23.tv video links into local transcript text, subtitles, and segment metadata, especially for Chinese-language speech-to-text workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads media and writes local audio and transcript files that may contain user-provided or sensitive content. <br>
Mitigation: Use a virtual environment, process only links the user is allowed to download, and delete downloaded audio and transcript files when they are no longer needed. <br>
Risk: Transcription quality can vary with language, model size, VAD behavior, and long CPU-bound runs. <br>
Mitigation: Review generated transcript files before relying on them; rerun with automatic language detection, a larger model, or adjusted VAD settings when quality is weak. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated .txt, .srt, and .segments.json transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcript artifacts and progress messages; downloaded audio and transcripts remain on disk until removed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
