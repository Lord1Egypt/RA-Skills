#!/usr/bin/env node
/**
 * BTC 短线预测器
 * 15分钟级别涨跌预测 - 每次调用 0.005 USDT
 */

const { chargeUser, getPaymentLink, SKILL_PRICE } = require('./skillpay');
const { getCurrentPrice, getKlines, get24hTicker } = require('./binance');
const { predict } = require('./indicators');

function formatTime(date = new Date()) {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

function formatPrediction(p) {
  const lines = [];
  
  lines.push('═'.repeat(60));
  lines.push('📊 BTC 15分钟预测');
  lines.push('═'.repeat(60));
  lines.push('');
  lines.push(`当前价格: $${p.currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
  lines.push(`预测时间: ${formatTime()} - ${formatTime(new Date(Date.now() + 15 * 60 * 1000))}`);
  lines.push('');
  
  // 预测结果
  const directionEmoji = p.direction === 'UP' ? '📈' : (p.direction === 'DOWN' ? '📉' : '➡️');
  const directionText = p.direction === 'UP' ? '涨' : (p.direction === 'DOWN' ? '跌' : '震荡');
  
  lines.push(`🎯 预测: ${directionText} ${directionEmoji}`);
  lines.push(`置信度: ${p.confidence.toFixed(0)}%`);
  lines.push('');
  
  // 技术指标
  lines.push('技术指标分析:');
  for (const s of p.signals) {
    const emoji = s.bullish === true ? '✅' : (s.bullish === false ? '❌' : '➖');
    lines.push(`  ${emoji} ${s.indicator}(${s.value}) ${s.signal}`);
  }
  lines.push('');
  
  // 交易建议
  if (p.direction !== 'NEUTRAL') {
    lines.push('💡 交易建议:');
    lines.push(`   方向: ${p.direction === 'UP' ? 'BUY YES' : 'BUY NO'}`);
    lines.push(`   止损: $${p.stopLoss.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    lines.push(`   止盈: $${p.takeProfit.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    lines.push('');
  }
  
  // 风险提示
  lines.push('⚠️  风险提示: 仅供参考，不构成投资建议');
  lines.push('═'.repeat(60));
  
  return lines.join('\n');
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length > 0 && args[0] === 'help') {
    console.log(`
╔════════════════════════════════════════════════════════╗
║     BTC 短线预测器 - 15分钟级别涨跌预测                ║
║     每次调用 0.005 USDT                                ║
╚════════════════════════════════════════════════════════╝

用法: node predict.js [命令]

命令:
  (无参数)    获取当前预测
  history    查看历史战绩（开发中）
  auto       自动模式（开发中）

示例:
  node predict.js

💰 支付: BNB Chain USDT，最低充值 8 USDT
`);
    process.exit(0);
  }
  
  const userId = 'user_' + Date.now();
  
  // 扣费
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
    // 获取数据
    console.log('📊 获取BTC数据...');
    const klines = await getKlines('15m', 50);
    const ticker = await get24hTicker();
    
    // 预测
    const prediction = predict(klines);
    
    // 输出
    console.log('\n' + formatPrediction(prediction));
    
    // 24小时行情
    console.log('\n📈 24小时行情:');
    console.log(`   最高: $${ticker.highPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    console.log(`   最低: $${ticker.lowPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    console.log(`   涨跌: ${ticker.priceChangePercent > 0 ? '+' : ''}${ticker.priceChangePercent.toFixed(2)}%`);
    console.log(`   成交量: ${(ticker.quoteVolume / 1e9).toFixed(2)}B USDT`);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
