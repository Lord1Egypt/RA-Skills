## Description:

Connects an agent to the Cloudflare MCP server so it can search and execute Cloudflare API operations across Workers, DNS, R2, D1, KV, Vectorize, and related services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to configure Cloudflare MCP access and ask an agent to inspect or change Cloudflare resources such as DNS records, Workers, KV namespaces, R2 buckets, and account details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad write-capable Cloudflare API access across production resources.

Mitigation: Use the narrowest OAuth permissions available and confirm each DNS, Worker, KV, R2, D1, or account-changing action before execution.

Risk: Short generic triggers such as CF, DNS, or Workers may activate during unrelated infrastructure work.

Mitigation: Use explicit Cloudflare-scoped requests and review the selected action before allowing execution.

## Reference(s):

- [Cloudflare MCP GitHub repository](https://github.com/cloudflare/mcp)
- [Cloudflare MCP endpoint](https://mcp.cloudflare.com/mcp)
- [ClawHub skill page](https://clawhub.ai/2233admin/skills/cloudflare-mcp)

## Skill Output:

**Output Type(s):** [Text, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Cloudflare MCP server configuration and Cloudflare OAuth authorization before first use.]

## Skill Version(s):

1.0.0 (source: artifact metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
