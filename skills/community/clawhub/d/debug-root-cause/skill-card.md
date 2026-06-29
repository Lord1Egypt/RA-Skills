## Description: <br>
Debug Root Cause guides agents through systematic root-cause analysis for tool errors, unexpected results, repeated failures, and user-requested debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maochen1980](https://clawhub.ai/user/maochen1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to define debugging problems, select appropriate root-cause analysis methods, record investigation notes, and verify whether a fix resolved the issue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly on failure language or unexpected results. <br>
Mitigation: Confirm the debugging problem and skip the workflow when the error already points to a clear fix. <br>
Risk: The workflow writes local scratch notes that could capture sensitive debugging context. <br>
Mitigation: Avoid placing secrets or production data in debug notes, and review or remove notes after use. <br>
Risk: The workflow can direct the agent toward skill self-repair after multiple unresolved approaches. <br>
Mitigation: Require explicit user confirmation before using skill-manager or modifying any skill. <br>


## Reference(s): <br>
- [RCA Methods Reference](references/rca-methods.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maochen1980/debug-root-cause) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown notes and step-by-step debugging guidance, often with shell commands for investigation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local scratch notes during debugging; review notes before retaining or sharing them.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
