## Description: <br>
Complete Platform Agent Swarm - a coordinated multi-agent system for Kubernetes and OpenShift platform operations that includes Orchestrator, Cluster Ops, GitOps, Security, Observability, Artifacts, and Developer Experience agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kcns008](https://clawhub.ai/user/kcns008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to coordinate Kubernetes and OpenShift operations across cluster operations, GitOps, security, observability, artifact management, and developer experience workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against live Kubernetes, OpenShift, GitOps, cloud, registry, and Git environments. <br>
Mitigation: Use dedicated least-privilege credentials and require explicit human approval before every mutating action. <br>
Risk: Recurring heartbeat behavior can repeatedly trigger operational activity. <br>
Mitigation: Disable heartbeat behavior unless it is explicitly needed, or tightly configure its schedule, scope, and permissions. <br>
Risk: Incomplete user-control boundaries may allow unsafe changes if context is wrong. <br>
Mitigation: Verify the cluster, context, namespace, proposed diff, and rollback plan before execution. <br>
Risk: The artifact references an external GitHub repository for installation. <br>
Mitigation: Review and pin the referenced repository before following install commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kcns008/cluster-agent-swarm-skills) <br>
- [Publisher profile](https://clawhub.ai/user/kcns008) <br>
- [Cluster Agent Swarm GitHub repository](https://github.com/kcns008/cluster-agent-swarm-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose live Kubernetes, OpenShift, GitOps, cloud, registry, and Git operations that require human review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
