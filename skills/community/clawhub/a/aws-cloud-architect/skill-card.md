## Description: <br>
AWS云架构师 helps agents use local AWS CLI credentials for AWS resource inventory, security audits, cost optimization, CloudWatch troubleshooting, and planned infrastructure changes with read-only defaults and explicit confirmation for writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and AWS operators use this skill to query AWS resources, review security posture, analyze costs, troubleshoot CloudWatch signals, and plan infrastructure changes through AWS CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local AWS credentials may grant broad account access if the agent uses an over-permissive profile. <br>
Mitigation: Use a least-privilege AWS profile, preferably read-only by default, and verify identity before running account-scoped commands. <br>
Risk: Generated AWS CLI commands for create, modify, delete, IAM, billing, or credential-related actions could change sensitive resources if executed without review. <br>
Mitigation: Review every generated command, use dry-run or impact analysis where available, and require explicit confirmation before any write or destructive operation. <br>
Risk: AWS access keys, session tokens, or callback data could be exposed through chat, logs, or untrusted endpoints. <br>
Mitigation: Do not paste AWS secrets into chat, do not print secret values, and avoid callback URLs unless the endpoint and transmitted data are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-cloud-architect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with AWS CLI command examples and JSON/table-oriented result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only commands by default; write, destructive, IAM, billing, and credential-related actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
