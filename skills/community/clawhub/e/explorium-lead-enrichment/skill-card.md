## Description:

Enriches existing leads, contacts, and company lists with B2B emails, phone numbers, firmographics, technographics, job details, and CSV export workflows using Explorium AgentSource.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haroexplorium](https://clawhub.ai/user/haroexplorium)

### License/Terms of Use:


## Use Case:

External users, sales operations teams, and CRM operators use this skill to enrich single contacts, company lists, inline records, and CSV files with lead and company data before review and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead, contact, company, and optional request text may be sent to Explorium.

Mitigation: Use only datasets approved for this external service and avoid sensitive customer or contact records unless data-sharing requirements are satisfied.

Risk: API keys can be exposed through command-line configuration or echoed setup prompts.

Mitigation: Prefer environment variables or a managed secret store, never paste keys into agent chat, and rotate any key that may have been exposed.

Risk: Enrichment results and CSV exports can contain personal or business-sensitive data in temporary or download files.

Mitigation: Review output paths, restrict file access, remove temporary result files after use, and inspect exported CSVs before sharing or importing them.

Risk: The skill discovers a local CLI from broad filesystem locations before execution.

Mitigation: Verify the resolved CLI path points to the expected installed AgentSource tool before running enrichment commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haroexplorium/skills/explorium-lead-enrichment)
- [Publisher Profile](https://clawhub.ai/user/haroexplorium)
- [Explorium API Endpoint](https://api.explorium.ai/v1/)
- [Enrichment Reference](references/enrichments.md)
- [Filter Reference](references/filters.md)
- [Events Reference](references/events.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, structured enrichment previews, JSON intermediates, and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses EXPLORIUM_API_KEY and sends search filters, entity IDs, and optional request metadata to https://api.explorium.ai/v1/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
