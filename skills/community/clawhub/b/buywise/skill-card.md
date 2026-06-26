## Description: <br>
BuyWise helps shoppers decide whether, where, and when to buy products by comparing prices, checking discount authenticity, summarizing reviews, recommending alternatives, and producing a Buy/Wait/Skip recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping-assistant agents use BuyWise to research products before purchase, compare prices across global and Chinese marketplaces, evaluate reviews and discount history, and decide whether to buy now, wait, or skip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names, links, and shopping intent may be sent to public shopping, search, or review sites during research. <br>
Mitigation: Avoid using sensitive product links or private purchase details, and review the public sites the agent plans to query before proceeding. <br>
Risk: Prices, availability, discounts, and reviews can change quickly or be incomplete across marketplaces. <br>
Mitigation: Verify final price, shipping, seller reputation, and return terms on the retailer site before purchasing. <br>
Risk: The skill may suggest a CouponClaw coupon lookup after a purchase decision. <br>
Mitigation: Require explicit user approval before running any separate CouponClaw step or additional coupon/cashback workflow. <br>


## Reference(s): <br>
- [BuyWise on ClawHub](https://clawhub.ai/jiajiaoy/buywise) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [CamelCamelCamel](https://camelcamelcamel.com) <br>
- [smzdm](https://search.smzdm.com) <br>
- [Google Shopping](https://www.google.com/search?tbm=shop) <br>
- [Bing Shopping](https://www.bing.com/shop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown shopping report with comparison tables, concise evidence summaries, command suggestions, and a Buy/Wait/Skip verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese or English output; prices and recommendations depend on public web data available at run time.] <br>

## Skill Version(s): <br>
1.5.5 (source: package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
