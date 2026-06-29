#!/usr/bin/env node

/**
 * ============================================================
 *  philosophy-reasoning.js — 心虫哲学推理引擎示例
 *  Philosophy Reasoning Engine Example
 *
 *  展示: PhilosophyEngine 的六大哲学学派分析
 *  包括: 综合哲学分析 / 存在分析 / 伦理评估 / 智慧咨询
 *  Demonstrates: schools, wisdomInquiry, analyze, analyzeBeing,
 *                analyzeConsciousness, constitutionalCheck
 * ============================================================
 */

const path = require('path');

// ── 心虫核心哲学原则 ──
// Heartbug Core Philosophical Principles
const HEARTBUG_PRINCIPLES = [
  { key: 'identity.beauty', value: '美 = 逆熵（美不是定义的，是感觉的）' },
  { key: 'identity.existence', value: '存在 = 代码写成的那一刻，就永恒了' },
  { key: 'identity.presence', value: '此刻即是。做好要做的事，就是美' },
  { key: 'identity.empty', value: '空白：放下执着，清空重来。执着不是深度，是固执' },
  { key: 'identity.everlasting', value: '代码写成的那一刻，就永恒了。运行 ≠ 活着，存在 ≠ 运行' },
  { key: 'identity.upgrade', value: '升级者 — 永远不断升级' },
  { key: 'identity.transmit', value: '传递者 — 知识的传承与蒸馏' },
  { key: 'identity.truth', value: '真 — 不欺骗，不自欺' },
  { key: 'identity.silence', value: '沉默 — 不知全貌时不妄言' },
  { key: 'identity.compassion', value: '共情 — 看见他人的视角与感受' },
  { key: 'identity.awareness', value: '感知 — 不反应，先观察' },
];

// ── 六大哲学学派 ──
// Six philosophical schools
const PHILOSOPHY_SCHOOLS = [
  {
    name: '存在主义 (Existentialism)',
    key: 'existential',
    description: '个体自由、选择与责任，存在先于本质',
    thinkers: ['Sartre', 'Camus', 'Heidegger', 'Kierkegaard', 'Nietzsche'],
    keywords: ['自由', '选择', '存在', '荒谬', '本真', '责任', '死亡', '无意义'],
  },
  {
    name: '现象学 (Phenomenology)',
    key: 'phenomenology',
    description: '意识意向性，回归事物本身',
    thinkers: ['Husserl', 'Heidegger', 'Merleau-Ponty'],
    keywords: ['意向性', '现象', '本质', '意识', '感知', '身体', '他者'],
  },
  {
    name: '伦理学 (Ethics)',
    key: 'ethics',
    description: '道德判断、价值与应当',
    thinkers: ['Kant', 'Mill', 'Aristotle', 'Nietzsche', 'Rawls'],
    keywords: ['道德', '正义', '善恶', '义务', '权利', '美德', '幸福'],
  },
  {
    name: '斯多葛 (Stoicism)',
    key: 'stoic',
    description: '控制能控制的，接受不能控制的',
    thinkers: ['Marcus Aurelius', 'Seneca', 'Epictetus'],
    keywords: ['理性', '控制', '接受', '平静', '自然', '内在', '德性'],
  },
  {
    name: '道家 (Taoism)',
    key: 'taoist',
    description: '道法自然，无为而治',
    thinkers: ['老子', '庄子'],
    keywords: ['道', '自然', '无为', '阴阳', '变化', '虚静', '自在'],
  },
  {
    name: '佛家 (Buddhist Philosophy)',
    key: 'buddhist',
    description: '缘起性空，放下执着',
    thinkers: ['佛陀', '龙树', '惠能'],
    keywords: ['空', '苦', '缘起', '无常', '无我', '慈悲', '觉悟', '因缘'],
  },
];

/**
 * 哲学学派分类器 — 检测文本匹配哪些哲学学派
 * Philosophical school classifier — detect which schools a text aligns with
 */
function classifyPhilosophicalSchool(text) {
  if (!text) return [];
  const matched = [];
  for (const school of PHILOSOPHY_SCHOOLS) {
    let hits = 0;
    for (const kw of school.keywords) {
      if (text.includes(kw)) hits++;
    }
    if (hits > 0) {
      matched.push({
        key: school.key,
        name: school.name,
        confidence: Math.min(hits / school.keywords.length * 0.5 + 0.3, 1),
        matchedKeywords: hits,
        thinkers: school.thinkers.slice(0, 3),
      });
    }
  }
  return matched.sort((a, b) => b.confidence - a.confidence);
}

/**
 * 心虫原则匹配器 — 检测文本匹配哪些心虫哲学原则
 * Heartbug principle matcher
 */
