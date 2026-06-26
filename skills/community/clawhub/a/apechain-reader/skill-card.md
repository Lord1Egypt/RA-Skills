## Description: <br>
Apechain Reader helps agents analyze EVM wallet activity, smart contracts, NFT holdings, transaction history, USD balances, ENS inputs, and bot-like behavior across ApeChain and seven other networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Luigi08001](https://clawhub.ai/user/Luigi08001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect wallet profiles, contract metadata, NFT portfolios, transfer activity, and bot-detection signals for supported EVM addresses. It is suited to read-only due diligence, cross-chain investigation, reporting, and community or airdrop review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, contract addresses, selected chains, query timing, and related investigation context may be visible to public RPC providers, CoinGecko, and Alchemy when enabled. <br>
Mitigation: Use private or dedicated RPC endpoints and a dedicated Alchemy key for sensitive investigations; avoid querying sensitive addresses through public providers when privacy is required. <br>
Risk: Some supported chains are documented as intermittent, and external RPC or pricing services can timeout or return incomplete data. <br>
Mitigation: Prefer the documented reliable chains for critical workflows, retry failed calls, compare results across providers when possible, and treat empty or delayed responses as inconclusive. <br>
Risk: Bot-detection output is heuristic and requires enough NFT purchase activity to produce a meaningful score. <br>
Mitigation: Use bot scores as review signals rather than final decisions, and manually inspect transaction history when scores are near thresholds or data is insufficient. <br>
Risk: ENS support may be unavailable or unreliable in this artifact, and resolved names can fail depending on runtime dependencies and network behavior. <br>
Mitigation: Test ENS inputs before relying on them and use canonical hexadecimal addresses when an investigation requires repeatable results. <br>


## Reference(s): <br>
- [Chain Details](references/CHAINS.md) <br>
- [Bot Detection Scoring](references/bot-scoring.md) <br>
- [Apechain Reader on ClawHub](https://clawhub.ai/Luigi08001/apechain-reader) <br>
- [Alchemy](https://alchemy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON by default, with optional human-readable text output when pretty mode is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are read-only blockchain analysis results from public RPC endpoints and optional Alchemy enrichment; command output may include balances, USD estimates, NFT collections, transaction summaries, contract metadata, explorer links, and bot-score breakdowns.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
