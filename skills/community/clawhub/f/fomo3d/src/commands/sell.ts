import { readConfig, requirePrivateKey, ADDRESSES } from "../lib/config.js"
import { getPublicClient, getWalletClient } from "../lib/client.js"
import { ensureAllowance, getTokenBalance } from "../lib/erc20.js"
import { output, log, fatal } from "../lib/output.js"
import { getFlagValue } from "../lib/args.js"
import { FLAP_SKILL_ADDRESS, FLAP_SKILL_ABI } from "../lib/flap.js"

export async function sell(args: string[]) {
  const amountStr = getFlagValue(args, "--amount")
  const percentStr = getFlagValue(args, "--percent")

  if (!amountStr && !percentStr) {
    fatal("Missing --amount <token_wei> or --percent <bps>. Usage: fomo3d sell --amount 1000000000000000000 or fomo3d sell --percent 5000")
  }
  if (amountStr && percentStr) {
    fatal("Cannot use both --amount and --percent")
  }

  const config = readConfig()

  if (config.network !== "mainnet") {
    fatal("Sell is only available on mainnet.")
  }

  const pk = requirePrivateKey(config)
  const publicClient = getPublicClient(config.network, config.rpcUrl)
  const walletClient = getWalletClient(pk, config.network, config.rpcUrl)
  const fomoToken = ADDRESSES[config.network].fomoToken
  const account = walletClient.account!.address

  if (amountStr) {
    // 按数量卖出
    const tokenAmount = BigInt(amountStr)
    if (tokenAmount <= 0n) fatal("Amount must be positive")

    await ensureAllowance(publicClient, walletClient, fomoToken, FLAP_SKILL_ADDRESS, tokenAmount)

    log(`Selling ${tokenAmount} FOMO tokens (wei)...`)
    const hash = await walletClient.writeContract({
      address: FLAP_SKILL_ADDRESS,
      abi: FLAP_SKILL_ABI,
      functionName: "sellTokens",
      args: [fomoToken, tokenAmount],
      chain: walletClient.chain,
    })

    log(`Transaction: ${hash}`)
    const receipt = await publicClient.waitForTransactionReceipt({ hash })

    output({
      txHash: hash,
      blockNumber: Number(receipt.blockNumber),
      status: receipt.status,
      tokensSold: tokenAmount.toString(),
      method: "sellTokens",
    }, (d) => {
      log(`\nSell ${d.status === "success" ? "successful" : "failed"}!`)
      log(`Tokens sold: ${d.tokensSold}`)
      log(`Block: ${d.blockNumber}`)
      log("")
    })
  } else {
    // 按比例卖出
    const percentBps = BigInt(percentStr!)
    if (percentBps <= 0n || percentBps > 10000n) fatal("Percent must be 1-10000 (bps, 10000=100%)")

    // 授权全部余额
    const balance = await getTokenBalance(publicClient, fomoToken, account)
    if (balance === 0n) fatal("No FOMO tokens to sell")

    await ensureAllowance(publicClient, walletClient, fomoToken, FLAP_SKILL_ADDRESS, balance)

    log(`Selling ${percentBps} bps (${Number(percentBps) / 100}%) of FOMO holdings...`)
    const hash = await walletClient.writeContract({
      address: FLAP_SKILL_ADDRESS,
      abi: FLAP_SKILL_ABI,
      functionName: "sellTokensByPercent",
      args: [fomoToken, percentBps],
      chain: walletClient.chain,
    })

    log(`Transaction: ${hash}`)
    const receipt = await publicClient.waitForTransactionReceipt({ hash })

    output({
      txHash: hash,
      blockNumber: Number(receipt.blockNumber),
      status: receipt.status,
      percentBps: percentBps.toString(),
      method: "sellTokensByPercent",
    }, (d) => {
      log(`\nSell ${d.status === "success" ? "successful" : "failed"}!`)
      log(`Sold: ${d.percentBps} bps (${Number(d.percentBps) / 100}%)`)
      log(`Block: ${d.blockNumber}`)
      log("")
    })
  }
}
