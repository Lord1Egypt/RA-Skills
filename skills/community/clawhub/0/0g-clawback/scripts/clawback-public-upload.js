import { ZgFile, Indexer } from '@0gfoundation/0g-ts-sdk'
import { ethers } from 'ethers'
import path from 'path'
import fs from 'fs'
import 'dotenv/config'

// Initialize 0G SDK with your network configuration
const RPC_URL = process.env.RPC_URL
const INDEXER_RPC = process.env.INDEXER_RPC

// Initialize provider and signer
const provider = new ethers.JsonRpcProvider(RPC_URL)
const signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider)

// Initialize indexer
const indexer = new Indexer(INDEXER_RPC)

async function uploadFile(filePath) {
  // Resolve to absolute path to avoid tracking issues inside OpenClaw workspaces
  const absolutePath = path.resolve(filePath)

  // Validate that the file actually exists before hitting the SDK
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`File not found at path: ${absolutePath}`)
  }

  const file = await ZgFile.fromFilePath(absolutePath)

  // Must call merkleTree() before upload — populates internal state
  const [tree, treeErr] = await file.merkleTree()
  if (treeErr !== null) throw new Error(`Merkle tree error: ${treeErr}`)

  console.log('Root Hash:', tree?.rootHash())

  const [tx, uploadErr] = await indexer.upload(file, RPC_URL, signer)
  if (uploadErr !== null) throw new Error(`Upload error: ${uploadErr}`)

  await file.close() // Always close when done

  // Handle both single and fragmented (>4GB) responses
  if ('rootHash' in tx) {
    return { rootHash: tx.rootHash, txHash: tx.txHash }
  } else {
    return { rootHashes: tx.rootHashes, txHashes: tx.txHashes }
  }
}

async function main() {
  // process.argv[0] is the node executable path
  // process.argv[1] is the script path
  // process.argv[2] is the first user-provided argument (the file path)
  const targetFilePath = process.argv[2]

  if (!targetFilePath) {
    console.error('Error: Please provide a file path.')
    console.log('Usage: node clawback.js <file-path>')
    process.exit(1)
  }

  try {
    console.log(`Starting ClawBack upload for: ${targetFilePath}...`)
    const result = await uploadFile(targetFilePath)
    console.log('Upload completed successfully!')
    console.log(JSON.stringify(result, null, 2))
  } catch (error) {
    console.error('ClawBack Operation Failed:', error.message)
    process.exit(1)
  }
}

main()