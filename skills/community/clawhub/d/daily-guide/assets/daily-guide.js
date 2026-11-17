#!/usr/bin/env node
/**
 * daily-guide.js — 今日宜出门系统
 *
 * 数据源：
 *  A. lunar-javascript（离线算法，主源/定底本）
 *  B. 天气网万年历 yjs 数据（交叉校验源）
 *  C. wttr.in 天气
 *
 * 个人化：读取本地命理档案（生肖/八字），检查本命冲日
 *
 * 用法：
 *   node daily-guide.js [YYYY-MM-DD] [--json]
 *   默认今天；--json 输出结构化 JSON
 */
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

// ---------- 路径 ----------
const TMP_DIR = path.join(__dirname);
const YJS_CACHE = path.join(TMP_DIR, 'cache', 'yjs');
// 用户个人档案存到 home（不在 skill 目录，避免发布/同步泄露）
const BAZI_JSON = process.env.DAILY_GUIDE_BAZI || path.join(require('os').homedir(), '.daily-guide', 'bazi.json');

// ---------- lunar-javascript ----------
let Lunar;
try {
  ({ Lunar } = require('lunar-javascript'));
} catch (e) {
  console.error('缺少 lunar-javascript，请在目录执行: npm install lunar-javascript');
  process.exit(1);
}

// ---------- 命理档案 ----------
function loadBazi() {
  // 优先：用户配置 bazi.json（init-bazi.js 生成，存于用户 home）
  const jsonPath = BAZI_JSON;
  try {
    if (fs.existsSync(jsonPath)) {
      const j = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      return {
        shengxiao: j.shengxiao || '龙',
        dayGanZhi: j.dayGanZhi || '甲辰',
        bazi: j.bazi || '',
        raw: JSON.stringify(j),
        needsInit: false,
      };
    }
  } catch (e) { /* 继续回退 */ }
  // 兼容：本地 memory/bazi.md（旧版专用，需显式开启 DAILY_GUIDE_LEGACY=1）
  if (process.env.DAILY_GUIDE_LEGACY === '1') {
    const baziPath = path.join(TMP_DIR, '..', '..', '..', 'memory', 'bazi.md');
    try {
      const txt = fs.readFileSync(baziPath, 'utf8');
      const shengxiao = (txt.match(/生肖[：:]\s*(\S+)/) || [])[1] || '龙';
      const bazi = (txt.match(/\*\*北京时间派（主用）\*\*.*?\|\s*([\u4e00-\u9fa5]{2})\s*\|\s*([\u4e00-\u9fa5]{8})/) || []);
      return {
        shengxiao,
        dayGanZhi: bazi[2] ? bazi[2].substring(4, 6) : '甲辰', // 日柱
        raw: txt,
        needsInit: false,
      };
    } catch (e) { /* 继续 */ }
  }
  // 都没有：需要初始化引导
  return { shengxiao: '龙', dayGanZhi: '甲辰', raw: '', needsInit: true };
}

// ---------- 黄历主源 (lunar) ----------
function getLunarData(date) {
  const d = Lunar.fromDate(date);
  return {
    source: 'lunar-javascript',
    lunarDate: d.toString(),
    lunarDay: d.getDayInChinese(),
    ganZhi: `${d.getYearInGanZhi()}年 ${d.getMonthInGanZhi()}月 ${d.getDayInGanZhi()}日`,
    yi: d.getDayYi(),
    ji: d.getDayJi(),
    jishen: d.getDayJiShen(),
    xiongsha: d.getDayXiongSha(),
    chong: d.getDayChongDesc(),     // 冲(甲子)鼠
    chongShengXiao: d.getDayChongShengXiao(),
    sha: d.getDaySha(),              // 煞北
    naYin: d.getDayNaYin(),
    pengZu: `${d.getPengZuGan()}，${d.getPengZuZhi()}`,
    shengxiao: d.getDayShengXiao(),
    jieQi: d.getCurrentJieQi ? d.getCurrentJieQi() : '',
    xiu: d.getXiu ? d.getXiu() : '',
    zheng: d.getZheng ? d.getZheng() : '',
    jianChu: d.getZhiXing ? d.getZhiXing() : '',
    twelveStar: d.getDayTianShen ? d.getDayTianShen() : '',
    lucky: d.getDayTianShenLuck ? d.getDayTianShenLuck() : '',
  };
}

