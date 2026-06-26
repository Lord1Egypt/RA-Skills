#!/usr/bin/env node
import { Command } from "commander"
import { readFileSync } from "node:fs"
import { join, dirname } from "node:path"
import { fileURLToPath } from "node:url"

const __dirname = dirname(fileURLToPath(import.meta.url))
const pkg = JSON.parse(readFileSync(join(__dirname, "..", "package.json"), "utf8"))

const cli = new Command()
cli.name("awp-wallet").version(pkg.version).description("AWP EVM Wallet CLI")

// --- Global options ---
cli.option("--pretty", "Pretty-print JSON output")
cli.option("--chain <chain>", "Chain name or ID")
cli.option("--rpc-url <url>", "Custom RPC URL")
cli.option("--native-symbol <sym>", "Native currency symbol for custom chains")

// --- Output utilities ---
function json(obj) { console.log(JSON.stringify(obj, null, cli.opts().pretty ? 2 : undefined)) }
function fail(msg) { console.error(JSON.stringify({ error: msg })); process.exit(1) }

// --- Chain resolution (called within actions, chain module is preloaded) ---
let _chains = null

async function getChains() {
  if (!_chains) _chains = await import("./lib/chains.js")
  return _chains
}

async function resolveChain() {
  const globalOpts = cli.opts()
  const chains = await getChains()

  // If --rpc-url is provided, register custom chain
  if (globalOpts.rpcUrl) {
    if (!globalOpts.chain) throw new Error("--rpc-url requires --chain <chainId> to identify the chain.")
    const chainId = chains.resolveChainId(globalOpts.chain)
    const nativeCurrency = globalOpts.nativeSymbol
      ? { name: globalOpts.nativeSymbol, symbol: globalOpts.nativeSymbol, decimals: 18 }
      : undefined
    chains.viemChain(chainId, globalOpts.rpcUrl, nativeCurrency)
  }

  if (globalOpts.chain) return globalOpts.chain

  // Read default chain from config
  try {
    const cfg = chains.loadConfig()
    if (cfg.defaultChain) return cfg.defaultChain
  } catch { /* ignore */ }

  throw new Error("No --chain specified and no defaultChain in config.")
}

// --- Command definitions ---

cli.command("init")
  .description("Create a new wallet")
  .action(async () => {
    try {
      const { initWallet } = await import("./lib/keystore.js")
      json(await initWallet())
    } catch (e) { fail(e.message) }
  })

cli.command("import")
  .description("Import wallet from mnemonic")
  .requiredOption("--mnemonic <phrase>", "Mnemonic seed phrase")
  .action(async (opts) => {
    try {
      const { importWallet } = await import("./lib/keystore.js")
      json(await importWallet(opts.mnemonic))
    } catch (e) { fail(e.message) }
  })

cli.command("unlock")
  .description("Unlock wallet and get session token")
  .option("--duration <seconds>", "Session duration in seconds", "3600")
  .option("--scope <scope>", "Session scope (read|transfer|full)", "full")
  .action(async (opts) => {
    try {
      const duration = parseInt(opts.duration)
      if (isNaN(duration) || duration < 1) throw new Error("--duration must be a positive integer (seconds).")
      const { unlockWallet } = await import("./lib/session.js")
      json(unlockWallet(duration, opts.scope))
    } catch (e) { fail(e.message) }
  })

cli.command("lock")
  .description("Lock wallet and revoke all sessions")
  .action(async () => {
    try {
      const { lockWallet } = await import("./lib/session.js")
      json(lockWallet())
    } catch (e) { fail(e.message) }
  })

cli.command("change-password")
  .description("Change wallet password")
  .action(async () => {
    try {
      const { changePassword } = await import("./lib/keystore.js")
      json(await changePassword())
    } catch (e) { fail(e.message) }
  })

cli.command("export")
  .description("Export wallet mnemonic")
  .action(async () => {
    try {
      const { exportMnemonic } = await import("./lib/keystore.js")
      json(exportMnemonic())
    } catch (e) { fail(e.message) }
  })

cli.command("verify-log")
  .description("Verify transaction log integrity")
  .action(async () => {
    try {
      const { verifyIntegrity } = await import("./lib/tx-logger.js")
      json(verifyIntegrity())
    } catch (e) { fail(e.message) }
  })

cli.command("status")
  .description("Show wallet status")
  .requiredOption("--token <token>", "Session token")
  .action(async (opts) => {
    try {
      const { validateSession } = await import("./lib/session.js")
      const { getAddress } = await import("./lib/keystore.js")
      const session = validateSession(opts.token)
      const address = getAddress("eoa")
      json({
        address,
        sessionValid: true,
        sessionExpires: session.expires,
      })
    } catch (e) { fail(e.message) }
  })

