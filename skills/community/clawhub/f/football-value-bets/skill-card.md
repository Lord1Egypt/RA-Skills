## Description:

Professional football bet analysis skill that generates data-driven bet slips from form, head-to-head records, standings, injuries, odds value, and result tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandichi](https://clawhub.ai/user/nandichi)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to analyze professional football matches for betting-oriented picks, generate concise bet slip recommendations, and track saved results, hitrate, ROI, and monthly budget usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores bet slips and betting statistics locally.

Mitigation: Review saved data behavior before installation and ask the user before saving betting history when local retention is not desired.

Risk: Security evidence reports a date path-validation issue that could allow result updates to touch JSON files outside the betting folder.

Mitigation: Use canonical YYYY-MM-DD dates, validate dates before result updates, and prefer a version that confines file paths to the betting data folder.

Risk: The skill may use web searches for betting context and external football-data.org API calls.

Mitigation: Review external data sources, configure only the required FOOTBALL_DATA_API_KEY, and treat betting recommendations as uncertain analysis rather than guaranteed outcomes.

## Reference(s):

- [football-data.org API v4](https://api.football-data.org/v4)
- [ClawHub skill page](https://clawhub.ai/nandichi/skills/football-value-bets)
- [Publisher profile](https://clawhub.ai/user/nandichi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations with tables, JSON helper-script output, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and FOOTBALL_DATA_API_KEY; helper scripts may save local JSON bet history and statistics.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
