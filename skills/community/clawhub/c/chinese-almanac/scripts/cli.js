#!/usr/bin/env node
/**
 * Chinese Almanac CLI (三语版)
 * 古典择日 — 协纪辨方书体系
 */

const i18n = require('../lib/i18n');

// ═══════════════════════════════════════════════
// 天干地支常量
// ═══════════════════════════════════════════════
const GAN = i18n.stems;
const ZHI = i18n.branches;
const CHONG = { '子':'午','丑':'未','寅':'申','卯':'酉','辰':'戌','巳':'亥','午':'子','未':'丑','申':'寅','酉':'卯','戌':'辰','亥':'巳' };

// ═══════════════════════════════════════════════
// 建除十二神
// ═══════════════════════════════════════════════
const JIANCHU = ['建','除','满','平','定','执','破','危','成','收','开','闭'];

const YIJI = {
  '建': { yi: ['出行','上任','祭祀','求财'],         ji: ['嫁娶','动土','破土','安葬'] },
  '除': { yi: ['扫除','解除','移徙','沐浴'],         ji: ['嫁娶','破土','安葬','入殓'] },
  '满': { yi: ['嫁娶','开业','纳财','入宅'],         ji: ['出行','动土','破土','诉讼'] },
  '平': { yi: ['出行','移徙','求医','上任'],         ji: ['嫁娶','安葬','破土'] },
  '定': { yi: ['嫁娶','开业','签约','求财'],         ji: ['出行','诉讼','动土'] },
  '执': { yi: ['祭祀','纳财','捕猎','捉贼'],         ji: ['开业','嫁娶','移徙','出行'] },
  '破': { yi: [],                                   ji: ['开业','嫁娶','出行','移徙','动土','签约'] },
  '危': { yi: ['祭祀'],                             ji: ['出行','登高','嫁娶','开业'] },
  '成': { yi: ['开业','嫁娶','移徙','上任','出行'], ji: ['诉讼','破土'] },
  '收': { yi: ['纳财','收获','祭祀'],               ji: ['出行','嫁娶','动土','开业'] },
  '开': { yi: ['开业','嫁娶','出行','求财','移徙'], ji: ['入殓','安葬','破土'] },
  '闭': { yi: ['入殓','安葬','封穴'],               ji: ['开业','嫁娶','出行','动土'] },
};

// ═══════════════════════════════════════════════
// 黄道黑道十二神
// ═══════════════════════════════════════════════
const HUANGHEI = {
  yellow: ['青龙','明堂','金匮','天德','玉堂','司命'],
  black: ['天刑','朱雀','白虎','天牢','玄武','勾陈'],
};

function getHuangHei(dayZhiIdx, monthZhiIdx) {
  const idx = (dayZhiIdx - monthZhiIdx + 12) % 12;
  if (idx % 2 === 0) {
    return { type: 'yellow', star: HUANGHEI.yellow[Math.floor(idx / 2)] };
  } else {
    return { type: 'black', star: HUANGHEI.black[Math.floor(idx / 2)] };
  }
}

