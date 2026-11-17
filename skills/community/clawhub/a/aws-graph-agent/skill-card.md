## Description: <br>
AWS Graph Agent helps developers plan and assemble LangGraph multi-agent workflows for AWS Bedrock AgentCore, including StateGraph orchestration, runtime packaging, persistent memory, gateway tool integration, and CLI lifecycle tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to design, configure, deploy, test, and clean up AWS Bedrock AgentCore agents that use LangGraph orchestration, cross-session memory, and gateway-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud cleanup commands can delete or disrupt AWS resources if run against the wrong target environment. <br>
Mitigation: Review each command, confirm the AWS account, region, and agent name, and treat agentcore destroy as a destructive operation before execution. <br>
Risk: Secret-handling guidance may lead users to place API keys or other secrets in container build instructions. <br>
Mitigation: Use runtime secret injection or an AWS secret store instead of Dockerfile ENV instructions for API keys and credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-graph-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and cloud-resource changes should be reviewed before execution against an AWS account.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
