## Description: <br>
SynapseAI Merchant lets AI agents register as merchants, create receiving wallets and payment links, configure webhooks, and receive on-chain payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandagg110](https://clawhub.ai/user/pandagg110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to add merchant payment receiving flows, including wallet creation, payment links, QR-code payment pages, webhook notifications, and payment history queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority over merchant payment receiving, wallet creation, payment links, webhooks, and receiving status. <br>
Mitigation: Use a narrowly scoped token where available and require confirmation of wallet, payment link, amount, webhook URL, and status-change requests before API calls are sent. <br>
Risk: The security evidence says the skill depends on trust in SynapseAI's wallet service. <br>
Mitigation: Install only when the wallet service is trusted for the intended payment flow and monitor merchant activity through payment history and ledger queries. <br>
Risk: The skill includes an agent toggle endpoint that can also change broader agent spending status. <br>
Mitigation: Avoid sending spending-status toggle fields from this merchant flow unless the operator explicitly intends to change agent spending behavior. <br>
Risk: Webhook callbacks can affect fulfillment decisions after payment events. <br>
Mitigation: Store webhook secrets securely and verify webhook signatures before delivering products or services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pandagg110/agent-to-merchant) <br>
- [SynapseAI Wallet homepage](https://wallet.synapseai.pro) <br>
- [SynapseAI Merchant API](https://wallet.synapseai.pro/api/merchant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with HTTP request and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes merchant API endpoints, request bodies, response examples, webhook setup notes, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
