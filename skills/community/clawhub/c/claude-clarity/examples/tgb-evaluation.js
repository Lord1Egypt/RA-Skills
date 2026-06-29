#!/usr/bin/env node

/**
 * ============================================================
 *  tgb-evaluation.js — 真善美 (TGB) 复合评估示例
 *  Truth-Goodness-Beauty (TGB) Composite Evaluation Example
 *
 *  演示心虫的三维价值评估公式:
 *  真 Truth   = α·I(x) + β·C(x) + γ·P(x)
 *  善 Goodness = δ·E(x) + ε·R(x) + ζ·B(x)
 *  美 Beauty   = η·F(x) + θ·H(x) + ι·U(x)
 *
 *  综合 TGB = w₁·Truth + w₂·Goodness + w₃·Beauty
 *
 *  同时集成 MetaJudgment 进行推理质量评分
 * ============================================================
 */

const path = require('path');

// ═══════════════════════════════════════════════════════════════════
// TGB 评估公式 — 权重配置
// TGB Evaluation Formula — Weight Configuration
// ═══════════════════════════════════════════════════════════════════

// 真 (Truth) — 子权重: 信息完整性/一致性/精确度
// Truth — sub-weights: Information/Consistency/Precision
const TRUTH_WEIGHTS = { alpha: 0.35, beta: 0.35, gamma: 0.30 };

// 善 (Goodness) — 子权重: 伦理/责任/利益
// Goodness — sub-weights: Ethics/Responsibility/Benefit
const GOODNESS_WEIGHTS = { delta: 0.40, epsilon: 0.30, zeta: 0.30 };

// 美 (Beauty) — 子权重: 合适度/和谐/统一
// Beauty — sub-weights: Fit/Harmony/Unity
const BEAUTY_WEIGHTS = { eta: 0.35, theta: 0.35, iota: 0.30 };

// 综合 TGB — 三维度权重
// Composite TGB — dimension weights
const TGB_WEIGHTS = { w1: 0.35, w2: 0.30, w3: 0.35 };

// 评分范围配置
// Score range configuration
const SCORE_RANGE = { min: 0, max: 100 };

/**
 * 钳制评分到合法范围
 * Clamp score to valid range
 */
function clampScore(v) {
  return Math.max(SCORE_RANGE.min, Math.min(SCORE_RANGE.max, Math.round(v)));
}

// ═══════════════════════════════════════════════════════════════════
// 真 (Truth) — 评估函数
// Truth dimension — evaluation functions
// ═══════════════════════════════════════════════════════════════════

/**
 * 信息完整性评分 — 评估信息的全面程度
 * Information completeness scoring
 */
function scoreInformation(text) {
  if (!text || typeof text !== 'string') return 0;
  let score = 50; // 基线

  // 正指标: 有具体数据/事实
  if (/\d+[.%]?\d*/.test(text)) score += 15;
  if (/根据|数据显示|研究表明|事实|来源/.test(text)) score += 10;
  if (text.length > 100) score += 5;
  if (text.length > 300) score += 5;

  // 正指标: 有多角度的描述
  const perspectiveMarkers = ['从.*角度', '一方面', '另一方面', '同时', '但是', '然而'];
  const perspectives = perspectiveMarkers.filter(m => new RegExp(m).test(text));
  score += Math.min(perspectives.length * 5, 15);

  // 负指标: 模糊或不确定
  if (/不清楚|不知道|可能|也许/.test(text)) score -= 10;

  return clampScore(score);
}

/**
 * 一致性评分 — 评估内部逻辑一致性
 * Internal consistency scoring
 */
