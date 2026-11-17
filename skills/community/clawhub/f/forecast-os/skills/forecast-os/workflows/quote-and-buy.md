# Workflow: quote and buy

Quote or buy a chosen market. Search and list stay on SKILL routing.

**Done when:** a quote was shown without `--confirm` and a buy ran only after approval.

If the binary is missing, load [config-and-auth.md](../references/config-and-auth.md). If short refs or predict pairs fail, load [pitfalls.md](../references/pitfalls.md) and [commands.md](../references/commands.md).

## Quote or buy

1. `market get` the chosen market with its list/search JSON `reference`:

```bash
forecast market get POLYMARKET:EVENT:EVENT_ID --only-outcomes --all --output json --no-input
```

2. Quote with that JSON's outcome `reference` (not `local_reference`). Use exactly one option pair from [commands.md](../references/commands.md). Precog cannot use `--buy-size` alone (add `--price-limit`, or use `--buy-shares` + `--spend-limit`):

```bash
forecast predict POLYMARKET:MARKET:MARKET_ID:OUTCOME:1 --buy-shares 10 --spend-limit 0.45 --output json --no-input
```

3. Show the quote. Stop unless they explicitly ask to submit.

4. Before `--confirm`, follow the setup loop in [config-and-auth.md](../references/config-and-auth.md) if that platform is not trading-ready.

5. Submit only after approval:

```bash
forecast predict POLYMARKET:MARKET:MARKET_ID:OUTCOME:1 --buy-shares 10 --spend-limit 0.45 --confirm --output json --no-input
```

Optional safe retry: add `--request-id <uuid>` together with `--confirm`.

## Completion check

- Quote response has `ok: true` and `data.submitted` is false/absent before confirm.
- After confirm, `data.submitted` is true (or equivalent success fields / `next_actions` from the CLI).
- `--confirm` was used only after user approval.
