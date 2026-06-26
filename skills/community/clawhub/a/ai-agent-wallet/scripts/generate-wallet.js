#!/usr/bin/env node

const { mkdir, readFile, writeFile } = require('node:fs/promises')
const path = require('node:path')
const { generateMnemonic, generatePrivateKey, mnemonicToAccount, privateKeyToAccount } = require('viem/accounts')
const { encryptSecret } = require('./secret-crypto')

const walletDir = path.resolve(__dirname, '..', 'wallet')
const signerPath = path.join(walletDir, 'signer.json')

main().catch((error) => fail(error.message))

function parseArgs(rawArgs) {
  const parsed = {}
  for (const arg of rawArgs) {
    if (!arg.startsWith('--')) continue
    const [k, v] = arg.slice(2).split('=')
    parsed[k] = v === undefined ? 'true' : v
  }
  return parsed
}

function toBool(value) {
  return String(value).toLowerCase() === 'true'
}

function fail(message) {
  console.error(JSON.stringify({ status: 'failed', error: message }, null, 2))
  process.exit(1)
}

async function readJson(filePath) {
  try {
    const raw = await readFile(filePath, 'utf8')
    return JSON.parse(raw)
  } catch (error) {
    if (error && error.code === 'ENOENT') return null
    fail(`Unable to read JSON from ${relativePathFromRepoRoot(filePath)}: ${error.message}`)
  }
}

function relativePathFromRepoRoot(absolutePath) {
  return path.relative(path.resolve(__dirname, '..'), absolutePath)
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const method = (args.method || 'private-key').toLowerCase()

  if (!['seed-phrase', 'private-key'].includes(method)) {
    fail('Invalid --method. Use "private-key" or "seed-phrase".')
  }

  const overwrite = toBool(args.overwrite)

  await mkdir(walletDir, { recursive: true })
  const existing = await readJson(signerPath)
  if (existing && !overwrite) {
    fail('wallet/signer.json already exists. Re-run with --overwrite=true to replace it.')
  }

  let signerRecord
  if (method === 'seed-phrase') {
    const mnemonic = generateMnemonic()
    const account = mnemonicToAccount(mnemonic)
    signerRecord = {
      method: 'seed_phrase',
      address: account.address,
      encryptedSeedPhrase: encryptSecret(mnemonic),
      encryptedPrivateKey: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
  } else {
    const privateKey = generatePrivateKey()
    const account = privateKeyToAccount(privateKey)
    signerRecord = {
      method: 'private_key',
      address: account.address,
      encryptedSeedPhrase: null,
      encryptedPrivateKey: encryptSecret(privateKey),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
  }

  await writeFile(signerPath, JSON.stringify(signerRecord, null, 2))

  console.log(
    JSON.stringify(
      {
        action: 'generate',
        method: signerRecord.method,
        address: signerRecord.address,
        status: 'success',
        walletFile: relativePathFromRepoRoot(signerPath),
        next_step: 'Run get-balance or fund the wallet before sending.',
      },
      null,
      2
    )
  )
}
