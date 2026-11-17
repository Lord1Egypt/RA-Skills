## Description:

Manage Alibaba Cloud Firewall NAT boundary firewalls by querying protection status, assessing protectable NAT gateways, planning or creating firewall protection, diagnosing route inconsistencies, toggling protection, and changing engine strict mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations, network security, and platform engineers use this skill to manage Alibaba Cloud Firewall NAT gateway protection, plan safe enablement, validate permissions, and guide manual console steps when resource release is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing or upgrading the Alibaba Cloud CLI through a remote installer before running privileged cloud operations.

Mitigation: Review the CLI installation source through an official, verifiable channel before installation, then validate the CLI and required plugins before use.

Risk: Enable, disable, create, and manual preparation workflows can change firewall routing or cloud network resources.

Mitigation: Use least-privilege RAM policies, run assessments and dry-runs first, require explicit confirmation for state-changing steps, and verify results after execution.

Risk: Disabling protection stops NAT boundary traffic from passing through Cloud Firewall controls.

Mitigation: Warn users about the security impact and prefer off-peak operation windows with post-action verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-nat-firewall-protect)
- [NAT prerequisites](references/nat-prerequisites.md)
- [RAM policies](references/ram-policies.md)
- [API errors](references/api-errors.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, tables, and JSON-style operation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assessment, dry-run, permission-probe, confirmation, and verification guidance; delete and release operations are intentionally limited to read-only guidance.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