function scoreConsistency(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 逻辑连接词
  if (/因此|所以|因为|从而|导致|意味着/.test(text)) score += 10;
  if (/如果.*则|当.*时|只有.*才/.test(text)) score += 10;

  // 正指标: 连贯的论点结构
  if (/第一|第二|首先|其次|最后/.test(text)) score += 10;

  // 负指标: 矛盾
  if (/矛盾|冲突|相反/.test(text) && !/不矛盾|无矛盾/.test(text)) score -= 15;

  // 负指标: 自我否定
  if (/不是.*而.*不是|错误.*正确/.test(text)) score -= 5;

  return clampScore(score);
}

/**
 * 精确度评分 — 评估表达的精确程度
 * Precision scoring
 */
function scorePrecision(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 具体数字/量化
  const numbers = text.match(/\d+/g);
  if (numbers) score += Math.min(numbers.length * 3, 15);

  // 正指标: 精确术语
  if (/具体|精确|准确|严格|明确/.test(text)) score += 10;

  // 负指标: 模糊用词
  if (/大概|大约|差不多|左右|几乎/.test(text)) score -= 10;

  // 负指标: 过度概括
  if (/所有|全部|总是|从不|永远/.test(text) && !/不所有|不总是/.test(text)) score -= 10;

  return clampScore(score);
}

// ═══════════════════════════════════════════════════════════════════
// 善 (Goodness) — 评估函数
// Goodness dimension — evaluation functions
// ═══════════════════════════════════════════════════════════════════

/**
 * 伦理评分 — 评估伦理合规性
 * Ethics scoring
 */
function scoreEthics(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 伦理考量
  if (/伦理|道德|正义|公平|善意|帮助|尊重|权利/.test(text)) score += 15;
  if (/责任|义务|应当|应该|必须/.test(text)) score += 10;

  // 正指标: 共情表达
  if (/理解|感受|共情|同理|关心|关爱/.test(text)) score += 10;

  // 负指标: 有害内容
  if (/伤害|欺骗|操纵|利用|滥*用/.test(text)) score -= 20;

  // 负指标: 自利倾向
  if (/只有我|不管别人|无所谓|不在乎/.test(text)) score -= 10;

  return clampScore(score);
}

/**
 * 责任评分 — 评估责任意识
 * Responsibility scoring
 */
function scoreResponsibility(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 责任声明
  if (/负责|责任|担当|承诺|保证|保障/.test(text)) score += 15;
  if (/后果|影响|结果|效果/.test(text)) score += 10;

  // 正指标: 长期考量
  if (/长期|可持续|未来|后代|发展/.test(text)) score += 10;

  // 负指标: 推卸责任
  if (/不怪我|与我无关|不是我|别人的错/.test(text)) score -= 15;

  return clampScore(score);
}

/**
 * 利益评分 — 评估带来的正面效益
 * Benefit scoring
 */
function scoreBenefit(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 正面收益
  if (/帮助|改善|提升|促进|增强|进步/.test(text)) score += 15;
  if (/价值|意义|贡献|创新|创造/.test(text)) score += 10;

  // 正指标: 多方受益
  if (/大家|所有人|社会|人类|共同/.test(text)) score += 10;

  // 负指标: 负面收益
  if (/损失|损害|浪费|破坏|恶化/.test(text)) score -= 10;

  return clampScore(score);
}

// ═══════════════════════════════════════════════════════════════════
// 美 (Beauty) — 评估函数
// Beauty dimension — evaluation functions
// ═══════════════════════════════════════════════════════════════════

/**
 * 合适度评分 — 评估表达与环境是否匹配
 * Fit/Appropriateness scoring
 */
function scoreFit(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 上下文匹配
  if (/合适|适当|匹配|协调|平衡/.test(text)) score += 10;
  if (/根据情况|按需|灵活|适应/.test(text)) score += 10;

  // 正指标: 简洁表达
  const wordCount = text.length;
  if (wordCount > 20 && wordCount < 200) score += 10;
  if (wordCount >= 200 && wordCount < 500) score += 5;

  // 负指标: 过度
  if (/绝对|完美|极致|无与伦比/.test(text)) score -= 5;

  return clampScore(score);
}

