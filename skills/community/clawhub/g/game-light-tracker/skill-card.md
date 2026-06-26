## Description: <br>
Track live NFL, NBA, NHL, or MLB games and automatically change Hue light colors based on which team is leading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xadamsu](https://clawhub.ai/user/0xadamsu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and smart-home hobbyists use this skill to configure an agent to monitor live sports scores and control Hue lights through Home Assistant based on the leading team. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to use a Home Assistant token and control smart lights. <br>
Mitigation: Use a least-privilege Home Assistant token, confirm the exact light entity before execution, and store credentials only in the expected local configuration file. <br>
Risk: The evidence references PowerShell scripts that were not included in the artifact. <br>
Mitigation: Review or obtain the actual game-tracker.ps1 and keeper.ps1 scripts before running the tracker. <br>
Risk: The described keeper launches a hidden auto-restarting process and the stop command broadly force-stops matching PowerShell processes. <br>
Mitigation: Avoid hidden background launch unless explicitly desired and prefer stopping only the process IDs started for this tracker. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xadamsu/game-light-tracker) <br>
- [ESPN NFL teams](https://www.espn.com/nfl/teams) <br>
- [ESPN NBA teams](https://www.espn.com/nba/teams) <br>
- [ESPN NHL teams](https://www.espn.com/nhl/teams) <br>
- [ESPN MLB teams](https://www.espn.com/mlb/teams) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with PowerShell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include team abbreviations, RGB color values, Home Assistant light entity IDs, and tracker start or stop commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
