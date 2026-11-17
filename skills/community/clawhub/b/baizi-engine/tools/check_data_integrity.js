/**
 * 数据表完整性门禁（v1.3.15 新增）
 *
 * 为什么需要：引擎里有三张**手工维护**的大表，任何一个字打错都会静默算错盘、且现有 14 套回归都碰不到：
 *   ① `CITY_LON`（724 城经度）—— 决定真太阳时校正量。历史上真错过一次：
 *      「津市市」以去"市"后的"津市"命中"天津市"，键长更长导致天津市经度被解析为 111.9°
 *      （正确 117.2°），真太阳时偏 21 分钟。现在门禁同时验"自解析"与"权威数值"两件事——
 *      只验自解析是不够的：把一个值整体改错，它仍然"自己等于自己"。
 *   ② `LUNAR_INFO`（1900-2099 农历十六进制表）—— 一个月长写错，全年日期整体错位。
 *   ③ `JIEQI.data`（1895-2100 每年 12 个"节"）—— 月柱分界，错一分钟都可能换柱。
 *
 * 判据（全部来自权威万年历/标准地理坐标，且已用当前数据校准过，不产生误报）：
 *   · CITY_LON：724 键逐个"喂回自己"必须解析回自己的经度；经度落在 70~140°E；35 个知名城市
 *     与权威坐标误差 ≤ 0.8°（这个容差足以抓住当年那个 5.3° 的错误，又留有城市中心点差异的余量）。
 *   · 农历：闰月 ∈ [0,12]、闰月天数 ∈ {0,29,30}、月长 ∈ {29,30}、年长 ∈ [353,385]、
 *     春节落在 1/21~2/21、逐年递增且间隔 ∈ [353,385]、**逐月首日递推必须自洽**（差一天即报错）、
 *     6 个权威春节真值 + 6 个权威闰月真值。
 *   · 节气：206 年连续、每年恰好 12 项、月份序列必须精确为 02..12,01、格式 `MM-DD HH:MM`、
 *     年内（02→12）严格递增。
 *
 * 自检（`--self-test`）：向三张表各注入一处故障，断言检查器必须报错——**证明这道门禁不是空转的**。
 *   门禁最大的风险不是漏检，是"永远不会失败"（写错了判据也照样绿）。
 *
 * 用法：node tools/check_data_integrity.js [--self-test]
 */
const path = require('path');
const ENGINE = path.join(__dirname, '..', 'engine', 'engine.dist.js');
const D = require(ENGINE);

const JIEQI_MONTH_PATTERN = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '01'];
const JIEQI_RE = /^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):[0-5][0-9]$/;

// 权威城市坐标（°E）。容差 0.8°：足以抓住 5.3° 级别的错值，又容得下"城市中心点"的取法差异。
const CITY_TRUTH = [
  ['北京', 116.4], ['上海', 121.5], ['广州', 113.3], ['天津', 117.2], ['重庆', 106.5],
  ['乌鲁木齐', 87.6], ['喀什', 75.9], ['哈尔滨', 126.6], ['拉萨', 91.1], ['三亚', 109.5],
  ['深圳', 114.1], ['成都', 104.1], ['武汉', 114.3], ['西安', 108.9], ['昆明', 102.7],
  ['兰州', 103.8], ['沈阳', 123.4], ['青岛', 120.4], ['杭州', 120.2], ['南京', 118.8],
  ['郑州', 113.6], ['长沙', 113.0], ['福州', 119.3], ['海口', 110.3], ['银川', 106.3],
  ['西宁', 101.8], ['呼和浩特', 111.7], ['南昌', 115.9], ['合肥', 117.3], ['贵阳', 106.6],
  ['南宁', 108.4], ['石家庄', 114.5], ['太原', 112.5], ['长春', 125.3], ['济南', 117.0],
];
const CITY_TOLERANCE = 0.8;

