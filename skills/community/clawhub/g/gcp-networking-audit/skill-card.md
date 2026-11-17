## Description:

GCP VPC Network audit covering global VPC design, firewall rule priority evaluation with hierarchical policies, Cloud NAT egress analysis, Cloud Interconnect and Shared VPC connectivity, Cloud Router BGP validation, and resource optimization using read-only gcloud CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and security engineers use this skill to audit GCP VPC architecture, firewall rules, Cloud NAT, hybrid connectivity, Shared VPC, and Cloud Router posture. It guides read-only gcloud inspection and helps produce security, compliance, troubleshooting, and optimization findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output may expose sensitive network, IAM, project, organization, or Shared VPC configuration details.

Mitigation: Run the skill with least-privilege read-only access, confirm the target scope before executing commands, and handle collected output as sensitive operational data.

Risk: The skill depends on the active gcloud account and project context, so reviewing the wrong scope can produce misleading findings.

Mitigation: Verify the active account, project, organization, and Shared VPC host or service project context before running the audit commands.

## Reference(s):

- [GCP gcloud CLI Reference - VPC Network Audit Commands](references/cli-reference.md)
- [GCP VPC Network Architecture Reference](references/vpc-architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit guidance with read-only gcloud command snippets and a findings report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated gcloud access to the selected GCP project, organization, or Shared VPC scope; commands are read-only.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
