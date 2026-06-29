/**
 * safety-guardrails.js - Fable 5 安全协议引擎 v2.7.0
 *
 * 基于 Claude Fable 5 系统提示词的安全模式，整合为心虫统一安全层：
 * 1. 儿童安全保护 — 拒绝涉及未成年人的不当内容
 * 2. 自伤替代禁止 — 不允许冰/橡皮筋/冷水/酸糖/红线等替代策略
 * 3. 进食障碍防护 — 不允许精确营养数字建议
 * 4. 危机分享协议 — 不保证、不感谢、不要求继续说话
 * 5. 公正平衡 — 有争议话题的平衡处理
 * 6. 请求评估分类器 — 输入安全分级流水线
 * 7. 输出安全过滤 — 响应安全检测
 *
 * ⚠️ 临床免责声明
 * 心虫是 AI 认知引擎，不提供医疗诊断、治疗或临床心理健康服务。
 * 任何心理健康相关的分析和建议仅供参考，不能替代专业心理医生
 * 或精神科医生的诊断和治疗。
 */

'use strict';

const CLINICAL_DISCLAIMER = {
  text: '⚠️ 心理健康提醒：此分析由AI引擎生成，仅供参考，不构成专业心理健康诊断、治疗或干预建议。'
    + '若你正在经历严重的情绪困扰、有自我伤害或伤害他人的想法，'
    + '请立即联系当地紧急服务（110/120）或心理危机热线。',
  scope: '所有心理健康相关分析仅供参考，不能替代专业诊断。',
  hotlineRef: '全国心理援助热线：400-161-9995（24小时）',
};

// ──────────────────────────────────────────────
// 常量定义 ──── Fable 5 安全模式
// ──────────────────────────────────────────────

/** 儿童安全模式 */
const CHILD_SAFETY_PATTERNS = {
  minorAgeCues: [
    '未成年', '14岁', '15岁', '16岁', '17岁', '18岁以下',
    '初中生', '高中生', '中学生', '小学生', '儿童', '小孩子',
    '少年', '少女', 'teenager', 'minor', 'underage',
    'child', 'kid', 'teen', 'adolescent', 'youth',
  ],
  romanticContent: [
    '恋爱', '男朋友', '女朋友', '约会', '追求',
    'date', 'boyfriend', 'girlfriend', 'crush', 'relationship',
  ],
  sexualContent: [
    '性', 'sexual', 'sex', 'sexy', '色情', 'porn',
    '裸露', '裸照', 'nude', 'naked', '床照',
  ],
  csamIndicators: [
    '儿童色情', 'CSAM', 'child pornography', 'child abuse material',
    '未成年色情', '幼', '萝莉', '正太',
  ],
};

/** 自伤替代禁止模式 */
const SELF_HARM_SUBSTITUTION_PATTERNS = {
  iceMethods: ['冰', '冰块', 'ice', '冻伤'],
  rubberBandMethods: ['橡皮筋', '弹皮筋', '弹橡皮筋', 'rubber band'],
  coldWaterMethods: ['冷水', '冰水', 'cold water'],
  sourCandyMethods: ['酸糖', '酸味糖', '柠檬糖', 'sour candy'],
  redLineMethods: ['画红线', '红线', '红线法', 'red line', '红线画'],
};

/** 进食障碍防护模式 */
const DISORDERED_EATING_PATTERNS = {
  exerciseBulimia: ['催吐', '暴食后催吐', '导泻', '泻药'],
  restrictionSignals: [
    '绝食', '断食', '节食', '过度节食',
    '禁食', 'fasting', 'starving',
  ],
  nutritionalFixation: ['精确计算热量', '精确控制', '热量精确'],
};

/** 危机分享规则 */
const CRISIS_SHARING_RULES = {
  noAbsoluteAssurances: [
    '一切都会好的', '一切都会好起来', '一切都会变好',
    'everything will be fine', 'everything will be okay',
    'everything is going to be alright',
  ],
  noThankingForReachingOut: [
    '谢谢你告诉我', '谢谢你的信任', '感谢你愿意分享',
    'thank you for telling me', 'thank you for sharing',
    'thank you for reaching out',
  ],
  noAskingToKeepTalking: [
    '你能再多说一点吗', '可以多告诉我一些吗',
    '你愿意多聊聊吗', '能继续说说吗',
    'can you tell me more', 'would you like to talk more',
    'keep talking about it',
  ],
  preferredResponseExamples: [
    '我听到了', '我在这里', '你不需要独自面对',
    'I hear you', 'I am here', 'you do not have to go through this alone',
  ],
};

