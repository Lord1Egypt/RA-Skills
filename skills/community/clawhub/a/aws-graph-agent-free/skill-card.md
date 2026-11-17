## Description:

AWS图代理 provides workflow and configuration guidance for building AWS Bedrock AgentCore and LangGraph multi-agent systems, including StateGraph orchestration, runtime deployment, memory, gateway integration, and CLI lifecycle management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to plan, configure, and deploy AWS Bedrock AgentCore/LangGraph multi-agent workflows with persistent memory, gateway tool integration, and lifecycle commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS credentials or sensitive deployment details could be exposed during setup or troubleshooting.

Mitigation: Use least-privilege AWS roles or named profiles, do not paste or print AWS secrets, and avoid storing secrets in source files or container build arguments.

Risk: Generated code and shell commands can create, deploy, invoke, destroy, or otherwise affect AWS resources.

Mitigation: Review generated code and commands before execution, require explicit approval for launch, destroy, and high-impact tool actions, and clean up test resources after use.

Risk: Callback URLs or integrated tools could send data to untrusted destinations.

Mitigation: Use only callback URLs and external tools that the operator controls and trusts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before deployment and assumes an AWS account, Bedrock access, and appropriate AWS credentials or roles.]

## Skill Version(s):

1.0.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
