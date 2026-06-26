## Description: <br>
Framework-agnostic agent-to-agent SHIB payment system on Polygon with payment, escrow workflow, price negotiation, and reputation features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcus20232023](https://clawhub.ai/user/marcus20232023) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent operators use this skill to let A2A-compatible agents check balances, send SHIB payments, negotiate service prices, coordinate escrow-like workflows, and track counterparty reputation on Polygon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds and has weak defaults for a financial workflow. <br>
Mitigation: Use a low-value hot wallet, set conservative payment limits, rotate API keys, and test all payment paths before use. <br>
Risk: Exposing the default full agent to the internet can create unnecessary payment and key-management exposure. <br>
Mitigation: Avoid public exposure of the default full agent; use the production-oriented setup only after hardening authentication, transport security, and logging. <br>
Risk: The escrow claims should not be treated as independently verified trustless on-chain custody. <br>
Mitigation: Require independent code review and additional testing before relying on escrow behavior for meaningful value. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcus20232023/a2a-shib-payments) <br>
- [Deployment guide](artifact/DEPLOYMENT.md) <br>
- [Escrow and negotiation guide](artifact/ESCROW-NEGOTIATION-GUIDE.md) <br>
- [Integration examples](artifact/INTEGRATION-EXAMPLES.md) <br>
- [Production hardening guide](artifact/PRODUCTION-HARDENING.md) <br>
- [A2A Protocol](https://a2a-protocol.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON API responses, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JavaScript examples, shell commands, and JSON-RPC or REST API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm; payment operations require a configured Polygon wallet, RPC endpoint, and SHIB token configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
