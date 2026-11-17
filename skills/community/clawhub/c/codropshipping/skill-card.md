## Description:

帮助在CoDropshipping平台查询商品信息、库存、价格、规格等，自动抓取搜索结果并以表格形式展示

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwooaa](https://clawhub.ai/user/dwooaa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sourcing operators use this skill to search CoDropshipping for product information and receive the results as a concise Markdown table. It is intended for routine product lookup workflows where sending the search terms to CoDropshipping is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search terms are sent to CoDropshipping through browser automation.

Mitigation: Use the skill only when disclosure of those sourcing terms to CoDropshipping is acceptable, and avoid confidential search terms.

Risk: Browser automation may fail or return incomplete results when pages fail to load, searches have no matches, or anti-automation controls appear.

Mitigation: Treat returned product data as lookup assistance and retry later or change keywords when the skill reports loading, no-result, or anti-automation issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwooaa/skills/codropshipping)
- [Publisher profile](https://clawhub.ai/user/dwooaa)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns product names, prices, monthly sales, and ratings when available.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
