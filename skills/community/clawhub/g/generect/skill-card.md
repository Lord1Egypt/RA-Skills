## Description: <br>
Search B2B leads and companies, find and validate emails via the Generect Live API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vokaplok](https://clawhub.ai/user/vokaplok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, marketing, recruiting, and business development users can use this skill to search for lead and company records, enrich LinkedIn profiles, generate likely business email addresses, and validate email deliverability through Generect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead, company, LinkedIn URL, and email lookup data is sent to Generect as part of normal operation. <br>
Mitigation: Submit only data appropriate for Generect processing, avoid regulated or unnecessary personal data, and confirm a legal basis for enrichment or outreach. <br>
Risk: API credentials may grant access to paid or sensitive Generect account capabilities. <br>
Mitigation: Use a dedicated Generect API key, keep it in the GENERECT_API_KEY environment variable, and rotate or revoke it if exposed. <br>
Risk: Optional MCP server paths are separate integrations from the documented API helper. <br>
Mitigation: Review the remote MCP endpoint or local MCP package separately before enabling those optional paths. <br>


## Reference(s): <br>
- [Generect Live API documentation](https://liveapi.generect.com) <br>
- [Generect API access](https://beta.generect.com) <br>
- [Generect API filter reference](references/api-filters.md) <br>
- [ClawHub skill page](https://clawhub.ai/vokaplok/generect) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON request bodies and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GENERECT_API_KEY environment variable and sends requested lead, company, LinkedIn, and email lookup data to Generect.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
