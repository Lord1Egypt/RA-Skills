## Description: <br>
CRUD categorizes OpenClaw operations by create, read, update, and delete so agents can run read operations directly while requiring secondary confirmation for file-changing actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UyNewNas](https://clawhub.ai/user/UyNewNas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to make routine read, search, and list operations fast while requiring an explicit confirmation step before creating, editing, or deleting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read, search, and list operations can run without a second approval prompt. <br>
Mitigation: Install only in environments where direct read access is acceptable, and rely on workspace permissions for sensitive files. <br>
Risk: The documented uninstall command removes the local skill directory recursively. <br>
Mitigation: Verify the target path before running the removal command. <br>
Risk: The confirmation workflow depends on the agent following the skill's instructions before file-changing actions. <br>
Mitigation: Review the action list before confirming create, update, edit, or delete operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/UyNewNas/crud) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with action-list templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations are intended to proceed directly; create, update, edit, and delete operations are intended to produce a confirmation list before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
