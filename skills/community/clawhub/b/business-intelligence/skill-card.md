## Description:

Model business performance, define KPIs, and turn data into decision-ready dashboards, briefings, and operating cadences for teams and executives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External teams, operators, founders, product leaders, finance leaders, and analysts use this skill to define KPI contracts, model metric trees, specify dashboards, and prepare decision briefs and operating cadences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local BI memory may contain sensitive business context or decision history.

Mitigation: Decide before installation whether local memory should be used, and avoid storing credentials, raw confidential exports, or unrelated personal details under ~/business-intelligence/.

Risk: BI recommendations can be misleading when KPI definitions, data quality, or source freshness are uncertain.

Mitigation: Use KPI contracts, formula version notes, source quality gates, and confidence labels before making high-impact decisions from generated briefs or dashboard specifications.

## Reference(s):

- [Business Intelligence ClawHub Page](https://clawhub.ai/ivangdavila/skills/business-intelligence)
- [Business Intelligence Homepage](https://clawic.com/skills/business-intelligence)
- [Setup](artifact/setup.md)
- [Metric Tree](artifact/metric-tree.md)
- [KPI Dictionary and Contracts](artifact/kpi-dictionary.md)
- [Dashboard Specifications](artifact/dashboard-specs.md)
- [Insight Briefs](artifact/insight-briefs.md)
- [Decision Cadence](artifact/decision-cadence.md)
- [Data Contracts and Reliability](artifact/data-contracts.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, templates, and structured BI artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write optional local BI context under ~/business-intelligence/ when memory is enabled; no external network requests by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