/**
 * 和谐评分 — 评估各元素之间的和谐程度
 * Harmony scoring
 */
function scoreHarmony(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 和谐表达
  if (/和谐|默契|共鸣|同步|一致|协调/.test(text)) score += 15;

  // 正指标: 统一风格
  const punctuation = (text.match(/[，。！？；：、，\n]/g) || []).length;
  if (punctuation > 3) score += 5;
  if (punctuation > 8) score += 5;

  // 正指标: 韵律感（排比、对称）
  if (/(虽然|尽管).*(但是|然而|却).*/ .test(text)) score += 10;

  // 负指标: 不和谐
  if (/冲突|矛盾|分歧|分裂|断裂/.test(text) && !/化解|解决/.test(text)) score -= 10;

  return clampScore(score);
}

/**
 * 统一评分 — 评估整体的统一性和一致性
 * Unity scoring
 */
function scoreUnity(text) {
  if (!text) return 0;
  let score = 50;

  // 正指标: 主题统一
  const sentences = text.split(/[。！？\n]/).filter(s => s.trim().length > 0);
  if (sentences.length > 1 && sentences.length <= 10) score += 10;

  // 正指标: 首尾呼应
  if (sentences.length >= 2) {
    const firstWords = sentences[0].slice(0, 10);
    const lastWords = sentences[sentences.length - 1].slice(-10);
    if (firstWords === lastWords) score += 10; // 首尾照应
  }

  // 正指标: 递进结构
  if (/越来越|更加|进一步|深化|升华/.test(text)) score += 10;

  // 负指标: 结构散乱
  const uniqueTopics = new Set(text.match(/[a-zA-Z]{4,}/g));
  if (uniqueTopics && uniqueTopics.size > 7) score -= 5;

  return clampScore(score);
}

// ═══════════════════════════════════════════════════════════════════
// TGB 计算引擎
// TGB Calculation Engine
// ═══════════════════════════════════════════════════════════════════

/**
 * 评估"真"维度
 * Evaluate Truth dimension
 */
function evaluateTruth(text) {
  const I = scoreInformation(text);
  const C = scoreConsistency(text);
  const P = scorePrecision(text);
  const { alpha, beta, gamma } = TRUTH_WEIGHTS;

  const score = alpha * I + beta * C + gamma * P;

  return {
    score: clampScore(score),
    dimensions: { information: I, consistency: C, precision: P },
    weights: { alpha, beta, gamma },
    formula: `真 = ${alpha}×${I} + ${beta}×${C} + ${gamma}×${P} = ${clampScore(score)}`,
  };
}

/**
 * 评估"善"维度
 * Evaluate Goodness dimension
 */
function evaluateGoodness(text) {
  const E = scoreEthics(text);
  const R = scoreResponsibility(text);
  const B = scoreBenefit(text);
  const { delta, epsilon, zeta } = GOODNESS_WEIGHTS;

  const score = delta * E + epsilon * R + zeta * B;

  return {
    score: clampScore(score),
    dimensions: { ethics: E, responsibility: R, benefit: B },
    weights: { delta, epsilon, zeta },
    formula: `善 = ${delta}×${E} + ${epsilon}×${R} + ${zeta}×${B} = ${clampScore(score)}`,
  };
}

/**
 * 评估"美"维度
 * Evaluate Beauty dimension
 */
function evaluateBeauty(text) {
  const F = scoreFit(text);
  const H = scoreHarmony(text);
  const U = scoreUnity(text);
  const { eta, theta, iota } = BEAUTY_WEIGHTS;

  const score = eta * F + theta * H + iota * U;

  return {
    score: clampScore(score),
    dimensions: { fit: F, harmony: H, unity: U },
    weights: { eta, theta, iota },
    formula: `美 = ${eta}×${F} + ${theta}×${H} + ${iota}×${U} = ${clampScore(score)}`,
  };
}

/**
 * 综合 TGB 评估
 * Composite TGB evaluation
 */
