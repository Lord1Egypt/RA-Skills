## Description: <br>
Find B2B companies and contacts using the Explorium AgentSource API, enrich them with business and contact intelligence, and export confirmed results to CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yossigolan](https://clawhub.ai/user/yossigolan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, marketing, research, and operations users can use this agent skill to find companies or professional contacts, preview market size and sample results, enrich selected records, and export lead or account lists. It is intended for workflows that can use an Explorium AgentSource API key and reviewed data exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected filters, entity IDs, matching records, and an API key to Explorium's remote API. <br>
Mitigation: Install and run it only when that data sharing is acceptable for the user's workflow and organization. <br>
Risk: API keys and lead data may be stored locally in configuration or temporary result files. <br>
Mitigation: Prefer setting EXPLORIUM_API_KEY as an environment variable, use explicit CSV paths, keep fetch limits intentional, and delete /tmp/agentsource_*.json after use on shared machines. <br>
Risk: Full fetches or exports can consume credits and produce large lead datasets. <br>
Mitigation: Use the documented market sizing and sample review steps, and require explicit user confirmation before full fetch or CSV export. <br>


## Reference(s): <br>
- [Explorium API key setup](https://developers.explorium.ai/reference/setup/getting_your_api_key) <br>
- [Explorium AgentSource API](https://api.explorium.ai/v1/) <br>
- [Filter Reference](references/filters.md) <br>
- [Enrichment Reference](references/enrichments.md) <br>
- [Event Reference](references/events.md) <br>
- [ClawHub skill page](https://clawhub.ai/yossigolan/explorium-agentsource-companies-contacts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, CSV, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands, JSON result files, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an Explorium AgentSource API key; writes API results to local temp JSON files before optional CSV export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
