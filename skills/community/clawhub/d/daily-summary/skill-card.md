## Description: <br>
Generates a daily learning summary with date, achievements, task status, plans, and token usage statistics from OpenClaw status data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can trigger this skill to create a dated daily summary of accomplishments, task status, plans, and token usage. It is useful for maintaining a lightweight daily work log in the user's workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes or updates a dated summary file in the user's OpenClaw workspace. <br>
Mitigation: Check whether memory/YYYY-MM-DD.md already contains notes that should be preserved, and review the generated summary before relying on it. <br>
Risk: The release references separate cron_daily_summary.py automation that is not included in the artifact. <br>
Mitigation: Inspect that automation before running any scheduled or automated workflow that uses this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/daily-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown summary file with a brief text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates memory/YYYY-MM-DD.md under the user's OpenClaw workspace when used as documented.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
