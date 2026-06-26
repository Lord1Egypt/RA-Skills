#!/usr/bin/env node

const { mkdir, readFile, writeFile } = require('node:fs/promises')
const path = require('node:path')
const { mnemonicToAccount, privateKeyToAccount } = require('viem/accounts')
const { encryptSecret } = require('./secret-crypto')

const walletDir = path.resolve(__dirname, '..', 'wallet')
const signerPath = path.join(walletDir, 'signer.json')

main().catch((error) => fail(error.message))

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const overwrite = toBool(args.overwrite)
  const seedPhrase = normalizeSeedPhrase(args.seedPhrase)
  const privateKey = normalizePrivateKey(args.privateKey)

  if (!seedPhrase && !privateKey) {
    fail('Provide --seedPhrase="<12/24 words>" or --privateKey=0x...')
  }
  if (seedPhrase && privateKey) {
    fail('Provide only one secret source: seed phrase or private key.')
  }

  await mkdir(walletDir, { recursive: true })
  const existing = await readJson(signerPath)
  if (existing && !overwrite) {
    fail('wallet/signer.json already exists. Re-run with --overwrite=true to replace it.')
  }

  let signerRecord
  if (seedPhrase) {
    const wordCount = seedPhrase.split(' ').length
    if (![12, 24].includes(wordCount)) {
      fail('Seed phrase must contain 12 or 24 words.')
    }
    const account = mnemonicToAccount(seedPhrase)
    signerRecord = {
      method: 'seed_phrase',
      address: account.address,
      encryptedSeedPhrase: encryptSecret(seedPhrase),
      encryptedPrivateKey: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
  } else {
    if (!isValidPrivateKey(privateKey)) {
      fail('Invalid private key. Expected 32-byte hex (64 chars after 0x).')
    }
    const normalizedPrivateKey = privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`
    const account = privateKeyToAccount(normalizedPrivateKey)
    signerRecord = {
      method: 'private_key',
      address: account.address,
      encryptedSeedPhrase: null,
      encryptedPrivateKey: encryptSecret(normalizedPrivateKey),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
  }

  await writeFile(signerPath, JSON.stringify(signerRecord, null, 2))
  console.log(
    JSON.stringify(
      {
        action: 'import',
        method: signerRecord.method,
        address: signerRecord.address,
        status: 'success',
        walletFile: relativePathFromRepoRoot(signerPath),
        next_step: 'Run get-balance to verify wallet connectivity.',
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

function toBool(value) {
  return String(value).toLowerCase() === 'true'
}

function normalizeSeedPhrase(value) {
  if (!value) return null
  return String(value).trim().replace(/\s+/g, ' ')
}

function normalizePrivateKey(value) {
  if (!value) return null
  return String(value).trim().replace(/^['"]|['"]$/g, '')
}

function isValidPrivateKey(value) {
  if (!value) return false
  const normalized = value.startsWith('0x') ? value.slice(2) : value
  return /^[0-9a-fA-F]{64}$/.test(normalized)
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

function fail(message) {
  console.error(JSON.stringify({ status: 'failed', error: message }, null, 2))
  process.exit(1)
}
