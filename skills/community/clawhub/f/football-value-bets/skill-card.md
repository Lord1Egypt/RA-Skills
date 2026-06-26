## Description: <br>
Professional football bet analysis skill that generates data-driven bet slips from form, head-to-head records, standings, injuries, and value analysis, with result tracking for hitrate and ROI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandichi](https://clawhub.ai/user/nandichi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to analyze football matches for betting picks, generate main and backup bet slips, record results, and review hitrate, ROI, and betting history. It is intended for advisory analysis and tracking, not automated bet placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external football match data and may rely on web lookups for news, injuries, odds, and weather, so analysis can be incomplete or outdated. <br>
Mitigation: Review the cited data and current match context before relying on picks, and keep the skill's honesty check and responsible gambling limits in place. <br>
Risk: The skill requires a football-data.org API key and can read it from configuration. <br>
Mitigation: Prefer the FOOTBALL_DATA_API_KEY environment variable, avoid committing keys to config files, and rotate the key if it is exposed. <br>
Risk: The skill stores local betting slips, stakes, results, ROI, and history. <br>
Mitigation: Confirm before saving slips and periodically delete local betting data if retained history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nandichi/football-value-bets) <br>
- [football-data.org API](https://api.football-data.org/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with tables and inline shell commands; helper scripts emit JSON for match data, saved bets, statistics, and history.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON betting-history files under the skill data directory when saving slips or results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
