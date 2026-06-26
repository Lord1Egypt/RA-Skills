#!/usr/bin/env node
/**
 * A股早盘提醒脚本
 * 获取开盘数据、资金流向、板块表现并发送飞书消息
 */

import https from 'https';
import { execSync } from 'child_process';

// 获取股票数据（使用公开 API）
async function fetchStockData() {
  // 使用腾讯股票 API 获取指数数据
  const indices = [
    { code: 'sh000001', name: '上证指数' },
    { code: 'sz399001', name: '深证成指' },
    { code: 'sz399006', name: '创业板指' },
    { code: 'sh000300', name: '沪深300' }
  ];
  
  const results = {};
  
  for (const idx of indices) {
    try {
      const data = await fetchTencentStock(idx.code);
      results[idx.name] = data;
    } catch (e) {
      console.error(`获取 ${idx.name} 失败:`, e.message);
    }
  }
  
  return results;
}

function fetchTencentStock(code) {
  return new Promise((resolve, reject) => {
    const url = `https://qt.gtimg.cn/q=${code}`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          // 解析腾讯股票数据格式
          const match = data.match(/v_.*?="(.+?)"/);
          if (match) {
            const parts = match[1].split('~');
            resolve({
              name: parts[1],
              current: parseFloat(parts[3]),
              change: parseFloat(parts[31]),
              changePercent: parseFloat(parts[32]),
              open: parseFloat(parts[5]),
              high: parseFloat(parts[33]),
              low: parseFloat(parts[34]),
              volume: parts[6],
              amount: parts[37]
            });
          } else {
            reject(new Error('解析失败'));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

// 检查是否为交易日（简单判断：工作日且非节假日）
function isTradingDay() {
  const now = new Date();
  const day = now.getDay();
  // 0=周日, 6=周六
  if (day === 0 || day === 6) return false;
  
  // TODO: 添加节假日判断
  // 可以接入节假日 API 或维护节假日列表
  return true;
}

// 获取资金流向数据（通过 Tavily 搜索）
async function fetchFundFlow() {
  try {
    const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '年').replace(/\//, '月') + '日';
    const query = `A股 北向资金 主力资金 资金流向 ${today}`;
    
    const result = execSync(
      `cd /Users/chris/.openclaw/workspace/skills/openclaw-tavily-search && python3 scripts/tavily_search.py --query "${query}" --max-results 3 --include-answer --format md`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    
    // 解析结果
    const lines = result.split('\n');
    const fundData = {
      northbound: '数据获取中',
      mainForce: [],
      raw: result
    };
    
    // 简单提取北向资金信息
    if (result.includes('净流入') || result.includes('净买入')) {
      fundData.northbound = '净流入';
    } else if (result.includes('净流出') || result.includes('净卖出')) {
      fundData.northbound = '净流出';
    }
    
    return fundData;
  } catch (e) {
    console.error('获取资金流向失败:', e.message);
    return { northbound: '暂无数据', mainForce: [], raw: '' };
  }
}

// 获取板块数据（通过 Tavily 搜索）
async function fetchSectorData() {
  try {
    const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '年').replace(/\//, '月') + '日';
    const query = `A股 板块涨跌幅 热门板块 行业表现 ${today}`;
    
    const result = execSync(
      `cd /Users/chris/.openclaw/workspace/skills/openclaw-tavily-search && python3 scripts/tavily_search.py --query "${query}" --max-results 5 --include-answer --format md`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    
    // 解析板块数据
    const sectorData = {
      gainers: [],
      losers: [],
      hot: [],
      raw: result
    };
    
    // 提取热门板块
    const hotPatterns = ['算力', 'AI', '电网', '煤炭', 'IT服务', '光伏', '锂电', '半导体', '军工'];
    for (const p of hotPatterns) {
      if (result.includes(p)) {
        sectorData.hot.push(p);
      }
    }
    
    // 限制数量
    sectorData.hot = sectorData.hot.slice(0, 5);
    
    return sectorData;
  } catch (e) {
    console.error('获取板块数据失败:', e.message);
    return { gainers: [], losers: [], hot: ['暂无数据'], raw: '' };
  }
}

// 生成操作建议
function generateAdvice(data) {
  const advice = [];
  
  // 沪深300 分析
  if (data['沪深300']) {
    const hs300 = data['沪深300'];
    if (hs300.changePercent > 1) {
      advice.push('沪深300大涨，市场情绪偏积极，可关注蓝筹股机会');
    } else if (hs300.changePercent < -1) {
      advice.push('沪深300下跌，建议观望为主，控制仓位');
    } else {
      advice.push('沪深300震荡，可关注结构性机会');
    }
  }
  
  // 整体市场判断
  const allChanges = Object.values(data).map(d => d.changePercent).filter(c => !isNaN(c));
  const avgChange = allChanges.reduce((a, b) => a + b, 0) / allChanges.length;
  
  if (avgChange > 0.5) {
    advice.push('大盘整体偏强，适合逢低布局');
  } else if (avgChange < -0.5) {
    advice.push('大盘整体偏弱，注意风险控制');
  } else {
    advice.push('市场震荡分化，精选个股为主');
  }
  
  return advice;
}

// 生成报告
function generateReport(data, fundData, sectorData) {
  const now = new Date();
  const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  const date = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
  
  let report = `📊 **A股早盘快报** ${date} ${time}\n\n`;
  
  // 指数概览（表格形式）
  report += `### 📈 指数概览\n`;
  report += `| 指数 | 最新点位 | 涨跌幅 |\n`;
  report += `|------|----------|--------|\n`;
  for (const [name, info] of Object.entries(data)) {
    if (!info) continue;
    const sign = info.changePercent >= 0 ? '+' : '';
    report += `| ${name} | ${info.current.toFixed(2)} | ${sign}${info.changePercent.toFixed(2)}% |\n`;
  }
  
  // 资金流向
  report += `\n### 💰 资金流向\n`;
  report += `- **北向资金**：${fundData.northbound}\n`;
  if (fundData.mainForce && fundData.mainForce.length > 0) {
    report += `- **主力资金**：${fundData.mainForce.join('、')}\n`;
  }
  
  // 板块表现
  report += `\n### 📊 板块表现\n`;
  if (sectorData.hot && sectorData.hot.length > 0) {
    report += `- **热门板块**：${sectorData.hot.join('、')}\n`;
  }
  
  // 操作建议
  report += `\n### 💡 操作建议\n`;
  const advice = generateAdvice(data);
  advice.forEach(a => report += `- ${a}\n`);
  
  report += `\n---\n*数据来源：腾讯股票 API + Tavily*`;
  
  return report;
}

// 通过 OpenClaw CLI 发送飞书消息
async function sendToFeishu(message) {
  const { execSync } = await import('child_process');
  try {
    // 使用 openclaw message send 命令，指定 target 为当前对话
    const escapedMsg = message.replace(/"/g, '\\"').replace(/\n/g, '\\n');
    const result = execSync(`openclaw message send -t . -c feishu -m "${escapedMsg}"`, {
      encoding: 'utf-8',
      timeout: 30000
    });
    console.log('飞书消息发送成功');
    return true;
  } catch (e) {
    console.error('飞书消息发送失败:', e.message);
    // 如果 CLI 发送失败，输出报告供手动处理
    console.log('\n--- 报告内容 ---\n' + message);
    return false;
  }
}

// 主函数
async function main() {
  console.log('检查是否为交易日...');
  if (!isTradingDay()) {
    console.log('今天不是交易日，跳过');
    process.exit(0);
  }
  
  console.log('获取股票指数数据...');
  const data = await fetchStockData();
  
  // 检查是否有数据
  if (Object.keys(data).length === 0) {
    console.error('未能获取任何股票数据');
    process.exit(1);
  }
  
  // 获取资金流向数据
  console.log('获取资金流向数据...');
  const fundData = await fetchFundFlow();
  
  // 获取板块数据
  console.log('获取板块数据...');
  const sectorData = await fetchSectorData();
  
  console.log('生成报告...');
  const report = generateReport(data, fundData, sectorData);
  
  // 发送到飞书
  const args = process.argv.slice(2);
  const shouldSend = args.includes('--send') || args.includes('-s');
  
  if (shouldSend) {
    await sendToFeishu(report);
  } else {
    // 默认输出报告
    console.log('\n' + report);
  }
  
  return report;
}

main().catch(console.error);
