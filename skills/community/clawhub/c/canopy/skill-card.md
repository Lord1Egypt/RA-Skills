## Description: <br>
Canopy lets AI agents make policy-gated USD payments on Base, pay x402 or MPP paywalled APIs, and discover paid services while enforcing spend caps, allowlists, approval thresholds, and human approval for higher-risk payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atifazam](https://clawhub.ai/user/atifazam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and organizations use Canopy to let an agent spend from a Canopy treasury through an MCP server while applying per-agent payment policies. It is intended for agents that need to send USD payments, check paywalled API offers, discover paid services, or manage explicit human approval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can initiate real payments through a Canopy treasury wallet. <br>
Mitigation: Install the skill only for agents that intentionally need treasury access, and configure least-privileged Canopy agents with tight spend caps and allowlists. <br>
Risk: Approval tools can authorize pending payments if used without clear user intent. <br>
Mitigation: Require explicit human approval, show the recipient and amount before approval, and never auto-approve on the user's behalf. <br>
Risk: The MCP server requires sensitive Canopy credentials. <br>
Mitigation: Store CANOPY_API_KEY and CANOPY_AGENT_ID as secrets, verify the MCP URL and dashboard, and rotate or remove credentials when access is no longer needed. <br>
Risk: Denied payments could be split into smaller transactions to bypass policy limits. <br>
Mitigation: Do not chunk denied payments; surface the policy reason and direct the user to adjust the policy in the dashboard if appropriate. <br>


## Reference(s): <br>
- [Canopy ClawHub listing](https://clawhub.ai/atifazam/canopy) <br>
- [Canopy homepage](https://www.trycanopy.ai) <br>
- [Canopy MCP tools reference](https://www.trycanopy.ai/documentation/reference/mcp-tools) <br>
- [Payment outcomes](https://www.trycanopy.ai/documentation/concepts/payment-outcomes) <br>
- [Policies](https://www.trycanopy.ai/documentation/concepts/policies) <br>
- [x402 protocol](https://www.trycanopy.ai/documentation/concepts/x402) <br>
- [Connect MCP hosts](https://www.trycanopy.ai/documentation/connect/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CANOPY_API_KEY and CANOPY_AGENT_ID credentials for the Canopy MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
