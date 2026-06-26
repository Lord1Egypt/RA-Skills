## Description: <br>
Alibaba Cloud Compute Provision automatically selects an Alibaba Cloud compute resource (ECS, FC, ACK, PAI) based on user intent, then creates instances and executes scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select, price, provision, run, and clean up Alibaba Cloud compute workloads across ECS, Function Compute, ACK, and PAI. It is intended for cloud compute jobs, script execution, model training, and containerized application deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real Alibaba Cloud resources and may create billable infrastructure. <br>
Mitigation: Use a least-privilege RAM role in a test account first, require explicit cost confirmation before creation, and review resource identifiers and cleanup status after each run. <br>
Risk: The skill can execute user-provided or generated scripts on cloud compute resources. <br>
Mitigation: Avoid untrusted or secret-containing scripts, validate script contents before execution, and review logs before sharing transcripts. <br>
Risk: Network exposure, region choice, workspace creation, and deletion can affect availability, cost, and data exposure. <br>
Mitigation: Require explicit confirmation for regions, public network exposure, workspace creation, and deletion; restrict public ingress to only required ports and trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/sdk-team/alibabacloud-compute-provision) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [Alibaba Cloud Compute Resource Selection Guide](artifact/references/select-resource.md) <br>
- [ECS Reference](artifact/references/ecs.md) <br>
- [FC (Function Compute) Reference](artifact/references/fc.md) <br>
- [ACK (Container Service for Kubernetes) Reference](artifact/references/ack.md) <br>
- [PAI (DLC Deep Learning Container) Reference](artifact/references/pai.md) <br>
- [VPC Reference](artifact/references/vpc.md) <br>
- [RAM permission list](artifact/references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks, cost estimates, comparison tables, and execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud API calls, generated scripts, resource identifiers, logs, and cleanup status.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
