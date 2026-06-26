// 决策脚本
// 调用决策引擎生成 DecisionReport

/**
 * @param {any} request
 * @returns {Promise<DecisionReport>}
 */
export async function decide(request) {
  // STUB: 调用 mock 决策引擎
  const { runDecisionEngine } = await import("../engine/router.ts");
  return runDecisionEngine(request);
}
