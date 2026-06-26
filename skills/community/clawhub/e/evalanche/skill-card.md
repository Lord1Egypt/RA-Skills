## Description: <br>
Evalanche is a multi-EVM agent wallet SDK for autonomous wallet operation, on-chain identity, payment-gated requests, cross-chain liquidity, trading, market intelligence, prediction markets, and DeFi actions across supported EVM and Avalanche networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ijaack](https://clawhub.ai/user/ijaack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate blockchain wallets, query markets, move funds, execute trades, bridge assets, and perform DeFi workflows through CLI or MCP interfaces. It is intended for environments where wallet credentials, transaction authority, spending limits, and chain policies are controlled before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous agents can move funds, trade, bridge assets, and use private keys. <br>
Mitigation: Use a dedicated low-balance wallet and enforce strict confirmation, spending-limit, approved-chain, approved-contract, and trade-size policies before enabling write actions. <br>
Risk: Wallet secrets and mnemonics may be exposed through prompts, logs, environment variables, or local files. <br>
Mitigation: Prefer OpenClaw secrets or a protected secret manager, avoid sharing mnemonics in prompts or logs, and restrict keystore and environment access. <br>
Risk: Authenticated Polymarket operations depend on an external CLI binary. <br>
Mitigation: Pin the Polymarket CLI path with EVALANCHE_POLYMARKET_CLI_BIN and review the binary source before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ijaack/evalanche) <br>
- [Project Homepage](https://github.com/iJaack/evalanche) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with tables and inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference wallet credentials, network selection, paid services, external CLI binaries, and on-chain transaction results.] <br>

## Skill Version(s): <br>
1.11.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
