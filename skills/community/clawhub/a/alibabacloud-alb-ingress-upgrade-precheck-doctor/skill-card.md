## Description:

Diagnoses Alibaba Cloud ACK ALB Ingress Controller upgrade precheck failures and configuration drift between ALB resources and Kubernetes resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud engineers use this skill to diagnose ALB Ingress Controller upgrade precheck failures in Alibaba Cloud ACK. It compares observed ALB settings with AlbConfig and Ingress expectations and provides targeted remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics may collect regional ALB resources beyond the target, exposing details about unrelated workloads.

Mitigation: Avoid using the skill until regional collection is limited to the target ALB; restrict shared diagnostic output to relevant entries and redact unrelated workload details.

## Reference(s):

- [Precheck error and configuration comparison guide](references/precheck_errors.md)
- [RAM permissions](references/ram-policies.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [ALB Ingress Controller documentation](https://help.aliyun.com/zh/ack/product-overview/alb-ingress-controller)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown diagnosis with findings and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only diagnostic commands and user-executable remediation suggestions.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
