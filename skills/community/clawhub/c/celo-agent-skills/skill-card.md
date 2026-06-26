## Description: <br>
Celo Agent Skills is an end-to-end Celo development playbook covering viem-first transaction code, thirdweb wallet and React dApp patterns, Foundry smart contract workflows, MiniPay, stablecoins, fee abstraction, ERC-8004 trust, and x402 payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viral-sangani](https://clawhub.ai/user/viral-sangani) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Celo dApps, smart contracts, MiniPay experiences, stablecoin payment flows, and AI-agent payment or trust integrations. It helps agents choose appropriate Celo tooling, generate code, configure networks, and provide testing, deployment, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and generated workflows may deploy contracts, transfer or approve assets, bridge funds, make x402 payments, or broadcast raw transactions. <br>
Mitigation: Use testnets first and require explicit human confirmation before any deploy, transfer, approval, bridge, x402 payment, or raw transaction broadcast. <br>
Risk: Wallet data, private keys, mnemonics, and API keys can be exposed through generated code, logs, or source control. <br>
Mitigation: Keep secrets out of source control and logs, use environment-based secret handling, and review generated code before running it. <br>
Risk: MiniPay and local testing guidance may expose local services through ngrok. <br>
Mitigation: Expose local services only for intentional testing, scope tunnels to the needed service, and shut them down after testing. <br>
Risk: Generated production code or command sequences may contain incorrect or incomplete blockchain assumptions. <br>
Mitigation: Review and scan generated changes before deployment, verify network IDs and contract addresses, and run tests against the intended Celo network. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/viral-sangani/celo-agent-skills) <br>
- [Root Celo Development Skill](artifact/skill.md) <br>
- [Celo Fee Currency Guide](https://docs.celo.org/developer/fee-currency) <br>
- [Celo MiniPay Documentation](https://docs.celo.org/build-with-celo/minipay) <br>
- [Celo Token Contracts](https://docs.celo.org/tooling/contracts/token-contracts) <br>
- [Celo Core Contracts](https://docs.celo.org/tooling/contracts/core-contracts) <br>
- [viem Celo Chain Documentation](https://viem.sh/docs/chains/celo) <br>
- [thirdweb x402 Documentation](https://portal.thirdweb.com/x402) <br>
- [ERC-8004 EIP Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [Fee Currency Reference](artifact/skills/fee-abstraction/references/fee-currencies.md) <br>
- [MiniPay Testing Guide](artifact/skills/minipay-integration/references/testing-guide.md) <br>
- [Contract Verification Configuration](artifact/skills/contract-verification/references/verification-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Celo network, fee currency, wallet compatibility, testing, deployment, and verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
