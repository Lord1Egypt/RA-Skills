## Description: <br>
Douyin video transcription suite. Extract audio from Douyin/TikTok China videos, transcribe with Whisper, and analyze content. Supports video links, local files, and image notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content analysts use this skill to transcribe Douyin or TikTok China videos, local media files, and image-note pages into structured summaries, transcripts, key points, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download video or audio content, write local media and transcript files, and run ffmpeg or ffprobe. <br>
Mitigation: Review target URLs and file paths before execution, use a controlled working directory, and inspect generated transcripts before relying on them. <br>
Risk: The skill can automatically start or create a persistent Docker Whisper service. <br>
Mitigation: Pre-provision and pin the Whisper container image when possible, and stop or remove the whisper-asr container when transcription work is complete. <br>
Risk: Configured cloud ASR paths may send audio outside the local machine. <br>
Mitigation: Use local Whisper by default and configure cloud ASR API keys only when external audio processing is intended and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/don068589/douyin-video-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown transcript with summaries, key points, tags, and optional command-line transcription output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audio, video, and transcript files and may return structured transcription result objects from helper scripts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
