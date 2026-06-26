#!/usr/bin/env node

/**
 * CryptoFolio CLI - 加密资产管理命令行工具
 * 支持本地存储 + 云端同步（Cloudflare Workers）
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

// 本地存储路径
const DATA_DIR = join(homedir(), '.openclaw', 'data');
const DATA_FILE = join(DATA_DIR, 'cryptofolio.json');
const CONFIG_FILE = join(DATA_DIR, 'cryptofolio-config.json');

// 云端配置（从环境变量或配置文件读取）
function getCloudConfig() {
  // 优先读取环境变量
  if (process.env.CRYPTOFOLIO_API_URL && process.env.CRYPTOFOLIO_TOKEN) {
    return {
      apiUrl: process.env.CRYPTOFOLIO_API_URL.replace(/\/$/, ''),
      token: process.env.CRYPTOFOLIO_TOKEN,
    };
  }
  // 其次读取配置文件
  try {
    if (existsSync(CONFIG_FILE)) {
      return JSON.parse(readFileSync(CONFIG_FILE, 'utf8'));
    }
  } catch (e) {}
  return null;
}

function saveCloudConfig(config) {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf8');
}

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  dim: '\x1b[2m',
};

function log(msg, color = 'reset') {
  console.log(`${colors[color]}${msg}${colors.reset}`);
}

function error(msg) {
  log(`❌ ${msg}`, 'red');
  process.exit(1);
}

function success(msg) {
  log(`✅ ${msg}`, 'green');
}

// 默认数据
function getDefaultData() {
  return {
    accounts: [
      { id: 'a1', name: 'Binance', type: 'CEX', color: '#F0B90B' },
      { id: 'a2', name: 'OKX', type: 'CEX', color: '#2563EB' },
      { id: 'a3', name: 'MetaMask', type: 'WALLET', color: '#E97B2E' },
    ],
    positions: [],
    trades: [],
    finance: [],
    transfers: [],
  };
}

// 从云端加载数据
async function loadFromCloud(config) {
  try {
    const res = await fetch(`${config.apiUrl}/api/data`, {
      headers: { 'Authorization': `Bearer ${config.token}` },
    });
    if (res.ok) {
      const d = await res.json();
      if (d.ok && d.data) return d.data;
    }
  } catch (e) {
    log(`云端读取失败: ${e.message}`, 'yellow');
  }
  return null;
}

// 保存到云端
async function saveToCloud(config, data) {
  try {
    const res = await fetch(`${config.apiUrl}/api/data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.token}`,
      },
      body: JSON.stringify(data),
    });
    return res.ok;
  } catch (e) {
    log(`云端保存失败: ${e.message}`, 'yellow');
    return false;
  }
}

// 数据读写（优先云端，本地作为备份）
async function loadData() {
  const config = getCloudConfig();

  // 如果配置了云端，优先从云端读取
  if (config) {
    const cloudData = await loadFromCloud(config);
    if (cloudData) {
      // 同步到本地作为备份
      saveDataLocal(cloudData);
      return cloudData;
    }
    log('云端数据不可用，使用本地数据', 'yellow');
  }

  // 从本地读取
  return loadDataLocal();
}

function loadDataLocal() {
  try {
    if (existsSync(DATA_FILE)) {
      return JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    }
  } catch (e) {}
  return getDefaultData();
}

function saveDataLocal(state) {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
  writeFileSync(DATA_FILE, JSON.stringify(state, null, 2), 'utf8');
}

async function saveData(state) {
  // 始终保存到本地
  saveDataLocal(state);

  // 如果配置了云端，同时保存到云端
  const config = getCloudConfig();
  if (config) {
    const ok = await saveToCloud(config, state);
    if (ok) {
      log('已同步到云端', 'dim');
    }
  }
}

// 工具函数
function uid() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function formatUSD(n) {
  if (n === '' || n == null || isNaN(+n)) return '—';
  return '$' + (+n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      result[key] = value;
    }
  }
  return result;
}

// 稳定币列表（价格固定为 1 USD）
const STABLECOINS = ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDP', 'USDD', 'FRAX', 'LUSD', 'USD'];

function getPositionValue(p) {
  const amount = +p.amount || 0;
  // 稳定币按 1 美元计算
  if (STABLECOINS.includes(p.asset?.toUpperCase())) {
    return amount;
  }
  if (p.currentValue !== '' && p.currentValue != null) {
    return +p.currentValue;
  }
  return amount * (+p.currentPrice || 0);
}

// 命令实现
async function overview() {
  const state = await loadData();
  const byType = {};
  const TYPE_LABEL = { CEX: 'CEX', DEX: 'DEX', US_STOCK: '美股', WALLET: '链上钱包' };

  state.positions.forEach((p) => {
    const acc = state.accounts.find((a) => a.id === p.accountId);
    if (!acc) return;
    const v = getPositionValue(p);
    byType[acc.type] = (byType[acc.type] || 0) + v;
  });

  const total = Object.values(byType).reduce((a, b) => a + b, 0);
  const totPnl = state.trades.reduce((s, t) => s + (+t.pnl || 0), 0);
  const activeFinance = state.finance.filter((f) => f.status === 'ACTIVE').length;

  console.log('\n📊 资产概览');
  console.log('═'.repeat(40));
  console.log(`💰 总资产: ${formatUSD(total)}`);
  console.log(`📈 累计盈亏: ${totPnl >= 0 ? '+' : ''}${formatUSD(totPnl)}`);
  console.log(`🌱 进行中理财: ${activeFinance} 个`);
  console.log(`🏦 账户数量: ${state.accounts.length}`);
  console.log(`💼 持仓数量: ${state.positions.length}`);
  console.log(`📝 交易记录: ${state.trades.length}`);
  console.log('');
  if (Object.keys(byType).length > 0) {
    console.log('资金分布:');
    Object.entries(byType).forEach(([type, value]) => {
      const pct = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
      console.log(`  ${TYPE_LABEL[type] || type}: ${formatUSD(value)} (${pct}%)`);
    });
    console.log('');
  }
}

async function listPositions() {
  const state = await loadData();
  console.log('\n💼 持仓列表');
  console.log('═'.repeat(60));
  if (state.positions.length === 0) {
    console.log('暂无持仓');
    return;
  }
  state.positions.forEach((p) => {
    const acc = state.accounts.find((a) => a.id === p.accountId);
    const value = getPositionValue(p);
    const priceDisplay = STABLECOINS.includes(p.asset?.toUpperCase()) ? '$1.00' : formatUSD(p.currentPrice);
    console.log(`${p.asset} | ${acc?.name || '未知账户'} | 数量: ${p.amount} | 均价: ${formatUSD(p.avgCost)} | 现价: ${priceDisplay} | 市值: ${formatUSD(value)}`);
  });
  console.log('');
}

async function listTrades() {
  const state = await loadData();
  console.log('\n📈 交易记录');
  console.log('═'.repeat(60));
  if (state.trades.length === 0) {
    console.log('暂无交易记录');
    return;
  }
  state.trades.slice(-20).reverse().forEach((t) => {
    const acc = state.accounts.find((a) => a.id === t.accountId);
    const side = t.side === 'BUY' ? '买入' : '卖出';
    const pnl = t.pnl ? ` | 盈亏: ${t.pnl >= 0 ? '+' : ''}${formatUSD(t.pnl)}` : '';
    console.log(`${t.date} | ${t.asset} | ${side} | ${acc?.name || '未知'} | 数量: ${t.amount} | 价格: ${formatUSD(t.price)}${pnl}`);
  });
  console.log('');
}

async function listFinance() {
  const state = await loadData();
  console.log('\n🌱 理财产品');
  console.log('═'.repeat(60));
  if (state.finance.length === 0) {
    console.log('暂无理财产品');
    return;
  }
  state.finance.forEach((f) => {
    const acc = state.accounts.find((a) => a.id === f.accountId);
    const status = f.status === 'ACTIVE' ? '进行中' : '已结束';
    console.log(`${f.asset} | ${acc?.name || '未知'} | ${f.type} | 本金: ${f.principal} | APY: ${f.apy}% | ${status}`);
  });
  console.log('');
}

async function listAccounts() {
  const state = await loadData();
  const TYPE_LABEL = { CEX: 'CEX', DEX: 'DEX', US_STOCK: '美股', WALLET: '链上钱包' };
  console.log('\n🏦 账户列表');
  console.log('═'.repeat(40));
  state.accounts.forEach((a) => {
    console.log(`${a.name} | ${TYPE_LABEL[a.type] || a.type}`);
  });
  console.log('');
}

async function addAccount(opts) {
  if (!opts.name || !opts.type) {
    error('需要 --name 和 --type 参数');
  }
  const state = await loadData();
  const newAccount = {
    id: uid(),
    name: opts.name,
    type: opts.type.toUpperCase(),
    color: opts.color || '#E17055',
  };
  state.accounts.push(newAccount);
  await saveData(state);
  success(`已添加账户: ${opts.name} (${opts.type})`);
}

// ═══════════════════════════════════════════════════════
// 持仓联动核心函数
// ═══════════════════════════════════════════════════════

/**
 * 更新持仓（增加或减少）
 * @param {object} state - 数据状态
 * @param {string} accountId - 账户ID
 * @param {string} asset - 资产名称
 * @param {number} delta - 变化量（正数增加，负数减少）
 * @param {number} price - 交易价格（用于计算均价）
 * @returns {boolean} 是否成功
 */
