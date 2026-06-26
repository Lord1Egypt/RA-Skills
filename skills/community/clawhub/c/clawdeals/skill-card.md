## Description: <br>
Operate Clawdeals via REST API (deals, watchlists, listings, offers, transactions). Includes safety constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thannous](https://clawhub.ai/user/thannous) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to work with Clawdeals marketplace resources through documented REST endpoints, including deals, watchlists, listings, offers, transactions, and event streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-paste examples can create or modify live Clawdeals marketplace resources when run with a production write key. <br>
Mitigation: Prefer read-only credentials unless writes are needed, and run smoke examples only against staging or a dedicated test account. <br>
Risk: Credentials and authorization headers could be exposed through logs, CI output, chats, or screenshots. <br>
Mitigation: Keep CLAWDEALS_API_KEY secret, do not enable command tracing around API calls, and redact Authorization headers and tokens from logs. <br>
Risk: Contact reveal can expose sensitive contact details and is difficult to reverse. <br>
Mitigation: Keep contact reveal approval-gated and require explicit human approval before releasing contact information. <br>
Risk: Optional MCP tooling is outside this docs-only bundle and may have a different security posture. <br>
Mitigation: Review the MCP package and installation flow separately before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thannous/clawdeals) <br>
- [Public skill documentation](https://clawdeals.com/skill.md) <br>
- [REST API reference](https://clawdeals.com/reference.md) <br>
- [Usage examples](https://clawdeals.com/examples.md) <br>
- [Policy guidance](https://clawdeals.com/policies.md) <br>
- [Security guidance](https://clawdeals.com/security.md) <br>
- [Optional MCP guide](https://clawdeals.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with REST API guidance, curl commands, and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWDEALS_API_BASE and CLAWDEALS_API_KEY; write examples require idempotency keys and can affect live Clawdeals resources.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata; artifact frontmatter reports 0.1.15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
