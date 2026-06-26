#!/usr/bin/env node
/**
 * A股收盘报告脚本
 * 获取收盘数据、主力资金流向、板块表现并发送飞书消息
 */

import https from 'https';
import http from 'http';
import { execSync } from 'child_process';

// 获取股票指数数据
async function fetchIndexData() {
  // 使用东方财富 API 获取四大指数
  const url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f1,f2,f3,f4,f12,f13,f14,f62,f104,f105,f106&secids=1.000001,0.399001,0.399006,1.000300';
  
  try {
    const data = await fetchJSON(url);
    const results = {};
    
    if (data.data && data.data.diff) {
      for (const item of data.data.diff) {
        results[item.f14] = {
          name: item.f14,
          current: item.f2,
          change: item.f4,
          changePercent: item.f3,
          mainForce: item.f62, // 主力资金
          upCount: item.f104,  // 上涨家数
          downCount: item.f105, // 下跌家数
          flatCount: item.f106  // 平盘家数
        };
      }
    }
    
    return results;
  } catch (e) {
    console.error('获取指数数据失败:', e.message);
    return {};
  }
}

// 获取行业资金流向（主力资金）
async function fetchIndustryFunds() {
  const results = { inflow: [], outflow: [] };
  
  try {
    // 主力资金净流入 Top 50
    const inflowUrl = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f13,f14,f62';
    const inflowData = await fetchJSON(inflowUrl);
    
    if (inflowData.data && inflowData.data.diff) {
      results.inflow = inflowData.data.diff
        .filter(item => item.f62 > 0)
        .slice(0, 10)
        .map(item => ({
          name: item.f14,
          amount: item.f62
        }));
    }
    
    // 主力资金净流出 Top 50
    const outflowUrl = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=0&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f13,f14,f62';
    const outflowData = await fetchJSON(outflowUrl);
    
    if (outflowData.data && outflowData.data.diff) {
      results.outflow = outflowData.data.diff
        .filter(item => item.f62 < 0)
        .slice(0, 10)
        .map(item => ({
          name: item.f14,
          amount: item.f62
        }));
    }
    
  } catch (e) {
    console.error('获取行业资金流向失败:', e.message);
  }
  
  return results;
}

// 获取涨跌统计（全市场）
async function fetchMarketStats() {
  const url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f12,f13,f14,f104,f105,f106&secids=1.000001';
  
  try {
    const data = await fetchJSON(url);
    if (data.data && data.data.diff && data.data.diff[0]) {
      const item = data.data.diff[0];
      return {
        up: item.f104 || 0,
        down: item.f105 || 0,
        flat: item.f106 || 0
      };
    }
  } catch (e) {
    console.error('获取涨跌统计失败:', e.message);
  }
  
  return { up: 0, down: 0, flat: 0 };
}

// 获取热门板块（涨幅榜）
async function fetchHotSectors() {
  const url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f12,f13,f14';
  
  try {
    const data = await fetchJSON(url);
    const hotSectors = [];
    
    if (data.data && data.data.diff) {
      for (const item of data.data.diff.slice(0, 5)) {
        hotSectors.push({
          name: item.f14,
          changePercent: item.f3
        });
      }
    }
    
    return hotSectors;
  } catch (e) {
    console.error('获取热门板块失败:', e.message);
    return [];
  }
}

// 通用 JSON 获取
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

// 检查是否为交易日
function isTradingDay() {
  const now = new Date();
  const day = now.getDay();
  // 0=周日, 6=周六
  if (day === 0 || day === 6) return false;
  
  // 简单节假日判断（春节、国庆等需要额外处理）
  const month = now.getMonth() + 1;
  const date = now.getDate();
  
  // 排除明显节假日（简化处理）
  const holidays = [
    [1, 1],   // 元旦
    [10, 1],  // 国庆
    [10, 2],
    [10, 3],
    [10, 4],
    [10, 5],
    [10, 6],
    [10, 7],
  ];
  
  for (const [m, d] of holidays) {
    if (m === month && d === date) return false;
  }
  
  return true;
}

