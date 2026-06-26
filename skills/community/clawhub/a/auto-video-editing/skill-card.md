## Description: <br>
Automates talk, vlog, and standup video editing by extracting audio, transcribing speech, splitting and merging sentence-level clips, adding subtitles, and generating covers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxazure](https://clawhub.ai/user/maxazure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn spoken videos into sentence-level clips, choose useful segments, burn subtitles, merge final videos, and add covers or chapter bars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local FFmpeg and Python processing creates generated files such as *_audio.wav, transcript JSON, clip directories, and final videos near the source media. <br>
Mitigation: Run the skill only on media you choose, preferably in a dedicated working directory where generated names will not overwrite files you need. <br>
Risk: Whisper models, Python packages, and fonts may be downloaded during setup or first use, including through configured mirrors. <br>
Mitigation: In restricted environments, preinstall and pin approved models, packages, and fonts, and disable or control mirror use according to local policy. <br>
Risk: Speech recognition, subtitle text, and generated cover or chapter titles can contain transcription or summarization mistakes. <br>
Mitigation: Review and correct the transcript JSON, subtitles, and final rendered video before publishing or relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxazure/auto-video-editing) <br>
- [Tsinghua PyPI mirror](https://pypi.tuna.tsinghua.edu.cn/simple) <br>
- [Hugging Face mirror](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands plus generated media files and transcript JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local FFmpeg and Python workflows that create audio, transcript, clip, subtitle, cover, chapter, and final video files near the input media.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
