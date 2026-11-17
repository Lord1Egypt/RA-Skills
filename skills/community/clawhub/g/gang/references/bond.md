# Creator bonds (押金承诺, GangBond)

A creator of a GangLaunchpad token can back a promise with money: **"my creating address keeps at least X tokens
until N days after the token reaches PancakeSwap."** The bond is paid in the token's quote (WBNB tokens: the CLI pays
native BNB). Whether the promise holds is read from the chain alone (`balanceOf(creator)`): no oracle, no platform
decision.

- **When**: any time after create — on the V3 curve (buy first: X can't exceed what the creator holds), during a 打新
  sale, or after graduation / launch. One bond per token at a time; after it ends (settled, refunded, or slashed and
  fully bought back) the creator may post a new one.
- **The clock**: the promise binds from the post. T = the moment the token reaches its pair (V3 graduation / 打新 launch)
  + N days (7–90); posted after that, T = post + N days. GangBond can't be told about a graduation, so anyone starts the
  clock with `gang bond start` (the keeper does it at once; any other bond write does it too).
- **Who**: only the token's creator posts, tops up, raises X, extends or refunds. Start, report, settle and burn are open
  to anyone.
- **Endings**:
  - **settle** — two steps from T on, anyone (the platform keeper does both): `gang bond settle` once asks (the creator
    holds ≥ X now), and again 1 hour later settles (still ≥ X): the whole bond goes back to the creator. X has to be
    held for real across that hour, not just inside one transaction. The time after T and before settle still counts.
  - **report** — any time before settle (on the curve too), once the creator holds < X: the reporter gets **1%** of the
    bond (none when the creator reports itself); the rest buys the token back from its pair in chunks and sends it to
    0xdead. Slashed before the pair, the buy-back waits for it; if there is still no pair 30 days after the post, the
    rest goes to 0xdead as quote.
  - **refund** — posted before the pair and still no pair 30 days after the post: the creator asks (`gang bond refund`),
    which starts a 3-day notice shown on gang.fun; X still binds through it, and a graduation / launch voids the request
    (the clock starts instead). After the notice, still no pair and X held, the creator runs it again and gets the whole
    bond back (not counted as honored). So a bond can't be pulled unseen right before graduation.
  There is **no other early withdrawal**. Selling on the curve, selling 打新 shares back, or moving tokens to another own
  wallet all count as a breach.
- **Buy-back** (`gang bond burn`, also the keeper every 5 minutes): at most one chunk per 4 minutes, each at most 0.5% of
  the pair's quote side. The first call after a slash only records a price observation; buying starts 10 minutes later and pauses
  while the price is more than 2% above its 10-minute average; after 20 minutes without a call the observation starts
  over. The token's buy tax applies to the buy-back as usual.
- **The record is not a reputation score**: `posted / honored / slashed` counts bonds of any size, and a tiny bond is
  cheap to honor. Read it next to the bond amounts.

## Coverage

`coverage = bond ÷ dumpValue`, where dumpValue is what selling X into the pair fetches now (after the sell tax, the
0.25% DEX fee and price impact). ≥ 100%: dumping X loses money. It falls when the price rises; `toFullCover` says how
much quote would bring it back to 100%. Tiers on gang.fun: ≥ 100% green "押金全覆盖", 50–100% yellow "押金", < 50% a plain gray "押金"
badge. The colours also need an allow-listed quote (WBNB, a QuoteRegistry quote, GANG) and an X of at least half the
creator's balance when it was set; otherwise the badge stays gray (any other quote: no coverage shown, its value is
unknown).
Coverage is for display and screening only; it never decides where a bond goes. Before the pair there is no market
to price X: no coverage, a gray badge — show the bond amount and X (% of supply) instead, and `--cover` is not available.

## Commands

| Command | Who | What |
|---|---|---|
| `gang bond post --token <addr> --hold <tokens\|N%> --days <7-90> (--amount <quote> \| --cover <%>)` | creator | `--hold 1%` = 1% of the 1B supply; `--days` counts from graduation / launch (from now if already there); `--cover 100` posts exactly what dumping X fetches now (only once on the pair) |
| `gang bond topup --token <addr> (--amount <quote> \| --cover <%>)` | creator | add to the bond (`--cover` = target coverage, once running) |
| `gang bond raise-hold --token <addr> --hold <tokens\|N%>` | creator | raise X, up to the current balance |
| `gang bond extend --token <addr> --days <n>` | creator | lengthen the commitment: before the pair 90 days in all at most, after it a deadline at most 90 days from now |
| `gang bond status --token <addr>` | anyone | state, phase (pending / running), X vs balance (headroom), coverage + tier once on the pair, time left or refund date, buy-back progress, the creator's record |
| `gang bond start --token <addr>` | anyone | the token graduated / launched: start the clock (deadline = now + N days) |
| `gang bond report --token <addr>` | anyone | simulated first; nothing is built when the creator still holds ≥ X |
| `gang bond settle --token <addr>` | anyone | after T while X is held: run once to ask, again 1 hour later to settle |
| `gang bond refund --token <addr>` | creator | posted before the pair, no pair 30 days after the post: first run asks (3-day notice), a run after the notice gets the bond back |
| `gang bond burn --token <addr> [--slippage 1]` | anyone | one buy-back chunk (or the observation / a skip, see above); slashed before the pair and still none 30 days after the post: the rest to 0xdead as quote |
| `gang bond tx --hash <0x..>` | anyone | decode GangBond events |

All take `--testnet`, `--calldata` (raw tx) and `--from <addr>` ([trade.md](trade.md#raw-transactions-and-other-wallets)).
Writes print a preview → `gang execute`; none carries a `--note`. Relay any `warning` in the output.
`post` / `topup` of a WBNB-quoted token pay native BNB; `--use-wbnb` pays WBNB instead (approve first, then re-run).
A `burn` preview made while no chunk is ready sends the maximum minimum: if a chunk has become buyable by the time it
lands, it reverts instead of buying unpriced; re-run for a priced preview.
GangBond is built in per pad generation: BSC mainnet 2.0 `0x231339463d04A2127E6dD5756756Dd56853AE0D8` (1.0
`0xe92dC940CB23Dc328639A7334e69F9CCdf3a14E4`), testnet 2.0 `0x39749B59066d9cd1c55E2Fc48B31a3978C9951F9` (1.0
`0xd6a8dd5d1E6641a34A255f25Db2B3ED397CB1086`). A token's bond is on its own generation's GangBond.

## Sell protection

`gang sell` (on the curve or in the pool) and `gang withdraw` (打新 shares back while minting, each share = 50,000
tokens) from the creator of a bonded token check the bond first:

1. The sell leaves less than X before T → refused (`error`, `maxSellKeepingBond`): pass both on. `--break-bond` sends
   it anyway, losing the whole bond: only when the user, told so, still says sell.
2. Past T (the clock running), not settled, and the sell leaves less than X → refused; `--settle-first` returns the next
   settle step first (the request; or the settle once its 1-hour wait is over), then re-run the sell.
3. The sell leaves at least X → goes on; the preview carries `bondCheck.headroomAfter`.

This only covers the CLI. A sell on the PancakeSwap site or from another wallet is not stopped and loses the bond.
