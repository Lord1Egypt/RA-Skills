## Description: <br>
Plan Kubernetes cluster upgrades with API deprecation checks, addon compatibility verification, and rollback-safe runbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and Kubernetes operators use this skill to prepare cluster upgrades by checking current state, deprecated APIs, addon compatibility, workload disruption risks, and rollback procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Kubernetes and package-management commands can affect live clusters if run against the wrong environment or without review. <br>
Mitigation: Confirm kubeconfig targets the intended cluster, have a qualified cluster administrator approve the runbook, and review every command before execution. <br>
Risk: Cluster upgrades can disrupt workloads or make recovery difficult if backups, staging rehearsal, or maintenance windows are missing. <br>
Mitigation: Schedule a maintenance window, rehearse in staging where possible, verify etcd and manifest backups before upgrade, and protect backup files with restrictive access controls. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and checklist-style runbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing preflight reports, upgrade runbooks, deprecation scan reports, and command suggestions for review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
