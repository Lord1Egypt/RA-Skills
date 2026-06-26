#!/usr/bin/env node
/**
 * daily-sales-digest/scripts/digest.js
 * 매출 요약 및 리포트 생성 스크립트
 * 
 * 사용법:
 *   node digest.js --date yesterday --format text
 *   node digest.js --period week --format markdown
 *   node digest.js --date 2026-02-17 --deliver discord
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 설정 파일 로드
function loadConfig() {
  const configPath = path.join(process.env.HOME, '.openclaw/workspace/config/daily-sales-digest.json');
  
  if (!fs.existsSync(configPath)) {
    console.error('❌ 설정 파일이 없습니다:', configPath);
    process.exit(1);
  }
  
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// 날짜 파싱
function parseDate(dateStr) {
  if (dateStr === 'today') {
    return new Date();
  } else if (dateStr === 'yesterday') {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  } else {
    return new Date(dateStr);
  }
}

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// 데이터 로드
function loadData(config, date) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const dateStr = formatDate(date);
  const filePath = path.join(dataDir, `${dateStr}.json`);
  
  if (!fs.existsSync(filePath)) {
    return null;
  }
  
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

// 변화율 계산
function calcChange(current, previous) {
  if (!previous || previous === 0) return null;
  return ((current - previous) / previous);
}

// 변화율을 퍼센트 문자열로
function formatChange(change) {
  if (change === null) return 'N/A';
  const sign = change >= 0 ? '↑' : '↓';
  return `${sign} ${Math.abs(change * 100).toFixed(1)}%`;
}

// 일일 요약 생성
function generateDailySummary(config, date) {
  const data = loadData(config, date);
  
  if (!data) {
    console.error('❌ 데이터가 없습니다:', formatDate(date));
    process.exit(1);
  }
  
  // 전일 데이터
  const yesterday = new Date(date);
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayData = loadData(config, yesterday);
  
  // 전주 동요일 데이터
  const lastWeek = new Date(date);
  lastWeek.setDate(lastWeek.getDate() - 7);
  const lastWeekData = loadData(config, lastWeek);
  
  // 전월 동일 데이터
  const lastMonth = new Date(date);
  lastMonth.setMonth(lastMonth.getMonth() - 1);
  const lastMonthData = loadData(config, lastMonth);
  
  // 변화율 계산
  const vsYesterday = {
    revenue: calcChange(data.total.revenue, yesterdayData?.total.revenue),
    orders: calcChange(data.total.orders, yesterdayData?.total.orders),
    avgOrderValue: calcChange(data.total.avgOrderValue, yesterdayData?.total.avgOrderValue)
  };
  
  const vsLastWeek = {
    revenue: calcChange(data.total.revenue, lastWeekData?.total.revenue),
    orders: calcChange(data.total.orders, lastWeekData?.total.orders),
    avgOrderValue: calcChange(data.total.avgOrderValue, lastWeekData?.total.avgOrderValue)
  };
  
  const vsLastMonth = {
    revenue: calcChange(data.total.revenue, lastMonthData?.total.revenue),
    orders: calcChange(data.total.orders, lastMonthData?.total.orders),
    avgOrderValue: calcChange(data.total.avgOrderValue, lastMonthData?.total.avgOrderValue)
  };
  
  return {
    date: data.date,
    summary: data.total,
    comparison: {
      vsYesterday,
      vsLastWeek,
      vsLastMonth
    },
    sources: data.sources
  };
}

// 주간 요약 생성
function generateWeeklySummary(config, endDate) {
  const results = [];
  
  for (let i = 6; i >= 0; i--) {
    const d = new Date(endDate);
    d.setDate(d.getDate() - i);
    const data = loadData(config, d);
    if (data) results.push(data);
  }
  
  if (results.length === 0) {
    console.error('❌ 주간 데이터가 없습니다.');
    process.exit(1);
  }
  
  const totalRevenue = results.reduce((sum, d) => sum + d.total.revenue, 0);
  const totalOrders = results.reduce((sum, d) => sum + d.total.orders, 0);
  
  return {
    period: 'week',
    startDate: results[0].date,
    endDate: results[results.length - 1].date,
    summary: {
      revenue: totalRevenue,
      avgDailyRevenue: Math.floor(totalRevenue / results.length),
      orders: totalOrders,
      avgOrderValue: totalOrders > 0 ? Math.floor(totalRevenue / totalOrders) : 0
    },
    daily: results
  };
}

// 월간 요약 생성
function generateMonthlySummary(config, endDate) {
  const results = [];
  const year = endDate.getFullYear();
  const month = endDate.getMonth();
  
  // 해당 월의 1일부터 endDate까지
  const startDate = new Date(year, month, 1);
  
  let current = new Date(startDate);
  while (current <= endDate) {
    const data = loadData(config, current);
    if (data) results.push(data);
    current.setDate(current.getDate() + 1);
  }
  
  if (results.length === 0) {
    console.error('❌ 월간 데이터가 없습니다.');
    process.exit(1);
  }
  
  const totalRevenue = results.reduce((sum, d) => sum + d.total.revenue, 0);
  const totalOrders = results.reduce((sum, d) => sum + d.total.orders, 0);
  
  return {
    period: 'month',
    startDate: results[0].date,
    endDate: results[results.length - 1].date,
    summary: {
      revenue: totalRevenue,
      avgDailyRevenue: Math.floor(totalRevenue / results.length),
      orders: totalOrders,
      avgOrderValue: totalOrders > 0 ? Math.floor(totalRevenue / totalOrders) : 0
    },
    daily: results
  };
}

// 텍스트 형식 출력
function formatText(summary) {
  if (summary.period === 'week') {
    return formatWeeklyText(summary);
  } else if (summary.period === 'month') {
    return formatMonthlyText(summary);
  }
  
  // 일일 요약
  let output = `📊 ${summary.date} 매출 요약\n\n`;
  output += `💰 총 매출: ₩${summary.summary.revenue.toLocaleString()}`;
  if (summary.comparison.vsYesterday.revenue !== null) {
    output += ` (${formatChange(summary.comparison.vsYesterday.revenue)} vs 전일)`;
  }
  output += '\n';
  
  output += `🛒 주문 수: ${summary.summary.orders}건`;
  if (summary.comparison.vsYesterday.orders !== null) {
    output += ` (${formatChange(summary.comparison.vsYesterday.orders)} vs 전일)`;
  }
  output += '\n';
  
  output += `💳 객단가: ₩${summary.summary.avgOrderValue.toLocaleString()}`;
  if (summary.comparison.vsYesterday.avgOrderValue !== null) {
    output += ` (${formatChange(summary.comparison.vsYesterday.avgOrderValue)} vs 전일)`;
  }
  output += '\n';
  
  // 비교 분석
  output += '\n📈 비교 분석:\n';
  if (summary.comparison.vsYesterday.revenue !== null) {
    output += `  • 전일 대비: ${formatChange(summary.comparison.vsYesterday.revenue)}\n`;
  }
  if (summary.comparison.vsLastWeek.revenue !== null) {
    output += `  • 전주 동요일: ${formatChange(summary.comparison.vsLastWeek.revenue)}\n`;
  }
  if (summary.comparison.vsLastMonth.revenue !== null) {
    output += `  • 전월 동일: ${formatChange(summary.comparison.vsLastMonth.revenue)}\n`;
  }
  
  // 채널별
  output += '\n🏪 채널별:\n';
  for (const [key, data] of Object.entries(summary.sources)) {
    output += `  • ${key}: ₩${data.revenue.toLocaleString()} (${data.orders}건)\n`;
  }
  
  return output;
}

function formatWeeklyText(summary) {
  let output = `📊 주간 매출 리포트 (${summary.startDate} ~ ${summary.endDate})\n\n`;
  output += `💰 총 매출: ₩${summary.summary.revenue.toLocaleString()}\n`;
  output += `📅 평균 일매출: ₩${summary.summary.avgDailyRevenue.toLocaleString()}\n`;
  output += `🛒 총 주문: ${summary.summary.orders}건\n`;
  output += `💳 평균 객단가: ₩${summary.summary.avgOrderValue.toLocaleString()}\n`;
  return output;
}

function formatMonthlyText(summary) {
  let output = `📊 월간 매출 리포트 (${summary.startDate} ~ ${summary.endDate})\n\n`;
  output += `💰 총 매출: ₩${summary.summary.revenue.toLocaleString()}\n`;
  output += `📅 평균 일매출: ₩${summary.summary.avgDailyRevenue.toLocaleString()}\n`;
  output += `🛒 총 주문: ${summary.summary.orders}건\n`;
  output += `💳 평균 객단가: ₩${summary.summary.avgOrderValue.toLocaleString()}\n`;
  return output;
}

// Discord 전송
function deliverDiscord(config, content) {
  if (!config.delivery.discord.enabled) {
    console.error('❌ Discord 전송이 비활성화되어 있습니다.');
    return;
  }
  
  const channelId = config.delivery.discord.channelId;
  
  try {
    execSync(`openclaw message send --channel discord --target "${channelId}" --message "${content.replace(/"/g, '\\"')}"`, {
      stdio: 'inherit'
    });
    console.log('✅ Discord 전송 완료');
  } catch (err) {
    console.error('❌ Discord 전송 실패:', err.message);
  }
}

// 이메일 전송
function deliverEmail(config, content, date) {
  if (!config.delivery.email.enabled) {
    console.error('❌ 이메일 전송이 비활성화되어 있습니다.');
    return;
  }
  
  const subject = config.delivery.email.subject.replace('{date}', date);
  const to = config.delivery.email.to;
  
  console.log('📧 이메일 전송 (TODO: himalaya 스킬 연동)');
  console.log(`To: ${to}`);
  console.log(`Subject: ${subject}`);
}

// 메인 실행
function main() {
  const args = process.argv.slice(2);
  
  let dateStr = 'yesterday';
  let period = null;
  let format = 'text';
  let deliver = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && i + 1 < args.length) {
      dateStr = args[i + 1];
      i++;
    } else if (args[i] === '--period' && i + 1 < args.length) {
      period = args[i + 1];
      i++;
    } else if (args[i] === '--format' && i + 1 < args.length) {
      format = args[i + 1];
      i++;
    } else if (args[i] === '--deliver' && i + 1 < args.length) {
      deliver = args[i + 1].split(',');
      i++;
    }
  }
  
  const config = loadConfig();
  const date = parseDate(dateStr);
  
  let summary;
  
  if (period === 'week') {
    summary = generateWeeklySummary(config, date);
  } else if (period === 'month') {
    summary = generateMonthlySummary(config, date);
  } else {
    summary = generateDailySummary(config, date);
  }
  
  // 출력
  let output;
  
  if (format === 'json') {
    output = JSON.stringify(summary, null, 2);
  } else if (format === 'markdown') {
    // TODO: Markdown 포맷 구현
    output = formatText(summary);
  } else {
    output = formatText(summary);
  }
  
  console.log(output);
  
  // 전송
  if (deliver) {
    if (deliver.includes('discord')) {
      deliverDiscord(config, output);
    }
    if (deliver.includes('email')) {
      deliverEmail(config, output, summary.date || summary.endDate);
    }
  }
}

main();
