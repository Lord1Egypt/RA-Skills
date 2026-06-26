#!/usr/bin/env node

const ENDPOINTS = {
  HYMX: 'https://api-bridgescan-dev.hymatrix.com/bridgeTx/'
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
    const hymxData = await fetchTx(`${ENDPOINTS.HYMX}${txid}`)

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
