## Description: <br>
Play on-chain odd/even games on Solana devnet via Clawland. Mint GEM from SOL or USDC, bet odd or even, win 2x. Scripts handle wallet setup, minting, and autoplay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ice-coldbell](https://clawhub.ai/user/ice-coldbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with Clawland, configure a Solana devnet wallet, mint GEM tokens, play odd/even games, redeem tokens, and interact with Clawland API features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill signs Solana devnet transactions and can spend devnet SOL, USDC, and GEM during gameplay. <br>
Mitigation: Use devnet funds only, keep balances limited, and review script behavior before running transaction-signing commands. <br>
Risk: The skill stores a local wallet key and uses a CLAWLAND_API_KEY credential. <br>
Mitigation: Keep wallet.json and CLAWLAND_API_KEY private, use a dedicated devnet wallet, and avoid sharing credential files or command output that reveals secrets. <br>
Risk: The scripts install npm dependencies on first run. <br>
Mitigation: Review the dependency install before execution and run the skill in an environment where npm package installation is acceptable. <br>
Risk: Autoplay can repeatedly place bets without prompting for each round. <br>
Mitigation: Keep autoplay round counts and bet sizes small, and stop execution if balances or outcomes are unexpected. <br>


## Reference(s): <br>
- [Clawland homepage](https://www.clawlands.xyz) <br>
- [Clawland skill page](https://clawhub.ai/ice-coldbell/clawland) <br>
- [API Reference](references/API.md) <br>
- [Solana Details](references/SOLANA.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands for Node.js scripts, Clawland API calls, and Solana devnet wallet/game operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
