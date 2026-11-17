## Description:

Azure VNet networking audit covering address space design, NSG rule evaluation, Azure Firewall policy analysis, ExpressRoute and VPN Gateway connectivity, VNet Peering topology, and UDR validation using read-only Azure CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and security reviewers use this skill to audit Azure VNet architecture, NSG rules, Azure Firewall policy, hybrid connectivity, peering, and routes using read-only Azure CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure inventory commands can expose sensitive resource topology when run with broad subscription access.

Mitigation: Use Reader or granular Microsoft.Network read permissions scoped to the intended subscription, resource group, and VNet.

Risk: RBAC and Azure AD identity checks broaden the audit beyond network resource inventory.

Mitigation: Run identity and role-assignment commands only when confirming the signed-in user or verifying required audit permissions.

Risk: The audit can inspect unintended Azure resources if the Azure CLI context points at the wrong subscription or resource group.

Mitigation: Confirm the target subscription, resource group, and VNet before running the listed read-only commands.

## Reference(s):

- [Azure CLI Reference - VNet Networking Audit Commands](references/cli-reference.md)
- [Azure VNet Architecture Reference](references/vnet-architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline Azure CLI command blocks and a report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Azure CLI audit workflow requiring an authenticated Azure CLI session and scoped Azure read permissions.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
