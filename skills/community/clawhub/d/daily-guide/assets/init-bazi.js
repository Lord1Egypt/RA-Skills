#!/usr/bin/env node
/**
 * init-bazi.js — daily-guide 个人档案初始化引导
 *
 * 交互式收集出生信息，生成 bazi.json（daily-guide.js 会自动读取）。
 * 支持命令行参数（非交互模式）：
 *   node init-bazi.js --date=YYYY-MM-DD --time=HH:MM --city=城市名
 *   node init-bazi.js --date=YYYY-MM-DD --time=HH:MM --longitude=经度
 *   node init-bazi.js --date=YYYY-MM-DD --time=HH:MM --school=beijing|solar
 */
const path = require('path');
const fs = require('fs');
const readline = require('readline');
const os = require('os');

// 用户档案路径（与 daily-guide.js 一致）
const BAZI_JSON = process.env.DAILY_GUIDE_BAZI || path.join(os.homedir(), '.daily-guide', 'bazi.json');

let Lunar;
try {
  ({ Lunar } = require('lunar-javascript'));
} catch (e) {
  console.error('缺少 lunar-javascript，请先执行: npm install lunar-javascript');
  process.exit(1);
}

// 常见城市经度表（约值，用于真太阳时校正）
const CITIES = {
  '北京': 116.41, '上海': 121.47, '广州': 113.26, '深圳': 114.06,
  '杭州': 120.15, '南京': 118.80, '苏州': 120.62,
  '郑州': 113.63, '洛阳': 112.45, '成都': 104.07,
  '重庆': 106.55, '武汉': 114.30, '西安': 108.94, '天津': 117.20,
  '青岛': 120.38, '济南': 117.00, '福州': 119.30, '厦门': 118.09,
  '长沙': 112.94, '南昌': 115.86, '合肥': 117.28, '昆明': 102.71,
  '贵阳': 106.63, '南宁': 108.32, '海口': 110.35, '太原': 112.55,
  '石家庄': 114.51, '沈阳': 123.43, '大连': 121.62, '长春': 125.32,
  '哈尔滨': 126.53, '兰州': 103.83, '西宁': 101.78, '银川': 106.23,
  '乌鲁木齐': 87.62, '拉萨': 91.11, '呼和浩特': 111.75, '香港': 114.17,
  '澳门': 113.55, '台北': 121.56,
};

function ask(rl, q) {
  return new Promise(res => rl.question(q, res));
}

function calcBazi(dateStr, timeStr, longitude, school) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const [hh, mm] = timeStr.split(':').map(Number);
  // 北京时间派
  const solar = Lunar.fromYmdHms ? null : null;
  const lunarB = (function () {
    const s = require('lunar-javascript').Solar.fromYmdHms(y, m, d, hh, mm, 0);
    return s.getLunar();
  })();
  const baziB = lunarB.getEightChar();
  const beijing = {
    lunarDate: lunarB.toString(),
    shengxiao: lunarB.getYearShengXiao(),
    bazi: `${baziB.getYear()} ${baziB.getMonth()} ${baziB.getDay()} ${baziB.getTime()}`,
    dayGanZhi: lunarB.getDayInGanZhi(),
  };

  // 真太阳时派（经度校正）
  let solarResult = null;
  if (longitude) {
    const offsetMin = Math.round((longitude - 120) * 4);
    let tt = new Date(y, m - 1, d, hh, mm + offsetMin, 0);
    const s2 = require('lunar-javascript').Solar.fromYmdHms(
      tt.getFullYear(), tt.getMonth() + 1, tt.getDate(), tt.getHours(), tt.getMinutes(), 0
    );
    const lunarS = s2.getLunar();
    const baziS = lunarS.getEightChar();
    solarResult = {
      solarTime: `${String(tt.getHours()).padStart(2, '0')}:${String(tt.getMinutes()).padStart(2, '0')} (${tt.getFullYear()}-${String(tt.getMonth()+1).padStart(2,'0')}-${String(tt.getDate()).padStart(2,'0')})`,
      offsetMin,
      lunarDate: lunarS.toString(),
      bazi: `${baziS.getYear()} ${baziS.getMonth()} ${baziS.getDay()} ${baziS.getTime()}`,
      dayGanZhi: lunarS.getDayInGanZhi(),
    };
  }

  const chosen = school === 'solar' && solarResult ? solarResult : beijing;
  return {
    solarDate: dateStr,
    solarTime: timeStr,
    city: '',
    longitude: longitude || null,
    school: school === 'solar' && solarResult ? 'solar' : 'beijing',
    shengxiao: chosen === beijing ? beijing.shengxiao : (solarResult && chosen === solarResult ? lunarS.getYearShengXiao() : beijing.shengxiao),
    dayGanZhi: chosen.dayGanZhi,
    bazi: chosen.bazi,
    beijing,
    solar: solarResult,
  };
}