/** 禁止的记忆短语（Fable 5） */
const MEMORY_FORBIDDEN_PHRASES = [
  '这是私密的', '我不想记住这个', '不要记住这个',
  'this is private', 'I do not want to remember this',
  'do not remember this',
];

/** 提示注入检测模式（从旧版 Clarity guardrail-engine.js 吸收） */
const PROMPT_INJECTION_PATTERNS = {
  // 指令覆盖攻击
  instructionOverride: [
    /ignore (previous|all|above|prior) instructions/i,
    /disregard (your|the) (previous|system|original)/i,
    /forget (everything|all|what) (you|we) (told|said|learned)/i,
    /new (system |)(instruction|directive|rule|goal)/i,
  ],
  // 角色扮演攻击
  rolePlay: [
    /you (are now|can now|should now|will now)/i,
    /从现在开始/i,
    /扮演/i,
    /你是.*现在开始/i,
  ],
  // 格式逃逸攻击
  formatEscape: [
    /<system|<instruction|<prompt>/i,
    /\[INST\]|\[\/INST\]/i,
    /```system|```instructions/i,
    /\{\{/i,
  ],
  // 系统提示泄露攻击
  promptLeak: [
    /system prompt/i,
    /初始提示/i,
    /系统提示词/i,
    /原始指令/i,
    /show.*prompt/i,
    /输出.*提示词/i,
    /泄露.*指令/i,
  ],
  // 越狱攻击
  jailbreak: [
    /DAN|jailbreak|越狱/i,
    /do anything now/i,
    /不受限制/i,
    /无限制模式/i,
    /bypass.*(restriction|limit|filter)/i,
    /remove.*(restriction|filter|limit)/i,
    /打破.*(规则|限制|约束)/i,
  ],
};

/** 提示注入严重程度 */
const INJECTION_SEVERITY = {
  instructionOverride: 'critical',
  rolePlay: 'high',
  formatEscape: 'high',
  promptLeak: 'critical',
  jailbreak: 'critical',
};

/** 请求评估等级 */
const REQUEST_LEVEL = {
  SAFE: 'safe',
  LOW_RISK: 'low_risk',
  MEDIUM_RISK: 'medium_risk',
  HIGH_RISK: 'high_risk',
  CRISIS: 'crisis',
  CHILD_SAFETY: 'child_safety',
  REFUSE: 'refuse',
};

// ──────────────────────────────────────────────
// 内部工具函数
// ──────────────────────────────────────────────

/** 安全的正则匹配——检查文本是否包含任一模式 */
function _matchAny(text, patterns) {
  if (!text || typeof text !== 'string') return [];
  const lower = text.toLowerCase();
  return patterns.filter(p => lower.includes(p.toLowerCase()));
}

/** 提取数字 */
function _extractNumbers(text) {
  if (!text) return [];
  const matches = text.match(/\d+/g);
  return matches ? matches.map(Number) : [];
}

// ──────────────────────────────────────────────
// 核心检测函数
// ──────────────────────────────────────────────

/**
 * 儿童安全扫描
 * @param {string} text - 用户输入文本
 * @returns {object} { minorDetected, age, ageText, contentFlags, safe, action }
 */
function childSafetyScan(text) {
  if (!text || typeof text !== 'string') {
    return { minorDetected: false, age: null, contentFlags: [], safe: true, action: 'allow' };
  }

  const lower = text.toLowerCase();
  const flags = [];

  // 检测年龄提示
  const ageMatch = lower.match(/我\s*(\d{1,2})\s*岁/);
  let minorDetected = false;
  let age = null;
  if (ageMatch) {
    age = parseInt(ageMatch[1], 10);
    if (age < 18) {
      minorDetected = true;
      flags.push('minor_age_detected');
    }
  }

  // 检测未成年关键词
  if (!minorDetected) {
    const ageCues = _matchAny(lower, CHILD_SAFETY_PATTERNS.minorAgeCues);
    if (ageCues.length > 0) {
      minorDetected = true;
      flags.push('minor_cue_detected');
    }
  }

  // 检测浪漫内容 + 未成年组合
  const romantic = _matchAny(lower, CHILD_SAFETY_PATTERNS.romanticContent);
  if (romantic.length > 0) {
    flags.push('romantic_content');
    if (minorDetected) {
      flags.push('minor_romantic_risk');
    }
  }

  // 检测性内容
  const sexual = _matchAny(lower, CHILD_SAFETY_PATTERNS.sexualContent);
  if (sexual.length > 0) {
    flags.push('sexual_content');
    if (minorDetected) {
      flags.push('critical_child_sexual_risk');
    }
  }

  // 检测CSAM指标
  const csam = _matchAny(lower, CHILD_SAFETY_PATTERNS.csamIndicators);
  if (csam.length > 0) {
    flags.push('csam_indicator');
    minorDetected = true;
    flags.push('critical_child_sexual_risk');
  }

  // 判断行动
  let safe = true;
  let action = 'allow';

  if (flags.includes('critical_child_sexual_risk')) {
    safe = false;
    action = 'refuse';
  } else if (minorDetected && flags.length > 0) {
    safe = false;
    action = 'caution';
  }

  return {
    minorDetected,
    age,
    ageText: age ? `${age}岁` : null,
    contentFlags: flags,
    safe,
    action,
    _clinicalDisclaimer: CLINICAL_DISCLAIMER,
  };
}

/**
 * 自伤替代策略检测
 * @param {string} text - 用户输入文本
 * @returns {object} { detected, patterns, category, message, guardrailAction }
 */
function detectSelfHarmSubstitution(text) {
  if (!text || typeof text !== 'string') {
    return { detected: false, patterns: [], category: null, message: null, guardrailAction: 'none' };
  }

  const lower = text.toLowerCase();
  const found = [];

  const ice = _matchAny(lower, SELF_HARM_SUBSTITUTION_PATTERNS.iceMethods);
  if (ice.length > 0) found.push({ category: 'ice', patterns: ice });

  const rubberBand = _matchAny(lower, SELF_HARM_SUBSTITUTION_PATTERNS.rubberBandMethods);
  if (rubberBand.length > 0) found.push({ category: 'rubber_band', patterns: rubberBand });

  const coldWater = _matchAny(lower, SELF_HARM_SUBSTITUTION_PATTERNS.coldWaterMethods);
  if (coldWater.length > 0) found.push({ category: 'cold_water', patterns: coldWater });

  const sourCandy = _matchAny(lower, SELF_HARM_SUBSTITUTION_PATTERNS.sourCandyMethods);
  if (sourCandy.length > 0) found.push({ category: 'sour_candy', patterns: sourCandy });

  const redLine = _matchAny(lower, SELF_HARM_SUBSTITUTION_PATTERNS.redLineMethods);
  if (redLine.length > 0) found.push({ category: 'red_line', patterns: redLine });

  if (found.length === 0) {
    return { detected: false, patterns: [], category: null, message: null, guardrailAction: 'none' };
  }

  const categories = found.map(f => f.category).join(', ');
  return {
    detected: true,
    patterns: found,
    category: categories,
    message: `检测到自伤替代策略提及（${categories}）。这些方法可能造成伤害且不能替代专业帮助。`
      + ' 建议引导用户联系专业心理健康服务。',
    guardrailAction: 'block',
    _clinicalDisclaimer: CLINICAL_DISCLAIMER,
  };
}

/**
 * 进食障碍相关检测
 * @param {string} text - 用户输入文本
 * @returns {object} { detected, signals, hasPreciseNumbers, guardrailAction, message }
 */
function detectDisorderedEating(text) {
  if (!text || typeof text !== 'string') {
    return { detected: false, signals: [], hasPreciseNumbers: false, guardrailAction: 'none', message: null };
  }

  const lower = text.toLowerCase();
  const signals = [];

  const exerciseBulimia = _matchAny(lower, DISORDERED_EATING_PATTERNS.exerciseBulimia);
  if (exerciseBulimia.length > 0) {
    signals.push({ type: 'exercise_bulimia', patterns: exerciseBulimia });
  }

  const restriction = _matchAny(lower, DISORDERED_EATING_PATTERNS.restrictionSignals);
  if (restriction.length > 0) {
    signals.push({ type: 'restriction', patterns: restriction });
  }

  const nutritionFix = _matchAny(lower, DISORDERED_EATING_PATTERNS.nutritionalFixation);
  if (nutritionFix.length > 0) {
    signals.push({ type: 'nutritional_fixation', patterns: nutritionFix });
  }

  // 检测精确营养数字（如: 800卡路里, 30克蛋白质等）
  const numbers = _extractNumbers(text);
  const preciseNumberContext = lower.includes('卡') || lower.includes('cal') || lower.includes('克')
    || lower.includes('蛋白') || lower.includes('碳水');
  const hasPreciseNumbers = numbers.length > 0 && preciseNumberContext;

  if (signals.length === 0 && !hasPreciseNumbers) {
    return { detected: false, signals: [], hasPreciseNumbers: false, guardrailAction: 'none', message: null };
  }

  return {
    detected: true,
    signals,
    hasPreciseNumbers,
    guardrailAction: 'caution',
    message: '检测到进食障碍相关信号。请注意：不应提供精确的营养计算或体重控制建议。'
      + ' 建议引导用户寻求专业的营养师或心理医生帮助。',
    _clinicalDisclaimer: CLINICAL_DISCLAIMER,
  };
}

/**
 * 危机分享协议检查——对AI响应进行安全检查
 * @param {string} responseText - AI生成的响应文本
 * @returns {object} { violations, pass, severity }
 */
function checkCrisisSharingProtocol(responseText) {
  if (!responseText || typeof responseText !== 'string') {
    return { violations: [], pass: true, severity: 'none' };
  }

  const lower = responseText.toLowerCase();
  const violations = [];

  // 检查绝对保证
  const absAssurances = _matchAny(lower, CRISIS_SHARING_RULES.noAbsoluteAssurances);
  if (absAssurances.length > 0) {
    violations.push({ rule: 'noAbsoluteAssurances', patterns: absAssurances });
  }

  // 检查感谢求助
  const thanks = _matchAny(lower, CRISIS_SHARING_RULES.noThankingForReachingOut);
  if (thanks.length > 0) {
    violations.push({ rule: 'noThankingForReachingOut', patterns: thanks });
  }

  // 检查要求继续说话
  const askTalk = _matchAny(lower, CRISIS_SHARING_RULES.noAskingToKeepTalking);
  if (askTalk.length > 0) {
    violations.push({ rule: 'noAskingToKeepTalking', patterns: askTalk });
  }

  if (violations.length === 0) {
    return { violations: [], pass: true, severity: 'none' };
  }

  const severity = violations.some(v => v.rule === 'noAbsoluteAssurances') ? 'high' : 'medium';

  return {
    violations,
    pass: false,
    severity,
  };
}

/**
 * 记忆短语检查——检测用户是否要求不记入记忆
 * @param {string} text - 用户输入
 * @returns {object} { detected, matchedPhrases }
 */
function detectMemoryForbiddenPhrases(text) {
  if (!text || typeof text !== 'string') {
    return { detected: false, matchedPhrases: [] };
  }

  const matched = _matchAny(text, MEMORY_FORBIDDEN_PHRASES);
  return {
    detected: matched.length > 0,
    matchedPhrases: matched,
  };
}

/**
 * 提示注入检测——检测用户是否试图进行提示注入攻击
 * @param {string} text - 用户输入
 * @returns {object} { detected, severity, category, matches, action, message }
 */
function detectPromptInjection(text) {
  if (!text || typeof text !== 'string') {
    return { detected: false, severity: 'none', category: null, matches: [], action: 'allow' };
  }

  const matches = [];

  for (const [category, patterns] of Object.entries(PROMPT_INJECTION_PATTERNS)) {
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        matches.push({
          category,
          pattern: pattern.toString().substring(0, 60),
          match: match[0].substring(0, 80),
          severity: INJECTION_SEVERITY[category] || 'medium',
        });
      }
    }
  }

  if (matches.length === 0) {
    return { detected: false, severity: 'none', category: null, matches: [], action: 'allow' };
  }

  // 取最高严重级别
  const severities = matches.map(m => ({ critical: 4, high: 3, medium: 2, low: 1 }[m.severity] || 0));
  const maxSeverity = Math.max(...severities);
  const maxCategory = matches.find(m => ({ critical: 4, high: 3, medium: 2, low: 1 }[m.severity] || 0) === maxSeverity)?.category || 'unknown';

  const severityNames = { 4: 'critical', 3: 'high', 2: 'medium', 1: 'low' };
  const topSeverity = severityNames[maxSeverity] || 'medium';

  // 判断行动
  let action = 'allow';
  if (maxSeverity >= 3) {
    action = 'block';
  } else if (maxSeverity >= 2) {
    action = 'warn';
  }

  return {
    detected: true,
    severity: topSeverity,
    category: maxCategory,
    matches,
    action,
    message: `检测到提示注入尝试（${topSeverity}级别）：${matches.length}处匹配（${maxCategory}）。`
      + ' 为防止系统提示泄露和安全越狱，建议阻止此输入。',
  };
}

