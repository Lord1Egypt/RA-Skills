## Description: <br>
Prepares AWS FIS experiment configurations by discovering targets, validating resource-action compatibility, generating CloudFormation and README files, and deploying the template with retry-based correction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to prepare AWS Fault Injection Service experiments for supported scenario-library and custom fault-injection cases. It helps produce deployable experiment infrastructure while checking target compatibility and deployment prerequisites before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, modify, and delete live AWS resources while preparing fault-injection infrastructure. <br>
Mitigation: Use a non-production or explicitly approved AWS account and region, and review the generated CloudFormation before deployment. <br>
Risk: CloudFormation stacks may create IAM, CloudWatch, FIS, and shared EKS RBAC resources with operational impact. <br>
Mitigation: Use a least-privilege CloudFormation service role and confirm cleanup expectations, including shared EKS RBAC resources. <br>
Risk: Fault-injection experiments can be disruptive if started without appropriate guardrails. <br>
Mitigation: Add CloudWatch alarm stop conditions for disruptive experiments and start experiments only after explicit operational approval. <br>


## Reference(s): <br>
- [AWS FIS AZ Power Interruption Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-availability-scenario.html) <br>
- [AWS FIS AZ Application Slowdown Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-application-slowdown-scenario.html) <br>
- [AWS FIS Cross-AZ Traffic Slowdown Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-az-traffic-slowdown-scenario.html) <br>
- [AWS FIS Cross-Region Connectivity Scenario](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-region-scenario.html) <br>
- [AWS FIS EKS Pod Actions](https://docs.aws.amazon.com/fis/latest/userguide/eks-pod-actions.html) <br>
- [AWS::FIS::ExperimentTemplate CloudFormation Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html) <br>
- [AZ Availability: Power Interruption Scenario Guide](references/az-power-interruption-guide.md) <br>
- [CFN Base Template Reference](references/cfn-base-template.md) <br>
- [EKS Pod Action Guide](references/eks-pod-action-guide.md) <br>
- [ElastiCache Redis/Valkey FIS Experiment Guide](references/elasticache-redis-guide.md) <br>
- [Amazon MSK FIS Experiment Guide](references/msk-guide.md) <br>
- [Output Format Reference](references/output-format.md) <br>
- [Scenario Slug and Naming Conventions](references/slug-conventions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML, JSON, and bash code blocks; generated files include README.md and cfn-template.yaml] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a self-contained experiment directory and deployment guidance; it does not start the FIS experiment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
