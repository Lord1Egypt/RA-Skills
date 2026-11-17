## Description:

从客户材料自动抽取企业碳资信评级字段，确认缺失项和行业参数，计算企业碳资信评分，并生成正式 Word 评级报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, and consultants use this skill to prepare Chinese-language enterprise carbon-credit rating work from customer-provided materials, including field extraction, missing-data confirmation, scoring, no-rating decisions, and formal DOCX report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer materials and generated rating artifacts may contain confidential enterprise financial, identity, and carbon-account data.

Mitigation: Handle uploaded materials, rating_result.json, and DOCX outputs as confidential and limit access to authorized reviewers.

Risk: Incorrect extracted fields, missing required data, or unconfirmed industry weights can produce misleading rating conclusions.

Mitigation: Require user confirmation of enterprise identity, industry classification, alpha/beta/gamma weights, SWV weights, and critical missing fields before scoring or report generation.

Risk: Reports generated from untrusted JSON inputs may reflect unsupported or manipulated values.

Mitigation: Validate source materials and rating_result.json independently before relying on generated reports.

## Reference(s):

- [Extraction Dictionary](references/extraction_dictionary.md)
- [Model Rules](references/model_rules.md)
- [Report Generation](references/report_generation.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/enterprise-carbon-credit-rating)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown/text guidance plus generated JSON and DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses confirmed input data to produce rating_result.json and a formal Word report; may disclose missing data, adjustment items, and no-rating triggers.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
