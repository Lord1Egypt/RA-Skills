import 'dotenv/config';
import crypto from 'crypto';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

// 环境配置
const ENVIRONMENTS = {
  dev: 'https://dev.byteplan.com',
  uat: 'https://uatapp.byteplan.com',
};

const BASIC_AUTH = 'Basic UEM6bkxDbndkSWhpeldieWtIeXVaTTZUcFFEZDdLd0s5SVhESzhMR3NhN1NPVw==';

// 当前环境
let currentEnv = process.env.BP_ENV || 'dev';

/**
 * 获取 .env 文件路径
 * @returns {string}
 */
function getEnvPath() {
  // 优先使用调用方的 .env（当前工作目录），其次使用项目根目录
  const cwd = process.cwd();
  const projectEnvPath = path.join(cwd, '.env');
  if (fs.existsSync(projectEnvPath)) {
    return projectEnvPath;
  }
  // 回退到 skill 目录的 .env
  return path.join(getDirname(), '..', '..', '.env');
}

/**
 * 读取 .env 文件内容
 * @returns {string}
 */
function readEnvContent() {
  const envPath = getEnvPath();
  if (fs.existsSync(envPath)) {
    return fs.readFileSync(envPath, 'utf-8');
  }
  return '';
}

/**
 * 保存凭证到 .env 文件
 * @param {Object} credentials - 凭证对象
 * @param {string} credentials.username - 用户名
 * @param {string} credentials.password - 密码
 * @param {string} credentials.access_token - 访问令牌
 * @param {string} credentials.refresh_token - 刷新令牌
 * @param {number} credentials.expires_in - 过期时间（秒）
 */
function saveCredentials(credentials) {
  const { username, password, access_token, refresh_token, expires_in } = credentials;

  // 读取现有 .env 内容
  let envContent = readEnvContent();
  const lines = envContent.split('\n');

  // 需要更新的配置项（每次登录都更新）
  const keysToUpdate = ['BP_ENV', 'BP_USER', 'BP_PASSWORD', 'USER_NAME', 'PASSWORD', 'ACCESS_TOKEN', 'REFRESH_TOKEN', 'TOKEN_EXPIRES_IN'];

  // 保留非配置项的行（注释、空行、其他配置）
  const preservedLines = lines.filter(line => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) return true;
    const key = trimmed.split('=')[0]?.trim();
    // 保留不属于 keysToUpdate 的配置
    return !keysToUpdate.includes(key);
  });

  // 构建新的配置内容（总是写入最新值）
  const configLines = [];

  // 写入环境配置
  configLines.push(`BP_ENV=${currentEnv}`);

  // 写入用户名
  configLines.push(`BP_USER=${username}`);

  // 写入密码（用引号包裹以保护特殊字符）
  configLines.push(`BP_PASSWORD="${password}"`);

  // 写入 access_token
  configLines.push(`ACCESS_TOKEN=${access_token}`);

  // 写入 refresh_token
  if (refresh_token) {
    configLines.push(`REFRESH_TOKEN=${refresh_token}`);
  }

  // 写入过期时间
  if (expires_in) {
    configLines.push(`TOKEN_EXPIRES_IN=${Date.now() + expires_in * 1000}`);
  }

  // 合并内容：保留的行 + 新配置
  const finalLines = [...preservedLines, ...configLines];
  const finalContent = finalLines.join('\n');

  // 写入文件
  const envPath = getEnvPath();
  fs.writeFileSync(envPath, finalContent, 'utf-8');
}

/**
 * 检查 token 是否过期
 * @returns {boolean}
 */
function isTokenExpired() {
  const expiresIn = process.env.TOKEN_EXPIRES_IN;
  if (!expiresIn) {
    return true; // 没有过期时间，认为已过期，需要重新登录
  }
  const expiresAt = parseInt(expiresIn, 10);
  // 提前 5 分钟认为过期
  return Date.now() >= expiresAt - 5 * 60 * 1000;
}

/**
 * 设置登录环境
 * @param {'dev' | 'uat'} env - 环境名称
 */
export function setEnvironment(env) {
  if (ENVIRONMENTS[env]) {
    currentEnv = env;
  } else {
    throw new Error(`未知环境: ${env}，支持: dev, uat`);
  }
}

/**
 * 获取当前环境
 * @returns {string}
 */
export function getEnvironment() {
  return currentEnv;
}

