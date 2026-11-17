## Description:

Guides agents through planning, creating, registering, reusing, verifying, repairing, and resuming user cloud roles in connected Alibaba Cloud, AWS, and Tencent Cloud IDaaS EIAM accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to collect role and permission requirements, inspect connected IDaaS accounts, prepare an approved plan, and configure or verify cloud roles across Alibaba Cloud, AWS, and Tencent Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reuse mode may create roles or restore permission attachments without separate approval.

Mitigation: Use credentials that cannot change permissions during reuse checks, and require explicit approval for any role creation or permission restoration before granting provisioning access.

## Reference(s):

- [Workflow and safety requirements](artifact/references/workflow.md)
- [Role request and plan format](artifact/references/plan-format.md)
- [Release validation and current limits](artifact/references/validation.md)
- [Alibaba Cloud RAM CreateRole API](https://help.aliyun.com/en/ram/developer-reference/api-ram-2015-05-01-createrole)
- [AWS IAM CreateRole CLI reference](https://docs.aws.amazon.com/cli/latest/reference/iam/create-role.html)
- [Tencent Cloud CAM CreateRole API](https://cloud.tencent.com/document/product/598/19381)

## Skill Output:

**Output Type(s):** [Guidance, JSON plans and audit evidence, Shell commands, Cloud role configuration, Status reports]

**Output Format:** [Markdown guidance, JSON plans and evidence, and cloud role configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutations require explicit user approval; user and group assignment is not supported.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
