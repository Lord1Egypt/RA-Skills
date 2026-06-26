## Description: <br>
Use when an agent needs one universal entrypoint to discover and use the unified Clash of Coins gateway for sale and shop flows, choose the active protocol on the live instance, and execute purchase or integration workflows without mixing contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clash-deployer](https://clawhub.ai/user/clash-deployer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover a live Clash of Coins gateway, select the correct sale or shop surface, choose the active x402 or MPP payment protocol, and return endpoint-level checkout or integration guidance. It is intended for flows where the agent must validate route, recipient, protocol, and payment status before any spending action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers quote, buy, order creation, wallet funding, and payment retry flows that can initiate real spending actions. <br>
Mitigation: Verify the origin, item, recipient, amount, protocol, endpoint, and status route before allowing the agent to proceed with any checkout or funding step. <br>
Risk: A sale route and shop route can use different contracts and recipient rules. <br>
Mitigation: Use live discovery and catalog metadata to select exactly one surface and protocol, and stop if the selected item does not match the target buy endpoint. <br>
Risk: Shop checkout can be misdirected if recipient fields are missing or ambiguous. <br>
Mitigation: Require exactly one recipient identifier, either nickname or address, before shop quote or buy calls. <br>
Risk: Treating an unpaid payment challenge or pending fulfillment as success can misreport purchase completion. <br>
Mitigation: Preserve retry payloads exactly for paid retries and confirm settlement through the documented purchase-status or ledger endpoint. <br>


## Reference(s): <br>
- [Clash of Coins - Agentic Gateway](https://clawhub.ai/clash-deployer/clash-of-coins-agentic) <br>
- [Client Installation](references/client-installation.md) <br>
- [Discovery And Routing](references/discovery-and-routing.md) <br>
- [Integration Playbook](references/integration-playbook.md) <br>
- [Purchase Playbooks](references/purchase-playbooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with endpoint paths, JSON payload constraints, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a concise Clash of Coins handoff with origin, enabled protocols, selected surface, next endpoint, payload constraints, payment retry rule, status endpoint, and risks.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
