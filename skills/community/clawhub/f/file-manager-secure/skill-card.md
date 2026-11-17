## Description:

Safe file operations with validation, dry-run previews, recoverable trash deletion, batch confirmation, and operation logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houssameddinemaatallah](https://clawhub.ai/user/houssameddinemaatallah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan and perform file listing, search, copy, move, delete, and restore workflows with safer defaults than direct shell file commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promised file safety controls may be bypassed, allowing moves or restores outside the intended workspace.

Mitigation: Review before installation and restrict use to non-critical workspaces until restore destinations and delete-confirm execution paths are revalidated against the workspace boundary.

Risk: Execution may not be bound to the dry-run plan that the user reviewed.

Mitigation: Require execution commands to consume a trusted current plan or recompute validation immediately before performing file operations.

Risk: Bulk or large operations may exceed the documented safety expectations.

Mitigation: Enforce operation-count and total-size limits before execution and require explicit confirmation for bulk actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houssameddinemaatallah/skills/file-manager-secure)
- [Publisher profile](https://clawhub.ai/user/houssameddinemaatallah)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, plus JSON output from helper script operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation plans are intended for user review before execution; script commands may create logs, trash metadata, backups, or moved/copied files inside the configured workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
