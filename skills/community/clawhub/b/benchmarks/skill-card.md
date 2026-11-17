## Description:

Benchmark storage routing guidance for agent memory and benchmark stacks, including where to place benchmark databases, scripts, result summaries, and run-resilience controls for long LLM-driven runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minopop](https://clawhub.ai/user/minopop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and benchmark maintainers use this skill before creating benchmark databases or output paths, and when hardening long-running benchmark or ingestion jobs against transient provider failures. It guides agents to keep code and score artifacts in the repository while routing run databases and scratch workspaces outside the repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark databases and checkpoints may be routed outside the repository, typically under a scratch directory.

Mitigation: Confirm the scratch root is acceptable for local storage policy, backups, cleanup, and data retention before running large benchmarks.

Risk: Incorrect output routing can place large binary run databases in the repository.

Mitigation: Use explicit benchmark output paths outside the repository and keep a repository .gitignore backstop for database files.

Risk: Transient provider failures or empty model responses can silently thin benchmark data or force expensive reruns.

Mitigation: Apply retry hardening, checkpoint/resume, data-quality gates, and probe settings that distinguish provider failures from token-budget truncation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minopop/skills/benchmarks)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command examples and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing rules, resilience patterns, operational checks, and warnings for benchmark runs; it does not execute code directly.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
