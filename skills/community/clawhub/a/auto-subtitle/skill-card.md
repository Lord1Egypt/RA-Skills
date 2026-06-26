## Description: <br>
Auto Subtitle batch-generates SRT or VTT subtitle files for videos by extracting audio and transcribing or translating it with OpenAI Whisper, with preview and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and localization teams use this skill to generate or translate subtitles for batches of local video files. It is suited for workflows that need SRT or VTT output, configurable language settings, preview mode, and recovery from overwritten subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video audio is sent to OpenAI for transcription or translation and may consume OpenAI API quota. <br>
Mitigation: Use the skill only with videos approved for OpenAI processing and verify API cost expectations before batch runs. <br>
Risk: Existing subtitle files may be overwritten during generation. <br>
Mitigation: Run preview mode first and rely on the generated backup and undo workflow before processing intended folders. <br>
Risk: Recursive processing can affect more videos than intended. <br>
Mitigation: Scope the directory and extension filters carefully before enabling recursive processing. <br>


## Reference(s): <br>
- [Auto Subtitle ClawHub release](https://clawhub.ai/utopiabenben/auto-subtitle) <br>
- [utopiabenben publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [SRT or VTT subtitle files, terminal status text, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local subtitle files, backup directories, and an operation log; requires OPENAI_API_KEY and ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill.json, and source/auto_subtitle.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
