## Description:

Provides cloud architecture guidance across AWS, Google Cloud Platform, and Azure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan cloud architectures across AWS, Google Cloud Platform, and Azure, including architecture patterns, cost optimization, security, compliance, disaster recovery, and migration strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Terraform or CloudFormation could affect cloud accounts if applied without review.

Mitigation: Treat generated infrastructure templates as advisory and review them before applying changes to any cloud account.

Risk: Broad cloud-provider activation wording may select the skill for general mentions of AWS, Google Cloud Platform, or Azure.

Mitigation: Confirm the user is asking for cloud architecture guidance before relying on the skill output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with architecture diagrams, infrastructure-as-code templates, cost estimates, security considerations, and migration strategies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Terraform or CloudFormation should be reviewed before applying it to any cloud account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
