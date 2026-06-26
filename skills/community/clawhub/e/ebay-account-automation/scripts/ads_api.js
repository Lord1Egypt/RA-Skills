/**
 * ADS Power Local API 封装
 * 文档: https://localapi-doc-zh.adspower.net/
 */

const axios = require('axios');
const config = require('./config');

const BASE_URL = config.ADS_API_BASE;

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'API-KEY': config.ADS_API_KEY,
  },
});

class ExceedingDailyLimit extends Error {
  constructor(message, waitSeconds) {
    super(message);
    this.name = 'ExceedingDailyLimit';
    this.waitSeconds = waitSeconds || 8 * 3600;
  }
}

async function getAllUsers(page = 1, pageSize = 100, groupName = null) {
  const params = { page, page_size: pageSize };
  if (groupName) params.group_name = groupName;

  let groupId = null;
  try {
    const groupRes = await api.get('/api/v1/group/list', { params: { group_name: groupName || '' } });
    if (groupRes.data?.data?.list?.length > 0) {
      groupId = groupRes.data.data.list[0].group_id;
    }
  } catch (e) {}

  if (groupId) params.group_id = groupId;

  const res = await api.get('/api/v1/user/list', { params });
  if (res.data?.code === 0) return res.data.data?.list || [];
  throw new Error(`获取账号列表失败: ${JSON.stringify(res.data)}`);
}

async function getAllUsersFull() {
  const allUsers = [];
  let page = 1;
  const pageSize = 100;
  let hasMore = true;

  while (hasMore) {
    console.log(`  正在读取第 ${page} 页账号...`);
    const users = await getAllUsers(page, pageSize);
    console.log(`  第 ${page} 页返回 ${users.length} 个账号`);
    allUsers.push(...users);
    if (users.length < pageSize) hasMore = false;
    else page++;
  }

  return allUsers;
}

async function startBrowser(userId, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`  [尝试 ${attempt}/${maxRetries}] 启动浏览器 user_id=${userId}`);
      const res = await api.get('/api/v1/browser/start', {
        params: { user_id: userId, open_tabs: '0', ip_tab: '0' },
      });

      if (res.data?.code === 0) {
        console.log(`  启动成功: debug_port=${res.data.data.debug_port}`);
        return res.data.data;
      }

      const msg = res.data?.msg || '';

      if (msg.includes('Exceeding open daily limit') || res.data?.code === -1) {
        const waitMatch = msg.match(/recovery after (\d+)/);
        const waitHours = waitMatch ? parseInt(waitMatch[1]) : 8;
        throw new ExceedingDailyLimit(
          `ADS Power 当日配额耗尽，需等待 ${waitHours} 小时后恢复`,
          waitHours * 3600
        );
      }

      if (msg.includes('updating') || msg.includes('downloading')) {
        console.log(`  浏览器正在更新，等待 15 秒后重试...`);
        await new Promise(r => setTimeout(r, 15000));
        continue;
      }

      throw new Error(`启动失败 [${userId}]: ${JSON.stringify(res.data)}`);

    } catch (e) {
      if (e instanceof ExceedingDailyLimit) throw e;
      console.warn(`  启动出错，5 秒后重试: ${e.message}`);
      if (attempt < maxRetries) await new Promise(r => setTimeout(r, 5000));
    }
  }
  throw new Error(`启动失败 [${userId}]: 已达到最大重试次数`);
}

async function stopBrowser(userId) {
  try {
    const res = await api.get('/api/v1/browser/stop', { params: { user_id: userId } });
    if (res.data?.code === 0) {
      console.log(`  浏览器已关闭 [${userId}]`);
    } else {
      const msg = res.data?.msg || '';
      if (msg.includes('not open') || msg.includes('not running') || msg.includes('not found')) {
        console.log(`  浏览器未在运行，跳过关闭 [${userId}]`);
      } else {
        console.warn(`  关闭浏览器返回异常 [${userId}]: ${msg}`);
      }
    }
  } catch (e) {
    console.warn(`  关闭浏览器请求失败 [${userId}]: ${e.message}`);
  }
}

async function checkBrowserStatus() {
  const res = await api.get('/api/v1/browser/active-list');
  if (res.data?.code === 0) return res.data.data || [];
  return [];
}

async function getUserInfo(userId) {
  const res = await api.get('/api/v1/user/list', { params: { user_id: userId } });
  if (res.data?.code === 0 && res.data?.data?.list?.length > 0) {
    return res.data.data.list[0];
  }
  return null;
}

module.exports = { startBrowser, stopBrowser, getAllUsers, getAllUsersFull, checkBrowserStatus, getUserInfo, ExceedingDailyLimit };
