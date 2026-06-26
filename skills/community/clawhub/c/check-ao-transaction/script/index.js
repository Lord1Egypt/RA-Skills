#!/usr/bin/env node

const ENDPOINTS = {
  AOX: 'https://api.aox.xyz/tx/'
}

async function readInput() {
  return new Promise((resolve) => {
    let data = ''

    process.stdin.on('data', (chunk) => {
      data += chunk
    })

    process.stdin.on('end', () => {
      try {
        resolve(JSON.parse(data || '{}'))
      } catch {
        resolve({})
      }
    })
  })
}

async function fetchTx(url) {
  const res = await fetch(url)

  if (!res.ok) {
    throw new Error('not_found')
  }

  return res.json()
}

function output(data) {
  process.stdout.write(JSON.stringify(data))
}

export const fromDecimalToUnit = (x, decimals) => {
  const value = typeof x === 'bigint' ? x : BigInt(String(x))

  const negative = value < 0n
  const absValue = negative ? -value : value
  const base = 10n ** BigInt(decimals)

  const integerPart = absValue / base
  const fractionalPart = absValue % base

  const fraction = fractionalPart
    .toString()
    .padStart(decimals, '0')
    .replace(/0+$/, '')

  const result = fraction
    ? `${integerPart.toString()}.${fraction}`
    : integerPart.toString()

  return negative ? `-${result}` : result
}

async function main() {
  const input = await readInput()

  const txid = input.txid || input.txId || input.txHash || input.tx_hash

  if (!txid) {
    return output({
      success: false,
      error: 'txid_required'
    })
  }

  try {
    // Hymatrix
    const hymxData = await fetchTx(`${ENDPOINTS.AOX}${txid}`)
    hymxData.quantity = fromDecimalToUnit(hymxData.quantity, hymxData.decimals)
    hymxData.fee = fromDecimalToUnit(hymxData.fee, hymxData.decimals)
    return output({
      success: true,
      data: hymxData
    })
  } catch {
    return output({
      success: false,
      error: 'transaction_not_found'
    })
  }
}

main()