cli.command("balance")
  .description("Check balance on chain")
  .requiredOption("--token <token>", "Session token")
  .option("--asset <asset>", "Token symbol or contract address")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { getBalance } = await import("./lib/balance.js")
      json(await getBalance(opts.token, chain, opts.asset || null))
    } catch (e) { fail(e.message) }
  })

cli.command("portfolio")
  .description("Check balances across all configured chains")
  .requiredOption("--token <token>", "Session token")
  .action(async (opts) => {
    try {
      const { getPortfolio } = await import("./lib/balance.js")
      json(await getPortfolio(opts.token))
    } catch (e) { fail(e.message) }
  })

cli.command("send")
  .description("Send tokens")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--to <address>", "Recipient address")
  .requiredOption("--amount <amount>", "Amount to send")
  .option("--asset <asset>", "Token symbol or contract address")
  .option("--mode <mode>", "Transaction mode (direct|gasless)")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { sendTransaction } = await import("./lib/tx-router.js")
      json(await sendTransaction({
        sessionToken: opts.token, to: opts.to, amount: opts.amount,
        asset: opts.asset, chain, mode: opts.mode,
      }))
    } catch (e) { fail(e.message) }
  })

cli.command("batch")
  .description("Send multiple operations")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--ops <json>", "Operations JSON array")
  .option("--mode <mode>", "Transaction mode (direct|gasless)")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const operations = JSON.parse(opts.ops)
      if (!Array.isArray(operations) || operations.length === 0)
        throw new Error("--ops must be a non-empty JSON array of operations.")
      const { batchTransaction } = await import("./lib/tx-router.js")
      json(await batchTransaction({ sessionToken: opts.token, operations, chain, mode: opts.mode }))
    } catch (e) { fail(e.message) }
  })

cli.command("approve")
  .description("Approve token spending")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--asset <asset>", "Token symbol or contract address")
  .requiredOption("--spender <address>", "Spender address")
  .requiredOption("--amount <amount>", "Amount to approve")
  .option("--mode <mode>", "Transaction mode (direct|gasless)")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { approveToken } = await import("./lib/tx-router.js")
      json(await approveToken({
        sessionToken: opts.token, asset: opts.asset, spender: opts.spender,
        amount: opts.amount, chain, mode: opts.mode,
      }))
    } catch (e) { fail(e.message) }
  })

cli.command("revoke")
  .description("Revoke token approval")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--asset <asset>", "Token symbol or contract address")
  .requiredOption("--spender <address>", "Spender address")
  .option("--mode <mode>", "Transaction mode (direct|gasless)")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { revokeApproval } = await import("./lib/tx-router.js")
      json(await revokeApproval({
        sessionToken: opts.token, asset: opts.asset, spender: opts.spender,
        chain, mode: opts.mode,
      }))
    } catch (e) { fail(e.message) }
  })

cli.command("estimate")
  .description("Estimate gas cost")
  .requiredOption("--to <address>", "Recipient address")
  .requiredOption("--amount <amount>", "Amount")
  .option("--asset <asset>", "Token symbol or contract address")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { estimateGas } = await import("./lib/tx-router.js")
      json(await estimateGas({ to: opts.to, amount: opts.amount, asset: opts.asset, chain }))
    } catch (e) { fail(e.message) }
  })

cli.command("tx-status")
  .description("Check transaction status")
  .requiredOption("--hash <hash>", "Transaction hash")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { getTxStatus } = await import("./lib/balance.js")
      json(await getTxStatus(opts.hash, chain))
    } catch (e) { fail(e.message) }
  })

cli.command("sign-message")
  .description("Sign a message (EIP-191)")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--message <message>", "Message to sign")
  .action(async (opts) => {
    try {
      const { requireScope } = await import("./lib/session.js")
      requireScope(opts.token, "full")
      const { signMessage } = await import("./lib/signing.js")
      json(await signMessage(opts.message))
    } catch (e) { fail(e.message) }
  })

cli.command("receive")
  .description("Show receive addresses")
  .action(async () => {
    try {
      const globalOpts = cli.opts()
      const { getReceiveInfo } = await import("./lib/keystore.js")
      let chainId = null
      if (globalOpts.chain) {
        const chains = await getChains()
        chainId = chains.resolveChainId(globalOpts.chain)
      }
      json(getReceiveInfo(chainId))
    } catch (e) { fail(e.message) }
  })