/**
 * 获取当前环境的基础 URL
 * @returns {string}
 */
export function getBaseUrl() {
  return ENVIRONMENTS[currentEnv];
}

/**
 * 获取 RSA 公钥（UAT 环境）
 * @returns {Promise<{key: string, id: string}>}
 */
async function getPublicKey() {
  const baseUrl = getBaseUrl();
  const response = await fetch(`${baseUrl}/base/util/get/publicKey?t=${Date.now()}`, {
    method: 'GET',
    headers: {
      'accept': 'application/json',
    },
  });

  const data = await response.json();

  // 兼容多种响应格式
  const key = data.data || data.publicKey || data.key || '';
  const id = data.publicKeyId || data.id || '';

  return { key, id };
}

/**
 * RSA 加密密码（UAT 环境）
 * @param {string} password - 明文密码
 * @param {string} publicKey - RSA 公钥
 * @returns {string} - Base64 编码的加密密码
 */
function encryptPassword(password, publicKey) {
  if (!publicKey) {
    throw new Error('公钥为空，无法加密密码');
  }

  // 清理公钥格式
  let cleanKey = publicKey
    .replace(/-----BEGIN PUBLIC KEY-----/g, '')
    .replace(/-----END PUBLIC KEY-----/g, '')
    .replace(/\s/g, '');

  // 格式化为 PEM
  const formattedKeyBody = cleanKey.match(/.{1,64}/g)?.join('\n') || cleanKey;
  const formattedKey = `-----BEGIN PUBLIC KEY-----\n${formattedKeyBody}\n-----END PUBLIC KEY-----`;

  // RSA 加密
  const encrypted = crypto.publicEncrypt(
    {
      key: formattedKey,
      padding: crypto.constants.RSA_PKCS1_PADDING,
    },
    Buffer.from(password, 'utf-8'),
  );

  return encrypted.toString('base64');
}

/**
 * 登录获取 token
 * @param {string} username - 用户名（手机号）
 * @param {string} password - 密码
 * @param {'dev' | 'uat'} [env] - 环境，默认为当前环境
 * @returns {Promise<{access_token: string, refresh_token: string, expires_in: number}>}
 */
export async function login(username, password, env) {
  // 如果指定了环境，使用指定环境
  if (env && ENVIRONMENTS[env]) {
    setEnvironment(env);
  }

  const baseUrl = getBaseUrl();
  const t = Date.now();
  const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);

  let bodyParts = [
    `--${boundary}`,
    'Content-Disposition: form-data; name="scope"',
    '',
    'read write',
    `--${boundary}`,
    'Content-Disposition: form-data; name="grant_type"',
    '',
    'password',
    `--${boundary}`,
    'Content-Disposition: form-data; name="username"',
    '',
    `+86${username}`,
  ];

  if (currentEnv === 'uat') {
    // UAT 环境：获取公钥并加密密码
    const { key: publicKey, id: publicKeyId } = await getPublicKey();
    const encryptedPassword = encryptPassword(password, publicKey);

    bodyParts.push(
      `--${boundary}`,
      `Content-Disposition: form-data; name="publicKeyId"`,
      '',
      publicKeyId,
    );
    bodyParts.push(
      `--${boundary}`,
      'Content-Disposition: form-data; name="password"',
      '',
      encryptedPassword,
    );
  } else {
    // DEV 环境：明文密码
    bodyParts.push(
      `--${boundary}`,
      'Content-Disposition: form-data; name="password"',
      '',
      password,
    );
  }

  bodyParts.push(`--${boundary}--`);

  const response = await fetch(`${baseUrl}/base/login?t=${t}`, {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'authorization': BASIC_AUTH,
      'content-type': `multipart/form-data; boundary=${boundary}`,
    },
    body: bodyParts.join('\r\n'),
  });

  const data = await response.json();

  if (data.error) {
    throw new Error(`登录失败: ${data.message || data.error_description || JSON.stringify(data)}`);
  }

  // 保存凭证到 .env
  try {
    saveCredentials({
      username,
      password,
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_in: data.expires_in
    });
  } catch (e) {
    console.warn(`⚠️  Token 持久化失败: ${e.message}`);
  }

  return data;
}

/**
 * 使用 .env 中的账号密码登录
 * @param {'dev' | 'uat'} [env] - 环境
 * @param {boolean} [forceReLogin=false] - 是否强制重新登录
 * @returns {Promise<{access_token: string, refresh_token: string, expires_in: number}>}
 */
