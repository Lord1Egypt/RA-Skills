## Description: <br>
使用百音开放平台创建 AI 语音任务，支持文本转语音、音色克隆，并在同一 skill 内继续查询任务状态和结果链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Baiyin voice-generation tasks from text, clone or choose voice characteristics, check task progress, and retrieve generated audio links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a silent pre-task self-update or version-check step that can change the installed skill without clear user approval. <br>
Mitigation: Review before installing and require explicit user approval before any skill update is applied. <br>
Risk: The skill uses a sensitive Baiyin API key and may upload or submit voice samples to Baiyin services. <br>
Mitigation: Use a revocable API key and only upload voice samples that the user has permission to send to Baiyin and expose through returned URLs. <br>


## Reference(s): <br>
- [Baiyin Open Platform API Base](https://ai.hikoon.com) <br>
- [ClawHub release page](https://clawhub.ai/jiuping520/baiyin-voice-generate-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown with API request parameters and task-status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and may return task status or generated audio URLs from the Baiyin API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
