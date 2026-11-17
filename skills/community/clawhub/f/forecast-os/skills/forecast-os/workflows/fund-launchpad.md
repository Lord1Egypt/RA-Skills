# Workflow: fund / claim launchpad markets

Fund a Precog upcoming market, then claim investment or incentive after deploy. Backend: `https://service.precog.markets/api/v1`. Key resolves like the CLI: `--key-file` > `PRECOG_PRIVATE_KEY` > `forecast_config.toml [precog]`. RPC resolves `--rpc` > `BASE_RPC` / `ARBITRUM_RPC` > `[precog] base_rpc` / `arbitrum_rpc`. Never echo keys. Needs `pip install web3 eth-account`. Diagnostics go to stderr via logging; stdout carries only result JSON. Run the scripts from the skill directory (the `scripts` folder next to `SKILL.md`).

Multitoken note: each market has ONE funding collateral, but the incentive can be a different token on a different chain. The fund script prints both (`collateral_symbol` + `incentive_collateral_symbol`/`incentive_chain_id`) — verify before funding.

**Done when:** a preview ran without `--confirm`, and fund/claim ran only after approval.

## Discover

List fundable markets first (VALIDATED plus FUNDED with room under the max cap, end date in the future). No key needed:

```bash
python3 scripts/list_upcoming.py
python3 scripts/list_upcoming.py --chain-id 8453 --limit 20
```

Pass `--all` to list every status with non-fundable rows tagged (`FULL`, `DEPLOYED`, `EXPIRED`, `ENDED`, ...). Narrow with `--status`, `--category`, `--collateral-symbol`, `--funder-address`, or `--json` for full rows. Pick a market id, then continue with the fund preview below.

## Fund

1. Preview (fetches market, shows collateral vs incentive token):

```bash
python3 scripts/fund_upcoming.py --market 123 --amount 10
```

2. Submit after approval. Pre-flight checks run first: collateral `balanceOf` must cover the amount and native balance must cover estimated gas (EIP-1559, via `estimate_gas`) — aborts before sending otherwise. Then sends the ERC20 transfer to the precog creator (`0x5D45B7d8e517eF6b7085175ed395D9c8562b952f`), EIP-712-signs `FUND_UPCOMING_MARKET`, and registers `{upcoming_market, amount, tx_hash, funder_address, funder_signature}`:

```bash
python3 scripts/fund_upcoming.py --market 123 --amount 10 --confirm
```

Skip the transfer with `--tx-hash 0x...` when already sent. The receipt is hard-validated (status, sender == funder, receiver == creator, token, amount within 0.00001) and registration aborts on any mismatch. Domain logic lives in `scripts/common/` (`launchpad_service.py` in `MarketService` shape, slim `web3_service.py` port, verbatim `signature_verifier.py` and `abis/IERC20.json` from precog-tracker).

## Claim

`--market` is the *deployed* master market id (`deployed_market_id`), not the upcoming id. Investment pays collateral on the market chain; incentive pays the incentive token on the incentive chain. Preview shows claimable totals; confirm checks native gas balance first:

```bash
python3 scripts/claim_upcoming.py --kind investment --market 42 --chain-id 8453
python3 scripts/claim_upcoming.py --kind investment --market 42 --chain-id 8453 --confirm
python3 scripts/claim_upcoming.py --kind incentive --market 42 --chain-id 8453 --confirm
```

## Completion check

- Preview without `--confirm` shown first.
- `--confirm` used only after user approval.
- Key via file/env/config, never argv.
