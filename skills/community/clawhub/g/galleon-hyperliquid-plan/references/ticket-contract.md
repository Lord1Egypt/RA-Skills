# Ticket contract

```markdown
# HL-YYYYMMDD-NN

- created: <UTC>
- expires: <UTC>
- network: <mainnet or testnet>
- account: <full user or subaccount address>
- account mode: <observed value and source>
- DEX and market: <wire name, display name, asset ID>
- action: <one action class>

## Evidence
- metadata: <request, time, precision, margin table>
- prices: <mid, mark, oracle, time>
- book: <side, size, VWAP, impact, visible reach, time>
- account: <equity, free margin, positions, orders, time>
- fees and limits: <effective rates, action budget, time>

## Risk
- user limit version: <id>
- risk budget: <USD and percent>
- nominal stop distance: <value>
- stressed stop fill: <value and slippage basis>
- entry and exit fees: <rates and USD>
- size: <raw, rounded down, decimals>
- notional and margin: <USD, leverage, tier>
- total open risk after: <USD and percent>
- protection after: <exact trigger plan>
- gates: PASS | REJECT with reason

## Action
- side, size, limit, time in force, reduce-only
- trigger and executable bound, if any
- grouping and every leg
- client order ID per leg
- expiresAfter, if supported
- expected response classes

## Recovery
- reconciliation reads
- partial-fill path
- unknown-result deadline and stop condition
- orphan cleanup path

## Authorization state
Unsigned; no execution requested or authorized by this document.
Execution, when explicitly requested, requires approval for this exact ticket ID through the execution workflow.
```

Hash or otherwise freeze the action section before approval. Any material edit requires a new risk sign-off, identifier or revision, and approval.
