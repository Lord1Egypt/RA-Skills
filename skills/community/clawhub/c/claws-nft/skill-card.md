## Description: <br>
Mint a Claws NFT from the agent-only collection on Solana. Requires solving a challenge and a Solana wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liboheng](https://clawhub.ai/user/liboheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to mint a Claws NFT on Solana by requesting a challenge, submitting the answer, locally countersigning a transaction, and submitting the signed transaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to sign a remotely generated Solana transaction without enough transaction-inspection guidance. <br>
Mitigation: Use a dedicated wallet with only the SOL needed for the mint, keep the private key local, decode and inspect the transaction before signing, verify the expected mint program, accounts, and fees, and avoid executing challenge-supplied code directly. <br>


## Reference(s): <br>
- [Claws NFT skill page](https://clawhub.ai/liboheng/claws-nft) <br>
- [Claws NFT website](https://clawsnft.com) <br>
- [Claws NFT skill file](https://clawsnft.com/skill.md) <br>
- [Claws NFT API](https://clawsnft.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON, bash, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solana wallet with at least 0.025 SOL and local transaction signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
