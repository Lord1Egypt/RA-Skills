const crypto = require('crypto');

// ==================== 常量定义 ====================

const CONFIG = {
  TIMEOUT_MS: 15000,          // 请求超时时间 15s
  MAX_PAGE_SIZE: 100,         // 单页最大条数
  DEFAULT_PAGE_SIZE: 10,      // 默认每页条数
  DEFAULT_PAGE: 1,            // 默认页码
  API_URL: 'https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx',
  REFERER: 'https://search.bidcenter.com.cn/',
  USER_AGENT: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  MAX_RETRIES: 2,             // 请求失败最大重试次数
  RETRY_DELAY_MS: 1000,       // 重试间隔
};

// 地区编码映射
const REGION_MAP = {
  '全国': 0, '山西': 4, '北京': 1, '天津': 2, '河北': 3,
  '内蒙古': 5, '辽宁': 6, '吉林': 7, '黑龙江': 8, '上海': 9,
  '江苏': 10, '浙江': 11, '安徽': 12, '福建': 13, '江西': 14,
  '山东': 15, '河南': 16, '湖北': 17, '湖南': 18, '广东': 19,
  '广西': 20, '海南': 21, '重庆': 22, '贵州': 24, '四川': 23,
  '云南': 25, '西藏': 26, '陕西': 27, '甘肃': 28, '青海': 29,
  '宁夏': 30, '新疆': 31, '台湾': 32, '香港': 33, '澳门': 34,
  '跨省': 99,
};

// 信息类型映射
const TYPE_MAP = {
  '全部': '', '招标公告': 1, '标书下载': 8, '中标结果': 4,
  '招标预告': 2, '招标变更': 6, 'VIP独家': 12, '拟在建项目': 3,
  '参考项目': 90, '土地挂牌': 32, '审批公示': 17, '拍卖转让': 9,
};

// 时间范围映射
const TIME_MAP = {
  '全部': '', '近三天': 3, '近一周': 7, '近一月': 30,
  '近三月': 90, '近半年': 180, '近一年': 11,
};

// ==================== 工具函数 ====================

/**
 * 延迟函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 带超时的 fetch 请求
 */
async function fetchWithTimeout(url, options, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timer);

    if (!response.ok) {
      throw new Error(`HTTP 请求失败，状态码: ${response.status}`);
    }
    return response;
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      throw new Error(`请求超时（${timeoutMs / 1000}s），采招网服务可能不可用`);
    }
    throw err;
  }
}

/**
 * AES-128-CBC 解密（兼容 CryptoJS 格式）
 */
function decrypt(str) {
  if (!str || typeof str !== 'string') {
    return null;
  }

  function wordsToBuffer(words) {
    const buf = Buffer.alloc(words.length * 4);
    for (let i = 0; i < words.length; i++) {
      buf.writeInt32BE(words[i], i * 4);
    }
    return buf;
  }

  const keyWords = [863652730, 2036741733, 1164342596, 1782662963];
  const ivWords = [1719227713, 1314533489, 1397643880, 1749959510];
  const key = wordsToBuffer(keyWords);
  const iv = wordsToBuffer(ivWords);

  try {
    const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
    decipher.setAutoPadding(false);

    let decrypted = decipher.update(str, 'base64', 'utf8');
    decrypted += decipher.final('utf8');

    // 去除 ZeroPadding 产生的 \u0000
    decrypted = decrypted.replace(/\0+$/, '');

    if (!decrypted || decrypted.trim() === '') {
      return null;
    }

    return JSON.parse(decrypted);
  } catch (err) {
    console.error('解密失败:', err.message);
    return null;
  }
}

/**
 * 参数解析与规范化
 * 支持中文别名和数字编码两种输入方式
 */
function normalizeInput(input = {}) {
  const result = {};

  // 地区：支持中文名称或数字编码
  if (input.diqu !== undefined && input.diqu !== '') {
    if (typeof input.diqu === 'string' && REGION_MAP.hasOwnProperty(input.diqu)) {
      result.diqu = REGION_MAP[input.diqu];
    } else {
      const num = Number(input.diqu);
      result.diqu = isNaN(num) ? 0 : num;
    }
  } else {
    result.diqu = 0;
  }

  // 信息类型：支持中文名称或数字编码
  if (input.type !== undefined && input.type !== '') {
    if (typeof input.type === 'string' && TYPE_MAP.hasOwnProperty(input.type)) {
      result.type = String(TYPE_MAP[input.type]);
    } else {
      result.type = String(input.type);
    }
  } else {
    result.type = '';
  }

  // 时间范围：支持中文别名或数字编码
  if (input.time !== undefined && input.time !== '') {
    if (typeof input.time === 'string' && TIME_MAP.hasOwnProperty(input.time)) {
      result.time = String(TIME_MAP[input.time]);
    } else {
      result.time = String(input.time);
    }
  } else {
    result.time = '';
  }

  // 关键词：必填
  const kw = (input.keyword !== undefined && input.keyword !== null)
    ? String(input.keyword).trim()
    : '';
  if (!kw) {
    throw new Error('keyword 为必填参数，请提供搜索关键词');
  }
  result.keyword = kw;

  // 页码：确保为正整数
  const page = Number(input.page);
  result.page = Number.isInteger(page) && page > 0 ? page : CONFIG.DEFAULT_PAGE;

  // 每页条数：限制范围 [1, MAX_PAGE_SIZE]
  const pageSize = Number(input.pageSize);
  if (!Number.isInteger(pageSize) || pageSize <= 0) {
    result.pageSize = CONFIG.DEFAULT_PAGE_SIZE;
  } else if (pageSize > CONFIG.MAX_PAGE_SIZE) {
    result.pageSize = CONFIG.MAX_PAGE_SIZE;
  } else {
    result.pageSize = pageSize;
  }

  return result;
}

