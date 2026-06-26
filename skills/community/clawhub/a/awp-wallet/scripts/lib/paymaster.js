import { erc20Abi } from "viem"
import { resolveChainId, chainConfig, publicClient, tokenInfo } from "./chains.js"
import { getAddress } from "./keystore.js"
import { createClients } from "./bundler.js"

async function userHasStablecoin(chainId) {
  try {
    const addr = getAddress("eoa")
    const { address: usdcAddr, decimals } = await tokenInfo(chainId, "USDC")
    const client = publicClient(chainId)
    const bal = await client.readContract({
      address: usdcAddr, abi: erc20Abi,
      functionName: "balanceOf", args: [addr]
    })
    // >= 0.01 USDC, calculate threshold based on actual decimals (BSC uses 18 decimals, not 6)
    const threshold = (10n ** BigInt(decimals)) / 100n
    return BigInt(bal) >= threshold
  } catch { return false }
}

export async function selectStrategy(chain) {
  const chainId = resolveChainId(chain)
  const strategies = []
  const cfg = chainConfig(chain)

  if (cfg?.gasStrategy === "verifying_paymaster") strategies.push("verifying_paymaster")
  if (await userHasStablecoin(chainId)) strategies.push("erc20_paymaster")
  strategies.push("smart_account")  // fallback

  return strategies
}

export async function isGaslessAvailable(chainNameOrId) {
  try {
    const { bundlerClient } = createClients(chainNameOrId)
    const entryPoints = await bundlerClient.request({
      method: "eth_supportedEntryPoints", params: []
    })
    return { available: true, entryPoints }
  } catch (err) {
    return { available: false, reason: err.message }
  }
}

export function paymasterFor(chainNameOrId, strategy, paymasterClient) {
  const chainId = resolveChainId(chainNameOrId)

  if (strategy === "verifying_paymaster") {
    return paymasterClient  // Standard viem PaymasterClient, no extra context
  }

  if (strategy === "erc20_paymaster") {
    // Wrap paymasterClient to inject token context into each request
    const cfg = chainConfig(chainId)
    const usdcAddr = cfg?.tokens?.USDC?.address
    return {
      async getPaymasterData(params) {
        return paymasterClient.getPaymasterData({
          ...params, context: { token: usdcAddr }
        })
      },
      async getPaymasterStubData(params) {
        return paymasterClient.getPaymasterStubData({
          ...params, context: { token: usdcAddr }
        })
      },
    }
  }

  return paymasterClient  // Fallback: smart_account strategy uses standard paymaster
}
