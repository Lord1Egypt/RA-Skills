## Description: <br>
1688 分销选品助手 - 提供关键词选品、图搜选品等核心选品能力，以及分销参谋查询、推荐决策分析等深度评估功能。当用户需要搜索货源、以图搜货、筛选包邮/一件代发商品、分析商品分销价值或评估铺货风险时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and agents use this skill to search 1688 distribution products by keyword or image, screen candidates for fulfillment and channel fit, and generate recommendation and risk summaries before choosing products to distribute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires and stores sensitive AK and ISV token credentials. <br>
Mitigation: Use only trusted releases, keep credentials private, rotate credentials if exposed, and remove cached tokens when no longer needed. <br>
Risk: Authenticated API traffic may be exposed to higher transport risk because security evidence reports disabled HTTPS certificate checks. <br>
Mitigation: Prefer a release with normal HTTPS certificate verification before using real business credentials or production accounts. <br>
Risk: Product recommendations and risk summaries depend on authenticated 1688 API responses and may be incomplete when credentials, permissions, or service availability are limited. <br>
Mitigation: Review candidate products and recommendation reasons manually before acting on distribution decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-distribution-product-selection-newton) <br>
- [Product Selection Reference](scripts/biz/product_selection/reference.md) <br>
- [Offer Info Reference](scripts/capabilities/offer_info/reference.md) <br>
- [ClawHub AK Portal](https://clawhub.1688.com) <br>
- [1688 AI Workbench](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown with shell command snippets and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an ALI_1688_AK credential; authenticated API results depend on 1688 service availability and account permissions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
