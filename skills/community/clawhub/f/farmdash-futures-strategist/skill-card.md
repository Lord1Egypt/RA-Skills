## Description: <br>
Adaptive Hyperliquid perps execution engine for OpenClaw agents. Provides research, pre-trade simulation, predictive funding shifts, and zero-custody EIP-712 order routing with forensic telemetry. Scout (5/day), Pioneer (unlimited), and Syndicate (unlimited) execution supported. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to research Hyperliquid perpetual futures markets, simulate strategies, size positions, and prepare order or cancellation requests. State-changing actions require explicit user confirmation and a fresh user-signed EIP-712 payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared futures orders can cause financial loss, liquidation, or unwanted exposure if confirmed with incorrect details. <br>
Mitigation: Before every execution or cancellation, verify the asset, side, size, leverage, stop, liquidation estimate, margin impact, and order IDs before signing or confirming. <br>
Risk: Private key, seed phrase, mnemonic, or raw wallet export disclosure would compromise the user's funds. <br>
Mitigation: Do not provide wallet secrets to the agent or FarmDash; use only fresh local EIP-712 signatures from the user's Hyperliquid API wallet. <br>
Risk: Stale strategy data or mutated order parameters can make a signed request unsafe or invalid. <br>
Mitigation: Re-run strategy analysis when quotes are stale, and use nonce, expiresAt, and intentHash checks so signed actions match the presented order. <br>
Risk: Oracle latency, price deviation, low liquidity, or conflicting signals can make leveraged execution unsuitable. <br>
Mitigation: Respect no-trade outcomes, oracle-latency and deviation guardrails, adaptive risk reductions, and explicit user review before any non-reduce-only action. <br>


## Reference(s): <br>
- [FarmDash agents homepage](https://www.farmdash.one/agents) <br>
- [ClawHub skill page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-futures-strategist) <br>
- [Bundled OpenAPI contract](artifact/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, JSON, API Calls, Shell commands] <br>
**Output Format:** [Markdown guidance with structured JSON strategy, sizing, simulation, receipt, and order or cancellation payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scout tier supports up to 5 execution or analysis requests per day; state-changing actions require explicit user confirmation and user-signed EIP-712 authorization.] <br>

## Skill Version(s): <br>
1.0.20 (source: server release metadata; artifact frontmatter version 3.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