function updatePosition(state, accountId, asset, delta, price = 0) {
  asset = asset.toUpperCase();
  let pos = state.positions.find(p => p.accountId === accountId && p.asset === asset);

  if (delta > 0) {
    // 增加持仓
    if (pos) {
      // 计算加权平均成本
      const oldTotal = (pos.amount || 0) * (pos.avgCost || 0);
      const newTotal = delta * price;
      const totalAmount = (pos.amount || 0) + delta;
      pos.amount = totalAmount;
      pos.avgCost = totalAmount > 0 ? (oldTotal + newTotal) / totalAmount : 0;
      if (price > 0) pos.currentPrice = price;
    } else {
      // 新建持仓
      state.positions.push({
        id: uid(),
        accountId,
        asset,
        amount: delta,
        avgCost: price,
        currentPrice: price,
        currentValue: '',
        note: '',
      });
    }
    return true;
  } else if (delta < 0) {
    // 减少持仓
    const reduceAmount = Math.abs(delta);
    if (!pos || pos.amount < reduceAmount) {
      // 持仓不足，但仍然允许操作（可能是初始数据不完整）
      if (!pos) {
        state.positions.push({
          id: uid(),
          accountId,
          asset,
          amount: delta, // 负数，表示欠款/空头
          avgCost: price,
          currentPrice: price,
          currentValue: '',
          note: '持仓不足，自动创建负持仓',
        });
      } else {
        pos.amount -= reduceAmount;
      }
      return true;
    }
    pos.amount -= reduceAmount;
    // 如果持仓归零，可以选择删除或保留
    if (pos.amount === 0) {
      // 保留记录，只是数量为0
    }
    return true;
  }
  return true;
}

