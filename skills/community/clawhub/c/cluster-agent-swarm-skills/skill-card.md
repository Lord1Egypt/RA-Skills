## Description:

Cluster Agent Swarm coordinates seven specialized agents for Kubernetes and OpenShift platform operations, including cluster operations, GitOps, security, observability, artifacts, and developer experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kcns008](https://clawhub.ai/user/kcns008)

### License/Terms of Use:


## Use Case:

Platform engineers and cluster operators use this skill to coordinate agent-assisted Kubernetes and OpenShift operations across cluster lifecycle, GitOps deployment, security review, observability triage, artifact workflows, and developer enablement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags mutable remote installation guidance for high-impact cluster and cloud workflows.

Mitigation: Prefer a pinned commit or signed release, verify provenance, and confirm the complete referenced skill files and scripts match the reviewed artifact before installation.

Risk: The skill can guide workflows involving real cluster, cloud, GitOps, registry, or repository credentials.

Mitigation: Install in a least-privileged sandbox first and only grant production access after environment-specific review.

Risk: Artifact behavior includes proposed operational commands and runbook actions for Kubernetes and OpenShift environments.

Mitigation: Require human approval for production deletion, cluster-wide policy changes, secret changes, irreversible upgrades, cluster-admin RBAC changes, and production deployments.

## Reference(s):

- [Cluster Agent Swarm ClawHub page](https://clawhub.ai/kcns008/skills/cluster-agent-swarm-skills)
- [Publisher profile](https://clawhub.ai/user/kcns008)
- [Cluster Agent Swarm repository](https://github.com/kcns008/cluster-agent-swarm-skills)
- [Orchestrator skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/orchestrator)
- [Cluster Ops skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/cluster-ops)
- [GitOps skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/gitops)
- [Security skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/security)
- [Observability skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/observability)
- [Artifacts skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/artifacts)
- [Developer Experience skill](https://github.com/kcns008/cluster-agent-swarm-skills/skills/developer-experience)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include operational plans, runbook steps, command proposals, configuration snippets, reports, and escalation guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
