## Description:

Provides a five-stage infrastructure auto-healing workflow for detection intake, diagnosis, repair, verification, regression checks, and healing history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure and platform engineers use this skill to diagnose faults, preview or execute repair playbooks, verify recovery, run regression checks, and inspect auto-healing history for operational systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically run high-impact infrastructure repair actions.

Mitigation: Install it only in approved infrastructure environments, review the playbook and MCP implementation first, and begin with diagnosis-only or dry-run use.

Risk: Unattended repairs may affect unintended targets if target scope is too broad.

Mitigation: Require explicit target allowlists and confirmation before enabling unattended repair actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/auto-healing-manager)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call infrastructure repair, verification, regression, history, and healthcheck actions through the bundled Python command wrapper.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