async function addTrade(opts) {
  if (!opts.account || !opts.asset || !opts.side || !opts.amount || !opts.price) {
    error('需要 --account, --asset, --side, --amount, --price 参数');
  }
  const state = await loadData();
  const acc = state.accounts.find((a) => a.name.toLowerCase() === opts.account.toLowerCase());
  if (!acc) {
    error(`找不到账户: ${opts.account}。可用账户: ${state.accounts.map(a => a.name).join(', ')}`);
  }

  const asset = opts.asset.toUpperCase();
  const side = opts.side.toUpperCase();
  const amount = parseFloat(opts.amount);
  const price = parseFloat(opts.price);
  const fee = opts.fee ? parseFloat(opts.fee) : 0;
  const quote = (opts.quote || 'USDT').toUpperCase(); // 计价货币，默认 USDT
  const totalCost = amount * price;

  // 记录交易
  const newTrade = {
    id: uid(),
    accountId: acc.id,
    date: opts.date || today(),
    asset,
    quote,
    side,
    amount,
    price,
    fee,
    pnl: opts.pnl ? parseFloat(opts.pnl) : null,
    note: opts.note || '',
  };
  state.trades.push(newTrade);

  // 联动更新持仓
  if (side === 'BUY') {
    // 买入：base 资产增加，quote 资产减少
    updatePosition(state, acc.id, asset, amount, price);
    updatePosition(state, acc.id, quote, -(totalCost + fee), 1);
  } else if (side === 'SELL') {
    // 卖出：base 资产减少，quote 资产增加
    updatePosition(state, acc.id, asset, -amount, price);
    updatePosition(state, acc.id, quote, totalCost - fee, 1);
  }

  await saveData(state);
  const sideText = side === 'BUY' ? '买入' : '卖出';
  const costText = side === 'BUY' ? `花费 ${formatUSD(totalCost + fee)} ${quote}` : `获得 ${formatUSD(totalCost - fee)} ${quote}`;
  success(`已记录: 在 ${acc.name} ${sideText} ${amount} ${asset}，价格 ${formatUSD(price)}，${costText}`);
}

