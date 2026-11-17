## Description:

AWS VPC networking audit covering CIDR architecture, Security Group and NACL rule analysis, Transit Gateway connectivity, VPC Flow Log forensics, Route Table validation, and ENI/EIP resource optimization using read-only AWS CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, security teams, and auditors use this skill to review AWS VPC architecture, security filtering, connectivity, VPC Flow Logs, route tables, and unused networking resources with read-only AWS CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS credentials or assumed roles could expose infrastructure beyond the intended audit scope.

Mitigation: Install and run the skill only with intentionally read-only permissions scoped to the accounts, regions, VPCs, and log groups being audited.

Risk: VPC Flow Logs and network inventory can reveal sensitive infrastructure topology and traffic patterns.

Mitigation: Treat generated audit notes and command output as sensitive infrastructure data and limit storage and sharing to authorized reviewers.

Risk: Audit findings may lead to remediation actions that change AWS networking behavior outside the skill's read-only workflow.

Mitigation: Review proposed remediation separately and apply changes through normal change-control or infrastructure-as-code review before modifying AWS resources.

## Reference(s):

- [AWS CLI Reference - VPC Networking Audit Commands](references/cli-reference.md)
- [AWS VPC Architecture Reference](references/vpc-architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and structured audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only AWS CLI command guidance and report templates for scoped VPC networking audits.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
