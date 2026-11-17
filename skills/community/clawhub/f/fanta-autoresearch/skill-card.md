## Description:

Autoresearch guides agents through bounded goal-metric iteration loops that make focused changes, verify them mechanically, keep improvements, revert regressions, and log results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run structured optimization loops for benchmark improvement, test fixing, configuration tuning, bundle-size reduction, coverage increases, and similar metric-driven tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to edit files and run verification commands across repeated iterations.

Mitigation: Use it only with a defined file scope, maximum iteration count, explicit verification commands, timeouts, and rollback expectations.

Risk: Long-running loops, subagents, or background runs can continue making changes longer than intended.

Mitigation: Set a fixed iteration limit, require progress logs, and allow subagents or background execution only when the task boundary is clear.

Risk: Verification commands may include unreviewed package or external commands.

Mitigation: Review commands before execution, avoid sensitive directories, and do not run unreviewed npx or package-manager commands.

## Reference(s):

- [Autoresearch Workflows](artifact/references/workflows.md)
- [Common Metrics for Autoresearch](artifact/references/metrics.md)
- [ClawHub Skill Page](https://clawhub.ai/fantaclaw-ai/skills/fanta-autoresearch)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command examples and an optional Python loop executor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce TSV iteration logs when the bundled executor script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
