## Description: <br>
File To JSON Parsing converts CSV, HTML, JSON, ICS, ODS, PDF, RTF, plain text, XLS, and XLSX files into structured JSON output from base64 content or cloud file IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this AgentPMT-hosted skill to parse uploaded files into JSON for database import, API submission, scheduling integrations, document processing, and data transformation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected file contents or cloud file IDs are sent to AgentPMT for remote processing. <br>
Mitigation: Use only files approved for transfer to AgentPMT, and avoid secrets, credentials, highly sensitive personal data, legal or medical records, and confidential business files unless explicit approval and acceptable retention terms are in place. <br>
Risk: The skill requires AgentPMT account setup and may involve credentials or payment headers in surrounding setup workflows. <br>
Mitigation: Use the setup skills for credential handling and keep account secrets, wallet private keys, mnemonics, signatures, and payment headers out of prompts and logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/file-to-json-parsing) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/file-to-json-parsing) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides remote AgentPMT MCP or REST calls that return structured JSON from selected file inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
