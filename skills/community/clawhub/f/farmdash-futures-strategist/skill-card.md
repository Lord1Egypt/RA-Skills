## Description: <br>
Adaptive Hyperliquid perps execution engine for OpenClaw that researches market, funding, liquidity, regime, and account context; returns structured strategy objects with simulations and no-trade outcomes; and supports user-signed EIP-712 execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to research Hyperliquid perpetual futures, compare opportunities, inspect sizing and account risk, and prepare user-approved order execution or cancellation. It is intended for zero-custody workflows where financial actions require explicit confirmation and a fresh user signature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial loss from incorrect, stale, or misunderstood futures order details. <br>
Mitigation: Before signing, verify asset, side, size, leverage, price, order IDs, liquidation risk, and whether the strategy or quote must be refreshed. <br>
Risk: Exposure of wallet secrets or overly broad credentials. <br>
Mitigation: Use FARMDASH_API_KEY only for FarmDash access tiering and never provide private keys, seed phrases, mnemonics, wallet exports, or raw wallet secrets. <br>
Risk: Unintended order execution or cancellation. <br>
Mitigation: Execute or cancel only after explicit user confirmation and a fresh EIP-712 signature; include nonce, expiry, and intent hash when required by the artifact contract. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parmasanandgarlic/farmdash-futures-strategist) <br>
- [FarmDash agents homepage](https://www.farmdash.one/agents) <br>
- [Public FarmDash Futures Strategist skill](https://www.farmdash.one/openclaw-skills/farmdash-futures-strategist/SKILL.md) <br>
- [FarmDash OpenAPI specification](https://www.farmdash.one/agents/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown summaries with structured JSON strategy and execution objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market analysis, confidence, regime labels, pre-trade simulation, sizing, account context, no-trade reasons, and order or cancellation payload requirements.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release metadata; artifact frontmatter reports 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
