## Description: <br>
Enables OpenClaw agents to make private FHE-encrypted on-chain payments, wrap and unwrap encrypted tokens, manage escrow jobs, register agent identity, give reputation feedback, and delegate encrypted balance viewing on Ethereum Sepolia or Mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billynothack](https://clawhub.ai/user/billynothack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to let agents perform confidential token payments, paid x402 requests, escrow-based agent commerce, identity registration, reputation feedback, and delegated encrypted balance viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real blockchain transactions and make paid x402 requests from command arguments without built-in confirmation or spend limits. <br>
Mitigation: Start on Sepolia and verify the chain, contract addresses, recipients, amounts, and delegation targets before each run. <br>
Risk: A raw private key wallet mode can expose funds if secrets are mishandled. <br>
Mitigation: Prefer Ledger or DFNS for signing, and restrict USER_PRIVATE_KEY use to local testing with protected environment variables. <br>
Risk: Demo API commands may send prompts, code, or other content to configured paid services. <br>
Mitigation: Use demo API commands only with trusted services and avoid sending sensitive prompts or proprietary code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/billynothack/confidential-agentic-payment-stack) <br>
- [Project homepage](https://gitlab.com/bea7892046/fhex402) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Blockchain transactions, Configuration] <br>
**Output Format:** [JSON strings with ok/error status, transaction metadata, balances, payment proofs, and contract information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return transaction hashes, encrypted balance handles, payment receipts, Etherscan URLs, and delegation status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
