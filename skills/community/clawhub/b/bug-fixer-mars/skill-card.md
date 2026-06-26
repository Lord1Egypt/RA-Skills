## Description: <br>
Autonomous bug diagnosis and repair. Use when user reports a bug, error, or unexpected behavior in code or systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose reported bugs, classify common error types, choose repair strategies, and record verification results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed automatic monitoring that can process recent pitfall files when the script is run with no arguments. <br>
Mitigation: Review the script before installation and run it with explicit arguments unless monitor-mode processing is intended. <br>
Risk: The security review reports that repair details may be sent through a Feishu messaging integration without confirmation. <br>
Mitigation: Disable or remove the Feishu notification block before use in workspaces containing sensitive code, logs, or incident details. <br>
Risk: The security guidance notes persistent logs under ~/.openclaw. <br>
Mitigation: Use the skill only in non-sensitive workspaces unless persistent local logging is acceptable, and review or clear generated logs according to local policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mars82311111/bug-fixer-mars) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown repair records, log text, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write logs and fix records under the user's .openclaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
