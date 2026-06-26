"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RPC_CONF_API_URL = exports.CONTRACTS_ADDRESSES = exports.ContractABI = void 0;
exports.fetchRpcConfigs = fetchRpcConfigs;
exports.getCachedRpcConfigs = getCachedRpcConfigs;
exports.getRpcUrlFromRemote = getRpcUrlFromRemote;
var index_1 = require("./abi/index");
Object.defineProperty(exports, "ContractABI", { enumerable: true, get: function () { return index_1.ContractABI; } });
exports.CONTRACTS_ADDRESSES = {
    1: {
        ElementEx: '0x20F780A973856B93f63670377900C1d2a50a77c4',
        ElementExSwapV2: '0xb4E7B8946fA2b35912Cc0581772cCCd69A33000c',
        Helper: '0x68dc8D3ab93220e84b9923706B3DDc926C77f1Df',
        WToken: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    },
    11155111: {
        ElementEx: '0x5df0d6a56523d49650a2526873c2c055201aa879',
        ElementExSwapV2: '0xfb099ce799d8ea457cd7a4401d621c00d87c87fa',
        Helper: '0x7a758546926f19b2dcffd114a36b3c8e04be7475',
        WToken: '0x097d90c9d3e0b50ca60e1ae45f6a81010f9fb534'
    },
    56: {
        ElementEx: '0xb3e3DfCb2d9f3DdE16d78B9e6EB3538Eb32B5ae1',
        ElementExSwapV2: '0x46A03313FA8eF8ac8798f502bB38d35E5e1acbfC',
        Helper: '0xb54ee46dACE4ecAC1dBC2488B61094B4b3174139',
        WToken: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
    },
    97: {
        ElementEx: '0x30FAD3918084eba4379FD01e441A3Bb9902f0843',
        ElementExSwapV2: '0x8751796ba398412A1520fa177E421183C49a8780',
        Helper: '0x61311202273f9857685852FC76aEA83294F90a80',
        WToken: '0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd'
    },
    137: {
        ElementEx: '0xEAF5453b329Eb38Be159a872a6ce91c9A8fb0260',
        ElementExSwapV2: '0x25956Fd0A5FE281D921b1bB3499fc8D5EFea6201',
        Helper: '0x4D5E03AF11d7976a0494f0ff2F65986d6548fc3e',
        WToken: '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
    },
    80001: {
        ElementEx: '0x2431e7671d1557d991a138c7af5d4cd223a605d6',
        ElementExSwapV2: '0xA9fF4783fA66bc2774f2c41489BA570EbE82E141',
        Helper: '0xcCcd0afEAfB6625cd655Cf8f39B02c85947dB6f6',
        WToken: '0x9c3C9283D3e44854697Cd22D3Faa240Cfb032889'
    },
    43114: {
        ElementEx: '0x18cd9270DbdcA86d470cfB3be1B156241fFfA9De',
        ElementExSwapV2: '0x917ef4F231Cbd0972A10eC3453F40762C488e6fa',
        Helper: '0x4c95419b74D420841CaaAd6345799522475f91D2',
        WToken: '0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7'
    },
    43113: {
        ElementEx: '0xd089757a20a36B0978156659Cc1063B929Da76aB',
        ElementExSwapV2: '0x786596CFaA0020EC7fFdE499049E3b9981E99f4A',
        Helper: '0x1f66918D87aab33158DBA4b5Dfe73f2245cfDc20',
        WToken: '0xd00ae08403B9bbb9124bB305C09058E32C39A48c'
    },
    42161: {
        ElementEx: '0x18cd9270dbdca86d470cfb3be1b156241fffa9de',
        ElementExSwapV2: '0x1e0E556b7f310c320bA22b5dEC0A0755C1c9854b',
        Helper: '0xb4E7B8946fA2b35912Cc0581772cCCd69A33000c',
        WToken: '0x82af49447d8a07e3bd95bd0d56f35241523fbab1'
    },
    421613: {
        ElementEx: '0x6938d12679ba4e646934a6900bd4077c3cc09a04',
        ElementExSwapV2: '0xf6bD4a8dfe1FB577C311Bd361CB1b0e7DD3b83ab',
        Helper: '0xccf79726adA5333B41793994fAe78a28F0c6278A',
        WToken: '0x204a6679557ec1adfb3752c88891aa885adb53f1'
    },
    324: {
        ElementEx: '0x64848eefbc2921102a153b08fa64536ae1f8e937',
        ElementExSwapV2: '0x7868a55b638ed298370c16f83fa32b26664726ab',
        Helper: '0x4ff83aa3a2a993270c7921ce6f22892213c3c446',
        WToken: '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
    },
    280: {
        ElementEx: '0x0ec4d499f46a154e7faf52c1695b2da8a41900d4',
        ElementExSwapV2: '0x448798ccc3a9d15ce5d4369c928c86b4085c106d',
        Helper: '0xbc91448f965c684238686532f17492d207f0a9b7',
        WToken: '0xf8dcf9b36817151d36ff2e35d9f43094dde4c737'
    },
    59144: {
        ElementEx: '0x0caB6977a9c70E04458b740476B498B214019641',
        ElementExSwapV2: '0x42c759a719c228050901299b88fd316c3a050617',
        Helper: '0x701a4A5238AF84a9c4ed8a23DeE670069b44eEb7',
        WToken: '0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f'
    },
    59140: {
        ElementEx: '0xc23cf8BC7cD2f2Dcb2e151E81b8a1F9EA7c017B6',
        ElementExSwapV2: '0x4B2C3677432a918F197B9c546d0844f53d374eB0',
        Helper: '0x9A6324eBF46288FD872c08BA7C6e51fbb62dC259',
        WToken: '0x2C1b868d6596a18e32E61B901E4060C872647b6C'
    },
    8453: {
        ElementEx: '0xa39A5f160a1952dDf38781Bd76E402B0006912A9',
        ElementExSwapV2: '0x66950320086664429C69735318724Ae24ec0D835',
        Helper: '0x217efe077801387d125fE98E1b61CDDA4D1364d2',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    84531: {
        ElementEx: '0x8237A37FC696D944d4Cdb089A89443B55Cb5e7F9',
        ElementExSwapV2: '0xcCcd0afEAfB6625cd655Cf8f39B02c85947dB6f6',
        Helper: '0x89A34a7EDC273555bB11ba4484ec417B05df3a15',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    204: {
        ElementEx: '0x5417c5215F239B8D04f9D9c04bF43034B35AD4BD',
        ElementExSwapV2: '0x8629E04a83902721FBD816fE9d41FD2053DAC79b',
        Helper: '0x3c19784F5247ca471E27eA1C604b48D266eb000C',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    10: {
        ElementEx: '0x2317d8b224328644759319dffa2a5da77c72e0e9',
        ElementExSwapV2: '0xc9605a76b0370e148b4a510757685949f13248c7',
        Helper: '0xbe6461385106793d2099399358d233c934d41581',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    534352: {
        ElementEx: '0x0cab6977a9c70e04458b740476b498b214019641',
        ElementExSwapV2: '0x217efe077801387d125fe98e1b61cdda4d1364d2',
        Helper: '0x17bab823e1b4716f9bbe9eefc274f55ddf4056fd',
        WToken: '0x5300000000000000000000000000000000000004'
    },
    169: {
        ElementEx: '0x0cab6977a9c70e04458b740476b498b214019641',
        ElementExSwapV2: '0xbcfa22a36e555c507092ff16c1af4cb74b8514c8',
        Helper: '0x4bd6ff0413a095a79a855d83399a4850476be81e',
        WToken: '0x0dc808adce2099a9f62aa87d9670745aba741746'
    },
    5000: {
        ElementEx: '0x2fa13cf695ec51ded5b8e45ad0bef838ab17e2af',
        ElementExSwapV2: '0x9f47921d360aee0651a4f1ed2c4892b4923f9e52',
        Helper: '0x4c95419b74d420841caaad6345799522475f91d2',
        WToken: '0x78c1b0c915c4faa5fffa6cabf0219da63d7f4cb8'
    },
    42766: {
        ElementEx: '0x0cab6977a9c70e04458b740476b498b214019641',
        ElementExSwapV2: '0xc9605a76b0370e148b4a510757685949f13248c7',
        Helper: '0x0fd3d35c4536134e48a6bc05558b8d870878e119',
        WToken: '0xd33db7ec50a98164cc865dfaa64666906d79319c'
    },
    81457: {
        ElementEx: '0x4196b39157659bf0de9ebf6e505648b7889a39ce',
        ElementExSwapV2: '0xe29799ca0b98ba41343a4ea52fe15ed7d5e05662',
        Helper: '0x0fd3d35c4536134e48a6bc05558b8d870878e119',
        WToken: '0x4300000000000000000000000000000000000004'
    },
    4200: {
        ElementEx: '0x4196b39157659bf0de9ebf6e505648b7889a39ce',
        ElementExSwapV2: '0xe4ac19434cef450ead2942fa9ab01ec8fc0cf181',
        Helper: '0x917ef4f231cbd0972a10ec3453f40762c488e6fa',
        WToken: '0xf6d226f9dc15d9bb51182815b320d3fbe324e1ba'
    },
    //mode
    34443: {
        ElementEx: '0xa39A5f160a1952dDf38781Bd76E402B0006912A9',
        ElementExSwapV2: '0x2473e8d725f7b3eCa344c272F110948D63280f96',
        Helper: '0x66950320086664429C69735318724Ae24ec0D835',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    //cyber
    7560: {
        ElementEx: '0xa39A5f160a1952dDf38781Bd76E402B0006912A9',
        ElementExSwapV2: '0xF937CDf1c6457c9b22ecC8310CE7c6374cF78353',
        Helper: '0x4c95419b74D420841CaaAd6345799522475f91D2',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    //bob
    60808: {
        ElementEx: '0x2fa13cf695EC51Ded5B8E45Ad0BEf838aB17E2aF',
        ElementExSwapV2: '0x2040491367062EA1Ae1c73Bc3961c6D0151Aa39f',
        Helper: '0xfE357D8d1B285C846185b4Cae4F96bD81DF19445',
        WToken: '0x4200000000000000000000000000000000000006'
    },
    // lightlink
    1890: {
        ElementEx: '0xa39A5f160a1952dDf38781Bd76E402B0006912A9',
        ElementExSwapV2: '0x66950320086664429C69735318724Ae24ec0D835',
        Helper: '0x26Df6Fea89f1C9e4A3A2bfc2128542B7a05FbA8E',
        WToken: '0x7EbeF2A4b1B09381Ec5B9dF8C5c6f2dBECA59c73'
    },
    //zeta
    7000: {
        ElementEx: '0x4196b39157659BF0De9ebF6E505648B7889a39cE',
        ElementExSwapV2: '0x9f47921D360aeE0651A4F1ED2c4892B4923F9E52',
        Helper: '0x66950320086664429C69735318724Ae24ec0D835',
        WToken: '0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf'
    },
    //nibiru
    6900: {
        ElementEx: '0xa39A5f160a1952dDf38781Bd76E402B0006912A9',
        ElementExSwapV2: '0xf71a05E3749b0F9611307A37AFE3d853Bd734E13',
        Helper: '0xbe6461385106793d2099399358D233C934d41581',
        WToken: '0x0CaCF669f8446BeCA826913a3c6B96aCD4b02a97'
    },
    //abstract
    2741: {
        ElementEx: '0x3f33a3dab9e6f691a11D0EEBDf93dA445A021096',
        ElementExSwapV2: '0xA4306F9CeFC471447580C617905F49d43Df1Ece9',
        Helper: '0xb82F08665d2DDD19F219FadD6e01701E876D41eC',
        WToken: '0x3439153EB7AF838Ad19d56E1571FBD09333C2809'
    },
    //monad
    143: {
        ElementEx: '0x0cab6977a9c70e04458b740476b498b214019641',
        ElementExSwapV2: '0x42c759a719c228050901299b88fd316c3a050617',
        Helper: '0x701a4a5238af84a9c4ed8a23dee670069b44eeb7',
        WToken: '0x3bd359c1119da7da1d913d1c4d2b7c461115433a'
    },
    //bitlayer
    200901: {
        ElementEx: '0x0caB6977a9c70E04458b740476B498B214019641',
        ElementExSwapV2: '0xa52C8a12C728e95f1BeF74835b1316b7407b61A8',
        Helper: '0xe29799cA0B98BA41343A4eA52Fe15ed7D5e05662',
        WToken: '0xfF204e2681A6fA0e2C3FaDe68a1B28fb90E4Fc5F'
    },
};
const RPC_URLS = {
    1: 'https://api.zan.top/node/v1/eth/mainnet/6e96cfbcaff949bfbdaeb5fbc554ac7c',
};
// RPC 配置 API 地址
exports.RPC_CONF_API_URL = 'https://api.element.market/v1/quote/rpcConfInfo';
// 缓存的 RPC 配置
let cachedRpcConfigs = null;
let lastFetchTime = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 分钟缓存
/**
 * 从 HTTP 接口获取所有 RPC 配置
 * @returns Promise<RpcConfInfo[]> RPC 配置列表
 */
async function fetchRpcConfigs() {
    try {
        const response = await fetch(exports.RPC_CONF_API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        if (result.code !== 0) {
            throw new Error(`API error: ${result.status}`);
        }
        return result.data;
    }
    catch (error) {
        console.error('Failed to fetch RPC configs:', error);
        throw error;
    }
}
/**
 * 获取缓存的 RPC 配置（带缓存机制）
 * @returns Promise<Map<number, RpcConfInfo>> 链 ID 到 RPC 配置的映射
 */
async function getCachedRpcConfigs() {
    const now = Date.now();
    if (cachedRpcConfigs && now - lastFetchTime < CACHE_DURATION) {
        return cachedRpcConfigs;
    }
    const configs = await fetchRpcConfigs();
    const filteredConfigs = configs.filter(config => !config.isWalletPriority);
    cachedRpcConfigs = new Map(filteredConfigs.map(config => [config.chainMId, config]));
    // 将 RPC_URLS 中的静态配置也加入缓存
    Object.entries(RPC_URLS).forEach(([chainMId, rpcUrl]) => {
        if (!cachedRpcConfigs.has(parseInt(chainMId))) {
            cachedRpcConfigs.set(parseInt(chainMId), {
                chainMId: parseInt(chainMId),
                rpcUrl,
                isWalletPriority: false
            });
        }
    });
    lastFetchTime = now;
    return cachedRpcConfigs;
}
/**
 * 从远程获取指定链的 RPC URL
 * @param chainId 链 ID
 * @returns Promise<string | undefined> RPC URL
 */
async function getRpcUrlFromRemote(chainMId) {
    try {
        const configs = await getCachedRpcConfigs();
        const config = configs.get(chainMId);
        return config?.rpcUrl;
    }
    catch (error) {
        console.error(`Failed to get RPC URL for chain ${chainMId} from remote:`, error);
        return undefined;
    }
}
//# sourceMappingURL=config.js.map