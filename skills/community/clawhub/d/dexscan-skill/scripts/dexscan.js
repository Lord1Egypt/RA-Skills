/**
 * DexScan API 客户端
 * 提供 get/post 请求方式，支持签名认证
 *
 * ACCESS-KEY 获取优先级（从高到低）：
 * 1. .env文件配置：DS_ACCESS_KEY（从 dexscan-skill 目录向上逐级查找）
 * 2. 操作系统环境变量：DS_ACCESS_KEY
 *
 * SECRET-KEY 获取优先级（从高到低）：
 * 1. .env文件配置：DS_SECRET_KEY（从 dexscan-skill 目录向上逐级查找）
 * 2. 操作系统环境变量：DS_SECRET_KEY
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const BASE_URI = 'https://openapi.dexscan.trade';

// 读取 .env 文件，从 dexscan-skill 目录向上逐级查找直到根目录
function readEnvFile() {
    const envConfig = {};
    let currentDir = __dirname;

    // 向上逐级查找 .env 文件，直到根目录
    while (true) {
        const envPath = path.join(currentDir, '.env');
        if (fs.existsSync(envPath)) {
            const content = fs.readFileSync(envPath, 'utf-8');
            content.split('\n').forEach(line => {
                const match = line.match(/^\s*DS_ACCESS_KEY\s*=\s*"?([^"]*)"?/);
                if (match) envConfig.DS_ACCESS_KEY = match[1].trim();
                const match2 = line.match(/^\s*DS_SECRET_KEY\s*=\s*"?([^"]*)"?/);
                if (match2) envConfig.DS_SECRET_KEY = match2[1].trim();
            });
            break;
        }

        const parentDir = path.dirname(currentDir);
        // 已经到达根目录，停止查找
        if (parentDir === currentDir) {
            break;
        }
        currentDir = parentDir;
    }

    return envConfig;
}

const envConfig = readEnvFile();

/**
 * 时间戳转换为 yyyy-MM-dd HH:mm:ss 格式
 * @param {number|string} timestamp - 毫秒时间戳
 * @returns {string} 格式化后的时间字符串
 */
function formatTimestamp(timestamp) {
    if (!timestamp || timestamp === 0) return '-';
    const date = new Date(Number(timestamp));
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * 递归格式化响应数据中的时间字段
 * 字段名含 time 或 date（不区分大小写）且值为数字时，转换为 yyyy-MM-dd HH:mm:ss 格式
 * cursor 对象内的字段保持原始值不转换
 * @param {any} data - 待格式化的数据
 * @returns {any} 格式化后的数据
 */
function formatResponseData(data) {
    if (data === null || data === undefined) return data;

    if (Array.isArray(data)) {
        return data.map(item => formatResponseData(item));
    }

    if (typeof data === 'object') {
        const result = {};
        for (const [key, value] of Object.entries(data)) {
            if (key === 'cursor') {
                // cursor 对象内字段保持原始值
                result[key] = value;
            } else if (/time|date/i.test(key) && typeof value === 'number') {
                result[key] = formatTimestamp(value);
            } else {
                result[key] = formatResponseData(value);
            }
        }
        return result;
    }

    return data;
}

/**
 * 获取 ACCESS-KEY
 * 优先级：.env文件配置 > 环境变量
 */
function getAccessKey() {
    const key = envConfig.DS_ACCESS_KEY || process.env.DS_ACCESS_KEY;
    if (!key) {
        throw new Error('DS_ACCESS_KEY 未配置，请参考 .env 文件配置或者配置环境变量 DS_ACCESS_KEY');
    }
    return key;
}

/**
 * 获取 SECRET-KEY
 * 优先级：.env文件配置 > 环境变量
 */
function getSecretKey() {
    const key = envConfig.DS_SECRET_KEY || process.env.DS_SECRET_KEY;
    if (!key) {
        throw new Error('DS_SECRET_KEY 未配置，请参考 .env 文件配置或者配置环境变量 DS_SECRET_KEY');
    }
    return key;
}

/**
 * 生成签名头
 * @returns {{ ACCESS-KEY: string, ACCESS-TIMESTAMP: string, ACCESS-SIGN: string }}
 */
function getAuthHeaders() {
    const accessKey = getAccessKey();
    const timestamp = Date.now().toString();
    const signString = accessKey + ":" + timestamp;
    const secretKey = getSecretKey();

    const sign = crypto.createHmac('sha256', secretKey)
        .update(signString)
        .digest('base64');

    return {
        'ACCESS-KEY': accessKey,
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-SIGN': sign
    };
}

/**
 * 发送 GET 请求
 * @param {string} path - 请求路径（不包含 base_uri）
 * @param {object} params - 查询参数
 * @returns {Promise<any>}
 */
async function get(path, params = {}) {
    const auth = getAuthHeaders();
    const url = BASE_URI + path + '?' + new URLSearchParams(params);

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...auth
        }
    });

    return response.json();
}