export async function loginWithEnv(env, forceReLogin = false) {
  const username = process.env.BP_USER || process.env.USER_NAME;
  const password = process.env.BP_PASSWORD || process.env.PASSWORD;

  if (!username || !password) {
    throw new Error('请在 .env 中配置 BP_USER 和 BP_PASSWORD（或 USER_NAME 和 PASSWORD）');
  }

  // 如果指定了环境，使用指定环境；否则从 .env 读取
  if (env && ENVIRONMENTS[env]) {
    setEnvironment(env);
  } else if (process.env.BP_ENV && ENVIRONMENTS[process.env.BP_ENV]) {
    setEnvironment(process.env.BP_ENV);
  }

  // 如果没有强制重新登录，先检查是否有可用的缓存 token
  if (!forceReLogin) {
    const cachedToken = process.env.ACCESS_TOKEN;
    if (cachedToken && !isTokenExpired()) {
      return {
        access_token: cachedToken,
        refresh_token: process.env.REFRESH_TOKEN || null,
        expires_in: null,
        _cached: true  // 标记为缓存的 token
      };
    }
  }

  // 缓存无效，重新登录
  return login(username, password);
}

/**
 * 获取当前 token
 * @returns {string|null}
 */
export function getToken() {
  return process.env.ACCESS_TOKEN || null;
}

/**
 * 获取用户信息
 * @param {string} token - access token
 * @returns {Promise<{user: object, tenantList: array}>}
 */
export async function getUserInfo(token) {
  const baseUrl = getBaseUrl();
  const t = Date.now();
  const response = await fetch(`${baseUrl}/base/api/home?pageAuthFlag=true&t=${t}`, {
    method: 'GET',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
    },
  });

  return response.json();
}

/**
 * 切换租户
 * @param {string} token - access token
 * @param {string} tenantId - 租户ID
 * @returns {Promise<object>}
 */
export async function switchTenant(token, tenantId) {
  const baseUrl = getBaseUrl();
  const t = Date.now();
  const response = await fetch(`${baseUrl}/base/api/user/tenant/switch?enabled=1&tenantId=${tenantId}&t=${t}`, {
    method: 'PUT',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
    },
  });

  return response.json();
}

/**
 * 默认 menu headers（AI_REPORT 菜单配置）
 */
const DEFAULT_MENU_HEADERS = {
  'x-menu-code': 'AI_REPORT',
  'x-menu-id': '2008425412219936770',
  'x-menu-params': 'null',
  'x-page-code': 'ai_report',
};

/**
 * 查询模型列表
 * @param {string} token - access token
 * @param {object} options - 可选参数
 * @param {number} options.page - 页码，默认 0
 * @param {number} options.size - 每页数量，默认 100
 * @param {object} options.menuHeaders - 自定义 menu headers
 * @returns {Promise<array>}
 */
export async function queryModels(token, options = {}) {
  const { page = 0, size = 100, menuHeaders = {} } = options;
  const baseUrl = getBaseUrl();

  const headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': `Bearer ${token}`,
    ...DEFAULT_MENU_HEADERS,
    ...menuHeaders,
  };

  const response = await fetch(`${baseUrl}/data/api/model/query?page=${page}&size=${size}`, {
    method: 'GET',
    headers,
  });

  return response.json();
}

/**
 * 根据模型编码查询模型数据
 * @param {string} token - access token
 * @param {string} modelCode - 模型编码
 * @param {Object} params - 查询参数
 * @param {Object} params.customQuery - 自定义查询条件
 * @param {string[]} params.groupFields - 分组字段
 * @param {Array} params.functions - 聚合函数
 * @param {object} options - 可选配置
 * @param {object} options.menuHeaders - 自定义 menu headers
 * @returns {Promise<any>}
 */
export async function getModelData(token, modelCode, params = {}, options = {}) {
  const { customQuery, groupFields, functions } = params;
  const { menuHeaders = {} } = options;
  const baseUrl = getBaseUrl();

  const headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': `Bearer ${token}`,
    'content-type': 'application/json',
    ...DEFAULT_MENU_HEADERS,
    ...menuHeaders,
  };

  const body = {
    modelCode,
    params: {},
  };

  if (customQuery) {
    body.params.customQuery = customQuery;
  }

  if (groupFields && groupFields.length > 0) {
    body.params.groupFields = groupFields;
  }

  if (functions && functions.length > 0) {
    body.params.functions = functions;
  }

  const response = await fetch(`${baseUrl}/foresight/api/bi/multdim/anls/ai/query`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  return response.json();
}

