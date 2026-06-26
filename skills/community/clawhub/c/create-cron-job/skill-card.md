## Description: <br>
Create and configure OpenClaw cron jobs with correct scheduling, execution modes, and delivery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kjvarga](https://clawhub.ai/user/kjvarga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to define OpenClaw scheduled jobs, including recurring tasks, one-shot reminders, execution mode, delivery mode, and post-creation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can persist and run later with the selected agent, session mode, delivery target, or webhook. <br>
Mitigation: Confirm the schedule, target agent, session mode, delivery target, webhook URL if used, and one-shot versus recurring behavior before adding or testing a job. <br>
Risk: Outdated or unnecessary cron jobs can continue running after they are no longer needed. <br>
Mitigation: Periodically review existing cron jobs and delete old jobs that should no longer run. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces human-readable setup steps and command examples for OpenClaw cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
