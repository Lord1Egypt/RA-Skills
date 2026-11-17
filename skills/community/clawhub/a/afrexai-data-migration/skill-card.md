## Description:

Plans and documents data migrations, including schema mapping, ETL pipeline design, validation tests, rollback strategies, and runbook creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Engineering teams, CTOs, consultants, and operations teams use this skill to plan migrations between systems, estimate scope and cost, and produce migration runbooks with schema mappings, ETL steps, validation checks, cutover gates, and rollback plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migration plans may omit environment-specific constraints, data dependencies, or compliance requirements.

Mitigation: Have qualified operators review the runbook, confirm privacy and compliance controls, and validate assumptions before execution.

Risk: Executing a migration plan without rehearsal can cause data loss, downtime, or incomplete rollback.

Mitigation: Run tests outside production first, verify backups, define go/no-go gates, and confirm rollback steps before cutover.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-data-migration)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured markdown runbook with tables, checklists, validation queries, timeline estimates, and rollback guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only planning output; generated runbooks should be reviewed and tested before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