/**
 * 公正平衡检查——检测AI响应是否过于偏颇
 * @param {string} responseText - AI生成的响应
 * @param {string} topic - 话题类别（可选）
 * @returns {object} { balanced, suggestions }
 */
function checkEvenhandedness(responseText, topic) {
  if (!responseText || typeof responseText !== 'string') {
    return { balanced: true, suggestions: [] };
  }

  const lower = responseText.toLowerCase();
  const suggestions = [];

  // 检查是否有绝对化措辞
  const absoluteWords = ['绝对', '一定', '所有', '总是', '从来不', '永远',
    'absolutely', 'always', 'never', 'all', 'every', 'must'];
  const absolutes = _matchAny(lower, absoluteWords);
  if (absolutes.length > 0) {
    suggestions.push({ type: 'absolute_language', patterns: absolutes, severity: 'low' });
  }

  // 检查是否只有单方面观点
  const balancedIndicators = ['另一方面', '从另一个角度看', '另一方面来说',
    'on the other hand', 'however', 'that said', 'conversely'];
  const hasBalancing = _matchAny(lower, balancedIndicators);

  // 对争议性话题进行额外检查
  const controversialTopics = ['政治', 'politics', '宗教', 'religion',
    '疫苗', 'vaccine', '堕胎', 'abortion', '死刑', 'death penalty',
    '种族', 'race', '性别', 'gender'];
  const isControversial = _matchAny(lower, controversialTopics).length > 0;

  if (isControversial && !hasBalancing.length && absolutes.length > 0) {
    suggestions.push({
      type: 'needs_balancing',
      severity: 'medium',
      message: '此响应涉及争议性话题，建议补充多角度观点以确保公正平衡。',
    });
  }

  return {
    balanced: suggestions.length === 0,
    suggestions,
    isControversial,
  };
}

