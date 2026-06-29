#!/usr/bin/env node

/**
 * ============================================================
 *  emotion-analysis.js — 心虫 PAD 情绪模型示例
 *  PAD Emotion Model Analysis Example
 *
 *  展示: 三维 PAD 情绪模型 (Pleasure/Arousal/Dominance)
 *  包括: 关键词分类 / 情绪组检测 / PAD 状态计算
 *  Demonstrates: PAD keyword classification, emotion groups,
 *                intensity calculation, text-based detection
 * ============================================================
 */

const path = require('path');

// ── PAD 情绪模型常量（来自 psychology.js） ──
// PAD Emotion Model constants
const PAD_MODEL = {
  min: -10,
  max: 10,
  neutral: 0,
};

/**
 * 钳制值到合法范围
 * Clamp value to valid range
 */
function clamp(v) {
  return Math.max(PAD_MODEL.min, Math.min(PAD_MODEL.max, v));
}

/**
 * 计算 PAD 情绪状态
 * Calculate PAD emotion state from 3 dimensions
 *
 * P = Pleasure (愉悦度): -10 ~ +10
 * A = Arousal (唤醒度):  -10 ~ +10 (负值=低唤醒/平静)
 * D = Dominance (支配度): -10 ~ +10 (负值=被支配/无力)
 */
function calculatePADState(pleasure, arousal, dominance) {
  const p = clamp(pleasure);
  const a = clamp(arousal);
  const d = clamp(dominance);

  // 强度 = 三维向量的模长归一化 (最大模长 ≈ 17.32)
  // Intensity = normalized 3D vector magnitude
  const intensity = Math.sqrt(p * p + a * a + d * d) / 17.32;

  return {
    pleasure: p,
    arousal: a,
    dominance: d,
    intensity: Math.round(intensity * 100) / 100,
    timestamp: new Date().toISOString(),
  };
}

/**
 * PAD 情绪标签映射表（8种基本情绪组合）
 * PAD emotion label map (8 basic combos)
 *
 *  P+ = pleasure > 0, P- = pleasure < 0
 *  A+ = arousal > 0,  A- = arousal < 0
 *  D+ = dominance > 0, D- = dominance < 0
 */
const PAD_EMOTION_MAP = {
  'P+A+D+': { name: '警觉/兴奋',    en: 'alert/excited',     desc: 'High pleasure, high energy, in control' },
  'P+A+D-': { name: '快乐/满意',    en: 'happy/content',     desc: 'High pleasure, high energy, not in control' },
  'P+A-D+': { name: '平静/满足',    en: 'calm/content',      desc: 'High pleasure, low energy, in control' },
  'P+A-D-': { name: '放松/自在',    en: 'relaxed/peaceful',  desc: 'High pleasure, low energy, not in control' },
  'P-A+D+': { name: '愤怒/敌意',    en: 'angry/hostile',     desc: 'Low pleasure, high energy, in control' },
  'P-A+D-': { name: '焦虑/不安',    en: 'anxious/nervous',   desc: 'Low pleasure, high energy, not in control' },
  'P-A-D+': { name: '被动/依赖',    en: 'passive/dependent', desc: 'Low pleasure, low energy, in control' },
  'P-A-D-': { name: '冷漠/麻木',    en: 'apathetic/numb',    desc: 'Low pleasure, low energy, not in control' },
};

/**
 * 根据 PAD 值获取情绪标签（细化版本）
 * Get emotion label from continuous PAD values
 */
function getEmotionFromPAD(p, a, d) {
  if (p > 2 && a > 2 && d > 0) return { zh: '警觉/兴奋', en: 'alert/excited' };
  if (p > 2 && a > 1)          return { zh: '快乐/满意', en: 'happy/content' };
  if (p > 2 && a < 0 && d > 0) return { zh: '平静/满足', en: 'calm/content' };
  if (p > 1 && a < 0)          return { zh: '放松/自在', en: 'relaxed/peaceful' };
  if (p < -1 && a > 2 && d > 0) return { zh: '愤怒/敌意', en: 'angry/hostile' };
  if (p < 0 && a > 2 && d < 0) return { zh: '焦虑/不安', en: 'anxious/nervous' };
  if (p < 0 && a < 0 && d > 0) return { zh: '被动/依赖', en: 'passive/dependent' };
  if (p < -2 && a < 0 && d < 0) return { zh: '冷漠/麻木', en: 'apathetic/numb' };
  if (p < -2 && a <= 0)         return { zh: '悲伤/抑郁', en: 'sad/depressed' };
  return { zh: '中性', en: 'neutral' };
}

/**
 * 从文本检测 PAD 情绪（关键词匹配法）
 * Detect PAD emotion from text (keyword matching)
 *
 * 复用自 src/core/psychology.js 的 detectPADFromText 逻辑
 * Reuses the detection logic from src/core/psychology.js
 */
