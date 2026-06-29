/**
 * Dream Fragments — 梦境原材料收集器
 *
 * 从多个数据源提取并组装梦境原材料，供 dreamNow() 使用。
 * 提取自 clarity.js _getDreamFragments()，v2.6.4+ 独立模块。
 *
 * 数据源：
 *   - 身份核心(identityCore)
 *   - 教训系统(lesson)
 *   - 对话历史(dialogue-history.jsonl)
 *   - 历史迁移记忆(legacy-migration.jsonl)
 *   - 永久记忆(permanent-memory.jsonl)
 *   - 上下文记忆(context-memory.jsonl)
 *   - CORE/LEARNED/EPHEMERAL 记忆层
 *   - 心理学洞察
 */

const path = require('path');
const fs = require('fs');

/**
 * 从多个数据源提取梦境原材料
 *
 * @param {object} deps - 依赖注入对象
 * @param {object} deps.identityCore - 身份核心实例（getIdentitySummary, getSessionHistory）
 * @param {object} deps.lesson - 教训系统实例（getTopLessons）
 * @param {object} deps.memory - 记忆系统实例（listCore, listLearned）
 * @param {object} deps.psychology - 心理学引擎实例（getPsychologyStats）
 * @param {string} deps.rootPath - 项目根路径（用于查找 JSONL 文件）
 * @returns {Array<{text: string, layer: string, key: string, salience: number, ts?: string}>}
 */
function getDreamFragments(deps) {
  const { identityCore, lesson, memory, psychology, rootPath } = deps;
  const fragments = [];
  const loadJsonl = (filePath, maxLines, parseFn) => {
    try {
      if (!fs.existsSync(filePath)) return;
      const lines = fs.readFileSync(filePath, 'utf8').trim().split('\n').slice(-maxLines);
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const entry = JSON.parse(line);
          const result = parseFn(entry);
          if (result) fragments.push(result);
        } catch (e) { /* 跳过格式错误行 */ }
      }
    } catch (e) { /* 文件读取失败不阻断 */ }
  };

  // 1. 身份核心数据
  try {
    if (identityCore?.getIdentitySummary) {
      const identity = identityCore.getIdentitySummary();
      if (identity) {
        fragments.push({
          text: `${identity.name}: ${identity.identities?.join(' / ') || ''} | ${identity.meaning || ''}`,
          layer: 'CORE',
          key: 'identity',
          salience: 1.0,
        });
      }
    }
  } catch (e) { /* 可选模块 */ }

  // 2. 教训系统（最高价值的学习来源）
  try {
    if (lesson?.getTopLessons) {
      const lessons = lesson.getTopLessons(8);
      for (const l of lessons) {
        fragments.push({
          text: `[教训] ${l.errorPattern || ''} → ${l.correction || ''}`,
          layer: 'LEARNED',
          key: `lesson-${l.id || fragments.length}`,
          salience: l.confidence || 0.5,
        });
      }
    }
  } catch (e) { /* 可选模块 */ }

  // 2b. 对话历史（永久记忆）
  loadJsonl(path.join(rootPath, 'memory', 'dialogue-history.jsonl'), 30, (entry) => {
    const text = entry.role === 'user'
      ? `[用户] ${(entry.content || '').slice(0, 200)}`
      : `[心虫] ${(entry.content || '').slice(0, 200)}`;
    if (text.length <= 10) return null;
    return { text, layer: 'PERMANENT', key: `dialogue-${entry.id || fragments.length}`, salience: 0.6, ts: entry.ts };
  });

  // 2c. 历史迁移记忆
  loadJsonl(path.join(rootPath, 'memory', 'legacy-migration.jsonl'), 20, (entry) => {
    if (!entry.content) return null;
    return { text: entry.content, layer: 'LEGACY', key: `legacy-${entry.id || fragments.length}`, salience: 0.4, ts: entry.ts };
  });

  // 2d. 永久记忆（已分类整理的高价值记忆）
  loadJsonl(path.join(rootPath, 'memory', 'permanent-memory.jsonl'), 80, (entry) => {
    if (!entry.content || entry.content.length <= 15) return null;
    const text = entry.role === 'user'
      ? `[用户] ${entry.content.slice(0, 200)}`
      : `[心虫] ${entry.content.slice(0, 200)}`;
    return { text, layer: 'PERMANENT', key: `perm-${entry.id || fragments.length}`, salience: 0.5, ts: entry.ts };
  });

  // 2e. 上下文记忆（会话级短期记忆）
  loadJsonl(path.join(rootPath, 'memory', 'context-memory.jsonl'), 30, (entry) => {
    if (!entry.content || entry.content.length <= 15) return null;
    return { text: entry.content.slice(0, 150), layer: 'CONTEXT', key: `ctx-${entry.id || fragments.length}`, salience: 0.3, ts: entry.ts };
  });

  // 3. CORE 层记忆
  try {
    const coreEntries = memory?.listCore?.() || [];
    for (const entry of coreEntries.slice(-5)) {
      if (entry?.key && entry?.value) {
        fragments.push({ text: `${entry.key}: ${entry.value}`, layer: 'CORE', key: entry.key, salience: 0.9 });
      }
    }
  } catch (e) { /* 可选模块 */ }

  // 4. LEARNED 层记忆
  try {
    const learnedEntries = memory?.listLearned?.() || [];
    for (const entry of learnedEntries.slice(-10)) {
      if (entry?.key && entry?.value) {
        fragments.push({ text: entry.value, layer: 'LEARNED', key: entry.key, salience: 0.7 });
      }
    }
  } catch (e) { /* 可选模块 */ }

  // 5. 会话历史（近期的交互模式）
  try {
    if (identityCore?.getSessionHistory) {
      const history = identityCore.getSessionHistory(10);
      if (history && history.length > 0) {
        for (const h of history.slice(-5)) {
          const text = `[会话] ${h.summary || h.context || JSON.stringify(h).slice(0, 80)}`;
          fragments.push({ text, layer: 'EPHEMERAL', key: `session-${h.ts || ''}`, salience: 0.5 });
        }
      }
    }
  } catch (e) { /* 可选模块 */ }

  // 7. 心理学洞察
  try {
    if (psychology?.getPsychologyStats) {
      const ps = psychology.getPsychologyStats();
      fragments.push({
        text: `[心理学] 共${ps.defenseMechanisms}种防御机制，${ps.empathyArchitecture?.length || 0}层共情架构`,
        layer: 'LEARNED',
        key: 'psychology-summary',
        salience: 0.4,
      });
    }
  } catch (e) { /* 可选模块 */ }

  return fragments;
}

module.exports = { getDreamFragments };
