## Description: <br>
AWS VPC networking audit covering CIDR architecture, Security Group and NACL rule analysis, Transit Gateway connectivity, VPC Flow Log forensics, Route Table validation, and ENI/EIP resource optimization using read-only AWS CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and security reviewers use this skill to audit AWS VPC architecture, security filtering, Transit Gateway and peering connectivity, VPC Flow Logs, route tables, and unused networking resources with read-only AWS CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read sensitive AWS networking configuration and VPC Flow Log data. <br>
Mitigation: Use a dedicated least-privilege read-only role and restrict account, region, VPC, and log-query time ranges. <br>
Risk: The release declares an AWS networking MCP dependency. <br>
Mitigation: Review and approve the declared MCP dependency before use. <br>


## Reference(s): <br>
- [AWS CLI Reference - VPC Networking Audit Commands](references/cli-reference.md) <br>
- [AWS VPC Architecture Reference](references/vpc-architecture.md) <br>
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/aws-networking-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit guidance with inline read-only AWS CLI commands and a findings report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sensitive but disclosed read-only AWS networking and Flow Log queries; scope should be bounded by account, region, VPC, and time range.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
