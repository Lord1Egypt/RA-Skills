import { encodeFunctionData, parseUnits, erc20Abi, getAddress as checksumAddr } from "viem"
import { entryPoint07Address } from "viem/account-abstraction"
import { createSmartAccountClient } from "permissionless"
import { toEcdsaKernelSmartAccount } from "permissionless/accounts"
import { loadSigner, getAddress, saveSmartAccountAddress } from "./keystore.js"
import { viemChain, publicClient, tokenInfo, resolveChainId, chainConfig } from "./chains.js"
import { createClients } from "./bundler.js"
import { selectStrategy, paymasterFor } from "./paymaster.js"

async function buildClient(chain, strategy) {
  const chainId = resolveChainId(chain)
  const chainObj = viemChain(chainId)
  const client = publicClient(chainId)
  const { account: signer } = loadSigner()

  const smartAccount = await toEcdsaKernelSmartAccount({
    client,
    owners: [signer],
    entryPoint: { address: entryPoint07Address, version: "0.7" },
  })

  // Deduplicate: only write to meta.json if not already recorded
  try {
    if (getAddress("smart", chainId) !== smartAccount.address) {
      saveSmartAccountAddress(chainId, smartAccount.address)
    }
  } catch {
    saveSmartAccountAddress(chainId, smartAccount.address)
  }

  const { bundlerClient, paymasterClient, bundlerTransport } = createClients(chainId)
  const paymaster = paymasterFor(chainId, strategy, paymasterClient)

  const smartAccountClient = createSmartAccountClient({
    account: smartAccount,
    chain: chainObj,
    bundlerTransport,  // Use raw fallback transport, not client.transport
    paymaster,
  })

  return { smartAccountClient, smartAccount, bundlerClient }
}

export async function sendGasless({ to, amount, asset, chain, _customCall }) {
  const chainId = resolveChainId(chain)
  const strategies = await selectStrategy(chain)

  let lastError
  for (const strategy of strategies) {
    // Build client once per strategy — reuse across nonce retries
    let smartAccountClient, smartAccount, bundlerClient
    try {
      ({ smartAccountClient, smartAccount, bundlerClient } = await buildClient(chain, strategy))
    } catch (err) {
      lastError = err
      continue  // Strategy setup failed -> try next strategy
    }

    // Support custom call data (for approve/revoke and other non-transfer operations)
    let callData
    if (_customCall) {
      callData = _customCall
    } else if (asset) {
      const { address: tokenAddr, decimals } = await tokenInfo(chainId, asset)
      callData = { to: tokenAddr, value: 0n, data: encodeFunctionData({
        abi: erc20Abi, functionName: "transfer",
        args: [checksumAddr(to), parseUnits(amount, decimals)]
      })}
    } else {
      callData = { to: checksumAddr(to), value: parseUnits(amount, viemChain(chainId).nativeCurrency.decimals), data: "0x" }
    }

    const MAX_NONCE_RETRIES = 3
    for (let attempt = 0; attempt <= MAX_NONCE_RETRIES; attempt++) {
      try {
        // permissionless 0.3 API: pass calls array directly, no manual encodeCalls needed
        const userOpHash = await smartAccountClient.sendUserOperation({
          calls: [callData]
        })
        const receipt = await bundlerClient.waitForUserOperationReceipt({
          hash: userOpHash, timeout: 60_000,
        })

        return {
          status: "sent", mode: "gasless",
          txHash: receipt.receipt.transactionHash,  // Actual on-chain hash
          userOpHash,
          chain: viemChain(chainId).name, chainId, to, amount,
          asset: asset || viemChain(chainId).nativeCurrency.symbol,
          gasStrategy: strategy,
          smartAccount: smartAccount.address,
          blockNumber: Number(receipt.receipt.blockNumber),
        }
      } catch (err) {
        lastError = err
        // Nonce conflict -> retry same strategy (inner loop)
        if ((err.message?.includes("AA25") || err.message?.includes("nonce")) && attempt < MAX_NONCE_RETRIES) {
          await new Promise(r => setTimeout(r, 2000))
          continue
        }
        // Paymaster rejected -> break inner loop, try next strategy
        if (err.message?.match(/paymaster|AA3/i)) break
        throw err
      }
    }
  }
  throw new Error(`All gas strategies failed. Last error: ${lastError?.message}`)
}
