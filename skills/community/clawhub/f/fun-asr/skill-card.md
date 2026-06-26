## Description: <br>
阿里云百炼 FunASR 录音文件识别，使用阿里云 DashScope API 进行语音转文字。当用户需要转录音频文件时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhendong](https://clawhub.ai/user/pengzhendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to transcribe supported audio files into text through Alibaba Cloud DashScope FunASR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files are processed by Alibaba Cloud DashScope, which may expose sensitive recordings to a third-party service. <br>
Mitigation: Use the skill only for recordings you are authorized to process with DashScope, and avoid sensitive audio unless the provider is approved for that data. <br>
Risk: The skill requires a DashScope API key in the execution environment. <br>
Mitigation: Use a dedicated API key, keep it out of shared logs and prompts, and run the Python dependencies in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengzhendong/fun-asr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DASHSCOPE_API_KEY and sends selected audio files to Alibaba Cloud DashScope for recognition.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
