## Description:

当用户查询物流指数总分时，输出物流指数数据、行业排名、数据分析、定位异常指数、输出运营建议

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-vb](https://clawhub.ai/user/a-vb)

### License/Terms of Use:

MIT-0

## Use Case:

Operations employees use this skill to query a carrier and statistical date, retrieve logistics index data, compare rankings and seven-day trends, identify the fixed sub-indicator 揽收及时率, and produce operational recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads operational data from local Excel files.

Mitigation: Keep 2.xlsx and 揽收及时率异常明细.xlsx in a controlled location and confirm they contain only data needed for this analysis before use.

Risk: The skill opens a business portal over plain HTTP.

Mitigation: Install only if access to the named logistics portal is expected, and prefer an HTTPS portal URL when available.

## Reference(s):

- [Fullask ClawHub skill page](https://clawhub.ai/a-vb/skills/fullask)
- [Jingwe shipper overview portal](http://jingwe.jdl.com/#/indexCenter/shipperOverview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style logistics index summary with rankings, trend analysis, anomaly counts, category proportions, and operational recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires carrier name and statistical date as inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
