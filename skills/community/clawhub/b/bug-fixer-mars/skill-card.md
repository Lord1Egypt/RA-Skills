## Description:

Autonomous bug diagnosis and repair. Use when user reports a bug, error, or unexpected behavior in code or systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose reported code or system bugs, choose a repair strategy, record the repair process, and validate whether the issue was resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill can quietly run a separate Feishu messaging script and pass repair details if that sibling integration exists.

Mitigation: Review the skill before installing, confirm whether the sibling messaging integration is trusted, and disable or remove that integration when repair details should not be sent externally.

Risk: The security evidence reports that the skill may create records in the OpenClaw home workspace.

Mitigation: Run it only in an acceptable workspace and review generated logs and repair records before sharing or retaining them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and shell-command oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local repair records and logs in the user's OpenClaw home workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
