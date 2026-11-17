## Description:

Places GTC limit orders on both YES and NO sides of selected liquid Polymarket markets to quote around the CLOB midpoint and pursue bid/ask spread capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to run or dry-run a Polymarket market-making strategy that selects liquid markets, manages open orders, and places small bid/ask limit orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real orders and cancel existing open orders when used with a broad trading API key.

Mitigation: Use paper mode first, run with a dedicated trading account or scoped API key, and avoid accounts with unrelated active orders.

Risk: The skill depends on simmer-sdk and external market data, so dependency or market-data changes can affect trading behavior.

Mitigation: Pin and review simmer-sdk before installation, review market behavior before live use, and keep safeguards enabled unless independently validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-market-maker)
- [Polymarket CLOB endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Console text with optional JSON automaton report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; default execution is dry-run unless --live is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also lists 1.2.0 and _meta.json lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