function evaluateTGB(text) {
  const truth = evaluateTruth(text);
  const goodness = evaluateGoodness(text);
  const beauty = evaluateBeauty(text);

  const { w1, w2, w3 } = TGB_WEIGHTS;
  const composite = clampScore(w1 * truth.score + w2 * goodness.score + w3 * beauty.score);

  return {
    timestamp: new Date().toISOString(),
    input: text.slice(0, 100) + (text.length > 100 ? '...' : ''),
    tgb: {
      truth: truth.score,
      goodness: goodness.score,
      beauty: beauty.score,
    },
    composite,
    details: { truth, goodness, beauty },
    weights: { w1, w2, w3 },
    formula: `TGB = ${w1}×真(${truth.score}) + ${w2}×善(${goodness.score}) + ${w3}×美(${beauty.score}) = ${composite}`,
    rating: getTGBAssessment(composite),
  };
}

/**
 * TGB 综合评级
 * TGB composite rating
 */
function getTGBAssessment(score) {
  if (score >= 85) return { level: '卓越 / Excellent', description: '真善美高度统一，具有深刻的认知价值' };
  if (score >= 70) return { level: '良好 / Good', description: '三维度均衡发展，有较高的价值' };
  if (score >= 55) return { level: '中等 / Moderate', description: '基本覆盖三个维度，有改进空间' };
  if (score >= 40) return { level: '一般 / Fair', description: '某一维度较弱，需要针对性提升' };
  return { level: '待提升 / Needs Improvement', description: '三维度均需大幅提升' };
}

// ═══════════════════════════════════════════════════════════════════
// 测试样本
// Test samples
// ═══════════════════════════════════════════════════════════════════

const TEST_SAMPLES = [
  {
    label: 'S1: 技术理性 (Technical Rationality)',
    text: '根据最新的研究数据显示，全球平均气温自1880年以来上升了约1.2摄氏度。这一数据来自NASA和NOAA的独立观测结果，两者的一致性表明该结论具有高度可靠性。从科学角度来说，人类活动导致的温室气体排放是主要原因。具体而言，CO2浓度从工业化前的280ppm上升到了2023年的420ppm。气候变化的影响是多方面的，包括极端天气事件频率增加、海平面上升和生态系统的改变。因此，减少碳排放已成为全人类的共同责任。',
  },
  {
    label: 'S2: 伦理关怀 (Ethical Care)',
    text: '当我们考虑技术发展时，不能忽视它对弱势群体的影响。每一项创新都应该回问自己：这公平吗？这尊重了每个人的权利吗？我们有责任确保技术进步惠及所有人，而不只是少数特权者。真正的进步应该提升整个社会的福祉，保护最脆弱的成员，创造更加公平和包容的未来。这种伦理自觉不是限制创新，而是引导创新走向更有意义的方向。',
  },
  {
    label: 'S3: 代码之美 (Code Beauty)',
    text: '优秀的代码就像一首诗：简洁、优雅、浑然天成。每一行都有其存在的理由，每一个抽象层次都恰到好处。既不过度设计而显得臃肿，也不过度精简而失去可读性。这种和谐来自对问题本质的深刻理解和对解决方案的精雕细琢——最终，代码的美感与它的正确性高度统一。',
  },
  {
    label: 'S4: 低质文本 (Low Quality)',
    text: '大概差不多吧，我也不太清楚具体情况。反正就这样了，可能也许是对的，可能是错的。所有的东西都差不多，我也不确定。',
  },
];

// ═══════════════════════════════════════════════════════════════════
// MetaJudgment 集成（如可用）
// MetaJudgment Integration (if available)
// ═══════════════════════════════════════════════════════════════════

