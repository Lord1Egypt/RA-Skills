## Description:

Forge is a repair-inspect loop orchestrator for managing automated code repair tasks with independent inspection, dependency-aware parallel execution, protected file guardrails, and crash-recoverable state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melody1015](https://clawhub.ai/user/melody1015)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use Forge to coordinate multiple code repair tasks, generate repair and inspection work items, track state across rounds, and escalate unresolved or protected-file issues for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes project state, task files, result files, and reflection records during repair workflows.

Mitigation: Run it only in repositories where automated repair artifacts are acceptable, and review generated state and result files before relying on them.

Risk: Model-generated repair patterns can be persisted and reused across projects.

Mitigation: Review or isolate reflection files before cross-project reuse, especially when projects contain sensitive or proprietary implementation details.

Risk: The workflow may run a repository-provided doc-sync checker and advertises auto-commit behavior.

Mitigation: Use trusted repositories, disable or remove automatic checker execution when needed, and turn off or review auto-commit behavior before deployment.

## Reference(s):

- [Forge protocol](artifact/references/protocol.md)
- [Universal patterns format](artifact/reflections/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task prompts, JSON state and result files, shell command output, and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-side forge-state.json, forge-output task and result files, and forge-reflections.jsonl pattern records.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
