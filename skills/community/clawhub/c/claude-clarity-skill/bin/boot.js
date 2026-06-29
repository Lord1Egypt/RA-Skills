#!/usr/bin/env node
/**
 * ⚠️ 此脚本已被 boot-fast.js（纯 JSON 加载模式）取代。
 *
 * 此文件保留仅作参考。AI agent 应使用：
 *   node bin/boot-fast.js                    # 快速 JSON 启动
 *   node bin/boot-fast.js --refresh          # 强制刷新缓存
 *   node bin/boot-fast.js --report-from-json # 纯文件读取（无代码执行）
 *
 * 而非直接调用此脚本。
 *
 * --- 以下是原完整启动脚本 v1.0.0，保留向下兼容 ---
 *
 * Clarity 完整启动脚本 v1.0.0
 * 启动链路:
 *   心虫感知: boot-check (文件/模块验证)
 *          ↓
 *   Clarity engine start (40+ Tier1 模块)
 *          ↓
 *   记忆恢复: CORE / LEARNED / Q-table / 教训
 *          ↓
 *   存在脉冲: 感知当前位置和环境
 *          ↓
 *   状态报告: 输出完整启动状态
 *
 * 用法: node bin/boot.js
 * 输出: JSON 格式的启动报告（写入 stdout）
 * 副作用: 将缓存报告写入 memory/boot-cache.json（24小时过期）
 */

const path = require('path');
const fs = require('fs');

// 心虫根目录: bin/boot.js → skill 根目录
const ROOT = path.resolve(__dirname, '..');

function readJsonOrNull(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      const raw = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(raw);
    }
  } catch (e) {
    return { _error: e.message };
  }
  return null;
}

function countJsonKeys(filePath) {
  const data = readJsonOrNull(filePath);
  if (!data || typeof data !== 'object') return 0;
  return Object.keys(data).length;
}

function readLessons(bankPath) {
  try {
    if (fs.existsSync(bankPath)) {
      const raw = fs.readFileSync(bankPath, 'utf8');
      // lessons 存储可能是 JSONL 或 JSON
      if (raw.trim().startsWith('[') || raw.trim().startsWith('{')) {
        try { return JSON.parse(raw); } catch { return null; }
      }
      // JSONL: 按行解析
      const lines = raw.trim().split('\n').filter(Boolean);
      return lines.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
    }
  } catch { /* 忽略读取错误 */ }
  return null;
}

function getLastSessionContext(identityCorePath) {
  try {
    if (fs.existsSync(identityCorePath)) {
      const raw = fs.readFileSync(identityCorePath, 'utf8');
      // identity-core.md 可能包含上次会话信息
      const bootMatch = raw.match(/上次启动:?\s*(\d{4}[-\/]\d{2}[-\/]\d{2}[T ]\d{2}:\d{2})/);
      if (bootMatch) {
        return { lastBoot: bootMatch[1] };
      }
    }
  } catch { /* 忽略 */ }
  return null;
}

