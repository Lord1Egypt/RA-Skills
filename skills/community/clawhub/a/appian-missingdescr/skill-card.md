## Description: <br>
Audit Appian application objects for missing descriptions. Given an application UUID, reports every object whose description field is empty or absent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Appian administrators use this skill to audit an Appian application by UUID and identify objects with empty or absent description fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a user-configured local Node runner through APPIAN_RUNNER. <br>
Mitigation: Confirm APPIAN_RUNNER points to a trusted local script before use. <br>
Risk: The skill connects to the Appian environment named by APPIAN_PROC_URL and prints full audit output. <br>
Mitigation: Verify APPIAN_PROC_URL targets the intended environment and use the skill only for Appian applications you are authorized to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solarspiker/appian-missingdescr) <br>
- [Publisher profile](https://clawhub.ai/user/solarspiker) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Markdown with inline shell command and verbatim command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_PROC_URL, APPIAN_RUNNER, and the node binary; the skill reports the runner output without summarizing or omitting lines.] <br>

## Skill Version(s): <br>
1.5.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