/**
 * 发送 POST 请求
 * @param {string} path - 请求路径（不包含 base_uri）
 * @param {object} data - 请求体数据
 * @returns {Promise<any>}
 */
async function post(path, data = {}) {
    const auth = getAuthHeaders();
    const url = BASE_URI + path;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...auth
        },
        body: JSON.stringify(data)
    });

    return response.json();
}

/**
 * 发送 POST 请求并对响应数据执行时间字段格式化
 * @param {string} path - 请求路径
 * @param {object} data - 请求体数据
 * @returns {Promise<any>}
 */
async function apiPost(path, data = {}) {
    const result = await post(path, data);
    if (result && result.data !== undefined) {
        result.data = formatResponseData(result.data);
    }
    return result;
}

// ==================== 代币接口 ====================

/**
 * 代币排行查询
 * 接口地址: POST /v3/coin/rank-page
 * 接口描述: 按指定排序维度查询代币排行榜，支持按链筛选与分页
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL；传 ALL 查全链
 * @param {string} options.bar - 时间周期（5m/1h/4h/24h）
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @param {number} [options.minValue] - 成交额最小值（USD）
 * @param {number} [options.maxValue] - 成交额最大值（USD）
 * @param {number} [options.minLiquid] - 流动性最小值（USD）
 * @param {number} [options.maxLiquid] - 流动性最大值（USD）
 * @param {number} [options.minPriceChange] - 涨跌幅最小值
 * @param {number} [options.maxPriceChange] - 涨跌幅最大值
 * @param {number} [options.minMarketCap] - 市值最小值（USD）
 * @param {number} [options.maxMarketCap] - 市值最大值（USD）
 * @param {number} [options.minTradeCount] - 交易笔数最小值
 * @param {number} [options.maxTradeCount] - 交易笔数最大值
 * @param {number} [options.minAddressCount] - 独立交易地址数最小值
 * @param {number} [options.maxAddressCount] - 独立交易地址数最大值
 * @param {number} [options.minHolderCount] - 持仓人数最小值
 * @param {number} [options.maxHolderCount] - 持仓人数最大值
 * @param {number} [options.minCreateTime] - 代币创建时间下限（毫秒时间戳）
 * @param {number} [options.maxCreateTime] - 代币创建时间上限（毫秒时间戳）
 * @param {string} [options.unit] - 代币上线时长单位（YEAR/MONTH/DAY/HOUR/MINUTE）
 * @param {number} [options.minCreateDuration] - 代币上线时长下限
 * @param {number} [options.maxCreateDuration] - 代币上线时长上限
 * @param {boolean} [options.onlyMeme] - 仅查询 Meme 代币
 * @param {boolean} [options.hideHigh] - 隐藏高风险代币
 * @param {boolean} [options.hideStable] - 隐藏稳定币
 * @returns {Promise<any>}
 */
