## Description: <br>
Fresh Feeds helps agents find trending, new, and changed MCP servers and live x402 services using freshness-ranked, liveness-probed data with an x402-paid change-data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foomworks](https://clawhub.ai/user/foomworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to discover maintained MCP servers, verify a specific server's liveness and trust signals, inspect recent registry changes, and find x402-payable services that are currently responding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends discovery and verification queries to a hosted third-party service. <br>
Mitigation: Review query content before sending sensitive internal requirements or server names, and use free preview endpoints when full reports are not needed. <br>
Risk: Full datasets or reports may require x402 USDC micropayments when an agent has an automatic payment handler configured. <br>
Mitigation: Use free preview endpoints and ETag checks first, and configure wallet spending limits or disable automatic payment when cost control is required. <br>


## Reference(s): <br>
- [Fresh Feeds service](https://fresh-feeds.foomworks.workers.dev) <br>
- [Fresh Feeds remote MCP endpoint](https://fresh-feeds.foomworks.workers.dev/mcp) <br>
- [Fresh Feeds OpenAPI descriptor](https://fresh-feeds.foomworks.workers.dev/openapi.json) <br>
- [Fresh Feeds ClawHub listing](https://clawhub.ai/foomworks/skills/fresh-feeds) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown prose with endpoint lists and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Direct HTTP examples require curl; MCP clients can connect to the remote MCP endpoint instead.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
