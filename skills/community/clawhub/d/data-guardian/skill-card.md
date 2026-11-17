## Description:

Guardian is a safety gatekeeper for AI agents that checks destructive file, database, system, and external-write operations before execution, verifies backup status, and escalates risky actions for human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Guardian as a pre-flight or tool-layer safety gate for AI agents before destructive file, database, system, or external-write operations. It provides backup checks, proceed-or-halt decisions, and human escalation for higher-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guardian is advisory policy and should not be treated as a reliable enforcement layer.

Mitigation: Use it with an independent human approval path for high-risk deletes, overwrites, database changes, system changes, and external writes.

Risk: Backup-verification scripts can incorrectly approve destructive operations.

Mitigation: Confirm backup coverage and restoreability independently before allowing destructive operations to proceed.

## Reference(s):

- [Guardian ClawHub Skill Page](https://clawhub.ai/tooled-app/skills/data-guardian)
- [Guardian README](artifact/README.md)
- [Operation Taxonomy](artifact/OPERATION-TAXONOMY.md)
- [Decision Matrix](artifact/DECISION-MATRIX.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON]

**Output Format:** [Markdown/text escalation guidance plus JSON backup-verification results from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May halt or require human approval for destructive operations; backup checks are intended to complete quickly.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter reports 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
