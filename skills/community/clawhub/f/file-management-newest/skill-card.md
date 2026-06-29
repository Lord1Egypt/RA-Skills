## Description: <br>
File Management lets agents upload, list, retrieve, share, download, delete, and manage AgentPMT cloud-storage files with signed URLs, metadata updates, access history, and expiration controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to manage AgentPMT-hosted files across upload, retrieval, sharing, auditing, metadata, and expiration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded or shared files are handled by AgentPMT cloud storage and may include external data handling. <br>
Mitigation: Avoid sensitive files unless approved for AgentPMT storage, and keep uploads limited to the minimum content needed. <br>
Risk: Share links and signed URLs can expose files beyond the current agent run. <br>
Mitigation: Use short share and URL expiration limits where possible and confirm the target file before sharing. <br>
Risk: Delete operations permanently remove files from storage. <br>
Mitigation: Confirm the exact file identifier and intended file before invoking delete. <br>
Risk: Wallet and payment setup may require sensitive credentials or payment headers. <br>
Mitigation: Use the referenced setup skills for credential handling and do not place secrets, wallet keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [AgentPMT File Management marketplace page](https://www.agentpmt.com/marketplace/file-management) <br>
- [ClawHub File Management skill page](https://clawhub.ai/agentpmt/file-management-newest) <br>
- [File Management action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [AgentPMT no-account AgentAddress/x402 setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API request examples] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes AgentPMT MCP, REST, and x402 invocation patterns; product responses are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
