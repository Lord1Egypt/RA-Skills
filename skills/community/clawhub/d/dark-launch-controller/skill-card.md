## Description:

Plan and execute dark launches with feature flags, performance monitoring, and gradual exposure rollouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to plan dark launches, monitor hidden production code paths, and promote feature-flagged releases through controlled exposure phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shell/Python heredoc snippet can turn a crafted feature name into code execution in the user's environment.

Mitigation: Pass feature names through environment variables or argv, quote heredoc delimiters, validate feature names against a narrow safe pattern, and require human approval before applying rollout, rollback, or restart commands.

Risk: Generated Kubernetes rollout, rollback, and restart commands can affect production systems if run with broad credentials.

Mitigation: Use read-only, namespace-scoped Kubernetes credentials for planning and monitoring, and require explicit human approval before executing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/dark-launch-controller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, YAML, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are operator-facing plans, monitoring reports, rollout commands, rollback commands, and feature-flag configuration examples.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