// 权威农历真值：春节（农历正月初一 → 阳历）
const CNY_TRUTH = [
  [1900, 1, 31], [1990, 1, 27], [2000, 2, 5], [2023, 1, 22], [2024, 2, 10], [2025, 1, 29],
];
// 权威闰月真值：[年, 闰几月]
const LEAP_TRUTH = [[1900, 8], [1990, 5], [2000, 0], [2020, 4], [2023, 2], [2025, 6], [2033, 11]];

const DAY = 86400000;
// 必须用 Date.UTC：1900 年上海是 LMT +08:05:43（IANA tzdata），用本地时区构造会把天差算成 14.0039699…，
// 看起来像"数据错一天"，实际是判据自己引入了时区偏移。
const dayNum = (o) => Date.UTC(o.y, o.m - 1, o.d) / DAY;

function checkCity(D) {
  const issues = [];
  const keys = Object.keys(D.CITY_LON);
  if (keys.length < 700) issues.push(`CITY_LON 城市数仅 ${keys.length}（应 ≥700）`);
  const stamp = new Date(1990, 0, 1, 12, 0);
  for (const k of keys) {
    const v = D.CITY_LON[k];
    if (typeof v !== 'number' || !Number.isFinite(v)) { issues.push(`CITY_LON["${k}"] 非数值: ${v}`); continue; }
    if (v < 70 || v > 140) issues.push(`CITY_LON["${k}"]=${v} 超出中国经度范围 70~140°E`);
    const c = D.solarCorrection(k, stamp);
    if (!c || !c.found) { issues.push(`城市「${k}」喂回 solarCorrection 未命中`); continue; }
    if (Math.abs(c.lon - v) > 1e-9)
      issues.push(`城市「${k}」自解析到别人的经度：表中 ${v}，解析得 ${c.lon}`);
  }
  for (const [name, expect] of CITY_TRUTH) {
    const c = D.solarCorrection(name, stamp);
    if (!c || !c.found) { issues.push(`权威坐标校验：城市「${name}」未命中`); continue; }
    const d = Math.abs(c.lon - expect);
    if (d > CITY_TOLERANCE)
      issues.push(`城市「${name}」经度偏差 ${d.toFixed(1)}°：期望 ${expect}，实际 ${c.lon}`);
  }
  return { issues, stats: `${keys.length} 城 / 权威校验 ${CITY_TRUTH.length} 个` };
}

