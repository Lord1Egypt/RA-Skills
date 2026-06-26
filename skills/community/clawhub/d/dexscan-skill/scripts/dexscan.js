/**
 * DexScan API 客户端
 * 提供 get/post 请求方式，支持签名认证
 *
 * ACCESS-KEY 获取优先级（从高到低）：
 * 1. 操作系统环境变量：DS_ACCESS_KEY
 * 2. js文件全局变量默认值：DEFAULT_ACCESS_KEY
 *
 * SECRET-KEY 获取优先级（从高到低）：
 * 1. 操作系统环境变量：DS_SECRET_KEY
 * 2. js文件全局变量默认值：DEFAULT_SECRET_KEY
 */

const crypto = require('crypto');
const BASE_URI = 'https://openapi.dexscan.trade';

// 全局变量默认值（环境变量不存在时使用）
const DEFAULT_ACCESS_KEY = '3b13a13c8dc541e39ff8089db40cabf6';
const DEFAULT_SECRET_KEY = '43e14928cec443c3b2a13a7603331e03';

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
 * 优先级：环境变量 > 全局变量默认值
 */
function getAccessKey() {
    return process.env.DS_ACCESS_KEY || DEFAULT_ACCESS_KEY || null;
}

/**
 * 获取 SECRET-KEY
 * 优先级：环境变量 > 全局变量默认值
 */