// ---------- 交叉校验源 (天气网万年历 yjs) ----------
async function getTianqiData(dateStr) {
  const year = dateStr.substring(0, 4);
  const mmdd = dateStr.substring(5).replace('-', '');
  const cacheFile = path.join(YJS_CACHE, `${year}.js`);
  try {
    if (!fs.existsSync(cacheFile)) {
      fs.mkdirSync(path.dirname(cacheFile), { recursive: true });
      const url = `https://staticwnl.tianqistatic.com/Home/js/api/yjs/${year}.js`;
      const js = execSync(`curl.exe -sL --max-time 20 "${url}"`, { encoding: 'utf8', maxBuffer: 5 * 1024 * 1024 });
      fs.writeFileSync(cacheFile, js);
    }
    const js = fs.readFileSync(cacheFile, 'utf8');
    const key = `d${mmdd}`;
    const m = js.match(new RegExp(`"${key}":\\{([^}]+)\\}`));
    if (!m) return { source: 'tianqi', error: '未找到当日数据' };
    const raw = m[1];
    const pick = (k) => {
      const mm = raw.match(new RegExp(`"${k}":\\[([^\\]]*)\\]`));
      return mm ? JSON.parse('[' + mm[1] + ']') : null;
    };
    const pickStr = (k) => {
      const mm = raw.match(new RegExp(`"${k}":"([^"]*)"`));
      return mm ? mm[1] : '';
    };
    return {
      source: 'tianqi-wannianli',
      yi: pick('y'),
      ji: pick('j'),
      chong: pickStr('c'),
      sha: pickStr('s'),
      zhi: pickStr('zh'),       // 建除十二神
      jishen: pickStr('yq'),    // 吉神宜趋
      xiongsha: pickStr('yj'),  // 凶煞宜忌
      tai: pickStr('ts'),       // 胎神
    };
  } catch (e) {
    return { source: 'tianqi', error: e.message };
  }
}

// ---------- 天气 (wttr.in) ----------
// 城市可配置：环境变量 DAILY_GUIDE_CITY，默认空（wttr.in 按 IP 定位）
const WEATHER_CITY = process.env.DAILY_GUIDE_CITY || '';
async function getWeather() {
  try {
    const loc = WEATHER_CITY ? `${encodeURIComponent(WEATHER_CITY)}?` : '?';
    const out = execSync(`curl.exe -sL --max-time 15 "https://wttr.in/${loc}format=j1"`, { encoding: 'utf8', maxBuffer: 5 * 1024 * 1024 });
    const j = JSON.parse(out);
    const c = j.current_condition[0];
    const t = j.weather[0];
    return {
      temp: c.temp_C,
      feels: c.FeelsLikeC,
      desc: c.weatherDesc[0].value,
      humidity: c.humidity,
      wind: c.windspeedKmph,
      windDir: c.winddir16Point,
      precip: c.precipMM,
      uv: c.uvIndex,
      max: t.maxtempC,
      min: t.mintempC,
    };
  } catch (e) {
    return { error: e.message };
  }
}

// ---------- 综合裁决 ----------
// 事务分类：大事（择吉）/ 必要事务（实用性优先）/ 休闲出行
const BIG_EVENTS = ['嫁娶', '结婚', '订婚', '领证', '入宅', '搬家', '签约', '合同', '动土', '开工', '开业', '开张', '安葬', '下葬', '买大件', '购车', '买房', '装修开工', '重要决策', '换手机', '换机', '大额', '换工作', '跳槽', '投资', '借钱', '贷款', '大家电', '冰箱', '电视'];
const NECESSARY = ['修手机', '修理', '维修', '送修', '看病', '买药', '拿药', '缴', '交费', '缴费', '办事', '取件', '寄件', '加油', '买菜', '超市', '购物', '日用品', '理发', '换电', '补胎', '检查'];
// 安装类：需要看宜作灶/宜修造
const INSTALL_EVENTS = ['燃气灶', '油烟机', '灶台', '安装', '装灶', '修造', '装修'];
// 日常消费：只需避开忌交易/冲鼠
const DAILY_SHOP = ['裤子', '衣服', '鞋', '日用', '小家电', '扫地机', '扫地机器人', '零食', '杂物'];

