// ============================================================
// 1688 Data Claw - Background Service Worker
// 数据汇总、存储管理、OpenClaw API接口
// ============================================================

const CLAW_VERSION = '1.0.0';
const DEBUG = true;

function log(...args) {
  if (DEBUG) console.log('[1688-Claw-BG]', ...args);
}

// --- 存储管理 ---
const Storage = {
  async get(key) {
    try {
      const result = await chrome.storage.local.get(key);
      return result[key];
    } catch (e) {
      log('存储读取失败:', e);
      return undefined;
    }
  },

  async set(key, value) {
    try {
      await chrome.storage.local.set({ [key]: value });
    } catch (e) {
      log('存储写入失败:', e);
    }
  },

  async getDataStore() {
    const raw = await this.get('clawDataStore');
    const defaults = {
      version: CLAW_VERSION,
      createdAt: new Date().toISOString(),
      sycm: [],
      work: [],
      stats: {
        totalSycm: 0,
        totalWork: 0,
        lastUpdate: null
      }
    };
    if (!raw) return defaults;
    // 合并旧数据，确保新字段存在
    return {
      ...defaults,
      ...raw,
      sycm: raw.sycm || [],
      work: raw.work || [],
      stats: { ...defaults.stats, ...(raw.stats || {}) }
    };
  },

  async saveDataStore(store) {
    store.stats.lastUpdate = new Date().toISOString();
    await this.set('clawDataStore', store);
  }
};

// --- 数据处理 ---
const DataProcessor = {
  // 合并生意参谋数据
  async mergeSycmData(newData) {
    const store = await Storage.getDataStore();
    let added = 0;
    let updated = 0;

    const companyName = newData.companyName;
    if (!companyName) {
      log('生意参谋数据缺少companyName，无法合并');
      return { added: 0, updated: 0, total: store.sycm.length };
    }

    const existingIndex = store.sycm.findIndex(s => s.companyName === companyName);
    if (existingIndex >= 0) {
      store.sycm[existingIndex] = { ...store.sycm[existingIndex], ...newData, _updatedAt: new Date().toISOString() };
      updated++;
    } else {
      store.sycm.push({ ...newData, _addedAt: new Date().toISOString() });
      added++;
    }

    store.stats.totalSycm = store.sycm.length;
    await Storage.saveDataStore(store);
    log(`生意参谋数据合并完成: 新增${added}, 更新${updated}`);
    return { added, updated, total: store.sycm.length };
  },

  // 合并工作台数据
  async mergeWorkData(newData) {
    const store = await Storage.getDataStore();
    let added = 0;
    let updated = 0;

    // 优先使用 accountId（从cookie提取的稳定账号标识）去重，同账号切换页面不会重复
    const accountId = newData.accountId;
    if (!accountId) {
      log('工作台数据缺少accountId，无法合并');
      return { added: 0, updated: 0, total: store.work.length };
    }

    const existingIndex = store.work.findIndex(w => w.accountId === accountId);
    if (existingIndex >= 0) {
      store.work[existingIndex] = { ...store.work[existingIndex], ...newData, _updatedAt: new Date().toISOString() };
      updated++;
      log(`工作台数据更新: accountId=${accountId}, url=${newData.url}`);
    } else {
      store.work.push({ ...newData, _addedAt: new Date().toISOString() });
      added++;
    }

    store.stats.totalWork = store.work.length;
    await Storage.saveDataStore(store);
    log(`工作台数据合并完成: 新增${added}, 更新${updated}, 共${store.work.length}条（按账号去重）`);
    return { added, updated, total: store.work.length };
  },

  // 获取汇总数据
  async getSummary() {
    const store = await Storage.getDataStore();
    return {
      version: store.version,
      createdAt: store.createdAt,
      stats: store.stats,
      sycmCount: store.sycm.length,
      workCount: store.work.length,
      sycmCompanies: [...new Set(store.sycm.map(s => s.companyName).filter(Boolean))]
    };
  },

};

