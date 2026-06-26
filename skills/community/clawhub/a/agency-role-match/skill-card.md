## Description: <br>
Agency Role Match is a Chinese-language workflow that matches a user-described task to 2-3 suitable AI roles, waits for confirmation, and then loads the selected role's SOUL.md before producing work in that role. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzdongyifan-bit](https://clawhub.ai/user/wzdongyifan-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to choose an appropriate local agency role for a task before asking the agent to complete the work in that role's style and expertise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may activate on common role or workflow requests when that is not the user's intent. <br>
Mitigation: Ask the agent to stop the workflow or use a preferred language if the role-selection flow is not wanted. <br>
Risk: Role-specific output depends on local SOUL.md role definitions loaded after user selection. <br>
Mitigation: Review the local agency role definitions before deployment and before relying on outputs in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzdongyifan-bit/agency-role-match) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or structured text role recommendations and task outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations include 2-3 roles with reasons and require user confirmation before role-specific output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