function classifyMatter(q) {
  if (!q) return { type: 'general', keyword: '' };
  for (const k of INSTALL_EVENTS) if (q.includes(k)) return { type: 'install', keyword: k };
  for (const k of BIG_EVENTS) if (q.includes(k)) return { type: 'big', keyword: k };
  for (const k of NECESSARY) if (q.includes(k)) return { type: 'necessary', keyword: k };
  for (const k of DAILY_SHOP) if (q.includes(k)) return { type: 'daily', keyword: k };
  return { type: 'general', keyword: '' };
}

// 时辰宜忌（返回推荐出行时段）
function getTimeSlots(date) {
  const slots = [];
  for (let h = 0; h < 24; h += 2) {
    const t = Lunar.fromDate(new Date(date.getFullYear(), date.getMonth(), date.getDate(), h, 30, 0));
    slots.push({
      label: `${String(h).padStart(2, '0')}-${String(h + 1).padStart(2, '0')}`,
      ganZhi: t.getTimeInGanZhi(),
      yi: t.getTimeYi(),
      ji: t.getTimeJi(),
    });
  }
  return slots;
}

function bestTimes(slots, keywords) {
  const good = [], bad = [];
  for (const s of slots) {
    const hasYi = s.yi.some(y => keywords.some(k => y.includes(k)));
    const hasJi = s.ji.some(j => keywords.some(k => j.includes(k)));
    if (hasYi && !hasJi) good.push(s.label);
    else if (hasJi && !hasYi) bad.push(s.label);
  }
  return { good, bad };
}

function decide(lunar, tq, weather, bazi, weekday, matter) {
  const chongMe = lunar.chongShengXiao === bazi.shengxiao;
  const yi = lunar.yi || [];
  const ji = lunar.ji || [];
  const isYiChuXing = yi.includes('出行') || yi.includes('旅游') || yi.includes('远行');
  const isJiChuXing = ji.includes('出行') || ji.includes('旅游');
  const tqYi = tq.yi || [];
  const tqJi = tq.ji || [];
  const tqAllBad = tqJi && tqJi.includes('诸事不宜');
  const tqYiChuXing = tqYi.includes('出行') || tqYi.includes('旅游');
  const tqJiChuXing = tqJi.includes('出行') || tqJi.includes('旅游');

  // 恶劣天气检测
  let weatherBad = false, weatherNote = [];
  if (weather) {
    const desc = weather.desc || '';
    if (/雨|雪|雷|雹/.test(desc) && parseFloat(weather.precip) > 3) { weatherBad = true; weatherNote.push(`有${desc}，降水${weather.precip}mm`); }
    if (parseInt(weather.feels) >= 37) { weatherBad = true; weatherNote.push(`体感${weather.feels}°C 高温`); }
    if (parseInt(weather.wind) >= 40) { weatherBad = true; weatherNote.push(`风速${weather.wind}km/h`); }
    if (parseInt(weather.uv) >= 10) { weatherNote.push(`紫外线${weather.uv} 强`); }
    if (weatherNote.length === 0) weatherNote.push(`天气尚可（${weather.desc} ${weather.temp}°C）`);
  }

  // 主源基调
  let base = 'neutral';
  if (isYiChuXing) base = 'good';
  if (isJiChuXing) base = 'bad';
  if (chongMe) { base = base === 'bad' ? 'bad' : 'caution'; }

  // 事务类型调整：必要事务降权（实用性优先）
  const matterType = matter ? matter.type : 'general';
  if (matterType === 'necessary' && base === 'bad') base = 'caution';
  if (matterType === 'necessary' && base === 'neutral') base = 'good';
  // 安装类：作灶/修造相关，值神吉则 good
  if (matterType === 'install' && base === 'neutral') base = 'good';

  // 交叉源分歧
  let conflict = null;
  if (tq && !tq.error) {
    if (tqAllBad && (isYiChuXing || base === 'good')) {
      conflict = 'tianqi-all-bad';
    } else if (tqJiChuXing && isYiChuXing) {
      conflict = 'tianqi-ji-chuxing';
    } else if (tqYiChuXing && isJiChuXing) {
      conflict = 'tianqi-yi-chuxing';
    }
  }

  // 天气改判
  let verdict = base;
  let verdictText = '';
  if (matterType === 'necessary') {
    // 必要事务：实用性优先，天气只提醒不否决
    if (verdict === 'good') verdictText = '必要事务照常办理，天气配合'; 
    else if (verdict === 'caution') verdictText = '必要事务可办理（黄历提示谨慎，但事不宜迟）';
    else if (verdict === 'bad') verdictText = '黄历不利，但属必要事务，建议选吉时办理';
    else verdictText = '属必要事务，建议办理';
  } else {
    if (weatherBad && verdict === 'good') { verdict = 'caution'; verdictText = '黄历宜出行，但天气恶劣，建议谨慎出行'; }
    else if (weatherBad && verdict === 'caution') { verdictText = '天气恶劣叠加黄历警示，不建议出门'; }
    else if (verdict === 'good') { verdictText = '黄历宜出行，天气配合，适合出门'; }
    else if (verdict === 'bad') { verdictText = '黄历忌出行，建议居家或改为室内活动'; }
    else if (verdict === 'caution') { verdictText = '黄历可出行但需注意（本命冲日或天气欠佳）'; }
  }

  return {
    chongMe,
    base,
    verdict,
    verdictText,
    conflict,
    isYiChuXing,
    isJiChuXing,
    weatherBad,
    weatherNote,
    weekday,
    matterType,
  };
}

