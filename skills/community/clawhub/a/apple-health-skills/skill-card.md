## Description: <br>
Use this skill when the user asks for Apple Health summaries, trends, alerts, or check-ins from the local collector. Validate collector connectivity over HTTP and fetch fresh data with shell commands before giving coaching-style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajde0606](https://clawhub.ai/user/ajde0606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to query local Apple Health, live heart-rate, and Whoop-style wearable data, then receive concise summaries, trends, alerts, and coaching-style guidance grounded in recent measurements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and displays sensitive local health, live heart-rate, and wearable data. <br>
Mitigation: Keep query windows narrow, protect .env and database files, and avoid sharing transcripts or logs that contain health metrics. <br>
Risk: Whoop setup and sync guidance may involve credentials, tokens, scheduled syncs, and scripts that are not included in this artifact. <br>
Mitigation: Review the referenced setup and sync scripts, token storage, and data destination before running Whoop authorization, sync, or cron steps. <br>
Risk: Coaching-style summaries of health metrics can be mistaken for medical advice. <br>
Mitigation: Keep responses informational, tie suggestions to observed values, and recommend clinician contact for extreme or persistent readings. <br>


## Reference(s): <br>
- [Apple Health Query Skill](SKILL.md) <br>
- [Whoop Query Skill](WHOOP_SKILL.md) <br>
- [Whoop Developer Portal](https://developer.whoop.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown narrative with inline shell commands and JSON-derived metric summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounded in local SQLite query results and expected to include informational safety framing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
