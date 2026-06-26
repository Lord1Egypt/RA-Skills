## Description: <br>
Extracts and transcribes speech from Douyin video links or local audio and video files into Chinese text and readable Markdown transcripts using local Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuzheng60](https://clawhub.ai/user/liuzheng60) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn authorized Douyin videos or local media files into Chinese transcripts for review, note-taking, or downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Douyin and downloads videos for shared links. <br>
Mitigation: Use it only for content you are authorized to access and review whether the workflow is appropriate for the platform terms and your use case. <br>
Risk: Full transcripts can be saved to files and printed in tool logs. <br>
Mitigation: Avoid confidential media unless the output directory and logs are acceptable storage locations, and remove transcript artifacts when they are no longer needed. <br>
Risk: First-time setup installs a local Python environment, Chromium, and Whisper dependencies. <br>
Mitigation: Run setup in an isolated environment with sufficient disk space and review dependency installation before deploying it on managed systems. <br>
Risk: Automatic speech recognition may mishear names, technical terms, or mixed-language content. <br>
Mitigation: Review and correct transcripts before relying on them for publication, compliance, or decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuzheng60/douyin-transcribe-lz) <br>
- [Whisper usage reference](references/whisper_usage.md) <br>
- [Whisper medium model download](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcripts, raw text transcripts, JSON transcription metadata, and setup or execution commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save downloaded Douyin video files, raw Whisper transcript text, Whisper JSON, and cleaned Markdown in the selected output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
