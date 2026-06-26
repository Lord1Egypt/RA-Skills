## Description: <br>
Deep data migration workflow for scope, mapping, validation, batching and ordering, dual-write and cutover, rollback, and reconciliation when moving tenants, bulk backfills, or changing stores without losing trust in data correctness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan high-trust data migrations, tenant moves, large backfills, and datastore changes. It guides scope definition, field mapping, restartable batching, validation, cutover, rollback, and post-migration reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration or cutover guidance may affect production data correctness if applied without review. <br>
Mitigation: Require human review, staging validation, tested rollback steps, and explicit approval before running migration or cutover commands. <br>
Risk: Data movement can silently corrupt records or miss ordering dependencies. <br>
Mitigation: Document invariants, field mappings, checkpoints, validation rules, and reconciliation checks before sign-off. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists and possible implementation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no code or hidden execution behavior in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
