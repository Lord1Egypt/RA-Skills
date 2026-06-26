## Description: <br>
Purchase travel eSIM data plans using USDC on Base Mainnet or Base Sepolia through x402, then deliver an eSIM installation page with QR-code setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inthaiguy](https://clawhub.ai/user/inthaiguy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to search travel eSIM packages by country, quote prices, coordinate USDC payment, and return the resulting installation link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mainnet purchases can spend real USDC and incur gas fees. <br>
Mitigation: Confirm the network, package, USDC amount, token contract, recipient address, and gas fee before approving payment; use testnet or a limited-balance wallet for testing. <br>
Risk: The flow depends on the external esimqr.link service and dynamically returned payment addresses. <br>
Mitigation: Install only if the service is trusted and use payment details returned by the quote or 402 response rather than hardcoded addresses. <br>
Risk: The API rate limit is 10 requests per minute per IP. <br>
Mitigation: Handle HTTP 429 responses by respecting the Retry-After header before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inthaiguy/get-esim) <br>
- [Mainnet agent API documentation](https://esimqr.link/api/agent/docs) <br>
- [Testnet agent API documentation](https://esimqr.link/api/agent-testnet/docs) <br>
- [Agent landing page](https://esimqr.link/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API details, command examples, and Python client code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include eSIM package options, quote details, transaction status, and installation URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
