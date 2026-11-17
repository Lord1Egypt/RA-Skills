## Description:

基于企查查、爱企查、天眼查、启信宝、国家企业信用信息公示系统等公开渠道，生成中国企业尽职调查报告（结构化HTML报告）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[spzhangsanfeng](https://clawhub.ai/user/spzhangsanfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to compile China-focused enterprise due diligence reports from public company information sources, including registration, ownership, judicial risk, operations, and source disclosures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public company-record sources may be incomplete, stale, or inconsistent.

Mitigation: Verify important claims against primary sources before making business, legal, or compliance decisions.

Risk: Generated due-diligence reports may contain sensitive company or personal information.

Mitigation: Limit collection and sharing to necessary information and handle reports as sensitive material.

Risk: Generated HTML can contain untrusted content from source data.

Mitigation: Escape or sanitize report content before opening, storing, or sharing the HTML output.

## Reference(s):

- [企业报告数据采集清单](references/data-sources.md)
- [ClawHub skill page](https://clawhub.ai/spzhangsanfeng/skills/enterprise-report)

## Skill Output:

**Output Type(s):** [HTML, Analysis, Guidance]

**Output Format:** [Structured HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a report template with sections for company registration, ownership, management, risk analysis, changes, branches, permits, annual reports, conclusions, and source statements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
