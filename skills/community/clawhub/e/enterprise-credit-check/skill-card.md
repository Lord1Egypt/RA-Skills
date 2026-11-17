## Description:

Enterprise Credit Check helps agents guide five-dimensional enterprise credit checks using official Chinese government data sources, scoring rules, hard-stop risk triggers, and Markdown report templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business reviewers use this skill to structure enterprise credit checks, calculate risk scores, identify hard-stop risk conditions, and generate concise Markdown reports for Chinese enterprise due-diligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Official-source claims and generated reports may be unreliable if live source checks, provenance, authorization, or missing-data handling are not verified.

Mitigation: Require documented authorization, record live source checks with retained evidence, verify provenance, and treat missing or inaccessible data as a review blocker before using reports in credit, lending, procurement, or compliance decisions.

Risk: Fail-open scoring can understate risk when data is incomplete or unavailable.

Mitigation: Require explicit missing-data status in each report section and escalate incomplete checks to human review rather than relying on the calculated score alone.

Risk: The artifact includes a hardcoded promotional contact in generated report templates.

Mitigation: Remove promotional contact content or replace it with an approved organizational contact before deployment.

Risk: One referenced official source URL uses HTTP rather than HTTPS.

Mitigation: Require secure HTTPS source access where supported and document any exception before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/enterprise-credit-check)
- [Publisher profile](https://clawhub.ai/user/golngod)
- [Data Sources](references/data_sources.md)
- [Risk Rules](references/risk_rules.md)
- [Scoring Standards](references/scoring_standards.md)
- [People's Bank of China Credit Reference Center](https://www.pbccrc.org.cn)
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn)
- [China Enforcement Information Disclosure Network](http://zxgk.court.gov.cn)
- [China Judgments Online](https://wenshu.court.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports, risk alerts, scoring summaries, and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory enterprise credit-check materials that require live source verification, authorization, and human review before use in decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