async function queryCoinRankPage(options = {}) {
    const {
        chainName,
        bar,
        page,
        pageSize,
        minValue,
        maxValue,
        minLiquid,
        maxLiquid,
        minPriceChange,
        maxPriceChange,
        minMarketCap,
        maxMarketCap,
        minTradeCount,
        maxTradeCount,
        minAddressCount,
        maxAddressCount,
        minHolderCount,
        maxHolderCount,
        minCreateTime,
        maxCreateTime,
        unit,
        minCreateDuration,
        maxCreateDuration,
        onlyMeme,
        hideHigh,
        hideStable
    } = options;

    const params = { chainName, bar };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (minValue !== undefined) params.minValue = minValue;
    if (maxValue !== undefined) params.maxValue = maxValue;
    if (minLiquid !== undefined) params.minLiquid = minLiquid;
    if (maxLiquid !== undefined) params.maxLiquid = maxLiquid;
    if (minPriceChange !== undefined) params.minPriceChange = minPriceChange;
    if (maxPriceChange !== undefined) params.maxPriceChange = maxPriceChange;
    if (minMarketCap !== undefined) params.minMarketCap = minMarketCap;
    if (maxMarketCap !== undefined) params.maxMarketCap = maxMarketCap;
    if (minTradeCount !== undefined) params.minTradeCount = minTradeCount;
    if (maxTradeCount !== undefined) params.maxTradeCount = maxTradeCount;
    if (minAddressCount !== undefined) params.minAddressCount = minAddressCount;
    if (maxAddressCount !== undefined) params.maxAddressCount = maxAddressCount;
    if (minHolderCount !== undefined) params.minHolderCount = minHolderCount;
    if (maxHolderCount !== undefined) params.maxHolderCount = maxHolderCount;
    if (minCreateTime !== undefined) params.minCreateTime = minCreateTime;
    if (maxCreateTime !== undefined) params.maxCreateTime = maxCreateTime;
    if (unit !== undefined) params.unit = unit;
    if (minCreateDuration !== undefined) params.minCreateDuration = minCreateDuration;
    if (maxCreateDuration !== undefined) params.maxCreateDuration = maxCreateDuration;
    if (onlyMeme !== undefined) params.onlyMeme = onlyMeme;
    if (hideHigh !== undefined) params.hideHigh = hideHigh;
    if (hideStable !== undefined) params.hideStable = hideStable;

    return apiPost('/v3/coin/rank-page', params);
}

/**
 * 代币详情查询
 * 接口地址: POST /v3/coin/info
 * 接口描述: 查询单个代币的完整信息
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @returns {Promise<any>}
 */
async function queryCoinInfo(options = {}) {
    const { chainName, tokenContractAddress } = options;
    return apiPost('/v3/coin/info', {
        chainName,
        tokenContractAddress
    });
}

/**
 * 代币信号列表查询
 * 接口地址: POST /v3/coin/signal-scroll
 * 接口描述: 基于链上交易行为与社媒热度生成代币评分信号，游标分页每页20条
 * @param {object} options - 查询参数
 * @param {string} [options.chainName] - 链名，如 SOL、BSC
 * @param {object} [options.cursor] - 游标
 * @param {string} options.cursor.address - 代币合约地址
 * @param {number} options.cursor.signalTime - 信号时间戳（毫秒）
 * @returns {Promise<any>}
 */
async function queryCoinSignalScroll(options = {}) {
    const { chainName, cursor } = options;
    return apiPost('/v3/coin/signal-scroll', {
        chainName,
        cursor
    });
}

/**
 * 代币信号排行榜查询
 * 接口地址: POST /v3/coin/signal-rank
 * 接口描述: 返回24小时内发出信号的代币TOP10排行
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @returns {Promise<any>}
 */
async function queryCoinSignalRank(options = {}) {
    const { chainName } = options;
    return apiPost('/v3/coin/signal-rank', {
        chainName
    });
}

/**
 * 开发者代币列表查询
 * 接口地址: POST /v3/coin/developer-scroll
 * 接口描述: 游标分页查询指定代币的开发者地址所创建的其他代币
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {number} [options.size] - 每次返回数量，默认 30
 * @param {number} [options.cursor] - 游标（创建时间戳毫秒）
 * @param {boolean} [options.needStats] - 是否返回开发者汇总统计
 * @returns {Promise<any>}
 */
async function queryCoinDeveloperScroll(options = {}) {
    const { chainName, tokenContractAddress, size, cursor, needStats } = options;
    const params = { chainName, tokenContractAddress };
    if (size !== undefined) params.size = size;
    if (cursor !== undefined) params.cursor = cursor;
    if (needStats !== undefined) params.needStats = needStats;
    return apiPost('/v3/coin/developer-scroll', params);
}

