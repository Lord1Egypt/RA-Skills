## Description: <br>
Discovers AWS-hosted AI agent and MCP-relevant assets with operator-controlled AWS credentials, writes canonical agent-bom inventory JSON, and optionally scans or exports that inventory when the operator requests it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security engineers use this skill to collect AWS Bedrock, ECS, SageMaker, Lambda, EKS, Step Functions, EC2, and related agentic infrastructure inventory as schema-valid local JSON. They can then run agent-bom scans or exports only after an explicit operator-approved handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS credentials used for discovery may expose more cloud inventory than intended if the selected profile or role is too broad. <br>
Mitigation: Use operator-controlled AWS SSO, WebIdentity, or STS assumed-role credentials with read-only IAM scope and confirm the target account, region, and services before running discovery. <br>
Risk: Generated inventory and export files may contain sensitive cloud metadata even when credential-like values are redacted. <br>
Mitigation: Write outputs only to operator-selected paths and review the JSON or export before sharing it outside the operator environment. <br>
Risk: A substituted package or unexpected publisher/source could change runtime behavior despite the clean scan telemetry for this release. <br>
Mitigation: Install only from the expected ClawHub publisher handle or source link and review the artifact files when stronger assurance is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/agent-bom-discover-aws) <br>
- [agent-bom homepage](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI package](https://pypi.org/project/agent-bom/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and operator-selected JSON inventory or export file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local inventory or export files to operator-selected paths; uses the local AWS SDK credential chain and does not require a hosted agent-bom service handoff.] <br>

## Skill Version(s): <br>
0.89.2 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
