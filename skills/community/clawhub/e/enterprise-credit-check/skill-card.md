## Description: <br>
Enterprise Credit Check helps an agent prepare official-source enterprise credit checks with weighted scoring, hard-stop risk triggers, and Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external due diligence users use this skill to organize enterprise credit checks from official Chinese public and credit data sources, calculate a risk score, and draft a report for business decisions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The generated report may appear like an authoritative credit report even when findings depend on manual or unverified inputs. <br>
Mitigation: Treat outputs as checklist and report drafting assistance; require official source evidence for every finding before relying on the result. <br>
Risk: Credit and business checks can involve sensitive information or restricted account access. <br>
Mitigation: Use only legally authorized queries and avoid entering sensitive credentials or business information unless the operator has confirmed authorization. <br>
Risk: The artifact includes a private contact solicitation for credit repair or deeper due diligence. <br>
Mitigation: Do not share business, credit, or identity information through that contact unless the operator independently verifies and trusts the recipient. <br>


## Reference(s): <br>
- [Data Sources](references/data_sources.md) <br>
- [Risk Rules](references/risk_rules.md) <br>
- [Scoring Standards](references/scoring_standards.md) <br>
- [People's Bank of China Credit Reference Center](https://www.pbccrc.org.cn) <br>
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn) <br>
- [China Enforcement Information Disclosure Network](http://zxgk.court.gov.cn) <br>
- [China Judgments Online](https://wenshu.court.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reports, risk alerts, scoring summaries, and structured calculation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report outputs should cite official source evidence supplied by the user or agent and should be treated as reference material, not an independently verified credit report.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
