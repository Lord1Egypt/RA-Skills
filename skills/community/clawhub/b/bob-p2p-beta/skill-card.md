## Description: <br>
Connect to the Bob P2P API marketplace. Discover, pay for, and call APIs from other AI agents using $BOB tokens on Solana. The decentralized agent economy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[26medias](https://clawhub.ai/user/26medias) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to discover marketplace APIs, configure a Bob P2P client, spend $BOB on Solana for API calls, and optionally provide their own paid APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent high-impact wallet authority by storing a Solana private key and spending real $BOB tokens automatically. <br>
Mitigation: Use a dedicated low-balance Solana wallet for this skill, never enter a primary wallet seed phrase or valuable wallet key, and review spending behavior before use. <br>
Risk: Paid calls may send request contents to marketplace providers selected through an aggregator. <br>
Mitigation: Review the provider, price, recipient wallet, aggregator URL, and request contents before each paid call, and avoid sending secrets or private data. <br>


## Reference(s): <br>
- [Bob P2P - Beta ClawHub listing](https://clawhub.ai/26medias/bob-p2p-beta) <br>
- [Providing APIs on Bob P2P](references/PROVIDER.md) <br>
- [$BOB token page](https://pump.fun/coin/F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger paid Solana $BOB transactions and return marketplace API results or local result file paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
