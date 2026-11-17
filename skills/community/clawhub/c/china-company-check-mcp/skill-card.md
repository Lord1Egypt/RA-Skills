## Description:

Look up and verify mainland-China companies from official GSXT/SAMR registration data using the China-Check MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ballcheung](https://clawhub.ai/user/ballcheung)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sourcing teams use this skill to find, verify, and vet mainland-China companies, suppliers, factories, manufacturers, brands, and business partners. It helps retrieve legal names, registration status, Unified Social Credit Codes, legal representatives, registered capital, addresses, industries, and business scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company lookup queries are sent to China-Check's remote MCP service.

Mitigation: Avoid submitting confidential investigation context or personal phone numbers unless that disclosure is acceptable.

Risk: Registry snapshots may be insufficient for mission-critical decisions.

Mitigation: Independently verify important registry information with official sources before relying on it.

## Reference(s):

- [Source repository](https://github.com/ballcheung/china-company-check-mcp)
- [ClawHub skill page](https://clawhub.ai/ballcheung/skills/china-company-check-mcp)
- [China-Check MCP endpoint](https://www.china-check.com/api/mcp/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with registry fields and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only remote MCP lookup results may include official registry identifiers, capital, address, business scope, report options, purchase URL, and disclaimer text.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
