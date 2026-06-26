#!/usr/bin/env node
/**
 * daily-mood — register.js
 * 用户注册与档案管理：language、mood 偏好、推送开关
 *
 * 用法:
 *   node scripts/register.js <userId> [--lang zh|en] [--mood <mood>]
 *   node scripts/register.js --show <userId>
 *   node scripts/register.js --list
 */

const fs = require('fs');
const path = require('path');

const ALLOWED_LANGS = new Set(['zh', 'en']);
const ALLOWED_MOODS = new Set([
  'happy','sad','anxious','tired','lost','calm','grateful','angry','neutral'
]);
const USERS_DIR = path.join(__dirname, '..', 'data', 'users');

const args = process.argv.slice(2);

// --list
if (args.includes('--list')) {
  if (!fs.existsSync(USERS_DIR)) { console.log('No users registered yet.'); process.exit(0); }
  const files = fs.readdirSync(USERS_DIR).filter(f => f.endsWith('.json'));
  if (files.length === 0) { console.log('No users registered yet.'); process.exit(0); }
  console.log(`\nRegistered users (${files.length}):\n`);
  files.forEach(f => {
    const u = JSON.parse(fs.readFileSync(path.join(USERS_DIR, f), 'utf8'));
    console.log(`  ${u.userId}  lang=${u.language}  mood=${u.mood}  push=${u.pushEnabled}  since=${u.registeredAt.substring(0,10)}`);
  });
  process.exit(0);
}

// --show <userId>
const showIdx = args.indexOf('--show');
if (showIdx !== -1) {
  const userId = args[showIdx + 1];
  if (!userId) { console.error('Usage: node scripts/register.js --show <userId>'); process.exit(1); }
  const filePath = path.join(USERS_DIR, `${userId}.json`);
  if (!fs.existsSync(filePath)) { console.error(`User "${userId}" not found.`); process.exit(1); }
  const u = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  console.log(JSON.stringify(u, null, 2));
  process.exit(0);
}

// Register / update
const userId = args.filter(a => !a.startsWith('--'))[0];
if (!userId) {
  console.error('Usage: node scripts/register.js <userId> [--lang zh|en] [--mood <mood>]');
  console.error('       node scripts/register.js --show <userId>');
  console.error('       node scripts/register.js --list');
  console.error('');
  console.error('Moods:', [...ALLOWED_MOODS].join(', '));
  process.exit(1);
}

// Sanitize userId: alphanumeric + hyphen/underscore, max 64 chars
const safeUserId = userId.replace(/[^a-zA-Z0-9_-]/g, '').substring(0, 64);
if (!safeUserId) { console.error('ERROR: userId must be alphanumeric.'); process.exit(1); }

const langIdx = args.indexOf('--lang');
const rawLang = langIdx !== -1 ? args[langIdx + 1] : null;
const lang = rawLang && ALLOWED_LANGS.has(rawLang) ? rawLang : 'zh';

const moodIdx = args.indexOf('--mood');
const rawMood = moodIdx !== -1 ? args[moodIdx + 1] : null;
const mood = rawMood && ALLOWED_MOODS.has(rawMood) ? rawMood : 'neutral';

if (!fs.existsSync(USERS_DIR)) fs.mkdirSync(USERS_DIR, { recursive: true });

const filePath = path.join(USERS_DIR, `${safeUserId}.json`);
const existing = fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, 'utf8')) : {};

const profile = {
  userId: safeUserId,
  language: lang,
  mood: mood,
  pushEnabled: existing.pushEnabled !== undefined ? existing.pushEnabled : true,
  registeredAt: existing.registeredAt || new Date().toISOString(),
  updatedAt: new Date().toISOString()
};

fs.writeFileSync(filePath, JSON.stringify(profile, null, 2));

const action = existing.userId ? 'Updated' : 'Registered';
console.log(`${action} user: ${safeUserId}`);
console.log(`  Language: ${lang}  |  Default mood: ${mood}  |  Push: ${profile.pushEnabled}`);
console.log('');
console.log(`To enable scheduled push:`);
console.log(`  node scripts/push-toggle.js on --userId ${safeUserId}`);
