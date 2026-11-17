## Description:

Use when designing chaos experiments, implementing failure injection frameworks, or conducting game day exercises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhwa8685](https://clawhub.ai/user/lhwa8685)

### License/Terms of Use:

MIT

## Use Case:

Developers, SREs, and platform engineers use this skill to design controlled chaos experiments, implement failure injection, plan game days, define blast radius controls, and document resilience improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands and manifests can intentionally disrupt infrastructure through failure injection, pod deletion, instance termination, network partitioning, or resource exhaustion.

Mitigation: Require manual approval, target allowlists, small blast radius, non-production or tightly controlled game-day environments, and active monitoring before execution.

Risk: Copy-pastable examples may contain unsafe scoping, rollback, privilege, image, or remote manifest patterns.

Mitigation: Pin remote manifests and images, use least-privilege credentials, verify namespaces and targets, and test rollback and cleanup steps before running experiments.

Risk: Chaos experiments can create customer impact if production safety controls are missing or misconfigured.

Mitigation: Start with staging or canary targets, require feature flags or kill switches, define rollback thresholds, and confirm customer-impact safeguards before production use.

## Reference(s):

- [Chaos Experiment Design](references/experiment-design.md)
- [Infrastructure Chaos Engineering](references/infrastructure-chaos.md)
- [Kubernetes Chaos Engineering](references/kubernetes-chaos.md)
- [Chaos Engineering Tools & Automation](references/chaos-tools.md)
- [Game Day Planning & Execution](references/game-days.md)
- [ClawHub skill page](https://clawhub.ai/lhwa8685/skills/chaos-engineer)
- [Publisher profile](https://clawhub.ai/user/lhwa8685)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, YAML manifests, configuration examples, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs require human review before any experiment or command is run against real infrastructure.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
