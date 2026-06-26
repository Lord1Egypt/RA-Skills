## Description: <br>
Generate or align SRT subtitles from audio using this repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sariel2018](https://clawhub.ai/user/sariel2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to generate SRT subtitles from audio, align a reference transcript to audio timing, run timing quality checks, and create subtitle preview videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can change the local Python environment. <br>
Mitigation: Install in a dedicated virtual environment and review the pinned faster-whisper dependency before running pip install. <br>
Risk: Preview rendering depends on the ffmpeg executable found in PATH. <br>
Mitigation: Use a trusted ffmpeg binary and provide only intended audio, SRT, and output paths. <br>
Risk: Automatic transcription may require model files at runtime. <br>
Mitigation: Provide a trusted local model path when avoiding runtime model retrieval is required. <br>


## Reference(s): <br>
- [Command Templates](references/command-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sariel2018/audio-srt-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated SRT or MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local subtitle, timing report, and optional preview-video artifacts when the packaged scripts are run.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
