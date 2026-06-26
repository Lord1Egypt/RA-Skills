## Description: <br>
Audio Tools helps an agent extract WAV audio from video, clip audio segments, play local media, transcribe speech with Whisper, and inspect audio or video metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[risehorizon](https://clawhub.ai/user/risehorizon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local audio and video processing workflows, including extraction, clipping, playback, transcription, and metadata inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages at runtime, including unpinned dependencies. <br>
Mitigation: Run it in a controlled virtual environment and preinstall approved versions of ffmpeg, moviepy, and Whisper before use. <br>
Risk: Metadata extraction is flagged for unsafe dynamic evaluation on media metadata. <br>
Mitigation: Avoid untrusted media files for metadata extraction until the unsafe evaluation behavior is removed or reviewed. <br>
Risk: The skill can write output files, launch a system media player, and generate transcripts that may contain sensitive content. <br>
Mitigation: Choose output paths deliberately, review generated transcript and metadata files before sharing them, and use local media only from trusted sources. <br>


## Reference(s): <br>
- [Audio Tools usage guide](references/usage.md) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated WAV, JSON, and TXT files from the tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription output may include timestamps, confidence values, and plain text; metadata output may be printed or saved as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
