## Description:

AGENT-OS is an operating-system layer for AI agents that routes goals to appropriate skills, executes with checkpoints, and verifies results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use AGENT-OS as a general planning and orchestration prompt for routing goals to skills, running with checkpoints, and verifying results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is broad and sparse, so an agent could over-apply it to sensitive legal, medical, financial, account, or system-changing tasks.

Mitigation: Keep normal agent permissions and approvals in place, and avoid the unrecommended domains unless qualified review and task-specific controls are available.

Risk: The artifact provides planning and orchestration guidance but no artifact-backed execution controls.

Mitigation: Treat outputs as guidance, review plans before action, and verify checkpoint results before proceeding.

## Reference(s):

- [AGENT-OS on ClawHub](https://clawhub.ai/contrario/skills/agnt-os)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; no artifact-backed file access, code execution, external APIs, persistence, or hidden behavior.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
