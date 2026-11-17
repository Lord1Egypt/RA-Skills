## Description:

Bind Protocol MCP server for credential verification, policy authoring, and zero-knowledge proof generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-c-child](https://clawhub.ai/user/jason-c-child)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure and operate the Bind Protocol MCP server for VC-JWT parsing and verification, revocation checks, issuer and policy inspection, policy authoring, proof generation, credential issuance, and proof sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is installed through an unpinned external package path.

Mitigation: Pin or locally vendor the MCP package before use, and review updates before changing the installed version.

Risk: The server uses a sensitive Bind agent key and exposes mutation-capable tools.

Mitigation: Use a tightly scoped Bind agent key, avoid broad policy-authoring or sharing permissions unless required, and rotate the key after suspected compromise.

Risk: API-backed workflows send hashes, policy specs, proof inputs, and metadata to the Bind API.

Mitigation: Review proof inputs and policy data before submission, and avoid sending unnecessary sensitive values.

Risk: Credential leakage can occur if the Bind agent key is hardcoded in shared configuration.

Mitigation: Store the key in the BIND_API_KEY environment variable and avoid committing secrets to project or MCP configuration files.

## Reference(s):

- [Bind Protocol MCP Documentation](https://docs.bindprotocol.xyz/mcp/overview)
- [Bind Dashboard](https://dashboard.bindprotocol.xyz)
- [Bind API Endpoint](https://api.bindprotocol.xyz)
- [ClawHub Skill Page](https://clawhub.ai/jason-c-child/skills/bind-protocol-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local MCP setup, environment variable handling, credential verification workflows, policy specs, proof jobs, and Bind tool calls.]

## Skill Version(s):

2.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
