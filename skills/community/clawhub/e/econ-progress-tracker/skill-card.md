## Description:

This Chinese-language skill guides agents to collect current financial news and official economic indicators, then assess China economic progress across diagnostic indicators, policy paths, industrial progress, and risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skfrom](https://clawhub.ai/user/skfrom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this Chinese-language workflow to track China economic conditions with current public financial news, official macro indicators, and dated local snapshots for comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow browses public financial sources and may archive prompt context in dated local snapshots.

Mitigation: Avoid including confidential research notes or private business context unless that information may be retained in the local archive.

Risk: The skill produces economic analysis from current news and indicators, which can be incomplete, stale, or misinterpreted.

Mitigation: Review cited source data and trend judgments before using the output for business, investment, or policy decisions.

## Reference(s):

- [中国经济进展跟踪完整分析框架](references/framework.md)
- [中国国家统计局](http://www.stats.gov.cn)
- [中国人民银行](http://www.pbc.gov.cn)
- [中国财政部](http://www.mof.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown analysis report with a dated local snapshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public financial sources and official macroeconomic indicators; stores snapshots under memory/econ-tracker/ when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
