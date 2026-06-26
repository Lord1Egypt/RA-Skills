## Description: <br>
Bind Protocol MCP server for credential verification, policy authoring, and zero-knowledge proof generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-c-child](https://clawhub.ai/user/jason-c-child) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate the Bind Protocol MCP server for verifiable credential parsing, verification, policy authoring, zero-knowledge proof generation, credential issuance, and proof sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Bind agent key can enable real account actions through API-backed tools. <br>
Mitigation: Use a dedicated least-privilege Bind agent key, keep it in an environment variable, and confirm before creating policies, issuing credentials, submitting proof inputs, or sharing proofs. <br>
Risk: API-backed tools can send credential hashes, policy specs, proof inputs, and metadata to the Bind API. <br>
Mitigation: Confirm the intended data flow with the user before using API-backed tools and avoid submitting sensitive proof inputs unless the user explicitly intends to use Bind Protocol for that action. <br>
Risk: The MCP server is installed through an upstream npm package. <br>
Mitigation: Review the upstream package before using production credentials. <br>


## Reference(s): <br>
- [Bind Protocol MCP documentation](https://docs.bindprotocol.xyz/mcp/overview) <br>
- [Bind dashboard](https://dashboard.bindprotocol.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/jason-c-child/bind-protocol-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Node.js, npx, and a BIND_API_KEY environment variable for API-backed tools.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
