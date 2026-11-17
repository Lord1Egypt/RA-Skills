## Description:

Write safe, zero-downtime database migration plans for schema changes, including compatibility analysis, expand/contract phases, SQL, validation, rollback steps, and a deployment runbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to plan database schema migrations that preserve availability, compatibility, data integrity, and rollback options across deployment phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL examples may contain safety or correctness issues that could disrupt a production migration if copied directly.

Mitigation: Require DBA review, staging tests against production-scale data, and database-engine-specific correction before execution.

Risk: Concurrent indexes, backfills, rollback steps, and destructive contract phases can create production risk if the plan is followed without adaptation.

Mitigation: Treat generated SQL as a planning template and verify lock behavior, batch strategy, rollback windows, and destructive steps for the target database and deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/database-migration-plan)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/database-migration-plan.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with SQL and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured migration plan with phase-by-phase rollout, validation, rollback, and runbook sections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