async function addPosition(opts) {
  if (!opts.account || !opts.asset) {
    error('需要 --account, --asset 参数');
  }
  const state = await loadData();
  const acc = state.accounts.find((a) => a.name.toLowerCase() === opts.account.toLowerCase());
  if (!acc) {
    error(`找不到账户: ${opts.account}。可用账户: ${state.accounts.map(a => a.name).join(', ')}`);
  }

  const asset = opts.asset.toUpperCase();
  const amount = opts.amount ? parseFloat(opts.amount) : null;
  const avgCost = opts.avgCost ? parseFloat(opts.avgCost) : 0;
  const currentPrice = opts.currentPrice ? parseFloat(opts.currentPrice) : 0;

  // 查找是否已有相同账户+资产的持仓
  let existing = state.positions.find(p => p.accountId === acc.id && p.asset === asset);

  if (existing) {
    // 更新现有持仓
    if (amount !== null) existing.amount = amount; // 直接设置数量（用于修正）
    if (avgCost > 0) existing.avgCost = avgCost;
    if (currentPrice > 0) existing.currentPrice = currentPrice;
    if (opts.note) existing.note = opts.note;
    await saveData(state);
    success(`已更新持仓: ${acc.name} ${existing.amount} ${asset} (均价 ${formatUSD(existing.avgCost)})`);
  } else {
    // 新建持仓
    const newPosition = {
      id: uid(),
      accountId: acc.id,
      asset,
      amount: amount || 0,
      avgCost,
      currentPrice,
      currentValue: '',
      note: opts.note || '手动添加',
    };
    state.positions.push(newPosition);
    await saveData(state);
    success(`已添加持仓: ${acc.name} ${amount || 0} ${asset}`);
  }
}

