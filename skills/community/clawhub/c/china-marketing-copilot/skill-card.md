## Description:

中国3C营销助手帮助中国消费电子营销团队完成新品上市策略、信息架构、创意策划、KOL渠道计划、竞品洞察、负面预警、上线判断和复盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[killsnake01](https://clawhub.ai/user/killsnake01)

### License/Terms of Use:

MIT

## Use Case:

Marketing, product, social media, KOL/channel, and startup teams use this skill to plan China-market consumer-electronics launches, review claims and creative assets, analyze competitors and comments, and decide whether to continue, adjust, or pause campaign activity.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Marketing strategy or launch guidance may rely on stale offline data for prices, rankings, product specs, KOL status, or platform trends.

Mitigation: Verify high-timeliness claims against current sources before real campaign use and label unverified claims as pending verification.

Risk: Imported comments, briefs, or campaign data may contain confidential business information.

Mitigation: Use only data intended for analysis and redact sensitive fields before providing comment exports or internal materials.

Risk: Launch, pause, compliance, or safety recommendations could be mistaken for final approval.

Mitigation: Treat outputs as marketing decision support and route final materials through legal, advertising compliance, and product safety review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killsnake01/skills/china-marketing-copilot)
- [Skill instructions](SKILL.md)
- [Agent router](docs/agent-router.md)
- [Data index and freshness rules](docs/data-index.md)
- [2026 market signal library](docs/ecosystem/market-signals-2026.md)
- [Negative early-warning library](docs/ecosystem/negative-early-warning.md)
- [Industry ecosystem framework](docs/references/industry-ecosystem.md)
- [Market signal source: Campaign Asia](https://www.campaignasia.com/article/xiaomi-sacks-staff-and-penalises-executives-after-a-kol-tie-up-triggers-fan-backl/506868)
- [Market signal source: People's Daily Online](https://finance.people.com.cn/n1/2026/0105/c1004-40638996.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown responses, structured decision JSON when requested, and optional shell commands for bundled validation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled offline docs first; Python scripts can process user-provided comment batches or validate structured decision outputs when available.]

## Skill Version(s):

1.4.33 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
