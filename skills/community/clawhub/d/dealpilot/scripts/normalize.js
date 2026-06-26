// 需求解析脚本
// 将用户的自然语言输入规范化为 ShoppingRequest

/**
 * @param {any} raw
 * @returns {ShoppingRequest}
 */
export function normalizeRequest(raw) {
  // STUB: 简单解析，下一阶段接入 LLM 做意图识别
  return {
    product: raw.product || raw.q || raw.query || raw.item,
    budget: raw.budget || raw.priceRange,
    priorities: raw.priorities || ["价格", "品质"],
    quantity: raw.quantity || 1,
    scenario: raw.scenario || "personal",
    urgency: raw.urgency || "medium",
    platforms: raw.platforms,
    mustHave: raw.mustHave,
    mustAvoid: raw.mustAvoid,
  };
}
