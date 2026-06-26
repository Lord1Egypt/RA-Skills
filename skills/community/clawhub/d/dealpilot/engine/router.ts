// DealPilot 决策引擎 - 路由层
// 负责接收 ShoppingRequest，分发到各平台适配器，汇总结果

import type { ShoppingRequest, DecisionReport, Platform } from "./types";

// STUB: 各平台适配器注册表
// 下一阶段替换为真实适配器
const platformAdapters: Record<Platform, any> = {
  taobao: { platform: "taobao", stub: true },
  pdd: { platform: "pdd", stub: true },
  jd: { platform: "jd", stub: true },
  yhd: { platform: "yhd", stub: true },
  vip: { platform: "vip", stub: true },
};

export async function runDecisionEngine(
  request: ShoppingRequest
): Promise<DecisionReport> {
  const platforms: Platform[] = request.platforms || ["taobao", "pdd", "jd", "yhd", "vip"];

  // STUB: 返回模拟决策报告
  // 下一阶段替换为真实的多平台查询和评分逻辑
  return buildMockReport(request, platforms);
}

function buildMockReport(request: ShoppingRequest, platforms: Platform[]): DecisionReport {
  const product = request.product || "未知商品";

  return {
    recommendedPlatform: "pdd",
    recommendedPrice: 89,
    reasons: [
      "拼多多百亿补贴后价格最低",
      "该品类在拼多多有官方补贴标识",
      "退货包运费降低试错成本",
    ],
    risks: [
      {
        level: "medium",
        description: "拼多多第三方卖家品质参差不齐",
        mitigation: "选择有「退货包运费」和「假一赔十」标识的卖家",
      },
    ],
    alternatives: [
      { platform: "jd", score: 82, price: 109, keyReason: "京东物流最快，自营品质有保障" },
      { platform: "taobao", score: 75, price: 95, keyReason: "淘宝价格适中，售后比拼多多稳定" },
      { platform: "yhd", score: 70, price: 92, keyReason: "一号店日常用品价格稳定" },
      { platform: "vip", score: 65, price: 88, keyReason: "唯品会品牌特卖可能有低价" },
    ],
    timingAdvice: {
      verdict: "buy_now",
      reason: "该商品当前价格已接近历史低价，暂无大型促销节点临近",
    },
    comparison: platforms.map((p) => ({
      platform: p,
      price: p === "pdd" ? 89 : p === "jd" ? 109 : p === "taobao" ? 95 : p === "yhd" ? 92 : 88,
      quality: p === "jd" ? "high" : p === "taobao" ? "medium" : "medium",
      shipping: p === "jd" ? "fast" : p === "yhd" ? "fast" : p === "pdd" ? "slow" : "medium",
      afterSales: p === "jd" ? "strong" : p === "taobao" ? "medium" : "weak",
      authenticity: p === "jd" ? "safe" : p === "pdd" ? "risky" : "medium",
      score: p === "pdd" ? 85 : p === "jd" ? 82 : p === "taobao" ? 75 : 70,
    })),
    conclusion: `针对"${product}"，综合价格、品质、售后风险，推荐在**拼多多百亿补贴**购买，到手价约89元。若更看重品质和售后保障，建议选**京东自营**，到手价约109元。`,
  };
}
