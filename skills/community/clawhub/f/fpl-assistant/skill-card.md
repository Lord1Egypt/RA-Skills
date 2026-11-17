## Description:

Fantasy Premier League (FPL) assistant for squad management, transfer planning, captain selection, and chip strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongbinnie](https://clawhub.ai/user/dongbinnie)

### License/Terms of Use:

MIT-0

## Use Case:

External FPL managers and agents use this skill to analyze squads, plan transfers, choose captains, set lineups, and time chips using public Fantasy Premier League data and the bundled rules and strategy references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad terms such as fantasy, captain, or transfer may activate the skill outside a Fantasy Premier League context.

Mitigation: Use the skill for clearly FPL-related requests and confirm the user's gameweek or team context before making recommendations.

Risk: The skill may ask for a manager ID and fetch public FPL team data.

Mitigation: Use manager IDs only when the user is comfortable referencing that public team information, and avoid requesting unrelated personal or sensitive data.

## Reference(s):

- [FPL API Reference](references/api.md)
- [FPL Rules Reference](references/rules.md)
- [FPL Player Selection Strategy](references/strategy.md)
- [Fantasy Premier League Public API](https://fantasy.premierleague.com/api/)
- [ClawHub Skill Page](https://clawhub.ai/dongbinnie/skills/fpl-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with optional inline shell commands for public FPL API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference public FPL manager IDs and live public API data when the user provides enough context.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
