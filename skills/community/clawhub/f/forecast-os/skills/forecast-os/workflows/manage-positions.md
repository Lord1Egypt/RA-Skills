# Workflow: manage positions

Inspect owned predictions from local history, then sell, claim, or redeem with an explicit user warning first.

**Done when:** the user has a view from list/get, any sell/claim/redeem ran only after the user confirmed they want that side effect, and redeemable winnings were surfaced, not left unmentioned.

Sell, claim, and redeem execute immediately. Warn, then wait for approval.

`prediction list` reads local history. Sync is a write. If setup/auth fails on live-account `prediction sync` or sell, follow the setup loop in [config-and-auth.md](../references/config-and-auth.md). Kalshi claim stays skipped.

## Steps

1. List or inspect positions. Use JSON `reference`, not `PRED:n`:

```bash
forecast prediction list --output json --no-input
forecast prediction list --platform precog --output json --no-input
forecast prediction get POLYMARKET:POSITION:TOKEN --output json --no-input
```

2. Sync only when history is missing or stale and the user wants live data:

```bash
forecast prediction sync --confirm --output json --no-input
```

`--confirm` is required when replacing an existing `history.json`.

3. Before sell or claim, warn the user that the command executes immediately. Proceed only if they approve.

4. Sell (optional size / minimum return). Omit `--shares` to sell all (Precog floors to whole shares). `--min-return` above the quote exits 2:

```bash
forecast prediction sell POLYMARKET:POSITION:TOKEN --shares 2 --min-return 1.20 --output json --no-input
```

5. Redeem winnings on a closed market. `prediction list` shows a `redeemable` flag per position; run `prediction sync --confirm` first when the market may have resolved since the last sync, since local history goes stale. Then claim the winning position:

```bash
forecast prediction claim PRECOG:<chain_id>:<master_address>:<market_id>:POSITION:<n> --output json --no-input
forecast prediction claim POLYMARKET:POSITION:TOKEN --output json --no-input
```

Per-platform behavior:

- Precog: claim calls `redeemShares` on the master contract and settles every position the wallet holds in that market in one transaction. Claiming any one position in the market redeems them all, and local history drops every snapshot sharing the market prefix. Needs native ETH for gas, unlike market creation.
- Polymarket: claim redeems the condition and withdraws the resulting collateral to the signer wallet in the same command.
- Kalshi: settlements are automatic. Skip claim there and say so.

After a claim, report the `claimed_amount`, the collateral symbol, and the transaction reference from the JSON. If the claim fails with "not ready to claim", the market has no reported result yet. Say that and stop. Do not retry blindly.

## Kalshi notes

- One net Yes/No position per market; buying the opposite side nets or closes.
- Position refs look like `KALSHI:MARKET:<ticker>:POSITION:1|2`.

## Completion check

- List/get JSON has `ok: true` (or a clear explained failure). Sync ran only when history was missing or stale and the user wanted live data.
- Sell/claim ran only after user approval.
- Redeemable positions were surfaced with the claim command, or their absence stated.
- Kalshi claim was skipped.
