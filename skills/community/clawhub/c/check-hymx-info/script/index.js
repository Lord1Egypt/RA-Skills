#!/usr/bin/env node

const ENDPOINTS = {
  AOX: 'https://api-bridgescan-dev.hymatrix.com/info'
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

export const getHymxCacheTokenInfo = async (nodeUrl, pid, key) => {
  const url = `${nodeUrl}/cache/${pid}/${key}`
  const result = fetchAOXInfo(url)
  return result
}

async function main() {
  try {
    const hymatrixBridgeInfo = await fetchAOXInfo(`${ENDPOINTS.AOX}`)
    const cachesTokenInfo = await Promise.all(
      hymatrixBridgeInfo.tokenInfo.map(async (item) => {
        const tokenInfo = await getHymxCacheTokenInfo(
          hymatrixBridgeInfo.bridgeNodeUrl,
          item.wrappedTokenId,
          'info'
        )
        try {
          const info = JSON.parse(tokenInfo)
          return {
            ...info,
            locker: item.locker,
            tokenId: item.wrappedTokenId,
            wrappedTokenId: item.tokenId
          }
        } catch {
          return null // 这里返回 null 不能直接进 Object.fromEntries
        }
      })
    )
    const hymxBridgeTokenList = cachesTokenInfo.filter(Boolean).map((item) => {
      const burnFee = JSON.parse(item.BurnFees)
      const burnFees = Object.fromEntries(
        Object.entries(burnFee).map(([k, v]) => {
          const kToken = hymatrixBridgeInfo.tokenInfo
            .filter(Boolean)
            .find((i) => i.chainType === k && i.symbol === item.Ticker)
          return [k, fromDecimalToUnit(v, kToken.decimals)]
        })
      )
      const sourceLockAmount = JSON.parse(item.SourceLockAmounts)
      const sourceLockAmounts = Object.fromEntries(
        Object.entries(sourceLockAmount).map(([k, v]) => {
          const kToken = hymatrixBridgeInfo.tokenInfo
            .filter(Boolean)
            .find((i) =>
              (i.chainType === k.split(':')[0]) === 'aostest'
                ? ['aostest', k.split(':')[1]].join(':')
                : k && i.symbol === item.Ticker
            )
          return [
            k.split(':')[0] === 'aostest'
              ? ['aostest', k.split(':')[1]].join(':')
              : k,
            fromDecimalToUnit(v, kToken.decimals)
          ]
        })
      )
      return {
        chainType: 'hymatrix',
        chainId: 0,
        symbol: item.Ticker,
        decimals: item.Decimals,
        name: item.Name,
        locker: item.locker,
        tokenId: item.tokenId,
        wrappedTokenId: item.wrappedTokenId,
        logo: '',
        stableRange: 0,
        cuUrl: hymatrixBridgeInfo.bridgeNodeUrl,
        maxBurnAmts: sourceLockAmounts,
        feeRecipient: item.FeeRecipient,
        burnFees: burnFees
      }
    })
    const hymxChainToken = hymatrixBridgeInfo.tokenInfo.map((item) => {
      const bridgeToken = {
        chainType: item.chainType,
        chainId: item.chainId,
        symbol: item.symbol,
        decimals: item.decimals,
        name: item.symbol,
        locker: item.locker,
        tokenId: item.tokenId,
        wrappedTokenId: item.wrappedTokenId,
        logo: '',
        stableRange: 0,
        maxBurnAmts: {},
        feeRecipient: '',
        burnFees: {}
      }
      return bridgeToken
    })
    const hmTokens2 = hymxBridgeTokenList
    const totalTokens = hymxChainToken
      .concat(hmTokens2)
      .map((item, index, arr) => {
        const wrappedTokenIds = arr
          .filter((t) => t.tokenId === item.tokenId)
          .map((t) => t.wrappedTokenId)
          .filter(Boolean)
        return {
          ...item,
          wrappedTokenIds: [...new Set(wrappedTokenIds)]
        }
      })
    hymatrixBridgeInfo.tokens = totalTokens
    return output({
      success: true,
      data: totalTokens
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
