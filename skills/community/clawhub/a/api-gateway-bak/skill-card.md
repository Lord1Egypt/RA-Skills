## Description: <br>
Connects agents to 100+ external APIs through Maton's managed OAuth gateway for native endpoint access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonymd323](https://clawhub.ai/user/tonymd323) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to call third-party service APIs through Maton's gateway after the user has configured a Maton API key and authorized the relevant service connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers access to real connected services and can enable broad account actions. <br>
Mitigation: Install only when Maton is trusted for the connected services, and use least-privilege connections with read-only scopes where possible. <br>
Risk: Agent-driven API calls can perform high-impact write, delete, send, publish, payment, or admin actions. <br>
Mitigation: Require explicit user confirmation before any write, delete, send, publish, payment, or administrative action. <br>
Risk: API-key-based provider connections may not provide the same user-scoped OAuth protections. <br>
Mitigation: Treat API-key-based connections as higher risk, limit their scopes, and avoid exposing them to workflows that do not require them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonymd323/api-gateway-bak) <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and the MATON_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
