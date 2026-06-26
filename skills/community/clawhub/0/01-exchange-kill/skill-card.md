## Description: <br>
AI-powered 01.xyz exchange development skill for monitoring, trading strategies, and N1 blockchain integration. Covers REST API (FTX-inspired), Nord.ts SDK (@n1xyz/nord-ts), non-custodial trading patterns, and market making on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bouncyknighter](https://clawhub.ai/user/Bouncyknighter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to build 01.xyz market monitoring, SDK integration, account health tracking, and risk-aware trading workflows for the N1 blockchain ecosystem. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for real-money trading workflows on 01.xyz mainnet. <br>
Mitigation: Use devnet first, verify packages and endpoints from official sources, use a dedicated low-balance wallet, and require explicit confirmation before any order, withdrawal, deposit, or position-closing action. <br>
Risk: Trading actions depend on a local signing API that controls transaction signing. <br>
Mitigation: Keep the local signing API bound to the user's own machine, avoid exposing it on public servers, and never provide private keys to the agent. <br>
Risk: Perpetual futures trading can cause liquidation or loss of margin. <br>
Mitigation: Monitor margin health, validate strategies on devnet, use conservative position sizing, and configure circuit breakers, stop-losses, and manual kill switches. <br>


## Reference(s): <br>
- [01.xyz](https://01.xyz) <br>
- [01.xyz Developer Docs](https://docs.01.xyz) <br>
- [01.xyz API Reference](https://api.01.xyz) <br>
- [N1 Blockchain Docs](https://docs.n1.xyz) <br>
- [Skill overview](artifact/SKILLS.md) <br>
- [Safety guide](artifact/01xyz-developer-safety-first.md) <br>
- [Risk management guide](artifact/01xyz-developer-risk-management.md) <br>
- [SDK reference](artifact/01xyz-developer-sdk-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API examples, SDK setup steps, monitoring guidance, and risk-management checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
