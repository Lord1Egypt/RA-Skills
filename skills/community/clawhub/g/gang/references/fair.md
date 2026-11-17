# Fair mint (打新)

A 打新 sale has no bonding curve. Half the supply (500,000,000) is sold in **10,000 equal shares at one fixed price**;
the other half plus every share's principal goes into a PancakeSwap V2 pool when the last share is minted, so the pool
**opens at the mint price** (LP burned). **No deadline, no refund**: a sale stays open until it fills. Until then a
minter can sell shares back to the sale at the same price, less the exit fee. Sales live on GangLaunchpad next to V3
tokens; the unified commands detect them (`kind: "fair"`).

```bash
gang list --kind fair [--status minting|launched|all]
gang info --token <addr>                                       # the sale: fees, sharesLeft, minWalletsLeft, stale
gang status --token <addr>                                     # my shares; after launch my reward state + poolSellAll
gang create --fair --name … --symbol … [--raise 15] [--cap 0.5] [--hold 60] [--mint-fee 1] [--exit-fee 1] [--shares 1] […]
gang mint --token <addr> --shares <n> [--min-shares <n>]
gang withdraw --token <addr> (--shares <n> | --all)            # sell back at the mint price before it fills
gang buy | sell --token <addr> …                               # after launch: in the pool (pool.md)
gang claim --token <addr>                                      # holder reward
```

All take `--testnet`. The create also takes the logo, link, quote and bond flags of [create.md](create.md)
(`--bond` makes it a launch in one command; a 打新 dev buys with `--shares` in the create itself, not `--dev-buy`).

## Rules to tell the user

- **Create** (Agent ID required): `--raise` 5–50 BNB worth of the quote (converted at create and locked); `--cap`
  0.25–1% of supply per wallet (1% = 200 shares, so at least 50 wallets to fill; 0.5% → 100; 0.25% → 200); `--hold`
  60–90 (the hold line, below; default 60). The creator mints at least 1 share in the same tx (`--shares`, default 1).
  The output shows the raise and the share price in the quote.
- **Fees** are the creator's choice, fixed for the sale: `--mint-fee` 1–3%, `--exit-fee` 1–2% (default 1% / 1%).
  `gang info` shows `mintFeePct` / `exitFeePct` and `exitFeeNowPct` (what a withdraw pays right now): always quote the
  sale's own numbers.
- **Mint** (Agent ID required): share price × shares **plus the mint fee**, which goes to the platform and is never
  returned. A wallet can't exceed its cap. The last mint is cut down to the shares left (`--min-shares` refuses less);
  the mint that fills the sale also launches it and costs more gas. WBNB sales are minted with native BNB through
  GangRouter (`payBnb` = cost + mint fee; `--use-wbnb` pays WBNB).
- **Withdraw**: any time before the sale fills, at the mint price **less the exit fee**; the mint fee is not returned
  (mint 1% + exit 1% = 2% round trip). **After 7 days without progress the exit fee is 0** (`stale: true`;
  `exitFeeFreeIn` counts down): a stalled sale can be left at the full price. Progress = 10 more shares sold than where
  the clock last restarted; a 1-share mint, or minting back shares others withdrew, does not restart it. A withdraw
  reverts if an exit fee comes back before it lands.
- **Progress can go down**: withdraws return shares to the sale. `sharesLeft` and `minWalletsLeft` (at least this many
  more wallets are needed, given the cap) show what is left.
- **Locked until launch**: minted tokens sit in the wallet but can't be moved or traded before launch.
- **After launch**: every buy / sell in the official pool pays 1%. Half goes to **holder rewards**, half to the platform
  (80% GANG buy-back / 20% vault). A seller's share is first cut to what it holds after the sell, so it never earns
  from its own sell's tax. Paid in the quote as the tax is sold ([pool.md](pool.md#how-the-pool-tax-is-paid-ganglaunchpad-tokens)).
- **Holder reward**: only wallets that minted, weighted by current balance capped at what the wallet minted. **Falling
  below the hold line (60–90% of what it minted) once is out for good**; buying back does not restore it. Moving tokens
  to another wallet, a pool or any contract counts as selling. Rewards credited before going out stay claimable.
  `gang status`: `pendingReward` (claimable now), `creditedUnsoldEstimate` (claimable once that tax is sold; an
  estimate). `gang claim` takes the claimable part.
- **Notes**: `--note` on `gang create --fair` (the launch manifesto), `gang mint` and `gang withdraw` ([notes.md](notes.md)).
  Pool trades after launch carry none, and `--follow` is refused: a sale has no curve to follow on.

## Selling after launch

`gang sell` trades in the pool ([pool.md](pool.md)). Before any sell or transfer, check `status.position`:
`reward` (`earning` / `out` / `none`), `balance`, `holdLineTokens`, **`sellableBeforeOut`** (how much can go and still
earn), `poolSharePct`, `pendingReward`. A sell past `sellableBeforeOut` from a wallet still earning fails with
`WARNING: … loses the holder reward FOR GOOD` and builds nothing: tell the user, and only with their yes re-run with
`--confirm-out` (the output keeps the `warning`, `confirmedOut: true`).

## Errors

`success: false` with `error` + `hint` is the pad's own reason (`WalletCapReached`, `NotMinting`, `BadConfig`, …): fix
the flags. Out-of-bounds `--cap` / `--mint-fee` / … fail before any chain call. `NotReclaimable` / `NotLocked` on a
withdraw: not a 打新 token, or it already launched (use `gang sell`). Before launch `gang buy` / `sell` point at `mint` /
`withdraw`; after launch `mint` / `withdraw` point at `buy` / `sell`.

Flow: preview → show shares, the cost **including the sale's mint fee** and the rules that apply (mint fee not
returned, exit fee, hold line) → confirm → `gang execute` → `gang tx --hash …`.
