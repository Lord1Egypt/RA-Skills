## Description: <br>
智能音频降噪服务，基于阿里巴巴通义实验室 AI 算法，一键消除背景噪音，还原纯净人声。支持 wav、mp3、aac 等主流格式，适用于录音降噪、语音识别预处理、播客后期制作、会议录音优化等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songguocola](https://clawhub.ai/user/songguocola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audio workflow users use this skill to denoise recorded speech, prepare audio for ASR, and improve podcasts, meetings, interviews, online education recordings, and audiobook production through Alibaba DashScope audio processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected recordings are processed through Alibaba DashScope and may contain sensitive, regulated, or confidential speech. <br>
Mitigation: Use only approved recordings, review the provider privacy and retention terms before use, and avoid sensitive content unless authorized. <br>
Risk: The skill requires a DashScope API key for authentication. <br>
Mitigation: Store the API key in a protected environment variable and run the skill only in a trusted Python environment. <br>


## Reference(s): <br>
- [fun-denoise ClawHub page](https://clawhub.ai/songguocola/fun-denoise) <br>
- [Denoise.py source reference](audio_process/Denoise.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; runtime output is denoised audio files plus JSON-like processing metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key and sends selected audio to Alibaba DashScope for cloud processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
