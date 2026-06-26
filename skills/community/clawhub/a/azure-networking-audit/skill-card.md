## Description: <br>
Azure VNet networking audit covering address space design, NSG rule evaluation, Azure Firewall policy analysis, ExpressRoute and VPN Gateway connectivity, VNet Peering topology, and UDR validation using read-only Azure CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud, network, and security engineers use this skill to inspect Azure VNet architecture, NSG exposure, firewall policy posture, hybrid connectivity, peering, and route table behavior. It supports design reviews, post-migration audits, compliance preparation, connectivity troubleshooting, and cost-oriented cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects Azure networking configuration in the selected account and can expose sensitive topology, routing, firewall, and IAM context in the audit output. <br>
Mitigation: Use least-privileged Reader or granular network read permissions, target the subscription, resource group, and VNet explicitly, and avoid sharing audit output beyond the intended review audience. <br>
Risk: The bundled command reference includes role-assignment listing commands that may reveal access-control details when IAM context is not required. <br>
Mitigation: Run role-assignment queries only when IAM review is part of the audit scope and redact principal or role details before external sharing. <br>


## Reference(s): <br>
- [Azure CLI Reference - VNet Networking Audit Commands](references/cli-reference.md) <br>
- [Azure VNet Architecture Reference](references/vnet-architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline Azure CLI commands and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only audit steps and findings guidance for a selected Azure subscription, resource group, or VNet.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
