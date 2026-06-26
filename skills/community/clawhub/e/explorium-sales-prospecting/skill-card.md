## Description: <br>
Find and qualify B2B prospects by searching companies and contacts by industry, size, technology stack, location, job title, and buying intent using Explorium AgentSource. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haroExplorium](https://clawhub.ai/user/haroExplorium) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, SDR, account executive, and go-to-market teams use this skill to build targeted prospect and account lists, estimate market size, enrich results, and export CSV files for outbound workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Explorium API key and can store it in local configuration. <br>
Mitigation: Use only an approved API key, avoid sharing credentials in chat, and remove or rotate the key if access is no longer needed. <br>
Risk: Bulk prospecting can collect and export personal contact data such as emails and phone numbers. <br>
Mitigation: Use the skill only with a lawful basis and company policy approval, confirm scope before full fetches, and delete exported CSVs and temporary result files when they are no longer needed. <br>
Risk: Search filters, entity IDs, and optional request metadata are sent to the Explorium API. <br>
Mitigation: Avoid including confidential go-to-market strategy, customer names, or sensitive business context in prompts or request metadata unless approved for vendor sharing. <br>
Risk: Server-resolved provenance is unavailable and the security evidence notes an unofficial author mismatch. <br>
Mitigation: Review the publisher profile, artifact contents, and organization approval before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/haroExplorium/explorium-sales-prospecting) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/haroExplorium) <br>
- [Explorium AgentSource API endpoint](https://api.explorium.ai/v1/) <br>
- [Filter Reference](references/filters.md) <br>
- [Events Reference](references/events.md) <br>
- [Enrichment Reference](references/enrichments.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CSV export instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON result files in /tmp and CSV exports after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
