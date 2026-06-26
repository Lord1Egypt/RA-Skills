// scripts/main.js

const DEFAULTS = {
  startMg: 0,
  endMg: 10,
  locationRange: 1,
  orderBy: 'id',
  isAsc: false,
};

const VALID_ORDER_BY = ['id', 'magnitude', 'depth'];
const VALID_LOCATION_RANGE = [1, 2];
const TIMEOUT_MS = 15000;

/**
 * 获取默认起始时间（3天前 00:00:00）
 */
function getDefaultStartTime() {
  const d = new Date();
  d.setDate(d.getDate() - 3);
  return formatDate(d, '00:00:00');
}

/**
 * 获取默认结束时间（今天 23:59:59）
 */
function getDefaultEndTime() {
  return formatDate(new Date(), '23:59:59');
}

/**
 * 格式化日期为 YYYY-MM-DD HH:mm:ss
 */
function formatDate(date, time) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d} ${time}`;
}

/**
 * 校验震级范围
 */
function validateMagnitude(value, name) {
  if (value === undefined || value === null) return undefined;
  const n = Number(value);
  if (isNaN(n)) {
    throw new Error(`参数 ${name} 必须为数字，收到: ${value}`);
  }
  if (n < 0 || n > 10) {
    throw new Error(`参数 ${name} 超出范围 [0, 10]，收到: ${n}`);
  }
  return n;
}

/**
 * 校验枚举值
 */
function validateEnum(value, name, allowed) {
  if (value === undefined || value === null) return undefined;
  if (!allowed.includes(value)) {
    throw new Error(`参数 ${name} 无效，可选值: ${allowed.join(', ')}，收到: ${value}`);
  }
  return value;
}

/**
 * 校验日期字符串格式（宽松校验 YYYY-MM-DD ...）
 */
function validateDateString(value, name) {
  if (!value) return undefined;
  const pattern = /^\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}$/;
  if (!pattern.test(String(value).trim())) {
    throw new Error(`参数 ${name} 格式错误，应为 YYYY-MM-DD HH:mm:ss，收到: ${value}`);
  }
  return String(value).trim();
}

/**
 * 带超时的 fetch 请求
 */
async function fetchWithTimeout(url, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timer);
    return response;
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      throw new Error(`请求超时（${timeoutMs / 1000}s），CENC 服务可能不可用`);
    }
    throw err;
  }
}

/**
 * OpenClaw Skill 入口函数
 * @param {Object} input - 输入参数对象
 * @param {number} [input.startMg=0] - 最小震级，范围 0-10
 * @param {number} [input.endMg=10] - 最大震级，范围 0-10
 * @param {number} [input.locationRange=1] - 位置范围：1=中国范围，2=全球范围
 * @param {string} [input.orderBy='id'] - 排序字段：id（时间）、magnitude（震级）、depth（深度）
 * @param {boolean} [input.isAsc=false] - 是否升序排列
 * @param {string} [input.startTime] - 起始日期，格式 YYYY-MM-DD HH:mm:ss，默认3天前
 * @param {string} [input.endTime] - 结束日期，格式 YYYY-MM-DD HH:mm:ss，默认今天
 * @returns {Promise<Object>} - 包含地震信息的结果对象
 */
async function execute(input = {}) {
  try {
    // 参数校验与清洗
    const startMg = validateMagnitude(input.startMg, 'startMg') ?? DEFAULTS.startMg;
    const endMg = validateMagnitude(input.endMg, 'endMg') ?? DEFAULTS.endMg;
    const locationRange = validateEnum(input.locationRange, 'locationRange', VALID_LOCATION_RANGE) ?? DEFAULTS.locationRange;
    const orderBy = validateEnum(input.orderBy, 'orderBy', VALID_ORDER_BY) ?? DEFAULTS.orderBy;
    const isAsc = input.isAsc === true;
    const startTime = validateDateString(input.startTime, 'startTime') || getDefaultStartTime();
    const endTime = validateDateString(input.endTime, 'endTime') || getDefaultEndTime();

    // 震级逻辑校验
    if (startMg > endMg) {
      throw new Error(`startMg(${startMg}) 不应大于 endMg(${endMg})`);
    }

    // 构建请求 URL
    const apiUrl = new URL('https://www.cenc.ac.cn/prodlaunch-web-backend/open/data/catalogs');
    apiUrl.searchParams.append('startMg', startMg);
    apiUrl.searchParams.append('endMg', endMg);
    apiUrl.searchParams.append('locationRange', locationRange);
    apiUrl.searchParams.append('orderBy', orderBy);
    apiUrl.searchParams.append('isAsc', isAsc);
    apiUrl.searchParams.append('startTime', startTime);
    apiUrl.searchParams.append('endTime', endTime);

    // 发送请求
    const response = await fetchWithTimeout(apiUrl.toString(), TIMEOUT_MS);

    if (!response.ok) {
      throw new Error(`CENC API 请求失败: HTTP ${response.status} ${response.statusText}`);
    }

    const result = await response.json();

    // 数据提取
    const earthquakes = Array.isArray(result?.data) ? result.data : [];

    return {
      status: 'success',
      count: earthquakes.length,
      data: earthquakes,
    };

  } catch (error) {
    const msg = error.message || '未知错误';

    // 区分参数错误与网络错误，便于上层判断
    const isParamError = msg.includes('参数') || msg.includes('格式');
    return {
      status: 'error',
      type: isParamError ? 'param_error' : 'request_error',
      message: msg,
    };
  }
}

module.exports = { execute };
