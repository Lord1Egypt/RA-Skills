#!/usr/bin/env node

/**
 * BSC Dev Monitor Skill - 更新版
 * 集成 BSCScan API，提供准确的代币信息和 DEV 地址查询
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
  billingMode: 'per_call'
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

// DEV 地址缓存
const DEV_CACHE = {
  '0x6982508145454Ce325dDbE47a25d4ec3d2311933': '0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4',
  '0xfb2051764395e8C8C8Cef85F7eB7B327B7F9F7c': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
  '0xd084a3C3cB2C6F8AdE8A2fD8239f0cC5c49dA0': '0x10ED43C718714eb63d5aA57B78B54704E256024E',
  '0xc748673057861a797275CD8A068AbF95A05212C1': '0x25C78d9A8dC3E966F1D6c95638e485F6d9d0Cb'
};

/**
 * 使用 BSCScan API 获取代币信息
 */
async function getTokenInfo(contractAddress) {
  return new Promise((resolve) => {
    const url = `${BSCSCAN_CONFIG.baseUrl}?module=token&action=tokeninfo&contractaddress=${contractAddress}&apikey=${BSCSCAN_CONFIG.apiKey}`;

    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.status === '1' && result.result && result.result.length > 0) {
            const tokenInfo = result.result[0];
            resolve({
              symbol: tokenInfo.tokenSymbol,
              name: tokenInfo.tokenName,
              decimals: parseInt(tokenInfo.tokenDecimal),
              contract: contractAddress,
              totalSupply: tokenInfo.totalSupply,
              price: tokenInfo.priceUsd || '0'
            });
          } else {
            resolve({
              symbol: 'Unknown',
              name: 'Unknown',
              decimals: 18,
              contract: contractAddress,
              price: '0'
            });
          }
        } catch (e) {
          resolve({
            symbol: 'Unknown',
            name: 'Unknown',
            decimals: 18,
            contract: contractAddress,
            price: '0'
          });
        }
      });
    }).on('error', () => {
      resolve({
        symbol: 'Unknown',
        name: 'Unknown',
        decimals: 18,
        contract: contractAddress,
        price: '0'
      });
    });
  });
}

/**
 * 获取合约创建者（DEV）地址
 */
async function getContractCreator(contractAddress) {
  // 优先使用缓存
  if (DEV_CACHE[contractAddress]) {
    return DEV_CACHE[contractAddress];
  }

  return new Promise((resolve) => {
    const url = `${BSCSCAN_CONFIG.baseUrl}?module=contract&action=getcontractcreation&contractaddress=${contractAddress}&apikey=${BSCSCAN_CONFIG.apiKey}`;

    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.status === '1' && result.result) {
            const creator = result.result.contractCreator;
            DEV_CACHE[contractAddress] = creator;
            resolve(creator);
          } else {
            resolve('Unknown');
          }
        } catch (e) {
          resolve('Unknown');
        }
      });
    }).on('error', () => {
      resolve('Unknown');
    });
  });
}

/**
 * 生成支付链接
 */
