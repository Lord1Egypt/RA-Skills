# Workflow: create Precog market

Preview a market creation from a YAML/JSON spec, submit only after explicit user approval, then check creation status.

**Done when:** a preview ran without `--confirm`, and submit ran only after approval (or status was checked for an existing creation ref).

Preview without `--confirm` first. Do not run `status` to start. Flag map: [commands.md](../references/commands.md). Creation needs no funds: a zero ETH balance never blocks it. Gate submit only on a valid Precog key.

Run `scripts/validate_market_spec.py` on the spec before the CLI preview. It enforces the safe rails below offline and fails fast with field-specific errors.

## Safe rails

Hard rules (validator fails, CLI preview never runs):

- English only. Non-ASCII text in `question`, `resolution_criteria`, or any outcome fails.
- `question` under 40 characters, ends with `?`.
- Outcomes: 2 or more, each 23 characters or fewer, no empty labels, no commas.
- `resolution_criteria` at least 40 characters and must contain a source signal (a URL or words like official, website, announced, published, according to, based on) and a fallback signal (cancel, postpone, void, default, no change, or what the market resolves to if the event does not happen).
- `category` uppercase, one token or CSV. `start_timestamp` < `end_timestamp`. `collateral_address` a valid `0x` address.

## Spec requirements

Required fields: `question`, `resolution_criteria`, `image_url`, `category`, `outcomes`, `end_timestamp`, `collateral_address`.

Optional: `start_timestamp` (defaults to now). Optional CLI flag: `--chain base|arbitrum`.

Launchpad rules (CLI outer bounds; safe rails above are stricter):

- `question` must end with `?`, max 65 characters
- ≥2 outcomes; no empty labels; no commas in labels; max 32 characters each
- `image_url` is `http(s)` or `ipfs://` with a host (CID counts as host)
- `start_timestamp` < `end_timestamp`
- `category` must be uppercase: one token or CSV (`SPORTS` or `SPORTS,POLITICS`). Do not send title case.
- `collateral_address` must be a valid `0x` address. Creator comes from the Precog key, not the spec.

Design (unless the user asked otherwise):

- Prefer a multi-outcome market (≥3 named outcomes) over binary Yes/No. Use binary only when the event has exactly two exclusive results.
- Outcomes must be MECE: mutually exclusive and collectively exhaustive. One winner only; together they cover every possible result. Add a remainder label (for example `Other`) when the named set would otherwise miss cases.
- Set `end_timestamp` to one week before the event happens, not the event time. Close trading while the result is still uncertain.

Example:

```yaml
question: Which team wins the final?
resolution_criteria: Use the official organizer result.
image_url: ipfs://bafybeigdyrzt
category: SPORTS
outcomes:
  - North
  - South
  - East
end_timestamp: 1800000000
collateral_address: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

`end_timestamp` is Unix seconds for (event time − 7 days).

## Steps

1. Validate the spec offline:

```bash
python scripts/validate_market_spec.py --spec market.yaml
```

Fix every failure before continuing.

2. Preview creation (no submit):

```bash
forecast create market --spec market.yaml --output json --no-input
```

3. Show the preview to the user. Stop unless they explicitly ask to submit.

4. Before `--confirm`, follow the setup loop in [config-and-auth.md](../references/config-and-auth.md) if the Precog key is missing or invalid. Zero balance never blocks submit. Submit after approval:

```bash
forecast create market --spec market.yaml --confirm --output json --no-input
```

5. Follow up with creation status when a creation ref is available:

```bash
forecast create status PRECOG:8453:UPCOMING:42 --output json --no-input
```

## Completion check

- Validator script passed before the CLI preview.
- Preview completed without `--confirm`.
- `--confirm` was used only after user approval.
- Status check used when a creation reference exists.