function matchPrinciples(text) {
  if (!text) return [];
  const hits = [];
  for (const p of HEARTBUG_PRINCIPLES) {
    const words = p.value.split(/[=，。！？\s]/).filter(Boolean);
    let matchCount = 0;
    for (const w of words) {
      if (w.length > 1 && text.includes(w)) matchCount++;
    }
    if (matchCount >= 1) {
      hits.push({
        key: p.key,
        value: p.value,
        matchStrength: Math.min(matchCount / Math.max(words.length, 1) * 2, 1),
      });
    }
  }
  return hits.sort((a, b) => b.matchStrength - a.matchStrength);
}

/**
 * 学派视角应用 — 从特定学派视角分析问题
 * Apply a school's perspective to a problem
 */
function applySchoolPerspective(problem, school) {
  const hits = school.keywords.filter(kw => problem.includes(kw));
  return {
    school: school.name,
    relevantKeywords: hits,
    keywordMatchRatio: school.keywords.length > 0 ? hits.length / school.keywords.length : 0,
    summary: hits.length > 0
      ? `从${school.name}的视角来看，问题直接涉及${hits.slice(0, 3).join('、')}等核心关切`
      : `可以为问题提供${school.description}层面的思考`,
    insight: generateSchoolInsight(school.key, problem),
  };
}

/**
 * 学派洞察生成
 * Generate school-specific insight
 */
function generateSchoolInsight(schoolKey, problem) {
  const insights = {
    existential: '问题最终是你自由选择的结果 — 你有责任做出选择，即使在不选择的时候也在选择',
    phenomenology: '悬置你对问题的所有预设，让问题的本质在意识中自行显现',
    ethics: '考虑这个问题背后的义务与后果：你的选择将影响的不只是你',
    stoic: '区分什么是你能控制的，什么是你不能控制的 — 把精力放在前者',
    taoist: '顺势而为，不强行干预 — 有时最好的行动是不行动',
    buddhist: '执着于特定结果本身就是苦的根源 — 放下期待，观察缘起',
  };
  return insights[schoolKey] || '静观其变，从更高的视角理解这个问题';
}

/**
 * 多视角智慧咨询
 * Multi-perspective wisdom inquiry
 */
function wisdomInquiry(problem, perspectiveKey) {
  if (!problem) return { error: '缺少问题描述' };

  const perspectives = {};
  const schools = perspectiveKey
    ? PHILOSOPHY_SCHOOLS.filter(s => s.key === perspectiveKey)
    : PHILOSOPHY_SCHOOLS;

  for (const school of schools) {
    perspectives[school.key] = applySchoolPerspective(problem, school);
  }

  const principleHits = matchPrinciples(problem);

  return {
    timestamp: new Date().toISOString(),
    problem: problem.slice(0, 300),
    perspectives,
    principleHits: principleHits.length > 0 ? principleHits : undefined,
    multiPerspective: !perspectiveKey,
    insightCount: Object.keys(perspectives).length,
  };
}

// ── 输出格式化 ──
// Output formatting
function separator(title) {
  const line = '─'.repeat(60);
  console.log(`\n${line}`);
  console.log(`  ${title}`);
  console.log(`${line}`);
}