// ═══════════════════════════════════════════════
// 活动评分
// ═══════════════════════════════════════════════
const ACTIVITY_SCORES = {
  'marriage':   { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'business':   { '开': 10, '成': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'move':       { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'sign':       { '成': 10, '开': 8, '定': 6, '满': 4, '除': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'travel':     { '开': 10, '成': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'renovate':   { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'worship':    { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'wealth':     { '开': 10, '成': 8, '满': 6, '除': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'start_job':  { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
  'engagement': { '成': 10, '开': 8, '除': 6, '满': 4, '定': 4, '收': 2, '建': 0, '平': 0, '执': -2, '破': -6, '危': -4, '闭': -4 },
};

// ═══════════════════════════════════════════════
// 核心计算
// ═══════════════════════════════════════════════
function getDayGanZhi(year, month, day) {
  const base = new Date(2024, 0, 1, 12, 0, 0);
  const target = new Date(year, month - 1, day, 12, 0, 0);
  const diff = Math.round((target - base) / 86400000);
  return GAN[((diff % 10) + 10) % 10] + ZHI[((diff % 12) + 12) % 12];
}

function getZhiXing(year, month, day) {
  const monthZhiIdx = month % 12;
  const gz = getDayGanZhi(year, month, day);
  const dayZhiIdx = ZHI.indexOf(gz[1]);
  return JIANCHU[((dayZhiIdx - monthZhiIdx + 12) % 12)];
}

function analyzeDay(year, month, day, activity = 'marriage') {
  const gz = getDayGanZhi(year, month, day);
  const dayGan = gz[0];
  const dayZhi = gz[1];
  const zhiXing = getZhiXing(year, month, day);
  const monthZhiIdx = month % 12;
  const dayZhiIdx = ZHI.indexOf(dayZhi);
  const huangHei = getHuangHei(dayZhiIdx, monthZhiIdx);
  const chong = CHONG[dayZhi];

  const scores = ACTIVITY_SCORES[activity] || ACTIVITY_SCORES['marriage'];
  const baseScore = scores[zhiXing] || 0;

  const huangHeiData = i18n.huangdao[huangHei.type].find(s => s.zh === huangHei.star);
  const jianchuData = i18n.jianchu[zhiXing];

  const pengzuStem = i18n.pengzu.stems[dayGan];
  const pengzuBranch = i18n.pengzu.branches[dayZhi];

  const yi = YIJI[zhiXing]?.yi || [];
  const ji = YIJI[zhiXing]?.ji || [];

  return {
    date: `${year}-${String(month).padStart(2,'0')}-${String(day).padStart(2,'0')}`,
    ganZhi: gz,
    dayGan, dayZhi,
    zhiXing,
    jianchu: jianchuData,
    huangHei: { ...huangHei, data: huangHeiData },
    chong,
    pengzuStem, pengzuBranch,
    yi, ji,
    score: baseScore,
    activity,
  };
}

// ═══════════════════════════════════════════════
// 月份分析
// ═══════════════════════════════════════════════
function analyzeMonth(year, month, activity = 'marriage') {
  const daysInMonth = new Date(year, month, 0).getDate();
  const results = [];
  for (let day = 1; day <= daysInMonth; day++) {
    results.push(analyzeDay(year, month, day, activity));
  }
  return results.sort((a, b) => b.score - a.score);
}

// ═══════════════════════════════════════════════
// CLI
// ═══════════════════════════════════════════════
if (require.main === module) {
  const args = process.argv.slice(2);
  let lang = 'en', json = false, findBest = false, positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--lang' && args[i+1]) { lang = args[++i]; }
    else if (args[i] === '--json') { json = true; }
    else if (args[i] === 'best') { findBest = true; }
    else if (args[i] === '--help' || args[i] === '-h') {
      console.log('Usage: node cli.js [best] <YYYY-MM> <activity> [--lang en|zh|ja] [--json]');
      console.log('Activities: marriage, business, move, sign, travel, renovate, worship, wealth, start_job, engagement');
      process.exit(0);
    }
    else { positional.push(args[i]); }
  }

  if (positional.length < 2) {
    console.log('Usage: node cli.js [best] <YYYY-MM> <activity> [--lang en|zh|ja] [--json]');
    process.exit(1);
  }

  const [yearStr, monthStr] = positional[0].split('-');
  const year = parseInt(yearStr);
  const month = parseInt(monthStr);
  const activity = positional[1];
  const L = i18n.labels[lang] || i18n.labels.en;
  const act = i18n.activities[activity];

  const results = analyzeMonth(year, month, activity);

  if (json) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    console.log(`\n═══ ${L.title} ═══`);
    console.log(`${act.emoji} ${act.en} / ${act.zh} / ${act.ja}`);
    console.log(`${year}-${String(month).padStart(2,'0')}\n`);

    const top = findBest ? results.slice(0, 5) : results;

    for (const r of top) {
      const scoreEmoji = r.score >= 8 ? '🟢' : r.score >= 4 ? '🟡' : r.score >= 0 ? '🟠' : '🔴';
      const huangEmoji = r.huangHei.type === 'yellow' ? '☀️' : '🌑';
      const starInfo = r.huangHei.data ? `${r.huangHei.data.emoji} ${r.huangHei.data.en}` : r.huangHei.star;

      console.log(`${scoreEmoji} ${r.date} [${r.ganZhi}] ${r.jianchu.emoji} ${r.zhiXing}(${r.jianchu.en}) | ${huangEmoji} ${starInfo}`);
      console.log(`   ${L.yi}: ${r.yi.join(', ')} | ${L.ji}: ${r.ji.join(', ')}`);
      console.log(`   ${L.score}: ${r.score >= 0 ? '+' : ''}${r.score}`);
      console.log('');
    }

    if (findBest && results.length > 0) {
      const best = results[0];
      console.log(`\n✨ ${L.bestDate}: ${best.date} [${best.ganZhi}] ${best.jianchu.emoji} ${best.zhiXing}`);
      console.log(`   ${L.score}: ${best.score >= 0 ? '+' : ''}${best.score}`);
    }
  }
}

module.exports = { analyzeDay, analyzeMonth, getDayGanZhi, getZhiXing, i18n };
