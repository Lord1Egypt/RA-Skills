#!/usr/bin/env npx tsx

// 抑制 Promise.all 中未处理的 rejection（已由 main catch 处理）
process.on("unhandledRejection", () => {})

import { setJsonMode, error } from "../src/lib/output.js"
import { hasFlag, getFlagValue, removeFlags, removeFlagWithValue } from "../src/lib/args.js"

async function main() {
  let args = process.argv.slice(2)

  // 全局 flags
  if (hasFlag(args, "--json")) setJsonMode(true)
  if (hasFlag(args, "--version")) { console.log("0.1.0"); return }

  // --network 覆盖
  const networkOverride = getFlagValue(args, "--network")
  if (networkOverride) {
    process.env.FOMO3D_NETWORK = networkOverride
    args = removeFlagWithValue(args, "--network")
  }

  args = removeFlags(args, "--json")

  if (hasFlag(args, "--help", "-h") || args.length === 0) {
    args = removeFlags(args, "--help", "-h")
    // 如果有子命令带 --help，仍然路由到对应命令
    if (args.length === 0) {
      printHelp()
      return
    }
  }

  const [command, subcommand] = args
  const rest = args.slice(1)

  switch (command) {
    case "setup": {
      const { setup } = await import("../src/commands/setup.js")
      return setup(rest)
    }
    case "wallet": {
      const { wallet } = await import("../src/commands/wallet.js")
      return wallet(rest)
    }
    case "status": {
      const { status } = await import("../src/commands/status.js")
      return status(rest)
    }
    case "player": {
      const { player } = await import("../src/commands/player.js")
      return player(rest)
    }
    case "purchase": {
      const { purchase } = await import("../src/commands/purchase.js")
      return purchase(rest)
    }
    case "exit": {
      const { exit } = await import("../src/commands/exit.js")
      return exit(rest)
    }
    case "settle": {
      const { settle } = await import("../src/commands/settle.js")
      return settle(rest)
    }
    case "end-round": {
      const { endRound } = await import("../src/commands/end-round.js")
      return endRound(rest)
    }
    case "buy": {
      const { buy } = await import("../src/commands/buy.js")
      return buy(rest)
    }
    case "sell": {
      const { sell } = await import("../src/commands/sell.js")
      return sell(rest)
    }
    case "token-info": {
      const { tokenInfo } = await import("../src/commands/token-info.js")
      return tokenInfo(rest)
    }
    case "slot": {
      const slotRest = args.slice(2)
      switch (subcommand) {
        case "status": {
          const { slotStatus } = await import("../src/commands/slot-status.js")
          return slotStatus(slotRest)
        }
        case "spin": {
          const { slotSpin } = await import("../src/commands/slot-spin.js")
          return slotSpin(slotRest)
        }
        case "cancel": {
          const { slotCancel } = await import("../src/commands/slot-cancel.js")
          return slotCancel(slotRest)
        }
        case "deposit": {
          const { slotDeposit } = await import("../src/commands/slot-deposit.js")
          return slotDeposit(slotRest)
        }
        case "claim": {
          const { slotClaim } = await import("../src/commands/slot-claim.js")
          return slotClaim(slotRest)
        }
        default:
          console.error(`Unknown slot command: ${subcommand ?? "(none)"}`)
          console.error("Available: status, spin, cancel, deposit, claim")
          process.exit(1)
      }
      break
    }
    default:
      console.error(`Unknown command: ${command}`)
      printHelp()
      process.exit(1)
  }
}

function printHelp() {
  console.log(`
fomo3d — Play Fomo3D and Slot Machine on BNB Chain (BSC)

USAGE:
  fomo3d <command> [options]

SETUP:
  setup                         Configure wallet and network

INFO:
  wallet                        Show BNB + token balances
  status                        Game round status, countdown, pools
  player [--address 0x...]      Player shares, earnings, pending

GAME ACTIONS:
  purchase --shares <n>         Buy shares (auto-approves token)
  exit                          Exit game, claim dividends
  settle                        Settle after round ends + claim prize
  end-round                     End expired round

TOKEN TRADING (mainnet only):
  buy --amount <usdt_wei>       Buy FOMO with USDT via FLAP
  sell --amount <token_wei>     Sell FOMO tokens for USDT
  sell --percent <bps>          Sell by % (10000=100%, 5000=50%)
  token-info                    Token status, price, balances

SLOT MACHINE:
  slot status                   Slot machine status and stats
  slot spin --bet <n>           Spin (requires BNB for VRF fee)
  slot cancel                   Cancel timed-out spin
  slot deposit --amount <n>     Deposit tokens to prize pool
  slot claim                    Claim slot dividends

FLAGS:
  --json                        JSON output (for AI agents)
  --network testnet|mainnet     Override network
  --help                        Show help
  --version                     Show version
`)
}

main().catch((err) => {
  error(err instanceof Error ? err.message : String(err))
  process.exit(1)
})
