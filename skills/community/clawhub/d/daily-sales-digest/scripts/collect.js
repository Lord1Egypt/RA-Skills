#!/usr/bin/env node
/**
 * daily-sales-digest/scripts/collect.js
 * 매출 데이터 수집 스크립트
 * 
 * 사용법:
 *   node collect.js --date yesterday
 *   node collect.js --date 2026-02-17
 *   node collect.js --date today --source naver
 *   node collect.js --date yesterday --force
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 설정 파일 로드
function loadConfig() {
  const configPath = path.join(process.env.HOME, '.openclaw/workspace/config/daily-sales-digest.json');
  
  if (!fs.existsSync(configPath)) {
    console.error('❌ 설정 파일이 없습니다:', configPath);
    console.error('config.template.json을 복사하여 설정하세요.');
    process.exit(1);
  }
  
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// 날짜 파싱 (yesterday, today, YYYY-MM-DD)
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

// 날짜를 YYYY-MM-DD 형식으로
function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// 네이버 스마트스토어 데이터 수집
async function collectNaver(config, date) {
  if (!config.sources.naver.enabled) {
    return null;
  }
  
  console.log('📦 네이버 스마트스토어 데이터 수집 중...');
  
  // TODO: 실제 네이버 API 호출 구현
  // 현재는 mock 데이터 반환
  
  const mockRevenue = Math.floor(Math.random() * 2000000) + 500000;
  const mockOrders = Math.floor(Math.random() * 50) + 20;
  
  return {
    revenue: mockRevenue,
    orders: mockOrders,
    avgOrderValue: Math.floor(mockRevenue / mockOrders),
    source: 'naver',
    fetchedAt: new Date().toISOString()
  };
}

// 쿠팡 Wing API 데이터 수집
async function collectCoupang(config, date) {
  if (!config.sources.coupang.enabled) {
    return null;
  }
  
  console.log('📦 쿠팡 데이터 수집 중...');
  
  // TODO: 실제 쿠팡 Wing API 호출 구현
  
  const mockRevenue = Math.floor(Math.random() * 1500000) + 300000;
  const mockOrders = Math.floor(Math.random() * 40) + 15;
  
  return {
    revenue: mockRevenue,
    orders: mockOrders,
    avgOrderValue: Math.floor(mockRevenue / mockOrders),
    source: 'coupang',
    fetchedAt: new Date().toISOString()
  };
}

// 배민셀러 API 데이터 수집
async function collectBaemin(config, date) {
  if (!config.sources.baemin.enabled) {
    return null;
  }
  
  console.log('📦 배민셀러 데이터 수집 중...');
  
  // TODO: 실제 배민 API 호출 구현
  
  const mockRevenue = Math.floor(Math.random() * 1000000) + 200000;
  const mockOrders = Math.floor(Math.random() * 30) + 10;
  
  return {
    revenue: mockRevenue,
    orders: mockOrders,
    avgOrderValue: Math.floor(mockRevenue / mockOrders),
    source: 'baemin',
    fetchedAt: new Date().toISOString()
  };
}

// POS 시스템 데이터 수집
async function collectPOS(config, date) {
  if (!config.sources.pos.enabled) {
    return null;
  }
  
  console.log('📦 POS 시스템 데이터 수집 중...');
  
  // TODO: 실제 POS API 호출 구현
  
  const mockRevenue = Math.floor(Math.random() * 800000) + 150000;
  const mockOrders = Math.floor(Math.random() * 25) + 8;
  
  return {
    revenue: mockRevenue,
    orders: mockOrders,
    avgOrderValue: Math.floor(mockRevenue / mockOrders),
    source: 'pos',
    fetchedAt: new Date().toISOString()
  };
}

// 데이터 저장
function saveData(config, date, data) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  const dateStr = formatDate(date);
  const filePath = path.join(dataDir, `${dateStr}.json`);
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  console.log('✅ 데이터 저장 완료:', filePath);
}

// 메인 실행
async function main() {
  const args = process.argv.slice(2);
  
  // 인자 파싱
  let dateStr = 'yesterday';
  let sourceFilter = null;
  let force = false;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && i + 1 < args.length) {
      dateStr = args[i + 1];
      i++;
    } else if (args[i] === '--source' && i + 1 < args.length) {
      sourceFilter = args[i + 1];
      i++;
    } else if (args[i] === '--force') {
      force = true;
    }
  }
  
  const config = loadConfig();
  const date = parseDate(dateStr);
  const dateFormatted = formatDate(date);
  
  console.log(`📅 수집 날짜: ${dateFormatted}`);
  
  // 이미 데이터가 있는지 확인
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const filePath = path.join(dataDir, `${dateFormatted}.json`);
  
  if (fs.existsSync(filePath) && !force) {
    console.log('⚠️  이미 데이터가 존재합니다. --force 옵션으로 덮어쓸 수 있습니다.');
    process.exit(0);
  }
  
  // 소스별 데이터 수집
  const sources = {};
  
  if (!sourceFilter || sourceFilter === 'naver') {
    const naverData = await collectNaver(config, date);
    if (naverData) sources.naver = naverData;
  }
  
  if (!sourceFilter || sourceFilter === 'coupang') {
    const coupangData = await collectCoupang(config, date);
    if (coupangData) sources.coupang = coupangData;
  }
  
  if (!sourceFilter || sourceFilter === 'baemin') {
    const baeminData = await collectBaemin(config, date);
    if (baeminData) sources.baemin = baeminData;
  }
  
  if (!sourceFilter || sourceFilter === 'pos') {
    const posData = await collectPOS(config, date);
    if (posData) sources.pos = posData;
  }
  
  if (Object.keys(sources).length === 0) {
    console.log('⚠️  활성화된 데이터 소스가 없습니다.');
    process.exit(1);
  }
  
  // 합계 계산
  let totalRevenue = 0;
  let totalOrders = 0;
  
  for (const [key, data] of Object.entries(sources)) {
    totalRevenue += data.revenue;
    totalOrders += data.orders;
  }
  
  const result = {
    date: dateFormatted,
    sources,
    total: {
      revenue: totalRevenue,
      orders: totalOrders,
      avgOrderValue: totalOrders > 0 ? Math.floor(totalRevenue / totalOrders) : 0
    },
    collectedAt: new Date().toISOString()
  };
  
  // 저장
  saveData(config, date, result);
  
  console.log('\n📊 수집 요약:');
  console.log(`💰 총 매출: ₩${totalRevenue.toLocaleString()}`);
  console.log(`🛒 주문 수: ${totalOrders}건`);
  console.log(`💳 객단가: ₩${result.total.avgOrderValue.toLocaleString()}`);
}

// 에러 핸들링
main().catch(err => {
  console.error('❌ 에러 발생:', err.message);
  process.exit(1);
});