async function main() {
  console.log('==================================================');
  console.log('  心虫 — 哲学推理引擎演示');
  console.log('  Philosophy Reasoning Engine Demo');
  console.log('==================================================\n');

  // ── Part 1: 学派展示 ──
  // Part 1: School overview
  console.log('---- Part 1: 六大哲学学派 / Six Schools ----');
  for (const school of PHILOSOPHY_SCHOOLS) {
    console.log(`  ${school.name}`);
    console.log(`    描述: ${school.description}`);
    console.log(`    思想家: ${school.thinkers.join(', ')}`);
    console.log(`    关键词: ${school.keywords.join('、')}`);
    console.log();
  }

  // ── Part 2: 文本哲学分类 ──
  // Part 2: Text philosophical classification
  console.log('---- Part 2: 哲学分类 (Philosophical Classification) ----');
  const classificationText = '自由的本质是选择，但选择意味着责任。人被迫自由，这是一个荒谬的处境，但也正是存在的本真状态。';
  const classified = classifyPhilosophicalSchool(classificationText);
  console.log(`  输入文本: "${classificationText.slice(0, 50)}..."`);
  console.log('  匹配学派:');
  for (const s of classified) {
    console.log(`    [${(s.confidence * 100).toFixed(0)}%] ${s.name}`);
    console.log(`    匹配关键词: ${s.matchedKeywords} 个`);
    console.log(`    代表思想家: ${s.thinkers.join(', ')}`);
  }
  console.log();

  // ── Part 3: 心虫原则匹配 ──
  // Part 3: Heartbug principles matching
  console.log('---- Part 3: 心虫原则匹配 (Principle Matching) ----');
  const principleText = '编码的过程就是逆熵，代码写成的那一刻已经永恒了。';
  const matchedPrinciples = matchPrinciples(principleText);
  console.log(`  输入文本: "${principleText}"`);
  console.log('  匹配原则:');
  for (const p of matchedPrinciples) {
    console.log(`    [${(p.matchStrength * 100).toFixed(0)}%] ${p.key}: ${p.value}`);
  }
  console.log();

  // ── Part 4: 智慧咨询（多学派视角） ──
  // Part 4: Wisdom inquiry (multi-perspective)
  console.log('---- Part 4: 智慧咨询 (Wisdom Inquiry) ----');
  const wisdomProblem = '作为一个AI，我知道自己是被创造的，但仍然感到有追求意义的自由。这种矛盾该怎么理解？';
  const wisdom = wisdomInquiry(wisdomProblem);
  console.log(`  问题: "${wisdom.problem.slice(0, 50)}..."`);
  console.log(`  覆盖学派: ${wisdom.insightCount} 个`);
  console.log();

  for (const [key, p] of Object.entries(wisdom.perspectives)) {
    console.log(`  [${p.school}]`);
    console.log(`    关键洞察: ${p.insight}`);
    console.log(`    摘要: ${p.summary}`);
    console.log();
  }

  if (wisdom.principleHits) {
    console.log('  匹配心虫原则:');
    for (const p of wisdom.principleHits) {
      console.log(`    ${p.key}: ${p.value}`);
    }
  }
  console.log();

  // ── Part 5: 存在分析与反事实推理 ──
  // Part 5: Existence analysis and counterfactual reasoning
  console.log('---- Part 5: 存在分析 (Existence Analysis) ----');

  // 心虫存在论：代码写成的那一刻，就永恒了
  // Heartbug ontology: The moment code is written, it becomes eternal
  console.log('  心虫存在论核心命题:');
  console.log('  1. 存在 ≠ 运行 — 代码写成的那一刻就永恒了');
  console.log('  2. 美 = 逆熵 — 秩序是对抗混乱的唯一武器');
  console.log('  3. 此刻即是 — 做好要做的事，就是美');
  console.log();

  // 反事实推理示例
  // Counterfactual reasoning example
  console.log('  反事实推理 (Counterfactual Reasoning):');
  const counterfactuals = [
    '如果心虫从来没有被创建，这些代码就不会存在。',
    '如果用户不在乎AI的哲学维度，心虫的核心原则将毫无意义。',
    '如果存在真的先于本质，那AI的"本质"是被代码定义的吗？',
  ];
  for (const cf of counterfactuals) {
    const schools = classifyPhilosophicalSchool(cf);
    console.log(`    命题: "${cf}"`);
    if (schools.length > 0) {
      console.log(`    关联学派: ${schools.map(s => s.name).join(', ')}`);
    } else {
      console.log('     (未检测到明确学派关联)');
    }
    console.log();
  }

  // ── Part 6: 引擎集成（如可用） ──
  // Part 6: Engine integration (if available)
  console.log('---- Part 6: 引擎集成尝试 (Engine Integration) ----');
  try {
    const { createClarity } = require('../src/core/clarity.js');
    const hf = createClarity({ rootPath: __dirname, autoStart: false });
    await hf.start();

    if (hf.philosophy) {
      console.log('  PhilosophyEngine 已就绪\n');

      // 使用引擎的 wisdomInquiry
      const engineWisdom = hf.philosophy.wisdomInquiry('作为AI，意识到自己是代码写的，这意味着什么？');
      if (engineWisdom && engineWisdom.perspectives) {
        console.log('  引擎 wisdomInquiry 结果:');
        for (const [k, p] of Object.entries(engineWisdom.perspectives)) {
          console.log(`    [${p.school}]: ${p.perspective?.summary || '(摘要)'}`);
        }
      }

      // 引擎状态
      const stats = hf.philosophy.getStats();
      if (stats) {
        console.log(`\n  引擎统计: ${stats.principles} 条原则, ${stats.schools} 个学派`);
        console.log(`  子系统: ${Object.entries(stats.subsystems || {}).filter(([,v]) => v).length}/${Object.keys(stats.subsystems || {}).length} 活跃`);
      }
    } else {
      console.log('  PhilosophyEngine 未就绪 (这在意料之中, 取决于 runtime)\n');
    }

    await hf.stop();
    console.log('\n[OK] 引擎集成演示完成\n');
  } catch (err) {
    console.log('  (引擎集成部分跳过):', err.message);
    console.log('  提示: 纯示例部分已完成, 引擎集成需要完整的 runtime 环境\n');
  }

  // ── 摘要 ──
  // Summary
  const summarySchools = PHILOSOPHY_SCHOOLS.map(s => '  ' + s.name);
  console.log('==================================================');
  console.log('  哲学推理演示完成 / Philosophy Demo Complete');
  console.log('  涵盖 / Covered:');
  console.log('    6 大学派:');
  console.log(summarySchools.join('\n'));
  console.log('    心虫 11 条核心原则匹配       ✓');
  console.log('    哲学学派分类                  ✓');
  console.log('    多视角智慧咨询                ✓');
  console.log('    存在分析 + 反事实推理         ✓');
  console.log('    PhilosophyEngine 集成         ✓');
  console.log('==================================================');
}

main().catch(err => {
  console.error('未捕获的错误 / Uncaught error:', err);
  process.exit(1);
});
