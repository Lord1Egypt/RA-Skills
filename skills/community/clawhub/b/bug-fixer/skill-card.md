## Description: <br>
Autonomous bug diagnosis and repair. Use when user reports a bug, error, or unexpected behavior in code or systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to triage reported bugs, classify common error types, record root-cause notes, suggest repair actions, and verify whether the issue appears resolved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send repair status through an existing Feishu helper without clear user-facing disclosure or consent. <br>
Mitigation: Review or disable the Feishu helper path before use, and test the skill first in a workspace without sensitive error logs. <br>
Risk: The skill writes repair logs under ~/.openclaw, which may retain excerpts of error reports or paths. <br>
Mitigation: Run it with non-sensitive inputs first and review generated logs before using it on private projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mars82311111/bug-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown repair records and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes repair logs under ~/.openclaw and may call a configured Feishu helper for repair notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
