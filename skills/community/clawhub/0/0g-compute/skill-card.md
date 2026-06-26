## Description: <br>
Use cheap, TEE-verified AI models from the 0G Compute Network as OpenClaw providers while discovering available models, comparing pricing vs OpenRouter, verifying provider integrity via hardware attestation (Intel TDX), managing your 0G wallet and sub-accounts, and configuring models in OpenClaw with one workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in-liberty420](https://clawhub.ai/user/in-liberty420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to discover, verify, fund, and configure 0G Compute Network inference providers for OpenClaw workflows. It also helps compare 0G provider pricing against OpenRouter for overlapping models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses an external 0G CLI package that handles wallet keys, on-chain funds, and provider API secrets. <br>
Mitigation: Install only if you trust the external package, use a dedicated low-balance wallet, protect ~/.0g-compute-cli/config.json and openclaw.json, and avoid exposing private keys in shell history or process lists. <br>
Risk: Deposits, transfers, retrieves, and refunds can move on-chain funds. <br>
Mitigation: Manually confirm fund-moving commands and monitor main-account and provider sub-account balances before running inference. <br>
Risk: Using an unverified or unhealthy provider can expose requests to unreliable or untrusted inference infrastructure. <br>
Mitigation: Run provider TEE verification, check provider health and uptime, and protect provider API secrets before adding a provider to OpenClaw. <br>


## Reference(s): <br>
- [0G Compute Skill Page](https://clawhub.ai/in-liberty420/0g-compute) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [OpenClaw Config](references/openclaw-config.md) <br>
- [0G Serving Broker npm Package](https://www.npmjs.com/package/@0glabs/0g-serving-broker) <br>
- [CoinGecko 0G Token Price Endpoint](https://api.coingecko.com/api/v3/simple/price?ids=zero-gravity&vs_currencies=usd) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands, JSON configuration examples, and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 0g-compute-cli binary from @0glabs/0g-serving-broker; the price comparison helper uses public CoinGecko and OpenRouter endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
