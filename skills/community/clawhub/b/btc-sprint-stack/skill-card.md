## Description:

Trade BTC 5m/15m Polymarket fast markets on Simmer with dry-run-first execution, fee-aware filtering, bankroll limits, flat signal_data, journaling, heartbeat summaries, and a strict BTC-only LLM decision layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captainslab](https://clawhub.ai/user/captainslab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to run or inspect a BTC-only Simmer and Polymarket sprint trading workflow with dry-run-first execution, risk limits, LLM decision validation, journaling, and learning summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can submit real BTC market trades and, when a wallet private key is present, can link a wallet and perform token approvals.

Mitigation: Start in dry-run mode, use an isolated environment, keep WALLET_PRIVATE_KEY unset unless wallet linkage and approvals are intentional, and review account settings before enabling live mode.

Risk: The skill can use LLM API keys, Codex OAuth credentials, or Google application-default credentials, and custom LLM base URLs could expose prompts or tokens to an unintended service.

Mitigation: Use dedicated least-privilege credentials, avoid custom LLM_BASE_URL values unless routed through a trusted proxy with separate credentials, and do not run on a host with unrelated sensitive tokens.

Risk: Self-tuning behavior can change live parameters and pending rules based on prior runs.

Mitigation: Review or reset live_params.json and pending_rules.json before live use, and inspect the journal and LLM decision logs after each run.

Risk: Discord alerting can post operational details to the configured webhook.

Mitigation: Use a dedicated webhook, verify the destination before testing alerts, and rotate the webhook if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/captainslab/skills/btc-sprint-stack)
- [Publisher profile](https://clawhub.ai/user/captainslab)
- [Binance.US klines endpoint](https://api.binance.us/api/v3/klines)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON runtime reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the artifact can write local JSON and JSONL journals, learning state, pending rules, and heartbeat summaries.]

## Skill Version(s):

0.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
