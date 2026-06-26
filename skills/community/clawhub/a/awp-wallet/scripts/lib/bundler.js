import { http, fallback } from "viem"
import { createBundlerClient, createPaymasterClient } from "viem/account-abstraction"
import { viemChain, resolveChainId, loadConfig } from "./chains.js"

function expandUrl(template, chainId, apiKey) {
  // Resolve chain name for {chainName} placeholder
  // Alchemy requires specific names like "base-mainnet", "arb-mainnet"
  let chainName
  try {
    const cfg = loadConfig()
    for (const [name, entry] of Object.entries(cfg.chains || {})) {
      if (entry.chainId === chainId) {
        chainName = entry.alchemyName || name  // Prefer Alchemy-specific name
        break
      }
    }
  } catch { /* ignore */ }
  if (!chainName) {
    const chain = viemChain(chainId)
    chainName = (chain.name || `chain-${chainId}`).toLowerCase().replace(/\s+/g, "-")
  }
  return template
    .replace("{chainId}", String(chainId))
    .replace("{chainName}", chainName)
    .replace("{key}", apiKey)
}

export function createClients(chainNameOrId) {
  const chainId = resolveChainId(chainNameOrId)
  const chain = viemChain(chainId)
  const cfg = loadConfig()

  const providers = (cfg.bundlerProviders || [])
    .filter(p => process.env[p.envKey])
    .sort((a, b) => a.priority - b.priority)

  if (providers.length === 0)
    throw new Error("No bundler API key set. Export PIMLICO_API_KEY, ALCHEMY_API_KEY, or STACKUP_API_KEY.")

  // Create separate transports for bundler and paymaster (URLs differ for Alchemy/Stackup)
  const bundlerTransports = providers.map(p =>
    http(expandUrl(p.bundlerUrlTemplate, chainId, process.env[p.envKey]), { timeout: p.timeout })
  )
  const paymasterTransports = providers.map(p =>
    http(expandUrl(p.paymasterUrlTemplate || p.bundlerUrlTemplate, chainId, process.env[p.envKey]), { timeout: p.timeout })
  )

  const bundlerTransport = fallback(bundlerTransports)
  return {
    bundlerClient: createBundlerClient({ chain, transport: bundlerTransport }),
    paymasterClient: createPaymasterClient({ chain, transport: fallback(paymasterTransports) }),
    bundlerTransport,  // Raw transport, used by createSmartAccountClient
  }
}
