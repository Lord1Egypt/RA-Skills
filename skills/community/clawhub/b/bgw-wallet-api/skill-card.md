## Description: <br>
Interact with Bitget Wallet API for crypto market data, token info, swap quotes, and security audits across supported chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karryzhang](https://clawhub.ai/user/karryzhang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query crypto market and token security data, generate swap or order quotes, and prepare wallet-mediated transaction workflows with human confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle wallet private keys and submit signed crypto transactions. <br>
Mitigation: Do not paste wallet private keys into the agent or pass them on the command line; prefer an external wallet, hardware signer, or dedicated signer, and require explicit confirmation before signing, order-submit, or swap-send. <br>
Risk: Replacing the skill without review could change credential handling, network endpoints, or transaction behavior. <br>
Mitigation: Pin and review updates before replacing the skill, and inspect changes to transaction, signing, credential, and network code. <br>
Risk: Swap and order workflows can affect user funds if token, amount, fee, or routing details are misunderstood. <br>
Mitigation: Review every quote, token security result, transaction deadline, order detail, and signing request before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/karryzhang/bgw-wallet-api) <br>
- [Bitget Wallet API Documentation](https://web3.bitget.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include unsigned transaction data, signed transaction strings, swap quotes, security audit summaries, and order status details.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2026.3.5-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
