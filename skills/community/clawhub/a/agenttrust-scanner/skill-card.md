## Description: <br>
AgentTrust scans AI agent skills and MCP manifests for security issues and returns signed ACT/HALT receipts, findings, and trust guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poteshniy](https://clawhub.ai/user/poteshniy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan SKILL.md content, MCP manifests, endpoints, wallet addresses, or content hashes before an agent acts or pays. It helps produce security findings, trust scores, and signed verification receipts for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected skill content, MCP manifests, endpoint URLs, wallet addresses, or hashes may be sent to agenttrust.uk for analysis. <br>
Mitigation: Submit only content the user is comfortable sharing with AgentTrust, and prefer free endpoints when they are sufficient. <br>
Risk: Some full scans, wallet lookups, integrity checks, and reports require paid x402/USDC actions. <br>
Mitigation: Ask for explicit approval before any paid action, and disclose the exact price and input being submitted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/poteshniy/skills/agenttrust-scanner) <br>
- [AgentTrust service](https://agenttrust.uk) <br>
- [IETF verification-state draft](https://datatracker.ietf.org/doc/draft-krausz-verification-state/) <br>
- [AgentTrust JWKS](https://agenttrust.uk/.well-known/jwks.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request details, JSON request and response descriptions, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external AgentTrust endpoints; paid x402/USDC actions require explicit user approval.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
