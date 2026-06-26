## Description: <br>
Provides reputation intelligence for Solana wallets so agents can ask natural-language trust, bot, whale, and eligibility questions and receive data-backed answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RisheeA](https://clawhub.ai/user/RisheeA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to assess Solana wallet reputation before trades, swaps, airdrops, whitelists, and access-control decisions. It helps agents check FairScore, tier, bot-like behavior, wallet traits, and custom eligibility criteria before taking an action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, wallet lists, custom scoring rules, and transaction amounts may be sent to FairScale for reputation checks. <br>
Mitigation: Confirm with the user before sending sensitive wallet lists or transaction amounts, and disclose that the request will be processed by FairScale. <br>
Risk: API keys can be exposed if passed directly on command lines or stored in prompts. <br>
Mitigation: Store API keys in environment-backed secrets such as FAIRSCALE_API_KEY and avoid passing keys as shell arguments. <br>
Risk: x402 wallet-funded requests or paid API tiers may incur charges. <br>
Mitigation: Enable wallet-funded or paid calls only with explicit spending limits and per-call approval for chargeable requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RisheeA/fairscale-solana) <br>
- [FairScale API Reference](references/API.md) <br>
- [FairScale Docs](https://docs.fairscale.xyz) <br>
- [FairScale API Docs](https://api2.fairscale.xyz/docs) <br>
- [FairScale API Key](https://sales.fairscale.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with natural-language answers, inline shell commands, configuration snippets, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet reputation scores, tiers, badges, feature explanations, eligibility decisions, and transaction-risk recommendations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
