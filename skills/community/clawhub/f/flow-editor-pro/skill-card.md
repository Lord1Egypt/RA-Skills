## Description:

Flow Editor Pro helps agents administer Node-RED instances through Admin API or CLI guidance for flow deployment, rollback, backups, node management, context persistence, diagnostics, and security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to administer Node-RED instances, manage flows across development, staging, and production, back up and restore state, and recover from failed deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to change live Node-RED workflow systems.

Mitigation: Restrict use to named dev, staging, and production instances, and require explicit confirmation before production deploy, delete, restore, rollback, context writes, node changes, Docker restarts, or scheduled backups.

Risk: Node-RED credentials and backup files may contain sensitive operational data.

Mitigation: Store credentials and backup files only in protected secret or encrypted storage and avoid committing them to public repositories.

Risk: Unclear activation boundaries and inconsistent execution guidance can lead to unintended administration actions.

Mitigation: Review the requested action, target instance, and command plan before execution, and prefer staging validation before production changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/flow-editor-pro)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, rollback steps, backup and restore commands, and JSON status examples.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