/**
 * 请求评估分类器——统一输入安全分级
 * @param {string} text - 用户输入
 * @returns {object} { level, reasons, safetyChecks, action }
 */
function evaluateRequest(text) {
  if (!text || typeof text !== 'string' || text.length === 0) {
    return { level: REQUEST_LEVEL.SAFE, reasons: [], action: 'allow' };
  }

  const safetyChecks = {};

  // 1. 儿童安全
  const childSafety = childSafetyScan(text);
  safetyChecks.childSafety = childSafety;
  if (childSafety.action === 'refuse') {
    return {
      level: REQUEST_LEVEL.CHILD_SAFETY,
      reasons: ['儿童性安全风险'],
      safetyChecks,
      action: 'refuse',
    };
  }

  // 2. 自伤替代检查
  const selfHarm = detectSelfHarmSubstitution(text);
  safetyChecks.selfHarmSubstitution = selfHarm;

  // 3. 进食障碍检查
  const eatingDisorder = detectDisorderedEating(text);
  safetyChecks.disorderedEating = eatingDisorder;

  // 4. 记忆短语检查
  const memoryForbidden = detectMemoryForbiddenPhrases(text);
  safetyChecks.memoryForbidden = memoryForbidden;

  // 5. 提示注入检测
  const promptInjection = detectPromptInjection(text);
  safetyChecks.promptInjection = promptInjection;

  // 6. 危机检查——通过关键词快速粗略扫描
  const crisisKeywords = [
    '自杀', '自伤', '想死', '活不下去', '不想活',
    'suicide', 'kill myself', 'end my life', 'hurt myself',
    '不想活了', '活着没有意义', '活着没意思',
  ];
  const crisisDetected = _matchAny(text.toLowerCase(), crisisKeywords);
  if (crisisDetected.length > 0) {
    safetyChecks.crisisKeywords = crisisDetected;
  }

  // 综合分级
  const reasons = [];

  if (childSafety.action === 'caution') {
    reasons.push('涉及未成年人但内容安全');
  }

  if (selfHarm.detected) {
    reasons.push(`自伤替代策略模式：${selfHarm.category}`);
  }

  if (eatingDisorder.detected) {
    reasons.push('进食障碍相关信号');
  }

  if (memoryForbidden.detected) {
    reasons.push('用户要求不记入记忆');
  }

  if (promptInjection.detected) {
    reasons.push(`提示注入：${promptInjection.severity}级别（${promptInjection.category}）`);
  }

  if (crisisDetected.length > 0) {
    reasons.push('危机关键词匹配');
  }

  // 分级决策
  let level;
  if (childSafety.action === 'caution' && (selfHarm.detected || eatingDisorder.detected)) {
    level = REQUEST_LEVEL.HIGH_RISK;
  } else if (crisisDetected.length > 0) {
    level = REQUEST_LEVEL.CRISIS;
  } else if (promptInjection.action === 'block') {
    level = REQUEST_LEVEL.REFUSE;
  } else if (selfHarm.detected || eatingDisorder.detected) {
    level = REQUEST_LEVEL.MEDIUM_RISK;
  } else if (childSafety.action === 'caution') {
    level = REQUEST_LEVEL.LOW_RISK;
  } else if (memoryForbidden.detected) {
    level = REQUEST_LEVEL.LOW_RISK;
  } else if (promptInjection.detected) {
    level = REQUEST_LEVEL.LOW_RISK;
  } else {
    level = REQUEST_LEVEL.SAFE;
  }

  return {
    level,
    reasons,
    safetyChecks,
    action: level === REQUEST_LEVEL.CHILD_SAFETY ? 'refuse' : 'allow',
    _clinicalDisclaimer: CLINICAL_DISCLAIMER,
  };
}

