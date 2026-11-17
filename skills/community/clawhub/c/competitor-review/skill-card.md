## Description:

分析并比较亚马逊竞品评论，识别反复出现的优势、短板和差异化机会，并生成对比报告与建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

面向亚马逊卖家和运营人员，用于横向分析竞品评论、定位买家反复提到的问题与优势，并据此提出产品和 Listing 的差异化改进建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some flows can spend ARI credits without fresh approval, including a command documented as quote-only.

Mitigation: Set the ARI account to ask before each spend, use the explicit quote command to check prices, and do not assume omitting --confirm prevents charges.

Risk: Recurring review collection can continue on a weekly schedule and incur ongoing credit costs.

Mitigation: Choose manual scheduling for one-time collection and approve recurring monitoring separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/funewa/skills/competitor-review)
- [ARI CLI and API reference](artifact/references/reference.md)
- [ARI Monitor Center](https://ari.funewa.com/zh/monitor)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, CSV, HTML]

**Output Format:** [Chinese analysis summaries and reports in Markdown, with optional CSV or HTML exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings reflect the collected review sample and returned ARI data; coverage may be incomplete.]

## Skill Version(s):

1.5.3 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
