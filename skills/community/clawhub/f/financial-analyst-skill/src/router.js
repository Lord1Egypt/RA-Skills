"use strict";

/**
 * Financial Analyst — 意图路由模块
 * 
 * 判断用户请求属于哪个金融分析子领域
 * 路由结果用于在模型层叠加对应领域模块的提示
 */

const SUB_DOMAINS = {
  MACRO: "macro_market",        // 宏观与市场方向
  SECTOR: "sector_industry",    // 行业/板块
  STOCK: "stock_equity",        // 个股/标的
  FUND: "fund_etf",             // 基金/ETF
  WEALTH: "wealth_product",     // 理财产品
  PORTFOLIO: "portfolio",       // 持仓/组合复盘
  STRATEGY: "strategy_trade",   // 交易策略
  RISK: "risk_leverage",        // 风险管理/杠杆
  GENERAL: "general",           // 通用投资问题
  NON_FINANCIAL: null           // 不命中
};

const SUB_DOMAIN_KEYWORDS = {
  macro_market: [
    "大盘", "指数", "市场方向", "牛市", "熊市", "震荡", "加息", "降息",
    "利率", "通胀", "GDP", "经济周期", "宏观", "资金流向", "流动性",
    "北向", "外资", "A股", "港股", "美股", "纳指", "标普", "道指",
    "宏观环境", "宏观经济", "市场情绪", "VIX"
  ],
  sector_industry: [
    "板块", "行业", "赛道", "AI", "新能源", "半导体", "消费", "医疗",
    "金融", "周期", "板块轮动", "行业比较", "产业", "渗透率",
    "成长赛道", "价值板块", "主线"
  ],
  stock_equity: [
    "股票", "个股", "公司", "估值", "PE", "PB", "PS", "ROE", "ROIC",
    "财报", "净利润", "收入", "毛利率", "自由现金流", "护城河",
    "买入", "卖出", "建仓", "止盈", "止损", "目标价", "基本面",
    "市盈率", "市净率", "市销率"
  ],
  portfolio: [
    "持仓", "组合", "复盘", "归因", "仓位", "配置", "重仓", "轻仓",
    "调仓", "再平衡", "资产配置", "分散", "集中", "风险暴露"
  ],
  strategy_trade: [
    "策略", "交易", "趋势", "反转", "动量", "套利", "对冲",
    "量化", "技术分析", "K线", "均线", "突破", "入场", "出场",
    "盈亏比", "胜率"
  ],
  risk_leverage: [
    "杠杆", "融资", "配资", "保证金", "强平", "爆仓", "回撤",
    "风险", "风控", "止损线", "仓位管理", "波动率", "风险管理",
    "最大回撤"
  ],
  fund_etf: [
    "基金", "ETF", "LOF", "指数基金", "主动基金", "被动基金",
    "公募", "私募", "基金经理", "夏普", "最大回撤", "跟踪误差",
    "申购", "赎回", "管理费", "托管费", "申赎", "定投",
    "净值", "单位净值", "累计净值", "基金排名", "基金评级",
    "债券基金", "货币基金", "混合基金", "股票基金", "指数增强",
    "FOF", "QDII"
  ],
  wealth_product: [
    "理财", "理财产品", "银行理财", "结构性存款", "信托",
    "资管", "券商资管", "保险理财", "R1", "R2", "R3", "R4", "R5",
    "业绩比较基准", "预期收益", "年化", "封闭期", "开放期",
    "保本", "非保本", "净值型", "底层资产", "非标",
    "大额存单", "国债", "逆回购", "货币理财"
  ]
};

/**
 * 主路由函数
 * @param {string} message - 用户输入
 * @returns {object} { matched, intent, confidence, reason, subDomain, domainKeywords }
 */
function route(message) {
  if (!message || typeof message !== "string") {
    return {
      matched: false,
      intent: null,
      confidence: 0,
      reason: "empty input"
    };
  }

  const normalized = message.toLowerCase();

  // 先判断是否属于金融投资问题
  const financeSignals = [
    "买", "卖", "涨", "跌", "股票", "基金", "理财", "投资", "市场", "板块",
    "持仓", "仓位", "杠杆", "估值", "财报", "分析", "趋势", "风险",
    "大盘", "指数", "行情", "配置", "收益", "回撤", "止损", "止盈",
    "PE", "PB", "ROE", "AI", "赛道", "周期"
  ];

  const hasFinanceSignal = financeSignals.some(s => normalized.includes(s));

  if (!hasFinanceSignal) {
    return {
      matched: false,
      intent: null,
      confidence: 0,
      reason: "no financial keyword signal detected"
    };
  }

  // 计算每个子领域的命中分数
  let bestMatch = { intent: SUB_DOMAINS.GENERAL, score: 0, hits: [] };

  for (const [intent, keywords] of Object.entries(SUB_DOMAIN_KEYWORDS)) {
    const hits = keywords.filter(k => normalized.includes(k));
    if (hits.length > bestMatch.score) {
      bestMatch = { intent, score: hits.length, hits };
    }
  }

  // 计算置信度
  const confidence = Math.min(bestMatch.score / 3, 1.0);

  return {
    matched: true,
    intent: bestMatch.intent,
    confidence,
    reason: bestMatch.hits.length > 0
      ? `命中 ${bestMatch.intent}：匹配关键词 "${bestMatch.hits.slice(0, 5).join("、")}"`
      : "命中金融分析领域但未匹配具体子领域",
    subDomain: bestMatch.intent,
    domainKeywords: bestMatch.hits
  };
}

module.exports = { route, SUB_DOMAINS, SUB_DOMAIN_KEYWORDS };
