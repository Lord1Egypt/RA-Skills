## Description: <br>
Manage Solana wallets, launch tokens, run coordinated buys, volume bots, and wallet operations through the GANK trading terminal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pissdart](https://clawhub.ai/user/pissdart) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and traders use this skill to let an agent prepare and execute GANK API workflows for Solana token launches, multi-wallet buys and sells, volume sessions, copy trading, market-data lookup, and wallet transfer or recovery operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct live Solana trading and wallet-control operations, including automated buys, volume bots, wallet draining, clean-funds flows, copy trading, launches, and transfers. <br>
Mitigation: Use a dedicated low-balance account and API key, manually approve every trade or wallet operation, and verify destination wallets and amounts before execution. <br>
Risk: Exposure of the GANK API key can enable authenticated wallet and trading actions. <br>
Mitigation: Keep the key out of chat and logs, store it only in the configured secret or environment location, and rotate it if exposure is suspected. <br>
Risk: Automated or coordinated trading actions may execute with unintended financial or market effects. <br>
Mitigation: Review generated parameters such as token mint, wallet list, SOL amount, duration, intensity, slippage, and fee settings before sending requests. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/pissdart/gank-solana-bundler) <br>
- [GANK homepage](https://gank.dev) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with JSON, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GANK API key; generated actions can affect live Solana wallets, trades, token launches, and transfers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact skill.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
