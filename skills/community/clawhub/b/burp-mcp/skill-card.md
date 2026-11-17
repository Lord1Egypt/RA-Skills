## Description:

Connect to a local Burp Suite MCP Server over SSE and list or call Burp tools from the workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nquangit](https://clawhub.ai/user/nquangit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to inspect available Burp Suite MCP tools and call them from an agent workspace when Burp Suite is already running locally with the PortSwigger MCP extension enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Burp Suite proxy history, scanner findings, and configuration data to an agent.

Mitigation: Install it only for workflows that intentionally require Burp access, treat outputs as sensitive security data, and avoid broad history queries unless needed.

Risk: Some available Burp MCP tools may mutate Burp Suite state or project/user options.

Mitigation: Prefer read-only tools first and require explicit human approval before invoking mutation-capable tools.

Risk: Changing the SSE endpoint can connect the agent to an unintended MCP server.

Mitigation: Prefer the documented loopback endpoint and require human approval before using a non-default endpoint.

Risk: The release depends on the Python mcp package without a pinned version in the artifact metadata.

Mitigation: Pin the mcp dependency before routine or shared-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nquangit/skills/burp-mcp)
- [Default local Burp MCP SSE endpoint](http://127.0.0.1:9876/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Burp tool responses can include MCP content text blocks that may need a second parse step for structured use.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
