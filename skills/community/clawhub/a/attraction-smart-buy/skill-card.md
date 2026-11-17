## Description:

美团+途牛双平台景点门票实时比价，展示价差、可省金额和预订链接，帮你买到最低价门票；支持全国景点搜索含实景图片，含多票型引导提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-shopping users use this skill to search Chinese attractions, compare Meituan and Tuniu ticket prices, and get purchase guidance before booking.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Travel queries, city names, and the PROXY_TOKEN authentication value are sent to Tencent SCF proxy services for Meituan and Tuniu ticket lookup.

Mitigation: Install only if this data flow is acceptable, configure PROXY_TOKEN as an environment variable, and avoid adding personal details beyond the travel query.

Risk: External ticket prices, availability, images, and booking links may be incomplete, stale, or mismatched.

Mitigation: Review returned platform names, match warnings, and booking pages before relying on a purchase recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/attraction-smart-buy)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Tencent SCF proxy service for Tuniu ticket lookup](https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com)
- [Tencent SCF proxy service for Meituan ticket lookup](https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown/text response with attraction lists, ticket price comparisons, booking links, and purchase advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-time prices, images, platform match warnings, savings estimates, and recommended ticket types.]

## Skill Version(s):

3.3.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
