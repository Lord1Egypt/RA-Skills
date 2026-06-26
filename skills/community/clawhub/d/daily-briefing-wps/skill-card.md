## Description: <br>
Generates and sends a daily morning briefing that summarizes project progress, pending work items, and optional WPS calendar events from local memory logs and related work context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwanxia](https://clawhub.ai/user/wangwanxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and project operators use this skill to receive a concise daily status briefing from work notes, pending tags, project progress entries, and optional calendar events. It is intended for scheduled morning check-ins or user-requested project status summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private work notes and calendar context on a schedule. <br>
Mitigation: Install only when the daily briefing is intentional, verify which files and services it can read, and limit access to the minimum required context. <br>
Risk: The skill may send sensitive project details without a clear preview or consent step. <br>
Mitigation: Require preview or confirmation before sending briefings that include sensitive project status, pending items, or calendar information. <br>
Risk: Broad trigger phrases could cause unplanned status summaries. <br>
Mitigation: Narrow the trigger phrases and confirm the cron job is opt-in before enabling automated delivery. <br>


## Reference(s): <br>
- [Morning Briefing template](references/template.md) <br>
- [ClawHub skill page](https://clawhub.ai/wangwanxia/daily-briefing-wps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing text with optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The briefing is concise and may be sent automatically by a scheduled job.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
