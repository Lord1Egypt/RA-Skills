## Description: <br>
Generates an executive daily brief from Aicoo context, then derives top strategies and an Eisenhower matrix view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and assistants use this skill to generate a concise Aicoo daily briefing, identify top strategic priorities, and present Eisenhower matrix highlights for follow-up action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive calendar, note, task, and email-summary data through Aicoo. <br>
Mitigation: Install only for Aicoo daily briefing workflows and confirm users are comfortable with Aicoo processing those summaries. <br>
Risk: Recurring runs or saved briefing notes can repeatedly process or retain sensitive briefing context. <br>
Mitigation: Enable cron, /loop, /routine, or PULSE_BRIEF_SAVE_NOTE only when recurring execution or saved notes are intended. <br>
Risk: The skill requires the AICOO_API_KEY credential. <br>
Mitigation: Provide the credential only in trusted environments and review commands before execution. <br>


## Reference(s): <br>
- [Aicoo API Base URL](https://www.aicoo.io/api/v1) <br>
- [Aicoo Daily Brief on ClawHub](https://clawhub.ai/xisen-w/aicoo-daily-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Concise Markdown with optional bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICOO_API_KEY and may use recurring automation or saved notes when the user enables those options.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
