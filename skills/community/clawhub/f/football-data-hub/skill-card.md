## Description: <br>
Football Data Hub helps agents query football standings, fixtures, results, team and player data, and H2H match previews without sports-betting predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve football league tables, schedules, match results, team lookup data, player data, and pre-match H2H summaries from public or configured football data APIs. It is intended for informational football data lookup, not betting prediction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries external football APIs and may store optional API keys in a local config.yaml. <br>
Mitigation: Install only if external API access is acceptable, keep API keys out of shared logs and repositories, and use reviewed local configuration practices. <br>
Risk: Dependency hygiene issues could affect reliability or supply-chain review. <br>
Mitigation: Pin reviewed versions of requests and pyyaml before deployment. <br>
Risk: The H2H preview has known import and win-counting accuracy issues in the provided security guidance. <br>
Mitigation: Do not rely on H2H preview output for decisions until those bugs are fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bettermen/football-data-hub) <br>
- [OpenLigaDB API](https://api.openligadb.de/) <br>
- [API-Football on RapidAPI](https://rapidapi.com/api-sports/api/api-football) <br>
- [football-data.org API](https://api.football-data.org/v4) <br>
- [League mapping reference](references/leagues.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration notes, and text or tabular football data summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query external football APIs; optional API keys are read from local configuration when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