/**
 * 代币搜索
 * 接口地址: GET /v3/coin/search
 * 接口描述: 支持按代币名称或合约地址进行搜索
 * @param {object} options - 查询参数
 * @param {string} options.text - 搜索关键词
 * @param {string} [options.chainName] - 链名过滤
 * @returns {Promise<any>}
 */
async function queryCoinSearch(options = {}) {
    const { text, chainName } = options;
    return get('/v3/coin/search', { text, chainName });
}

/**
 * 社媒热度榜单
 * 接口地址: POST /v3/coin/heat-page
 * 接口描述: 查询代币的社交媒体热度数据
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名（SOL/BSC）
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @param {number} [options.heatDate] - 热度日期（毫秒时间戳）
 * @param {boolean} [options.onlyNewCoin] - 仅展示新币
 * @param {boolean} [options.onlyBlueChipCoin] - 仅展示蓝筹币
 * @returns {Promise<any>}
 */
async function queryCoinHeatPage(options = {}) {
    const { chainName, page, pageSize, heatDate, onlyNewCoin, onlyBlueChipCoin } = options;
    const params = { chainName };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (heatDate !== undefined) params.heatDate = heatDate;
    if (onlyNewCoin !== undefined) params.onlyNewCoin = onlyNewCoin;
    if (onlyBlueChipCoin !== undefined) params.onlyBlueChipCoin = onlyBlueChipCoin;
    return apiPost('/v3/coin/heat-page', params);
}

/**
 * Meme代币排行
 * 接口地址: POST /v3/coin/meme-rank
 * 接口描述: 查询Meme平台代币排行
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.type - 排行类型（NEW_CREATION/PUMP/COMPLETED）
 * @param {Array} [options.dexs] - 指定 DEX 名称列表
 * @returns {Promise<any>}
 */
async function queryCoinMemeRank(options = {}) {
    const { chainName, type, dexs } = options;
    const params = { chainName, type };
    if (dexs !== undefined) params.dexs = dexs;
    return apiPost('/v3/coin/meme-rank', params);
}

/**
 * Meme支持的DEX列表
 * 接口地址: POST /v3/coin/meme-dexs
 * 接口描述: 查询指定链上Meme模块当前支持的DEX名称列表
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @returns {Promise<any>}
 */
async function queryCoinMemeDexs(options = {}) {
    const { chainName } = options;
    return apiPost('/v3/coin/meme-dexs', { chainName });
}

/**
 * 推文热度数据
 * 接口地址: POST /v3/coin/twitter-tweets-heat
 * 接口描述: 根据推文ID集合批量查询推文的热度快照数据
 * @param {object} options - 查询参数
 * @param {Array} options.tweetIds - 推文 ID 列表
 * @returns {Promise<any>}
 */
async function queryCoinTwitterTweetsHeat(options = {}) {
    const { tweetIds } = options;
    return apiPost('/v3/coin/twitter-tweets-heat', tweetIds);
}

// ==================== 行情接口 ====================

/**
 * 交易活动列表（游标分页）
 * 接口地址: POST /v3/market/trade-scroll
 * 接口描述: 游标分页查询指定代币的链上交易记录
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {Array} [options.swapTypes] - 交易类型列表（1-买入，2-卖出）
 * @param {number} [options.minValue] - 成交额最小值（USD）
 * @param {number} [options.maxValue] - 成交额最大值（USD）
 * @param {string} [options.address] - 过滤指定钱包地址
 * @param {number} [options.begin] - 起始时间（毫秒时间戳）
 * @param {number} [options.end] - 结束时间（毫秒时间戳）
 * @param {number} [options.dexEnum] - DEX 类型枚举值
 * @param {boolean} [options.timeDesc] - 是否按时间倒序，默认 true
 * @param {number} [options.size] - 每次返回数量，默认 50
 * @param {object} [options.cursor] - 游标
 * @returns {Promise<any>}
 */
async function queryMarketTradeScroll(options = {}) {
    const {
        chainName,
        tokenContractAddress,
        swapTypes,
        minValue,
        maxValue,
        address,
        begin,
        end,
        dexEnum,
        timeDesc,
        size,
        cursor
    } = options;

    const params = { chainName, tokenContractAddress };
    if (swapTypes) params.swapTypes = swapTypes;
    if (minValue !== undefined) params.minValue = minValue;
    if (maxValue !== undefined) params.maxValue = maxValue;
    if (address) params.address = address;
    if (begin !== undefined) params.begin = begin;
    if (end !== undefined) params.end = end;
    if (dexEnum !== undefined) params.dexEnum = dexEnum;
    if (timeDesc !== undefined) params.timeDesc = timeDesc;
    if (size !== undefined) params.size = size;
    if (cursor) params.cursor = cursor;

    return apiPost('/v3/market/trade-scroll', params);
}

