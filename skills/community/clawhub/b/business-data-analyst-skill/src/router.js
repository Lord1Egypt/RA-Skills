"use strict";

const INTENT_RULES = [
  {
    intent: "growth_analysis",
    label: "增长分析",
    keywords: [
      "增长",
      "新增",
      "活跃",
      "gmv",
      "营收增长",
      "增长放缓",
      "拉新",
      "用户增长",
      "销售增长",
    ],
  },
  {
    intent: "funnel_analysis",
    label: "漏斗分析",
    keywords: [
      "漏斗",
      "转化",
      "转化率",
      "注册",
      "激活",
      "下单",
      "支付",
      "成交",
      "线索转化",
    ],
  },
  {
    intent: "retention_analysis",
    label: "留存分析",
    keywords: [
      "留存",
      "复购",
      "续费",
      "流失",
      "cohort",
      "召回",
      "次留",
      "7日留存",
      "30日留存",
    ],
  },
  {
    intent: "revenue_analysis",
    label: "收入利润分析",
    keywords: [
      "收入",
      "利润",
      "毛利",
      "客单价",
      "arpu",
      "ltv",
      "价格",
      "折扣",
      "收入结构",
    ],
  },
  {
    intent: "efficiency_analysis",
    label: "运营效率分析",
    keywords: [
      "人效",
      "效率",
      "库存",
      "交付",
      "客服",
      "门店",
      "产能",
      "履约",
      "周转",
    ],
  },
  {
    intent: "business_diagnosis",
    label: "经营诊断",
    keywords: [
      "复盘",
      "诊断",
      "异常",
      "波动",
      "定位原因",
      "原因",
      "为什么下降",
      "为什么上涨",
      "经营分析",
    ],
  },
  {
    intent: "market_research",
    label: "市场调研",
    keywords: [
      "市场调研",
      "市场研究",
      "市场规模",
      "行业分析",
      "行业报告",
      "竞品分析",
      "竞争对手",
      "竞争格局",
      "市场机会",
      "市场趋势",
      "客户调研",
      "用户调研",
      "目标市场",
      "市场进入",
      "赛道分析",
      "tam",
      "sam",
      "som",
      "份额",
      "市场渗透",
      "出海调研",
      "市场准入",
    ],
  },
];

const BUSINESS_SIGNALS = [
  "gmv",
  "roi",
  "ltv",
  "arpu",
  "收入",
  "营收",
  "利润",
  "毛利",
  "留存",
  "复购",
  "续费",
  "流失",
  "转化",
  "漏斗",
  "客单价",
  "人效",
  "库存",
  "交付",
  "经营",
  "渠道",
  "用户增长",
  "销售",
  "新增",
  "活跃",
  "市场调研",
  "市场规模",
  "行业分析",
  "竞品分析",
  "竞争对手",
  "竞争格局",
  "市场机会",
  "tam",
  "sam",
  "som",
  "行业报告",
  "市场趋势",
  "赛道分析",
];

const DIAGNOSIS_SIGNALS = [
  "分析",
  "拆解",
  "定位",
  "归因",
  "复盘",
  "原因",
  "建议",
  "动作",
  "优化",
  "诊断",
];

const NEGATIVE_SIGNALS = [
  "写代码",
  "报错",
  "bug",
  "接口开发",
  "前端页面",
  "翻译",
  "润色",
  "写邮件",
  "写文章",
];

function normalizeText(input) {
  return String(input || "").trim().toLowerCase();
}

function countMatches(text, keywords) {
  return keywords.reduce((count, keyword) => {
    return count + (text.includes(keyword.toLowerCase()) ? 1 : 0);
  }, 0);
}

function detectBusinessAnalysis(message) {
  const text = normalizeText(message);
  if (!text) {
    return {
      matched: false,
      score: 0,
      reason: "消息为空，无法判断是否属于经营分析场景。",
    };
  }

  const negativeMatches = countMatches(text, NEGATIVE_SIGNALS);
  const businessMatches = countMatches(text, BUSINESS_SIGNALS);
  const diagnosisMatches = countMatches(text, DIAGNOSIS_SIGNALS);
  const score = businessMatches * 0.2 + diagnosisMatches * 0.15 - negativeMatches * 0.35;
  const matched = businessMatches > 0 && score >= 0.2;

  let reason = "未命中经营分析关键信号。";
  if (matched) {
    reason =
      "命中经营分析语义，包含业务指标或诊断动作相关关键词。";
  } else if (negativeMatches > 0) {
    reason = "存在偏技术或通用写作信号，当前不判定为经营分析请求。";
  }

  return { matched, score: clamp(score), reason };
}

function detectIntent(message) {
  const text = normalizeText(message);
  let bestRule = null;
  let bestScore = 0;

  for (const rule of INTENT_RULES) {
    const score = countMatches(text, rule.keywords);
    if (score > bestScore) {
      bestScore = score;
      bestRule = rule;
    }
  }

  if (!bestRule || bestScore === 0) {
    return {
      intent: null,
      confidence: 0,
      reason: "未识别到明确的分析子场景。",
    };
  }

  const confidence = clamp(0.35 + bestScore * 0.15);
  return {
    intent: bestRule.intent,
    confidence,
    reason: `命中${bestRule.label}，检测到相关问题模式和关键词。`,
  };
}

function routeSkillIntent(input) {
  const payload =
    typeof input === "string" ? { message: input } : Object(input || {});
  const message = normalizeText(payload.message);
  const businessResult = detectBusinessAnalysis(message);

  if (!businessResult.matched) {
    return {
      matched: false,
      intent: null,
      confidence: businessResult.score,
      reason: businessResult.reason,
      promptHint: null,
    };
  }

  const intentResult = detectIntent(message);
  const confidence = clamp(
    businessResult.score * 0.45 + intentResult.confidence * 0.55
  );

  return {
    matched: true,
    intent: intentResult.intent || "business_diagnosis",
    confidence,
    reason: intentResult.intent ? intentResult.reason : businessResult.reason,
    promptHint: buildPromptHint(intentResult.intent || "business_diagnosis"),
  };
}

function buildPromptHint(intent) {
  const hints = {
    growth_analysis: "优先拆新增、活跃、渠道结构和增长驱动。",
    funnel_analysis: "优先输出分层漏斗、环节流失和最大损失点。",
    retention_analysis: "优先做 cohort、续费和流失阶段拆解。",
    revenue_analysis: "优先拆量、价、折扣、结构和毛利影响。",
    efficiency_analysis: "优先看单位产出、单位成本、周期和资源利用率。",
    business_diagnosis: "优先界定问题、统一口径、拆原因并给动作建议。",
    market_research: "优先明确决策问题、设计调研策略、使用搜索工具收集外部信息、交叉验证并输出结构化调研结论。",
  };

  return hints[intent] || hints.business_diagnosis;
}

function clamp(value) {
  if (value < 0) {
    return 0;
  }

  if (value > 1) {
    return 1;
  }

  return Number(value.toFixed(2));
}

module.exports = {
  INTENT_RULES,
  detectBusinessAnalysis,
  detectIntent,
  routeSkillIntent,
};
