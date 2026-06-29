## Description: <br>
File Utilities and Editing provides AgentPMT-hosted remote file utility actions for MIME lookup, path parsing and joining, CSV table rendering, JSON formatting, Base64 encoding and decoding, file size formatting, and hash generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to invoke AgentPMT remote file utilities for text-based metadata lookup, path manipulation, content formatting, Base64 conversion, and hash generation without local filesystem access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool inputs are sent to AgentPMT-hosted remote utilities and may contain private file names or text content. <br>
Mitigation: Keep inputs scoped to the minimum content needed, and do not submit secrets or private file contents unless that remote processing is approved. <br>
Risk: Account credentials, wallet private keys, mnemonics, signatures, or payment headers could be exposed if copied into prompts or logs. <br>
Mitigation: Use the AgentPMT setup skill for credential handling, and do not place credentials or payment material in prompts, examples, or logs. <br>
Risk: Hash generation supports MD5 and SHA-1 as well as SHA-256 and SHA-512. <br>
Mitigation: Use SHA-256 or SHA-512 for integrity-sensitive workflows unless a weaker algorithm is required for compatibility. <br>
Risk: The generated artifact says live schemas may change after publication. <br>
Mitigation: Fetch live schema or instructions before production integrations when parameters, enum values, outputs, or examples are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/file-utilities-and-editing) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/file-utilities-and-editing) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT main MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON examples; remote tool responses return JSON metadata and text strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stateless text transformations; inputs are strings; actions cost 5 credits; x402 is not enabled; the artifact states no local filesystem read or write behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
