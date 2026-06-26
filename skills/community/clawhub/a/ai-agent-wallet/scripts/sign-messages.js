#!/usr/bin/env node

const { readFile } = require('node:fs/promises')
const path = require('node:path')
const { mnemonicToAccount, privateKeyToAccount } = require('viem/accounts')
const { decryptSecret } = require('./secret-crypto')

const walletDir = path.resolve(__dirname, '..', 'wallet')
const signerPath = path.join(walletDir, 'signer.json')

main().catch((error) => fail(error.message))

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const message = normalizeMessage(args.message)
  if (!message) {
    fail('Provide a non-empty --message value.')
  }

  const account = await readSignerAccount()
  const signature = await account.signMessage({ message })

  console.log(
    JSON.stringify(
      {
        action: 'sign',
        chain: 'none',
        address: account.address,
        message,
        signature,
        status: 'success',
        txHash: null,
        next_step: 'Verify signature with your target app or contract.',
      },
      null,
      2
    )
  )
}

function parseArgs(rawArgs) {
  const parsed = {}
  for (const arg of rawArgs) {
    if (!arg.startsWith('--')) continue
    const [k, ...rest] = arg.slice(2).split('=')
    parsed[k] = rest.length ? rest.join('=') : 'true'
  }
  return parsed
}

function normalizeMessage(value) {
  if (value === undefined || value === null) return null
  const trimmed = String(value).trim()
  return trimmed || null
}

async function readSignerAccount() {
  const raw = await readFile(signerPath, 'utf8').catch((error) => {
    if (error && error.code === 'ENOENT') {
      fail('wallet/signer.json is missing. Generate or import wallet first.')
    }
    fail(`Unable to read wallet/signer.json: ${error.message}`)
  })

  let signer
  try {
    signer = JSON.parse(raw)
  } catch (error) {
    fail(`wallet/signer.json is invalid JSON: ${error.message}`)
  }

  if (signer.method === 'seed_phrase') {
    if (!signer.encryptedSeedPhrase) {
      fail('wallet/signer.json seed_phrase entry is missing encryptedSeedPhrase.')
    }
    const seedPhrase = decryptSecret(String(signer.encryptedSeedPhrase))
    return mnemonicToAccount(seedPhrase)
  }

  if (signer.method === 'private_key') {
    if (!signer.encryptedPrivateKey) {
      fail('wallet/signer.json private_key entry is missing encryptedPrivateKey.')
    }
    const privateKey = decryptSecret(String(signer.encryptedPrivateKey))
    const normalized = privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`
    return privateKeyToAccount(normalized)
  }

  fail('wallet/signer.json method must be "seed_phrase" or "private_key".')
}

function fail(message) {
  console.error(JSON.stringify({ status: 'failed', error: message }, null, 2))
  process.exit(1)
}
