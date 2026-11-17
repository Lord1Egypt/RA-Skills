## Description:

Build and run Python-based AI agents using the AWS Strands SDK for autonomous agents, multi-agent workflows, custom tools, and MCP integrations across local, Anthropic, OpenAI, Bedrock, and other model providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trippingkelsea](https://clawhub.ai/user/trippingkelsea)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold and run Python Strands agents, configure model providers, add tools, connect MCP servers, and work with multi-agent patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agents can receive local file read, file write, and shell command tools by default.

Mitigation: Run generated agents in a sandboxed workspace, remove tools that are not required, and use only trusted prompts.

Risk: Model providers and MCP servers may require API keys, AWS credentials, or network access.

Mitigation: Keep credentials out of broad-access workspaces, limit environment exposure, and avoid connecting untrusted MCP servers.

Risk: Unpinned dependencies or MCP server versions can change behavior across installations.

Mitigation: Pin Strands, tool, and MCP server versions before production use and review changes before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/trippingkelsea/skills/aws-strands)
- [Strands SDK](https://github.com/strands-agents/sdk-python)
- [Strands SDK Cheatsheet](references/cheatsheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Python agent scaffolds and configuration files when the bundled scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
