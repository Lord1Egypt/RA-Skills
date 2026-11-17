## Description:

Autoresearch guides an AI agent through autonomous, metric-driven experiment loops for optimization, ablation studies, and configuration search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Autoresearch to configure an agent to run controlled experiments against a single metric, modify approved target files, execute a run command, track results, and analyze improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous experiment loops can repeatedly edit code and run configured commands without a built-in stopping condition.

Mitigation: Run only in an isolated clone or disposable branch, and enforce explicit external time, command, and resource limits.

Risk: Repository rollback behavior can reset work and remove valuable uncommitted or concurrent changes.

Mitigation: Start from a clean worktree, keep unrelated work outside the experiment branch, and avoid rollback flows on repositories with valuable uncommitted work.

Risk: Broad write and execution authority can affect files beyond the intended experiment targets when setup constraints are incomplete.

Mitigation: Define explicit target files, read-only files, constraints, and metric extraction before running experiments; review changes before accepting kept commits.

## Reference(s):

- [Autoresearch Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and tab-separated result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create experiment configuration, result logs, run logs, and git commits while executing experiments.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
