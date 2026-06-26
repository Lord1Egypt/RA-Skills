## Description: <br>
GCP VPC Network audit covering global VPC design, firewall rule priority evaluation with hierarchical policies, Cloud NAT egress analysis, Cloud Interconnect and Shared VPC connectivity, Cloud Router BGP validation, and resource optimization using read-only gcloud CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, security teams, and auditors use this skill to review GCP VPC architecture, firewall posture, connectivity, routing, Cloud NAT, and optimization findings with read-only gcloud commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may expose sensitive infrastructure details from GCP networking configuration. <br>
Mitigation: Run it only with authorized read-only GCP access and treat generated findings, command output, project IDs, network names, routes, and firewall details as sensitive. <br>
Risk: Commands may run against the wrong active gcloud account or project. <br>
Mitigation: Confirm the active gcloud account and project before execution, and prefer a least-privilege read-only account. <br>


## Reference(s): <br>
- [GCP gcloud CLI Reference - VPC Network Audit Commands](references/cli-reference.md) <br>
- [GCP VPC Network Architecture Reference](references/vpc-architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/gcp-networking-audit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline read-only gcloud command blocks and audit report structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated gcloud access and appropriate read permissions for the target GCP project, organization, or Shared VPC scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
