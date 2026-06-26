## Description: <br>
Multi-source sports betting research tool that aggregates odds, team form, head-to-head history, weather conditions, and injury data to identify value betting opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research sports matches and teams before making betting decisions. It summarizes form, fixtures, head-to-head records, weather, odds, fatigue, motivation, and optional X/Twitter intelligence without claiming guaranteed outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Match and team names may be sent to sports-data, weather, odds, and X/Twitter search providers during research. <br>
Mitigation: Review provider usage before installation and avoid entering sensitive or private queries. <br>
Risk: The skill reads local API keys from documented configuration files and environment variables. <br>
Mitigation: Use least-privilege API keys, keep configuration files private, and rotate keys if exposure is suspected. <br>
Risk: When a local search-x skill is present, the skill can execute it for X/Twitter intelligence that is not clearly bounded by this artifact. <br>
Mitigation: Remove or disable the search-x calls unless that local skill and its API-key handling are trusted. <br>
Risk: Sports betting analysis can be incomplete, stale, or misleading and should not be treated as a guaranteed prediction. <br>
Mitigation: Use the output as research context only and independently verify injuries, lineups, odds, and local betting compliance before acting. <br>


## Reference(s): <br>
- [Data Sources Reference](references/data-sources.md) <br>
- [TheSportsDB](https://www.thesportsdb.com/) <br>
- [API-Football](https://www.api-football.com/) <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/stigg86/betting-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal-oriented text and markdown-style betting research summaries with setup commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external sports, weather, odds, and optional X/Twitter search services; outputs are research signals, not betting guarantees.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
