## Description: <br>
自动提取抖音分享文案中的视频链接，转录视频语音并结构化总结核心内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongym1234](https://clawhub.ai/user/kongym1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
用户将包含抖音短链接的分享文案交给 Agent，用于快速获取视频标题、语音转录文本和结构化内容摘要。需要完整内容时，Agent 可输出原始转录文本而不做总结。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin video or audio is downloaded locally and uploaded to SiliconFlow for transcription. <br>
Mitigation: Use the skill only for videos where local download and third-party transcription are acceptable, and avoid private, confidential, or sensitive content. <br>
Risk: The skill requires a sensitive SF_API_KEY credential. <br>
Mitigation: Store the API key in the configured environment file or environment variable, and do not place the key directly in prompts or shell commands. <br>
Risk: Temporary video files may remain if execution is interrupted before cleanup completes. <br>
Mitigation: Check and clear the temp_douyin directory after failures or interrupted runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongym1234/douyin2text) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary or plain transcript text, with shell commands used to run the extraction script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SF_API_KEY, network access, and temporary local video download before transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
