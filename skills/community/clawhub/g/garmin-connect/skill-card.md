## Description: <br>
Garmin Connect integration for Clawdbot: sync fitness data (steps, HR, calories, workouts, sleep) every 5 minutes using OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rayleigh3105](https://clawhub.ai/user/Rayleigh3105) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to authenticate with Garmin Connect, sync activity, sleep, and workout data to a local cache, and format that data for Clawdbot scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Garmin credentials, OAuth tokens, and sensitive health data. <br>
Mitigation: Use it only on a trusted single-user machine and protect ~/.garth/session.json and Garmin cache files as sensitive credential and health data. <br>
Risk: The authentication flow may pass a Garmin password on the command line. <br>
Mitigation: Modify the authentication script to prompt securely or use another protected secret-entry method before regular use. <br>
Risk: The cron wrapper includes /tmp logging and developer-specific paths or emails. <br>
Mitigation: Remove or change /tmp logging, replace hard-coded local paths and emails, and enable the five-minute cron job only when continuous syncing is intended. <br>


## Reference(s): <br>
- [ClawHub Garmin Connect skill page](https://clawhub.ai/Rayleigh3105/garmin-connect) <br>
- [Clawdbot](https://clawd.bot) <br>
- [Garmin SSO sign-in](https://sso.garmin.com/sso/signin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown/text guidance with Python and shell command snippets; sync scripts emit JSON data and cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Garmin OAuth session and local Garmin cache files; optional cron configuration controls repeated syncing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
