## Description: <br>
Ask a question in plain English, get data from 13,000+ APIs in one call, including crypto prices, social data, and market intelligence, with cryptographically signed responses and optional x402 payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1xmint](https://clawhub.ai/user/1xmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Claw-Net to route natural-language data questions to external data APIs, browse available data skills, estimate costs, and retrieve structured or synthesized responses. It is especially oriented toward market, crypto, social, and provenance-aware data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and payloads are sent to the external ClawNet API and may contain sensitive business, wallet, or personal data. <br>
Mitigation: Confirm trust in ClawNet before use, avoid unnecessary sensitive data in prompts and variables, and configure CLAWNET_API_KEY only for this service. <br>
Risk: Protected endpoints require an API key, credits, or paid x402 calls that may incur charges. <br>
Mitigation: Use free browse endpoints and cost-estimation endpoints before paid calls, and monitor credit or wallet usage. <br>
Risk: Returned market or API data may be time-sensitive or decision-impacting. <br>
Mitigation: Cross-reference important results against independent sources before acting on business, financial, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/1xmint/claw-net) <br>
- [Claw-Net homepage](https://claw-net.org) <br>
- [Claw-Net SOMA identity](https://api.claw-net.org/.well-known/soma.json) <br>
- [ClawNet API base](https://api.claw-net.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWNET_API_KEY for protected endpoints or wallet-based x402 payment for paid calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