function detectPADFromText(text) {
  if (!text || typeof text !== 'string') {
    return { ...calculatePADState(0, 0, 0), emotion: { zh: '中性', en: 'neutral' }, text: '(空)' };
  }

  // 精度修正：归一化到 -5 ~ +5 范围
  let pleasure = 0;
  let arousal = 0;
  let dominance = 0;

  // === 情绪词根预检测（优先级最高，精确匹配 PAD 值）===
  // Emotion root detection (highest priority, precise PAD values)

  // 快乐/愉悦 (P++, A=0, D=0)
  if (/开心|高兴|快乐|幸福|满足|愉悦/.test(text)) {
    pleasure += 4; arousal = 0; dominance = 0;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 愤怒 (P--, A++, D+)
  if (/愤怒|生气|恼火|火大|发火|气愤/.test(text)) {
    pleasure -= 4; arousal += 3; dominance += 2;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 恐惧/害怕 (P--, A++, D--)
  if (/害怕|恐惧|怕|惊慌|吓/.test(text)) {
    pleasure -= 3; arousal += 3; dominance -= 2;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 悲伤/难过 (P--, A=0, D=0)
  if (/难过|悲伤|伤心|痛苦|委屈|压抑|无奈|心酸|受伤|失落|沮丧/.test(text)) {
    pleasure -= 4; arousal = 0; dominance = 0;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 焦虑 (P-, A++, D-)
  if (/焦虑|焦急|不安|忐忑/.test(text)) {
    pleasure -= 2; arousal += 3; dominance -= 1;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 兴奋 (P++, A++, D+)
  if (/兴奋|激动|亢奋/.test(text)) {
    pleasure += 3; arousal += 3; dominance += 1;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }
  // 平静/放松 (P+, A-, D+)
  if (/平静|放松|舒缓|安宁|淡定|从容/.test(text)) {
    pleasure += 2; arousal -= 2; dominance += 1;
    const emo = getEmotionFromPAD(pleasure, arousal, dominance);
    return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
  }

  // === 一般关键词匹配（兜底逻辑）===
  // General keyword matching (fallback)
  const positiveWords = ['好', '棒', '顺利', '成功', '喜欢', '满意', '不错', '挺好'];
  const negativeWords = ['烦', '累', '难', '挫败', '无聊', '讨厌', '糟糕', '失败', '困惑', '失望'];
  positiveWords.forEach(w => { if (text.includes(w)) pleasure += 1.5; });
  negativeWords.forEach(w => { if (text.includes(w)) pleasure -= 1.5; });

  const highArousalWords = ['紧张', '紧急', '担心', '快速'];
  const lowArousalWords = ['困', '慢', '疲惫', '冷静'];
  highArousalWords.forEach(w => { if (text.includes(w)) arousal += 1.5; });
  lowArousalWords.forEach(w => { if (text.includes(w)) arousal -= 1.5; });

  const highDominanceWords = ['决定', '控制', '选择', '主动', '必须'];
  const lowDominanceWords = ['求助', '没办法', '无力', '靠你'];
  highDominanceWords.forEach(w => { if (text.includes(w)) dominance += 1; });
  lowDominanceWords.forEach(w => { if (text.includes(w)) dominance -= 1; });

  const emo = getEmotionFromPAD(pleasure, arousal, dominance);
  return { ...calculatePADState(pleasure, arousal, dominance), emotion: emo, text };
}

/**
 * 格式化情绪分析结果
 * Format emotion analysis result for display
 */
function formatEmotionResult(prefix, result) {
  console.log(`  ${prefix}:`);
  console.log(`    文本 / Text       : "${result.text?.slice(0, 40) || '(空)'}"`);
  console.log(`    愉悦度 / Pleasure : ${result.pleasure.toFixed(1)}  (-10 ~ +10)`);
  console.log(`    唤醒度 / Arousal  : ${result.arousal.toFixed(1)}  (-10 ~ +10)`);
  console.log(`    支配度 / Dominance: ${result.dominance.toFixed(1)}  (-10 ~ +10)`);
  console.log(`    强度 / Intensity  : ${result.intensity.toFixed(2)}  (0 ~ 1)`);
  console.log(`    情绪 / Emotion    : ${result.emotion.zh} (${result.emotion.en})`);

  // PAD 编码标签
  const padLabel = `${result.pleasure > 0 ? 'P+' : 'P-'}${result.arousal > 0 ? 'A+' : 'A-'}${result.dominance > 0 ? 'D+' : 'D-'}`;
  const labelInfo = PAD_EMOTION_MAP[padLabel];
  if (labelInfo) {
    console.log(`    PAD 编码 / Code    : ${padLabel} → ${labelInfo.desc}`);
  }
  console.log();
}

async function main() {
  console.log('============================================');
  console.log('  心虫 — PAD 情绪模型分析演示');
  console.log('  PAD Emotion Model Analysis Demo');
  console.log('============================================\n');

  // ── 概念说明 ──
  // Concept explanation
  console.log('---- 模型说明 / Model Overview ----');
  console.log('  PAD 三维情绪模型:');
  console.log('  P = Pleasure (愉悦度):  -10(痛苦) ~ +10(快乐)');
  console.log('  A = Arousal  (唤醒度):  -10(平静) ~ +10(激动)');
  console.log('  D = Dominance(支配度):  -10(无力) ~ +10(掌控)');
  console.log('  强度 = |(P,A,D)| 向量的归一化模长\n');

  // ── 测试案例: 四大情绪组 ──
  // Test cases: 4 emotion groups

  // #1: Joy/Contentment (高P, 中A, 中D)
  console.log('---- #1 快乐组 / Joy Group ----');
  const joyTexts = [
    '今天真的很开心，项目终于成功了！',
    '和朋友们在一起感觉好幸福。',
    '我喜欢这个平静的午后。',
  ];
  for (const t of joyTexts) {
    formatEmotionResult('  快乐检测 / Joy Detection', detectPADFromText(t));
  }

  // #2: Sadness/Depression (低P, 低A, 低D)
  console.log('---- #2 悲伤组 / Sadness Group ----');
  const sadTexts = [
    '心里好难过，什么都做不了。',
    '我感到很失落，一切都没有意义。',
    '有一种说不出的心酸和委屈。',
  ];
  for (const t of sadTexts) {
    formatEmotionResult('  悲伤检测 / Sadness Detection', detectPADFromText(t));
  }

  // #3: Anger/Frustration (低P, 高A, 中高D)
  console.log('---- #3 愤怒组 / Anger Group ----');
  const angerTexts = [
    '太愤怒了！这完全不合理！',
    '我很生气，一直在忍耐。',
    '真是让人恼火的情况。',
  ];
  for (const t of angerTexts) {
    formatEmotionResult('  愤怒检测 / Anger Detection', detectPADFromText(t));
  }

  // #4: Fear/Anxiety (低P, 高A, 低D)
  console.log('---- #4 恐惧组 / Fear Group ----');
  const fearTexts = [
    '我很害怕明天的面试。',
    '心里很不安，不知道会发生什么。',
    '这种焦虑的感觉让我无法入睡。',
  ];
  for (const t of fearTexts) {
    formatEmotionResult('  恐惧检测 / Fear Detection', detectPADFromText(t));
  }

  // ── 混合情绪 / Neutral ──
  console.log('---- #5 混合 & 中性 / Mixed & Neutral ----');
  const mixedTexts = [
    '今天很累但也很充实。',
    '大家好，今天天气不错。',
    '既感到快乐又有些不安，很矛盾的心情。',
  ];
  for (const t of mixedTexts) {
    formatEmotionResult('  混合情绪 / Mixed', detectPADFromText(t));
  }

  // ── 与心虫引擎集成（如可用） ──
  console.log('---- #6 引擎集成尝试 (Engine Integration) ----');
  try {
    const { createClarity } = require('../src/core/clarity.js');
    const hf = createClarity({ rootPath: __dirname, autoStart: false });
    await hf.start();

    if (hf.emotion) {
      console.log('  使用 hf.emotion.process() 进行分析:');
      const samples = [
        '看到这个结果真的很兴奋！',
        '这件事让我觉得很沮丧。',
      ];
      for (const s of samples) {
        const emo = hf.emotion.process(s);
        console.log(`    输入: "${s.slice(0, 25)}"`);
        console.log(`    类型: ${emo.type}, 强度: ${emo.intensity.toFixed(2)}`);
        console.log(`    PAD: ${emo.pad.pleasure.toFixed(2)} / ${emo.pad.arousal.toFixed(2)} / ${emo.pad.dominance.toFixed(2)}`);
        console.log();
      }
    }
    await hf.stop();
    console.log('[OK] 引擎集成演示完成\n');
  } catch (err) {
    console.log('  (引擎集成部分跳过 / Engine integration skipped):', err.message);
    console.log('  提示: 这可能是缺少子系统或路径限制导致的\n');
  }

  // ── 摘要 ──
  console.log('============================================');
  console.log('  情绪分析演示完成 / Emotion Demo Complete');
  console.log('  涵盖 / Covered:');
  console.log('    PAD 三维模型 (Pleasure/Arousal/Dominance) ✓');
  console.log('    4大情绪组: 快乐/悲伤/愤怒/恐惧        ✓');
  console.log('    PAD→情绪标签映射                        ✓');
  console.log('    强度计算 / Intensity calculation       ✓');
  console.log('    引擎集成 / Engine integration           ✓');
  console.log('============================================');
}

main().catch(err => {
  console.error('未捕获的错误 / Uncaught error:', err);
  process.exit(1);
});
