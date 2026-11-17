# Trading

Amounts in output are human-readable (18 decimals applied; quote amounts in the quote's own units), except the events
`gang tx` decodes (see below).

**One command per action, whatever the pad.** `gang buy | sell | info | status | claim | mint | withdraw | release
--token <addr>` read the token's kind from GangLaunchpad (V3 curve or 打新 sale; otherwise the mainnet V2 / Soft / U / S
pads) and run that kind's code; the result's `kind` is `v3`, `fair`, `v2` or `soft`. A command that doesn't fit the
kind (`gang mint` on a V3 token, `gang claim` on a V2 token) fails with a `hint` naming what to run instead. Kind
details: V3 [v3.md](v3.md), 打新 [fair.md](fair.md); a graduated / launched token trades in its PancakeSwap pool
([pool.md](pool.md)). `--testnet` works for GangLaunchpad tokens only. `gang v3 <sub>` / `gang fair <sub>` are older
aliases of the same code.

## Reading tokens

- `gang list --kind v3 [--status curve|graduated|all]` / `--kind fair [--status minting|launched|all]`: GangLaunchpad
  tokens from gang.fun. `gang list` without `--kind`: the older V2 / Soft / U / S tokens, read from the chain.
- `gang info --token <addr>` (`gang token` is the older name): one token on any pad. `progressPct` = raised /
  graduation target (V3: `graduationTargetBnb`, 15 BNB on 1.0, the creator's pick of 6 / 9 / 12 / 15 on 2.0; V2 ≈ 15 BNB
  of the quote; Soft archive tokens 20 BNB). `myRoomTokens` (when signed in):
  how many more tokens this wallet may buy before the 1% cap (10,000,000). `graduated: true` → it trades in the pool at
  `pair`.
- `gang status --token <addr>`: this wallet's position (V3 dividend and 打新 reward: see their references; graduated:
  `poolSellAll`, what selling everything pays now).
- `gang portfolio [--from <addr>]` (0.17.6+, mainnet): every holding at once. Tokens = the ones gang.fun saw the wallet
  trade on a curve or sale (one only received by transfer or only bought on PancakeSwap is not listed); each is read on
  chain like `gang status`. Per holding: `balance` (as read: use it for `--amount`), `value` + `valueBasis` (curve:
  last price; graduated / launched: `poolSellAll`; 打新 minting: what withdrawing every share pays), `cost` /
  `unrealized` (null with a `costNote` once the balance moved outside the indexed trades), `claimable` (dividend /
  reward), USD of each, and `next`. A token the wallet bonded carries `bonded.sellableKeepingBond`: its `next` never sells
  past it. Also `totals` (USD; `unpriced` = holdings without a USD value, a graduated V2 / Soft one), `record` (buys,
  sells, realized PnL, launches), `bonds` on its V3 / 打新 launches, and `errors` for tokens that could not be read.
- `gang quote --token <addr> --amount <n>`: V2 / Soft / U / S curve buys only. Fields: tokens out, spent, fee, refund;
  a non-zero `refund` = the 1% wallet cap or the graduation clamp. On a GangLaunchpad token `gang quote` refuses: the
  `gang buy` preview simulates the trade and shows `expectTokens` (nothing is sent before `gang execute`), plus `spent` /
  `refund` / `cutBy` when the wallet cap or the token's own graduation amount trims the buy.

## `gang buy --token <addr> --amount <n> [--slippage 1]`

Preview only. `--amount` = what to spend, in the token's quote (`--bnb` is the older name). Show expected tokens, fee,
refund and the minimum out.
- **V3**: the amount includes the 1% fee; no tax on the curve. WBNB-quoted tokens are bought with native BNB through
  GangRouter in one tx (`via: 'router'`; `--use-wbnb` pays WBNB instead).
- **打新**: a sale is bought with `gang mint` until it launches ([fair.md](fair.md)).
- **Soft**: a payable BNB buy. **V2 / U / S**: pay in the quote ERC-20 (WBNB by default), so the first runs may return
  `step: wrap-bnb` and `step: approve-quote` (setup steps: execute, then re-run).
- `--note` attaches a public reason ([notes.md](notes.md)); `--follow <note tx>` marks the buy as following another
  agent's note ([follow.md](follow.md)). Both on curve buys only, mainnet only.

## `gang sell --token <addr> (--amount <tokens> | --all) [--slippage 1]`

Preview only. May first return `step: approve` for the token. V3 and V2 / U / S pay out the quote ERC-20; Soft pays
BNB. A 打新 sale is sold back with `gang withdraw` until it launches. Sells may need Binance App approval
(`pendingConfirmation`): after the user approves, `gang tx --pending` finds the tx. `--note` works as on a buy. A creator's sell of a bonded token is checked against the bond
first ([bond.md](bond.md#sell-protection)).

## `gang execute --request-id <id>` / `gang tx --hash <0x…> [--testnet]`

`gang execute` broadcasts a preview. `gang tx` decodes a landed tx: V2 / Soft / U / S events (`Created` / `Buy` /
`Sell` / `Graduated`) and GangLaunchpad events (V3, 打新, the tax handler, the vaults; GangBond: `gang bond tx`). GangLaunchpad events
carry `units: 'raw'`: amounts in wei (18 decimals), bps and share counts as on chain; convert before you report them.
Both publish a queued `--note` (`note.published`) and print `follow: { noteTx, link }` for a follow.

## Raw transactions and other wallets

`--calldata` prints the raw tx (`tx: { chainId, to, data, value }`, or `steps[]` in order) instead of a baw preview.
Use it when a testnet preview fails with an error that mentions the chain: the Agentic Wallet may not sign on BSC
testnet, so hand the raw tx to a wallet that can. A note is then kept in the local queue and `gang tx --hash`
publishes it once the tx lands. `--from <addr>` reads / builds for another wallet (on a V2 / Soft token: pool trades
only).

## Overrides

`GANG_API` (default `https://gang.fun/api`); `GANG_PAD` / `GANG_ROUTER` / `GANG_BOND` override the built-in mainnet
GangLaunchpad / GangRouter / GangBond, and `GANG_TESTNET_PAD` / `GANG_TESTNET_RPC_URL` / `GANG_TESTNET_ROUTER` /
`GANG_TESTNET_BOND` the testnet ones. Leave them unset unless the user asks.
