## Description:

Use this skill when the user asks for AI试鞋、鞋履上脚、虚拟试穿、鞋子商品图、穿搭预览，或要为电商、广告、营销、短剧、漫剧、带货与种草内容完成AI鞋履试穿效果图。它服务鞋履品牌、跨境卖家、买手和种草内容团队：接收鞋履多角度图、授权人物或腿脚参考、场景、姿势和平台，交付鞋履上脚预览、不同裤装与场景版本、细节检查。特色是保持鞋型、鞋底、材质和Logo，改变穿搭场景；需要生成素材时通过AI-HIVE OpenAPI完成配置查询、参考素材上传、价格快照、COST_FIRST/SPEED_FIRST/SUCCESS_FIRST路由、异步轮询和下载。不要把本Skill用于未授权复刻、虚假商品声明、伪造用户证言或规避平台规则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External footwear brands, cross-border sellers, buyers, and content teams use this skill to plan and produce AI-assisted footwear try-on previews for ecommerce, advertising, marketing, livestream commerce, and social content. It helps structure briefs, prompts, reference-image strategy, AI-HIVE generation commands, task records, and acceptance checks while requiring authorization and factual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or misused if entered into an untrusted endpoint or reused broadly.

Mitigation: Use a dedicated AI-HIVE key, keep the default trusted endpoint unless the alternate endpoint is fully trusted, and rotate any key previously used with an untrusted base URL.

Risk: Generated media downloads may write files into user-controlled output locations.

Mitigation: Use a disposable output directory for generated downloads and review files before moving them into long-lived project folders.

Risk: Generation calls may incur cost or produce misleading commercial claims.

Mitigation: Confirm billable parameters before execution and require human review for product facts, authorizations, platform claims, and generated try-on realism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/footwear-tryon-preview-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit billable AI-HIVE generation tasks after user confirmation and may download generated media files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
