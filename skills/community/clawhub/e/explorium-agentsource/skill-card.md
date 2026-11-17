## Description:

Finds and exports B2B companies or contacts using the Explorium AgentSource API, with support for filters, enrichments, event signals, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yossigolan](https://clawhub.ai/user/yossigolan)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and go-to-market teams use this skill through an agent to turn natural-language prospecting requests into AgentSource API searches, preview market size and samples, enrich records, retrieve event signals, and export confirmed results to CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an Explorium AgentSource API key.

Mitigation: Set EXPLORIUM_API_KEY outside chat and avoid entering secrets where terminal output is logged; if using saved config, keep ~/.agentsource/config.json protected with owner-only permissions.

Risk: Prospecting, matching, enrichment, and events workflows can process customer lists or personal contact data.

Mitigation: Use the skill only with appropriate consent and data handling approval, and send only the fields needed for the requested search, match, enrichment, or export.

Risk: Search filters, entity IDs, optional call_reasoning, and imported CSV records may be sent to Explorium's remote API.

Mitigation: Review the request before execution and omit call_reasoning unless the user explicitly agrees to send natural-language query context.

Risk: Result files under /tmp/agentsource_*.json can contain prospecting results or contact data.

Mitigation: Remove or protect temporary result files after use, especially on shared machines or when processing customer lists.

## Reference(s):

- [Filter Reference](artifact/references/filters.md)
- [Enrichment Reference](artifact/references/enrichments.md)
- [Events Reference](artifact/references/events.md)
- [Explorium AgentSource API Key Setup](https://developers.explorium.ai/reference/setup/getting_your_api_key)
- [Explorium AgentSource API Endpoint](https://api.explorium.ai/v1/)
- [ClawHub Skill Page](https://clawhub.ai/yossigolan/skills/explorium-agentsource)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, CSV files]

**Output Format:** [Markdown guidance with inline shell commands, JSON result file paths, and CSV export paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXPLORIUM_API_KEY; writes API result data to /tmp/agentsource_*.json; free-text call_reasoning is opt-in]

## Skill Version(s):

1.0.3 (source: server release metadata and plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