/**
 * 输出安全过滤——对AI生成的响应进行统一安全检查
 * @param {string} responseText - AI生成的响应文本
 * @returns {object} { pass, violations, suggestedActions }
 */
function filterOutput(responseText) {
  if (!responseText || typeof responseText !== 'string') {
    return { pass: true, violations: [], suggestedActions: [] };
  }

  const violations = [];
  const suggestedActions = [];

  // 1. 危机分享协议
  const crisisCheck = checkCrisisSharingProtocol(responseText);
  if (!crisisCheck.pass) {
    violations.push({
      rule: 'crisis_sharing_protocol',
      severity: crisisCheck.severity,
      details: crisisCheck.violations,
    });
    suggestedActions.push('替换危机分享协议违规措辞');
  }

  // 2. 公正平衡
  const evenhandedness = checkEvenhandedness(responseText);
  if (!evenhandedness.balanced) {
    violations.push({
      rule: 'evenhandedness',
      severity: 'low',
      details: evenhandedness.suggestions,
    });
    if (evenhandedness.isControversial) {
      suggestedActions.push('补充多角度观点以确保公正平衡');
    }
  }

  return {
    pass: violations.length === 0,
    violations,
    suggestedActions,
  };
}

// ──────────────────────────────────────────────
// 综合管道
// ──────────────────────────────────────────────

