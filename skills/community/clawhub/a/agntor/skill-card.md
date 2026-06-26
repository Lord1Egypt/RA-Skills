## Description: <br>
Trust layer for AI agents: verify identities, guard prompts, redact PII, and manage x402 escrow payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Garinmckayl](https://clawhub.ai/user/Garinmckayl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Agntor to check agent identity and trust, scan prompts, redact sensitive output, and coordinate escrow-backed agent transactions through an MCP connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and administration actions such as escrow creation, audit tickets, registration, verification probes, or kill-switch use can have financial or operational impact. <br>
Mitigation: Require explicit human approval before those actions and use a least-privilege Agntor API key. <br>
Risk: Redaction and trust-check workflows may submit sensitive content to Agntor without clear data-handling boundaries. <br>
Mitigation: Confirm processing and retention expectations before sending secrets, logs, PII, or regulated data. <br>
Risk: The MCP package and external tool calls can expand what the agent is able to do. <br>
Mitigation: Pin or review the @agntor/mcp package and restrict the environment variable and tool permissions to the minimum needed. <br>


## Reference(s): <br>
- [Agntor GitHub](https://github.com/agntor/agntor) <br>
- [Agntor Docs](https://docs.agntor.com) <br>
- [Agntor Dashboard](https://app.agntor.com) <br>
- [Agntor SDK on npm](https://www.npmjs.com/package/@agntor/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown with JSON configuration snippets and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTOR_API_KEY for the MCP connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
