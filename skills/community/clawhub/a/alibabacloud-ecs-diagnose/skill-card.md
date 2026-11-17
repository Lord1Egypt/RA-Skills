## Description:

Diagnoses Alibaba Cloud ECS instance connectivity, performance, disk, and status issues using cloud checks and optional in-instance diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers and developers use this skill to investigate Alibaba Cloud ECS connectivity, resource, and disk performance problems and receive a diagnostic report with recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials grant the agent access to ECS resource details.

Mitigation: Use narrowly scoped credentials and keep routine diagnosis read-only.

Risk: In-instance commands and repairs can affect running systems, including when symptom descriptions are treated as approval.

Mitigation: Require explicit confirmation before every Cloud Assistant command and each repair; review the command, scope, and rollback plan.

Risk: The remote installer executes downloaded code.

Mitigation: Prefer the signed CLI package; only use the remote script after manual review and explicit acceptance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-ecs-diagnose)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Required RAM permissions](references/ram-policies.md)
- [Alibaba Cloud ECS API reference](https://www.alibabacloud.com/help/ecs/developer-reference/api-overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured diagnostic report with findings, risk warnings, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checks that could not run; in-instance diagnostics require separate authorization.]

## Skill Version(s):

0.0.5 (source: server release and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