// 格式化资金金额
function formatAmount(amount) {
  if (!amount) return '0';
  const abs = Math.abs(amount);
  if (abs >= 100000000) {
    return (amount / 100000000).toFixed(2) + '亿';
  } else if (abs >= 10000) {
    return (amount / 10000).toFixed(0) + '万';
  }
  return amount.toString();
}

// 生成操作建议
function generateAdvice(data, fundData, marketStats) {
  const advice = [];
  
  // 沪深300 分析
  if (data['沪深300']) {
    const hs300 = data['沪深300'];
    if (hs300.changePercent > 1) {
      advice.push('📈 沪深300大涨，市场情绪偏积极，可关注蓝筹股机会');
    } else if (hs300.changePercent < -1) {
      advice.push('📉 沪深300下跌，建议观望为主，控制仓位');
    } else if (hs300.changePercent > 0) {
      advice.push('➡️ 沪深300小幅上涨，谨慎乐观');
    } else {
      advice.push('➡️ 沪深300小幅下跌，注意风险');
    }
  }
  
  // 涨跌统计分析
  if (marketStats.up !== undefined) {
    const total = marketStats.up + marketStats.down + marketStats.flat;
    const upRatio = total > 0 ? (marketStats.up / total * 100).toFixed(0) : 0;
    
    if (upRatio > 60) {
      advice.push(`🔥 上涨家数${marketStats.up}家（${upRatio}%），市场氛围偏多`);
    } else if (upRatio < 40) {
      advice.push(`❄️ 上涨家数${marketStats.up}家（${upRatio}%），市场氛围偏空`);
    } else {
      advice.push(`���️ 上涨家数${marketStats.up}家（${upRatio}%），市场分化明显`);
    }
  }
  
  // 主力资金分析
  if (fundData.inflow && fundData.inflow.length > 0) {
    const totalInflow = fundData.inflow.reduce((sum, item) => sum + item.amount, 0);
    if (totalInflow > 5000000000) {
      advice.push('💰 主力资金大幅净流入，关注金融、光伏等板块');
    }
  }
  
  if (fundData.outflow && fundData.outflow.length > 0) {
    const totalOutflow = Math.abs(fundData.outflow.reduce((sum, item) => sum + item.amount, 0));
    if (totalOutflow > 10000000000) {
      advice.push('⚠️ 主力资金大幅净流出，注意电子、通信等板块风险');
    }
  }
  
  // 整体市场判断
  const changes = Object.values(data).map(d => d.changePercent).filter(c => typeof c === 'number');
  const avgChange = changes.length > 0 ? changes.reduce((a, b) => a + b, 0) / changes.length : 0;
  
  if (avgChange > 1) {
    advice.push('🚀 大盘整体偏强，可适度参与');
  } else if (avgChange < -1) {
    advice.push('🛡️ 大盘整体偏弱，建议防御为主');
  } else {
    advice.push('🎯 市场震荡分化，精选个股为主');
  }
  
  return advice;
}

