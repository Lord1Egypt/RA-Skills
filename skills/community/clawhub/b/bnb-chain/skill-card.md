## Description: <br>
Basic BNB Chain operations: check balances, send BNB, send BEP-20 tokens, derive wallet addresses, and inspect transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CLAWZAI](https://clawhub.ai/user/CLAWZAI) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to perform basic BNB Chain wallet and token operations from a Node.js helper script, including balance checks, token transfers, BNB transfers, address derivation, and transaction lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend cryptocurrency with a raw private key and has no built-in confirmation step before submitting BNB or BEP-20 transfers. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing private keys on the command line, prefer controlled secret storage, and manually verify the network, recipient address, token contract, and amount before any send operation. <br>
Risk: Private keys may be exposed if they are committed, logged, stored in shell history, or shared through command arguments. <br>
Mitigation: Keep private keys out of git and logs, use environment variables or a managed secret mechanism, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CLAWZAI/bnb-chain) <br>
- [CLAWZAI publisher profile](https://clawhub.ai/user/CLAWZAI) <br>
- [BNB Chain default RPC endpoint](https://bsc-dataseed.binance.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and ethers.js; reads BNB_PRIVATE_KEY and BNB_RPC_URL from the environment, with optional command-line private key input.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
