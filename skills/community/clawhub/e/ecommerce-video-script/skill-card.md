## Description:

当用户需要根据商品信息撰写带货短视频、商品演示或种草口播脚本时使用。提供商品链接或商品资料，输出分镜、口播、演示动作与行动引导；可按需参考同类商品。在线商品能力支持抖音与小红书，已有资料可直接写作。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和电商运营者可根据用户提供的商品资料，或抖音与小红书支持的商品信息，生成可拍摄的带货短视频脚本，包括分镜、口播、演示动作和行动引导。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses an unpinned, automatically accepted latest CLI version, which may handle credentials.

Mitigation: Pin the CLI to a reviewed release before installation or use.

Risk: Online lookups send product details or search terms to SocialDataX.

Mitigation: Use online lookups only when you are comfortable sharing those details or terms with SocialDataX.

Risk: The security scan inspected only the Markdown component and reported unresolved local references, so its coverage is incomplete.

Mitigation: Review the unresolved references and scan the complete release before relying on the security assessment.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/devinchen2014/skills/ecommerce-video-script)
- [SocialDataX API information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a script table, source notes, and items to verify]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aligns scene, narration, on-screen text, and actions; identifies missing facts and items requiring verification.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
