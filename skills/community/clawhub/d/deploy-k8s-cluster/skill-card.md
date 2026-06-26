## Description: <br>
Guides an agent through planning, deploying, validating, troubleshooting, and documenting a new kubeadm-based Kubernetes cluster on Ubuntu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t2phage](https://clawhub.ai/user/t2phage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to create a new Ubuntu Kubernetes cluster with kubeadm, from node information gathering and architecture design through deployment, validation, and delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for powerful SSH or root-level access and may reconfigure dedicated machines during cluster setup. <br>
Mitigation: Use dedicated or disposable Ubuntu machines, prefer temporary SSH keys or temporary admin accounts, verify every IP and hostname, and require exact command previews before approving each milestone. <br>
Risk: Cleanup guidance may affect test resources or destroy the whole cluster if approved with the wrong scope. <br>
Mitigation: Do not approve the cleanup milestone unless it clearly states whether it will delete only test namespaces and resources or destroy the entire cluster. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/t2phage/deploy-k8s-cluster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, checklists, command previews, troubleshooting options, and deployment reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires milestone-by-milestone user confirmation; supports Ubuntu and kubeadm-based clusters only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
