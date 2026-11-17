## Description:

抖音短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了抖音内容链接时使用，帮助基于输入材料生成情绪和舆情判断、用户画像和意图信号、运营建议和回复建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, brands, and e-commerce teams use this skill to analyze Douyin video comments and turn audience feedback into sentiment judgments, user intent signals, operations recommendations, and reply suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the API key and submitted Douyin content link to the configured AI Skills service endpoint.

Mitigation: Keep AISKILLS_BASE_URL at the trusted default or another verified HTTPS host, protect AISKILLS_API_KEY, and avoid submitting private or sensitive links unless external processing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/douyin-sentiment-dashboard)
- [form-schema.json](references/form-schema.json)
- [skill.json](references/skill.json)
- [AI Skills service](https://ai-skills.ai)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON response containing task status, comment analysis, sentiment signals, user insights, and operations advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Douyin video link or video ID and an AISKILLS_API_KEY before execution.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
