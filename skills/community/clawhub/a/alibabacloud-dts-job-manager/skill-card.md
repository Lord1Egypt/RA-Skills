## Description:

Helps manage Alibaba Cloud DTS database synchronization jobs, including creation, status checks, lifecycle operations, and instance-class pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud administrators use this skill to create, inspect, price, and manage one-way, same-account Alibaba Cloud DTS synchronization jobs for supported databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update local developer tools and DTS skills automatically.

Mitigation: Review installer and update behavior before use; disable automatic skill updates where pinned tooling is required.

Risk: Database credentials may be stored locally in Base64 form.

Mitigation: Protect the local credential store and do not provide database secrets in chat.

Risk: Creating or managing synchronization jobs can change cloud resources and incur charges.

Mitigation: Use the intended Alibaba Cloud CLI profile and review the target, operation, and billing impact before confirming changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-dts-job-manager)
- [Supported synchronization links](artifact/references/supported-links.md)
- [Job creation](artifact/references/job-creation.md)
- [Job lifecycle](artifact/references/job-lifecycle.md)
- [Instance classes and pricing](artifact/references/instance-classes-and-pricing.md)
- [Credentials and security](artifact/references/credentials-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports job status and progress or price and billing unit when requested.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
