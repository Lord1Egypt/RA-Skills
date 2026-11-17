## Description:

Aggregates customs trade intelligence, global company due diligence, and LinkedIn professional network data so agents can analyze markets, profile companies, identify buyers or suppliers, and map decision-maker networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, sourcing, export, and B2B prospecting teams use this skill to size product markets, validate supplier or buyer activity, inspect company ownership and employees, and find professional-network context before outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid lead-generation API and can incur charges for searches, list pages, and detail calls.

Mitigation: Confirm fee-incurring operations before execution and use the price-information flow for current pricing.

Risk: The skill handles an UPKUAJING_API_KEY and stores credentials under ~/.upkuajing.

Mitigation: Treat the API key as a secret, avoid printing credential files into chats or logs, and restrict permissions on local credential files.

Risk: The skill retrieves professional, company, and contact-related data that may be subject to privacy, outreach, and data-use obligations.

Mitigation: Use retrieved people and contact data only under applicable privacy, employment, and outreach laws and internal compliance policies.

Risk: Server security evidence marks the release as suspicious because the integration is real, paid, and handles personal/contact data.

Mitigation: Install only if you are comfortable with a paid lead-generation tool that can retrieve professional/contact data and store results locally. Do not print ~/.upkuajing/.env into chats or logs; treat the API key as a secret, use a virtual environment, restrict file permissions on ~/.upkuajing, and ensure your use of people/contact data complies with applicable privacy and outreach laws.

## Reference(s):

- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Customs analysis area API](references/customs-analysis-area-api.md)
- [Customs analysis HS code search API](references/customs-analysis-hscode-search-api.md)
- [Customs analysis trends API](references/customs-analysis-trends-api.md)
- [Customs company stats API](references/customs-company-stats-api.md)
- [Customs company partner stats API](references/customs-company-partner-stats-api.md)
- [Customs overview summary API](references/customs-overview-summary-api.md)
- [Customs overview top buyers and suppliers API](references/customs-overview-top-n-api.md)
- [Global company search API](references/global-company-list-api.md)
- [Global company person search API](references/global-company-person-list-api.md)
- [Company employee list API](references/company-employee-list-api.md)
- [Company shareholder list API](references/company-shareholder-list-api.md)
- [LinkedIn company search API](references/linkedin-company-list-api.md)
- [LinkedIn person search API](references/linkedin-person-list-api.md)
- [LinkedIn professional network APIs](references/linkedin-person-colleague-list-api.md)
- [Skill error report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with shell command examples and API-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, an UPKUAJING_API_KEY, paid API calls, and local storage of retrieved task data.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
