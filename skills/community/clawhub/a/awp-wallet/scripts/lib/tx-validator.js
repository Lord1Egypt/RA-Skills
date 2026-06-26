import { isAddress, getAddress as checksumAddr } from "viem"
import { getAddress as walletGetAddress } from "./keystore.js"
import { getHistory } from "./tx-logger.js"
import { loadConfig, resolveChainId, viemChain, nativeSymbol } from "./chains.js"

function checkLimit(amount, limitStr, label) {
  if (!limitStr) return  // No limit configured
  if (parseFloat(amount) > parseFloat(limitStr)) {
    throw new Error(`${label} exceeded: ${amount} > ${limitStr}`)
  }
}

function checkDailyLimit(amount, asset, chain, batchSpent = {}) {
  const cfg = loadConfig()
  // Resolve null asset (native transfer) to the chain's native currency symbol
  const resolvedAsset = asset || nativeSymbol(chain)
  const normalizedAsset = resolvedAsset.toUpperCase()
  const limitStr = cfg.dailyLimits?.[normalizedAsset] || cfg.dailyLimits?.default
  if (!limitStr) return
  // Use numeric chainId for history filtering (log entries store chainId as number)
  const chainId = resolveChainId(chain)
  const history = getHistory(null, Infinity)  // get ALL entries (no limit), filter by chainId below
  const since = Date.now() - 24 * 60 * 60 * 1000
  const spent = history
    .filter(e => new Date(e.timestamp).getTime() > since
      && e.chainId === chainId
      && (e.asset || "").toUpperCase() === normalizedAsset
      && e.type !== "approve" && e.type !== "revoke")  // Only accumulate transfers
    .reduce((sum, e) => sum + parseFloat(e.amount), 0)
  // Add the accumulated amount already validated in this batch but not yet written to the log
  const batchPending = batchSpent[normalizedAsset] || 0
  if (spent + batchPending + parseFloat(amount) > parseFloat(limitStr)) {
    throw new Error(`Daily limit exceeded for ${resolvedAsset}.`)
  }
}

export async function validateTransaction({ to, amount, asset, chain, _batchSpent, _skipAmountCheck }) {
  // 0. Amount validation (can be skipped for approve/revoke scenarios)
  if (!_skipAmountCheck) {
    const parsedAmount = parseFloat(amount)
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      throw new Error("Amount must be a positive number.")
    }
  }
  // 1. Address validation
  if (!isAddress(to)) throw new Error(`Invalid Ethereum address: ${to}`)
  const checksummed = checksumAddr(to)
  if (checksummed === "0x0000000000000000000000000000000000000000") {
    throw new Error("Cannot send to zero address.")
  }
  // Reject self-transfers
  const eoaAddr = walletGetAddress("eoa")
  if (checksummed.toLowerCase() === eoaAddr.toLowerCase()) {
    throw new Error("Cannot send to own address.")
  }
  // Check smart account self-transfer (ignore if smart account doesn't exist)
  try {
    const chainId = resolveChainId(chain)
    const smartAddr = walletGetAddress("smart", chainId)
    if (smartAddr && checksummed.toLowerCase() === smartAddr.toLowerCase()) {
      throw new Error("Cannot send to own Smart Account address.")
    }
  } catch (err) {
    if (err.message?.includes("Cannot send to own")) throw err
    // Smart account lookup failure is non-fatal (account may not exist)
  }

  // 2. Allowlist
  const cfg = loadConfig()
  if (cfg.allowlistMode) {
    const allowed = (cfg.allowlistedRecipients || []).map(a => a.toLowerCase())
    if (!allowed.includes(checksummed.toLowerCase())) {
      throw new Error(`Recipient ${checksummed} not in allowlist.`)
    }
  }

  // 3. Per-transaction limit
  const resolvedAsset = asset || nativeSymbol(chain)
  const perTxLimit = cfg.perTransactionMax?.[resolvedAsset.toUpperCase()] || cfg.perTransactionMax?.default
  checkLimit(amount, perTxLimit, "Per-transaction limit")

  // 4. Daily limit (in batch mode, includes accumulated amounts validated but not yet persisted)
  checkDailyLimit(amount, asset, chain, _batchSpent || {})
}

export async function validateBatchOps(operations, chain) {
  // Accumulate validated amounts within the batch to prevent bypassing daily limits via splitting
  const batchSpent = {}
  for (const op of operations) {
    if (op.type === "raw") throw new Error("Raw call type not allowed in batch.")
    await validateTransaction({ to: op.to, amount: op.amount, asset: op.asset, chain, _batchSpent: batchSpent })
    // Accumulate the amount for this batch
    const asset = (op.asset || nativeSymbol(chain)).toUpperCase()
    batchSpent[asset] = (batchSpent[asset] || 0) + parseFloat(op.amount)
  }
}
