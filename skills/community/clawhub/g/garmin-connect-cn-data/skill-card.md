## Description: <br>
Queries Garmin Connect CN personal health and activity data, including sleep, HRV, training metrics, activity details, and FIT, GPX, TCX, or CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xent9312](https://clawhub.ai/user/xent9312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents with access to a Garmin Connect CN account use this skill to retrieve personal health summaries, sleep and HRV metrics, activity details, running analysis, and activity exports for review or further analysis. <br>

### Deployment Geography for Use: <br>
Global; intended for Garmin Connect CN accounts. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Garmin Connect CN health, activity, and location-linked data. <br>
Mitigation: Use it only when the user explicitly wants Garmin account access, confirm before querying sensitive metrics, and keep exported activity files private. <br>
Risk: Login stores Garmin credentials on the local machine. <br>
Mitigation: Avoid entering passwords on shared machines or in logged shells, and remove ~/.config/garmin-cn/credentials.json after use when credentials should not persist. <br>
Risk: Broad activation guidance could lead an agent to query Garmin data for a general health or fitness request. <br>
Mitigation: Confirm user intent before running commands that access or export account data. <br>


## Reference(s): <br>
- [Advanced Usage](references/advanced-usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xent9312/garmin-connect-cn-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; invoked scripts return JSON and can export activity files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Garmin credential configuration and FIT, GPX, TCX, or CSV activity export files when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
