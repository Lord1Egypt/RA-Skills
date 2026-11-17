## Description:

Deep company research using Explorium AgentSource that produces company profiles, competitive intelligence, technology stack analysis, funding history, workforce trends, executive information, and recent news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haroexplorium](https://clawhub.ai/user/haroexplorium)

### License/Terms of Use:


## Use Case:

Sales, marketing, investment, and business research users use this skill to gather company intelligence for account planning, competitive analysis, due diligence, market mapping, and pre-call preparation. The skill can also find and enrich prospect or executive contact information when the user has proper authorization and a legal basis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow can send search filters, entity IDs, and optional request metadata, including the original request, to Explorium.

Mitigation: Avoid confidential prompt context unless the user has approved that disclosure, and omit optional request metadata when it is not needed.

Risk: The skill supports broad prospect and contact enrichment workflows that may return personal or professional contact data.

Mitigation: Use prospect and contact enrichment only with appropriate authorization, legal basis, and data-handling controls.

Risk: API keys can be saved locally or entered through setup/config commands.

Mitigation: Prefer a protected EXPLORIUM_API_KEY environment variable, avoid pasting keys into chat, keep local config files protected, and rotate any key that was exposed.

Risk: Research results and exports can persist in /tmp or CSV files after the agent finishes.

Mitigation: Review, protect, or delete temporary JSON files and CSV exports after use, especially when they contain company intelligence or contact data.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/haroexplorium/skills/explorium-company-research)
- [Explorium AgentSource API](https://api.explorium.ai/v1/)
- [Enrichment Reference](references/enrichments.md)
- [Events Reference](references/events.md)
- [Filter Reference](references/filters.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports with tables, CLI commands, JSON temp-file paths, and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Explorium API results and may write local JSON result files under /tmp and user-selected CSV export files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
