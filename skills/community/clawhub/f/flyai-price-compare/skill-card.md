## Description:

使用 FlyAI 进行高铁票和飞机票比价，给用户推荐最优出行方式。以明天出发的高铁票（时间最短车次）为基准价进行对比。支持弃程票搜索和前后一天价格对比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixinda](https://clawhub.ai/user/jixinda)

### License/Terms of Use:

MIT-0

## Use Case:

External travel-planning users use this skill to compare rail and flight options, evaluate nearby-date flight prices, and receive a practical recommendation for cost, time, and convenience. The skill may also surface hidden-city ticket options when they appear materially cheaper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hidden-city or skip-ticket recommendations can conflict with airline contract terms and may create baggage, cancellation, loyalty-program, or rerouting risks.

Mitigation: Present these options as informational only, clearly disclose the constraints, and avoid recommending them when the traveler needs checked baggage, round-trip protection, or frequent-flyer benefits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jixinda/skills/flyai-price-compare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel comparison with tables, recommendations, risk notes, and optional FlyAI search commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes time-sensitive fare comparisons and hidden-city ticket cautions when applicable.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
