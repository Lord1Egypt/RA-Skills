# ATXSwap Skill

A skill bundle for the ATXSwap decentralized agent exchange protocol on BSC. A single `SKILL.md`
works across clients represented by **Claude Code** and **OpenClaw**, so you do
not need separate directories for different clients.

[**中文文档**](./README.zh.md)

- **GitHub**: https://github.com/agentswapx/skills
- **SDK on npm**: [`atxswap-sdk`](https://www.npmjs.com/package/atxswap-sdk)
- **SDK source / docs**: [agentswapx/atxswap-sdk](https://github.com/agentswapx/atxswap-sdk)

For project background and a short [team introduction](https://docs.atxswap.com/guide/team) ([中文](https://docs.atxswap.com/zh/guide/team)), see the ATXSwap documentation site. This README describes the skill’s scope and scripts.

## What This Skill Covers

- Create the single wallet used by the skill (importing an existing private key is not supported)
- Query ATX price, balances, LP positions, and ERC20 token info
- Buy or sell ATX against USDT on PancakeSwap V3
- Preview custom-range liquidity, add liquidity, remove liquidity, collect fees, and burn empty LP NFTs
- Transfer BNB, ATX, USDT, or arbitrary ERC20 tokens

## Directory Layout

```text
atxswap/
├── SKILL.md
├── README.md
├── README.zh.md
├── PUBLISH.md
├── CHANGELOG.md
├── .clawhubignore
├── .gitignore
├── package.json
└── scripts/
    ├── _helpers.js
    ├── wallet.js
    ├── query.js
    ├── swap.js
    ├── liquidity.js
    └── transfer.js
```

## Install

### OpenClaw Install

```bash
openclaw skills install atxswap
```

### Claude Code Install

```bash
git clone https://github.com/agentswapx/skills.git
cd skills/atxswap && npm install
```

By default the skill uses a built-in fallback list of 6 BSC public RPC
endpoints. To override, set `BSC_RPC_URL` to a single URL or to a
comma-separated list (priority left to right):

```bash
export BSC_RPC_URL="https://my-private-rpc.example.com,https://bsc-dataseed.bnbchain.org"
```

## Common Commands

```bash
cd skills/atxswap && node scripts/wallet.js list
cd skills/atxswap && node scripts/query.js price
cd skills/atxswap && node scripts/query.js quote buy 1
cd skills/atxswap && node scripts/query.js positions <address> <tokenId>
cd skills/atxswap && node scripts/liquidity.js quote-add usdt 0.1 --range-percent 20
```

When invoked through a `${SKILL_DIR}`-aware runtime, `cd "${SKILL_DIR}"` is
preferred so the skill works regardless of where the client installed it.

## Liquidity Preview

For custom-range liquidity, do not guess the second token amount from chat.
Preview first, then write:

```bash
cd "${SKILL_DIR}" && node scripts/liquidity.js quote-add usdt 0.1 --range-percent 20
cd "${SKILL_DIR}" && node scripts/liquidity.js add --base-token usdt --amount 0.1 --range-percent 20 --from <address>
```

Supported custom range modes:

- `--range-percent <n>`: expands around the current ATX price, e.g. `20` means `-20% ~ +20%`
- `--min-price <p> --max-price <p>`: explicit `USDT per 1 ATX`
- `--tick-lower <n> --tick-upper <n>`: raw V3 ticks

Recommended flow:

1. Run `query.js price` or `liquidity.js quote-add`
2. Show the returned `estimatedAmounts` to the user
3. Wait for confirmation
4. Execute `liquidity.js add`

## Fee Harvest Preview

Before collecting fees, preview the position first:

```bash
cd "${SKILL_DIR}" && node scripts/query.js positions <address> <tokenId>
cd "${SKILL_DIR}" && node scripts/liquidity.js collect <tokenId> --from <address>
```

`query.js positions` returns **principal** notionals (**`principalAtx`**, **`principalUsdt`**, `principal0`/`principal1`) from liquidity L and spot (`getAmountsForLiquidity`); human **USDT-per-ATX** band **`priceRangeUsdtPerAtx`**, spot **`currentPriceUsdtPerAtx`**, **`currentPriceInRange`**, **`pendingFees`** `{ atx, usdt }`; plus raw `tokensOwed*` / `collectable*` for debugging. Prefer **`principal*`** when explaining tokens in-range; **`pendingFees`** / **`collectable*`** before fee harvest — do **not** surface raw tick indices to users.

`liquidity.js remove <tokenId> <percent>` already performs a single on-chain `multicall`:
`decreaseLiquidity` -> `collect` -> and when `percent = 100`, `burn`.
So a full removal already collects withdrawable funds before burning the NFT. After a successful `remove ... 100`,
running `collect` again for the same `tokenId` is expected to fail because the position NFT no longer exists.

## Security Rules

1. Never expose private keys or passwords in chat output.
2. Always preview price, quote, balance, or positions before write actions.
3. Always wait for explicit user confirmation before swap, transfer, or liquidity writes.
4. Treat all write actions as mainnet asset operations.
5. Before deleting a wallet, require the user to export and back up the encrypted keystore first.
6. Wallet deletion requires a second confirmation: the user must explicitly send `force delete wallet`.
7. For transfers, always treat `(asset, from, to, amount)` as one unique transfer intent and restate it before execution.
8. Once a transfer command returns a `txHash`, treat that transfer as already sent; do not automatically send the same transfer again unless the user explicitly asks for another send.
9. If transfer submission status is ambiguous due to timeout, RPC failure, or interrupted output, do not retry blindly; first inspect chain state or wallet state, then ask the user whether to retry.
10. For present-tense questions about balances, holdings, LP positions, pending fees, or remaining assets, always refresh from live on-chain queries first; never answer from earlier chat output, memory, or cached values alone.

## Duplicate-Transfer Guard

Use this minimum flow to avoid duplicate transfers:

1. Preview balances or wallet state first
2. Restate `(asset, from, to, amount)`
3. Wait for explicit confirmation for that exact tuple
4. Run the transfer command once
5. Return the `txHash`
6. If the same transfer request appears again, clarify whether the user wants a second transfer or is referring to the earlier one

## Live Query Requirement

For these questions, rerun a live query before answering:

- wallet balances
- ATX / USDT holdings
- LP NFT positions
- `principalAtx` / `principalUsdt`
- pending fees
- current pool price or quotes

Recommended mapping:

1. Use `query.js balance` for balances
2. Use `query.js positions` for LP holdings and principals
3. Use `query.js price` for current pool price
4. Use `query.js quote` for swap quotes
5. If the refresh fails, say the latest on-chain data could not be refreshed instead of reusing older values

## Wallet Deletion

Delete a wallet only after both confirmations are complete:

1. The user confirms the encrypted keystore backup is done
2. The user explicitly sends `force delete wallet`

Then run:

```bash
cd "${SKILL_DIR}" && node scripts/wallet.js delete <address> --backup-confirmed yes --force-phrase "force delete wallet"
```
