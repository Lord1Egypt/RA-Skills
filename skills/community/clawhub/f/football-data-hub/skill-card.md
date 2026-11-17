## Description:

Football Data Hub helps agents retrieve football standings, fixtures, results, team information, and optional player or H2H football data for information-only analysis without betting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query football league tables, fixtures, match results, team lookup data, and match preview context from documented football data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file-editing, search, network, and shell permissions beyond a read-only football lookup workflow.

Mitigation: Before deployment, remove unnecessary Write/Edit/Grep/WebSearch authority, constrain Bash to the bundled scripts, and restrict network access to documented football APIs.

Risk: Optional API-key-backed player and H2H features may be less reliable than the zero-config OpenLigaDB features.

Mitigation: Validate optional provider commands in the target environment and present unavailable features as optional rather than guaranteed.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and scan dependencies for the deployment environment before installing the skill.

## Reference(s):

- [Supported league mapping](references/leagues.md)
- [OpenLigaDB API](https://api.openligadb.de/)
- [API-Football](https://rapidapi.com/api-sports/api/api-football)
- [football-data.org API](https://api.football-data.org/v4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with tabular football data and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zero-config OpenLigaDB lookups are available without credentials; optional provider features may require API keys and validation in the target environment.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
