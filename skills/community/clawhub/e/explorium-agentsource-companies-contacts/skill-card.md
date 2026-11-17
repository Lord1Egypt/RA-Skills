## Description:

Find and enrich B2B companies and contacts through the Explorium AgentSource API, including contact information, firmographics, technographics, intent signals, event data, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yossigolan](https://clawhub.ai/user/yossigolan)

### License/Terms of Use:


## Use Case:

External users, sales teams, GTM teams, and developers use this skill to translate natural-language B2B prospecting requests into AgentSource searches, review samples before spending credits, enrich company or contact records, and export CSVs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospecting filters, entity IDs, matching records, and optional call reasoning may be sent to Explorium.

Mitigation: Install only when this data sharing is acceptable, and send free-text call reasoning only with user consent.

Risk: API keys can be exposed if pasted into chat or entered in recorded or shared terminals.

Mitigation: Set EXPLORIUM_API_KEY through the environment or the local config command, and do not share API keys in conversation.

Risk: Temporary JSON result files and exported CSVs can contain sensitive prospect or company data on the local machine.

Mitigation: Treat /tmp result files and CSV exports as sensitive data and clean them up according to local data handling policy.

## Reference(s):

- [Filter Reference](references/filters.md)
- [Enrichment Reference](references/enrichments.md)
- [Events Reference](references/events.md)
- [Explorium AgentSource API Key Setup](https://developers.explorium.ai/reference/setup/getting_your_api_key)
- [Explorium AgentSource API Endpoint](https://api.explorium.ai/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, CSV files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON result files, and CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXPLORIUM_API_KEY; result JSON files and exported CSVs may contain prospecting data.]

## Skill Version(s):

1.0.0 (source: server release evidence and plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
