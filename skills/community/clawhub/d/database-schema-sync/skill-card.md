## Description: <br>
Guides agents to manage database schema changes with an idempotent sync script, dry-run review, and verification instead of direct Alembic production migrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide database schema updates across development, staging, and production with dry-run review, explicit apply steps, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides high-impact production database changes. <br>
Mitigation: Require human approval of dry-run output, backups, rollback plan, maintenance timing, and database credentials before any production apply step. <br>
Risk: The workflow relies on an unreviewed local sync-production-schema.py script. <br>
Mitigation: Inspect and test the actual sync script in the intended project, verify required helpers exist, and use least-privileged database credentials. <br>


## Reference(s): <br>
- [Schema Sync Script vs Alembic Migrations](references/sync-vs-alembic.md) <br>
- [Schema Sync Workflow Examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes dry-run review before apply, environment sequencing, and verification after schema changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
