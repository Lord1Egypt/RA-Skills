## Description:

Helps agents discover commands and query or manage Alibaba Cloud WUYING resources through official Aliyun CLI product plugins using an OAuth profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to inspect and manage WUYING cloud computers, browsers, application delivery, users, policies, and related resources. It also helps discover supported commands and troubleshoot local Aliyun CLI setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud actions can delete resources or execute remote scripts; the executable wrapper does not enforce confirmation rules on its own.

Mitigation: Require fresh, target-specific confirmation before creating, modifying, deleting, resetting, rebuilding, releasing, or running commands; treat remote script execution and tenant skill administration as especially sensitive.

Risk: An active OAuth profile can grant broad access to WUYING resources.

Mitigation: Use a least-privilege account and prefer read-only permissions unless changes are necessary.

## Reference(s):

- [Authentication and OAuth setup](references/authentication.md)
- [Execution safety and confirmation rules](references/safety.md)
- [Least-privilege RAM policies](references/ram-policies.md)
- [CLI compatibility](references/compatibility.md)
- [Alibaba Cloud WUYING documentation](https://help.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports execution status, resource scope, blockers, and verification results.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