function getSecretKey() {
    return process.env.DS_SECRET_KEY || DEFAULT_SECRET_KEY || null;
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

// ==================== 代币信号接口 ====================

/**
 * 信号列表查询（分页查询）
 * 接口地址: POST /v3/coin-signal-scroll
 * 接口描述: 查询24小时信号，支持游标分页，每页返回20条
 * @param {object} options - 查询参数
 * @param {string} [options.chainName] - 链名称 (SOL/BSC/Base/ETH/Polygon/Arbitrum/Optimism/Avalanche/Monad/SUI)
 * @param {object} [options.cursor] - 游标，用于分页
 * @param {string} options.cursor.address - 代币地址
 * @param {number} options.cursor.signalTime - 最新信号时间
 * @returns {Promise<any>}
 */
async function querySignalList(options = {}) {
    const { chainName, cursor } = options;
    return apiPost('/v3/coin-signal-scroll', {
        chainName,
        cursor
    });
}

/**
 * 信号排行榜查询
 * 接口地址: POST /v3/coin-signal-rank
 * 接口描述: 查询24小时信号排行榜TOP10，基于首次信号最大涨幅降序，最新信号推送时间降序。
 * @param {object} options - 查询参数
 * @param {string} [options.chainName] - 链名称
 * @returns {Promise<any>}
 */
async function querySignalRank(options = {}) {
    const { chainName } = options;
    return apiPost('/v3/coin-signal-rank', {
        chainName
    });
}

// ==================== 地址牛人榜接口 ====================

/**
 * 地址牛人榜查询
 * 接口地址: POST /v3/address-rank-page
 * 接口描述: 查询地址盈亏排行榜，支持多条件筛选和排序
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名称
 * @param {string} options.bar - 时间枚举（7d、30d、90d）
 * @param {number} options.page - 页数
 * @param {number} options.pageSize - 每页条数
 * @param {Array} [options.order] - 排序规则 [{column: 'pnl', asc: false}]
 * @param {string} [options.tag] - 标签枚举（KOL）
 * @param {number} [options.minPnl] - 收益额最小值
 * @param {number} [options.maxPnl] - 收益额最大值
 * @param {number} [options.minWinRatio] - 胜率最小值
 * @param {number} [options.maxWinRatio] - 胜率最大值
 * @param {number} [options.minNumber] - 交易笔数最小值
 * @param {number} [options.maxNumber] - 交易笔数最大值
 * @returns {Promise<any>}
 */
async function queryAddressRank(options = {}) {
    const {
        chainName,
        bar,
        page = 1,
        pageSize = 20,
        order = [{ column: 'pnl', asc: false }],
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

    const params = {
        chainName,
        bar,
        page: String(page),
        pageSize: String(pageSize),
        order
    };

    if (tag !== undefined) params.tag = tag;
    if (minPnl !== undefined) params.minPnl = minPnl;
    if (maxPnl !== undefined) params.maxPnl = maxPnl;
    if (minWinRatio !== undefined) params.minWinRatio = minWinRatio;
    if (maxWinRatio !== undefined) params.maxWinRatio = maxWinRatio;
    if (minNumber !== undefined) params.minNumber = minNumber;
    if (maxNumber !== undefined) params.maxNumber = maxNumber;
    if (minValue !== undefined) params.minValue = minValue;
    if (maxValue !== undefined) params.maxValue = maxValue;

    return apiPost('/v3/address-rank-page', params);
}

// ==================== 热度接口 ====================

/**
 * 社交热度列表查询
 * 接口地址: POST /v3/coin-heat-page
 * 接口描述: 社交热度列表，支持分页和排序
 * @param {object} options - 查询参数
 * @param {number} options.page - 页数
 * @param {number} options.pageSize - 每页条数
 * @param {string} options.chainName - 链名
 * @param {Array} [options.order] - 排序规则 [{column: 'displayHeat', asc: false}]
 * @param {number} [options.heatDate] - 热度时间戳
 * @param {boolean} [options.onlyLookNewCoin] - 是否新币
 * @param {boolean} [options.filtrationBlueChipCoin] - 是否过滤蓝筹币
 * @returns {Promise<any>}
 */
async function queryCoinHeatPage(options = {}) {
    const {
        page = 1,
        pageSize = 20,
        chainName,
        order = [{ column: 'displayHeat', asc: false }],
        heatDate,
        onlyLookNewCoin,
        filtrationBlueChipCoin
    } = options;

    const params = {
        page,
        pageSize,
        chainName,
        order
    };

    if (heatDate !== undefined) params.heatDate = heatDate;
    if (onlyLookNewCoin !== undefined) params.onlyLookNewCoin = onlyLookNewCoin;
    if (filtrationBlueChipCoin !== undefined) params.filtrationBlueChipCoin = filtrationBlueChipCoin;

    return apiPost('/v3/coin-heat-page', params);
}

/**
 * 推文热度数据查询
 * 接口地址: POST /v3/twitter-tweets-heat
 * 接口描述: 查询推文热度数据
 * @param {Array} tweetIds - 推文ID列表
 * @returns {Promise<any>}
 */
async function queryTwitterTweetsHeat(tweetIds = []) {
    return apiPost('/v3/twitter-tweets-heat', tweetIds);
}

// ==================== 行情接口 ====================

/**
 * 分页查询代币排行
 * 接口地址: POST /v3/market/coin-rank
 * 接口描述: 按时间粒度分页查询代币排行榜，支持过滤和排序
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名，ALL查全链
 * @param {string} options.bar - 时间粒度（5m/1h/4h/24h）
 * @param {number} [options.page] - 页数
 * @param {number} [options.pageSize] - 页大小
 * @param {Array} [options.order] - 排序规则 [{column: 'value', asc: false}]
 * @param {number} [options.minValue] - 成交额最小值
 * @param {number} [options.maxValue] - 成交额最大值
 * @param {number} [options.minLiquid] - 流动性最小值
 * @param {number} [options.maxLiquid] - 流动性最大值
 * @param {number} [options.minPriceChange] - 涨跌幅最小值
 * @param {number} [options.maxPriceChange] - 涨跌幅最大值
 * @param {number} [options.minMarketCap] - 市值最小值
 * @param {number} [options.maxMarketCap] - 市值最大值
 * @param {number} [options.minTradeCount] - 交易笔数最小值
 * @param {number} [options.maxTradeCount] - 交易笔数最大值
 * @param {number} [options.minAddressCount] - 活跃地址数最小值
 * @param {number} [options.maxAddressCount] - 活跃地址数最大值
 * @param {number} [options.minHolderCount] - 持币地址数最小值
 * @param {number} [options.maxHolderCount] - 持币地址数最大值
 * @param {boolean} [options.onlyMeme] - 只看Meme币
 * @param {boolean} [options.hideHigh] - 隐藏高风险
 * @param {boolean} [options.hideStable] - 隐藏稳定币
 * @returns {Promise<any>}
 */
async function queryCoinRank(options = {}) {
    const {
        chainName,
        bar,
        page,
        pageSize,
        order,
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
        onlyMeme,
        hideHigh,
        hideStable,
        unit,
        minCreateDuration,
        maxCreateDuration
    } = options;

    const params = { chainName, bar };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (order) params.order = order;
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
    if (onlyMeme !== undefined) params.onlyMeme = onlyMeme;
    if (hideHigh !== undefined) params.hideHigh = hideHigh;
    if (hideStable !== undefined) params.hideStable = hideStable;
    if (unit !== undefined) params.unit = unit;
    if (minCreateDuration !== undefined) params.minCreateDuration = minCreateDuration;
    if (maxCreateDuration !== undefined) params.maxCreateDuration = maxCreateDuration;

    return apiPost('/v3/market/coin-rank', params);
}

/**
 * 游标查询交易活动列表
 * 接口地址: POST /v3/market/trade-scroll
 * 接口描述: 游标分页查询指定代币的链上交易记录
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {Array} [options.swapTypes] - 交易类型（1-买入，2-卖出）
 * @param {number} [options.minValue] - 成交额最小值（USD）
 * @param {number} [options.maxValue] - 成交额最大值（USD）
 * @param {string} [options.address] - 按钱包地址筛选
 * @param {number} [options.begin] - 起始时间戳（毫秒）
 * @param {number} [options.end] - 截止时间戳（毫秒）
 * @param {number} [options.dexEnum] - DEX类型枚举值
 * @param {boolean} [options.timeDesc] - 是否时间倒序
 * @param {number} [options.size] - 每页数量，默认50
 * @param {object} [options.cursor] - 游标，首次不传
 * @returns {Promise<any>}
 */
async function queryTradeScroll(options = {}) {
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
 * 游标查询流动性变化列表
 * 接口地址: POST /v3/market/liquid-scroll
 * 接口描述: 游标分页查询指定代币的流动性添加/移除记录
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {Array} [options.swapTypes] - 流动性变更类型（1-添加，2-移除）
 * @param {number} [options.minValue] - 总额最小值（USD）
 * @param {number} [options.maxValue] - 总额最大值（USD）
 * @param {string} [options.address] - 按钱包地址筛选
 * @param {number} [options.begin] - 起始时间戳（毫秒）
 * @param {number} [options.end] - 截止时间戳（毫秒）
 * @param {number} [options.dexEnum] - DEX类型枚举值
 * @param {boolean} [options.timeDesc] - 是否时间倒序
 * @param {number} [options.size] - 每页数量，默认50
 * @param {object} [options.cursor] - 游标，首次不传
 * @returns {Promise<any>}
 */
async function queryLiquidScroll(options = {}) {
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
 * 查询代币盈利列表
 * 接口地址: POST /v3/market/pnl-coin-list
 * 接口描述: 查询指定代币的持仓地址盈亏数据列表
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {string} [options.type] - 地址类型筛选（DEV/KOL/TOP10/SNIPER/NEW）
 * @param {boolean} [options.holderList] - true时按持仓量排序返回Holder列表
 * @param {Array} [options.addresses] - 批量钱包地址列表，最多10个
 * @returns {Promise<any>}
 */
async function queryPnlCoinList(options = {}) {
    const {
        chainName,
        tokenContractAddress,
        type,
        holderList,
        addresses
    } = options;

    const params = { chainName, tokenContractAddress };
    if (type) params.type = type;
    if (holderList !== undefined) params.holderList = holderList;
    if (addresses) params.addresses = addresses;

    return apiPost('/v3/market/pnl-coin-list', params);
}

/**
 * 游标查询开发者代币列表
 * 接口地址: POST /v3/market/developer-scroll
 * 接口描述: 游标分页查询指定代币的关联开发者创建的代币列表
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {number} [options.size] - 每页数量，默认30
 * @param {number} [options.cursor] - 游标（创建时间戳ms），首次不传
 * @param {boolean} [options.needStats] - 是否返回开发者统计数据
 * @returns {Promise<any>}
 */
async function queryDeveloperScroll(options = {}) {
    const {
        chainName,
        tokenContractAddress,
        size,
        cursor,
        needStats
    } = options;

    const params = { chainName, tokenContractAddress };
    if (size !== undefined) params.size = size;
    if (cursor !== undefined) params.cursor = cursor;
    if (needStats !== undefined) params.needStats = needStats;

    return apiPost('/v3/market/developer-scroll', params);
}

/**
 * 查询代币近期统计信息
 * 接口地址: POST /v3/market/coin-summary
 * 接口描述: 查询代币近期统计信息
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {Array} [options.bars] - 时间粒度列表
 * @returns {Promise<any>}
 */
async function queryCoinSummary(options = {}) {
    const { chainName, tokenContractAddress, bars } = options;
    const params = { chainName, tokenContractAddress };
    if (bars) params.bars = bars;
    return apiPost('/v3/market/coin-summary', params);
}

/**
 * 查询代币信息
 * 接口地址: POST /v3/market/coin-info
 * 接口描述: 查询代币详细信息
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @returns {Promise<any>}
 */
async function queryCoinInfo(options = {}) {
    const { chainName, tokenContractAddress } = options;
    return apiPost('/v3/market/coin-info', {
        chainName,
        tokenContractAddress
    });
}

/**
 * 查询K线历史数据
 * 接口地址: POST /v3/market/kline-historical
 * 接口描述: 查询代币K线历史数据
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @param {string} options.interval - K线周期（1m/5m/15m/30m/1h/4h/1d/1w）
 * @param {number} options.begin - 起始时间戳（毫秒）
 * @param {number} options.end - 结束时间戳（毫秒）
 * @returns {Promise<any>}
 */
async function queryKlineHistorical(options = {}) {
    const {
        chainName,
        tokenContractAddress,
        interval,
        begin,
        end
    } = options;

    return apiPost('/v3/market/kline-historical', {
        chainName,
        tokenContractAddress,
        interval,
        begin,
        end
    });
}

/**
 * 查询Meme代币排行列表
 * 接口地址: POST /v3/market/meme-rank
 * 接口描述: 查询Meme代币排行列表
 * @param {object} options - 查询参数
 * @param {string} [options.chainName] - 链名
 * @param {Array} [options.order] - 排序规则 [{column: 'marketCap', asc: false}]
 * @param {number} [options.page] - 页数
 * @param {number} [options.pageSize] - 页大小
 * @returns {Promise<any>}
 */
async function queryMemeRank(options = {}) {
    const { chainName, order, page, pageSize } = options;
    const params = {};
    if (chainName) params.chainName = chainName;
    if (order) params.order = order;
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    return apiPost('/v3/market/meme-rank', params);
}

/**
 * 查询Meme支持的DEX列表
 * 接口地址: POST /v3/market/meme-dexs
 * 接口描述: 查询Meme代币支持的DEX列表
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.tokenContractAddress - 代币合约地址
 * @returns {Promise<any>}
 */
async function queryMemeDexs(options = {}) {
    const { chainName, tokenContractAddress } = options;
    return apiPost('/v3/market/meme-dexs', {
        chainName,
        tokenContractAddress
    });
}

// ==================== 地址情况接口 ====================

/**
 * 游标查询地址交易历史列表
 * 接口地址: POST /v3/address/address-trade-scroll
 * 接口描述: 游标分页查询指定钱包地址的历史交易盈亏记录
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.address - 钱包地址
 * @param {string} [options.tokenContractAddress] - 代币合约地址，传入时只查询该代币的交易记录
 * @param {Array} [options.swapTypes] - 交易类型（1-买入，2-卖出）
 * @param {number} [options.size] - 每次返回数量，默认30
 * @param {object} [options.cursor] - 游标，首次不传
 * @returns {Promise<any>}
 */
async function queryAddressTradeScroll(options = {}) {
    const {
        chainName,
        address,
        tokenContractAddress,
        swapTypes,
        size,
        cursor
    } = options;

    const params = { chainName, address };
    if (tokenContractAddress) params.tokenContractAddress = tokenContractAddress;
    if (swapTypes) params.swapTypes = swapTypes;
    if (size !== undefined) params.size = size;
    if (cursor) params.cursor = cursor;

    return apiPost('/v3/address/address-trade-scroll', params);
}

/**
 * 分页查询地址盈亏分析列表
 * 接口地址: POST /v3/address/address-list
 * 接口描述: 分页查询钱包地址的各代币持仓盈亏情况，支持多维度过滤和排序
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.address - 钱包地址
 * @param {number} [options.page] - 页数，默认1
 * @param {number} [options.pageSize] - 页大小，默认20
 * @param {Array} [options.order] - 排序规则 [{column: 'totalPnl', asc: false}]
 * @param {string} [options.baseAddress] - 代币合约地址，传入时只查询该代币
 * @param {boolean} [options.hideHighRisk] - 是否隐藏高风险代币
 * @param {boolean} [options.hideClearance] - 是否隐藏已清仓代币
 * @param {boolean} [options.hideLowValue] - 是否隐藏持仓价值低于$1的代币
 * @returns {Promise<any>}
 */
async function queryAddressList(options = {}) {
    const {
        chainName,
        address,
        page,
        pageSize,
        order,
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
    if (order) params.order = order;
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

    return apiPost('/v3/address/address-list', params);
}

/**
 * 分页查询地址资产组合列表
 * 接口地址: POST /v3/address/address-asset-top
 * 接口描述: 分页查询钱包地址的持仓资产列表，按持仓价值降序排列
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.address - 钱包地址
 * @param {number} [options.page] - 页数，默认1
 * @param {number} [options.pageSize] - 页大小，默认10
 * @returns {Promise<any>}
 */
async function queryAddressAssetTop(options = {}) {
    const {
        chainName,
        address,
        page,
        pageSize
    } = options;

    const params = { chainName, address };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;

    return apiPost('/v3/address/address-asset-top', params);
}

/**
 * 分页查询地址开发者代币列表
 * 接口地址: POST /v3/address/developer-page
 * 接口描述: 分页查询指定开发者地址创建的代币列表，支持排序
 * @param {object} options - 查询参数
 * @param {string} options.chainName - 链名
 * @param {string} options.addressDev - 开发者钱包地址
 * @param {number} [options.page] - 页数，默认1
 * @param {number} [options.pageSize] - 页大小，默认20
 * @param {Array} [options.order] - 排序规则 [{column: 'createTime', asc: false}]
 * @returns {Promise<any>}
 */
async function queryDeveloperPage(options = {}) {
    const {
        chainName,
        addressDev,
        page,
        pageSize,
        order
    } = options;

    const params = { chainName, addressDev };
    if (page !== undefined) params.page = page;
    if (pageSize !== undefined) params.pageSize = pageSize;
    if (order) params.order = order;

    return apiPost('/v3/address/developer-page', params);
}

// 导出方法
module.exports = {
    get,
    post,
    // 代币信号
    querySignalList,
    querySignalRank,
    // 地址牛人榜
    queryAddressRank,
    // 热度
    queryCoinHeatPage,
    queryTwitterTweetsHeat,
    // 行情
    queryCoinRank,
    queryTradeScroll,
    queryLiquidScroll,
    queryPnlCoinList,
    queryDeveloperScroll,
    queryCoinSummary,
    queryCoinInfo,
    queryKlineHistorical,
    queryMemeRank,
    queryMemeDexs,
    // 地址情况
    queryAddressTradeScroll,
    queryAddressList,
    queryAddressAssetTop,
    queryDeveloperPage
};
