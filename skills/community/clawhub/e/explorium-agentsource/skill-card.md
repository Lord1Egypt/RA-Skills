## Description: <br>
B2B prospecting via Explorium AgentSource API. Requires EXPLORIUM_API_KEY. Find companies, prospects, enrich with firmographics/contacts, track events, export CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yossigolan](https://clawhub.ai/user/yossigolan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, growth, and market research users use this skill to find B2B companies or prospects, preview market size and sample records, enrich selected entities, inspect events, and export confirmed results to CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interactive setup can expose an Explorium API key in terminal output or shell history on shared, logged, or screen-shared terminals. <br>
Mitigation: Set EXPLORIUM_API_KEY in a private terminal or use the CLI config command only in a trusted local session; avoid interactive setup on shared or recorded terminals. <br>
Risk: Prospecting, enrichment, and matching results may include sensitive company or contact data written to predictable /tmp/agentsource_*.json files. <br>
Mitigation: Treat result files as sensitive, delete them after use, restrict local machine access, and confirm that contact enrichment and outreach comply with applicable privacy and legal obligations. <br>
Risk: Optional call_reasoning can transmit the user's natural-language query to Explorium as request metadata. <br>
Mitigation: Use call_reasoning only after user consent; omit it when query text should not be logged by the remote service. <br>


## Reference(s): <br>
- [Explorium AgentSource API key setup](https://developers.explorium.ai/reference/setup/getting_your_api_key) <br>
- [Explorium AgentSource API endpoint](https://api.explorium.ai/v1/) <br>
- [Filter reference](references/filters.md) <br>
- [Enrichment reference](references/enrichments.md) <br>
- [Events reference](references/events.md) <br>
- [ClawHub release page](https://clawhub.ai/yossigolan/explorium-agentsource) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI operations write JSON result files and can export CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXPLORIUM_API_KEY; optional call_reasoning sends the user's query text to Explorium when explicitly used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
