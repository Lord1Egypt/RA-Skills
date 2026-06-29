## Description: <br>
Converts data between base64, hexadecimal, binary strings, and AgentPMT-hosted file/base64 workflows for upload, inspection, and download tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transform encoded payloads, inspect binary or file headers, and create or read temporary cloud-stored files in AgentPMT workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote conversion and temporary cloud file storage can expose secrets, regulated data, private documents, or other sensitive file contents. <br>
Mitigation: Send only the minimum content needed and avoid secrets, regulated data, or private documents unless remote AgentPMT processing is explicitly intended. <br>
Risk: Base64-to-file can return signed URLs that function as temporary shareable download links. <br>
Mitigation: Treat signed URLs as sensitive, avoid logging or broadly sharing them, and rely on the shortest practical expiration period. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/binary-to-from-file-converter) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/binary-to-from-file-converter) <br>
- [Generated Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [AgentPMT Overview](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [JSON tool responses with encoded strings, file metadata, and temporary signed download URLs; Markdown instructions with JSON request examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File-to-base64 inline returns are limited to 10 MB; base64-to-file outputs expire in 1-7 days and may include signed URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
