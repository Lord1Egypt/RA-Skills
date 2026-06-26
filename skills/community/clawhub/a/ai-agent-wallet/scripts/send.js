#!/usr/bin/env node

const { readFile } = require('node:fs/promises')
const path = require('node:path')
const {
  createPublicClient,
  createWalletClient,
  defineChain,
  formatEther,
  formatUnits,
  http,
  isAddress,
  parseEther,
  parseUnits,
} = require('viem')
const { mnemonicToAccount, privateKeyToAccount } = require('viem/accounts')
const { decryptSecret } = require('./secret-crypto')

const walletDir = path.resolve(__dirname, '..', 'wallet')
const configPath = path.join(walletDir, 'config.json')
const signerPath = path.join(walletDir, 'signer.json')
const erc20Abi = [
  {
    type: 'function',
    name: 'transfer',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
    ],
    outputs: [{ name: '', type: 'bool' }],
  },
  {
    type: 'function',
    name: 'balanceOf',
    stateMutability: 'view',
    inputs: [{ name: 'owner', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'decimals',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint8' }],
  },
  {
    type: 'function',
    name: 'symbol',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'string' }],
  },
]

main().catch((error) => fail(error.message))

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const to = args.to
  const amount = args.amount
  const tokenAddress = args.tokenAddress
  const confirm = toBool(args.confirm)

  if (!to || !isAddress(to)) {
    fail('Provide a valid --to recipient address.')
  }
  if (!amount || Number(amount) <= 0) {
    fail('Provide a positive --amount value.')
  }
  if (tokenAddress && !isAddress(tokenAddress)) {
    fail('Invalid --tokenAddress.')
  }
  if (!confirm) {
    fail('Broadcast requires explicit --confirm=true.')
  }

  const currentNetwork = await readCurrentNetwork()
  const requiresMainnetDoubleConfirmation = isMainnetChainId(currentNetwork.chain_id)
  if (requiresMainnetDoubleConfirmation && !toBool(args.confirmMainnet)) {
    fail(
      'Mainnet broadcast requires double confirmation. Re-run with --confirm=true --confirmMainnet=true.'
    )
  }

  const account = await readSignerAccount()
  const chain = buildChain(currentNetwork)

  const publicClient = createPublicClient({
    chain,
    transport: http(currentNetwork.rpc_url),
  })
  const walletClient = createWalletClient({
    account,
    chain,
    transport: http(currentNetwork.rpc_url),
  })

  if (!tokenAddress) {
    const value = parseNativeAmount(amount)
    const balance = await publicClient.getBalance({ address: account.address })
    if (balance < value) {
      fail(
        `Insufficient native funds. Balance ${formatEther(balance)} is lower than transfer amount ${amount}.`
      )
    }

    const txHash = await walletClient.sendTransaction({
      account,
      to,
      value,
    })

    console.log(
      JSON.stringify(
        {
          action: 'send',
          mode: 'native',
          chain: currentNetwork.chain_id,
          address: account.address,
          to,
          amount,
          txHash,
          status: 'success',
          next_step: 'Track transaction confirmation using the tx hash.',
        },
        null,
        2
      )
    )
    return
  }

  const tokenMeta = await resolveTokenMeta(publicClient, tokenAddress, args)
  let tokenAmount
  try {
    tokenAmount = parseUnits(String(amount), tokenMeta.decimals)
  } catch (error) {
    fail(`Invalid token amount for decimals=${tokenMeta.decimals}: ${error.message}`)
  }

  if (tokenAmount <= 0n) {
    fail('Token amount must be greater than zero.')
  }

  const tokenBalance = await publicClient.readContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: [account.address],
  })

  if (tokenBalance < tokenAmount) {
    const balanceLabel = formatUnits(tokenBalance, tokenMeta.decimals)
    const symbolLabel = tokenMeta.symbol ? ` ${tokenMeta.symbol}` : ''
    fail(
      `Insufficient token funds. Balance ${balanceLabel}${symbolLabel} is lower than transfer amount ${amount}${symbolLabel}.`
    )
  }

  const txHash = await walletClient.writeContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: 'transfer',
    args: [to, tokenAmount],
    account,
  })

  console.log(
    JSON.stringify(
      {
        action: 'send',
        mode: 'token',
        chain: currentNetwork.chain_id,
        address: account.address,
        to,
        amount,
        decimals: tokenMeta.decimals,
        symbol: tokenMeta.symbol,
        tokenAddress,
        txHash,
        status: 'success',
        next_step: 'Track transaction confirmation using the tx hash.',
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

function parseNativeAmount(amount) {
  try {
    return parseEther(String(amount))
  } catch (error) {
    fail(`Invalid native amount: ${error.message}`)
  }
}

async function resolveTokenMeta(publicClient, tokenAddress, args) {
  let decimals = Number(args.decimals ?? NaN)
  let symbol = args.symbol ?? null

  if (!Number.isInteger(decimals) || decimals < 0) {
    try {
      const onchainDecimals = await publicClient.readContract({
        address: tokenAddress,
        abi: erc20Abi,
        functionName: 'decimals',
      })
      decimals = Number(onchainDecimals)
    } catch (_error) {
      decimals = 18
    }
  }

  if (args.symbol === undefined) {
    try {
      symbol = await publicClient.readContract({
        address: tokenAddress,
        abi: erc20Abi,
        functionName: 'symbol',
      })
    } catch (_error) {
      symbol = null
    }
  }

  return { decimals, symbol }
}

function isMainnetChainId(chainId) {
  const id = Number(chainId)
  if (!Number.isFinite(id)) return false

  // Common production chains where an extra explicit confirmation is required.
  const mainnetChainIds = new Set([1, 10, 56, 137, 250, 324, 8453, 42161, 43114])
  return mainnetChainIds.has(id)
}

async function readCurrentNetwork() {
  const raw = await readFile(configPath, 'utf8').catch((error) => {
    if (error && error.code === 'ENOENT') {
      fail('wallet/config.json is missing. Configure default network first.')
    }
    fail(`Unable to read wallet/config.json: ${error.message}`)
  })

  let list
  try {
    list = JSON.parse(raw)
  } catch (error) {
    fail(`wallet/config.json is invalid JSON: ${error.message}`)
  }

  if (!Array.isArray(list)) {
    fail('wallet/config.json must be an array of network objects.')
  }

  const currentEntries = list.filter((entry) => entry && entry.current === true)
  if (currentEntries.length !== 1) {
    fail('wallet/config.json must contain exactly one network with current=true.')
  }

  const current = currentEntries[0]
  if (!current.rpc_url || !current.chain_id) {
    fail('Current network must include rpc_url and chain_id.')
  }
  return current
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

function buildChain(currentNetwork) {
  const id = Number(currentNetwork.chain_id)
  if (!Number.isFinite(id) || id <= 0) {
    fail(`Invalid chain_id: ${currentNetwork.chain_id}`)
  }

  return defineChain({
    id,
    name: `chain-${currentNetwork.chain_id}`,
    network: `chain-${currentNetwork.chain_id}`,
    nativeCurrency: {
      name: 'Native Token',
      symbol: 'NATIVE',
      decimals: 18,
    },
    rpcUrls: {
      default: {
        http: [currentNetwork.rpc_url],
      },
      public: {
        http: [currentNetwork.rpc_url],
      },
    },
  })
}

function fail(message) {
  console.error(JSON.stringify({ status: 'failed', error: message }, null, 2))
  process.exit(1)
}
