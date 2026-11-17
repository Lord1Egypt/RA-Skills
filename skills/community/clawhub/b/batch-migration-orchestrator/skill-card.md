## Description:

Use when the user wants a large, mechanical change split into many independent units and executed in parallel with isolated workers and PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan broad, mechanical codebase migrations by decomposing work into isolated units with validation and mergeable outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate broad code changes across a repository.

Mitigation: Review the proposed work decomposition and write scopes before allowing workers to run.

Risk: Parallel work can create conflicting edits or invalid migration units.

Mitigation: Require isolated work scopes and per-unit validation before merging outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wimi321/skills/batch-migration-orchestrator)
- [Publisher Profile](https://clawhub.ai/user/wimi321)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured plans, worker prompts, status summaries, and PR or patch rollups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for agent-led migration planning and parallel execution coordination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
