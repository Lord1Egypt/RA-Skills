## Description: <br>
Diagnose Alibaba Cloud ACK cluster ALB Ingress reconcile errors, Warning events, and configuration issues using kubectl, optional aliyun-cli, and a knowledge base of known ALB Ingress patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and SREs use this skill to investigate Alibaba Cloud ACK ALB Ingress failures, match Warning events or misconfigurations to known error patterns, and produce root-cause analysis with corrective YAML or command guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional multi-cluster connection flow can fetch and persist kubeconfig credentials for every running ACK cluster in an account. <br>
Mitigation: Prefer the core read-only diagnostic flow with an existing scoped kubeconfig; run cluster_connect.sh only intentionally and remove generated ~/.kube/ack-*.yaml files after use. <br>
Risk: Troubleshooting output may propose cluster or cloud configuration changes. <br>
Mitigation: Review generated YAML and command proposals before execution, and require explicit user confirmation before kubectl or aliyun-cli write operations. <br>


## Reference(s): <br>
- [ALB Ingress concepts and annotation reference](artifact/references/alb_ingress_reference.md) <br>
- [ALB Ingress core concepts quick reference](artifact/references/concepts_reference.md) <br>
- [Diagnostic decision tree](artifact/references/diagnostic_tree.json) <br>
- [Error classification quick reference](artifact/references/error_classification.md) <br>
- [RAM permissions](artifact/references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostics with command snippets and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include kubectl and aliyun-cli read commands; write operations should require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
