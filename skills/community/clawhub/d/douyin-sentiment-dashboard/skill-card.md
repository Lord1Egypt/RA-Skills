## Description: <br>
抖音短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了抖音内容链接时使用，帮助基于输入材料生成情绪和舆情判断、用户画像和意图信号、运营建议和回复建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations teams, brands, and e-commerce teams use this skill to analyze Douyin video comments from a supplied link. It returns sentiment and public-opinion signals, audience and intent insights, operational recommendations, and reply suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Douyin links and resulting analysis requests to an external AI Skills API under the user's API key. <br>
Mitigation: Use explicit invocation for specific Douyin analysis tasks, keep the API key in environment variables or a secret manager, and confirm the service data terms before submitting private or regulated business material. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/allinherog-star/douyin-sentiment-dashboard) <br>
- [form-schema.json](references/form-schema.json) <br>
- [skill.json](references/skill.json) <br>
- [AI Skills](https://ai-skills.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, analysis, guidance] <br>
**Output Format:** [JSON response containing comment-analysis task status, sentiment insights, user intent signals, operational advice, and labeled comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY and sends Douyin links and analysis requests to ai-skills.ai.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