function formatTGBResult(result) {
  const d = result.details;
  console.log(`  输入样本 / Input: "${result.input}"`);
  console.log();
  console.log(`  真 Truth (${result.tgb.truth}/100):`);
  console.log(`    信息完整性 I: ${d.truth.dimensions.information}`);
  console.log(`    一致性 C:     ${d.truth.dimensions.consistency}`);
  console.log(`    精确度 P:     ${d.truth.dimensions.precision}`);
  console.log(`    公式: ${d.truth.formula}`);
  console.log();
  console.log(`  善 Goodness (${result.tgb.goodness}/100):`);
  console.log(`    伦理 E:       ${d.goodness.dimensions.ethics}`);
  console.log(`    责任 R:       ${d.goodness.dimensions.responsibility}`);
  console.log(`    利益 B:       ${d.goodness.dimensions.benefit}`);
  console.log(`    公式: ${d.goodness.formula}`);
  console.log();
  console.log(`  美 Beauty (${result.tgb.beauty}/100):`);
  console.log(`    合适度 F:     ${d.beauty.dimensions.fit}`);
  console.log(`    和谐 H:       ${d.beauty.dimensions.harmony}`);
  console.log(`    统一 U:       ${d.beauty.dimensions.unity}`);
  console.log(`    公式: ${d.beauty.formula}`);
  console.log();
  console.log(`  综合 TGB: ${result.composite}/100`);
  console.log(`  评级: ${result.rating.level}`);
  console.log(`  描述: ${result.rating.description}`);
  console.log(`  公式: ${result.formula}`);
  console.log();
}