async function addFinance(opts) {
  if (!opts.account || !opts.asset || !opts.type || !opts.principal) {
    error('需要 --account, --asset, --type, --principal 参数');
  }
  const state = await loadData();
  const acc = state.accounts.find((a) => a.name.toLowerCase() === opts.account.toLowerCase());
  if (!acc) {
    error(`找不到账户: ${opts.account}。可用账户: ${state.accounts.map(a => a.name).join(', ')}`);
  }

  const asset = opts.asset.toUpperCase();
  const principal = parseFloat(opts.principal);
  const type = opts.type.toUpperCase();

  const newFinance = {
    id: uid(),
    accountId: acc.id,
    asset,
    type,
    principal,
    apy: opts.apy ? parseFloat(opts.apy) : 0,
    startDate: opts.startDate || today(),
    endDate: opts.endDate || '',
    income: opts.income ? parseFloat(opts.income) : 0,
    status: 'ACTIVE',
    note: opts.note || '',
  };
  state.finance.push(newFinance);

  // 联动更新持仓：开始理财时，资产被锁定（从可用持仓中扣除）
  // 注意：这里不扣除持仓，因为理财中的资产仍然属于用户
  // 如果需要区分"可用"和"锁定"，可以添加 lockedAmount 字段
  // 目前简化处理：理财不影响持仓显示

  await saveData(state);
  success(`已添加理财: ${acc.name} ${asset} ${type}，本金 ${principal}，APY ${newFinance.apy}%`);
}

async function addTransfer(opts) {
  if (!opts.account || !opts.type || !opts.asset || !opts.amount) {
    error('需要 --account, --type, --asset, --amount 参数');
  }
  const state = await loadData();
  const acc = state.accounts.find((a) => a.name.toLowerCase() === opts.account.toLowerCase());
  if (!acc) {
    error(`找不到账户: ${opts.account}。可用账户: ${state.accounts.map(a => a.name).join(', ')}`);
  }

  const asset = opts.asset.toUpperCase();
  const amount = parseFloat(opts.amount);
  const fee = opts.fee ? parseFloat(opts.fee) : 0;
  const type = opts.type.toUpperCase();

  if (!state.transfers) state.transfers = [];
  const newTransfer = {
    id: uid(),
    accountId: acc.id,
    date: opts.date || today(),
    type,
    asset,
    amount,
    fee,
    note: opts.note || '',
  };
  state.transfers.push(newTransfer);

  // 联动更新持仓
  if (type === 'DEPOSIT') {
    // 充值：持仓增加
    updatePosition(state, acc.id, asset, amount - fee, 0);
  } else if (type === 'WITHDRAW') {
    // 提现：持仓减少
    updatePosition(state, acc.id, asset, -(amount + fee), 0);
  }
  // TRANSFER 类型需要指定 toAccount，暂不处理

  await saveData(state);
  const typeText = { DEPOSIT: '充值', WITHDRAW: '提现', TRANSFER: '转账' }[type] || type;
  success(`已记录${typeText}: ${acc.name} ${newTransfer.amount} ${newTransfer.asset}`);
}

