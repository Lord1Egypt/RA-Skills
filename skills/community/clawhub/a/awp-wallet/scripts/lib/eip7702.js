import { createWalletClient, http, zeroAddress } from "viem"
import { eip7702Actions } from "viem/experimental"
import { requireScope } from "./session.js"
import { loadSigner, getAddress } from "./keystore.js"
import { viemChain, publicClient, resolveChainId, getRpcUrl } from "./chains.js"

export async function upgradeVia7702(sessionToken, chain, target = "kernel") {
  requireScope(sessionToken, "full")
  const chainId = resolveChainId(chain)
  const client = publicClient(chainId)
  const balance = await client.getBalance({ address: getAddress("eoa") })
  const gasPrice = await client.getGasPrice()
  const estimatedFee = gasPrice * 100_000n  // Estimated gas fee for EIP-7702 transaction
  if (balance < estimatedFee) throw new Error(
    "EIP-7702 requires native gas in EOA. Use 'deploy-4337' for gasless setup instead."
  )

  const { account: signer } = loadSigner()
  const chainObj = viemChain(chainId)

  const walletClient = createWalletClient({
    account: signer,
    chain: chainObj,
    transport: http(getRpcUrl(chainId)),
  }).extend(eip7702Actions())

  // EIP-7702 upgrade transaction
  const authorization = await walletClient.signAuthorization({
    contractAddress: target === "kernel"
      ? "0x0DA6a956B9488eD4dd761E59f52FDc6c8068E6B5"  // Kernel v3 implementation address
      : target,
  })

  const hash = await walletClient.sendTransaction({
    authorizationList: [authorization],
    to: signer.address,
    data: "0x",
  })

  const receipt = await publicClient(chainId).waitForTransactionReceipt({
    hash, timeout: 120_000, confirmations: 1,
  })

  return {
    status: "upgraded", mode: "eip7702",
    txHash: hash, chain: chainObj.name,
    target, blockNumber: Number(receipt.blockNumber),
  }
}

export async function revokeVia7702(sessionToken, chain) {
  requireScope(sessionToken, "full")
  const chainId = resolveChainId(chain)
  const { account: signer } = loadSigner()
  const chainObj = viemChain(chainId)

  const walletClient = createWalletClient({
    account: signer,
    chain: chainObj,
    transport: http(getRpcUrl(chainId)),
  }).extend(eip7702Actions())

  // Revoke EIP-7702 delegation — set to zero address
  const authorization = await walletClient.signAuthorization({
    contractAddress: zeroAddress,
  })

  const hash = await walletClient.sendTransaction({
    authorizationList: [authorization],
    to: signer.address,
    data: "0x",
  })

  const receipt = await publicClient(chainId).waitForTransactionReceipt({
    hash, timeout: 120_000, confirmations: 1,
  })

  return {
    status: "revoked", mode: "eip7702",
    txHash: hash, chain: chainObj.name,
    blockNumber: Number(receipt.blockNumber),
  }
}
