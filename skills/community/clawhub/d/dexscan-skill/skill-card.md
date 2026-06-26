## Description: <br>
DexScan Skill retrieves on-chain crypto market data, including token market metrics, signal rankings, social heat, KOL activity, wallet analytics, and smart-money leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yishixing01](https://clawhub.ai/user/yishixing01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query DexScan for token prices, market rankings, on-chain trading activity, social heat, signal data, and wallet-level analytics across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds shared DexScan API credentials as defaults. <br>
Mitigation: Configure DS_ACCESS_KEY and DS_SECRET_KEY with your own credentials before use and avoid relying on the embedded defaults. <br>
Risk: DexScan queries are sent to an external service. <br>
Mitigation: Use the skill only when sending the requested token, address, and market queries to DexScan is acceptable. <br>
Risk: Wallet analytics can surface detailed address, PnL, transaction, tag, and source-of-funds data. <br>
Mitigation: Enable wallet-level analytics only for legitimate analysis where this profiling data is appropriate to process and display. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yishixing01/dexscan-skill) <br>
- [Token signal API reference](references/signal.md) <br>
- [Market API reference](references/market.md) <br>
- [Address API reference](references/address.md) <br>
- [Address ranking API reference](references/address-rank.md) <br>
- [Social heat API reference](references/heat.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with formatted DexScan API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats timestamps, numeric values, percentages, pagination prompts, and API error messages for user-facing responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
