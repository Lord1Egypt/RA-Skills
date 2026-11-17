## Description:

Helps agents answer Chinese-language questions about buying, comparing, recommending, and evaluating new or used new energy vehicles, including pricing, ownership costs, depreciation, insurance, financing, and Wuxi-specific considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangmengyang](https://clawhub.ai/user/zhangmengyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure practical car-buying advice for China's new energy vehicle market, especially for Wuxi users comparing models, prices, running costs, policy effects, financing, and used-car risks.

### Deployment Geography for Use:

China, with Wuxi-specific local guidance

## Known Risks and Mitigations:

Risk: Stored car preferences may be reused automatically, including budget, location, commute, parking, charging access, or prior deal-breakers.

Mitigation: Confirm current budget, city, commute, charging access, powertrain preference, and deal-breakers with the user before applying remembered details.

Risk: Vehicle pricing, incentives, insurance costs, reviews, and local policy details can become stale quickly.

Mitigation: Use current sources for pricing, reviews, and policy-sensitive claims, and label estimates clearly when real-time data is unavailable.

## Reference(s):

- [Buying Guide](artifact/references/buying-guide.md)
- [Cost Calculation](artifact/references/cost-calculation.md)
- [Pitfalls Guide](artifact/references/pitfalls.md)
- [Wuxi New Energy Vehicle Policy](artifact/references/wuxi-policy.md)
- [Brand Scores](artifact/data/brand-scores.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with comparison tables, bullet lists, estimates, and sourced claims]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should confirm core requirements before recommending vehicles and should use current search results for prices, reviews, and policy-sensitive claims.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