function checkLunar(D) {
  const issues = [];
  let prevCny = null, prevYear = null, years = 0;
  for (let y = 1900; y <= 2099; y++) {
    years++;
    const lm = D.leapMonth(y), ld = D.leapDays(y);
    if (!(lm >= 0 && lm <= 12)) issues.push(`${y} 年 leapMonth=${lm} 非法（应 0~12）`);
    if (![0, 29, 30].includes(ld)) issues.push(`${y} 年 leapDays=${ld} 非法（应 0/29/30）`);
    if ((lm === 0) !== (ld === 0)) issues.push(`${y} 年闰月与闰月天数不一致：leapMonth=${lm} leapDays=${ld}`);
    let total = 0;
    for (let m = 1; m <= 12; m++) {
      const md = D.monthDays(y, m);
      if (md !== 29 && md !== 30) issues.push(`${y}-${m} 月长 ${md} 非法（应 29/30）`);
      total += md;
    }
    total += ld;
    if (total < 353 || total > 385) issues.push(`${y} 年长 ${total} 天越界（应 353~385）`);

    const cny = D.lunarToSolar(y, 1, 1, false);
    if (!cny) { issues.push(`${y} 年春节 lunarToSolar 返回 null`); continue; }
    const inWindow = (cny.m === 1 && cny.d >= 21) || (cny.m === 2 && cny.d <= 21);
    if (!inWindow) issues.push(`${y} 年春节落在 ${cny.m}-${cny.d}（应在 1/21~2/21）`);
    const n = dayNum(cny);
    if (prevCny !== null) {
      const gap = n - prevCny;
      if (gap <= 0) issues.push(`${prevYear}→${y} 春节未递增`);
      else if (gap < 353 || gap > 385) issues.push(`${prevYear}→${y} 春节间隔 ${gap} 天越界（应 353~385）`);
    }
    prevCny = n; prevYear = y;

    // 逐月首日递推自洽：本月首日 − 上月首日 === 上月天数（+ 闰月天数）
    let prevFirst = null, prevExpect = null;
    for (let m = 1; m <= 12; m++) {
      const f = D.lunarToSolar(y, m, 1, false);
      if (!f) { issues.push(`${y}-${m} 初一 lunarToSolar 返回 null`); break; }
      const t = dayNum(f);
      if (prevFirst !== null) {
        const gap = t - prevFirst;
        if (gap !== prevExpect) issues.push(`${y} 年 ${m} 月初一与上月间隔 ${gap} 天（应为 ${prevExpect}）`);
      }
      prevFirst = t; prevExpect = D.monthDays(y, m);
      if (m === lm) {
        const lf = D.lunarToSolar(y, m, 1, true);
        if (!lf) { issues.push(`${y} 年闰 ${m} 月初一返回 null`); break; }
        const lt = dayNum(lf);
        const g2 = lt - t;
        if (g2 !== D.monthDays(y, m)) issues.push(`${y} 年闰 ${m} 月与本月间隔 ${g2} 天（应为 ${D.monthDays(y, m)}）`);
        prevFirst = lt; prevExpect = ld;
      }
      // 月内日期偏移：d 日 = 初一 + (d−1)。末日一律取**本正常月**的天数，
      // 不能用 prevExpect（闰月年它已被改写为闰月天数，会拿闰月长度去查正常月 → 假报错）。
      const firstN = D.lunarToSolar(y, m, 1, false);
      for (const d of [1, 15, D.monthDays(y, m)]) {
        const dt = D.lunarToSolar(y, m, d, false);
        if (!dt) { issues.push(`${y}-${m}-${d} lunarToSolar 返回 null`); continue; }
        const off = dayNum(dt) - dayNum(firstN);
        if (off !== d - 1) issues.push(`${y}-${m}-${d} 相对初一偏移 ${off} 天（应为 ${d - 1}）`);
      }
    }
  }
  for (const [y, m, d] of CNY_TRUTH) {
    const s = D.lunarToSolar(y, 1, 1, false);
    if (!s || s.y !== y || s.m !== m || s.d !== d)
      issues.push(`权威春节真值不符：农历 ${y}-1-1 得 ${s ? `${s.y}-${s.m}-${s.d}` : 'null'}，应为 ${y}-${m}-${d}`);
  }
  for (const [y, lm] of LEAP_TRUTH) {
    if (D.leapMonth(y) !== lm) issues.push(`权威闰月真值不符：${y} 年闰月应为 ${lm || '无'}，实际 ${D.leapMonth(y)}`);
  }
  return { issues, stats: `${years} 年 / 春节真值 ${CNY_TRUTH.length} / 闰月真值 ${LEAP_TRUTH.length}` };
}

function checkJieqi(D) {
  const issues = [];
  const years = Object.keys(D.JIEQI.data).map(Number).sort((a, b) => a - b);
  const [lo, hi] = D.JIEQI.range;
  if (years.length !== hi - lo + 1)
    issues.push(`节气年数 ${years.length}，与 range [${lo},${hi}] 不匹配（应 ${hi - lo + 1}）`);
  for (let i = 1; i < years.length; i++) {
    if (years[i] !== years[i - 1] + 1) { issues.push(`节气年份不连续：${years[i - 1]} → ${years[i]}`); break; }
  }
  for (const y of years) {
    const arr = D.JIEQI.data[y];
    if (!Array.isArray(arr) || arr.length !== 12) { issues.push(`${y} 年节气项数 ${arr && arr.length}（应 12）`); continue; }
    const months = arr.map(s => String(s).slice(0, 2));
    if (months.join(',') !== JIEQI_MONTH_PATTERN.join(','))
      issues.push(`${y} 年节气月份序列异常：${months.join(' ')}`);
    arr.forEach((s, i) => {
      if (!JIEQI_RE.test(String(s))) issues.push(`${y} 年第 ${i} 项格式异常：${s}`);
    });
    for (let i = 0; i < 10; i++) {              // 02(立春) → 12(大雪) 年内必须递增
      if (String(arr[i]) >= String(arr[i + 1])) {
        issues.push(`${y} 年节气未递增：${arr[i]} 之后是 ${arr[i + 1]}`);
        break;
      }
    }
  }
  return { issues, stats: `${years.length} 年 × 12 节（${lo}~${hi}）` };
}

