## Description: <br>
Rebuild and maintain garmin_tracking.json from Garmin web data (activities + training plan) with a fixed schema from 2026-02-01. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardotrevisan](https://clawhub.ai/user/ricardotrevisan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Garmin users and agents use this skill to sync, rebuild, and validate a workspace garmin_tracking.json file from Garmin activities and training-plan data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated Garmin browser session and has a password-based fallback mode. <br>
Mitigation: Prefer a logged-in or manually signed-in browser session; use credentials mode only in trusted environments and never write or echo credentials. <br>
Risk: The sync and reconciliation scripts can update garmin_tracking.json. <br>
Mitigation: Run without write mode first to inspect results, then use write mode only after confirming the target file and Garmin session are correct. <br>
Risk: Debug dumps may contain Garmin page data from the authenticated session. <br>
Mitigation: Avoid debug dumps unless needed for troubleshooting and handle any generated dumps as sensitive data. <br>
Risk: Runtime behavior depends on node, python3, playwright-core, and access to the configured browser CDP endpoint. <br>
Mitigation: Provision the required binaries, pin playwright-core in managed environments, and configure the CDP endpoint explicitly when defaults are not appropriate. <br>


## Reference(s): <br>
- [ClawHub Garmin Tracker skill page](https://clawhub.ai/ricardotrevisan/garmin-tracker) <br>
- [Garmin Connect sign-in](https://connect.garmin.com/signin/) <br>
- [Garmin Connect training plan](https://connect.garmin.com/app/training-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update garmin_tracking.json when run with write mode; otherwise reports parsed sync or reconciliation results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