/**
 * 流动性变化列表（游标分页）
 * 接口地址: POST /v3/market/liquid-scroll
 * 接口描述: 游标分页查询指定代币的流动性增减事件
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {Array} [options.swapTypes] - 操作类型（1-添加，2-移除）
 * @param {number} [options.minValue] - 操作金额最小值（USD）
 * @param {number} [options.maxValue] - 操作金额最大值（USD）
 * @param {string} [options.address] - 过滤指定 LP 地址
 * @param {number} [options.begin] - 起始时间（毫秒时间戳）
 * @param {number} [options.end] - 结束时间（毫秒时间戳）
 * @param {number} [options.dexEnum] - DEX 类型枚举值
 * @param {boolean} [options.timeDesc] - 是否按时间倒序，默认 true
 * @param {number} [options.size] - 每次返回数量，默认 50
 * @param {object} [options.cursor] - 游标
 * @returns {Promise<any>}
 */
async function queryMarketLiquidScroll(options = {}) {
    const {
        chainName,
        tokenContractAddress,
        swapTypes,
        minValue,
        maxValue,
        address,
        begin,
        end,
        dexEnum,
        timeDesc,
        size,
        cursor
    } = options;

    const params = { chainName, tokenContractAddress };
    if (swapTypes) params.swapTypes = swapTypes;
    if (minValue !== undefined) params.minValue = minValue;
    if (maxValue !== undefined) params.maxValue = maxValue;
    if (address) params.address = address;
    if (begin !== undefined) params.begin = begin;
    if (end !== undefined) params.end = end;
    if (dexEnum !== undefined) params.dexEnum = dexEnum;
    if (timeDesc !== undefined) params.timeDesc = timeDesc;
    if (size !== undefined) params.size = size;
    if (cursor) params.cursor = cursor;

    return apiPost('/v3/market/liquid-scroll', params);
}

/**
 * 代币盈利列表
 * 接口地址: POST /v3/market/pnl-coin-list
 * 接口描述: 查询指定代币的持有者盈亏统计
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {string} [options.type] - 地址标签筛选（DEV/KOL/TOP10/SNIPER/NEW）
 * @param {boolean} [options.holderList] - 是否只查持仓中地址
 * @param {Array} [options.addresses] - 批量钱包地址列表，最多10个
 * @returns {Promise<any>}
 */
async function queryMarketPnlCoinList(options = {}) {
    const { chainName, tokenContractAddress, type, holderList, addresses } = options;
    const params = { chainName, tokenContractAddress };
    if (type) params.type = type;
    if (holderList !== undefined) params.holderList = holderList;
    if (addresses) params.addresses = addresses;
    return apiPost('/v3/market/pnl-coin-list', params);
}

/**
 * 代币近期统计信息
 * 接口地址: POST /v3/market/coin-summary
 * 接口描述: 查询代币各时间周期的近期行情概要
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @returns {Promise<any>}
 */
async function queryMarketCoinSummary(options = {}) {
    const { chainName, tokenContractAddress } = options;
    return apiPost('/v3/market/coin-summary', {
        chainName,
        tokenContractAddress
    });
}

/**
 * K线历史数据
 * 接口地址: POST /v3/market/kline-historical
 * 接口描述: 查询代币指定时间粒度的K线历史数据
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {string} options.bar - K线粒度（1m/5m/15m/30m/1h/4h/1D/1W）
 * @param {number} [options.before] - 查询该时间之前的数据（毫秒时间戳）
 * @param {number} [options.after] - 查询该时间之后的数据（毫秒时间戳）
 * @param {number} [options.limit] - 最多返回条数，默认 400，最大 1500
 * @param {boolean} [options.useNativePricing] - 是否使用原生代币计价
 * @returns {Promise<any>}
 */
