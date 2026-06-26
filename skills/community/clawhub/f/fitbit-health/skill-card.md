## Description: <br>
Query Fitbit health data (activity, sleep, heart rate, weight) via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pb3975](https://clawhub.ai/user/pb3975) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an agent retrieve Fitbit profile, activity, steps, calories, heart-rate, and daily summary data after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive Fitbit health data, including activity, heart-rate, sleep, weight, and profile scopes. <br>
Mitigation: Install and authorize it only in conversations where Fitbit health details may safely appear, and review the Fitbit consent screen before approving access. <br>
Risk: OAuth tokens are stored locally for the CLI. <br>
Mitigation: Keep the local token file private, and run `fitbit logout` or revoke the app in Fitbit when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pb3975/fitbit-health) <br>
- [Publisher profile](https://clawhub.ai/user/pb3975) <br>
- [Fitbit developer app registration](https://dev.fitbit.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [CLI text output or JSON from Fitbit data commands, with setup and authentication commands in shell form.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the fitbit CLI, a Fitbit app client ID, OAuth consent, and local token storage.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
