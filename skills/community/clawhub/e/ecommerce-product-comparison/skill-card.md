## Description:

当用户需要对比已选商品、比较规格和卖点差异，或准备竞品对照表时使用。输入 2–5 个商品链接或商品资料，输出注明价格口径、信息缺口和来源的商品差异表。在线商品能力支持抖音与小红书，其他平台可基于用户提供的资料分析。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can compare 2–5 selected products using supplied product details or supported Douyin and Xiaohongshu listings. The skill prepares a sourced comparison table that highlights price basis, specification and selling-point differences, missing information, and suitable use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online lookups use a changeable, unpinned CLI package that may access credentials and product links or IDs; the security evidence reports no established intentional malicious behavior.

Mitigation: Use the CLI and SocialDataX only if trusted, and limit credential access to the execution environment that needs it.

Risk: Security scan coverage was partial because two referenced paths could not be resolved.

Mitigation: Treat the scan as incomplete and review the unresolved referenced files before deployment.

## Reference(s):

- [商品竞品对比 on ClawHub](https://clawhub.ai/devinchen2014/skills/ecommerce-product-comparison)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison table with source details and notes on missing information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares only user-selected products; records price conditions and data gaps, and avoids unsupported rankings.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
