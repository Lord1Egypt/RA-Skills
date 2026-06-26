## Description: <br>
Deep database migration workflow-expand/contract, backward-compatible deploys, backfills, locking risks, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to plan low-downtime production schema changes, including expand/contract sequencing, backfills, read/write cutovers, verification, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database migration guidance can affect production data availability or integrity if applied without environment-specific review. <br>
Mitigation: Confirm the database engine, lock behavior, rollback path, credentials, and repository state before executing migrations; use staged rollout, throttled backfills, monitoring, and human review. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists and command or configuration examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools, credentials, or API keys are declared by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
