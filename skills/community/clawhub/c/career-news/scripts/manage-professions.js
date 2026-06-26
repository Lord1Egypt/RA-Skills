#!/usr/bin/env node
/**
 * career-news — manage-professions.js
 * Add or remove extra profession news subscriptions for a user.
 * Users can subscribe to news from multiple professions beyond their primary one.
 *
 * Usage:
 *   node scripts/manage-professions.js --userId <id> --add <profession>
 *   node scripts/manage-professions.js --userId <id> --remove <profession>
 *   node scripts/manage-professions.js --userId <id> --list
 *   node scripts/manage-professions.js --userId <id> --clear        # remove all extras
 *   node scripts/manage-professions.js --suggest <userId>           # AI prompt: suggest professions for this user
 *
 * Professions: doctor, lawyer, engineer, developer, designer, product-manager,
 *              investor, teacher, journalist, entrepreneur, researcher, marketing, hr, sales
 *
 * Example — a developer who also wants investor and marketing news:
 *   node scripts/manage-professions.js --userId alice --add investor
 *   node scripts/manage-professions.js --userId alice --add marketing
 *   node scripts/manage-professions.js --userId alice --list
 *   → Primary: developer | Subscribed: investor, marketing
 *   → Morning push will deliver 3 separate briefs: developer · investor · marketing
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');

const VALID_PROFESSIONS = new Set([
  'doctor','lawyer','engineer','developer','designer','product-manager',
  'investor','teacher','journalist','entrepreneur','researcher','marketing','hr','sales'
]);

const PROFESSION_ZH_MAP = {
  '医生':'doctor','医疗':'doctor','律师':'lawyer','法律':'lawyer',
  '工程师':'engineer','开发者':'developer','程序员':'developer','开发':'developer',
  '设计师':'designer','设计':'designer','产品经理':'product-manager','产品':'product-manager',
  '投资人':'investor','投资':'investor','金融':'investor','教师':'teacher','教育':'teacher',
  '记者':'journalist','媒体':'journalist','创业者':'entrepreneur','创业':'entrepreneur',
  '研究员':'researcher','学者':'researcher','营销':'marketing','市场':'marketing',
  '人力资源':'hr','销售':'sales'
};

const PROFESSION_LABELS = {
  doctor: '医生/医疗', lawyer: '律师/法律', engineer: '工程师',
  developer: '软件开发者', designer: '设计师', 'product-manager': '产品经理',
  investor: '投资/金融', teacher: '教师/教育', journalist: '记者/媒体',
  entrepreneur: '创业者', researcher: '研究员', marketing: '市场营销',
  hr: '人力资源', sales: '销售'
};

function resolveProf(raw) {
  if (!raw) return null;
  const direct = PROFESSION_ZH_MAP[raw] || (VALID_PROFESSIONS.has(raw) ? raw : null);
  if (direct) return direct;
  for (const [key, val] of Object.entries(PROFESSION_ZH_MAP)) {
    if (raw.includes(key)) return val;
  }
  return null;
}

function loadUser(userId) {
  const safeId = userId.replace(/[^a-zA-Z0-9_-]/g, '');
  const fp = path.join(USERS_DIR, `${safeId}.json`);
  if (!fs.existsSync(fp)) {
    console.error(`User "${userId}" not found. Register first: node scripts/register.js ${userId} --profession <prof>`);
    process.exit(1);
  }
  return { fp, user: JSON.parse(fs.readFileSync(fp, 'utf8')) };
}

function saveUser(fp, user) {
  user.updatedAt = new Date().toISOString();
  fs.writeFileSync(fp, JSON.stringify(user, null, 2));
}

function printSubscriptions(user) {
  const extras = user.extraProfessions || [];
  const allProfs = [user.profession, ...extras].filter(Boolean);
  console.log(`\nUser: ${user.userId}`);
  console.log('─'.repeat(50));
  console.log(`  Primary profession : ${user.profession} (${PROFESSION_LABELS[user.profession] || user.profession})`);
  if (extras.length === 0) {
    console.log(`  Extra subscriptions: (none)`);
  } else {
    extras.forEach((p, i) => {
      console.log(`  Extra #${i+1}           : ${p} (${PROFESSION_LABELS[p] || p})`);
    });
  }
  console.log('─'.repeat(50));
  console.log(`  Total briefs per morning push: ${allProfs.length}`);
  console.log('');
  const available = [...VALID_PROFESSIONS].filter(p => !allProfs.includes(p));
  if (available.length > 0) {
    console.log(`  Available to add: ${available.join(', ')}`);
    console.log(`  → node scripts/manage-professions.js --userId ${user.userId} --add <profession>`);
  }
}

const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage:');
  console.error('  node scripts/manage-professions.js --userId <id> --add <profession>');
  console.error('  node scripts/manage-professions.js --userId <id> --remove <profession>');
  console.error('  node scripts/manage-professions.js --userId <id> --list');
  console.error('  node scripts/manage-professions.js --userId <id> --clear');
  console.error('  node scripts/manage-professions.js --suggest <userId>');
  console.error('');
  console.error('Professions: doctor, lawyer, engineer, developer, designer, product-manager,');
  console.error('             investor, teacher, journalist, entrepreneur, researcher, marketing, hr, sales');
  process.exit(1);
}

// --suggest <userId>  — generate an AI prompt recommending professions
const suggestIdx = args.indexOf('--suggest');
if (suggestIdx !== -1) {
  const suggestId = args[suggestIdx + 1];
  if (!suggestId) { console.error('--suggest requires a userId'); process.exit(1); }
  const { user } = loadUser(suggestId);
  const extras = user.extraProfessions || [];
  const allProfs = [user.profession, ...extras].filter(Boolean);
  const available = [...VALID_PROFESSIONS].filter(p => !allProfs.includes(p));
  const lang = user.language || 'zh';

  if (lang === 'en') {
    console.log(`[Career News — Profession Suggestion | user: ${user.userId}]

This user's current profession subscriptions: ${allProfs.join(', ')}
Primary profession: ${user.profession}
Region: ${user.region || 'cn'}

Available professions to add: ${available.join(', ')}

Please suggest 2–3 additional profession news subscriptions that would be most valuable for this user.

Consider:
- Career path overlaps (e.g. a developer who becomes an entrepreneur)
- Knowledge that amplifies their primary profession (e.g. a developer + investor = understands tech funding)
- Adjacent fields they likely monitor (e.g. a designer + product-manager = product design)
- Cross-disciplinary trends relevant to their region

For each suggestion:
1. Profession slug
2. Why it complements their primary profession (1–2 sentences)
3. Example news topics they would gain

Then ask the user: "Would you like me to add any of these? Just tell me which ones."
If they confirm, run:
  node scripts/manage-professions.js --userId ${user.userId} --add <profession>`);

  } else {
    console.log(`[职业新闻 — 职业订阅推荐 | 用户：${user.userId}]

该用户当前已订阅的职业：${allProfs.join('、')}
主职业：${user.profession}（${PROFESSION_LABELS[user.profession] || user.profession}）
地区：${user.region || 'cn'}

可添加的职业：${available.map(p => `${p}（${PROFESSION_LABELS[p]}）`).join('、')}

请为该用户推荐 2~3 个额外职业新闻订阅，要求对其最有价值。

推荐考量维度：
- 职业发展路径重叠（如开发者 → 创业者）
- 能放大主职业价值的知识（如开发者 + 投资 = 理解科技融资）
- 日常本就会关注的领域（如设计师 + 产品经理 = 产品设计全局视野）
- 与其所在地区最相关的跨行业趋势

对每个推荐，给出：
1. 职业名称（slug）
2. 为什么与主职业互补（1~2句）
3. 会获得哪类新闻举例

然后问用户："你想让我帮你加上哪几个？告诉我就好。"
用户确认后执行：
  node scripts/manage-professions.js --userId ${user.userId} --add <profession>`);
  }
  process.exit(0);
}

// All remaining commands need --userId
const userIdx = args.indexOf('--userId');
if (userIdx === -1) {
  console.error('--userId is required. Usage: node scripts/manage-professions.js --userId <id> --add|--remove|--list|--clear <profession>');
  process.exit(1);
}
const rawUserId = args[userIdx + 1] || '';
if (!rawUserId) { console.error('--userId requires a value'); process.exit(1); }

const { fp, user } = loadUser(rawUserId);
if (!user.extraProfessions) user.extraProfessions = [];

// --list
if (args.includes('--list')) {
  printSubscriptions(user);
  process.exit(0);
}

// --clear
if (args.includes('--clear')) {
  const removed = [...user.extraProfessions];
  user.extraProfessions = [];
  saveUser(fp, user);
  console.log(`✔ Cleared all extra subscriptions for "${user.userId}".`);
  if (removed.length) console.log(`  Removed: ${removed.join(', ')}`);
  console.log(`  Primary profession remains: ${user.profession}`);
  process.exit(0);
}

// --add <profession>
const addIdx = args.indexOf('--add');
if (addIdx !== -1) {
  const rawProf = args[addIdx + 1] || '';
  if (!rawProf) { console.error('--add requires a profession name'); process.exit(1); }
  const prof = resolveProf(rawProf);
  if (!prof) {
    console.error(`Unknown profession "${rawProf}".`);
    console.error(`Valid: ${[...VALID_PROFESSIONS].join(', ')}`);
    process.exit(1);
  }
  const allProfs = [user.profession, ...user.extraProfessions].filter(Boolean);
  if (allProfs.includes(prof)) {
    console.log(`ℹ "${prof}" is already in ${user.userId}'s subscriptions.`);
    printSubscriptions(user);
    process.exit(0);
  }
  user.extraProfessions.push(prof);
  saveUser(fp, user);
  console.log(`✔ Added "${prof}" (${PROFESSION_LABELS[prof] || prof}) to ${user.userId}'s subscriptions.`);
  printSubscriptions(user);
  process.exit(0);
}

// --remove <profession>
const removeIdx = args.indexOf('--remove');
if (removeIdx !== -1) {
  const rawProf = args[removeIdx + 1] || '';
  if (!rawProf) { console.error('--remove requires a profession name'); process.exit(1); }
  const prof = resolveProf(rawProf);
  if (!prof) {
    console.error(`Unknown profession "${rawProf}".`);
    process.exit(1);
  }
  if (prof === user.profession) {
    console.error(`Cannot remove primary profession "${prof}". To change it, re-register: node scripts/register.js ${user.userId} --profession <new>`);
    process.exit(1);
  }
  const before = user.extraProfessions.length;
  user.extraProfessions = user.extraProfessions.filter(p => p !== prof);
  if (user.extraProfessions.length === before) {
    console.log(`ℹ "${prof}" was not in ${user.userId}'s extra subscriptions.`);
  } else {
    saveUser(fp, user);
    console.log(`✔ Removed "${prof}" from ${user.userId}'s subscriptions.`);
  }
  printSubscriptions(user);
  process.exit(0);
}

console.error('Unknown command. Use --add, --remove, --list, --clear, or --suggest.');
process.exit(1);
