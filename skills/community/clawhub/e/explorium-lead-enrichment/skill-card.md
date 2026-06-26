## Description: <br>
Enriches existing leads, contacts, and company lists with B2B data, including emails, phone numbers, firmographics, technographics, and job details, for single records, inline lists, and bulk CSV workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haroExplorium](https://clawhub.ai/user/haroExplorium) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and business operations teams use this skill to enrich CRM leads, contacts, company lists, and CSV files with B2B contact and company data for data hygiene, list cleaning, and data append workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles lead lists, contact details, company records, and request metadata that may include personal or sensitive business data. <br>
Mitigation: Use it only with authorized data, disclose remote enrichment to affected workflows where required, and send only the fields needed for the requested enrichment. <br>
Risk: The skill sends search filters, entity IDs, and optional request metadata to the Explorium API. <br>
Mitigation: Confirm the user is comfortable sending the requested data to Explorium before API calls, and avoid --call-reasoning unless the user explicitly agrees. <br>
Risk: API key handling can expose credentials if users paste keys into chat or store them insecurely. <br>
Mitigation: Use EXPLORIUM_API_KEY or a secret manager, never request API keys in chat, and prefer secure local configuration with restricted file permissions. <br>
Risk: The workflow discovers and executes a local CLI path, which can be risky if the path is unexpected. <br>
Mitigation: Verify the resolved agentsource.py path before running commands and install only from a trusted publisher. <br>
Risk: The CLI writes enrichment results to /tmp/agentsource_*.json, which may retain contact or company data after use. <br>
Mitigation: Delete temporary agentsource JSON files after enrichment and avoid printing full bulk result files into chat. <br>


## Reference(s): <br>
- [Enrichment Reference](artifact/references/enrichments.md) <br>
- [Events Reference](artifact/references/events.md) <br>
- [Filter Reference](artifact/references/filters.md) <br>
- [ClawHub Release Page](https://clawhub.ai/haroExplorium/explorium-lead-enrichment) <br>
- [Explorium AgentSource API](https://api.explorium.ai/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON or CSV file outputs from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI results are written to temporary JSON files and may be exported to CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
