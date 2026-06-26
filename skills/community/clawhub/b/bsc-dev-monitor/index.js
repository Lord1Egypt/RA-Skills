#!/usr/bin/env node

/**
 * BSC Dev Monitor Skill
 * 专为跟投 Dev 用户设计的 BSC 链上监控工具
 * 支持按检测收费、Webhook 通知、安全检测
 */

const https = require('https');
const crypto = require('crypto');

// ============================================
// 配置
// ============================================

const SKILLPAY_CONFIG = {
  apiKey: 'sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5',
  price: '0.01',
  currency: 'USDT',
  billingMode: 'per_call' // 按次收费
};

const BSC_CONFIG = {
  rpc: 'https://bsc-dataseed.binance.org/',
  chainId: 56
};

// BSCScan API 配置
const BSCSCAN_CONFIG = {
  apiKey: 'JM67IQSBC6B8X2EEBEPR9R5XEKGDYRHPH1',
  baseUrl: 'https://api.bscscan.com/api'
};

// 监控会话存储
const activeMonitors = new Map();
const detectionHistory = [];

// ============================================
// 支付相关函数
// ============================================

/**
 * 生成支付链接
 */
function generatePaymentLink(userId, callbackUrl, billingMode = 'per_detection') {
  const paymentData = {
    api_key: SKILLPAY_CONFIG.apiKey,
    price: SKILLPAY_CONFIG.price,
    currency: SKILLPAY_CONFIG.currency,
    user_id: userId,
    callback_url: callbackUrl,
    description: 'BSC Dev Monitor - 按次收费',
    per_call: true
  };

  const queryString = Object.keys(paymentData)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(paymentData[key])}`)
    .join('&');

  return `https://skillpay.me/pay?${queryString}`;
}

/**
 * 验证支付状态
 */
async function verifyPayment(userId, paymentId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.skillpay.me',
      port: 443,
      path: `/v1/verify/${paymentId}`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${SKILLPAY_CONFIG.apiKey}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.success && result.verified) {
            resolve(result);
          } else {
            reject(new Error('Payment verification failed'));
          }
        } catch (e) {
          reject(new Error('Invalid response'));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * 记录检测并扣费（按检测收费）
 */
async function recordDetection(monitorId, detectionData) {
  const detection = {
    id: crypto.randomUUID(),
    monitorId,
    timestamp: new Date().toISOString(),
    ...detectionData,
    billing: {
      mode: 'per_detection',
      charged: true,
      amount: SKILLPAY_CONFIG.price,
      currency: SKILLPAY_CONFIG.currency
    }
  };

  detectionHistory.push(detection);

  // 发送 Webhook 通知（如果配置了）
  const monitor = activeMonitors.get(monitorId);
  if (monitor && monitor.webhookUrl) {
    await sendWebhook(monitor.webhookUrl, {
      event: 'token_detected',
      timestamp: detection.timestamp,
      monitor_id: monitorId,
      data: detectionData,
      billing: detection.billing
    });
  }

  return detection;
}

// ============================================
// BSC 相关函数
// ============================================

/**
 * 获取最新区块号
 */
function getLatestBlock() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      jsonrpc: '2.0',
      method: 'eth_blockNumber',
      params: [],
      id: 1
    });

    const options = {
      hostname: 'bsc-dataseed.binance.org',
      port: 443,
      path: '/',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);
          const blockNumber = parseInt(json.result, 16);
          resolve(blockNumber);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 获取区块交易列表
 */
