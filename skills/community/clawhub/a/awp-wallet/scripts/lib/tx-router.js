import { resolveChainId, publicClient, viemChain, loadConfig, getRpcUrl, tokenInfo } from "./chains.js"
import { formatUnits } from "viem"
import { getAddress } from "./keystore.js"
import { sendDirect } from "./direct-tx.js"
import { sendGasless } from "./gasless-tx.js"
import { requireScope } from "./session.js"
import { validateTransaction, validateBatchOps } from "./tx-validator.js"
import { logTransaction } from "./tx-logger.js"
import { createWalletClient, http, encodeFunctionData, parseUnits, erc20Abi, getAddress as checksumAddr } from "viem"
import { loadSigner } from "./keystore.js"

async function selectMode(chain, asset) {
  const chainId = resolveChainId(chain)
  const client = publicClient(chainId)
  const eoaAddr = getAddress("eoa")
  const balance = await client.getBalance({ address: eoaAddr })
  const gasPrice = await client.getGasPrice()
  const estimatedGas = asset ? 65_000n : 21_000n
  const needed = gasPrice * estimatedGas * 2n  // 2x buffer

  if (balance >= needed) return "direct"

  // Need gasless — check if bundler key exists
  const cfg = loadConfig()
  const hasKey = (cfg.bundlerProviders || []).some(p => process.env[p.envKey])
  if (hasKey) return "gasless"

  // Neither path is available
  throw new Error(
    `Insufficient native gas for direct transaction (have: ${balance}, need: ~${needed}), ` +
    `and no bundler API key configured for gasless mode. ` +
    `Either: (1) fund the EOA with native gas, or (2) set PIMLICO_API_KEY for gasless transactions.`
  )
}

export async function sendTransaction({ sessionToken, to, amount, asset, chain, mode }) {
  requireScope(sessionToken, "transfer")
  await validateTransaction({ to, amount, asset, chain })

  const selectedMode = mode || await selectMode(chain, asset)

  const result = selectedMode === "direct"
    ? await sendDirect({ to, amount, asset, chain })
    : await sendGasless({ to, amount, asset, chain })

  await logTransaction({ ...result, type: "transfer" })
  return result
}

export async function batchTransaction({ sessionToken, operations, chain, mode }) {
  requireScope(sessionToken, "transfer")
  // Validate all operations at once using batchSpent accumulator (prevent daily limit bypass)
  await validateBatchOps(operations, chain)

  // Call underlying send functions directly, bypassing sendTransaction (avoid duplicate validation/requireScope)
  const selectedMode = mode || await selectMode(chain, operations[0]?.asset)
  const results = []
  for (const op of operations) {
    const result = selectedMode === "direct"
      ? await sendDirect({ to: op.to, amount: op.amount, asset: op.asset, chain })
      : await sendGasless({ to: op.to, amount: op.amount, asset: op.asset, chain })
    await logTransaction({ ...result, type: "transfer" })
    results.push(result)
  }
  return { status: "batch_complete", results }
}

export async function approveToken({ sessionToken, asset, spender, amount, chain, mode, _logType = "approve", _logStatus = "approved" }) {
  requireScope(sessionToken, "transfer")
  // approve only needs address validation, not amount validation (amount=0 is valid for revoke)
  await validateTransaction({ to: spender, amount: "0", asset, chain, _skipAmountCheck: true })

  const chainId = resolveChainId(chain)
  const chainObj = viemChain(chainId)
  const { address: tokenAddr, decimals } = await tokenInfo(chainId, asset)

  const selectedMode = mode || await selectMode(chain, asset)

  if (selectedMode === "direct") {
    const { account: signer } = loadSigner()
    const walletClient = createWalletClient({
      account: signer, chain: chainObj,
      transport: http(getRpcUrl(chainId)),
    })
    const hash = await walletClient.sendTransaction({
      to: tokenAddr,
      data: encodeFunctionData({
        abi: erc20Abi, functionName: "approve",
        args: [checksumAddr(spender), parseUnits(amount, decimals)]
      }),
    })
    const receipt = await publicClient(chainId).waitForTransactionReceipt({
      hash, timeout: 120_000, confirmations: 1,
    })
    const result = {
      type: _logType, status: _logStatus, mode: "direct", txHash: hash,
      chain: chainObj.name, chainId, to: spender, asset, spender, amount,
      gasUsed: receipt.gasUsed.toString(),
      blockNumber: Number(receipt.blockNumber),
    }
    await logTransaction(result)
    return result
  } else {
    // gasless approve: construct approve call data and send via gasless
    const result = await sendGasless({
      to: spender, amount: "0", asset, chain,
      _customCall: {
        to: tokenAddr, value: 0n,
        data: encodeFunctionData({
          abi: erc20Abi, functionName: "approve",
          args: [checksumAddr(spender), parseUnits(amount, decimals)]
        })
      }
    })
    const approveResult = { ...result, type: _logType, status: _logStatus, to: spender, asset, spender, amount }
    await logTransaction(approveResult)
    return approveResult
  }
}

export async function revokeApproval({ sessionToken, asset, spender, chain, mode }) {
  return approveToken({ sessionToken, asset, spender, amount: "0", chain, mode, _logType: "revoke", _logStatus: "revoked" })
}

export async function estimateGas({ to, amount, asset, chain }) {
  const chainId = resolveChainId(chain)
  const chainObj = viemChain(chainId)
  const client = publicClient(chainId)
  const eoaAddr = getAddress("eoa")

  let estimatedGas, gasPrice
  try {
    gasPrice = await client.getGasPrice()
    if (asset) {
      const { address: tokenAddr, decimals } = await tokenInfo(chainId, asset)
      estimatedGas = await client.estimateGas({
        account: eoaAddr,
        to: tokenAddr,
        data: encodeFunctionData({
          abi: erc20Abi, functionName: "transfer",
          args: [checksumAddr(to), parseUnits(amount, decimals)]
        }),
      })
    } else {
      estimatedGas = await client.estimateGas({
        account: eoaAddr,
        to: checksumAddr(to),
        value: parseUnits(amount, chainObj.nativeCurrency.decimals),
      })
    }
  } catch {
    gasPrice = gasPrice || 0n
    estimatedGas = asset ? 65_000n : 21_000n
  }

  const estimatedCost = gasPrice * estimatedGas
  const cfg = loadConfig()
  const hasKey = (cfg.bundlerProviders || []).some(p => process.env[p.envKey])

  return {
    direct: {
      estimatedGas: estimatedGas.toString(),
      gasPrice: gasPrice.toString(),
      estimatedCost: estimatedCost.toString(),
      estimatedCostFormatted: `${formatUnits(estimatedCost, chainObj.nativeCurrency.decimals)} ${chainObj.nativeCurrency.symbol}`,
    },
    gasless: {
      available: hasKey,
      cost: hasKey ? "0 (paymaster sponsored)" : "N/A (no bundler API key)",
    },
  }
}
