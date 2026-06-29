## Description: <br>
Classify a database migration and surface production risks - locks, compatibility, backfills, rollback - and prefer expand-contract sequencing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review database migrations before deployment, classify migration type, identify lock, compatibility, backfill, and rollback risks, and propose safer rollout sequencing with verification and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Ritual Cloud setup can install a global CLI and connect external tooling. <br>
Mitigation: Use the standalone local workflow unless deeper context is needed, and review the optional setup before installing or connecting tools. <br>
Risk: Migration guidance can miss environment-specific dependencies, rollout constraints, or data-volume effects. <br>
Mitigation: Confirm assumptions with dry runs, explain plans, affected tests, canary rollout, monitoring, and owner review before production use. <br>
Risk: Destructive schema cleanup in the same deployment can break compatibility or reduce rollback options. <br>
Mitigation: Prefer expand-contract sequencing and defer destructive cleanup unless it is explicitly requested and proven safe. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ritual/database-migration-risk-review) <br>
- [Ritual homepage](https://ritual.work) <br>
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis with checklist-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a migration risk level, unsafe operations, safer sequence, backfill and rollback plan, verification steps, and monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