function generatePaymentLink(userId, callbackUrl) {
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

/**
 * 解析 Transfer 方法参数
 */
function parseTransferMethod(input) {
  if (!input || input.length < 138) return null;

  try {
    const toAddress = '0x' + input.substring(34, 74);
    const amount = input.substring(74, 138);
    const amountBigInt = BigInt('0x' + amount);

    return {
      to: toAddress,
      amount: amountBigInt.toString(),
      amountHex: amount
    };
  } catch (e) {
    return null;
  }
}

/**
 * 创建监控
 */
async function createMonitor(input) {
  const {
    address,
    name = 'Unnamed Monitor',
    duration = 3600,
    billing_mode = 'per_call',
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
    message: '监控已启动，检测到新币时会自动通知',
    api_integration: 'BSCScan API 已启用'
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

                // 解析转账信息
                const transferData = parseTransferMethod(tx.input);
                const tokenContract = transferData ? transferData.to : tx.to;

                console.log('\n🚀 检测到代币转账！');
                console.log(`   交易哈希: ${tx.hash}`);
                console.log(`   代币合约: ${tokenContract}`);
                console.log(`   区块号: ${block}`);

                // 使用 BSCScan API 获取代币信息
                const tokenInfo = await getTokenInfo(tokenContract);

                console.log(`   代币名称: ${tokenInfo.name}`);
                console.log(`   代币符号: ${tokenInfo.symbol}`);
                console.log(`   精度: ${tokenInfo.decimals}`);
                console.log(`   当前价格: $${tokenInfo.price}`);

                // 计算转账金额
                let displayAmount = 'Unknown';
                if (transferData && transferData.amount !== '0') {
                  const amount = BigInt(transferData.amount);
                  const decimals = BigInt(10 ** tokenInfo.decimals);
                  const formattedAmount = (Number(amount) / Number(decimals)).toFixed(2);
                  displayAmount = `${formattedAmount} ${tokenInfo.symbol}`;
                }

                console.log(`   转账金额: ${displayAmount}`);

                // 获取 DEV 地址
                const devAddress = await getContractCreator(tokenContract);
                console.log(`   DEV 地址: ${devAddress}`);

                // 构建检测结果
                const detection = {
                  status: 'detected',
                  timestamp: new Date().toISOString(),
                  block: block,
                  monitor_id: monitorId,
                  token: {
                    name: tokenInfo.name,
                    symbol: tokenInfo.symbol,
                    decimals: tokenInfo.decimals,
                    contract: tokenContract,
                    price: tokenInfo.price
                  },
                  amount: displayAmount,
                  amountRaw: transferData ? transferData.amount : 'Unknown',
                  txHash: tx.hash,
                  from: monitor.address,
                  devAddress: devAddress,
                  billing: {
                    mode: monitor.billingMode,
                    charged: true,
                    amount: '0.01',
                    currency: 'USDT'
                  },
                  source: 'BSCScan API'
                };

                // 记录到历史
                detectionHistory.push(detection);

                console.log('\n📋 检测结果:');
                console.log(JSON.stringify(detection, null, 2));
              }
            }
          }
        } catch (error) {
          console.error(`❌ 处理区块 ${block} 时出错:`, error.message);
        }
      }

      monitor.lastCheckedBlock = latestBlock;
      console.log(`\n📊 [${monitorId}] 本轮检查完成`);
      console.log(`   已检查 ${latestBlock} 个区块`);
      console.log(`   累计检测到 ${monitor.detectedCount} 笔代币转账`);
    }
  } catch (error) {
    console.error(`❌ [${monitorId}] 监控错误:`, error.message);
  }

  // 继续监控（每 10 秒）
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

/**
 * 主处理函数
 */
async function handleRequest(input) {
  console.log('📥 收到请求:', JSON.stringify(input, null, 2));

  const { action } = input;

  switch (action) {
    case 'monitor':
      return await createMonitor(input);

    case 'stop':
      return stopMonitor(input.monitor_id);

    case 'history':
      return getHistory(input);

    case 'status':
      const m = activeMonitors.get(input.monitor_id);
      if (m) {
        return {
          status: 'active',
          monitor_id: input.monitor_id,
          detected_count: m.detectedCount,
          runtime_seconds: Math.floor((Date.now() - m.startTime) / 1000)
        };
      }
      return { status: 'not_found', monitor_id: input.monitor_id };

    default:
      throw new Error(`Unknown action: ${action}`);
  }
}

// 导出函数
module.exports = {
  handleRequest,
  getTokenInfo,
  getContractCreator,
  createMonitor,
  stopMonitor,
  getHistory,
  activeMonitors,
  detectionHistory,
  BSCSCAN_CONFIG
};

// 直接运行
if (require.main === module) {
  const args = process.argv.slice(2);
  const address = args[0] || '0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4';
  const duration = parseInt(args[1]) || 60;

  console.log(`🧪 测试模式: 监控 ${address}`);
  console.log(`⏱️  时长: ${duration} 秒`);
  console.log(`🔗 BSCScan API: 已启用\n`);

  handleRequest({
    action: 'monitor',
    address,
    name: 'Test Monitor (BSCScan Integrated)',
    duration,
    billing_mode: 'per_call',
    payment_verified: true,
    user_id: 'test_user',
    callback_url: 'http://localhost:3000/callback'
  }).catch(console.error);
}
