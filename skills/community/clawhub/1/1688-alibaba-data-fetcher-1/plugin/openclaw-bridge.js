// ============================================================
// OpenClaw Bridge - 1688 Data Claw 调用桥接脚本
// 用于 OpenClaw 或其他外部脚本与插件交互
// ============================================================

/**
 * 1688DataClawBridge - OpenClaw 调用类
 * 
 * 使用方法:
 * 1. 确保 1688 Data Claw 扩展已安装并启用
 * 2. 在浏览器控制台或其他脚本中引入此文件
 * 3. 创建实例并调用API
 * 
 * 示例:
 * const claw = new Claw1688Bridge();
 * const data = await claw.getFullData(50);
 * console.log(data);
 */
class Claw1688Bridge {
  constructor(extensionId = null) {
    // 如果未指定，尝试从已知ID推断
    this.extensionId = extensionId || this._detectExtensionId();
    this.debug = true;
  }

  log(...args) {
    if (this.debug) console.log('[OpenClaw-Bridge]', ...args);
  }

  _detectExtensionId() {
    // 在Chrome扩展环境中，可以通过以下方式获取
    // 实际使用时需要在安装后手动填入
    // 或在popup中查看扩展ID
    return null;
  }

  // 检查扩展是否可用
  async ping() {
    return new Promise((resolve) => {
      if (!this.extensionId) {
        resolve({ success: false, error: '未设置扩展ID' });
        return;
      }
      
      chrome.runtime.sendMessage(this.extensionId, { action: 'GET_VERSION' }, (response) => {
        if (chrome.runtime.lastError) {
          resolve({ success: false, error: chrome.runtime.lastError.message });
        } else {
          resolve(response || { success: false, error: '无响应' });
        }
      });
    });
  }

  // 获取完整数据
  async getFullData(limit = 50) {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'full', limit });
  }

  // 获取列表商品数据
  async getItems(keyword = null, limit = 50) {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'items', keyword, limit });
  }

  // 获取详情数据
  async getDetails(offerId = null, limit = 50) {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'details', offerId, limit });
  }

  // 获取数据汇总
  async getSummary() {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'summary' });
  }

  // 获取生意参谋数据
  async getSycm(limit = 50) {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'sycm', limit });
  }

  // 获取工作台数据
  async getWork(limit = 50) {
    return this._sendMessage({ action: 'OPEN_CLAW_API', mode: 'work', limit });
  }

  // 获取原始数据存储
  async getRawData() {
    return this._sendMessage({ action: 'GET_ALL_DATA' });
  }

  // 通用消息发送
  _sendMessage(request) {
    return new Promise((resolve) => {
      if (!this.extensionId) {
        resolve({ success: false, error: '未设置扩展ID。请从popup中查看扩展ID并传入构造函数。' });
        return;
      }

      chrome.runtime.sendMessage(this.extensionId, request, (response) => {
        if (chrome.runtime.lastError) {
          this.log('通信错误:', chrome.runtime.lastError.message);
          resolve({ success: false, error: chrome.runtime.lastError.message });
        } else {
          resolve(response || { success: false, error: '无响应' });
        }
      });
    });
  }

  // 设置扩展ID
  setExtensionId(id) {
    this.extensionId = id;
    this.log('扩展ID已设置:', id);
  }
}

// ============================================================
// 便捷函数 - 供OpenClaw直接调用
// ============================================================

let _defaultBridge = null;

function getDefaultBridge() {
  if (!_defaultBridge) {
    _defaultBridge = new Claw1688Bridge();
  }
  return _defaultBridge;
}

// 设置默认桥接器的扩展ID
function setClawExtensionId(id) {
  getDefaultBridge().setExtensionId(id);
}

// 获取列表商品
async function clawItems(keyword, limit) {
  return getDefaultBridge().getItems(keyword, limit);
}

// 获取详情
async function clawDetails(offerId, limit) {
  return getDefaultBridge().getDetails(offerId, limit);
}

// 获取汇总
async function clawSummary() {
  return getDefaultBridge().getSummary();
}

// 获取全部
async function clawAll(limit) {
  return getDefaultBridge().getFullData(limit);
}

// 获取生意参谋数据
async function clawSycm(limit) {
  return getDefaultBridge().getSycm(limit);
}

// 获取工作台数据
async function clawWork(limit) {
  return getDefaultBridge().getWork(limit);
}

// 获取原始数据
async function clawRaw() {
  return getDefaultBridge().getRawData();
}

// ============================================================
// 导出 (支持 ES Module / CommonJS / 浏览器全局)
// ============================================================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Claw1688Bridge, setClawExtensionId, clawItems, clawDetails, clawSummary, clawAll, clawSycm, clawWork, clawRaw };
} else if (typeof window !== 'undefined') {
  window.Claw1688Bridge = Claw1688Bridge;
  window.setClawExtensionId = setClawExtensionId;
  window.clawItems = clawItems;
  window.clawDetails = clawDetails;
  window.clawSummary = clawSummary;
  window.clawAll = clawAll;
  window.clawSycm = clawSycm;
  window.clawWork = clawWork;
  window.clawRaw = clawRaw;
}
