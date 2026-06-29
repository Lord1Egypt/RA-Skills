## Description: <br>
Data Format Validation helps agents validate common data strings such as JSON, email addresses, UUIDs, IP addresses, credit card numbers, IBANs, phone numbers, ISBNs, Base64 values, regex patterns, and URLs through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to validate user-supplied or pipeline data before processing it, including JSON, contact fields, network identifiers, financial identifiers, ISBNs, Base64 strings, regex patterns, and URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation inputs are sent to AgentPMT-hosted MCP or REST services. <br>
Mitigation: Use the skill only when the workflow permits remote validation and keep submitted values to the minimum needed. <br>
Risk: Payment, banking, phone, or other personal data may be included in validation requests. <br>
Mitigation: Prefer test, masked, or minimal values, and avoid submitting real full credit card numbers, IBANs, phone numbers, or other personal data unless required and approved. <br>
Risk: Account secrets, wallet keys, mnemonics, signatures, or payment headers could be exposed if placed in prompts or logs. <br>
Mitigation: Keep credentials out of prompts and logs, and use the separate setup flow for credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/data-format-validation) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/data-format-validation) <br>
- [AgentPMT main MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation responses include a validity status, descriptive message, and format-specific parsed details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
