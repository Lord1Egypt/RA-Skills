## Description: <br>
Deep-dive company research using Explorium AgentSource, producing company profiles with firmographics, technographics, funding history, executive team context, competitors, workforce trends, and recent news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haroExplorium](https://clawhub.ai/user/haroExplorium) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, sales teams, market researchers, account planners, and due-diligence teams use this skill to research companies, compare competitors, map markets, and prepare structured business intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an Explorium API key. <br>
Mitigation: Treat the key as sensitive, prefer environment-variable configuration, and avoid copying real keys into chat, logs, screenshots, or shared files. <br>
Risk: Search filters, entity identifiers, and optional request context can be sent to a third-party API. <br>
Mitigation: Use the skill only when third-party company and prospect research is acceptable, and omit optional call-reasoning metadata when query logging is not appropriate. <br>
Risk: Company research exports may contain business intelligence or personal contact data. <br>
Mitigation: Review generated JSON and CSV outputs before saving or sharing them, and limit contact enrichment to the minimum fields needed. <br>
Risk: The server security verdict is suspicious because the skill performs credential handling, remote API calls, local exports, and person/contact enrichment. <br>
Mitigation: Review and scan the skill before deployment, and confirm the data handling posture matches the intended business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haroExplorium/explorium-company-research) <br>
- [Explorium API endpoint](https://api.explorium.ai/v1/) <br>
- [README](README.md) <br>
- [Enrichment Reference](references/enrichments.md) <br>
- [Events Reference](references/events.md) <br>
- [Filter Reference](references/filters.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and local JSON or CSV file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API results to temporary JSON files and export CSV files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
