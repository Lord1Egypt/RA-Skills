## Description: <br>
Use this skill when the user asks about buying, comparing, recommending, or evaluating new or used new energy vehicles, including BEV, PHEV, and EREV models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangmengyang](https://clawhub.ai/user/zhangmengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare new energy vehicles, estimate purchase and running costs, assess used-vehicle risks, and get Wuxi-oriented buying guidance. It supports budget, powertrain, usage, resale, insurance, financing, and policy questions with current market search when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle pricing, discounts, used-car listings, and local policy details can change quickly, which may make buying guidance or cost estimates stale. <br>
Mitigation: Use current web search for market-sensitive claims, label sources, and mark estimates clearly when search is unavailable. <br>
Risk: Broad car-cost, financing, or buying questions may activate the skill even when the user needs a different type of automotive help. <br>
Mitigation: Confirm budget, new-versus-used status, use case, and powertrain before giving recommendations, and gracefully decline topics outside the skill scope. <br>


## Reference(s): <br>
- [Buying Guide](references/buying-guide.md) <br>
- [Cost Calculation](references/cost-calculation.md) <br>
- [Pitfalls Guide](references/pitfalls.md) <br>
- [Wuxi Policy](references/wuxi-policy.md) <br>
- [Brand Scores](data/brand-scores.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown with tables, bullet lists, sourced claims, and cost estimates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current web search for pricing, discounts, reviews, complaints, and used-car listings; falls back to clearly marked estimates when search is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
