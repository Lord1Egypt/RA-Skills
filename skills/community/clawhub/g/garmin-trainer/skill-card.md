## Description: <br>
Generates adaptive 12-week training plans from Garmin Connect data, creates structured workouts, and schedules them on a user's Garmin calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bpauli](https://clawhub.ai/user/bpauli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Garmin users use this skill to generate or refresh a 12-week training calendar based on Garmin Connect events, recent activities, fitness metrics, and recovery signals. It helps create structured running, cycling, strength, and mobility workouts and schedule them to the user's Garmin calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read detailed Garmin fitness, health, recovery, activity, event, and schedule data. <br>
Mitigation: Run it only after user consent, request only the Garmin data needed for the plan, and avoid exposing raw health or training exports in shared outputs. <br>
Risk: The skill can create, reschedule, and force-delete future Garmin workouts, and W-prefixed workout names may not reliably prove the skill created them. <br>
Mitigation: Require a preview and explicit user approval before workout creation, rescheduling, or deletion, and verify each W-prefixed scheduled workout before removal. <br>


## Reference(s): <br>
- [gccli Command Reference](references/gccli-commands.md) <br>
- [gccli source repository](https://github.com/bpauli/gccli) <br>
- [Garmin Trainer on ClawHub](https://clawhub.ai/bpauli/garmin-trainer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown training plan summaries with gccli shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, schedule, or remove Garmin workouts through gccli when the user approves those actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