cli.command("allowances")
  .description("Check token allowances")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--asset <asset>", "Token symbol or contract address")
  .requiredOption("--spender <address>", "Spender address")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { getAllowances } = await import("./lib/balance.js")
      json(await getAllowances(opts.token, chain, opts.asset, opts.spender))
    } catch (e) { fail(e.message) }
  })

cli.command("history")
  .description("Show transaction history")
  .requiredOption("--token <token>", "Session token")
  .option("--limit <n>", "Number of entries", "50")
  .action(async (opts) => {
    try {
      const { requireScope } = await import("./lib/session.js")
      requireScope(opts.token, "read")
      const globalOpts = cli.opts()
      const { getHistory } = await import("./lib/tx-logger.js")
      // Resolve chain name to chainId for consistent filtering
      let chainFilter = globalOpts.chain || null
      if (chainFilter) {
        try {
          const chains = await getChains()
          chainFilter = chains.resolveChainId(chainFilter)
        } catch { /* keep original string if resolution fails */ }
      }
      json(getHistory(chainFilter, parseInt(opts.limit)))
    } catch (e) { fail(e.message) }
  })

cli.command("chain-info")
  .description("Show chain capabilities")
  .action(async () => {
    try {
      const chain = await resolveChain()
      const chains = await getChains()
      const chainId = chains.resolveChainId(chain)
      const chainObj = chains.viemChain(chainId)
      const cfg = chains.chainConfig(chainId)
      let gasless = { available: false, reason: "No bundler API key" }
      try {
        const { isGaslessAvailable } = await import("./lib/paymaster.js")
        gasless = await isGaslessAvailable(chainId)
      } catch { /* ignore */ }
      json({
        chainId,
        name: chainObj.name,
        nativeCurrency: chainObj.nativeCurrency,
        source: cfg ? "configured" : "viem-builtin",
        directTx: true,
        gasless,
        configuredTokens: cfg?.tokens ? Object.keys(cfg.tokens) : [],
      })
    } catch (e) { fail(e.message) }
  })

cli.command("chains")
  .description("List all supported chains")
  .action(async () => {
    try {
      const chains = await getChains()
      const cfg = chains.loadConfig()
      const list = Object.entries(cfg.chains || {}).map(([name, entry]) => ({
        name, chainId: entry.chainId, tokens: Object.keys(entry.tokens || {}),
      }))
      json({ chains: list })
    } catch (e) { fail(e.message) }
  })

cli.command("upgrade-7702")
  .description("Upgrade EOA via EIP-7702")
  .requiredOption("--token <token>", "Session token")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { upgradeVia7702 } = await import("./lib/eip7702.js")
      json(await upgradeVia7702(opts.token, chain))
    } catch (e) { fail(e.message) }
  })

cli.command("deploy-4337")
  .description("Deploy Smart Account (gasless)")
  .requiredOption("--token <token>", "Session token")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { requireScope } = await import("./lib/session.js")
      requireScope(opts.token, "full")
      json({ status: "auto_deploy_on_first_use", note: "Smart Account is deployed automatically on first gasless transaction.", chain })
    } catch (e) { fail(e.message) }
  })

cli.command("revoke-7702")
  .description("Revoke EIP-7702 delegation")
  .requiredOption("--token <token>", "Session token")
  .action(async (opts) => {
    try {
      const chain = await resolveChain()
      const { revokeVia7702 } = await import("./lib/eip7702.js")
      json(await revokeVia7702(opts.token, chain))
    } catch (e) { fail(e.message) }
  })

cli.command("sign-typed-data")
  .description("Sign typed data (EIP-712)")
  .requiredOption("--token <token>", "Session token")
  .requiredOption("--data <json>", "EIP-712 typed data as JSON")
  .action(async (opts) => {
    try {
      const { requireScope } = await import("./lib/session.js")
      requireScope(opts.token, "full")
      const { signTypedData } = await import("./lib/signing.js")
      json(await signTypedData(JSON.parse(opts.data)))
    } catch (e) { fail(e.message) }
  })

cli.command("wallets")
  .description("List all wallet profiles")
  .action(async () => {
    try {
      const { listWallets, walletId } = await import("./lib/paths.js")
      json({ currentWalletId: walletId, wallets: listWallets() })
    } catch (e) { fail(e.message) }
  })

cli.command("wallet-id")
  .description("Show current wallet ID")
  .action(async () => {
    try {
      const { walletId, WALLET_DIR } = await import("./lib/paths.js")
      json({ walletId, walletDir: WALLET_DIR })
    } catch (e) { fail(e.message) }
  })

// --- Run ---
cli.parseAsync(process.argv).catch(e => fail(e.message))