// --- 消息处理 ---
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  (async () => {
    try {
      switch (request.action) {
        case 'CLAW_DATA': {
          // 来自content script的数据
          const data = request.data;
          if (!data) {
            sendResponse({ success: false, error: 'No data' });
            return;
          }

          log('收到采集数据:', data._pageType, data.offerId || data.items?.length || data.companyName);

          let result;
          if (data._pageType === 'sycm') {
            result = await DataProcessor.mergeSycmData(data);
          } else if (data._pageType === 'work') {
            result = await DataProcessor.mergeWorkData(data);
          }

          sendResponse({ success: true, result });
          break;
        }

        case 'GET_SUMMARY': {
          const summary = await DataProcessor.getSummary();
          sendResponse({ success: true, summary });
          break;
        }

        case 'CLEAR_DATA': {
          const emptyStore = {
            version: CLAW_VERSION,
            createdAt: new Date().toISOString(),
            sycm: [],
            work: [],
            stats: { totalSycm: 0, totalWork: 0, lastUpdate: null }
          };
          await Storage.saveDataStore(emptyStore);
          sendResponse({ success: true });
          break;
        }

        case 'TRIGGER_CLAW_CONTENT': {
          // 向当前活动标签页发送采集命令
          const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
          if (tab && tab.id) {
            chrome.tabs.sendMessage(tab.id, { action: 'TRIGGER_CLAW' }, (resp) => {
              sendResponse({ success: true, tabResponse: resp });
            });
            return true; // 保持消息通道开放
          } else {
            sendResponse({ success: false, error: 'No active tab' });
          }
          break;
        }

        case 'OPEN_CLAW_API': {
          // OpenClaw 专用接口 - 获取结构化的商品数据
          const store = await Storage.getDataStore();
          const { mode = 'full', offerId, limit = 50 } = request;

          let responseData = {};

          if (mode === 'full') {
            responseData = {
              sycm: store.sycm.slice(0, limit),
              work: store.work.slice(0, limit),
              stats: store.stats
            };
          } else if (mode === 'sycm') {
            responseData = { sycm: store.sycm.slice(0, limit) };
          } else if (mode === 'work') {
            responseData = { work: store.work.slice(0, limit) };
          } else if (mode === 'summary') {
            responseData = await DataProcessor.getSummary();
          }

          sendResponse({
            success: true,
            clawVersion: CLAW_VERSION,
            data: responseData
          });
          break;
        }

        default:
          sendResponse({ success: false, error: 'Unknown action' });
      }
    } catch (e) {
      log('消息处理错误:', e);
      sendResponse({ success: false, error: e.message });
    }
  })();

  return true; // 保持异步消息通道
});

// --- 外部扩展/API访问 ---
chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
  (async () => {
    log('收到外部消息:', request.action, 'from:', sender.id || sender.origin);

    try {
      switch (request.action) {
        case 'OPEN_CLAW_API': {
          const store = await Storage.getDataStore();
          const { mode = 'full', offerId, limit = 50, keyword } = request;

          let responseData = {};

          if (mode === 'full') {
            responseData = {
              sycm: store.sycm.slice(0, limit),
              work: store.work.slice(0, limit),
              stats: store.stats
            };
          } else if (mode === 'sycm') {
            responseData = { sycm: store.sycm.slice(0, limit) };
          } else if (mode === 'work') {
            responseData = { work: store.work.slice(0, limit) };
          } else if (mode === 'summary') {
            responseData = await DataProcessor.getSummary();
          }

          sendResponse({
            success: true,
            clawVersion: CLAW_VERSION,
            source: '1688-data-claw',
            data: responseData
          });
          break;
        }

        case 'GET_VERSION': {
          sendResponse({
            success: true,
            version: CLAW_VERSION,
            name: '1688 Data Claw',
            description: '1688数据采集器 for OpenClaw'
          });
          break;
        }

        default:
          sendResponse({ success: false, error: 'Unknown external action' });
      }
    } catch (e) {
      log('外部消息处理错误:', e);
      sendResponse({ success: false, error: e.message });
    }
  })();

  return true;
});

// --- 安装/更新事件 ---
chrome.runtime.onInstalled.addListener((details) => {
  log('扩展安装/更新:', details.reason);

  if (details.reason === 'install') {
    // 初始化存储
    Storage.set('clawDataStore', {
      version: CLAW_VERSION,
      createdAt: new Date().toISOString(),
      sycm: [],
      work: [],
      stats: { totalSycm: 0, totalWork: 0, lastUpdate: null }
    });
  }
});

// --- 定期检查 ---
setInterval(async () => {
  const store = await Storage.getDataStore();
  log('定时检查 - 数据状态:', store.stats);
}, 300000); // 5分钟

log('1688 Data Claw 后台服务已启动');