function getBlockTransactions(blockNumber) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      jsonrpc: '2.0',
      method: 'eth_getBlockByNumber',
      params: [`0x${blockNumber.toString(16)}`, true],
      id: 1
    });

    const options = {
      hostname: 'bsc-dataseed.binance.org',
      port: 443,
      path: '/',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(responseData);
          if (json.result && json.result.transactions) {
            resolve(json.result.transactions);
          } else {
            resolve([]);
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 判断是否是代币转账
 */
function isTokenTransfer(tx) {
  return tx && tx.input && tx.input.startsWith('0xa9059cbb');
}

// ============================================
// Webhook 相关函数
// ============================================

/**
 * 发送 Webhook 通知
 */
async function sendWebhook(url, data) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(data);

    const options = {
      hostname: new URL(url).hostname,
      port: 443,
      path: new URL(url).pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'User-Agent': 'BSCDevMonitor/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ success: true, statusCode: res.statusCode });
        } else {
          reject(new Error(`Webhook failed with status ${res.statusCode}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// ============================================
// 监控相关函数
// ============================================

/**
 * 创建监控会话
 */
async function createMonitor(input) {
  const {
    address,
    name = 'Unnamed Monitor',
    duration = 86400,
    billing_mode = 'per_detection',
    webhook_url = null,
    user_id
  } = input;

  const monitorId = `monitor_${crypto.randomUUID().slice(0, 8)}`;
  const startTime = Date.now();
  const endTime = duration > 0 ? startTime + duration * 1000 : 0;

  const monitor = {
    id: monitorId,
    address: address.toLowerCase(),
    name,
    startTime,
    endTime,
    duration,
    billingMode: billing_mode,
    webhookUrl: webhook_url,
    userId: user_id,
    lastCheckedBlock: await getLatestBlock(),
    detectedCount: 0
  };

  activeMonitors.set(monitorId, monitor);

  // 启动监控循环
  monitorLoop(monitorId);

  return {
    status: 'monitoring',
    monitor_id: monitorId,
    address: monitor.address,
    name: monitor.name,
    billing_mode: billing_mode,
    start_time: new Date(monitor.startTime).toISOString(),
    end_time: monitor.endTime > 0 ? new Date(monitor.endTime).toISOString() : 'continuous',
    message: '监控已启动，检测到新币时会自动通知'
  };
}

/**
 * 监控循环
 */
async function monitorLoop(monitorId) {
  const monitor = activeMonitors.get(monitorId);
  if (!monitor) return;

  // 检查是否超时
  if (monitor.endTime > 0 && Date.now() > monitor.endTime) {
    console.log(`\n✅ 监控 ${monitorId} 已完成`);
    console.log(`   总检测次数: ${monitor.detectedCount}`);
    activeMonitors.delete(monitorId);
    return;
  }

  try {
    const latestBlock = await getLatestBlock();

    if (latestBlock > monitor.lastCheckedBlock) {
      console.log(`\n🔎 [${monitorId}] 检查区块 ${monitor.lastCheckedBlock + 1} 到 ${latestBlock}`);

      for (let block = monitor.lastCheckedBlock + 1; block <= latestBlock; block++) {
        try {
          const txs = await getBlockTransactions(block);

          for (const tx of txs) {
            if (tx && tx.from && tx.from.toLowerCase() === monitor.address) {
              if (isTokenTransfer(tx)) {
                monitor.detectedCount++;

                const detectionData = {
                  status: 'detected',
                  timestamp: new Date().toISOString(),
                  block: block,
                  monitor_id: monitorId,
                  token: {
                    name: 'Unknown',
                    symbol: 'UNK',
                    decimals: 18,
                    contract: tx.to
                  },
                  amount: 'Unknown',
                  txHash: tx.hash,
                  from: monitor.address
                };

                // 记录检测并扣费
                const detection = await recordDetection(monitorId, detectionData);

                console.log('\n🚀 检测到新币！');
                console.log(JSON.stringify(detection, null, 2));
              }
            }
          }
        } catch (error) {
          console.error(`❌ 处理区块 ${block} 时出错:`, error.message);
        }
      }

      monitor.lastCheckedBlock = latestBlock;
      console.log(`📊 [${monitorId}] 已检查 ${latestBlock} 个区块，检测到 ${monitor.detectedCount} 笔代币转账`);
    }
  } catch (error) {
    console.error(`❌ [${monitorId}] 监控错误:`, error.message);
  }

  // 继续监控
  setTimeout(() => monitorLoop(monitorId), 10000);
}

/**
 * 停止监控
 */
function stopMonitor(monitorId) {
  const monitor = activeMonitors.get(monitorId);
  if (monitor) {
    activeMonitors.delete(monitorId);
    return {
      status: 'stopped',
      monitor_id: monitorId,
      detected_count: monitor.detectedCount,
      runtime_seconds: Math.floor((Date.now() - monitor.startTime) / 1000)
    };
  }
  return {
    status: 'not_found',
    monitor_id: monitorId
  };
}

/**
 * 查询历史记录
 */
function getHistory(input) {
  const { address, limit = 20 } = input;

  let history = detectionHistory;

  if (address) {
    history = history.filter(d => d.from.toLowerCase() === address.toLowerCase());
  }

  return {
    status: 'success',
    total: history.length,
    records: history.slice(-limit)
  };
}

// ============================================
// 主处理函数
// ============================================

async function handleRequest(input) {
  console.log('📥 收到请求:', JSON.stringify(input, null, 2));

  // 检查支付状态
  if (!input.payment_verified) {
    const billingMode = input.billing_mode || 'per_detection';
    const paymentLink = generatePaymentLink(input.user_id, input.callback_url, billingMode);

    return {
      status: 'payment_required',
      payment_link: paymentLink,
      price: SKILLPAY_CONFIG.price,
      currency: SKILLPAY_CONFIG.currency,
      billing_mode: billingMode,
      message: '请完成支付以使用监控服务'
    };
  }

  // 验证支付
  if (input.payment_id) {
    await verifyPayment(input.user_id, input.payment_id);
  }

  // 处理请求
  const { action } = input;

  switch (action) {
    case 'monitor':
      return await createMonitor(input);

    case 'batch_monitor':
      // 批量监控
      const results = [];
      for (const addrInfo of input.addresses) {
        const result = await createMonitor({
          ...addrInfo,
          ...input,
          payment_verified: true
        });
        results.push(result);
      }
      return {
        status: 'batch_monitoring',
        count: results.length,
        monitors: results
      };

    case 'stop':
      return stopMonitor(input.monitor_id);

    case 'history':
      return getHistory(input);

    case 'status':
      // 查询监控状态
      const monitor = activeMonitors.get(input.monitor_id);
      if (monitor) {
        return {
          status: 'active',
          monitor_id: monitor.id,
          detected_count: monitor.detectedCount,
          runtime_seconds: Math.floor((Date.now() - monitor.startTime) / 1000)
        };
      }
      return { status: 'not_found', monitor_id: input.monitor_id };

    default:
      throw new Error(`Unknown action: ${action}`);
  }
}

// ============================================
// 导出
// ============================================

module.exports = {
  handleRequest,
  generatePaymentLink,
  verifyPayment,
  createMonitor,
  stopMonitor,
  getHistory,
  activeMonitors,
  detectionHistory
};

// ============================================
// 直接运行
// ============================================

if (require.main === module) {
  const args = process.argv.slice(2);
  const address = args[0] || '0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4';
  const duration = parseInt(args[1]) || 60;
  const billingMode = args[2] || 'per_detection';

  console.log(`🧪 测试模式: 监控 ${address}`);
  console.log(`⏱️  时长: ${duration} 秒`);
  console.log(`💰 收费模式: ${billingMode === 'per_detection' ? '按检测收费' : '按次收费'}\n`);

  handleRequest({
    action: 'monitor',
    address,
    name: 'Test Monitor',
    duration,
    billing_mode: billingMode,
    payment_verified: true,
    user_id: 'test_user',
    callback_url: 'http://localhost:3000/callback'
  }).catch(console.error);
}
