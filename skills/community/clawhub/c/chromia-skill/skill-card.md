## Description: <br>
Guides AI agents through Chromia blockchain dApp development using Rell, Chromia CLI (chr), and Postchain nodes, covering configuration, FT4 accounts, cross-chain communication, EVM integration, NFT standards, Filehub storage, TypeScript clients, AI extensions, and deployment pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deconsoleapp](https://clawhub.ai/user/deconsoleapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, configure, implement, test, and deploy Chromia dApps with Rell, Chromia CLI, Postchain clients, FT4, cross-chain integrations, Filehub, and related Chromia extensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys or mnemonics may be exposed during wallet, admin, or deployment workflows. <br>
Mitigation: Keep real private keys out of chat, logs, source control, and browser or client code; use secure key management for production. <br>
Risk: Deployment update, remove, auto-confirm, or local wipe commands can change or destroy blockchain state. <br>
Mitigation: Before running deployment create/update/remove, using -y, or running chr node start --wipe, verify the network, blockchain name, container, key identity, and whether state loss or removal is acceptable. <br>
Risk: On-chain storage may expose secrets, personal data, regulated data, or confidential prompts and outputs. <br>
Mitigation: Do not store secrets, personal data, regulated data, or confidential prompts and outputs on-chain. <br>


## Reference(s): <br>
- [Chromia Skill Source](https://bitbucket.org/chromawallet/chromia-skill/src) <br>
- [AI & Extensions Reference](references/ai-extensions.md) <br>
- [CRC2 NFT Standard Reference](references/crc2-nft.md) <br>
- [Deployment](references/deployment.md) <br>
- [EIF (Ethereum Interoperability Framework) Reference](references/eif-evm.md) <br>
- [Filehub Reference](references/filehub.md) <br>
- [FT4 Integration Reference](references/ft4-integration.md) <br>
- [Governance & Provider Staking Reference](references/governance.md) <br>
- [ICCF & ICMF Cross-Chain Communication Reference](references/iccf-icmf.md) <br>
- [Postchain Client Reference](references/postchain-client.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Chromia CLI binary `chr` for CLI-based workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
