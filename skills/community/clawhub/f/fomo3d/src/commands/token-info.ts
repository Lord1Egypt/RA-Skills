import { readConfig, requirePrivateKey, ADDRESSES } from "../lib/config.js"
import { getPublicClient, getWalletClient } from "../lib/client.js"
import { getTokenBalance } from "../lib/erc20.js"
import { output, log } from "../lib/output.js"
import {
  PORTAL_ADDRESS, PORTAL_ABI, USDT_ADDRESS,
  TOKEN_STATUS, type TokenStatusCode,
  FOMO_TOKEN,
} from "../lib/flap.js"
import { formatUnits } from "viem"

export async function tokenInfo(args: string[]) {
  const config = readConfig()
  const publicClient = getPublicClient(config.network, config.rpcUrl)

  const fomoToken = ADDRESSES[config.network].fomoToken

  // mainnet 才能查 Portal 状态
  if (config.network === "mainnet") {
    const pk = requirePrivateKey(config)
    const walletClient = getWalletClient(pk, config.network, config.rpcUrl)
    const account = walletClient.account!.address

    // 并行查询
    const [tokenState, fomoBalance, usdtBalance] = await Promise.all([
      publicClient.readContract({
        address: PORTAL_ADDRESS,
        abi: PORTAL_ABI,
        functionName: "getTokenV6",
        args: [fomoToken],
      }) as Promise<{
        status: number
        quoteToken: `0x${string}`
        currentPrice: bigint
        totalSupply: bigint
        reserveBalance: bigint
        progress: bigint
      }>,
      getTokenBalance(publicClient, fomoToken, account),
      getTokenBalance(publicClient, USDT_ADDRESS, account),
    ])

    const statusCode = tokenState.status as TokenStatusCode
    const statusName = TOKEN_STATUS[statusCode] ?? "Unknown"
    const phase = statusCode === 1 ? "内盘 (Portal)" : statusCode === 2 ? "外盘 (PancakeSwap)" : statusName

    output({
      token: fomoToken,
      network: config.network,
      status: statusName,
      statusCode,
      phase,
      quoteToken: tokenState.quoteToken,
      currentPrice: tokenState.currentPrice.toString(),
      totalSupply: tokenState.totalSupply.toString(),
      reserveBalance: tokenState.reserveBalance.toString(),
      progress: tokenState.progress.toString(),
      fomoBalance: fomoBalance.toString(),
      usdtBalance: usdtBalance.toString(),
      account,
    }, (d) => {
      log(`\nFOMO Token Info (${d.network})`)
      log(`Token: ${d.token}`)
      log(`Phase: ${d.phase}`)
      log(`Status: ${d.status} (${d.statusCode})`)
      log(`Quote Token: ${d.quoteToken}`)
      log(`Price: ${formatUnits(BigInt(d.currentPrice), 18)} USDT`)
      log(`Progress: ${formatUnits(BigInt(d.progress), 16)}%`)
      log(`\nYour Balances:`)
      log(`FOMO: ${formatUnits(BigInt(d.fomoBalance), 18)}`)
      log(`USDT: ${formatUnits(BigInt(d.usdtBalance), 18)}`)
      log("")
    })
  } else {
    // testnet 只显示余额
    const pk = requirePrivateKey(config)
    const walletClient = getWalletClient(pk, config.network, config.rpcUrl)
    const account = walletClient.account!.address

    const fomoBalance = await getTokenBalance(publicClient, fomoToken, account)

    output({
      token: fomoToken,
      network: config.network,
      status: "N/A",
      phase: "testnet (no FLAP Portal)",
      fomoBalance: fomoBalance.toString(),
      account,
    }, (d) => {
      log(`\nFOMO Token Info (${d.network})`)
      log(`Token: ${d.token}`)
      log(`Phase: ${d.phase}`)
      log(`FOMO Balance: ${formatUnits(BigInt(d.fomoBalance), 18)}`)
      log(`\nNote: Buy/sell only available on mainnet.`)
      log("")
    })
  }
}
