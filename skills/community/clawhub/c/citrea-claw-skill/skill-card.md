## Description: <br>
Run Citrea L2 monitoring commands to check arbitrage opportunities, token prices, pool liquidity, wallet balances, and new pools across JuiceSwap and Satsuma DEXes by executing node index.js commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-chew](https://clawhub.ai/user/jason-chew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders, liquidity providers, and developers use this skill to monitor Citrea mainnet DeFi activity, inspect token and pool data, and receive optional Telegram alerts for arbitrage opportunities or new pools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and chat IDs are configured through local environment variables. <br>
Mitigation: Use a dedicated Telegram bot token, keep the .env file private, and avoid committing it. <br>
Risk: The arb:monitor and pools:monitor commands can run continuously and send background Telegram alerts. <br>
Mitigation: Run PM2 or monitor commands only when continuous alerts are intended, and stop or delete PM2 processes when monitoring is no longer needed. <br>
Risk: Arbitrage results and pool prices are monitoring signals and may be stale or incomplete. <br>
Mitigation: Verify on-chain state independently before making trading or liquidity decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-chew/citrea-claw-skill) <br>
- [Citrea](https://citrea.xyz) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Citrea mainnet RPC](https://rpc.mainnet.citrea.xyz) <br>
- [Citrea mainnet explorer](https://explorer.mainnet.citrea.xyz) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact setup guide](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with Markdown command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live on-chain monitoring results, wallet or pool summaries, and Telegram alert setup guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: server-resolved release metadata; artifact package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
