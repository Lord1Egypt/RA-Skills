## Description: <br>
Safe, zero-downtime database migration strategies - schema evolution, rollback planning, data migration, tooling, and anti-pattern avoidance for production systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, write, and review safe database migrations for production systems, including schema changes, data backfills, rollback plans, and migration CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying migration guidance directly to production data can cause downtime, data loss, or irreversible schema changes. <br>
Mitigation: Use dry runs, production-like staging data, backups, rollback planning, and explicit approval before making real database changes. <br>
Risk: Generated SQL, shell commands, or migration steps may not match the target database engine, ORM, deployment order, or operational constraints. <br>
Mitigation: Review and adapt all guidance for the specific stack, benchmark lock impact, and validate the plan in CI or staging before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, checklists, SQL examples, and inline shell or CI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; does not automatically access databases or execute migrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
