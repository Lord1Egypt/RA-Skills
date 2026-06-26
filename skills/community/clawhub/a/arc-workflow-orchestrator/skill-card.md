## Description: <br>
Chain skills into automated pipelines with conditional logic, error handling, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trypto1019](https://clawhub.ai/user/Trypto1019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to define, validate, dry-run, and execute multi-step agent workflows from YAML or JSON files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow files can run broad local commands hands-free. <br>
Mitigation: Review workflow files as executable code, use validate and dry-run first, and avoid workflows from untrusted sources. <br>
Risk: Sensitive values may be exposed through command lines or saved output. <br>
Mitigation: Do not place secrets in workflow commands or saved outputs. <br>
Risk: Rollback handling has weak safety boundaries. <br>
Mitigation: Do not rely on rollback unless explicit reversal steps are implemented and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/Trypto1019/arc-workflow-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and YAML or JSON workflow definitions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports validation and dry-run output before workflow execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
