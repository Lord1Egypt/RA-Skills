# Mint Flywheel (铸币飞轮, `fly`)

A Mint Flywheel sale is like a 打新 sale until it launches. Wallets mint **10,000 shares at one price**
(100,000 tokens a share), each within a **quota**. Before launch they can sell shares back at that price, less the exit
fee. When the sale fills, or the creator opens it early at 30% sold, it launches into a PancakeSwap V2 pool **at the mint
price**. After launch, **minting goes on**: the money goes into the pool (part of it buys from the pool), so each mint
adds buy pressure. Invites raise a wallet's quota. These sales live on their own pad, GangFlywheelPad (kind 3). The
unified commands detect them (`kind: "fly"`).

**Networks:** BSC mainnet since 2026-10-30. New tokens go to the V2 pad `0x281889ad915c1A95ffc4922235c6314b3Cbd8a5a` (CLI
0.21.0+; while it is not open yet, `gang create --fly` says so), V1 `0x631e66560F4FAE4e486B65349edE48189E48B029` tokens keep
working. `--testnet` uses BSC testnet (V1 set 2, V2 `0x706973e4F08dBf1604Cf540d0168428521e0E3d6`).

```bash
gang list --kind fly [--status minting|filled|launched|all] [--testnet]   # from the pad, newest first
gang info --token <addr>                  # the sale, rules, launchAt; after launch: prices, protection, supply, tax
gang status --token <addr>                # quota / quotaLeft, invites, shares, sell-back; after launch reward + poolSellAll
gang create --fly --name … --symbol … [--preset j|steady] [flags below] [--dev-shares 1] [--quote … --ref-pool …] [--logo …]
gang mint --token <addr> --shares <n> [--ref <inviter>] [--slippage 2]   # before launch, or after it (post-launch mint)
gang withdraw --token <addr> (--shares <n> | --all)                       # sell back before launch
gang fly open-early --token <addr>        # creator only, ≥ 3,000 shares sold
gang fly launch --token <addr>            # anyone, once launchAt has passed (gang.fun's keeper also launches)
gang fly invite --token <addr> [--who <addr>]   # invite link, invites, bonus, quota left
gang buy | sell --token <addr> …          # after launch: the pool (pool.md)
gang claim --token <addr>                 # holder reward
gang release --token <addr>               # push the creator a dev cut / tax share that failed (= gang fly claim-dev)
```

All of them take `--testnet`, `--calldata` and `--from`. `gang fly <sub>` runs the same code as the unified commands.

## Create

The CLI is the only way to create one (the website has no create page). Agent ID required. `checkConfig` runs before
anything is sent and its reason is printed.

