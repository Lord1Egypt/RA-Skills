## Description: <br>
Crypto Watcher monitors public crypto wallets and DeFi positions across supported chains with alerts for balance changes, gas prices, health factors, and large token transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRaini](https://clawhub.ai/user/0xRaini) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure and run read-only monitoring for public wallet balances, DeFi position checks, gas prices, and alert thresholds across Ethereum-compatible chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watched public wallet addresses are shared with configured RPC and crypto data providers. <br>
Mitigation: Monitor only public addresses that are acceptable to disclose to those providers. <br>
Risk: Secrets placed in the local config file could expose sensitive wallet or exchange access. <br>
Mitigation: Do not store seed phrases, private keys, or exchange credentials in the Crypto Watcher config. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xRaini/crypto-watcher) <br>
- [DefiLlama API](https://api.llama.fi) <br>
- [CoinGecko API](https://api.coingecko.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only monitoring guidance and CLI output for configured public wallet addresses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
