## Description: <br>
Helps agents diagnose scheduled-job incidents by separating trigger failures from execution failures and grounding conclusions in run history, logs, authorization state, and recovery checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate cron and scheduled-job incidents, distinguish missing triggers from failed executions, and write evidence-backed incident conclusions. It also supports post-repair regression checks for OpenClaw-style scheduled task workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual verification of scheduled jobs can trigger production tasks or send real test notifications. <br>
Mitigation: Confirm the cron schedule, destination chat, message payload, and whether a real test notification is acceptable before approving verification runs. <br>
Risk: Incident conclusions can be misleading if process status is treated as proof that scheduled jobs recovered. <br>
Mitigation: Require run history, execution status, delivery or output evidence, and remaining error checks before declaring recovery. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown guidance with diagnostic steps, incident conclusion templates, and recovery validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include example error codes, log evidence summaries, task status checks, and recommended follow-up validation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
