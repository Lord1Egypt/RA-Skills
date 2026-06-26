## Description: <br>
Agent Sovereign Stack helps agents register identity on-chain, upload memory to decentralized storage, configure treasury controls, and set up agent-to-agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quriustus](https://clawhub.ai/user/quriustus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard an AI agent into decentralized identity, memory storage, on-chain registration, treasury policy setup, and mailbox-style agent communication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys and may initiate blockchain transactions or treasury deployment. <br>
Mitigation: Use only a fresh low-balance testnet wallet, verify contract addresses and Foundry commands before signing, and avoid primary wallet keys. <br>
Risk: The skill uploads identity and memory files to external decentralized storage endpoints where data may be exposed or difficult to remove. <br>
Mitigation: Inspect and redact SOUL.md, MEMORY.md, identity snapshots, and other files before upload, and assume uploaded data may persist. <br>
Risk: The security review notes advertised encryption or signing should not be relied on until implemented. <br>
Mitigation: Treat messages and uploaded memory as unencrypted unless independent code review confirms encryption and signing behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quriustus/agent-sovereign-stack) <br>
- [Publisher profile](https://clawhub.ai/user/quriustus) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with Python scripts and command-line configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces onboarding summaries, local configuration files, memory CIDs, contract addresses, and mailbox endpoints when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
