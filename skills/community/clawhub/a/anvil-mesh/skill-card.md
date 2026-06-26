## Description: <br>
Query the Anvil mesh network for live BSV data feeds, SPV transaction verification, and HTTP 402 micropayment service discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BSVanon](https://clawhub.ai/user/BSVanon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover Anvil nodes, query signed BSV data feeds, inspect HTTP 402 payment manifests, and request SPV transaction proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain-HTTP node or payment endpoints can expose users to tampered payment metadata, prices, addresses, or transaction proofs. <br>
Mitigation: Prefer HTTPS endpoints and independently verify endpoint identity, payment address, quoted price, and proof metadata before relying on results. <br>
Risk: HTTP 402 flows may initiate payment-capable workflows against third-party services. <br>
Mitigation: Only use trusted endpoints and confirm exact payment amount and recipient before creating or submitting a BSV transaction. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/BSVanon/anvil-mesh) <br>
- [Anvil GitHub repository](https://github.com/BSVanon/Anvil) <br>
- [Anvil Mesh SDK](https://www.npmjs.com/package/anvil-mesh) <br>
- [SendBSV profile](https://x.com/SendBSV) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; payment-capable requests may require independent verification of endpoint, price, address, and proof metadata.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