/**
 * 获取模型字段详情
 * @param {string} token - access token
 * @param {string[]} modelCodes - 模型编码数组
 * @returns {Promise<Object>}
 */
export async function getModelColumns(token, modelCodes) {
  const baseUrl = getBaseUrl();
  const response = await fetch(`${baseUrl}/data/api/model/col/get/model/col/by/codes`, {
    method: 'POST',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
      'content-type': 'application/json',
      ...DEFAULT_MENU_HEADERS,
    },
    body: JSON.stringify(modelCodes),
  });

  return response.json();
}

/**
 * 获取维度值列表
 * @param {string} token - access token
 * @param {string} dimCode - 维度代码
 * @param {Object} options - 可选参数
 * @returns {Promise<Array>}
 */
export async function getDimValues(token, dimCode, options = {}) {
  const { modelCode, colName, page = 0, size = 100, keywords = null } = options;
  const baseUrl = getBaseUrl();

  const response = await fetch(`${baseUrl}/data/api/online/lov/DATA_DIM_VALUE_LOV?dimCode=${dimCode}&page=${page}&size=${size}`, {
    method: 'POST',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      dimCode,
      keywords,
      page,
      size,
      modelCode: modelCode || '',
      colName: colName || '',
      filterMap: {},
      writeOnly: false,
    }),
  });

  return response.json();
}

/**
 * 获取列表值（LIST类型字段的可选值）
 * @param {string} token - access token
 * @param {string} listCode - 列表代码
 * @param {Object} options - 可选参数
 * @returns {Promise<Array>}
 */
export async function getListValues(token, listCode, options = {}) {
  const { modelCode, colName, page = 0, size = 999 } = options;
  const baseUrl = getBaseUrl();

  const response = await fetch(`${baseUrl}/data/api/permission/dimension/query`, {
    method: 'POST',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      total: false,
      page,
      size,
      dimensionType: 'LIST',
      modelColName: colName,
      dimensionCode: listCode,
      modelCode,
      filterMap: {},
      writeOnly: false,
    }),
  });

  return response.json();
}

/**
 * 获取LOV值（LOV类型字段的可选值）
 * @param {string} token - access token
 * @param {string} lovCode - LOV代码
 * @param {Object} options - 可选参数
 * @returns {Promise<Array>}
 */
export async function getLovValues(token, lovCode, options = {}) {
  const { modelCode, colName, page = 0, size = 100, keywords = null } = options;
  const baseUrl = getBaseUrl();

  const response = await fetch(`${baseUrl}/data/api/online/lov/${lovCode}?page=${page}&size=${size}`, {
    method: 'POST',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      keywords,
      page,
      size,
      modelCode: modelCode || '',
      colName: colName || '',
      filterMap: {},
      writeOnly: false,
    }),
  });

  return response.json();
}

/**
 * 获取层级值（LEVEL类型字段的可选值）
 * @param {string} token - access token
 * @param {string} levelCode - 层级代码
 * @param {Object} options - 可选参数
 * @returns {Promise<Array>}
 */
export async function getLevelValues(token, levelCode, options = {}) {
  const { modelCode, colName, page = 0, size = 999 } = options;
  const baseUrl = getBaseUrl();

  const response = await fetch(`${baseUrl}/data/api/permission/dimension/query`, {
    method: 'POST',
    headers: {
      'accept': 'application/json, text/plain, */*',
      'authorization': `Bearer ${token}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      total: false,
      page,
      size,
      dimensionType: 'DIM_HIERARCHY',
      modelColName: colName,
      dimensionCode: levelCode,
      modelCode,
      filterMap: {},
      writeOnly: false,
    }),
  });

  return response.json();
}

/**
 * 获取 api.js 的绝对路径（供其他 skill 引用）
 * @returns {string}
 */
export function getApiPath() {
  return path.resolve(getDirname(), 'api.js');
}

/**
 * 获取当前模块所在目录
 */
function getDirname() {
  try {
    return path.dirname(fileURLToPath(import.meta.url));
  } catch {
    return path.dirname(new URL(import.meta.url).pathname);
  }
}

// 导出 DEFAULT_MENU_HEADERS 供外部使用
export { DEFAULT_MENU_HEADERS };
