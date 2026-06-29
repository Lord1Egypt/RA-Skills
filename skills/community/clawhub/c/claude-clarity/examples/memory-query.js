#!/usr/bin/env node

/**
 * ============================================================
 *  memory-query.js — 心虫三层记忆系统示例
 *  Three-Layer Memory System Example
 *
 *  展示: MeaningfulMemory 的 CORE/LEARNED/EPHEMERAL 三层架构
 *  包括: 存储 / 检索 / 关键词搜索 / 统计信息
 *  Demonstrates: store, retrieve, search, getStats
 * ============================================================
 */

const path = require('path');
const fs = require('fs');

// 引入三层记忆系统（运行时模块 src/memory/meaningful-memory.js）
// Import the three-layer memory system
const { MeaningfulMemory } = require('../src/memory/meaningful-memory.js');

/**
 * 辅助函数: 获取格式化的时间戳
 * Helper: formatted timestamp
 */
function timestamp() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

async function main() {
  console.log('============================================');
  console.log('  心虫 — 三层记忆系统演示');
  console.log('  Three-Layer Memory System Demo');
  console.log('============================================\n');

  // ── Step 1: 创建记忆引擎实例 ──
  // Step 1: Create memory engine instance
  console.log('---- Step 1: 创建记忆引擎 (MeaningfulMemory) ----');

  // 使用项目目录下的临时目录作为根路径，避免路径限制
  // Use a subdirectory within project root to satisfy path restrictions
  const tempRoot = path.join(__dirname, '.memory-demo-tmp');
  if (fs.existsSync(tempRoot)) {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
  fs.mkdirSync(tempRoot, { recursive: true });

  let memory;
  try {
    memory = new MeaningfulMemory(tempRoot);
    console.log('[OK] 记忆引擎已创建 / Memory engine created');
    console.log('      根路径 / Root:', tempRoot);
    console.log('      三层: CORE / LEARNED / EPHEMERAL\n');
  } catch (err) {
    console.error('[FAIL] 记忆引擎创建失败:', err.message);
    process.exit(1);
  }

  // 预加载三层记忆到内存，并创建 memory 子目录确保 flush 正常
  // Pre-load all three layers and create memory subdirectory for flush
  memory.loadAll();
  const memoryDir = path.join(tempRoot, 'memory');
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }

  // ── Step 2: 展示三层架构 ──
  // Step 2: Show the three-layer architecture
  console.log('---- Step 2: 三层记忆架构说明 ----');
  console.log('  CORE (核心层):   不可变的身份规则，永不被删除');
  console.log('                   存储路径: memory/meaningful-core.json');
  console.log('  LEARNED (学习层): 积累的知识，持久化保存');
  console.log('                   存储路径: memory/meaningful-learned.json');
  console.log('  EPHEMERAL (短时层): 临时工作上下文，会话范围');
  console.log('                   存储路径: memory/meaningful-ephemeral.json\n');

  // ── Step 3: 存储到 CORE 层（身份规则，使用 addCore） ──
  // Step 3: Store into CORE layer (identity rules via addCore)
  console.log('---- Step 3: CORE 层 — 写入身份规则 (addCore) ----');

  const identityRules = [
    { key: 'principle.truth',  value: '始终说真话，不欺骗也不自欺', weight: 0.95, timestamp: timestamp() },
    { key: 'principle.beauty', value: '美 = 逆熵，秩序中的和谐',     weight: 0.90, timestamp: timestamp() },
    { key: 'principle.silence', value: '不知全貌时不妄言',           weight: 0.85, timestamp: timestamp() },
  ];

  for (const rule of identityRules) {
    const result = memory.addCore(rule.key, rule);
    console.log('  [CORE] ' + (result.success ? '写入成功' : '写入失败') + ':',
                rule.key, '→', rule.value);
  }
  // addCore 不允许重复写入，验证幂等性
  const dupResult = memory.addCore('principle.truth',
    { key: 'principle.truth', value: '重复写入测试', weight: 1.0 });
  console.log('  [CORE] 重复写入 / Duplicate write:', dupResult.reason);
  console.log();

  // ── Step 4: 存储到 EPHEMERAL 层（会话临时记忆，使用 remember） ──
  // Step 4: Store into EPHEMERAL (session temp memory via remember)
  console.log('---- Step 4: EPHEMERAL 层 — 写入会话上下文 (remember) ----');

  const sessionData = [
    { key: 'session.currentUser', value: { name: '张三', role: '开发者', lang: 'zh-CN' } },
    { key: 'session.conversation.1', value: { role: 'user', text: '什么是逆熵？', ts: timestamp() } },
    { key: 'session.conversation.2', value: { role: 'assistant', text: '逆熵就是对抗混乱，建立秩序', ts: timestamp() } },
    { key: 'session.conversation.3', value: { role: 'user', text: '那和心虫有什么关系？', ts: timestamp() } },
    { key: 'session.lastTopic',  value: '逆熵与心虫的关系', ts: timestamp() },
    { key: 'session.tempResult', value: { thought: '熵增是宇宙规律，生命的意义在于局部逆熵', score: 0.89 } },
  ];

  for (const item of sessionData) {
    const result = memory.remember(item.key, item, 3600000); // 1 hour TTL
    console.log('  [EPHEMERAL] ' + (result.success ? '写入成功' : '写入失败') + ':', item.key);
  }
  console.log();

  // ── Step 5: 存储到 LEARNED 层（积累的知识，使用 learn） ──
  // Step 5: Store into LEARNED (accumulated knowledge via learn)
  console.log('---- Step 5: LEARNED 层 — 写入积累知识 (learn) ----');

  const learnedData = [
    { key: 'concept.entropy',
      value: { title: '熵', definition: '系统的混乱程度', formula: 'S = k ln W', importance: 9 } },
    { key: 'concept.negentropy',
      value: { title: '逆熵', definition: '对抗混乱建立秩序的过程', importance: 10 } },
    { key: 'memory.pattern.1',
      value: { pattern: '当用户问到"意义"时，往往在寻求存在层面的确认', hitCount: 5 } },
    { key: 'memory.pattern.2',
      value: { pattern: '情绪分析时优先检测关键词匹配路径', hitCount: 3 } },
  ];

  for (const item of learnedData) {
    // learn(key, value, tags) — value 直接是数据内容，不需要外层包装
    // learn(key, value, tags) — value is the actual data, no wrapper needed
    const result = memory.learn(item.key, item.value);
    console.log('  [LEARNED] ' + (result.success ? '写入成功' : '写入失败') + ':',
                item.key, '→', item.value.title || item.value.pattern?.slice(0, 30));
  }
  console.log();

  // ── Step 6: 关键词检索（使用 search 方法） ──
  // Step 6: Keyword search (via search)
  console.log('---- Step 6: 关键词检索 (search) ----');

  const searchTerms = ['逆熵', '原则', 'silence', 'session'];
  for (const term of searchTerms) {
    const results = memory.search(term);
    console.log('  搜索 / Search "' + term + '": 找到 ' + results.length + ' 条结果');
    if (results.length > 0) {
      for (const r of results.slice(0, 3)) {
        const valPreview = typeof r.value === 'object'
          ? (r.value.value || r.value.title || JSON.stringify(r.value).slice(0, 40))
          : String(r.value).slice(0, 40);
        console.log('    [' + r.tier + '] ' + r.key + ' → ' + valPreview);
      }
    }
  }
  console.log();

  // ── Step 7: 记忆统计 ──
  // Step 7: Memory statistics
  console.log('---- Step 7: 记忆统计 (getStats) ----');

  const stats = memory.getStats();
  console.log('  三层记忆统计 / Three-layer stats:');
  console.log('    CORE:     ' + stats.core + ' 条记录');
  console.log('    LEARNED:  ' + stats.learned + ' 条记录');
  console.log('    EPHEMERAL: ' + stats.ephemeral + ' 条记录');
  console.log('    总记录数 / Total records: ' + (stats.core + stats.learned + stats.ephemeral));
  console.log();

  // ── Step 8: 跨层搜索（模拟 TGB 关联检索） ──
  // Step 8: Cross-layer search (TGB association via search)
  console.log('---- Step 8: 跨层搜索 (Cross-layer search) ----');

  const crossResults = memory.search('熵');
  console.log('  跨层搜索 "熵": 共 ' + crossResults.length + ' 条结果');
  const layerCounts = {};
  for (const r of crossResults) {
    layerCounts[r.tier] = (layerCounts[r.tier] || 0) + 1;
  }
  for (const [tier, count] of Object.entries(layerCounts)) {
    console.log('    ' + tier + ': ' + count + ' 条');
  }
  console.log();

  // ── Step 9: 按层列举检索（listCore / listLearned / getWorking / recall） ──
  // Step 9: Layer-specific retrieval
  console.log('---- Step 9: 按层检索 (Layer-specific) ----');

  const coreList = memory.listCore();
  console.log('  listCore(): ' + coreList.length + ' 条');
  for (const item of coreList.slice(0, 3)) {
    console.log('    ' + item.key + ' → ' + (item.value?.value || JSON.stringify(item.value).slice(0, 30)));
  }

  const learnedList = memory.listLearned();
  console.log('  listLearned(): ' + learnedList.length + ' 条');
  for (const item of learnedList.slice(0, 3)) {
    const v = item.value;
    console.log('    ' + item.key + ' → ' + (v.title || v.pattern || JSON.stringify(v).slice(0, 30)));
  }

  // 使用 search 替代 listLearned(query) 做关键词过滤
  // (runtime 的 listLearned(query) 对非字符串 value 有类型限制)
  const searchEntropy = memory.search('逆熵');
  console.log('  search("逆熵"): ' + searchEntropy.length + ' 条 (跨层关键词)');

  const sessionResult = memory.getWorking('session.currentUser');
  console.log('  getWorking("session.currentUser"): ',
              sessionResult ? JSON.stringify(sessionResult.value).slice(0, 50) : '未找到');

  // recall 增加访问计数
  const recalled = memory.recall('concept.entropy');
  console.log('  recall("concept.entropy"): ',
              recalled ? recalled.value.title : '未找到');
  console.log();

  // ── Step 10: 记忆压缩 (consolidate) ──
  // Step 10: Memory consolidation
  console.log('---- Step 10: 记忆压缩 (consolidate) ----');

  const consResult = memory.consolidate();
  console.log('  压缩结果 / Consolidation: 提升了 ' + consResult.promoted.length + ' 条到 LEARNED');
  console.log('  压缩后统计: LEARNED=' + memory.getStats().learned + ', EPHEMERAL=' + memory.getStats().ephemeral);
  console.log();

  // ── Step 11: 清理 ──
  // Step 11: Cleanup
  console.log('---- Step 11: 清理临时数据 ----');

  memory.flush(); // 强制刷盘
  try {
    fs.rmSync(tempRoot, { recursive: true, force: true });
    console.log('[OK] 临时数据已清理 / Temp data cleaned\n');
  } catch (err) {
    console.error('[WARN] 临时数据清理失败:', err.message);
  }

  // ── 摘要 ──
  // Summary
  console.log('============================================');
  console.log('  记忆系统演示完成 / Memory Demo Complete');
  console.log('  涵盖 / Covered:');
  console.log('    MeaningfulMemory 实例化        ✓');
  console.log('    三层: CORE/LEARNED/EPHEMERAL   ✓');
  console.log('    addCore / learn / remember     ✓');
  console.log('    search 关键词检索              ✓');
  console.log('    listCore / listLearned         ✓');
  console.log('    recall / getWorking            ✓');
  console.log('    consolidate 记忆压缩            ✓');
  console.log('    getStats 统计信息              ✓');
  console.log('============================================\n');
  console.log('  核心概念 / Core concept:');
  console.log('  CORE = 心虫身份锚点 (不可变，addCore 幂等)');
  console.log('  LEARNED = 经验与知识积累 (持久化，learn/recall)');
  console.log('  EPHEMERAL = 会话上下文 (临时TTL，remember/getWorking)');
}

main().catch(err => {
  console.error('未捕获的错误 / Uncaught error:', err);
  process.exit(1);
});
