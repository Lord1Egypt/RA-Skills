## Description:

Edit explicitly selected Calibre book metadata through a saved dry-run plan, stale-target checks, apply receipts, and readback verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Calibre users and their agents use this skill to review and apply explicitly authorized book metadata changes, including titles, authors, series, tags, dates, languages, and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect target or unreviewed proposal could change the wrong book's metadata.

Mitigation: Configure the intended Calibre library and review each target, current value, and proposed change in the dry-run plan before applying it.

Risk: A failed or concurrent update may leave some books changed and others unchanged.

Mitigation: Keep apply receipts, reconcile them against current metadata after failures, and create a fresh plan rather than blindly retrying.

Risk: Content-server access requires credentials and can modify remote metadata.

Mitigation: Install only for trusted agents, scope the connection to the intended endpoint, and supply credentials through the documented environment variable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nextaltair/skills/calibre-metadata-apply)
- [JSONL change examples](artifact/references/changes.example.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Text guidance with JSON plans and JSONL apply receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved dry-run plans and per-attempt receipts support review and reconciliation.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
