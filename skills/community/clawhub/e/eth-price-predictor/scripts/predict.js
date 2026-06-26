#!/usr/bin/env node
/**
 * ETH 价格预测器
 * 日/周级别涨跌预测 - 每次调用 0.003 USDT
 */

const { chargeUser, getPaymentLink, SKILL_PRICE } = require('./skillpay');
const { getCurrentPrice, getKlines, get24hTicker, getETHBTCPair } = require('./binance');
const { predict } = require('./indicators');

function formatTime(date = new Date()) {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

function formatPrediction(p, timeframe) {
  const lines = [];
  const period = timeframe === 'weekly' ? '7天' : '24小时';
  
  lines.push('═'.repeat(60));
  lines.push(`📊 ETH ${timeframe === 'weekly' ? '周线' : '日线'}预测`);
  lines.push('═'.repeat(60));
  lines.push('');
  lines.push(`当前价格: $${p.currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
  lines.push(`预测周期: ${period}`);
  lines.push('');
  
  const directionEmoji = p.direction === 'UP' ? '📈' : (p.direction === 'DOWN' ? '📉' : '➡️');
  const directionText = p.direction === 'UP' ? '涨' : (p.direction === 'DOWN' ? '跌' : '震荡');
  
  lines.push(`🎯 预测: ${directionText} ${directionEmoji}`);
  lines.push(`置信度: ${p.confidence.toFixed(0)}%`);
  lines.push('');
  
  lines.push('技术指标分析:');
  for (const s of p.signals) {
    const emoji = s.bullish === true ? '✅' : (s.bullish === false ? '❌' : '➖');
    lines.push(`  ${emoji} ${s.indicator}(${s.value}) ${s.signal}`);
  }
  lines.push('');
  
  if (p.direction !== 'NEUTRAL') {
    lines.push('💡 交易建议:');
    lines.push(`   方向: ${p.direction === 'UP' ? 'BUY YES' : 'BUY NO'}`);
    lines.push(`   止损: $${p.stopLoss.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    lines.push(`   止盈: $${p.takeProfit.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    lines.push('');
  }
  
  lines.push('⚠️  风险提示: 仅供参考，不构成投资建议');
  lines.push('═'.repeat(60));
  
  return lines.join('\n');
}

async function main() {
  const args = process.argv.slice(2);
  const timeframe = args[0] === 'weekly' ? 'weekly' : 'daily';
  
  if (args[0] === 'help') {
    console.log(`
╔════════════════════════════════════════════════════════╗
║     ETH 价格预测器 - 日/周级别涨跌预测                 ║
║     每次调用 0.003 USDT                                ║
╚════════════════════════════════════════════════════════╝

用法: node predict.js [命令]

命令:
  (无参数)    日线预测（24小时）
  weekly     周线预测（7天）
  etf        查看ETF资金流向（开发中）

示例:
  node predict.js
  node predict.js weekly

💰 支付: BNB Chain USDT，最低充值 8 USDT
`);
    process.exit(0);
  }
  
  const userId = 'user_' + Date.now();
  
  console.log('\n⏳ 检查余额并扣费...');
  const chargeResult = await chargeUser(userId, SKILL_PRICE);
  
  if (!chargeResult.ok) {
    console.log('\n❌ 余额不足');
    console.log(`当前余额: ${chargeResult.balance} USDT`);
    console.log('\n💳 请充值后继续:');
    const paymentUrl = await getPaymentLink(userId, 8);
    console.log(paymentUrl);
    process.exit(1);
  }
  
  console.log(`✅ 扣费成功 (${SKILL_PRICE} USDT)\n`);
  
  try {
    console.log('📊 获取ETH数据...');
    const interval = timeframe === 'weekly' ? '1w' : '1d';
    const klines = await getKlines(interval, 50);
    const ticker = await get24hTicker();
    const ethBtc = await getETHBTCPair();
    
    const prediction = predict(klines, timeframe);
    
    console.log('\n' + formatPrediction(prediction, timeframe));
    
    console.log('\n📈 24小时行情:');
    console.log(`   最高: $${ticker.highPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    console.log(`   最低: $${ticker.lowPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    console.log(`   涨跌: ${ticker.priceChangePercent > 0 ? '+' : ''}${ticker.priceChangePercent.toFixed(2)}%`);
    console.log(`   成交量: ${(ticker.quoteVolume / 1e9).toFixed(2)}B USDT`);
    console.log(`   ETH/BTC: ${ethBtc.toFixed(5)} (相对BTC强弱)`);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
