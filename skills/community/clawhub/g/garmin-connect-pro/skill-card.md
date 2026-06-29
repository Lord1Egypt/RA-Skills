## Description: <br>
Garmin Connect Pro helps agents retrieve Garmin Connect activity, sleep, heart rate, stress, body battery, training readiness, VO2 max, race prediction, and activity export data through a Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drpeterkalmar](https://clawhub.ai/user/drpeterkalmar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query Garmin Connect fitness and health data, generate summaries and trend views, export activity data, and automate recurring fitness reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Garmin health, activity, profile, device, and possibly location data. <br>
Mitigation: Install only when that access is acceptable, use the minimum commands needed, and avoid broad JSON exports unless required. <br>
Risk: Credentials and OAuth tokens may be stored locally, including a plaintext credentials fallback. <br>
Mitigation: Prefer environment variables or a system secret store, keep credential and token files protected, and remove saved tokens when use ends. <br>
Risk: Scheduled jobs that run with Garmin credentials can increase exposure. <br>
Mitigation: Use protected environment variables for automation, review cron jobs periodically, and remove them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drpeterkalmar/garmin-connect-pro) <br>
- [garminconnect Python library](https://github.com/cyberjunkie/garminconnect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Plain text CLI responses with ASCII charts, JSON exports, shell commands, and downloaded FIT or GPX activity files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Garmin Connect account, python3, and garminconnect>=0.2.38.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
