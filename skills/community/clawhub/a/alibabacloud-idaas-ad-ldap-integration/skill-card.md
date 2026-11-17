## Description:

Guides administrators through AD or OpenLDAP integration with IDaaS, scoped directory synchronization, delegated-login verification, readiness reviews, and evidence-based handovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

IDaaS administrators and identity engineers use this skill to plan or carry out AD/OpenLDAP inbound integration, review synchronization and identity-provider settings, and verify directory-password login separately from account synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled synchronization can delete accounts outside the source scope, and deleting the identity provider does not remove imported accounts or organizations.

Mitigation: Use a small test subtree and a read-only directory bind account, limit the cloud identity to required permissions, review synchronization and firewall changes, and keep passwords out of chat.

## Reference(s):

- [Alibaba Cloud IDaaS AD inbound integration guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-idaas-to-ad)
- [Alibaba Cloud IDaaS OpenLDAP inbound integration guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-idaas-to-openldap)
- [IDaaS identity-provider mapping API reference](references/identity-provider-mapping-api.md)
- [RAM policies reference](references/ram-policies.md)
- [Alibaba Cloud Eiam API portal](https://api.aliyun.com/product/Eiam)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports and checklists with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the requested integration, review, or handover task.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
