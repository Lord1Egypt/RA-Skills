## Description: <br>
Binary To/From File Converter converts data between base64, hexadecimal, and binary representations, and supports file-to-base64 and base64-to-file workflows through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert payloads among base64, hex, binary strings, and temporary cloud-backed files for API transmission, attachment decoding, file reconstruction, and binary inspection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs and generated files are processed by AgentPMT-hosted remote conversion services and may be exposed through temporary cloud file links. <br>
Mitigation: Use the skill only for content that can be sent to AgentPMT; avoid passwords, keys, regulated records, private business documents, and malware samples unless that exposure is acceptable. <br>
Risk: Temporary signed URLs returned by base64-to-file can provide access to converted files until they expire. <br>
Mitigation: Choose the shortest practical expiration period, share URLs only with intended recipients, and avoid storing sensitive content through base64-to-file. <br>
Risk: File-to-base64 returns inline content only up to the documented 10 MB limit. <br>
Mitigation: Check file size before requesting inline base64 output and use another transfer path for larger files. <br>


## Reference(s): <br>
- [Artifact action schema](artifact/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/binary-to-from-file-converter) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/binary-to-from-file-converter) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [AgentPMT overview](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT main MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces action schemas, example request bodies, remote tool invocation guidance, and guidance for handling JSON responses and temporary signed file URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