/**
 * 构建请求体，空值字段不传入
 */
function buildRequestBody(params) {
  return Object.keys(params)
    .filter(key => params[key] !== '' && params[key] !== null && params[key] !== undefined)
    .map(key => `${key}=${encodeURIComponent(params[key])}`)
    .join('&');
}

/**
 * 格式化单条招标信息
 * 适配采招网接口实际字段名
 */
function formatItem(item) {
  if (!item || typeof item !== 'object') return null;

  return {
    id: item.news_id || '',
    title: item.news_title_show || '无标题',
    type: item.news_type_des || '',
    url: item.news_url ? `https:${item.news_url}` : '',
    publishDate: item.news_star_time_show || '',
    endDate: item.news_end_time_show || '',
    location: item.news_diqustr || '',
    budget: item.news_zbje_show || '',
    winAmount: item.news_zhongbiaojine_show || '',
    projectValue: item.news_gczj_show || '',
    stage: item.news_jieduan_show || '',
    purchaseMethod: item.news_cgfs || '',
    isProject: item.is_xiangmu || false,
  };
}

// ==================== 主函数 ====================

/**
 * 查询采招网招标信息
 *
 * @param {Object} input - 查询参数
 * @param {string} input.keyword - 搜索关键词（必填）
 * @param {string|number} [input.diqu=0] - 地区：支持中文名(如"北京")或数字编码(如1)，默认全国(0)
 * @param {string|number} [input.type] - 信息类型：支持中文名(如"招标公告")或数字编码(如1)，不传表示全部
 * @param {string|number} [input.time] - 时间范围：支持中文(如"近一周")或数字编码(如7)，不传表示全部
 * @param {number} [input.page=1] - 页码，默认1
 * @param {number} [input.pageSize=10] - 每页数量，默认10，最大100
 * @returns {Promise<Object>} - { status, listData, total, page, pageSize, message? }
 */
async function execute(input = {}) {
  // 1. 参数规范化
  let norm;
  try {
    norm = normalizeInput(input);
  } catch (err) {
    return {
      status: 'error',
      message: err.message,
      listData: [],
      total: 0,
    };
  }

  // 2. 构建请求参数
  const params = {
    from: '6137',
    location: '6138',
    mod: '1',
    deftag: '1',
    diqu: norm.diqu,
    keywords: norm.keyword,
    type: norm.type,
    time: norm.time,
    page: norm.page,
    pageSize: norm.pageSize,
    guid: crypto.randomBytes(16).toString('hex'),
  };

  const options = {
    headers: {
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Referer': CONFIG.REFERER,
      'user-agent': CONFIG.USER_AGENT,
    },
    body: buildRequestBody(params),
    method: 'POST',
  };

  // 3. 带重试的请求
  let lastError = null;
  let text = '';

  for (let attempt = 0; attempt <= CONFIG.MAX_RETRIES; attempt++) {
    try {
      if (attempt > 0) {
        console.log(`第 ${attempt} 次重试...`);
        await sleep(CONFIG.RETRY_DELAY_MS * attempt);
      }

      const response = await fetchWithTimeout(CONFIG.API_URL, options, CONFIG.TIMEOUT_MS);
      text = await response.text();

      if (!text || text.trim() === '') {
        throw new Error('接口返回空内容');
      }

      // 请求成功，跳出重试循环
      break;
    } catch (err) {
      lastError = err;
      if (attempt === CONFIG.MAX_RETRIES) {
        return {
          status: 'error',
          message: `请求失败（已重试 ${CONFIG.MAX_RETRIES} 次）: ${err.message}`,
          listData: [],
          total: 0,
          page: norm.page,
          pageSize: norm.pageSize,
        };
      }
    }
  }

  // 4. 解密响应
  const result = decrypt(text);
  if (!result) {
    return {
      status: 'error',
      message: '响应解密失败，数据格式异常',
      listData: [],
      total: 0,
      page: norm.page,
      pageSize: norm.pageSize,
    };
  }

  // 5. 提取并格式化数据
  const rawList = result?.other2?.listData;
  const total = result?.other2?.realInfoCount || 0;

  if (!Array.isArray(rawList)) {
    return {
      status: 'success',
      listData: [],
      total: 0,
      page: norm.page,
      pageSize: norm.pageSize,
      message: total === 0 ? '未找到符合条件的招标信息' : '返回数据格式异常',
    };
  }

  const listData = rawList.map(formatItem).filter(Boolean);

  return {
    status: 'success',
    listData,
    total,
    page: norm.page,
    pageSize: norm.pageSize,
  };
}

module.exports = { execute };
