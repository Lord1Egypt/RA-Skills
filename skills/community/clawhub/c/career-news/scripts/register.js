#!/usr/bin/env node
/**
 * career-news — register.js
 * Register / view / list users. Supports one primary profession + multiple extra subscriptions.
 *
 * Usage:
 *   node scripts/register.js <userId> --profession <prof> [--lang zh|en] [--region cn|us|global] [--keywords kw1,kw2]
 *   node scripts/register.js --show <userId>
 *   node scripts/register.js --list
 *
 * Professions: doctor, lawyer, engineer, developer, designer, product-manager,
 *              investor, teacher, journalist, entrepreneur, researcher, marketing, hr, sales
 *
 * Note: to add/remove extra profession subscriptions use manage-professions.js
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'data', 'users');
if (!fs.existsSync(USERS_DIR)) fs.mkdirSync(USERS_DIR, { recursive: true });

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

function resolveProf(raw) {
  if (!raw) return null;
  const direct = PROFESSION_ZH_MAP[raw] || (VALID_PROFESSIONS.has(raw) ? raw : null);
  if (direct) return direct;
  for (const [key, val] of Object.entries(PROFESSION_ZH_MAP)) {
    if (raw.includes(key)) return val;
  }
  return null;
}

const args = process.argv.slice(2);

// --list
if (args.includes('--list')) {
  if (!fs.existsSync(USERS_DIR)) { console.log('No users registered.'); process.exit(0); }
  const files = fs.readdirSync(USERS_DIR).filter(f => f.endsWith('.json'));
  if (files.length === 0) { console.log('No users registered.'); process.exit(0); }
  console.log(`\nRegistered users (${files.length}):`);
  console.log('─'.repeat(70));
  files.forEach(f => {
    const u = JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8'));
    const allProfs = [u.profession, ...(u.extraProfessions || [])].filter(Boolean);
    const kw = u.keywords && u.keywords.length ? ` [${u.keywords.join(',')}]` : '';
    const push = u.pushEnabled === false ? '⏸' : '✅';
    console.log(`${push} ${u.userId.padEnd(20)} ${allProfs.join('+').padEnd(28)} ${u.language}/${u.region}${kw}`);
  });
  console.log('─'.repeat(70));
  process.exit(0);
}

// --show <userId>
const showIdx = args.indexOf('--show');
if (showIdx !== -1) {
  const showId = args[showIdx + 1];
  if (!showId) { console.error('--show requires a userId'); process.exit(1); }
  const fp = path.join(USERS_DIR, `${showId.replace(/[^a-zA-Z0-9_-]/g, '')}.json`);
  if (!fs.existsSync(fp)) { console.error(`User "${showId}" not found.`); process.exit(1); }
  const u = JSON.parse(fs.readFileSync(fp, 'utf8'));
  const allProfs = [u.profession, ...(u.extraProfessions || [])].filter(Boolean);
  console.log(JSON.stringify(u, null, 2));
  console.log(`\nSubscribed professions (${allProfs.length}): ${allProfs.join(', ')}`);
  console.log('Tip: node scripts/manage-professions.js --userId ' + u.userId + ' --add <profession>');
  process.exit(0);
}

// register
const profIdx     = args.indexOf('--profession');
const langIdx     = args.indexOf('--lang');
const regionIdx   = args.indexOf('--region');
const kwIdx       = args.indexOf('--keywords');
const profArg     = profIdx   !== -1 ? args[profIdx   + 1] : null;
const langArg     = langIdx   !== -1 ? args[langIdx   + 1] : 'zh';
const regionArg   = regionIdx !== -1 ? args[regionIdx + 1] : null;
const kwArg       = kwIdx     !== -1 ? args[kwIdx     + 1] : null;

const rawUserId = args.filter(a =>
  !a.startsWith('--') &&
  a !== profArg && a !== langArg && a !== regionArg && a !== kwArg
)[0] || '';

if (!rawUserId) {
  console.error('Usage: node scripts/register.js <userId> --profession <prof> [--lang zh|en] [--region cn|us] [--keywords kw1,kw2]');
  console.error('       node scripts/register.js --show <userId>');
  console.error('       node scripts/register.js --list');
  console.error('');
  console.error('Professions: doctor, lawyer, engineer, developer, designer, product-manager,');
  console.error('             investor, teacher, journalist, entrepreneur, researcher, marketing, hr, sales');
  console.error('');
  console.error('To manage extra profession subscriptions:');
  console.error('  node scripts/manage-professions.js --userId <id> --add <profession>');
  process.exit(1);
}

const userId = rawUserId.replace(/[^a-zA-Z0-9_-]/g, '').substring(0, 64);
if (!userId) { console.error('Invalid userId.'); process.exit(1); }

const profession = resolveProf(profArg) || 'developer';
const lang = langArg === 'en' ? 'en' : 'zh';
const region = regionArg || (lang === 'zh' ? 'cn' : 'us');
const keywords = kwArg ? kwArg.split(',').map(k => k.trim()).filter(Boolean) : [];

const fp = path.join(USERS_DIR, `${userId}.json`);
const existing = fs.existsSync(fp) ? JSON.parse(fs.readFileSync(fp, 'utf8')) : {};

const user = {
  ...existing,
  userId,
  profession,
  extraProfessions: existing.extraProfessions || [],   // preserved on re-register
  language: lang,
  region,
  keywords,
  pushEnabled: existing.pushEnabled !== undefined ? existing.pushEnabled : true,
  createdAt: existing.createdAt || new Date().toISOString(),
  updatedAt: new Date().toISOString()
};

fs.writeFileSync(fp, JSON.stringify(user, null, 2));
const allProfs = [user.profession, ...user.extraProfessions].filter(Boolean);
console.log(`✔ User "${userId}" registered.`);
console.log(`  Primary profession : ${profession}`);
console.log(`  Extra subscriptions: ${user.extraProfessions.length ? user.extraProfessions.join(', ') : '(none)'}`);
console.log(`  All professions    : ${allProfs.join(', ')}`);
console.log(`  Language           : ${lang} / Region: ${region}`);
if (keywords.length) console.log(`  Keywords           : ${keywords.join(', ')}`);
console.log(`  Push               : ${user.pushEnabled ? 'enabled' : 'disabled'}`);
console.log(`  Saved to           : ${fp}`);
console.log('');
console.log(`  → To add more profession subscriptions:`);
console.log(`    node scripts/manage-professions.js --userId ${userId} --add <profession>`);
