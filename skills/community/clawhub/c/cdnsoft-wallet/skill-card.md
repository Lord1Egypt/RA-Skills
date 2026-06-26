## Description: <br>
EVM wallet tool for autonomous agents that creates, signs, and broadcasts ETH and ERC20 transfers on EVM-compatible chains, then appends every transaction to a JSON log file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cromatikap](https://clawhub.ai/user/cromatikap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to send ETH or ERC20 payments, make x402-gated API requests, perform supported Uniswap V3 swaps, and maintain a local JSON audit log of wallet activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign irreversible crypto transactions and x402 payments with broad wallet authority. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit approval for every transaction, and prefer allowlisted recipients, RPC endpoints, and API domains. <br>
Risk: x402 requests or swaps could spend more than intended or execute with unfavorable terms. <br>
Mitigation: Set x402 --max-amount, set swap --min-out, and use --pay-to when the payment address is known and stable. <br>
Risk: Arbitrary contract calls through --calldata can execute opaque on-chain behavior. <br>
Mitigation: Avoid --calldata unless a human can decode and verify the exact contract call before signing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cromatikap/cdnsoft-wallet) <br>
- [Agentwallet documentation](https://cdnsoft.github.io/agentwallet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON transaction logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates a local agentwallet.json transaction log when the scripts are run.] <br>

## Skill Version(s): <br>
0.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