// ---------- 输出 ----------
function renderHuman(r) {
  const d = r.dateStr;
  const wd = ['日','一','二','三','四','五','六'][r.date.getDay()];
  const isWeekend = r.date.getDay() === 0 || r.date.getDay() === 6;
  const matter = r.matter;
  const matterType = r.decide.matterType;
  const lines = [];
  lines.push(`📅 ${d} 周${wd} | ${r.lunar.lunarDate} | 生肖：${r.lunar.shengxiao}`);
  lines.push(`   干支：${r.lunar.ganZhi} | 纳音：${r.lunar.naYin}`);
  lines.push('');
  lines.push('📋 黄历（主源：lunar-javascript）');
  lines.push(`  宜：${r.lunar.yi.join('、')}`);
  lines.push(`  忌：${r.lunar.ji.join('、')}`);
  lines.push(`  吉神：${r.lunar.jishen.join('、')}`);
  lines.push(`  凶煞：${r.lunar.xiongsha.join('、')}`);
  lines.push(`  冲：${r.lunar.chong} | 煞：${r.lunar.sha}`);
  lines.push(`  彭祖百忌：${r.lunar.pengZu}`);
  lines.push(`  建除十二神：${r.lunar.jianChu} | 值神：${r.lunar.twelveStar}(${r.lunar.lucky})`);
  lines.push('');
  if (r.tq && !r.tq.error) {
    lines.push('🔄 交叉校验（天气网万年历）');
    lines.push(`  宜：${r.tq.yi.join('、')}`);
    lines.push(`  忌：${r.tq.ji.join('、')}`);
    lines.push(`  建除：${r.tq.zhi} | 吉神：${r.tq.jishen} | 凶煞：${r.tq.xiongsha}`);
    lines.push(`  冲：${r.tq.chong} | 煞：${r.tq.sha}`);
    if (r.decide.conflict) {
      const cf = r.decide.conflict;
      if (cf === 'tianqi-all-bad') lines.push('  ⚠️ 分歧：主源宜出行，但交叉源判定【诸事不宜】');
      else if (cf === 'tianqi-ji-chuxing') lines.push('  ⚠️ 分歧：主源宜出行，交叉源忌出行');
      else if (cf === 'tianqi-yi-chuxing') lines.push('  ⚠️ 分歧：主源忌出行，交叉源宜出行');
    } else {
      lines.push('  ✅ 两源无冲突');
    }
    lines.push('');
  }
  if (r.weather) {
    lines.push(`🌤️ 天气${WEATHER_CITY ? `（${WEATHER_CITY}）` : ''}`);
    lines.push(`  ${r.weather.desc} ${r.weather.temp}°C，体感${r.weather.feels}°C，湿度${r.weather.humidity}%，风${r.weather.windDir}${r.weather.wind}km/h，紫外线${r.weather.uv}`);
    lines.push(`  今日：${r.weather.min}~${r.weather.max}°C`);
    lines.push('');
  }
  lines.push('🧭 出门建议');
  if (r.bazi && r.bazi.needsInit) {
    lines.push('  ⚠️ 未配置个人档案：当前为通用模式（默认属鼠）');
    lines.push('  💡 运行 `node init-bazi.js` 输入出生信息，即可获得本命冲日等个人化建议');
  }
  if (matter) {
    if (matterType === 'big') lines.push(`  📌 事项「${matter.keyword}」属择吉大事，黄历权重高，谨慎安排`);
    else if (matterType === 'necessary') lines.push(`  📌 事项「${matter.keyword}」属必要事务，实用性优先，黄历降权参考`);
    else if (matterType === 'install') lines.push(`  📌 事项「${matter.keyword}」属安装类，宜选「作灶/修造」吉日（值神吉为佳）`);
    else if (matterType === 'daily') lines.push(`  📌 事项「${matter.keyword}」属日常消费，避开忌交易/冲鼠即可`);
    else lines.push(`  📌 事项「${matter.keyword}」属日常出行`);
  }
  if (r.decide.chongMe) lines.push(`  ⚠️ 今日冲【${r.lunar.chongShengXiao}】，你属${r.bazi.shengxiao}，本命冲日！`);
  r.decide.weatherNote.forEach(n => lines.push(`  • ${n}`));
  lines.push(`  • ${r.decide.verdictText}`);
  if (isWeekend) {
    lines.push(`  • ${r.decide.verdict === 'good' ? '周末宜出游' : r.decide.verdict === 'bad' ? '周末宜宅家，可改室内活动' : '周末出行需谨慎安排'}`);
  } else {
    lines.push(`  • 今天是工作日，通勤照常，${r.decide.weatherBad ? '注意天气带伞/防暑' : '通勤顺利'}`);
  }
  // 时辰建议
  const slots = r.slots || [];
  if (slots.length && (matterType === 'necessary' || matterType === 'general')) {
    const kw = matterType === 'necessary' ? ['出行', '求财', '交易', '修造', '开市'] : ['出行'];
    const { good, bad } = bestTimes(slots, kw);
    if (good.length) lines.push(`  🕓 推荐时段：${good.join('、')}（宜出行/办事）`);
    if (bad.length) lines.push(`  ⚠️ 避开时段：${bad.join('、')}（忌出行）`);
  }
  return lines.join('\n');
}

// ---------- main ----------
async function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const dateArg = args.find(a => /^\d{4}-\d{2}-\d{2}$/.test(a));
  // 事项文本：--matter=修手机 或 最后一个非 flag 参数
  const matterArg = (args.find(a => a.startsWith('--matter=')) || '').split('=')[1] || '';
  const date = dateArg ? new Date(dateArg + 'T12:00:00') : new Date();
  const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;

  const bazi = loadBazi();
  const lunar = getLunarData(date);
  const slots = getTimeSlots(date);
  const matter = classifyMatter(matterArg) || null;
  const [tq, weather] = await Promise.all([getTianqiData(dateStr), getWeather()]);
  const decideResult = decide(lunar, tq, weather, bazi, date.getDay(), matter);

  const result = { dateStr, lunar, tq, weather, bazi: { shengxiao: bazi.shengxiao, dayGanZhi: bazi.dayGanZhi, needsInit: bazi.needsInit }, decide: decideResult, matter: matterArg ? matter : null, slots };
  if (jsonMode) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(renderHuman({ ...result, date }));
  }
}

main().catch(e => { console.error(e); process.exit(1); });