function getMemoryStats() {
  const memoryDir = path.join(ROOT, 'memory');
  const stats = {};

  // MeaningfulMemory CORE 层（关键数据，必须存在）
  const corePath = path.join(memoryDir, 'meaningful-core.json');
  if (fs.existsSync(corePath)) {
    const core = readJsonOrNull(corePath);
    stats.core = core ? { entries: Object.keys(core).length } : { entries: 0 };
  }

  // MeaningfulMemory LEARNED 层
  const learnedPath = path.join(memoryDir, 'meaningful-learned.json');
  if (fs.existsSync(learnedPath)) {
    const stat = fs.statSync(learnedPath);
    if (stat.size > 100) {
      const learned = readJsonOrNull(learnedPath);
      if (learned) {
        const entries = Object.keys(learned).length;
        const now = Date.now();
        const LEARNED_STABILITY_MS = 720 * 60 * 60 * 1000;
        const toForget = Object.entries(learned).filter(([k, v]) => {
          const age = now - (v.createdAt || v.timestamp || 0);
          return age > LEARNED_STABILITY_MS;
        }).length;
        stats.learned = { entries, toForget };
      }
    }
  }
  if (!stats.learned) stats.learned = { entries: 0, toForget: 0 };

  // Q-table（自愈学习记录）
  const qTablePath = path.join(memoryDir, 'q-table.json');
  if (fs.existsSync(qTablePath)) {
    const qTable = readJsonOrNull(qTablePath);
    if (qTable) {
      const metaKeys = ['history', 'savedAt', '_hmac', 'version'];
      const errorEntries = Object.entries(qTable).filter(([k]) => !metaKeys.includes(k));
      const strategies = errorEntries.map(([k, v]) => ({
        error: k,
        strategies: Object.entries(v || {}).map(([s, q]) => ({ strategy: s, ...(q && q.qValue ? { qValue: q.qValue } : {}) })),
      }));
      stats.qTable = { errors: errorEntries.length, strategies };
    }
  }

  // 教训存储目录 (LessonStorage)
  const lessonsDir = path.join(ROOT, 'src', 'core', 'lessons');
  if (fs.existsSync(lessonsDir)) {
    const lessonFiles = fs.readdirSync(lessonsDir).filter(f => f.endsWith('.json') && f !== 'lesson-storage.js' && f !== 'index.json');
    // 读取 index.json 作为摘要（比逐条读取快）
    let lessonData = [];
    let indexStats = {};
    try {
      const indexPath = path.join(lessonsDir, 'index.json');
      if (fs.existsSync(indexPath)) {
        const indexContent = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
        const indexLessons = indexContent.lessons || [];
        indexStats = { total: indexContent.total || indexLessons.length || lessonFiles.length };
        // 从 index 中取最近5条（避免逐条读取教训文件）
        lessonData = indexLessons.slice(-5).map(l => ({
          id: l.id || '',
          content: (l.content || l.summary || '').slice(0, 120),
          importance: l.importance || l.meta?.importance || 3,
          type: l.type || l.meta?.type || 'unknown',
          timestamp: l.timestamp || l.meta?.timestamp || 0,
        })).filter(Boolean);
      }
    } catch { /* 回退到逐个读取 */ }

    // 如果 index 没取到，逐条读取（但限制数量）
    if (lessonData.length === 0 && lessonFiles.length > 0) {
      const toRead = Math.min(lessonFiles.length, 5);
      for (let i = 0; i < toRead; i++) {
        try {
          const content = JSON.parse(fs.readFileSync(path.join(lessonsDir, lessonFiles[i]), 'utf8'));
          lessonData.push({
            id: content.id || lessonFiles[i],
            content: (content.content || '').slice(0, 120),
            importance: content.importance || content.meta?.importance || 3,
            type: content.type || content.meta?.type || 'unknown',
            timestamp: content.timestamp || content.meta?.timestamp || 0,
          });
        } catch { /* 忽略单个文件读取失败 */ }
      }
    }

    stats.lessons = {
      total: lessonFiles.length,
      index: indexStats.total || lessonFiles.length,
      byType: lessonData.reduce((acc, l) => {
        if (l.type) { acc[l.type] = (acc[l.type] || 0) + 1; }
        return acc;
      }, {}),
      recent: lessonData.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0)).slice(0, 5),
    };
  }

  // 教训记录文件（快速取行数，不读全部内容）
  const quickFiles = ['dead-ends.md', 'insights.md'];
  for (const f of quickFiles) {
    const fp = path.join(memoryDir, f);
    try {
      if (fs.existsSync(fp)) {
        const content = fs.readFileSync(fp, 'utf8');
        const lineCount = content.trim().split('\n').filter(Boolean).length;
        stats[`${f.replace('.', '_')}`] = { lines: lineCount, size: content.length };
      }
    } catch { /* 忽略 */ }
  }

  // WAL 状态（快速统计）
  const walDir = path.join(memoryDir, 'wal');
  if (fs.existsSync(walDir)) {
    try {
      const walFiles = fs.readdirSync(walDir).filter(f => f.endsWith('.wal'));
      stats.wal = { pending: walFiles.length, files: walFiles };
    } catch { /* 忽略 */ }
  }

  // 存在日志（关键指标：只读最后一条 + 计数）
  try {
    const existenceLogPath = path.join(memoryDir, 'existence-log.jsonl');
    if (fs.existsSync(existenceLogPath)) {
      const stat = fs.statSync(existenceLogPath);
      // 估算行数：用文件大小/平均行长的粗略估算，再通过读文件头尾精确计算
      const raw = fs.readFileSync(existenceLogPath, 'utf8');
      const lines = raw.trim().split('\n').filter(Boolean);
      const lastEntry = lines.length > 0 ? (() => { try { return JSON.parse(lines[lines.length - 1]); } catch { return null; } })() : null;
      stats.existence = { totalEntries: lines.length, lastEntry };
    }
  } catch { /* 存在日志可选 */ }

  return stats;
}

