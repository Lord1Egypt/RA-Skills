## Description: <br>
Query and monitor 5E CS2 player stats and match performance in real time with customizable player lists and detailed match analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddeellttaa](https://clawhub.ai/user/ddeellttaa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Players, analysts, and developers use this skill to query recent 5E CS2 match history, monitor selected players for new matches, and review detailed per-match performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried player names are sent to 5E services. <br>
Mitigation: Use the skill only when sharing those player names with 5E is acceptable. <br>
Risk: Continuous monitoring can keep polling in a background tmux session. <br>
Mitigation: Start monitoring deliberately and stop the tmux session when monitoring is no longer needed. <br>
Risk: Future use of login cookies could expose account credentials if placed in commands or configuration. <br>
Mitigation: Do not add login cookies to commands or config unless a future version documents safe handling. <br>
Risk: The 5E API returns only the last 5 matches, so reports may omit older history. <br>
Mitigation: Treat reports as recent-match summaries rather than complete season or historical analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ddeellttaa/cs2-stats-monitor-5e) <br>
- [5E Arena player search API](https://arena.5eplay.com/api/search/player/1/16) <br>
- [5E match data API](https://gate.5eplay.com/crane/http/api/data/player_match?uuid={uuid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include recent match statistics, scoreboard summaries, monitoring status, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
