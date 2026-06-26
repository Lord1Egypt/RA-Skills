## Description: <br>
Deploy production LangGraph agents on AWS Bedrock AgentCore for multi-agent orchestration, persistent cross-session memory, AgentCore Gateway tools, shared context, CLI deployment, observability, and scaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, deploy, inspect, and troubleshoot LangGraph multi-agent systems on AWS Bedrock AgentCore. It focuses on runtime deployment, managed memory, gateway tool integration, CLI workflows, and CloudWatch log inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud deployment and cleanup commands can affect the wrong AWS account, region, or resources. <br>
Mitigation: Use a least-privileged AWS profile, confirm account and region before deploy or destroy commands, and prefer dry-run cleanup where available. <br>
Risk: AgentCore memory features can retain conversation data across sessions or agents. <br>
Mitigation: Define retention, consent, deletion, and tenant-boundary rules before storing conversation memory. <br>


## Reference(s): <br>
- [AgentCore CLI Reference](references/agentcore-cli.md) <br>
- [AgentCore Runtime Patterns](references/agentcore-runtime.md) <br>
- [AgentCore Memory Integration](references/agentcore-memory.md) <br>
- [AgentCore Gateway Integration](references/agentcore-gateway.md) <br>
- [LangGraph 1.0 Patterns](references/langgraph-patterns.md) <br>
- [AWS Bedrock AgentCore Runtime documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html) <br>
- [AWS Bedrock AgentCore Memory documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) <br>
- [AWS Bedrock AgentCore Gateway documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) <br>
- [Bedrock AgentCore Starter Toolkit CLI reference](https://aws.github.io/bedrock-agentcore-starter-toolkit/api-reference/cli.html) <br>
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes AWS and AgentCore commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
