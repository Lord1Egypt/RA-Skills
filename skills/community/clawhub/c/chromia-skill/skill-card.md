## Description:

Guides AI agents through Chromia blockchain dApp development with Rell, Chromia CLI, Postchain nodes, and related integrations including FT4, ICCF/ICMF, EIF, CRC2, Filehub, and TypeScript clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deconsoleapp](https://clawhub.ai/user/deconsoleapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, test, and deploy Chromia dApps with Rell, Chromia CLI, Postchain, FT4, cross-chain messaging, EVM interoperability, NFTs, decentralized storage, and TypeScript clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production signing keys may be mishandled if copied into project .env files or browser/client code.

Mitigation: Keep production admin private keys out of generated project files and client-side bundles; use controlled signing workflows and review secret handling before deployment.

Risk: Deployment commands using -y, --wipe, or deployment remove can make high-impact changes without adequate confirmation.

Mitigation: Independently verify the target network, container, key, and destructive operation before execution; require explicit confirmation for reset or removal commands.

## Reference(s):

- [Chromia Skill Source](https://bitbucket.org/chromawallet/chromia-skill/src)
- [Chromia Skill on ClawHub](https://clawhub.ai/deconsoleapp/skills/chromia-skill)
- [AI & Extensions Reference](references/ai-extensions.md)
- [CRC2 NFT Standard Reference](references/crc2-nft.md)
- [Deployment](references/deployment.md)
- [EIF Ethereum Interoperability Framework Reference](references/eif-evm.md)
- [Filehub Reference](references/filehub.md)
- [FT4 Integration Reference](references/ft4-integration.md)
- [Governance & Provider Staking Reference](references/governance.md)
- [ICCF & ICMF Cross-Chain Communication Reference](references/iccf-icmf.md)
- [Postchain Client Reference](references/postchain-client.md)
- [FT4 Library](https://gitlab.com/chromaway/ft4-lib.git)
- [Directory Chain Library](https://gitlab.com/chromaway/core/directory-chain)
- [VectorDB Extension](https://gitlab.com/chromaway/core/vectordb-extension)
- [Stork Oracle Chromia Extension](https://gitlab.com/chromaway/core/stork-oracle-chromia-extension)
- [CRC2 Library](https://gitlab.com/chromaway/crc2-lib)
- [CRC2 Bridge Demo](https://bitbucket.org/chromawallet/crc2-bridge-demo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Chromia CLI binary chr for command execution.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
