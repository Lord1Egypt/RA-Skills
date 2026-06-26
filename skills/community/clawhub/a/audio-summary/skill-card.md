## Description: <br>
Automatically extracts audio from video, transcribes it with qwen3-asr-flash, and saves segmented text summaries alongside the original file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanOO7](https://clawhub.ai/user/alanOO7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content workflows use this skill to turn local video or audio files into transcribed, segmented summaries. It is useful when an agent needs to prepare readable notes from short media files while preserving the summary next to the source file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded live-looking API key. <br>
Mitigation: Replace the embedded key with a scoped secret managed outside the skill before use. <br>
Risk: The skill sends media-derived audio content to Bailian/DashScope for transcription. <br>
Mitigation: Use only non-sensitive media that is appropriate to send to the external transcription service. <br>
Risk: The skill runs ffmpeg through a shell command that includes the user's file path. <br>
Mitigation: Run it only on trusted filenames, or update the implementation to invoke ffmpeg with subprocess arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alanOO7/audio-summary) <br>
- [Publisher profile](https://clawhub.ai/user/alanOO7) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text summary printed to stdout and saved as a .txt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ffmpeg to create temporary 16 kHz mono audio before transcription; summaries are saved beside the source media file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