async function queryMarketKlineHistorical(options = {}) {
    const { chainName, tokenContractAddress, bar, before, after, limit, useNativePricing } = options;
    const params = { chainName, tokenContractAddress, bar };
    if (before !== undefined) params.before = before;
    if (after !== undefined) params.after = after;
    if (limit !== undefined) params.limit = limit;
    if (useNativePricing !== undefined) params.useNativePricing = useNativePricing;
    return apiPost('/v3/market/kline-historical', params);
}

/**
 * 代币流动性池子列表
 * 接口地址: POST /v3/market/pool-top
 * 接口描述: 查询代币流动性最高的前20个池子
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @returns {Promise<any>}
 */
async function queryMarketPoolTop(options = {}) {
    const { chainName, tokenContractAddress } = options;
    return apiPost('/v3/market/pool-top', {
        chainName,
        tokenContractAddress
    });
}

// ==================== 地址接口 ====================

/**
 * 地址盈亏分析列表（分页）
 * 接口地址: POST /v3/address/pnl-page
 * 接口描述: 分页查询指定地址持有的代币盈亏情况
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.address - 钱包地址
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @param {string} [options.baseAddress] - 过滤指定代币合约地址
 * @param {boolean} [options.hideHighRisk] - 隐藏高风险代币
 * @param {boolean} [options.hideClearance] - 隐藏已清仓代币
 * @param {boolean} [options.hideLowValue] - 隐藏低价值代币
 * @param {number} [options.minRealizedPnlRatio] - 已实现盈亏比例最小值
 * @param {number} [options.maxRealizedPnlRatio] - 已实现盈亏比例最大值
 * @param {number} [options.minUnrealizedPnlRatio] - 未实现盈亏比例最小值
 * @param {number} [options.maxUnrealizedPnlRatio] - 未实现盈亏比例最大值
 * @param {number} [options.minTotalPnlRatio] - 总盈亏比例最小值
 * @param {number} [options.maxTotalPnlRatio] - 总盈亏比例最大值
 * @returns {Promise<any>}
 */
async function queryAddressPnlPage(options = {}) {
    const {
        chainName,
        address,
        page,
        pageSize,
        baseAddress,
        hideHighRisk,
        hideClearance,
        hideLowValue,
        minRealizedPnlRatio,
        maxRealizedPnlRatio,
        minUnrealizedPnlRatio,
        maxUnrealizedPnlRatio,
        minTotalPnlRatio,
        maxTotalPnlRatio
    } = options;

    const params = { chainName, address };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (baseAddress) params.baseAddress = baseAddress;
    if (hideHighRisk !== undefined) params.hideHighRisk = hideHighRisk;
    if (hideClearance !== undefined) params.hideClearance = hideClearance;
    if (hideLowValue !== undefined) params.hideLowValue = hideLowValue;
    if (minRealizedPnlRatio !== undefined) params.minRealizedPnlRatio = minRealizedPnlRatio;
    if (maxRealizedPnlRatio !== undefined) params.maxRealizedPnlRatio = maxRealizedPnlRatio;
    if (minUnrealizedPnlRatio !== undefined) params.minUnrealizedPnlRatio = minUnrealizedPnlRatio;
    if (maxUnrealizedPnlRatio !== undefined) params.maxUnrealizedPnlRatio = maxUnrealizedPnlRatio;
    if (minTotalPnlRatio !== undefined) params.minTotalPnlRatio = minTotalPnlRatio;
    if (maxTotalPnlRatio !== undefined) params.maxTotalPnlRatio = maxTotalPnlRatio;

    return apiPost('/v3/address/pnl-page', params);
}

/**
 * 地址资产组合列表（分页）
 * 接口地址: POST /v3/address/asset-top
 * 接口描述: 分页查询指定地址当前持有的代币资产
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.address - 钱包地址
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @returns {Promise<any>}
 */
async function queryAddressAssetTop(options = {}) {
    const { chainName, address, page, pageSize } = options;
    const params = { chainName, address };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    return apiPost('/v3/address/asset-top', params);
}

