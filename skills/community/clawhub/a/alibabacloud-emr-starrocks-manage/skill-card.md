## Description:

Manage the full lifecycle of Alibaba Cloud EMR Serverless StarRocks instances, including creation, scaling, configuration, maintenance, and diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, SREs, operations engineers, and architects use this skill to manage Alibaba Cloud EMR Serverless StarRocks instances through the aliyun CLI. It focuses on instance lifecycle, capacity, configuration, maintenance, and diagnostics rather than SQL authoring, data import/export, query tuning, or unrelated Alibaba Cloud products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud creation, scaling, restart, modification, and diagnostic operations can change live resources or incur cost.

Mitigation: Use a least-privilege Alibaba Cloud profile and confirm the account, region, VPC, payment type, and expected cost before executing write operations.

Risk: Administrator passwords placed directly in command text can be exposed through shell history, logs, or shared transcripts.

Mitigation: Prefer secure secret input or temporary-file workflows when supported, mask sensitive output, and rotate credentials if example passwords were used.

Risk: The security summary says the skill overstates some lifecycle capabilities.

Mitigation: Treat scale, restart, modify, and diagnostic requests cautiously and verify the intended operation against current Alibaba Cloud API behavior before execution.

## Reference(s):

- [Quick Start: Create Your First StarRocks Instance from Scratch](references/getting-started.md)
- [RAM Permission Policy Reference](references/ram-policies.md)
- [Instance Full Lifecycle: Plan -> Create -> Manage](references/instance-lifecycle.md)
- [Daily Operations: Configuration, Maintenance, SSL, Billing, Gateway](references/operations.md)
- [API Parameter Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Alibaba Cloud CLI credentials; generated commands can affect cloud resources and costs.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
