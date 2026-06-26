## Description: <br>
A股估值质量审阅专家，面向IPO定价、并购重组、股权激励、私募估值等场景审阅估值报告，识别假设偏差、方法论缺陷和监管合规风险，并输出结构化审阅意见书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance, investment, and corporate transaction reviewers use this skill to assess A-share valuation reports for methodology quality, assumption support, data traceability, and regulatory risk. It is intended to produce structured review opinions, issue lists, valuation-range comments, and risk prompts for supported A-share valuation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides finance and valuation review guidance that may be inaccurate if the transaction type, company, exchange, jurisdiction, or source report is outside its intended A-share/PRC valuation scope. <br>
Mitigation: Confirm the transaction type, company, exchange, jurisdiction, and valuation scenario before relying on thresholds or compliance framing. <br>
Risk: Valuation reports may contain confidential transaction, company, or investor information. <br>
Mitigation: Use the skill only in an agent environment approved for confidential financial data. <br>
Risk: The artifact contains fixed review thresholds and regulatory framing that may become stale or may not apply to every transaction. <br>
Mitigation: Validate cited thresholds and regulatory requirements against current authoritative sources before using the output for business or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinfeihaaaaaaaaaaa/a-share-valuation-reviewer) <br>
- [Publisher profile](https://clawhub.ai/user/yinfeihaaaaaaaaaaa) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown structured review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces issue lists, valuation-range comments, regulatory risk prompts, and recommendations; it does not execute code or move data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
