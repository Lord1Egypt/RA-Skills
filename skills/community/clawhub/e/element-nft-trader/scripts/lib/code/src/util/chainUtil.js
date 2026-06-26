"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getChain = getChain;
exports.getChainMId = getChainMId;
exports.getChainId = getChainId;
const types_1 = require("../types/types");
const CHAIN_NAMES = {
    1: types_1.Network.ETH,
    11155111: types_1.Network.ETH,
    56: types_1.Network.BSC,
    97: types_1.Network.BSC,
    137: types_1.Network.Polygon,
    43114: types_1.Network.Avalanche,
    42161: types_1.Network.Arbitrum,
    324: types_1.Network.ZkSync,
    59144: types_1.Network.Linea,
    8453: types_1.Network.Base,
    204: types_1.Network.OpBNB,
    534352: types_1.Network.Scroll,
    169: types_1.Network.MantaPacific,
    10: types_1.Network.Optimism,
    5000: types_1.Network.Mantle,
    42766: types_1.Network.ZKFair,
    81457: types_1.Network.Blast,
    4200: types_1.Network.Merlin,
    34443: types_1.Network.Mode,
    7560: types_1.Network.Cyber,
    60808: types_1.Network.BOB,
    1890: types_1.Network.Lightlink,
    2748: types_1.Network.Nanon,
    80094: types_1.Network.Bera,
    7000: types_1.Network.Zeta,
    6900: types_1.Network.Nibiru,
    2741: types_1.Network.Abstract,
    143: types_1.Network.Monad,
    200901: types_1.Network.Bitlayer,
    5888: types_1.Network.Mantra,
};
// Element 平台全局唯一 ChainMId 映射 (chainId -> chainMId)
const CHAIN_MID_MAP = {
    1: 1, // Ethereum Mainnet
    137: 101, // Polygon Mainnet
    56: 201, // BSC Mainnet
    43114: 401, // Avalanche Mainnet
    42161: 601, // Arbitrum Mainnet
    324: 701, // zkSync Era Mainnet
    204: 1101, // opBNB Mainnet
    8453: 1201, // Base Mainnet
    534352: 1301, // Scroll Mainnet
    169: 1401, // Manta Pacific
    10: 1501, // Optimism Mainnet
    5000: 1601, // Mantle Mainnet
    42766: 1701, // ZKFair Mainnet
    81457: 1801, // Blast Mainnet
    4200: 1901, // Merlin Mainnet
    34443: 2001, // Mode Mainnet
    7560: 2101, // Cyber Mainnet
    60808: 2201, // BOB Mainnet
    1890: 2301, // Lightlink Mainnet
    2748: 2501, // Nanon Mainnet
    80094: 2601, // BeraChain Mainnet
    7000: 2701, // ZetaChain Mainnet
    6900: 2801, // Nibiru Mainnet
    2741: 2901, // Abstract Mainnet
    143: 3001, // Monad Mainnet
    200901: 3101, // Bitlayer Mainnet
    5888: 3201, // Mantra Mainnet
};
function getChain(chainId) {
    if (CHAIN_NAMES[chainId]) {
        return CHAIN_NAMES[chainId];
    }
    throw Error('getChain, unsupported chainId : ' + chainId);
}
/**
 * 根据 chainId 获取 Element 平台的 chainMId
 * @param chainId 区块链原生 chainId
 * @returns Element 平台全局唯一 chainMId
 */
function getChainMId(chainId) {
    if (CHAIN_MID_MAP[chainId]) {
        return CHAIN_MID_MAP[chainId];
    }
    throw Error('getChainMId, unsupported chainId : ' + chainId);
}
function getChainId(chain, isTestnet = false) {
    if (isTestnet) {
        switch (chain.toString()) {
            case types_1.Network.ETH:
                return 11155111;
            case types_1.Network.BSC:
                return 97;
        }
        throw Error('getChainId, unsupported chain : ' + chain);
    }
    else {
        switch (chain.toString()) {
            case types_1.Network.ETH:
                return 1;
            case types_1.Network.BSC:
                return 56;
            case types_1.Network.Polygon:
                return 137;
            case types_1.Network.Avalanche:
                return 43114;
            case types_1.Network.Arbitrum:
                return 42161;
            case types_1.Network.ZkSync:
                return 324;
            case types_1.Network.Linea:
                return 59144;
            case types_1.Network.Base:
                return 8453;
            case types_1.Network.OpBNB:
                return 204;
            case types_1.Network.Scroll:
                return 534352;
            case types_1.Network.MantaPacific:
                return 169;
            case types_1.Network.Optimism:
                return 10;
            case types_1.Network.Mantle:
                return 5000;
            case types_1.Network.ZKFair:
                return 42766;
            case types_1.Network.Blast:
                return 81457;
            case types_1.Network.Merlin:
                return 4200;
            case types_1.Network.Mode:
                return 34443;
            case types_1.Network.Cyber:
                return 7560;
            case types_1.Network.BOB:
                return 60808;
            case types_1.Network.Lightlink:
                return 1890;
            case types_1.Network.Nanon:
                return 2748;
            case types_1.Network.Bera:
                return 80094;
            case types_1.Network.Zeta:
                return 7000;
            case types_1.Network.Nibiru:
                return 6900;
            case types_1.Network.Abstract:
                return 2741;
            case types_1.Network.Monad:
                return 143;
            case types_1.Network.Bitlayer:
                return 200901;
            case types_1.Network.Mantra:
                return 5888;
        }
        throw Error('getChainId, unsupported chain : ' + chain);
    }
}
//# sourceMappingURL=chainUtil.js.map