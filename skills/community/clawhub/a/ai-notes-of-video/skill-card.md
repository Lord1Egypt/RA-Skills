## Description: <br>
Generates document, outline, and image-text AI notes from a user-provided video URL using Baidu video analysis and note extraction APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiduQianfanGroup](https://clawhub.ai/user/baiduQianfanGroup) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to submit a video URL to Baidu, create an AI-notes task, and poll for generated document, outline, and image-text notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided video URLs to Baidu for note generation. <br>
Mitigation: Use it only when the user is authorized to share the video URL with Baidu, and avoid private, internal, signed, authenticated, or sensitive URLs. <br>
Risk: The skill requires a Baidu API key and may consume quota or incur service costs. <br>
Mitigation: Use a scoped BAIDU_API_KEY where possible and monitor quota and billing during use. <br>


## Reference(s): <br>
- [AI Notes of Video ClawHub release](https://clawhub.ai/baiduQianfanGroup/ai-notes-of-video) <br>
- [baiduQianfanGroup publisher profile](https://clawhub.ai/user/baiduQianfanGroup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON task responses containing generated note content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and a user-provided video URL; task completion is checked by task_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
