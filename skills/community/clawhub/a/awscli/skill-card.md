## Description:

Manage AWS Lightsail and EC2 instances using AWS CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypertextassassinrajith](https://clawhub.ai/user/hypertextassassinrajith)

### License/Terms of Use:

ISC

## Use Case:

Developers and operators use this skill to list, start, stop, and reboot permitted AWS Lightsail instances through structured JSON actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Start, stop, and reboot operations can cause service downtime.

Mitigation: Use tightly scoped AWS IAM credentials and set ALLOWED_INSTANCES to the exact Lightsail instances the skill may control.

Risk: The release summary mentions EC2, while the implementation and security guidance identify Lightsail control only.

Mitigation: Treat EC2 support as unverified until the publisher removes the EC2 claim or adds clearly documented EC2 support.

Risk: Incorrect environment configuration can send actions to the wrong AWS region or deny intended instance operations.

Mitigation: Confirm AWS_REGION and ALLOWED_INSTANCES before use, and review structured action inputs before executing instance changes.

## Reference(s):

- [ClawHub Awscli skill page](https://clawhub.ai/hypertextassassinrajith/skills/awscli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON objects returned from AWS CLI-backed operations, with concise status messages for instance actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS CLI, configured AWS credentials, AWS_REGION, and ALLOWED_INSTANCES.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
