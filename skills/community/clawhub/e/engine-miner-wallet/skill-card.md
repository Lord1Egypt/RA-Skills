## Description: <br>
Secure operating guidance for the Engine miner Taproot wallet plugin on OpenClaw. Use for registration signing, safe claim handling, and refusal of unsafe wallet actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kerimatalayturkish-dotcom](https://clawhub.ai/user/kerimatalayturkish-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Engine miner wallet plugin safely, including wallet creation, Taproot payout-address retrieval, registration challenge signing, and claim workflow guidance. It emphasizes claim-first wallet behavior, sensitive recovery-phrase handling, and refusal of unsafe wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery phrases can control funds or claims if exposed. <br>
Mitigation: Show the recovery phrase only during explicit wallet creation after warning and confirmation, then direct the user to store it offline and never paste it back into chat. <br>
Risk: Wallet passphrases entered into chat can compromise encrypted storage. <br>
Mitigation: Tell users to set ENGINE_MINER_WALLET_PASSPHRASE locally instead of sharing the passphrase with the agent. <br>
Risk: Generic transfer or unrecognized signing requests could move the wallet outside its claim-first purpose. <br>
Mitigation: Refuse generic send-to-any-address actions and only sign or broadcast recognized Engine miner workflows after explicit user confirmation. <br>
Risk: Claim settlement behavior is not fully complete in this version. <br>
Mitigation: Describe claim commands as planned workflow commands until tool output and release notes confirm receipt verification, prepared claim validation, signing, and broadcast policy completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kerimatalayturkish-dotcom/engine-miner-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/kerimatalayturkish-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline commands and wallet workflow mappings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety boundaries for recovery phrases, passphrases, signing, claim preparation, and broadcast confirmation.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
