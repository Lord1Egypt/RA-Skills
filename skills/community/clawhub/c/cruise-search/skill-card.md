## Description:

全球邮轮航线实时搜索与智能推荐，接入途牛实时API，覆盖日韩、东南亚、地中海、加勒比海、长江三峡等航线，并支持按目的地、出发地、日期、价格筛选，查询产品详情、舱位房型、船舶信息和预订链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents, consumer travel assistants, and external users use this skill to search and compare cruise routes, retrieve cruise product details, inspect cabin and ship information, and open external Tuniu booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise search criteria, dates, departure cities, destination keywords, and product IDs are sent to the configured Tuniu proxy service.

Mitigation: Install only if this data sharing is acceptable, and avoid sending sensitive personal information in search queries.

Risk: Returned booking links lead to an external checkout flow where prices, availability, and terms may change.

Mitigation: Verify final prices, cancellation terms, booking notices, and payment conditions on Tuniu before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/travel-skills/skills/cruise-search)
- [Publisher Profile](https://clawhub.ai/user/travel-skills)
- [Tuniu Cruise Booking](https://m.tuniu.com/cruise/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown travel results or JSON records, depending on the selected output mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include prices, dates, product IDs, route details, cabin information, ship amenities, images, and external booking links.]

## Skill Version(s):

3.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
