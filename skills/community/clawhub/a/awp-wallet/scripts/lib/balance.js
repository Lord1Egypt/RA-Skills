import { erc20Abi, formatUnits } from "viem"
import { requireScope } from "./session.js"
import { getAddress } from "./keystore.js"
import { resolveChainId, publicClient, viemChain, chainConfig, tokenInfo, loadConfig } from "./chains.js"

export async function getBalance(sessionToken, chain, asset) {
  requireScope(sessionToken, "read")
  const chainId = resolveChainId(chain)
  const client = publicClient(chainId)
  const eoaAddr = getAddress("eoa")
  const smartAddr = getAddress("smart", chainId)
  const addrs = [eoaAddr, smartAddr].filter(Boolean)
  const chainObj = viemChain(chainId)
  const cfg = chainConfig(chainId)

  const queries = []
  // Fetch custom token info outside the loop (one RPC call shared by both addresses)
  let customTokenInfo = null
  if (asset && /^0x/i.test(asset)) {
    customTokenInfo = await tokenInfo(chainId, asset)
  }

  for (const addr of addrs) {
    // Native balance
    queries.push(
      client.getBalance({ address: addr })
        .then(b => ({ addr, sym: chainObj.nativeCurrency.symbol, bal: b, dec: chainObj.nativeCurrency.decimals }))
        .catch(() => null)
    )
    // Pre-configured tokens
    for (const [sym, info] of Object.entries(cfg?.tokens || {})) {
      if (asset && sym !== asset.toUpperCase()) continue
      queries.push(
        client.readContract({ address: info.address, abi: erc20Abi, functionName: "balanceOf", args: [addr] })
          .then(b => ({ addr, sym, bal: b, dec: info.decimals }))
          .catch(() => null)
      )
    }
    // Query custom token by contract address
    if (customTokenInfo) {
      queries.push(
        client.readContract({ address: customTokenInfo.address, abi: erc20Abi, functionName: "balanceOf", args: [addr] })
          .then(b => ({ addr, sym: customTokenInfo.symbol, bal: b, dec: customTokenInfo.decimals }))
          .catch(() => null)
      )
    }
  }

  const results = (await Promise.allSettled(queries))
    .filter(r => r.status === "fulfilled" && r.value).map(r => r.value)

  const balances = {}
  for (const { addr, sym, bal, dec } of results) {
    const label = addrs.length > 1 ? `${sym}(${addr === eoaAddr ? "EOA" : "Smart"})` : sym
    balances[label] = formatUnits(BigInt(bal), dec)
  }

  return { chain: chainObj.name, chainId, eoaAddress: eoaAddr, smartAccountAddress: smartAddr || null, balances }
}

export async function getAllowances(sessionToken, chain, asset, spender) {
  requireScope(sessionToken, "read")
  const chainId = resolveChainId(chain)
  const chainObj = viemChain(chainId)
  const client = publicClient(chainId)
  const eoaAddr = getAddress("eoa")
  const { address: tokenAddr, symbol, decimals } = await tokenInfo(chainId, asset)

  const spenders = spender
    ? [{ name: "specified", address: spender }]
    : []

  const results = []
  for (const s of spenders) {
    const allowance = await client.readContract({
      address: tokenAddr, abi: erc20Abi,
      functionName: "allowance", args: [eoaAddr, s.address]
    })
    results.push({ spender: s.address, name: s.name, allowance: formatUnits(allowance, decimals) })
  }
  return { token: symbol, chain: chainObj.name, allowances: results }
}

export async function getTxStatus(txHash, chain) {
  const client = publicClient(resolveChainId(chain))
  try {
    const receipt = await client.getTransactionReceipt({ hash: txHash })
    return {
      status: receipt.status === "success" ? "confirmed" : "reverted",
      blockNumber: Number(receipt.blockNumber),
      gasUsed: receipt.gasUsed.toString(),
    }
  } catch {
    return { status: "pending" }
  }
}

export async function getPortfolio(sessionToken) {
  requireScope(sessionToken, "read")
  const cfg = loadConfig()
  const chainNames = Object.keys(cfg.chains || {})

  const results = await Promise.allSettled(
    chainNames.map(name => getBalance(sessionToken, name, null))
  )

  const chains = chainNames.map((name, i) => {
    const r = results[i]
    if (r.status === "fulfilled") return r.value
    return { chain: name, chainId: cfg.chains[name]?.chainId, error: r.reason?.message }
  })

  return { chains }
}
