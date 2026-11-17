## Description:

Master-Worker Agent Cluster for parallel task execution. Use when building distributed agent systems with parallel processing needs, task orchestration, or MapReduce-style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gl813788-byte](https://clawhub.ai/user/gl813788-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Agent Weave to build master-worker agent clusters, distribute work across parallel workers, and implement MapReduce-style task orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release has install-supply-chain concerns because the package lock references a non-HTTPS npm registry mirror.

Mitigation: Regenerate the lockfile against an HTTPS registry before installation, CI use, or redistribution.

Risk: The package creates local log and report files during agent orchestration.

Mitigation: Run it in a controlled workspace and review generated files for sensitive task data before sharing or retaining logs.

Risk: The inter-agent communication layer should not be relied on for strong message confidentiality or authentication without code changes.

Mitigation: Use it only within trusted local boundaries unless additional authentication, authorization, and message protection are added.

Risk: Monitoring timers and long-running agent tasks can continue consuming local resources.

Mitigation: Set operational limits, cancel long-running tasks when no longer needed, and clean up agents after execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gl813788-byte/skills/agent-weave)
- [README](artifact/README.md)
- [Test Report](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated JavaScript code, CLI usage, cluster configuration, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
