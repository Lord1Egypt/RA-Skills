import { ZgFile, Indexer } from '@0gfoundation/0g-ts-sdk'
import { ethers } from 'ethers'
import path from 'path'
import fs from 'fs'
import * as crypto from 'crypto'
import 'dotenv/config'

// Initialize provider and signer
const RPC_URL = process.env.RPC_URL
const INDEXER_RPC = process.env.INDEXER_RPC

const provider = new ethers.JsonRpcProvider(RPC_URL)
const signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider)
const indexer = new Indexer(INDEXER_RPC)

async function uploadEncryptedFile(filePath) {
  // Resolve to absolute path so OpenClaw doesn't get confused by relative paths
  const absolutePath = path.resolve(filePath)

  // Validate the file exists
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`File not found at path: ${absolutePath}`)
  }

  // Generate a unique symmetric key for this specific file
  // Note: There is no server-side recovery for this key!
  const encryptionKey = crypto.randomBytes(32)

  const file = await ZgFile.fromFilePath(absolutePath)

  // Upload with built-in SDK encryption configuration
  const [tx, uploadErr] = await indexer.upload(file, RPC_URL, signer, {
    encryption: { type: 'aes256', key: encryptionKey },
  })

  if (uploadErr !== null) {
    throw new Error(`Upload error: ${uploadErr}`)
  }

  await file.close() // Clean up resources

  // Return the rootHash AND the hex-encoded key so the agent can save both
  return {
    rootHash: tx.rootHash,
    txHash: tx.txHash,
    encryptionKeyHex: encryptionKey.toString('hex') 
  }
}

async function main() {
  // Capture the file path argument from the CLI command
  const targetFilePath = process.argv[2]

  if (!targetFilePath) {
    console.error('Error: Missing file path parameter.')
    console.log('Usage: node clawback-secure.js <file-path>')
    process.exit(1)
  }

  try {
    console.log(`Locking down and uploading: ${targetFilePath}...`)
    const result = await uploadEncryptedFile(targetFilePath)
    
    console.log('ClawBack Secure Upload Completed Complete!')
    // Pretty-print the JSON output for the agent framework to read easily
    console.log(JSON.stringify(result, null, 2))
  } catch (error) {
    console.error('Secure Upload Failed:', error.message)
    process.exit(1)
  }
}

main()