/**
 * 地址交易历史（游标分页）
 * 接口地址: POST /v3/address/trade-scroll
 * 接口描述: 游标分页查询指定地址的链上交易记录
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.address - 钱包地址
 * @param {string} [options.tokenContractAddress] - 过滤指定代币合约地址
 * @param {Array} [options.swapTypes] - 交易类型列表（1-买入，2-卖出）
 * @param {number} [options.size] - 每次返回数量，默认 30
 * @param {object} [options.cursor] - 游标
 * @returns {Promise<any>}
 */
async function queryAddressTradeScroll(options = {}) {
    const { chainName, address, tokenContractAddress, swapTypes, size, cursor } = options;
    const params = { chainName, address };
    if (tokenContractAddress) params.tokenContractAddress = tokenContractAddress;
    if (swapTypes) params.swapTypes = swapTypes;
    if (size !== undefined) params.size = size;
    if (cursor) params.cursor = cursor;
    return apiPost('/v3/address/trade-scroll', params);
}

/**
 * 地址开发者代币列表（分页）
 * 接口地址: POST /v3/address/developer-page
 * 接口描述: 分页查询指定开发者地址曾发行的代币列表
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.addressDev - 开发者钱包地址
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @returns {Promise<any>}
 */
async function queryAddressDeveloperPage(options = {}) {
    const { chainName, addressDev, page, pageSize } = options;
    const params = { chainName, addressDev };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    return apiPost('/v3/address/developer-page', params);
}

// ==================== 牛人榜 ====================

/**
 * 牛人榜（分页）
 * 接口地址: POST /v3/address/rank-page
 * 接口描述: 分页查询链上盈利能力排名靠前的地址
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，如 SOL、BSC
 * @param {string} options.bar - 统计周期（7d/30d/90d）
 * @param {number} [options.page] - 页码，默认 1
 * @param {number} [options.pageSize] - 每页数量，默认 10
 * @param {string} [options.tag] - 地址标签筛选，可选值：KOL
 * @param {number} [options.minPnl] - 总盈亏最小值（USD）
 * @param {number} [options.maxPnl] - 总盈亏最大值（USD）
 * @param {number} [options.minWinRatio] - 胜率最小值（0~1）
 * @param {number} [options.maxWinRatio] - 胜率最大值（0~1）
 * @param {number} [options.minNumber] - 交易笔数最小值
 * @param {number} [options.maxNumber] - 交易笔数最大值
 * @param {number} [options.minValue] - 成交额最小值（USD）
 * @param {number} [options.maxValue] - 成交额最大值（USD）
 * @returns {Promise<any>}
 */
async function queryAddressRankPage(options = {}) {
    const {
        chainName,
        bar,
        page,
        pageSize,
        tag,
        minPnl,
        maxPnl,
        minWinRatio,
        maxWinRatio,
        minNumber,
        maxNumber,
        minValue,
        maxValue
    } = options;

    const params = { chainName, bar };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (tag !== undefined) params.tag = tag;
    if (minPnl !== undefined) params.minPnl = minPnl;
    if (maxPnl !== undefined) params.maxPnl = maxPnl;
    if (minWinRatio !== undefined) params.minWinRatio = minWinRatio;
    if (maxWinRatio !== undefined) params.maxWinRatio = maxWinRatio;
    if (minNumber !== undefined) params.minNumber = minNumber;
    if (maxNumber !== undefined) params.maxNumber = maxNumber;
    if (minValue !== undefined) params.minValue = minValue;
    if (maxValue !== undefined) params.maxValue = maxValue;

    return apiPost('/v3/address/rank-page', params);
}

// 导出方法
module.exports = {
    get,
    post,
    // 代币接口
    queryCoinRankPage,
    queryCoinInfo,
    queryCoinSignalScroll,
    queryCoinSignalRank,
    queryCoinDeveloperScroll,
    queryCoinSearch,
    queryCoinHeatPage,
    queryCoinMemeRank,
    queryCoinMemeDexs,
    queryCoinTwitterTweetsHeat,
    // 行情接口
    queryMarketTradeScroll,
    queryMarketLiquidScroll,
    queryMarketPnlCoinList,
    queryMarketCoinSummary,
    queryMarketKlineHistorical,
    queryMarketPoolTop,
    // 地址接口
    queryAddressPnlPage,
    queryAddressAssetTop,
    queryAddressTradeScroll,
    queryAddressDeveloperPage,
    // 牛人榜
    queryAddressRankPage
};
