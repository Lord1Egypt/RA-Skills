#!/usr/bin/env node

const ENDPOINTS = {
  AOX: 'https://api.aox.xyz/info'
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
async function fetchAOXInfo(url) {
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
  // const input = await readInput()
  try {
    const info = await fetchAOXInfo(`${ENDPOINTS.AOX}`)
    const aoTokens = info.wrappedTokens.map((token) => {
      // "wrappedTokenId": "YssglSwndbenUic3CnfYrwp3Em7i9JrJFXqOKP3JV78",
      // "name": "Ethereum-Wrapped USD Coin Test",
      // "ticker": "ethUSDC",
      // "denomination": "6",
      // "totalSupply": "65000000",
      // "minBurnAmt": "10000000",
      // "burnFee": "5000000",
      // "feeRecipient": "4S58xCqS6uKcrvqb2JlrCWllC2VIBs7qxU15QbWa3ZI",
      // "mintFee": "0",
      // "holderNum": "5",
      // "bridgeProcessId": "lp-ihMlyEo5NSoW5Rkd7kU1PoTqCIYAGfDrn2G4ihiI"
      const { ticker, burnFee, denomination, wrappedTokenId, minBurnAmt } =
        token
      const chainToken = info.chainTokens.find((i) => {
        return i.wrappedTokenId === wrappedTokenId
      })
      return {
        chainType: 'ao',
        chainId: 0,
        symbol: ticker,
        decimals: +denomination,
        name: token.name,
        stableRange: 0,
        locker: '',
        tokenId: wrappedTokenId,
        wrappedTokenId: chainToken.tokenId,
        minBurnAmt: fromDecimalToUnit(minBurnAmt, +denomination),
        burnFee: fromDecimalToUnit(burnFee, +denomination),
        logo: ''
      }
    })
    // return aoTokens.concat(info.chainTokens).concat([atest])

    const obj = {
      closeServer: info.closeServer,
      tokens: aoTokens.concat(info.chainTokens)
    }
    console.log(obj)
    return output({
      success: true,
      data: obj
    })
  } catch (err) {
    console.log(err.message)
    if (err.message) {
      return output({
        success: false,
        error: err.message
      })
    } else {
      return output({
        success: false,
        error: 'network_err'
      })
    }
  }
}

main()
