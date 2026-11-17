## Description:

美团优惠券，搜索连锁品牌全国通用优惠券。输入品牌名或品类关键词，返回覆盖50+城市的全国通用券，按销量排序。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search for nationwide brand coupons by brand name or category keyword, including food, beverage, retail, automotive service, and other consumer discounts. The agent returns sorted coupon options, purchase links, and image-backed Markdown results.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill sends coupon search terms to a remote Tencent Cloud Function.

Mitigation: Document the network behavior before installation and restrict use to intended coupon searches.

Risk: The artifact includes a reusable proxy token.

Mitigation: Rotate or remove the exposed token and replace it with a deployment-specific secret before release.

Risk: Remote coupon data is rendered into images and purchase links.

Mitigation: Validate or escape remote coupon fields before rendering and review links before user-facing deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/brand-coupons)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown text with coupon entries, remote images, purchase links, and pagination hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are filtered for nationally available coupons and sorted by reported sales volume.]

## Skill Version(s):

1.0.2 (source: server release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
