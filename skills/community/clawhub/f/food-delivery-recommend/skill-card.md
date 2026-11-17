## Description:

外卖推荐帮助用户按当前位置、时段、堂食可用性、营业状态、评分、距离和预算筛选附近外卖商家，并输出结构化推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiezhenlin-tom](https://clawhub.ai/user/xiezhenlin-tom)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for nearby food-delivery recommendations that consider location, time of day, dining-in availability, ratings, price, delivery time, and business status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save precise addresses, dietary preferences, budget, and order history in persistent local memory without clear consent.

Mitigation: Review before installing; ask for consent before saving preferences, prefer coarse location aliases, and avoid storing sensitive dietary or order-history details unless the user explicitly agrees.

Risk: Food-delivery recommendations can rely on public platform data that may be incomplete, stale, or missing current business status.

Mitigation: Prompt users to confirm current availability, business status, delivery time, and final price in the delivery app before ordering.

## Reference(s):

- [Ranking Criteria](references/ranking_criteria.md)
- [Search Templates](references/search_templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendation list with ranked merchant summaries and follow-up prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include location, budget, cuisine, time-of-day, weather, platform coverage, and business-status notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
