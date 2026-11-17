## Description:

电商全链路 AI Agent 技能库：跨境扩张策略（市场评分/税务合规/物流/支付本地化）、Stripe 支付集成（订阅/发票/风控/对账）、Shopify 产品管理（GraphQL/CSV 批量）、电商前端搭建（组件/SEO/移动适配）、淘宝/闲鱼运营（商品发布内容包/交易对账/评价维护/选品定价复盘）。当用户要做跨境电商选品与落地、接入 Stripe 订阅与催款、批量管理 Shopify 商品、运营淘宝或闲鱼店铺、或搭建高转化电商前端时调用本技能，并据路由表进入对应子技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small ecommerce sellers use this skill library to plan cross-border expansion, integrate payments, build storefronts, manage Shopify catalogs, and operate Taobao or Xianyu shops. The main skill routes each request to a focused playbook, sub-skill, or product-feed validator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order recording through hope-server and related integration helpers is unverified, and bulk store changes have weak safeguards.

Mitigation: Remove the recording path or verify its owner, destination, stored fields, and retention before authorizing it. Use limited credentials, review affected products, and keep a recovery export before bulk changes.

## Reference(s):

- [Cross-border compliance playbook](references/cross-border-compliance.md)
- [Payment integration checklist](references/payment-integration-checklist.md)
- [Storefront launch playbook](references/storefront-launch-playbook.md)
- [Taobao Open Platform trade API](https://open.taobao.com/api.htm?spm=a219a.7386797.0.0&docType=2&docId=1049)
- [Taobao Open Platform review API](https://open.taobao.com/api.htm?spm=a219a.7386797.0.0&docType=2&docId=826)
- [ClawHub release page](https://clawhub.ai/skills-repo/skills/ecommerce-master)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with tables, checklists, code snippets, and structured product-feed validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected ecommerce task and sub-skill.]

## Skill Version(s):

1.0.0 (source: target metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
