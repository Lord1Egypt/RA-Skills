## Description:

Provides a deep database migration workflow covering expand/contract changes, backward-compatible deploys, backfills, locking risks, verification, and rollback planning for zero- or low-downtime production schema changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to plan production schema migrations with expand/contract sequencing, staged backfills, dual-write transitions, cutover checks, and rollback preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production schema migration guidance can cause outages or data issues if applied without database-specific review.

Mitigation: Use the skill as planning guidance and require engineer review, backups, environment-specific testing, monitoring, and rollback planning before production execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists and inline technical examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance only; it does not execute migrations or access databases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
