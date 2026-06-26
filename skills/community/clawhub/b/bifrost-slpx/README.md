# bifrost-slpx

Agent skill for **Bifrost SLPx** (vTokens, vETH on-chain flows) using the [`@bifrostio/slpx-cli`](https://www.npmjs.com/package/@bifrostio/slpx-cli) CLI. Full agent behavior, pipelines, and guardrails are in **`SKILL.md`**.

## Install

```bash
npx skills add bifrost-io/skills --skill bifrost-slpx
```

### Agent install (non-interactive)

AI agents that need to **add this skill autonomously** without interactive prompts should run the same command with a target **`--agent`**, **`-g`** (install globally for that agent), and **`-y`** (assume yes):

```bash
npx skills add bifrost-io/skills --skill bifrost-slpx --agent <agentname> -g -y
```

Examples: `--agent cursor` or `--agent claude-code` (use the name your skills CLI expects for the host).

## What it does

- **Queries (all vTokens):** spot exchange `rate`, staking `apy` (optional `--lp` for DeFiLlama LP pool yields), and protocol `info` (TVL, holders, totals; vETH also contract / chains / paused).
- **vETH on EVM:** read `balance` and redemption `status`; write paths `mint` (ETH or WETH → vETH), `redeem` (queued, not instant), `claim` (ETH after redeem completes).
- **Coverage:** `vETH`, `vDOT`, `vKSM`, `vBNC`, `vGLMR`, `vMOVR`, `vFIL`, `vASTR`, `vMANTA`, `vPHA` for queries; **mint / redeem / claim / balance / status** are **vETH-only** on `ethereum`, `base`, `optimism`, `arbitrum`.

## Example user scenarios

| User intent                                                      | Typical CLI flow                                         |
| ---------------------------------------------------------------- | -------------------------------------------------------- |
| “What’s vDOT APY”                                                | `apy --token vDOT --json`                                |
| “Compare vETH vs vKSM staking yield”                             | `apy --token vETH --json` then `apy --token vKSM --json` |
| “vETH exchange rate for 10 ETH worth”                            | `rate 10 --json` (default token vETH)                    |
| “Protocol overview for vASTR”                                    | `info --token vASTR --json`                              |
| “How much vETH / ETH equivalent does this address have on Base?” | `balance 0x… --chain base --json`                        |
| “Stake 0.5 ETH on Arbitrum”                                      | `mint 0.5 --chain arbitrum --json`                       |

## Prerequisites

This skill assumes the **CLI signing key is already configured** for on-chain commands. If it is not, follow **`references/private-key-env.md`** in the skill. **Never** paste raw key material into chat.

## Contents

| Path                              | Purpose                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| `SKILL.md`                        | Entry point: when to use, pre-flight, mint/redeem/claim pipeline |
| `references/commands.md`          | CLI commands and flags                                           |
| `references/tokens-and-chains.md` | vToken matrix, vETH contract, WETH addresses                     |
| `references/errors.md`            | JSON error `code` values                                         |
| `references/pre-tx-checklist.md`  | Checks before broadcasting                                       |

The CLI package itself lives in a separate repo and does **not** ship these markdown files.