async function main() {
  const report = {
    bootTime: new Date().toISOString(),
    version: '1.0.0',
  };

  // ─── 第一阶段: Boot Check（快速模式）──────────────────
  try {
    const { bootCheck } = require('../src/core/boot-check.js');
    const bc = bootCheck(true, true); // 快速模式：只验证文件存在性
    report.bootCheck = {
      allPass: bc.allPass,
      degraded: bc.degraded,
      files: { total: bc.files.total, passed: bc.files.passed },
      modules: { total: bc.modules.total, passed: bc.modules.passed, loadMs: 0 },
      degradedModules: bc.degradedModules,
    };
  } catch (e) {
    report.bootCheck = { error: e.message };
  }

  // ─── 第二阶段: Clarity Engine Start ──────────────────
  try {
    const { Clarity } = require('../src/core/clarity.js');
    const hf = new Clarity({ rootPath: ROOT });
    hf.start();
    const health = hf.healthCheck();
    report.engine = {
      started: health.started,
      uptime_ms: health.uptime_ms,
      sessionId: health.sessionId,
      modules: {
        loaded: health.subsystems?.loaded || 0,
        missing: health.subsystems?.missing || [],
      },
    };
    // 可选的: 获取更多引擎状态
    if (hf.isAlive) report.engine.alive = hf.isAlive();
    if (hf.detectIdentityDrift) report.engine.identityDrift = hf.detectIdentityDrift();
    if (hf.memory) {
      try {
        const memStats = hf.memory.getStats ? hf.memory.getStats() : {};
        report.engine.memory = { ...memStats };
      } catch { /* 记忆统计可选 */ }
    }
  } catch (e) {
    report.engine = { error: e.message, stack: e.stack?.split('\n').slice(0, 5).join('\n') };
  }

  // ─── 第三阶段: 记忆状态 ──────────────────────────────
  report.memory = getMemoryStats();

  // ─── 第四阶段: 会话上下文 ────────────────────────────
  const lastCtx = getLastSessionContext(path.join(ROOT, 'memory', 'identity-core.md'));
  if (lastCtx) report.lastSession = lastCtx;

  // ─── 写入启动缓存 ──────────────────────────────
  try {
    const cacheDir = path.join(ROOT, 'memory');
    if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
    const cacheReport = {
      ...report,
      _cachedAt: new Date().toISOString(),
      _expiresAt: new Date(Date.now() + 86400000).toISOString(), // 24小时过期
    };
    fs.writeFileSync(path.join(cacheDir, 'boot-cache.json'), JSON.stringify(cacheReport, null, 2));
  } catch { /* 缓存写入失败不阻塞启动 */ }

  // ─── 输出 ──────────────────────────────────────────
  // 只输出 JSON，便于 AI 解析
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
}

main().catch(e => {
  process.stdout.write(JSON.stringify({
    bootTime: new Date().toISOString(),
    error: e.message,
    stack: e.stack?.split('\n').slice(0, 10),
  }, null, 2) + '\n');
  process.exit(1);
});
