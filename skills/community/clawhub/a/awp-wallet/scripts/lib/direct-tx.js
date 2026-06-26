import { createWalletClient, http, encodeFunctionData, parseUnits, erc20Abi, getAddress as checksumAddr } from "viem"
import { loadSigner } from "./keystore.js"
import { viemChain, publicClient, tokenInfo, resolveChainId, getRpcUrl } from "./chains.js"

export async function sendDirect({ to, amount, asset, chain }) {
  const chainId = resolveChainId(chain)
  const chainObj = viemChain(chainId)
  const { account: signer } = loadSigner()

  const walletClient = createWalletClient({
    account: signer, chain: chainObj,
    transport: http(getRpcUrl(chainId)),
  })

  let hash
  if (asset) {
    const { address: tokenAddr, decimals } = await tokenInfo(chainId, asset)
    hash = await walletClient.sendTransaction({
      to: tokenAddr,
      data: encodeFunctionData({
        abi: erc20Abi, functionName: "transfer",
        args: [checksumAddr(to), parseUnits(amount, decimals)]
      }),
    })
  } else {
    const client = publicClient(chainId)
    const balance = await client.getBalance({ address: signer.address })
    const value = parseUnits(amount, chainObj.nativeCurrency.decimals)
    const gasPrice = await client.getGasPrice()
    if (balance < value + gasPrice * 21_000n)
      throw new Error("Insufficient balance for transfer + gas.")

    hash = await walletClient.sendTransaction({ to: checksumAddr(to), value })
  }

  const receipt = await publicClient(chainId).waitForTransactionReceipt({
    hash,
    timeout: 120_000,
    confirmations: 1,
  })
  return {
    status: "sent", mode: "direct", txHash: hash,
    chain: chainObj.name, chainId, to, amount,
    asset: asset || chainObj.nativeCurrency.symbol,
    gasUsed: receipt.gasUsed.toString(),
    blockNumber: Number(receipt.blockNumber),
  }
}
