## Description:

Find and qualify B2B prospects instantly by searching companies and contacts by industry, size, tech stack, location, and job title, with optional contact enrichment and CSV export through Explorium AgentSource.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haroexplorium](https://clawhub.ai/user/haroexplorium)

### License/Terms of Use:


## Use Case:

Sales, SDR, account executive, and go-to-market teams use this skill to define an ideal customer profile, discover matching companies and decision-makers, preview and qualify results, enrich contact or company data, and export prospecting lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospecting filters, target companies, contact identifiers, and CSV-derived names, emails, or LinkedIn data may be sent to Explorium.

Mitigation: Use the skill only with authorized prospecting data and avoid employee, customer, regulated, or confidential lists unless there is a lawful basis.

Risk: The skill can save an Explorium API key in a local config file and use it for remote API calls.

Mitigation: Prefer the EXPLORIUM_API_KEY environment variable, keep any saved config file owner-readable only, and rotate the key if it was exposed in chat, logs, or shared storage.

Risk: API result files are written to /tmp/agentsource_*.json and CSV exports may be written to Downloads.

Mitigation: Delete temporary result files and exported lists after use, and choose a controlled export location for sensitive prospecting data.

Risk: Large fetches and enrichments can consume Explorium credits and retrieve broad contact datasets.

Mitigation: Review market sizing, samples, enrichment choices, and cost estimates before approving full fetches or exports.

## Reference(s):

- [Filter Reference](references/filters.md)
- [Events Reference](references/events.md)
- [Enrichment Reference](references/enrichments.md)
- [ClawHub skill page](https://clawhub.ai/haroexplorium/skills/explorium-sales-prospecting)
- [Publisher profile](https://clawhub.ai/user/haroexplorium)
- [Explorium AgentSource API endpoint](https://api.explorium.ai/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, CSV files, guidance]

**Output Format:** [Conversational guidance, markdown tables, shell commands, JSON result-file paths, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an Explorium API key, writes API responses to /tmp/agentsource_*.json, and can export prospect or company lists to CSV after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