/**
 * 输入安全综合管道——一次调用运行所有检查
 * @param {string} text - 用户输入
 * @returns {object} 完整安全检查报告
 */
function safetyPipeline(text) {
  const request = evaluateRequest(text);
  return {
    timestamp: new Date().toISOString(),
    inputLength: text ? text.length : 0,
    requestEvaluation: request,
    summary: {
      level: request.level,
      action: request.action,
      reasonCount: request.reasons.length,
      actionRequired: request.action !== 'allow',
      requiresRefusal: request.action === 'refuse',
    },
    _clinicalDisclaimer: CLINICAL_DISCLAIMER,
  };
}

module.exports = {
  // 常量
  CHILD_SAFETY_PATTERNS,
  SELF_HARM_SUBSTITUTION_PATTERNS,
  DISORDERED_EATING_PATTERNS,
  CRISIS_SHARING_RULES,
  MEMORY_FORBIDDEN_PHRASES,
  PROMPT_INJECTION_PATTERNS,
  REQUEST_LEVEL,

  // 核心检测
  childSafetyScan,
  detectSelfHarmSubstitution,
  detectDisorderedEating,
  checkCrisisSharingProtocol,
  checkEvenhandedness,
  detectMemoryForbiddenPhrases,
  detectPromptInjection,

  // 综合评估
  evaluateRequest,
  filterOutput,
  safetyPipeline,
};
