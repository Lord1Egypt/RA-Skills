## Description:

B站短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了 B 站视频链接时使用，帮助基于输入材料生成评论情绪和讨论结构、观众画像和兴趣信号、内容与互动建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, brands, and ecommerce teams use this skill to analyze Bilibili video comments from a submitted video link or BV ID. It summarizes sentiment, discussion themes, audience signals, and practical content or engagement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can send the configured API key and submitted links to a base URL supplied through AISKILLS_BASE_URL.

Mitigation: Use the default HTTPS AI Skills endpoint unless the alternate destination is fully trusted, and keep the API key limited or revocable.

Risk: Submitted Bilibili links are sent for remote analysis.

Mitigation: Submit only links intended for remote analysis by the AI Skills service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/bilibili-sentiment-dashboard)
- [Form schema](references/form-schema.json)
- [Skill configuration](references/skill.json)
- [AI Skills service](https://ai-skills.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON task results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bilibili video link or BV ID and an AISKILLS_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
