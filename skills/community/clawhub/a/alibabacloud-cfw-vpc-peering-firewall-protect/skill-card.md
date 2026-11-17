## Description:

Manage Alibaba Cloud Firewall VPC peering boundary firewalls, including assessment, creation, switch control, route updates, and IPS and ACL settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and network engineers use this skill to inspect and manage Alibaba Cloud Firewall protection for VPCs connected by Express Connect or VPC peering, including firewall setup, protection switches, routes, and IPS or ACL settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Switching firewall protection triggers route re-learning that can take 5–30 minutes and briefly interrupt long-lived connections.

Mitigation: Schedule switch changes off-peak and review the selected account, firewall IDs, and discovered route lists before confirming.

Risk: Firewall creation and configuration changes can affect route coverage and may consume cloud quota or incur charges.

Mitigation: Begin with read-only permissions, grant only the write actions needed for the requested operation, and do not grant deletion permission unless independently required.

Risk: A dry-run prevents writes but may still make read-only cloud calls; an unverified installer or CLI plugin update can also affect execution.

Mitigation: Verify the installer before execution, review CLI plugin updates, and treat dry-run as a write safeguard rather than an offline guarantee.

Risk: Built-in update verification checks the firewall name and may not confirm that updated CIDR routes are protected.

Mitigation: After CIDR updates, verify the protected routes directly.

Risk: The referenced regression tests are absent from this package, and stubbed checks do not validate live cloud behavior.

Mitigation: Verify cloud-side state after operations and do not treat stubbed checks as evidence of live behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-vpc-peering-firewall-protect)
- [VPC prerequisites and operational impact](artifact/references/vpc-prerequisites.md)
- [RAM policies and permissions](artifact/references/ram-policies.md)
- [API errors and behaviors](artifact/references/api-errors.md)
- [Verification method](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries and tables, JSON results, and shell command previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require explicit user confirmation; assessment and query workflows can provide read-only plans and results.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata, references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