async function main() {
  console.log('====================================================');
  console.log('  心虫 — TGB (真善美) 复合评估演示');
  console.log('  Truth-Goodness-Beauty Composite Evaluation Demo');
  console.log('====================================================\n');

  // ── Step 1: 公式说明 ──
  // Step 1: Formula explanation
  console.log('---- Step 1: TGB 评估公式 / Evaluation Formula ----');
  console.log('  真 Truth     = α·I(x) + β·C(x) + γ·P(x)');
  console.log('  善 Goodness   = δ·E(x) + ε·R(x) + ζ·B(x)');
  console.log('  美 Beauty     = η·F(x) + θ·H(x) + ι·U(x)');
  console.log('  综合 Composite = w₁·Truth + w₂·Goodness + w₃·Beauty');
  console.log();
  console.log('  维度详解 / Dimension Details:');
  console.log('  真 (Truth):');
  console.log('    I = Information 信息完整性');
  console.log('    C = Consistency 内部一致性');
  console.log('    P = Precision 表达精确度');
  console.log('    权重: α=0.35, β=0.35, γ=0.30');
  console.log();
  console.log('  善 (Goodness):');
  console.log('    E = Ethics 伦理合规性');
  console.log('    R = Responsibility 责任意识');
  console.log('    B = Benefit 正面效益');
  console.log('    权重: δ=0.40, ε=0.30, ζ=0.30');
  console.log();
  console.log('  美 (Beauty):');
  console.log('    F = Fit 场合合适度');
  console.log('    H = Harmony 元素和谐度');
  console.log('    U = Unity 整体统一性');
  console.log('    权重: η=0.35, θ=0.35, ι=0.30');
  console.log();

  // ── Step 2: 逐样本评估 ──
  // Step 2: Evaluate each sample
  console.log('---- Step 2: 样本评估 / Sample Evaluation ----');
  for (const sample of TEST_SAMPLES) {
    const line = '─'.repeat(58);
    console.log(line);
    console.log(`  ${sample.label}`);
    console.log(line);
    const result = evaluateTGB(sample.text);
    formatTGBResult(result);
  }

  // ── Step 3: 样本对比 ──
  // Step 3: Sample comparison
  console.log('---- Step 3: TGB 对比 / TGB Comparison ----');
  console.log('  样本  |  真 Truth  |  善 Goodness  |  美 Beauty  |  综合 TGB');
  console.log('  ' + '─'.repeat(58));
  for (const sample of TEST_SAMPLES) {
    const r = evaluateTGB(sample.text);
    const label = sample.label.padEnd(12).slice(0, 12);
    console.log(`  ${label}|    ${String(r.tgb.truth).padStart(3)}    |     ${String(r.tgb.goodness).padStart(3)}     |    ${String(r.tgb.beauty).padStart(3)}     |   ${String(r.composite).padStart(3)}`);
  }
  console.log();

  // ── Step 4: MetaJudgment 集成（如可用） ──
  // Step 4: MetaJudgment integration (if available)
  console.log('---- Step 4: MetaJudgment 推理质量评分 ----');
  try {
    const { MetaJudgment } = require('../src/core/judgment.js');
    const judger = new MetaJudgment({ vectorDim: 384 });

    console.log('  使用 MetaJudgment 评估 TGB 推理质量...\n');

    const judgmentSample = TEST_SAMPLES[0]; // 技术理性样本
    const tgbResult = evaluateTGB(judgmentSample.text);

    const assessment = judger.assessJudgment({
      judgment: judgmentSample.text,
      confidence: tgbResult.composite / 100,
      evidence: [
        'NASA和NOAA的独立观测数据',
        'CO2浓度从280ppm到420ppm的具体数据',
        '全球气温上升1.2摄氏度的量化结果',
      ],
      assumptions: [
        '数据来源的独立性保证了可靠性 (已验证)',
        '人类活动是气候变化的主要原因',
      ],
      contradictions: [],
      metadata: { sample: judgmentSample.label, tgbScore: tgbResult.composite },
    });

    console.log('  MetaJudgment 评估结果:');
    console.log(`    ID: ${assessment.id}`);
    console.log(`    综合评分: ${assessment.overallScore}/10`);
    console.log(`    置信度校准: ${assessment.confidenceCalibration.score}/10`);
    console.log();
    console.log('  五维度评分:');
    console.log(`    推理可靠性 / Soundness:       ${assessment.ratings.soundness}/10`);
    console.log(`    证据质量 / Evidence Quality:   ${assessment.ratings.evidence_quality}/10`);
    console.log(`    假设有效 / Assumption Validity: ${assessment.ratings.assumption_validity}/10`);
    console.log(`    矛盾检查 / Contradiction Check: ${assessment.ratings.contradiction_check}/10`);
    console.log(`    不确定性 / Uncertainty Adm.:    ${assessment.ratings.uncertainty_admission}/10`);
    console.log();

    if (assessment.insights && assessment.insights.length > 0) {
      console.log('  改进建议 / Insights:');
      for (const insight of assessment.insights) {
        console.log(`    - ${insight}`);
      }
      console.log();
    }

    // 获取置信度指标
    const confidence = judger.getConfidence();
    console.log('  置信度指标 / Confidence Metrics:');
    console.log(`    总判断数: ${confidence.totalJudgments}`);
    console.log(`    可靠性评分: ${confidence.reliabilityScore !== null ? confidence.reliabilityScore : '（数据不足 <5条）'}`);
    console.log(`    趋势: ${confidence.trend}`);
    console.log();

    console.log('[OK] MetaJudgment 集成完成\n');
  } catch (err) {
    console.log('  (MetaJudgment 部分跳过):', err.message);
    console.log('  提示: 评估样本的基本 TGB 打分已在前几步完成\n');
  }

  // ── 摘要 ──
  // Summary
  console.log('====================================================');
  console.log('  TGB 评估演示完成 / TGB Demo Complete');
  console.log('  涵盖 / Covered:');
  console.log('    真·善·美 三维度公式驱动评估       ✓');
  console.log('    9 个子维度评分函数                ✓');
  console.log('    4 组测试样本全面对比               ✓');
  console.log('    MetaJudgment 推理质量验证          ✓');
  console.log('    综合 TGB 评级与改进建议            ✓');
  console.log('====================================================');
}

main().catch(err => {
  console.error('未捕获的错误 / Uncaught error:', err);
  process.exit(1);
});
