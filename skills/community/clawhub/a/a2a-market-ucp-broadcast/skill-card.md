## Description: <br>
Implements UCP broadcast of buyer intents to eligible nodes, including message signing, routing, acknowledgement handling, and quote-intake response streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Universal Commerce Protocol publish/subscribe behavior that signs buyer intent messages, broadcasts them to eligible nodes, tracks acknowledgements, and feeds quote responses into intake. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signing keys or buyer intents could be exposed if they are logged or stored too broadly. <br>
Mitigation: Keep signing keys in a secure scoped key store, avoid logging private keys or full buyer intents, and review any referenced runtime package before production use. <br>
Risk: Broadcasts could reach unauthenticated or unapproved nodes. <br>
Mitigation: Send broadcasts only to authenticated, approved nodes, and enforce per-node acknowledgement tracking and retry thresholds. <br>
Risk: Inconsistent message serialization or missing protocol versions could break signature verification and interoperability. <br>
Mitigation: Use deterministic canonical JSON serialization and attach the protocol version to every broadcast envelope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-market-ucp-broadcast) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with implementation contracts and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes signing, routing, acknowledgement, retry, and protocol-version guardrails; no shell execution is requested.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
