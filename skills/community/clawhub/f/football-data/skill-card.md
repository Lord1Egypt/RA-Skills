## Description: <br>
Football (soccer) data across 13 leagues for standings, schedules, match stats, xG, transfers, and player profiles with no API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to answer football data questions, inspect league tables and fixtures, analyze match statistics, and retrieve player or transfer information across supported competitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup depends on the external sports-skills Python package and may fall back to an unpinned GitHub install. <br>
Mitigation: Install in an isolated Python 3.10+ environment, prefer a pinned package version, and trust the sports-skills package source before use. <br>
Risk: Some data sources have limited coverage or delayed updates, including xG for only top-five leagues and post-match rather than guaranteed live results. <br>
Mitigation: Use the documented coverage table before calling commands and explain coverage gaps or freshness limits in user-facing answers. <br>
Risk: Invalid season, team, event, or command names can produce empty or failed lookups. <br>
Mitigation: Derive current seasons with get_current_season, discover IDs through search or schedule commands, and avoid commands listed as unavailable or nonexistent. <br>


## Reference(s): <br>
- [Commands Reference](references/commands.md) <br>
- [Data Coverage by League](references/data-coverage.md) <br>
- [JSON Schemas](references/schemas.md) <br>
- [Machina Sports](https://machina.gg) <br>
- [Transfermarkt](https://www.transfermarkt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and structured football data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-shaped examples and CLI command invocations for supported football data endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