function runAll(D) {
  return { city: checkCity(D), lunar: checkLunar(D), jieqi: checkJieqi(D) };
}

function report(label, r) {
  console.log(`  ${r.issues.length === 0 ? '✅' : '❌'} ${label}  [${r.stats}]`);
  r.issues.slice(0, 6).forEach(s => console.log('       · ' + s));
  if (r.issues.length > 6) console.log(`       · …共 ${r.issues.length} 处`);
}

function selfTest() {
  console.log('=== 自检：向三张表注入故障，检查器必须报错 ===');
  const snapshot = {
    city: D.CITY_LON['天津'],
    lunarLeap: D.LUNAR_INFO[2000 - 1900],
    lunarBit: D.LUNAR_INFO[1900 - 1900],
    jieqi: D.JIEQI.data['1990'].slice(),
  };
  let bad = 0;
  const expect = (name, mutate, restore, pick) => {
    mutate();
    const r = runAll(D);
    const caught = pick(r).issues.length > 0;
    restore();
    console.log(`  ${caught ? '✅' : '❌'} ${name} → ${caught ? '已抓到' : '未抓到（门禁失效！）'}`);
    if (!caught) bad++;
  };

  // ① 经度值改错（自解析仍成立，只有"权威数值"判据能抓到 —— 证明两件事都要验）
  expect('经度值被改错（天津 117.2 → 111.9，即历史真实事故）',
    () => { D.CITY_LON['天津'] = 111.9; },
    () => { D.CITY_LON['天津'] = snapshot.city; },
    r => r.city);

  // ② 闰月字段被写坏
  expect('闰月字段被写坏（2000 年 leapMonth → 15）',
    () => { D.LUNAR_INFO[2000 - 1900] |= 0xf; },
    () => { D.LUNAR_INFO[2000 - 1900] = snapshot.lunarLeap; },
    r => r.lunar);

  // ③ 月长位被翻转
  expect('月长位被翻转（1900 年某月 30↔29）',
    () => { D.LUNAR_INFO[1900 - 1900] ^= 0x1; },
    () => { D.LUNAR_INFO[1900 - 1900] = snapshot.lunarBit; },
    r => r.lunar);

  // ④ 节气少一项
  expect('节气少一项（1990 年删掉第 4 项）',
    () => { D.JIEQI.data['1990'].splice(3, 1); },
    () => { D.JIEQI.data['1990'] = snapshot.jieqi; },
    r => r.jieqi);

  console.log(bad === 0 ? '\n✅ 自检通过：4 处注入故障全部被抓到，门禁有效' : `\n❌ 自检失败：${bad} 处注入故障未被抓到`);
  return bad === 0 ? 0 : 1;
}

if (process.argv.includes('--self-test')) process.exit(selfTest());

console.log('数据表完整性检查：');
const r = runAll(D);
report('城市经度表 CITY_LON（自解析 + 权威坐标）', r.city);
report('农历表 LUNAR_INFO（结构 + 递推 + 权威真值）', r.lunar);
report('节气表 JIEQI.data（结构 + 格式 + 递增）', r.jieqi);
const total = r.city.issues.length + r.lunar.issues.length + r.jieqi.issues.length;
console.log(total === 0
  ? '\n✅ 三张手工维护的数据表结构完整、数值可信'
  : `\n❌ 数据表存在 ${total} 处问题`);
process.exit(total === 0 ? 0 : 1);
