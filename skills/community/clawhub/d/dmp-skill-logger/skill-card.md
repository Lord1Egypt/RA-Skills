## Description: <br>
Records and queries cross-platform task history for Mingri DMP skills using a shared local history file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to record, inspect, and audit task history across Mingri DMP workflows, including task parameters, execution steps, status, result data, and platform information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detailed task histories may include sensitive parameters, customer identifiers, proprietary audience definitions, or credentials. <br>
Mitigation: Avoid logging sensitive values and use an isolated, access-controlled storage path with a clear cleanup process. <br>
Risk: Shared local storage can make task history visible across conversations or users in shared environments. <br>
Mitigation: Use the skill only where cross-session sharing is intended, and prefer workspace-specific storage for shared or multi-user systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mingri26/dmp-skill-logger) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON records and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and queries local task-history records, commonly in .skill-logger/task_history.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