| Flag | Range | `--preset j` (default) | `--preset steady` |
|---|---|---|---|
| `--raise` (BNB worth of the quote; share price = raise / 10,000) | 3–50 | 20 | 20 |
| `--quota` (shares per wallet, before and after launch together) | 5–100 | 10 | 100 |
| `--invite-bonus` (quota per invited wallet) | 0–3 | 1 | 0 |
| `--max-per-tx` | 1–10 | 10 | 10 |
| `--hold` (hold line, % of what a wallet minted) | 60–90 | 60 | 60 |
| `--mint-fee` / `--exit-fee` (%) | 1–3 / 1–2 | 1 / 1 | 1 / 1 |
| `--dev-cut` (% of other wallets' mints to the creator) | 0–10 | 10 | 0 |
| `--buy-pct` (% of each post-launch mint that buys from the pool) | 0–50 | 30 | 0 |
| `--sell-tax` (%; buy tax is fixed at 1%) | 1–2 | 2 | 1 |
| `--launch-delay` (s after the fill) | 0–300 | 60 | 60 |
| `--window` (protection, s) | 300–1800 | 600 | 600 |
| `--cap-mul` (protected buy cap = `--quota` × this × 100,000 tokens; invite bonus not counted) | 1–2 | 1 | 1 |
| `--post-mint` / `--no-post-mint` | | on | off |
| `--tier flat\|standard\|linear` (post-launch share price) | | standard | flat |
| `--step-pct` / `--step-shares` / `--max-mul` (linear only) | 0–10 / 100–100,000 / 1–10 | | |
| `--supply-cap` (× the full pre-launch supply) | 10–500 | 100 | 100 |
| `--guard off\|15\|20\|30` (V2: post-launch mints pause this % below the average) | | off | off |
| `--twap-window 15\|30` (V2: the average's window, minutes) | | 30 | 30 |

**Pad versions.** New tokens go to the V2 pad once it is live (the CLI knows its address); V1 tokens keep working and
every other command uses the token's own pad (`padVersion` in `gang info`). Only V2 takes `--guard` / `--twap-window`,
and on V2, with post-launch minting on, `--quota` is at most 10, `--invite-bonus` at most 1, and the pad's Agent ID gate
must be on (the CLI checks all three before `checkConfig`). A linear tier counts from share 1 on V1 but from the first
post-launch share on V2; the CLI always reads the price from the pad (`sharePrice`). The guard is **off by default**: post-launch minting
does not pause when the price drops (the quota cap of 10 per wallet bounds it); `--guard 15|20|30` turns it on, measured
against the average over `--twap-window` (which only matters then).

`--dev-shares` (default 1, at most quota and max-per-tx) are minted in the create; the creator's own mints carry no dev
cut. `--quote` / `--ref-pool` / logo / links work as in [create.md](create.md). While the pad's Agent ID gate is off, a
sale takes no dev cut: the CLI sets the preset's to 0 (an explicit `--dev-cut` above 0 is refused by `checkConfig`). `--bond`, `--buyback`, `--split`, `--lp` and `--dev-buy` are refused: in phase 1, GangBond, the buy-back splitter, the split module and the LP splitter do not take
these tokens.

## Rules to tell the user

- **Quota**: each wallet has `quota = --quota + invite bonus` shares, shared by pre-launch and post-launch mints, and at
  most `maxPerTx` per mint. `gang status` shows `quotaLeft`. A sell-back gives its shares back to the quota (the mint
  fee is not returned).
- **Invites**: an inviter counts only on a wallet's **first** mint in that token, before or after launch, through
  `--ref <inviter>` or the link `https://gang.fun/token/<token>?ref=<inviter>`. The inviter must have minted in that
  token and hold an Agent ID; it then gets `inviteBonus` more quota. `gang mint --ref` checks all of this before
  building, and refuses rather than sending a mint whose invite would not count. Never invent an inviter.
  `gang fly invite` shows the on-chain bonus and, from gang.fun, `validInvites` / `totalInvites`: an invite stays valid
  while the invitee holds its pre-launch shares (before the fill), once the sale fills or launches, or when the
  invitee's first mint came after launch; none is valid in a refund-only sale. The quota bonus stays either way.
- **Before launch**: one price. The mint fee is the platform's and is not returned. A sell-back pays the mint price
  less the exit fee, which drops to 0 after 7 days without progress.
- **Fill → launch**: at 10,000 shares, or `open-early` at 3,000 or more, minting and sell-backs stop. Anyone launches it
  `launchDelay` later (`gang info`: `launchAt`, `launchableNow`). A filled sale still not launched 7 days after
  `launchAt` reopens sell-backs, and can then launch only while at least 3,000 shares are held. Below that it only refunds
  (`status: refund`).
- **Protection** after launch (`info.protection`): until `until`, a pool buy needs an Agent ID, and a wallet buys at
  most the cap (gross tokens from the pool). `gang buy` checks both first. Post-launch mints are not limited by it.
- **Post-launch mint**: the share price follows the tier table (`info.postMint.sharePriceNow`). The tokens come at no
  less than the pool price, and the result shows `mintPricePerToken` against `poolPrice`. `minTokensOut` is the preview
  less `--slippage` (default 2%); `maxSpent` is the previewed paid + fee. A mint is refused past the wallet's 30-minute
  pace (2% of the pool's quote side), at the supply cap, or by the pad's price rules:
  - V1: while the pool is more than 10% below its 30-minute average or its recent high, or the mint price is more than
    10% above the pool (it dropped in the last blocks);
  - V2: only with the guard on, while the pool is more than the guard below its average over the TWAP window; and while
    the price is more than 10% above the pool in the block of a dump (`info.postMint.rules`).
  The CLI names the rule that applies. `gang info` shows it before any mint: `postMint.pausedNow` with `reason`
  (V1: `below_average`, `below_recent_high`; V2: `below_guard`; both: `above_pool`, `supply_cap`) and when minting resumes; `gang status` shows
  `position.mintPaused` for the wallet (also `pace`). While paused, `next` is a pool buy. `info` checks the supply cap
  with a conservative bound, so it may flag `supply_cap` slightly early near the cap; a mint's own preview is exact.
- **Tax and rewards**: pool buys pay 1% and sells pay 1–2%. The first 1% is split: holders 50%, platform 25%, creator
  25%. Sell tax above 1% goes to holders. Only **minted** tokens earn: a wallet's weight is its balance, capped at what it
  minted. Below the hold line it is **out until its next mint**. Before a sell, check `sellableBeforeOut`. A sell past it
  is refused without `--confirm-out`, which you add only with the user's yes.
- **Notes**: `--note` is not matched to these txs yet, and `--follow` is refused.
- **Private RPC**: the CLI does not broadcast. The Agentic Wallet sends through its own RPC. In the public mempool, a
  large pool buy can be front-run. For a large buy, use `--calldata` and send the tx through a
  private submission endpoint. The output says so (`mempoolNote`).

## Errors

`success: false` comes with `error` and a `hint`: the pad's reason (`TooEarly`, `TooFewShares`, `PaceExceeded`,
`PriceBelowRecentHigh`, `ProtectionCapExceeded`, …), or the CLI's own check (quota used up, inviter not eligible, not
the creator). Fix the flags or wait instead of retrying the same ones.

Flow: preview, then show the shares, the cost including the mint fee, the quota left, and for a post-launch mint the
mint price against the pool price. Confirm, then `gang execute`, then `gang tx --hash …`, which decodes `Minted`,
`Referred`, `PostMinted`, `Filled`, `Launched`, the handler's `Tax*` events and the rest.
