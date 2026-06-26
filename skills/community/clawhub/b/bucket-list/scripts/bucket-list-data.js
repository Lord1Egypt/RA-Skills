#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const VALID_STATUS = new Set(['pending', 'completed', 'cancelled']);

function getSkillDir() {
  return path.resolve(__dirname, '..');
}

function getWorkspaceDir() {
  return path.resolve(getSkillDir(), '..', '..');
}

function getDataFile() {
  return process.env.BUCKET_LIST_DATA_FILE || path.join(getWorkspaceDir(), 'data', 'bucket-list.json');
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function emptyData() {
  return { version: '1.4', wishes: [], createdAt: today() };
}

function generateId() {
  return `wish_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
}

function normalizeTimelineEntry(entry) {
  if (!entry || typeof entry !== 'object') return null;
  return {
    date: String(entry.date || today()).slice(0, 10),
    event: String(entry.event || '更新'),
    note: String(entry.note || ''),
  };
}

function normalizeWish(wish) {
  if (!wish || typeof wish !== 'object') return null;
  const status = VALID_STATUS.has(wish.status) ? wish.status : 'pending';
  return {
    id: String(wish.id || generateId()),
    content: String(wish.content || '').trim(),
    category: String(wish.category || '其他').trim() || '其他',
    status,
    createdAt: String(wish.createdAt || today()).slice(0, 10),
    endedAt: wish.endedAt ? String(wish.endedAt).slice(0, 10) : null,
    endedBy: wish.endedBy || null,
    completionNote: String(wish.completionNote || ''),
    cancelReason: String(wish.cancelReason || ''),
    timeline: Array.isArray(wish.timeline) ? wish.timeline.map(normalizeTimelineEntry).filter(Boolean) : [],
  };
}

function validateData(data) {
  if (!data || typeof data !== 'object') throw new Error('Data must be a JSON object.');
  if (!Array.isArray(data.wishes)) throw new Error('Data must contain a wishes array.');
  return {
    version: String(data.version || '1.4'),
    wishes: data.wishes.map(normalizeWish).filter((wish) => wish && wish.content),
    createdAt: String(data.createdAt || today()).slice(0, 10),
  };
}

function ensureDataFile() {
  const file = getDataFile();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (!fs.existsSync(file)) writeData(emptyData(), { backup: false });
}

function readData() {
  ensureDataFile();
  return validateData(JSON.parse(fs.readFileSync(getDataFile(), 'utf8')));
}

function writeData(data, options = {}) {
  const normalized = validateData(data);
  const file = getDataFile();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (options.backup !== false && fs.existsSync(file)) fs.copyFileSync(file, `${file}.bak`);
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, `${JSON.stringify(normalized, null, 2)}\n`, { mode: 0o600 });
  fs.renameSync(tmp, file);
  return normalized;
}

function addWish(content, category = '其他') {
  const trimmed = String(content || '').trim();
  if (!trimmed) throw new Error('Wish content is required.');
  const data = readData();
  const now = today();
  const wish = normalizeWish({
    id: generateId(),
    content: trimmed,
    category,
    status: 'pending',
    createdAt: now,
    timeline: [{ date: now, event: '添加愿望', note: trimmed }],
  });
  data.wishes.push(wish);
  writeData(data);
  return wish;
}

function findWish(data, keyword) {
  const query = String(keyword || '').trim();
  if (!query) throw new Error('Keyword is required.');
  return data.wishes.find((wish) => wish.id === query)
    || data.wishes.find((wish) => wish.content.includes(query));
}

function completeWish(keyword, note = '') {
  const data = readData();
  const wish = findWish(data, keyword);
  if (!wish) throw new Error(`没找到包含「${keyword}」的愿望`);
  const now = today();
  wish.status = 'completed';
  wish.endedAt = now;
  wish.endedBy = 'complete';
  wish.completionNote = String(note || '');
  wish.cancelReason = '';
  wish.timeline = wish.timeline || [];
  wish.timeline.push({ date: now, event: '完成', note: wish.completionNote || '完成愿望' });
  writeData(data);
  return wish;
}

function cancelWish(keyword, reason = '') {
  const data = readData();
  const wish = findWish(data, keyword);
  if (!wish) throw new Error(`没找到包含「${keyword}」的愿望`);
  const now = today();
  wish.status = 'cancelled';
  wish.endedAt = now;
  wish.endedBy = 'cancelled';
  wish.cancelReason = String(reason || '');
  wish.timeline = wish.timeline || [];
  wish.timeline.push({ date: now, event: '取消', note: wish.cancelReason || '取消愿望' });
  writeData(data);
  return wish;
}

function undoWish(keyword) {
  const data = readData();
  const wish = findWish(data, keyword);
  if (!wish) throw new Error(`没找到包含「${keyword}」的愿望`);
  wish.status = 'pending';
  wish.endedAt = null;
  wish.endedBy = null;
  wish.completionNote = '';
  wish.cancelReason = '';
  wish.timeline = (wish.timeline || []).filter((entry) => entry.event !== '完成' && entry.event !== '取消');
  writeData(data);
  return wish;
}

function printGroup(title, wishes) {
  console.log('');
  console.log(`${title}（${wishes.length}项）`);
  if (!wishes.length) {
    console.log('  （空）');
    return;
  }
  for (const wish of wishes) {
    const ended = wish.endedAt ? ` -> ${wish.endedAt}` : '';
    const note = wish.completionNote || wish.cancelReason;
    console.log(`  - ${wish.content}（${wish.category}）${wish.createdAt}${ended}`);
    if (note) console.log(`    ${note}`);
  }
}

function printView(data = readData()) {
  const pending = data.wishes.filter((wish) => wish.status === 'pending');
  const completed = data.wishes.filter((wish) => wish.status === 'completed');
  const cancelled = data.wishes.filter((wish) => wish.status === 'cancelled');
  console.log('愿望清单');
  printGroup('待完成', pending);
  printGroup('已完成', completed);
  printGroup('已取消', cancelled);
  const rate = data.wishes.length ? Math.round((completed.length * 100) / data.wishes.length) : 0;
  console.log(`总计：${data.wishes.length}个愿望，完成率 ${rate}%`);
}

function printAchievements(data = readData()) {
  const completed = data.wishes.filter((wish) => wish.status === 'completed');
  console.log('一起完成的成就');
  if (!completed.length) {
    console.log('  （暂无成就记录）');
    return;
  }
  const years = [...new Set(completed.map((wish) => (wish.endedAt || '').slice(0, 4)).filter(Boolean))].sort();
  for (const year of years) {
    console.log('');
    console.log(`${year}年：`);
    for (const wish of completed.filter((item) => (item.endedAt || '').startsWith(year))) {
      console.log(`  - ${wish.content}（${wish.endedAt || '未知日期'}）`);
    }
  }
  console.log('');
  console.log(`共 ${completed.length} 个愿望，跨越 ${years.length} 年`);
}

function recognizeIntent(input) {
  const text = String(input || '').trim();
  let match = text.match(/^添加愿望[：:]\s*(.+)$/);
  if (match) return ['add', match[1]];
  match = text.match(/^(?:完成了|完成)\s*(.+)$/);
  if (match) return ['complete', match[1]];
  match = text.match(/^(?:取消|不做)\s*(.+)$/);
  if (match) return ['cancel', match[1]];
  if (/查看愿望|愿望清单|看一下清单/.test(text)) return ['view'];
  if (/完成了什么|成就|回顾|一起完成/.test(text)) return ['achievements'];
  return ['help'];
}

function printHelp() {
  console.log('愿望清单 - 可用命令：');
  console.log('  add "愿望内容" ["分类"]');
  console.log('  complete "关键词或ID" ["完成备注"]');
  console.log('  cancel "关键词或ID" ["取消原因"]');
  console.log('  undo "关键词或ID"');
  console.log('  view');
  console.log('  achievements');
  console.log('  intent "添加愿望：..."');
}

function runCli(argv) {
  const [command = 'view', ...args] = argv;
  try {
    switch (command) {
      case 'add': {
        const wish = addWish(args[0], args[1]);
        console.log(`已记录愿望「${wish.content}」（${wish.category}）`);
        console.log(`添加时间：${wish.createdAt}`);
        break;
      }
      case 'complete': {
        const wish = completeWish(args[0], args[1]);
        console.log(`恭喜完成「${wish.content}」`);
        console.log(`完成时间：${wish.endedAt}`);
        break;
      }
      case 'cancel': {
        const wish = cancelWish(args[0], args[1]);
        console.log(`已取消愿望「${wish.content}」`);
        console.log(`取消时间：${wish.endedAt}`);
        break;
      }
      case 'undo': {
        const wish = undoWish(args[0]);
        console.log(`已撤销，愿望「${wish.content}」回到待完成`);
        break;
      }
      case 'view':
        printView();
        break;
      case 'achievements':
        printAchievements();
        break;
      case 'json':
        console.log(JSON.stringify(readData(), null, 2));
        break;
      case 'validate':
        writeData(readData(), { backup: false });
        console.log(`OK: ${getDataFile()}`);
        break;
      case 'intent':
        runCli(recognizeIntent(args.join(' ')));
        break;
      default:
        printHelp();
        break;
    }
  } catch (error) {
    console.error(`错误：${error.message}`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  runCli(process.argv.slice(2));
}

module.exports = {
  addWish,
  cancelWish,
  completeWish,
  emptyData,
  getDataFile,
  readData,
  validateData,
  writeData,
};
