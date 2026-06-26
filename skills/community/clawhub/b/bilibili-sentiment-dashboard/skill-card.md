## Description: <br>
B站短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了 B 站视频链接时使用，帮助基于输入材料生成评论情绪和讨论结构、观众画像和兴趣信号、内容与互动建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, operators, brand teams, and ecommerce teams use this skill to analyze Bilibili video comments from a provided video link and turn sentiment, discussion structure, audience signals, and interest signals into content and interaction recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive AI Skills API key. <br>
Mitigation: Use a service-specific API key, provide it through the environment, and rotate or revoke it if exposure is suspected. <br>
Risk: The skill sends the Bilibili link, parsed video metadata, and analysis task data to the configured AI Skills service. <br>
Mitigation: Avoid submitting private or internal links and confirm the configured service endpoint before use. <br>
Risk: Generated sentiment and operations guidance can be incomplete or misleading if source comments are sparse, biased, or unavailable. <br>
Mitigation: Review the returned analysis before using it for publishing, moderation, brand, or ecommerce decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/bilibili-sentiment-dashboard) <br>
- [Form schema](artifact/references/form-schema.json) <br>
- [Skill metadata](artifact/references/skill.json) <br>
- [AI Skills quick start](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance] <br>
**Output Format:** [JSON containing task status, comment-analysis summary, sentiment labels, audience signals, labeled comments, and operation advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AI Skills API key and sends the provided Bilibili link plus parsed video metadata to the configured AI Skills service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
