## Description:

免费、免第三方 API Key 的闲鱼标题文案助手。用户有商品资料、图片或现有草稿，想生成更清楚的标题、描述、卖点和搜索词，并检查明显敏感或夸大表达时使用。它只输出文案和检查报告，不自动发布、不保证曝光或成交。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

闲鱼卖家可用真实商品资料生成多组标题、商品描述、卖点和搜索词，并检查明显夸大或敏感表达。资料不足时，助手会列出需要补充的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill benign with medium confidence because scripts/run.mjs was only partially inspected; the scan does not establish that the skill is risk-free.

Mitigation: Consider the unresolved inspection gap before installing and review scripts/run.mjs before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/easy-xianyu-title-copy-free)
- [闲鱼文案规则](references/文案规则.md)
- [Easy WebBridge source instructions](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR official download page](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [JSON or Markdown containing title variants, a product description, selling points, search terms, missing facts, flagged phrases, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 3–5 title variants based on supplied facts; unknown details remain marked for confirmation. Does not publish listings or guarantee exposure, sales, or platform review outcomes.]

## Skill Version(s):

1.1.1 (source: server-resolved release, manifest.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
