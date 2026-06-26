## Description: <br>
Query Fitbit health data including sleep, heart rate, activity, SpO2, and breathing rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Fitbit users use this skill to have an agent run read-only Fitbit CLI queries for sleep, heart rate, activity, SpO2, breathing rate, profile, and device status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitbit queries can expose sensitive personal health, profile, and device data in the agent session. <br>
Mitigation: Run only user-requested metrics, keep date ranges narrow, and avoid asking for data the user does not want shown in the conversation. <br>
Risk: The skill depends on an installed fitbit-cli binary that can access Fitbit account data. <br>
Mitigation: Use a trusted fitbit-cli installation and complete authentication intentionally before allowing the agent to query data. <br>


## Reference(s): <br>
- [Fitbit homepage](https://www.fitbit.com) <br>
- [Fitbit skill on ClawHub](https://clawhub.ai/mjrussell/fitbit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fitbit-cli for read-only Fitbit queries; date inputs may be today, relative ranges, or explicit dates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
