## Description:

Helps migrate Kubernetes nginx Ingress resources to Alibaba Cloud ALB Ingress using offline YAML analysis, generated manifests, and a DNS cutover plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to assess nginx Ingress compatibility with Alibaba Cloud ALB Ingress, prepare AlbConfig, IngressClass, and Ingress YAML, and plan a controlled DNS migration without granting cluster or cloud access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreplaced address type, region, or vSwitch placeholders may lead to incorrect or failed deployment.

Mitigation: Replace and verify every placeholder against the intended environment before applying the manifests.

Risk: Unsupported or downgraded nginx features may change application behavior after migration.

Mitigation: Review every flagged feature and verify routing and application behavior before cutover.

Risk: Applying generated resources or changing DNS may incur charges or redirect production traffic.

Mitigation: Review commands and the cutover plan, then deploy and change DNS only with operator approval.

## Reference(s):

- [Alibaba Cloud: Migrate nginx Ingress workloads to ALB Ingress](https://help.aliyun.com/zh/slb/application-load-balancer/migrate-workloads-from-a-self-managed-nginx-ingress-to-an-alb-ingress)
- [Alibaba Cloud: ALB Ingress annotations](https://help.aliyun.com/zh/slb/application-load-balancer/user-guide/annotations)
- [Alibaba Cloud: Configure an ALB instance using AlbConfig](https://help.aliyun.com/zh/slb/application-load-balancer/user-guide/configure-an-alb-instance-by-using-albconfig)
- [Annotation mapping](references/annotation-mapping.md)
- [DNS cutover](references/dns-cutover.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown report with Kubernetes YAML manifests and cutover instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline analysis of user-provided YAML; generated resources and commands require review before deployment.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
