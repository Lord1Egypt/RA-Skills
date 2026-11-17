## Description:

Guides agents through database schema management with an idempotent sync script, emphasizing dry-run review before applying schema changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to update, review, and verify database schema changes across development, staging, and production with a preview-first sync workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a production schema sync script that is not included in the artifact.

Mitigation: Use the skill only after reviewing and controlling the referenced sync-production-schema.py script, and require dry-run review plus explicit human approval before any production --apply step.

Risk: The verifier script uses a hard-coded local path and attempts to change file permissions.

Mitigation: Replace the hard-coded path with the local repository path and make verification read-only before installing or running the skill.

Risk: Production schema changes can cause data loss, downtime, or schema drift if applied with excessive privileges or without rollback planning.

Mitigation: Require backups, least-privileged database credentials, dev and staging validation, and post-apply schema verification before production rollout.

## Reference(s):

- [Schema Sync Script vs Alembic Migrations](artifact/references/sync-vs-alembic.md)
- [Schema Sync Workflow Examples](artifact/references/workflow-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/urbantech/skills/database-schema-sync)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, apply, verification, and CI/CD workflow guidance for a repository-provided schema sync script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
