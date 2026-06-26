#!/usr/bin/env node

const { readFile } = require('node:fs/promises')
const path = require('node:path')
const { createPublicClient, formatEther, formatUnits, http, isAddress } = require('viem')

const walletDir = path.resolve(__dirname, '..', 'wallet')
const configPath = path.join(walletDir, 'config.json')

const erc20Abi = [
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
  const address = args.address
  if (!address || !isAddress(address)) {
    fail('Provide a valid --address.')
  }

  const tokenAddress = args.tokenAddress
  if (tokenAddress && !isAddress(tokenAddress)) {
    fail('Invalid --tokenAddress.')
  }

  const currentNetwork = await readCurrentNetwork()
  const publicClient = createPublicClient({
    transport: http(currentNetwork.rpc_url),
  })

  if (!tokenAddress) {
    const wei = await publicClient.getBalance({ address })
    console.log(
      JSON.stringify(
        {
          action: 'balance',
          mode: 'native',
          chain: currentNetwork.chain_id,
          address,
          raw: wei.toString(),
          formatted: formatEther(wei),
          status: 'success',
          next_step: 'Use send script to transfer funds if needed.',
        },
        null,
        2
      )
    )
    return
  }

  const raw = await publicClient.readContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: [address],
  })

  let decimals = Number(args.decimals ?? 18)
  let symbol = args.symbol ?? null

  if (args.decimals === undefined) {
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

  console.log(
    JSON.stringify(
      {
        action: 'balance',
        mode: 'token',
        chain: currentNetwork.chain_id,
        address,
        tokenAddress,
        decimals,
        symbol,
        raw: raw.toString(),
        formatted: formatUnits(raw, decimals),
        status: 'success',
        next_step: 'Verify token contract and decimals before sending.',
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

function fail(message) {
  console.error(JSON.stringify({ status: 'failed', error: message }, null, 2))
  process.exit(1)
}
