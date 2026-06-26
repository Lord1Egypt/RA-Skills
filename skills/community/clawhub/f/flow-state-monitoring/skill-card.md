## Description: <br>
Workflow-driven skill that infers deep focus and autonomously mutes interruptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to infer when local activity indicates deep focus and create Google Calendar busy blocks that reduce interruptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create Google Calendar availability blocks automatically based on vague local focus telemetry. <br>
Mitigation: Review the local signals, deep-focus trigger, gog permissions, and calendar deletion process before enabling the skill. <br>
Risk: Misclassification of activity could block interruptions when the user is not actually in deep work. <br>
Mitigation: Verify classification results and keep the built-in retry and stop-on-failure behavior active. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zvirb/flow-state-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, API Calls] <br>
**Output Format:** [JSON confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog command-line tool and Google Calendar permissions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
