## Description: <br>
自动化音视频字幕提取与翻译工具，利用 FFmpeg 和本地 Python 脚本生成双语 SRT。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongym1234](https://clawhub.ai/user/kongym1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert local audio or video into Chinese-English SRT subtitles through FFmpeg audio preparation, Groq Whisper transcription, and translation through a configured LLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media files are sent to Groq for transcription and transcript chunks are sent to the configured LLM provider for translation. <br>
Mitigation: Avoid sensitive or regulated recordings unless those providers' privacy and retention terms are acceptable. <br>
Risk: The workflow depends on API credentials and third-party Python dependencies. <br>
Mitigation: Keep API keys in environment variables and run the Python dependencies in an isolated environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, status text, and generated SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source and translated SRT files for a provided local media path; requires FFmpeg plus GROQ_API_KEY and LLM_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
