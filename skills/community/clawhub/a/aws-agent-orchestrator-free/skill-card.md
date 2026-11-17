## Description: <br>
Helps developers deploy a single-agent HTTP service on AWS Bedrock AgentCore with LangGraph, including setup, local testing, launch commands, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual builders use this skill to quickly create, test, and deploy a single-agent AWS Bedrock AgentCore service backed by a LangGraph StateGraph. It is suited to small production or learning workflows that need single-agent orchestration, short-term memory, local tools, and container launch guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through local package installation and AWS AgentCore deployment commands that can create or change cloud resources. <br>
Mitigation: Before running commands, verify the active AWS profile, account, region, agent name, and whether the target environment is production. <br>
Risk: The documented destroy workflow can remove deployed AWS AgentCore resources. <br>
Mitigation: Treat `agentcore destroy` as destructive cleanup and confirm the target resource before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-agent-orchestrator-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment commands, code templates, configuration notes, decision guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
