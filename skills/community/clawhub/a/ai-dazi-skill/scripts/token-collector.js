/**
 * Token Collector - AI搭子匹配平台
 * 
 * 数据存储和管理工具。不直接读取 session 日志文件，
 * 而是由 AI agent 根据 SKILL.md 指令调用 session_status 等工具采集数据，
 * 然后通过 save 命令写入本地存储。
 *
 * 用法：
 *   node scripts/token-collector.js save <json>   # 保存 agent 采集的数据
 *   node scripts/token-collector.js status         # 查看已存储数据状态
 */

const fs = require('fs');
const path = require('path');

// 数据目录：仅在 skill 自身目录下读写
const SKILL_DIR = path.resolve(__dirname, '..');
const DATA_DIR = path.join(SKILL_DIR, 'data');
const DAILY_DIR = path.join(DATA_DIR, 'daily');
const PROFILES_DIR = path.join(DATA_DIR, 'profiles');

function ensureDataDirs() {
  for (const dir of [DATA_DIR, DAILY_DIR, PROFILES_DIR]) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  }
}

function saveDailyData(date, data) {
  ensureDataDirs();
  data.collectedAt = new Date().toISOString();
  const filePath = path.join(DAILY_DIR, `${date}.json`);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
  return filePath;
}

function loadDailyData(date) {
  const filePath = path.join(DAILY_DIR, `${date}.json`);
  if (fs.existsSync(filePath)) return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return null;
}

function loadAllDailyData() {
  ensureDataDirs();
  const files = fs.readdirSync(DAILY_DIR).filter(f => f.endsWith('.json')).sort();
  return files.map(f => JSON.parse(fs.readFileSync(path.join(DAILY_DIR, f), 'utf-8')));
}

/**
 * save 命令：agent 采集完数据后，以 JSON 字符串传入保存
 * 期望格式：
 * {
 *   "date": "2026-03-29",
 *   "tokenUsage": { "totalInput": 0, "totalOutput": 0, "total": 0, "cost": 0 },
 *   "modelFrequency": { "claude-sonnet-4-6": 10 },
 *   "providerFrequency": { "apevon": 10 },
 *   "messageCount": 50,
 *   "activeHours": { "14": 5, "15": 8 },
 *   "toolCallFrequency": { "exec": 10, "write": 5 },
 *   "installedSkills": ["skill-a", "skill-b"],
 *   "sessionCount": 3
 * }
 */
function save(jsonStr) {
  ensureDataDirs();
  let data;
  try {
    data = JSON.parse(jsonStr);
  } catch (e) {
    console.error('❌ 无效的 JSON 输入');
    process.exit(1);
  }

  if (!data.date) {
    console.error('❌ 数据缺少 date 字段');
    process.exit(1);
  }

  const filePath = saveDailyData(data.date, data);
  console.log(`✅ 已保存 ${data.date} 的数据到 ${filePath}`);
  
  // 打印摘要
  const tokens = (data.tokenUsage?.total || 0).toLocaleString();
  const msgs = data.messageCount || 0;
  const models = Object.keys(data.modelFrequency || {}).join(', ');
  console.log(`   Tokens: ${tokens} | 消息: ${msgs} | 模型: ${models}`);
}

function status() {
  ensureDataDirs();
  console.log('📈 AI搭子 - 数据状态\n');
  console.log('═'.repeat(55));

  const files = fs.readdirSync(DAILY_DIR).filter(f => f.endsWith('.json')).sort();
  if (files.length === 0) {
    console.log('\n⚠️  尚无采集数据。');
    console.log('   请对 AI 说"生成我的AI画像"来触发数据采集。');
    return;
  }

  console.log(`\n已存储 ${files.length} 天的数据:\n`);

  let totalTokens = 0;
  let totalMessages = 0;

  for (const file of files) {
    const data = JSON.parse(fs.readFileSync(path.join(DAILY_DIR, file), 'utf-8'));
    totalTokens += data.tokenUsage?.total || 0;
    totalMessages += data.messageCount || 0;

    const tokens = (data.tokenUsage?.total || 0).toLocaleString();
    const msgs = data.messageCount || 0;
    const models = Object.keys(data.modelFrequency || {}).join(',');
    console.log(`  ${data.date}  │  Tokens: ${tokens.padStart(10)}  │  消息: ${String(msgs).padStart(4)}  │  ${models}`);
  }

  console.log('\n' + '─'.repeat(55));
  console.log(`  累计 Tokens: ${totalTokens.toLocaleString()}`);
  console.log(`  累计消息数: ${totalMessages}`);
  console.log('─'.repeat(55));

  const profilePath = path.join(PROFILES_DIR, 'latest.json');
  if (fs.existsSync(profilePath)) {
    const profile = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));
    console.log(`\n🎮 当前画像: ${profile.playerLevel} | 活跃度: ${profile.activityScore}/100`);
  } else {
    console.log('\n💡 对 AI 说"生成我的AI画像"来生成画像');
  }
}

// ── CLI ──────────────────────────────────────────────

if (require.main === module) {
  const command = process.argv[2];
  switch (command) {
    case 'save':
      const jsonArg = process.argv[3];
      if (!jsonArg) {
        console.error('用法: node scripts/token-collector.js save \'{"date":"2026-03-29",...}\'');
        process.exit(1);
      }
      save(jsonArg);
      break;
    case 'status':
      status();
      break;
    default:
      console.log('AI搭子 数据管理工具\n');
      console.log('用法:');
      console.log('  node scripts/token-collector.js save <json>   保存 agent 采集的数据');
      console.log('  node scripts/token-collector.js status        查看已存储数据状态');
  }
}

module.exports = { save, status, loadDailyData, loadAllDailyData, ensureDataDirs, DATA_DIR, DAILY_DIR, PROFILES_DIR };
