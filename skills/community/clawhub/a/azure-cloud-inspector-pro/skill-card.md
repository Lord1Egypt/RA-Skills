## Description:

Azure巡检员专业版 helps operations engineers, cloud architects, security engineers, FinOps specialists, and compliance auditors inspect Azure resources across subscriptions with RBAC auditing, cost checks, NSG exposure analysis, configuration drift detection, scheduling, trend comparison, and Markdown reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External Azure operations, security, FinOps, and compliance teams use this skill to generate Azure CLI inspection workflows, run read-oriented checks, audit RBAC and NSG exposure, summarize cost and health signals, and create shareable Markdown inspection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure inspection output can expose sensitive cloud posture, identity, cost, and access-control data.

Mitigation: Use least-privilege Azure roles, select the subscription or resource group explicitly, restrict generated report and log permissions, and clean up sensitive outputs when they are no longer needed.

Risk: Optional callback or webhook delivery can disclose inspection results to an untrusted destination.

Mitigation: Avoid callback_url or webhook delivery unless the destination is trusted and approved for the inspected Azure data.

Risk: User-requested write or destructive Azure actions can affect cloud resources if executed without review.

Mitigation: Keep the skill in its default read-only posture, require explicit confirmation for changes, and prefer dry-run or what-if previews before any write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-cloud-inspector-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Azure CLI and shell command blocks, configuration snippets, tables, and report templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local Markdown reports, JSON or CSV inspection snapshots, scheduling snippets, and callback/reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
