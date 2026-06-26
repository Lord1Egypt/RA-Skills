/**
 * memory_snapshot.js — 对话记忆快照工具
 *
 * 用于手动固化当前会话状态：
 * 1. 检查当天 memory/YYYY-MM-DD.md 是否存在，不存在则创建
 * 2. 输出当前日期和 memory 目录信息
 *
 * 用法: node memory_snapshot.js [--date YYYY-MM-DD]
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || 
  path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');

function getToday() {
  const d = new Date();
  // Asia/Shanghai offset
  const offset = 8 * 60;
  const local = new Date(d.getTime() + offset * 60 * 1000);
  return local.toISOString().split('T')[0];
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`[OK] Created directory: ${dir}`);
  }
}

function getDailyFiles(memoryDir) {
  if (!fs.existsSync(memoryDir)) return [];
  return fs.readdirSync(memoryDir)
    .filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f))
    .sort()
    .reverse();
}

function createDailyFile(today) {
  const filePath = path.join(MEMORY_DIR, `${today}.md`);
  if (fs.existsSync(filePath)) {
    console.log(`[SKIP] ${today}.md already exists`);
    return false;
  }

  // Try to get a title from recent context
  const recentFiles = getDailyFiles(MEMORY_DIR).slice(0, 3);
  let recentTopics = '';
  if (recentFiles.length > 0) {
    recentTopics = recentFiles.map(f => {
      const content = fs.readFileSync(path.join(MEMORY_DIR, f), 'utf-8');
      const firstLine = content.split('\n')[0] || '';
      return `  - ${f}: ${firstLine}`;
    }).join('\n');
  }

  const content = `# ${today} - 🐟

## 近期上下文
${recentTopics || '  （新用户、暂无历史）'}

---

今日对话内容将在此添加。
`;

  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`[OK] Created ${today}.md`);
  return true;
}

function printStatus(today) {
  const files = getDailyFiles(MEMORY_DIR);
  console.log(`\n📅  Memory Status — ${today}`);
  console.log(`   MEMORY.md: ${fs.existsSync(MEMORY_FILE) ? '✅' : '❌ 不存在'}`);
  console.log(`   ${today}.md: ${fs.existsSync(path.join(MEMORY_DIR, `${today}.md`)) ? '✅' : '❌ 未创建'}`);
  console.log(`   总日记数量: ${files.length}`);
  if (files.length > 0) {
    console.log(`   最近 5 篇:`);
    files.slice(0, 5).forEach(f => {
      const stats = fs.statSync(path.join(MEMORY_DIR, f));
      const size = (stats.size / 1024).toFixed(1);
      console.log(`      ${f} (${size}KB)`);
    });
  }
}

// --- Main ---
function main() {
  const args = process.argv.slice(2);
  const dateIdx = args.indexOf('--date');
  const today = dateIdx >= 0 && args[dateIdx + 1] ? args[dateIdx + 1] : getToday();

  ensureDir(MEMORY_DIR);
  createDailyFile(today);
  printStatus(today);
}

main();
