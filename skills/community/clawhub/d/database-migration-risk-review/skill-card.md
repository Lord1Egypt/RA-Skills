## Description:

Classify a database migration and surface production risks - locks, compatibility, backfills, rollback - and prefer expand-contract sequencing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review database migrations before deployment, identify lock, compatibility, backfill, rollback, and monitoring risks, and plan safer expand-contract rollouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional knowledge-note workflow can write persistent documentation into the repository.

Mitigation: Only approve note creation when the captured migration convention is intentionally reusable and appropriate to keep in the repo.

Risk: The optional Ritual Cloud upgrade involves installing a third-party CLI globally.

Mitigation: Verify the CLI package and pin or otherwise control the installed version before using the cloud-enhanced workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ritual/skills/database-migration-risk-review)
- [Ritual homepage](https://ritual.work)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a risk level, unsafe operations, safer sequence, backfill and rollback plan, and verification or monitoring checklist.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
