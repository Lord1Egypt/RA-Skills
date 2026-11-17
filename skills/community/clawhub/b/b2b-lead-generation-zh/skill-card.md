## Description:

B2B lead-generation aggregation skill for Chinese-language workflows that combines customs trade intelligence, global company due diligence, and LinkedIn professional network data to evaluate markets, investigate companies, and identify buyers, suppliers, and decision makers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Exporters, sourcing teams, sales teams, procurement agents, and B2B lead-generation specialists use this skill to analyze HS-code trade markets, review company trade activity and ownership signals, and map professional contacts for cross-border customer development and supplier due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls paid third-party APIs for B2B, customs, company, and professional contact data.

Mitigation: Confirm every billable action before execution and use the pricing endpoint or published price page rather than estimating cost.

Risk: The skill stores and reads an API key from the local UPKUAJING_API_KEY environment variable or ~/.upkuajing/.env file.

Mitigation: Do not print the .env file, restrict local file permissions, and rotate the key if it may have been exposed.

Risk: Search results can contain professional contact or person data and may be saved locally in task_data.

Mitigation: Handle exported results according to applicable privacy and outreach rules, and delete task_data files when they are no longer needed.

Risk: Error reporting can send request context to the provider.

Mitigation: Ask the user before submitting an error report and include only the context needed for troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/b2b-lead-generation-zh)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Platform](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [customs-analysis-area-api.md](references/customs-analysis-area-api.md)
- [customs-analysis-hscode-detail-api.md](references/customs-analysis-hscode-detail-api.md)
- [customs-analysis-hscode-search-api.md](references/customs-analysis-hscode-search-api.md)
- [customs-analysis-overview-api.md](references/customs-analysis-overview-api.md)
- [customs-analysis-trade-percent-api.md](references/customs-analysis-trade-percent-api.md)
- [customs-analysis-trends-api.md](references/customs-analysis-trends-api.md)
- [customs-company-stats-api.md](references/customs-company-stats-api.md)
- [customs-company-partner-stats-api.md](references/customs-company-partner-stats-api.md)
- [customs-company-product-list-api.md](references/customs-company-product-list-api.md)
- [customs-company-port-list-api.md](references/customs-company-port-list-api.md)
- [customs-company-trends-api.md](references/customs-company-trends-api.md)
- [customs-overview-summary-api.md](references/customs-overview-summary-api.md)
- [customs-overview-top-n-api.md](references/customs-overview-top-n-api.md)
- [customs-overview-trade-list-api.md](references/customs-overview-trade-list-api.md)
- [customs-overview-trend-api.md](references/customs-overview-trend-api.md)
- [customs-overview-us-import-api.md](references/customs-overview-us-import-api.md)
- [global-company-list-api.md](references/global-company-list-api.md)
- [global-company-person-list-api.md](references/global-company-person-list-api.md)
- [company-employee-list-api.md](references/company-employee-list-api.md)
- [company-shareholder-list-api.md](references/company-shareholder-list-api.md)
- [person-colleague-list-api.md](references/person-colleague-list-api.md)
- [person-alumni-list-api.md](references/person-alumni-list-api.md)
- [person-experience-list-api.md](references/person-experience-list-api.md)
- [person-education-list-api.md](references/person-education-list-api.md)
- [linkedin-company-list-api.md](references/linkedin-company-list-api.md)
- [linkedin-company-employee-list-api.md](references/linkedin-company-employee-list-api.md)
- [linkedin-person-list-api.md](references/linkedin-person-list-api.md)
- [linkedin-person-colleague-list-api.md](references/linkedin-person-colleague-list-api.md)
- [linkedin-person-alumni-list-api.md](references/linkedin-person-alumni-list-api.md)
- [linkedin-person-experience-list-api.md](references/linkedin-person-experience-list-api.md)
- [linkedin-person-education-list-api.md](references/linkedin-person-education-list-api.md)
- [linkedin-school-detail-api.md](references/linkedin-school-detail-api.md)
- [school-detail-api.md](references/school-detail-api.md)
- [skill-error-report-api.md](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python shell commands and JSON API results or saved result-file links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; large search jobs may save paginated results under task_data and return task identifiers or file links.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and skill metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