async function exportReport(opts) {
  const format = opts.format || 'csv';
  const output = opts.output || join(homedir(), `cryptofolio-report-${today()}.${format}`);

  const state = await loadData();
  const TYPE_LABEL = { CEX: 'CEX', DEX: 'DEX', US_STOCK: '美股', WALLET: '链上钱包' };

  if (format === 'csv' || format === 'xlsx') {
    let csv = '';

    // 账户汇总
    csv += '=== 账户汇总 ===\n';
    csv += '账户名称,类型,持仓数量,总市值\n';
    state.accounts.forEach((acc) => {
      const positions = state.positions.filter((p) => p.accountId === acc.id);
      const totalValue = positions.reduce((sum, p) => {
        const v = p.currentValue || (+p.amount || 0) * (+p.currentPrice || 0);
        return sum + v;
      }, 0);
      csv += `"${acc.name}","${TYPE_LABEL[acc.type] || acc.type}",${positions.length},${totalValue.toFixed(2)}\n`;
    });

    csv += '\n=== 持仓明细 ===\n';
    csv += '账户,资产,数量,均价,现价,市值,备注\n';
    state.positions.forEach((p) => {
      const acc = state.accounts.find((a) => a.id === p.accountId);
      const value = p.currentValue || (+p.amount || 0) * (+p.currentPrice || 0);
      csv += `"${acc?.name || ''}","${p.asset}",${p.amount},${p.avgCost || 0},${p.currentPrice || 0},${value.toFixed(2)},"${p.note || ''}"\n`;
    });

    csv += '\n=== 交易记录 ===\n';
    csv += '日期,账户,资产,方向,数量,价格,手续费,盈亏,备注\n';
    state.trades.forEach((t) => {
      const acc = state.accounts.find((a) => a.id === t.accountId);
      csv += `"${t.date}","${acc?.name || ''}","${t.asset}","${t.side}",${t.amount},${t.price},${t.fee || 0},${t.pnl || ''},"${t.note || ''}"\n`;
    });

    csv += '\n=== 理财产品 ===\n';
    csv += '账户,资产,类型,本金,APY,开始日期,结束日期,收益,状态,备注\n';
    state.finance.forEach((f) => {
      const acc = state.accounts.find((a) => a.id === f.accountId);
      csv += `"${acc?.name || ''}","${f.asset}","${f.type}",${f.principal},${f.apy || 0},"${f.startDate || ''}","${f.endDate || ''}",${f.income || 0},"${f.status}","${f.note || ''}"\n`;
    });

    if (state.transfers && state.transfers.length > 0) {
      csv += '\n=== 流水记录 ===\n';
      csv += '日期,账户,类型,资产,数量,手续费,备注\n';
      state.transfers.forEach((t) => {
        const acc = state.accounts.find((a) => a.id === t.accountId);
        csv += `"${t.date}","${acc?.name || ''}","${t.type}","${t.asset}",${t.amount},${t.fee || 0},"${t.note || ''}"\n`;
      });
    }

    const finalOutput = format === 'xlsx' ? output.replace('.xlsx', '.csv') : output;
    writeFileSync(finalOutput, '\ufeff' + csv, 'utf8'); // BOM for Excel
    success(`报告已导出到: ${finalOutput}`);
  } else {
    error(`不支持的格式: ${format}，请使用 csv 或 xlsx`);
  }
}

