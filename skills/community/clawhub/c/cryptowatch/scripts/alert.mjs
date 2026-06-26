#!/usr/bin/env node
/**
 * ₿ CryptoWatch - 价格预警
 * 数据源：CoinGecko API
 */

import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const API = 'https://api.coingecko.com/api/v3';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ALERTS_FILE = path.join(__dirname, '../config/alerts.json');

// 参数解析
const args = process.argv.slice(2);
const params = {
  coin: '',
  above: null,
  below: null,
  list: false,
  remove: null,
  help: false
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--help' || args[i] === '-h') params.help = true;
  else if (args[i] === '--list') params.list = true;
  else if (args[i] === '--remove') params.remove = parseInt(args[++i]);
  else if (args[i] === '--above') params.above = parseFloat(args[++i]);
  else if (args[i] === '--below') params.below = parseFloat(args[++i]);
  else if (!args[i].startsWith('--') && !params.coin) {
    params.coin = args[i].toLowerCase();
  }
}

const COIN_MAP = {
  btc: 'bitcoin',
  eth: 'ethereum',
  sol: 'solana',
  bnb: 'bnb',
  xrp: 'xrp',
  doge: 'dogecoin',
  ada: 'cardano',
  avax: 'avalanche-2'
};

function showHelp() {
  console.log(`
₿ CryptoWatch - 价格预警

用法:
  node scripts/alert.mjs [币种] [选项]

示例:
  node scripts/alert.mjs btc --above 100000    # BTC 突破 $100k 提醒
  node scripts/alert.mjs eth --below 3000     # ETH 跌破 $3k 提醒
  node scripts/alert.mjs --list               # 查看所有预警
  node scripts/alert.mjs --remove 1           # 删除第 1 个预警

选项:
  --above <price>    价格突破上方阈值
  --below <price>    价格跌破下方阈值
  --list             列出所有预警
  --remove <id>      删除指定预警
  --help, -h         显示帮助
`);
}

// 加载预警列表
function loadAlerts() {
  try {
    if (fs.existsSync(ALERTS_FILE)) {
      const data = fs.readFileSync(ALERTS_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {}
  return { alerts: [] };
}

// 保存预警列表
function saveAlerts(data) {
  fs.writeFileSync(ALERTS_FILE, JSON.stringify(data, null, 2));
}

// 添加预警
function addAlert(coinId, condition, price) {
  const data = loadAlerts();
  const alert = {
    id: data.alerts.length + 1,
    coin: coinId,
    condition: condition,
    price: price,
    created: new Date().toISOString()
  };
  data.alerts.push(alert);
  saveAlerts(data);
  return alert;
}

// 列出预警
function listAlerts() {
  const data = loadAlerts();
  
  if (data.alerts.length === 0) {
    console.log('\n📭 暂无价格预警\n');
    console.log('💡 添加预警：node scripts/alert.mjs btc --above 100000\n');
    return;
  }
  
  console.log('\n₿ CryptoWatch - 价格预警列表\n');
  console.log('ID   币种    条件'.padEnd(25) + '目标价格');
  console.log('─'.repeat(50));
  
  data.alerts.forEach(alert => {
    const id = String(alert.id).padEnd(4);
    const coin = alert.coin.toUpperCase().padEnd(8);
    const condition = alert.condition === 'above' ? '🔺 突破 >' : '🔻 跌破 <';
    const price = `$${alert.price.toLocaleString()}`;
    
    console.log(`${id} ${coin} ${condition.padEnd(14)} ${price}`);
  });
  
  console.log('─'.repeat(50) + '\n');
  console.log('🗑️  删除预警：node scripts/alert.mjs --remove <ID>');
  console.log('➕ 添加预警：node scripts/alert.mjs btc --above 100000\n');
}

// 删除预警
function removeAlert(id) {
  const data = loadAlerts();
  const before = data.alerts.length;
  data.alerts = data.alerts.filter(a => a.id !== id);
  
  if (data.alerts.length === before) {
    console.log(`❌ 未找到预警 ID: ${id}\n`);
    return false;
  }
  
  saveAlerts(data);
  console.log(`✅ 已删除预警 #${id}\n`);
  return true;
}

// 获取当前价格
async function getCurrentPrice(coinId) {
  const url = `${API}/simple/price?ids=${coinId}&vs_currencies=usd`;
  const response = await fetch(url);
  const data = await response.json();
  return data[coinId]?.usd || null;
}

// 检查预警
async function checkAlerts() {
  const data = loadAlerts();
  if (data.alerts.length === 0) return;
  
  console.log('\n🔔 检查预警...\n');
  
  for (const alert of data.alerts) {
    const currentPrice = await getCurrentPrice(alert.coin);
    if (!currentPrice) continue;
    
    let triggered = false;
    if (alert.condition === 'above' && currentPrice >= alert.price) {
      triggered = true;
      console.log(`🚨 ${alert.coin.toUpperCase()} 突破 $${alert.price}！当前：$${currentPrice}`);
    } else if (alert.condition === 'below' && currentPrice <= alert.price) {
      triggered = true;
      console.log(`🚨 ${alert.coin.toUpperCase()} 跌破 $${alert.price}！当前：$${currentPrice}`);
    }
    
    if (triggered) {
      // TODO: 发送通知（Telegram/邮件）
      console.log('   💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9\n');
    }
  }
}

// 主函数
async function main() {
  if (params.help) {
    showHelp();
    process.exit(0);
  }
  
  if (params.list) {
    listAlerts();
    return;
  }
  
  if (params.remove !== null) {
    removeAlert(params.remove);
    return;
  }
  
  if (!params.coin) {
    console.log('❌ 请指定币种\n');
    showHelp();
    process.exit(1);
  }
  
  if (params.above === null && params.below === null) {
    console.log('❌ 请指定 --above 或 --below\n');
    showHelp();
    process.exit(1);
  }
  
  const coinId = COIN_MAP[params.coin] || params.coin;
  
  // 获取当前价格验证
  const currentPrice = await getCurrentPrice(coinId);
  if (!currentPrice) {
    console.log(`❌ 找不到币种：${params.coin}\n`);
    process.exit(1);
  }
  
  // 添加预警
  if (params.above !== null) {
    const alert = addAlert(coinId, 'above', params.above);
    console.log(`\n✅ 预警已设置`);
    console.log(`   币种：${coinId.toUpperCase()}`);
    console.log(`   条件：突破 > $${params.above.toLocaleString()}`);
    console.log(`   当前：$${currentPrice.toLocaleString()}`);
    console.log(`   距离：${((params.above - currentPrice) / currentPrice * 100).toFixed(2)}%\n`);
  } else {
    const alert = addAlert(coinId, 'below', params.below);
    console.log(`\n✅ 预警已设置`);
    console.log(`   币种：${coinId.toUpperCase()}`);
    console.log(`   条件：跌破 < $${params.below.toLocaleString()}`);
    console.log(`   当前：$${currentPrice.toLocaleString()}`);
    console.log(`   距离：${((currentPrice - params.below) / currentPrice * 100).toFixed(2)}%\n`);
  }
  
  console.log('💡 运行 node scripts/alert.mjs --list 查看所有预警');
  console.log('💡 预警需要手动运行检查，或配置 cron 定时任务\n');
}

main();
