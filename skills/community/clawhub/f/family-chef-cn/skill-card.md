## Description:

为家庭规划一周菜单、搜索菜谱、计算营养、估算预算并生成购物清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[villadora](https://clawhub.ai/user/villadora)

### License/Terms of Use:

MIT-0

## Use Case:

External household users use this skill to plan Chinese-family weekly meals, find recipes and prices, estimate nutrition, and generate shopping lists based on household size, budget, city, preferences, and dietary restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household food-planning details, budget, city, and dietary restrictions are saved in a local plaintext profile file.

Mitigation: Tell users where the profile is stored, avoid collecting unnecessary sensitive details, and offer deletion guidance for ~/.family-chef-profile.json.

Risk: Recipe and price searches may expose search terms and city to a search provider.

Mitigation: Make web-search use clear before lookups and avoid including unnecessary personal details in search queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/villadora/skills/family-chef-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or conversational text with optional structured lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meal plans, recipes, nutrition estimates, budget estimates, and shopping lists.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
