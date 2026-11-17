## Description:

逐行审核并谈判中国境内大型线下活动、展会、展台、发布会及临时活动空间的预算或供应商报价，识别异常后给出可执行的第一口、成交红线、补件和谈判话术。适用于预算表、报价单、BOQ及结算表；不用于给承建商综合打分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, marketing, event, and finance teams use this Chinese-language skill to review China on-site event budgets and supplier quotes line by line. It identifies evidence-backed anomalies, missing support, potential add-ons, and negotiation positions while preserving traceability to source budget rows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for final commercial approval or professional legal, tax, fire, structural, electrical, labor, or insurance advice.

Mitigation: Treat outputs as decision support and require qualified internal, venue, or professional review before approvals, filings, or contractual commitments.

Risk: Budget files may contain confidential contract details, personal data, internal pricing, supplier identities, or negotiation red lines.

Mitigation: Sanitize sensitive details before using external search or sharing examples, and keep traceability without copying private source files into public skill artifacts.

Risk: Market-price comparisons can be misleading when city, venue, dates, specifications, quantities, service scope, tax basis, or procurement terms differ.

Mitigation: Use comparable, current, and documented benchmarks; mark incomplete comparisons as pending verification rather than confirmed overpricing.

## Reference(s):

- [逐项异常规则](references/anomaly-rules.md)
- [地区、场馆与价格基准](references/regional-benchmarking.md)
- [报告字段与呈现规则](references/report-schema.md)
- [一线砍价方法](references/negotiation-playbook.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown tables and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces line-level anomaly findings, evidence gaps, amount impacts, summary totals, and optional negotiation positions; does not produce executable code.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
