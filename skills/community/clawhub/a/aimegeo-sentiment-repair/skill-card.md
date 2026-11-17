## Description:

核对 AI 回答或客户质疑与产品事实，交付误解对照表、纠正 FAQ、修改位置及同题复测问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

品牌与产品团队可用此技能核对 AI 回答或客户质疑中的产品说法，并根据提供的事实写出可公开使用的纠正 FAQ、具体修改建议和后续复测问题。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A correction could overstate what the supplied product facts establish.

Mitigation: Review each public answer against its cited evidence and applicable product version; leave missing or conflicting facts marked for confirmation.

Risk: A planned retest could be mistaken for a completed platform check.

Mitigation: Keep unrun checks labeled as plans and record actual answers and native citations only after collection.

Risk: Publishing unreviewed corrections could put inaccurate content on public accounts.

Mitigation: Confirm the final content and target accounts before publishing; publishing remains under user control.

## Reference(s):

- [Data contract](references/data-contract.md)
- [aimeGeo sentiment repair repository](https://github.com/xxjrq/aimegeo-sentiment-repair)
- [GEOly AI Brand Sentiment Optimizer (functional reference)](https://clawhub.ai/geoly-geo/geo-sentiment-optimizer)
- [aimeGeo product site](https://geo.aimmme.com/)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [CSV claim-to-fact table, Markdown correction FAQ, and JSON retest plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-linked claims preserve source and time scope; unknown facts and unrun retests remain explicitly unresolved.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
