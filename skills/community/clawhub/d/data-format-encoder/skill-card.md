## Description: <br>
Data Format Encoder helps agents encode, decode, escape, and convert text between Base64, URL encoding, HTML entities, JSON escaping, hexadecimal, binary, ROT13, and Unicode escape formats through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transform text for web, data transmission, debugging, and source-code compatibility workflows. It is useful for encoding API payloads, URL parameters, HTML-safe text, JSON strings, byte representations, simple ROT13 obfuscation, and Unicode escape sequences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AgentPMT-hosted remote calls for text transformation, so submitted text may be processed by a remote service. <br>
Mitigation: Keep inputs to the minimum needed and avoid submitting secrets, wallet keys, mnemonics, tokens, payment headers, or private content unless remote processing is intended. <br>
Risk: Some actions require an AgentPMT account, enabled product access, and credits, which can block or change runtime behavior. <br>
Mitigation: Use the linked AgentPMT setup resources and fetch live schema or instructions before production integration when parameters, examples, or outputs are unclear. <br>
Risk: Decoding malformed Base64, URL-encoded, hexadecimal, binary, JSON-escaped, or Unicode-escaped input can fail validation. <br>
Mitigation: Validate input format before calling decode or unescape actions, and retry only after correcting schema, authentication, payment, or input errors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/data-format-encoder) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/data-format-encoder) <br>
- [Action Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, configuration] <br>
**Output Format:** [JSON responses containing transformed text and call metadata, with Markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All product actions require a text input; decoding actions can return validation errors for malformed input, and the evidence states processing uses UTF-8.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
