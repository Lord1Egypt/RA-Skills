## Description: <br>
Generates professional Chinese-language enterprise insight reports from multidimensional company data for credit analysis, business research, investment due diligence, and quick company understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Royyyyor](https://clawhub.ai/user/Royyyyor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, finance and banking professionals, legal professionals, and business counterparties use this skill to generate enterprise profile, credit, business research, and investment due diligence reports for mainland China entities. <br>

### Deployment Geography for Use: <br>
Global use with mainland China entity data scope. <br>

## Known Risks and Mitigations: <br>
Risk: Queried company names and related legal-representative identifiers are sent to the configured Qibook/CHINADAAS API using user credentials. <br>
Mitigation: Confirm the data-sharing posture before use, protect API credentials, and avoid querying sensitive or confidential entities unless approved. <br>
Risk: Generated reports may be used for credit, investment, legal, or counterparty decisions. <br>
Mitigation: Require human review and verify source data freshness before using reports for external delivery or high-impact decisions. <br>
Risk: Several templates instruct the agent to hide that reports are AI-generated. <br>
Mitigation: Remove or override that template language and disclose AI assistance where appropriate before production or external use. <br>


## Reference(s): <br>
- [Enterprise Intro ClawHub listing](https://clawhub.ai/Royyyyor/enterprise-intro) <br>
- [Qibook API provider homepage](https://qibook.com) <br>
- [Sample company report](artifact/examples/sample_company_report.md) <br>
- [Company report template](artifact/templates/company.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHINADAAS_UID, CHINADAAS_KEY, and CHINADAAS_BASE_URL; report length is capped by input size.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