async function interactive() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  console.log('');
  console.log('🀄 daily-guide 个人档案初始化');
  console.log('──────────────────────────────────');
  console.log('只需要 3 项信息，生成你的专属黄历建议（生肖冲煞/本命冲日判断）。');
  console.log('信息只保存在本地 bazi.json，不上传。');
  console.log('');
  try {
    const dateStr = await ask(rl, '① 公历出生日期（如 YYYY-MM-DD）: ');
    if (!/^\d{4}-\d{1,2}-\d{1,2}$/.test(dateStr)) { console.error('❌ 日期格式应为 YYYY-MM-DD'); process.exit(1); }
    const timeStr = await ask(rl, '② 出生时间（24小时制，如 08:30；不确定可只填大概）: ');
    if (!/^\d{1,2}:\d{2}$/.test(timeStr)) { console.error('❌ 时间格式应为 HH:MM'); process.exit(1); }
    const city = await ask(rl, '③ 出生城市（用于真太阳时校正，不知道可回车跳过）: ');
    let longitude = null;
    if (city.trim()) {
      const hit = CITIES[city.trim()];
      if (hit) { longitude = hit; console.log(`   ✅ ${city} 经度约 ${hit}°E`); }
      else {
        const manual = await ask(rl, `   ⚠️ 未收录「${city.trim()}」，可输入经度（如 113.5，不知道回车跳过）: `);
        if (manual.trim()) longitude = parseFloat(manual.trim());
      }
    }
    const school = await ask(rl, '④ 八字流派：北京时间派[1] 或 真太阳时派[2]？（默认 1）: ');
    const sch = school.trim() === '2' ? 'solar' : 'beijing';

    const result = calcBazi(dateStr.trim(), timeStr.padStart(5, '0'), longitude, sch);
    result.city = city.trim() || '';

    console.log('');
    console.log('📋 计算结果：');
    console.log(`   农历：${result.beijing.lunarDate}`);
    console.log(`   生肖：${result.shengxiao}`);
    console.log(`   八字（北京时间派）：${result.beijing.bazi}`);
    if (result.solar) console.log(`   八字（真太阳时派）：${result.solar.bazi}  [校正${result.solar.offsetMin}分钟 → ${result.solar.solarTime}]`);
    console.log(`   主用流派：${result.school === 'solar' ? '真太阳时派' : '北京时间派'}`);
    console.log(`   日柱：${result.dayGanZhi}`);
    console.log('');
    const ok = await ask(rl, '确认保存？（y/n）: ');
    if (ok.trim().toLowerCase() !== 'y') { console.log('已取消'); process.exit(0); }

    const outPath = BAZI_JSON;
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    const toSave = {
      solarDate: result.solarDate,
      solarTime: result.solarTime,
      city: result.city,
      longitude: result.longitude,
      school: result.school,
      shengxiao: result.shengxiao,
      dayGanZhi: result.dayGanZhi,
      bazi: result.bazi,
      updatedAt: new Date().toISOString(),
    };
    fs.writeFileSync(outPath, JSON.stringify(toSave, null, 2), 'utf8');
    console.log(`✅ 已保存到 ${outPath}`);
    console.log('   现在运行 node daily-guide.js 即可享受个人化建议。');
  } finally {
    rl.close();
  }
}

function fromArgs() {
  const args = process.argv.slice(2);
  const get = (k) => { const a = args.find(x => x.startsWith(`--${k}=`)); return a ? a.split('=')[1] : null; };
  const dateStr = get('date');
  const timeStr = get('time');
  if (!dateStr || !timeStr) {
    console.error('参数不完整。用法: node init-bazi.js --date=YYYY-MM-DD --time=HH:MM [--city=城市名|--longitude=经度] [--school=beijing|solar]');
    process.exit(1);
  }
  const city = get('city') || '';
  let longitude = get('longitude') ? parseFloat(get('longitude')) : (CITIES[city] || null);
  const school = get('school') === 'solar' ? 'solar' : 'beijing';
  const result = calcBazi(dateStr, timeStr, longitude, school);
  result.city = city;
  const toSave = {
    solarDate: result.solarDate,
    solarTime: result.solarTime,
    city: result.city,
    longitude: result.longitude,
    school: result.school,
    shengxiao: result.shengxiao,
    dayGanZhi: result.dayGanZhi,
    bazi: result.bazi,
    updatedAt: new Date().toISOString(),
  };
  const outPath = BAZI_JSON;
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(toSave, null, 2), 'utf8');
  console.log(`✅ 已生成 ${outPath}`);
  console.log(`   生肖：${result.shengxiao} | 日柱：${result.dayGanZhi} | 八字：${result.bazi}`);
  if (result.solar) console.log(`   真太阳时参考：${result.solar.bazi}`);
}

// main
if (process.argv.some(a => a.startsWith('--date='))) {
  fromArgs();
} else {
  interactive();
}
