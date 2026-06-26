## Description: <br>
Structured burnout recovery protocol based on clinical burnout dimensions for users who are exhausted, cynical about work, feel ineffective, cannot disconnect, or say they are burned out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to assess burnout severity, set boundaries, run energy audits, plan recovery activities, and identify when professional or crisis support may be needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to persist sensitive burnout assessments, work boundaries, recovery notes, and reflections across sessions. <br>
Mitigation: Ask for explicit consent before saving files or state, offer session-only use, and provide deletion steps for reminders, notes, and stored state. <br>
Risk: The skill can write a local boundary-scripts file and create recovery reminders or check-ins. <br>
Mitigation: Confirm file paths, reminder cadence, and calendar or filesystem actions with the user before executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howtousehumans/burnout-recovery) <br>
- [Gerber et al., Aerobic exercise training and burnout](https://doi.org/10.1186/1756-0500-6-78) <br>
- [988 Suicide & Crisis Lifeline](https://988lifeline.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with assessment questions, scripts, recovery plans, reminders, and saved-note instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create reminders, persist recovery state, and write local boundary-script notes when the host agent provides calendar or filesystem tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