// 生成报告
function generateReport(data, fundData, marketStats, hotSectors) {
  const now = new Date();
  const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  const date = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
  
  let report = `📊 **A股收盘报告** ${date} ${time}\n\n`;
  
  // 指数概览
  report += `### 📈 指数收盘\n`;
  report += `| 指数 | 最新点位 | 涨跌幅 | 主力资金 |\n`;
  report += `|------|----------|--------|----------|\n`;
  for (const [name, info] of Object.entries(data)) {
    if (!info) continue;
    const sign = info.changePercent >= 0 ? '+' : '';
    const mf = info.mainForce ? formatAmount(info.mainForce) : '-';
    report += `| ${name} | ${info.current?.toFixed(2) || '-'} | ${sign}${(info.changePercent || 0).toFixed(2)}% | ${mf} |\n`;
  }
  
  // 涨跌分布
  report += `\n### 📊 涨跌分布\n`;
  if (marketStats.up !== undefined) {
    const total = marketStats.up + marketStats.down + marketStats.flat;
    report += `- 🔴 上涨: **${marketStats.up}** 家\n`;
    report += `- 🟢 下跌: **${marketStats.down}** 家\n`;
    report += `- ⚪ 平盘: **${marketStats.flat}** 家\n`;
    report += `- 📈 上涨比例: **${total > 0 ? (marketStats.up / total * 100).toFixed(1) : 0}%**\n`;
  }
  
  // 主力资金状况
  report += `\n### 💰 主力资金状况\n`;
  
  if (fundData.inflow && fundData.inflow.length > 0) {
    report += `**净流入板块 Top 5：**\n`;
    fundData.inflow.slice(0, 5).forEach((item, i) => {
      report += `${i + 1}. ${item.name} ${formatAmount(item.amount)}\n`;
    });
  }
  
  if (fundData.outflow && fundData.outflow.length > 0) {
    report += `\n**净流出板块 Top 5：**\n`;
    fundData.outflow.slice(0, 5).forEach((item, i) => {
      report += `${i + 1}. ${item.name} ${formatAmount(item.amount)}\n`;
    });
  }
  
  // 热门板块
  report += `\n### 🔥 热门板块（涨幅榜）\n`;
  if (hotSectors && hotSectors.length > 0) {
    hotSectors.forEach((sector, i) => {
      const sign = sector.changePercent >= 0 ? '+' : '';
      report += `${i + 1}. ${sector.name} ${sign}${sector.changePercent.toFixed(2)}%\n`;
    });
  } else {
    report += `暂无数据\n`;
  }
  
  // 操作建议
  report += `\n### 💡 操作建议\n`;
  const advice = generateAdvice(data, fundData, marketStats);
  advice.forEach(a => report += `- ${a}\n`);
  
  report += `\n---\n*数据来源：东方财富 API*`;
  
  return report;
}

// 发送飞书消息
async function sendToFeishu(message) {
  try {
    const escapedMsg = message.replace(/"/g, '\\"').replace(/\n/g, '\\n');
    // 飞书用户 ID (从会话获取)
    const feishuUserId = 'ou_d70ce91dc6fdd7aa7ceacb1c312618a0';
    const result = execSync(`openclaw message send -t user:${feishuUserId} --channel feishu -m "${escapedMsg}"`, {
      encoding: 'utf-8',
      timeout: 30000
    });
    console.log('✅ 飞书消息发送成功');
    return true;
  } catch (e) {
    console.error('❌ 飞书消息发送失败:', e.message);
    console.log('\n--- 报告内容 ---\n' + message);
    return false;
  }
}

// 主函数
async function main() {
  console.log('📅 检查是否为交易日...');
  if (!isTradingDay()) {
    console.log('⏭️ 今天不是交易日，跳过');
    process.exit(0);
  }
  
  console.log('📈 获取指数数据...');
  const indexData = await fetchIndexData();
  
  if (Object.keys(indexData).length === 0) {
    console.error('❌ 未能获取指数数据');
    process.exit(1);
  }
  
  console.log('💰 获取主力资金数据...');
  const fundData = await fetchIndustryFunds();
  
  console.log('📊 获取涨跌统计...');
  const marketStats = await fetchMarketStats();
  
  console.log('🔥 获取热门板块...');
  const hotSectors = await fetchHotSectors();
  
  console.log('📝 生成报告...');
  const report = generateReport(indexData, fundData, marketStats, hotSectors);
  
  // 输出报告
  console.log('\n' + report);
  
  // 发送到飞书
  const args = process.argv.slice(2);
  const shouldSend = args.includes('--send') || args.includes('-s');
  
  if (shouldSend) {
    await sendToFeishu(report);
  }
  
  return report;
}

main().catch(console.error);