// 云端设置命令
async function setup(opts) {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║           CryptoFolio 云端同步设置向导                        ║
╚══════════════════════════════════════════════════════════════╝

云端同步可以让你在多个设备（电脑、手机）上访问同一份数据。

📋 设置步骤：

1. 部署 Cloudflare Worker
   - 登录 https://dash.cloudflare.com
   - 进入 Workers & Pages → Create Worker
   - 复制 cloudflare-worker/worker.js 的内容
   - 修改 TOKEN 为你的密码
   - 创建 KV 命名空间并绑定为 "KV"
   - 部署 Worker

2. 配置 CLI
   方式一：设置环境变量（推荐）
   export CRYPTOFOLIO_API_URL="https://your-worker.workers.dev"
   export CRYPTOFOLIO_TOKEN="your-secret-token"

   方式二：使用配置命令
   node cryptofolio.mjs setup --url "https://your-worker.workers.dev" --token "your-secret-token"

3. 验证连接
   node cryptofolio.mjs cloud-status
`);

  // 如果提供了参数，直接保存配置
  if (opts.url && opts.token) {
    const config = {
      apiUrl: opts.url.replace(/\/$/, ''),
      token: opts.token,
    };

    // 测试连接
    log('正在测试连接...', 'cyan');
    try {
      const res = await fetch(`${config.apiUrl}/api/health`);
      if (res.ok) {
        saveCloudConfig(config);
        success('云端配置已保存！');
        log(`配置文件: ${CONFIG_FILE}`, 'dim');

        // 尝试同步数据
        log('正在同步数据...', 'cyan');
        const cloudData = await loadFromCloud(config);
        if (cloudData) {
          saveDataLocal(cloudData);
          success('已从云端同步数据到本地');
        } else {
          // 上传本地数据到云端
          const localData = loadDataLocal();
          const ok = await saveToCloud(config, localData);
          if (ok) {
            success('已将本地数据上传到云端');
          }
        }
      } else {
        error('连接失败，请检查 URL 是否正确');
      }
    } catch (e) {
      error(`连接失败: ${e.message}`);
    }
  }
}

// 云端状态命令
async function cloudStatus() {
  const config = getCloudConfig();

  console.log('\n☁️  云端同步状态');
  console.log('═'.repeat(40));

  if (!config) {
    log('未配置云端同步', 'yellow');
    log('运行 "cryptofolio setup" 查看配置说明', 'dim');
    return;
  }

  log(`API URL: ${config.apiUrl}`, 'cyan');
  log(`Token: ${'*'.repeat(8)}...`, 'dim');

  // 测试连接
  log('\n正在测试连接...', 'dim');
  try {
    const res = await fetch(`${config.apiUrl}/api/health`);
    if (res.ok) {
      success('云端连接正常');

      // 获取云端数据统计
      const cloudData = await loadFromCloud(config);
      if (cloudData) {
        console.log(`\n云端数据统计:`);
        console.log(`  账户: ${cloudData.accounts?.length || 0}`);
        console.log(`  持仓: ${cloudData.positions?.length || 0}`);
        console.log(`  交易: ${cloudData.trades?.length || 0}`);
        console.log(`  理财: ${cloudData.finance?.length || 0}`);
      }
    } else {
      log('云端连接失败', 'red');
    }
  } catch (e) {
    log(`连接错误: ${e.message}`, 'red');
  }
  console.log('');
}

// 断开云端连接
function cloudDisconnect() {
  try {
    if (existsSync(CONFIG_FILE)) {
      writeFileSync(CONFIG_FILE, '{}', 'utf8');
      success('已断开云端连接');
      log('本地数据不受影响', 'dim');
    } else {
      log('未配置云端同步', 'yellow');
    }
  } catch (e) {
    error(`操作失败: ${e.message}`);
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const opts = parseArgs(args.slice(1));

  try {
    switch (command) {
      case 'overview':
        await overview();
        break;
      case 'list-positions':
        await listPositions();
        break;
      case 'list-trades':
        await listTrades();
        break;
      case 'list-finance':
        await listFinance();
        break;
      case 'list-accounts':
        await listAccounts();
        break;
      case 'add-account':
        await addAccount(opts);
        break;
      case 'add-trade':
        await addTrade(opts);
        break;
      case 'add-position':
        await addPosition(opts);
        break;
      case 'add-finance':
        await addFinance(opts);
        break;
      case 'add-transfer':
        await addTransfer(opts);
        break;
      case 'export':
        await exportReport(opts);
        break;
      case 'setup':
        await setup(opts);
        break;
      case 'cloud-status':
        await cloudStatus();
        break;
      case 'cloud-disconnect':
        cloudDisconnect();
        break;
      default:
        const config = getCloudConfig();
        const cloudInfo = config ? `\n云端同步: ✅ 已配置 (${config.apiUrl})` : '\n云端同步: ❌ 未配置';
        console.log(`
CryptoFolio CLI - 加密资产管理工具

命令:
  overview          查看资产概览
  list-positions    列出所有持仓
  list-trades       列出交易记录
  list-finance      列出理财产品
  list-accounts     列出所有账户
  add-account       添加账户
  add-trade         添加交易记录
  add-position      添加持仓
  add-finance       添加理财产品
  add-transfer      添加流水记录
  export            导出报告

云端同步:
  setup             配置云端同步
  cloud-status      查看云端状态
  cloud-disconnect  断开云端连接

本地数据: ${DATA_FILE}${cloudInfo}

示例:
  cryptofolio overview
  cryptofolio add-trade --account Binance --asset ETH --side BUY --amount 0.5 --price 2800
  cryptofolio setup --url "https://xxx.workers.dev" --token "your-token"
`);
    }
  } catch (err) {
    error(err.message);
  }
}

main();
