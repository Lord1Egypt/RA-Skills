import { createPublicClient, http, formatUnits } from 'viem'

// ─── Citrea Mainnet Config ────────────────────────────────────────────────────
const citrea = {
  id: 4114,
  name: 'Citrea Mainnet',
  nativeCurrency: { name: 'Citrea Bitcoin', symbol: 'cBTC', decimals: 18 },
  rpcUrls: { default: { http: ['https://rpc.mainnet.citrea.xyz'] } },
}

const client = createPublicClient({
  chain: citrea,
  transport: http(),
})

// ─── RedStone Oracle Addresses ───────────────────────────────────────────────
const PRICE_FEEDS = {
  BTC:  '0xc555c100DB24dF36D406243642C169CC5A937f09',
  USDC: '0xf0DEbDAE819b354D076b0D162e399BE013A856d3',
  USDT: '0x4aF6b78d92432D32E3a635E824d3A541866f7a78',
}

const AGGREGATOR_ABI = [
  {
    name: 'latestRoundData',
    type: 'function',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: 'roundId',         type: 'uint80'  },
      { name: 'answer',          type: 'int256'  },
      { name: 'startedAt',       type: 'uint256' },
      { name: 'updatedAt',       type: 'uint256' },
      { name: 'answeredInRound', type: 'uint80'  },
    ],
  },
  {
    name: 'decimals',
    type: 'function',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint8' }],
  },
]

// ─── Token price mapping ──────────────────────────────────────────────────────
const TOKEN_PRICE_MAP = {
  wcBTC:    'BTC',
  'WBTC.e': 'BTC',
  cBTC:     'BTC',
  'USDC.e': 'USDC',
  'USDT.e': 'USDT',
  ctUSD:    'USDC',
  JUSD:     'USDC',
  GUSD:     'USDC',
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function formatUSD(amount) {
  if (amount === 0) return '$0.00'
  if (amount < 0.01) return '<$0.01'
  if (amount < 1000) return '$' + amount.toFixed(2)
  if (amount < 1000000) return '$' + (amount / 1000).toFixed(2) + 'K'
  return '$' + (amount / 1000000).toFixed(2) + 'M'
}

function tokenAmountToUSD(amount, symbol, prices) {
  if (!prices) return 0
  const feedKey = TOKEN_PRICE_MAP[symbol]
  if (!feedKey) return 0
  const price = prices[feedKey]
  if (!price) return 0
  return amount * price
}

// ─── Stale warning deduplication ─────────────────────────────────────────────
const warnedStale = new Set()

async function fetchRedStonePrices() {
  try {
    const results = await Promise.all(
      Object.entries(PRICE_FEEDS).map(async ([symbol, address]) => {
        const [roundData, decimals] = await Promise.all([
          client.readContract({
            address,
            abi: AGGREGATOR_ABI,
            functionName: 'latestRoundData',
          }),
          client.readContract({
            address,
            abi: AGGREGATOR_ABI,
            functionName: 'decimals',
          }),
        ])

        const price     = Number(roundData[1]) / 10 ** decimals
        const updatedAt = Number(roundData[3])
        const age       = Math.floor(Date.now() / 1000) - updatedAt

        if (age > 7200 && !warnedStale.has(symbol)) {
          console.warn(`⚠️  ${symbol} price is ${Math.floor(age / 60)} minutes old`)
          warnedStale.add(symbol)
        }

        return [symbol, price]
      })
    )
    return Object.fromEntries(results)
  } catch (error) {
    console.error(`⚠️  Could not fetch RedStone prices: ${error.message}`)
    return null
  }
}

export { fetchRedStonePrices, formatUSD, tokenAmountToUSD }
