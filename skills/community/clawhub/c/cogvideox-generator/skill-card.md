## Description: <br>
使用 CogVideoX (智谱AI) 模型根据文本提示词生成视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilaus](https://clawhub.ai/user/ilaus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate videos from text prompts with CogVideoX through ZhipuAI. It accepts prompt, quality, resolution, frame-rate, and audio options and returns generation status plus the resulting video URL when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to ZhipuAI using the user's API key. <br>
Mitigation: Avoid sensitive personal or business information in prompts and use a dedicated API key with quota controls. <br>
Risk: Video generation uses asynchronous polling and may keep running if a generation task appears stuck. <br>
Mitigation: Monitor long-running tasks and stop the run manually if generation does not complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [JSON-like dictionary with status, message, generated video URL, and raw result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPUAI_API_KEY and sends prompts to ZhipuAI for video generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
