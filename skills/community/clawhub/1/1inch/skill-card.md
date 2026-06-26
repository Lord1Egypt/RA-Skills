## Description: <br>
Provides a Python client for the 1inch API v5.2 to request DEX trade quotes and prepare token swap transaction data across supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric1099281](https://clawhub.ai/user/eric1099281) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call 1inch quote, token, spender, approval, and swap helpers when preparing DEX aggregation workflows. It is intended to return trade and transaction data for review and signing through a trusted wallet or signing flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval and swap transaction data can authorize token movement or execute financially sensitive trades. <br>
Mitigation: Before signing, independently verify the chain, token addresses, amount, spender or router address, slippage, expected output, and gas fees in a trusted wallet or signing flow. <br>
Risk: Supplying private keys to an agent or script can expose wallet funds. <br>
Mitigation: Do not provide private keys to the agent; use a trusted wallet, hardware signer, or controlled signing service. <br>
Risk: The API client depends on a valid external 1inch API key and live service responses. <br>
Mitigation: Configure the API key outside generated code, handle API errors and rate limits, and review returned transaction data before broadcasting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eric1099281/1inch) <br>
- [1inch Developer Portal](https://portal.1inch.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python code examples that return JSON-like API response dictionaries and transaction-data objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a 1inch API key and user-supplied chain, token, amount, wallet, slippage, approval, and swap parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
