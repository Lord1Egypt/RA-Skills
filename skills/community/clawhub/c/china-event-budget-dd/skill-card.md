## Description:

逐行审核并谈判中国境内大型线下活动、展会、展台、发布会及临时活动空间的预算或供应商报价，识别异常后给出可执行的第一口、成交红线、补件和谈判话术。适用于预算表、报价单、BOQ及结算表；不用于给承建商综合打分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Event, procurement, finance, and operations teams use this skill to review China-based event budgets, BOQs, supplier quotes, and settlement sheets line by line. It identifies evidence-backed anomalies, missing documentation, amount impacts, and negotiation positions without assigning an overall vendor score.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: User-provided budgets, supplier quotes, and negotiation limits may contain confidential commercial information.

Mitigation: Use sanitized copies when information may leave the private workspace, and provide only documents the user is comfortable having an agent analyze.

Risk: External price checks can expose confidential project details if raw customer, supplier, venue, or budget information is searched directly.

Mitigation: Keep confidential project details out of external searches unless they are sanitized, and use public sources only as comparable evidence with matching city, venue, date, scope, tax, and service conditions.

## Reference(s):

- [逐项异常规则](references/anomaly-rules.md)
- [地区、场馆与价格基准](references/regional-benchmarking.md)
- [报告字段与呈现规则](references/report-schema.md)
- [一线砍价方法](references/negotiation-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured line-item tables, summaries, and negotiation wording when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include amount ranges, evidence gaps, recommended handling, negotiation anchor prices, internal red lines, and supplier-facing talk tracks.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
