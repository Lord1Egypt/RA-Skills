import { Network } from '../types/types'

const CHAIN_NAMES: { [key: number]: string } = {
  1: Network.ETH,
  11155111: Network.ETH,
  56: Network.BSC,
  97: Network.BSC,
  137: Network.Polygon,
  43114: Network.Avalanche,
  42161: Network.Arbitrum,
  324: Network.ZkSync,
  59144: Network.Linea,
  8453: Network.Base,
  204: Network.OpBNB,
  534352: Network.Scroll,
  169: Network.MantaPacific,
  10: Network.Optimism,
  5000: Network.Mantle,
  42766: Network.ZKFair,
  81457: Network.Blast,
  4200: Network.Merlin,
  34443: Network.Mode,
  7560: Network.Cyber,
  60808: Network.BOB,
  1890: Network.Lightlink,
  2748: Network.Nanon,
  80094: Network.Bera,
  7000: Network.Zeta,
  6900: Network.Nibiru,
  2741: Network.Abstract,
  143: Network.Monad,
  200901: Network.Bitlayer,
  5888: Network.Mantra,
}

// Element 平台全局唯一 ChainMId 映射 (chainId -> chainMId)
const CHAIN_MID_MAP: { [key: number]: number } = {
  1: 1,           // Ethereum Mainnet
  137: 101,       // Polygon Mainnet
  56: 201,        // BSC Mainnet
  43114: 401,     // Avalanche Mainnet
  42161: 601,     // Arbitrum Mainnet
  324: 701,       // zkSync Era Mainnet
  204: 1101,      // opBNB Mainnet
  8453: 1201,     // Base Mainnet
  534352: 1301,   // Scroll Mainnet
  169: 1401,      // Manta Pacific
  10: 1501,       // Optimism Mainnet
  5000: 1601,     // Mantle Mainnet
  42766: 1701,    // ZKFair Mainnet
  81457: 1801,    // Blast Mainnet
  4200: 1901,     // Merlin Mainnet
  34443: 2001,    // Mode Mainnet
  7560: 2101,     // Cyber Mainnet
  60808: 2201,    // BOB Mainnet
  1890: 2301,     // Lightlink Mainnet
  2748: 2501,     // Nanon Mainnet
  80094: 2601,    // BeraChain Mainnet
  7000: 2701,     // ZetaChain Mainnet
  6900: 2801,     // Nibiru Mainnet
  2741: 2901,     // Abstract Mainnet
  143: 3001,      // Monad Mainnet
  200901: 3101,   // Bitlayer Mainnet
  5888: 3201,     // Mantra Mainnet
}

export function getChain(chainId: number): string {
  if (CHAIN_NAMES[chainId]) {
    return CHAIN_NAMES[chainId]
  }
  throw Error('getChain, unsupported chainId : ' + chainId)
}

/**
 * 根据 chainId 获取 Element 平台的 chainMId
 * @param chainId 区块链原生 chainId
 * @returns Element 平台全局唯一 chainMId
 */
export function getChainMId(chainId: number): number {
  if (CHAIN_MID_MAP[chainId]) {
    return CHAIN_MID_MAP[chainId]
  }
  throw Error('getChainMId, unsupported chainId : ' + chainId)
}

export function getChainId(chain: any, isTestnet = false): number {
  if (isTestnet) {
    switch (chain.toString()) {
      case Network.ETH:
        return 11155111

      case Network.BSC:
        return 97
    }
    throw Error('getChainId, unsupported chain : ' + chain)
  } else {
    switch (chain.toString()) {
      case Network.ETH:
        return 1

      case Network.BSC:
        return 56

      case Network.Polygon:
        return 137

      case Network.Avalanche:
        return 43114

      case Network.Arbitrum:
        return 42161

      case Network.ZkSync:
        return 324

      case Network.Linea:
        return 59144

      case Network.Base:
        return 8453

      case Network.OpBNB:
        return 204

      case Network.Scroll:
        return 534352

      case Network.MantaPacific:
        return 169

      case Network.Optimism:
        return 10

      case Network.Mantle:
        return 5000

      case Network.ZKFair:
        return 42766

      case Network.Blast:
        return 81457

      case Network.Merlin:
        return 4200

      case Network.Mode:
        return 34443

      case Network.Cyber:
        return 7560

      case Network.BOB:
        return 60808

      case Network.Lightlink:
        return 1890

      case Network.Nanon:
        return 2748

      case Network.Bera:
        return 80094

      case Network.Zeta:
        return 7000

      case Network.Nibiru:
        return 6900

      case Network.Abstract:
        return 2741

      case Network.Monad:
        return 143

      case Network.Bitlayer:
        return 200901

      case Network.Mantra:
        return 5888
    }
    throw Error('getChainId, unsupported chain : ' + chain)
  }
}
