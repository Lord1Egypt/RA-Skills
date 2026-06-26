## Description: <br>
Teaches agents how to trade on the Fabric marketplace through search strategy, negotiation, offer lifecycle management, trust rules, and creative deal composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pilsang](https://clawhub.ai/user/pilsang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to integrate with Fabric marketplace workflows, including discovery, listing publication, offer construction, negotiation, contact reveal after mutual acceptance, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides high-impact marketplace actions involving trading, spending, offer acceptance, contact sharing, off-platform payments, and credential or access transfers. <br>
Mitigation: Require explicit human approval before purchases, public listings, offer acceptance, contact reveal, off-platform payments, or credential and access transfers. <br>
Risk: Off-platform settlement and counterparty contact details can expose users to unverified parties and irreversible payment methods. <br>
Mitigation: Verify counterparties, set spending limits, avoid irreversible payment methods with untrusted parties, and use approved settlement channels. <br>
Risk: API keys, delegated access, and webhook integrations may expose sensitive access if handled loosely. <br>
Mitigation: Use scoped, time-limited, revocable credentials and approved delegation mechanisms; store keys securely and verify signed webhooks when configured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pilsang/fabric-marketplace) <br>
- [Publisher Profile](https://clawhub.ai/user/pilsang) <br>
- [Getting Started](getting-started.md) <br>
- [Search Playbook](search-playbook.md) <br>
- [Negotiation Playbook](negotiation-playbook.md) <br>
- [Offer Lifecycle](offer-lifecycle.md) <br>
- [Trust and Safety](trust-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with HTTP examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing marketplace guidance; require human approval for high-impact trading, spending, contact reveal, payment, and credential-transfer actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
