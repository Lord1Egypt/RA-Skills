## Description: <br>
Garmin Connect CLI for activities, health, body composition, workouts, devices, gear, goals, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bpauli](https://clawhub.ai/user/bpauli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate `gccli` for Garmin Connect account setup, health and activity queries, data export, workout/course management, and related fitness workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help access sensitive Garmin Connect health data and account tokens. <br>
Mitigation: Treat `gccli auth token` and `gccli auth export` output like passwords; do not paste tokens into chats, logs, repositories, or unsecured files. <br>
Risk: Some commands can create, upload, rename, retype, link, unlink, schedule, send, or delete Garmin data. <br>
Mitigation: Require explicit user confirmation before running commands that modify Garmin Connect data or devices. <br>
Risk: Agent-selected strength exercise mappings may be incorrect when converting free text into Garmin catalog entries. <br>
Mitigation: Show the proposed Garmin CATEGORY/EXERCISE_NAME mapping and wait for user confirmation before creating the activity or setting exercise sets. <br>


## Reference(s): <br>
- [Garmin Connect CLI homepage](https://github.com/bpauli/gccli) <br>
- [ClawHub skill page](https://clawhub.ai/bpauli/garmin-connect-cli) <br>
- [Publisher profile](https://clawhub.ai/user/bpauli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce human-readable tables, JSON, TSV, and downloaded activity files depending on the selected gccli flags.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
