## Description:

Generates, validates, and deploys AWS FIS experiment CloudFormation templates for Scenario Library and custom fault-injection workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare AWS Fault Injection Service experiments, validate resource-action compatibility, generate CloudFormation and README files, and deploy the supporting stack before experiment execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change AWS infrastructure through CloudFormation and AWS FIS preparation.

Mitigation: Use only in approved sandbox or tightly controlled AWS accounts, review generated CloudFormation templates and IAM policies, and require explicit approval for deploy and delete steps.

Risk: Prepared experiments can have excessive blast radius if stop conditions or target scope are not reviewed.

Mitigation: Add CloudWatch stop conditions where appropriate, confirm target resources and scenario sub-actions before deployment, and use a dedicated CloudFormation service role.

Risk: EKS pod-action workflows may leave broad or persistent shared RBAC permissions.

Mitigation: Avoid EKS pod-action workflows until cluster-admin Lambda access and retained shared RBAC are narrowed or lifecycle-managed.

## Reference(s):

- [AZ Availability: Power Interruption Scenario Guide](references/az-power-interruption-guide.md)
- [CFN Base Template Reference](references/cfn-base-template.md)
- [EKS Pod Action Guide](references/eks-pod-action-guide.md)
- [ElastiCache Redis/Valkey FIS Experiment Guide](references/elasticache-redis-guide.md)
- [Amazon MSK FIS Experiment Guide](references/msk-guide.md)
- [Output Format Reference](references/output-format.md)
- [Scenario Slug and Naming Conventions](references/slug-conventions.md)
- [AWS FIS AZ Availability Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-availability-scenario.html)
- [AWS FIS AZ Application Slowdown Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-application-slowdown-scenario.html)
- [AWS FIS Cross-AZ Traffic Slowdown Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-az-traffic-slowdown-scenario.html)
- [AWS FIS Cross-Region Connectivity Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-region-scenario.html)
- [AWS FIS EKS Pod Actions](https://docs.aws.amazon.com/fis/latest/userguide/eks-pod-actions.html)
- [AWS::FIS::ExperimentTemplate CloudFormation Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html)
- [CloudFormation Service Role for FIS Experiment Setup Guide](https://panlm.github.io/others/cfn-service-role-for-fis-experiment-setup-guide/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML CloudFormation templates, README files, and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a self-contained experiment directory and may run AWS CLI and CloudFormation deployment commands; it does not start the FIS experiment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
