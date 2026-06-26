import { BudgetManager, CostCalculator, UsageTracker } from "../src/index.js";

async function main() {
  const tracker = new UsageTracker({
    dbPath: ":memory:",
    costCalculator: new CostCalculator({
      "gpt-4.1-mini": {
        inputCostPerMillion: 0.4,
        outputCostPerMillion: 1.6
      },
      "gpt-4.1": {
        inputCostPerMillion: 2,
        outputCostPerMillion: 8
      }
    })
  });

  await tracker.recordUsage({
    sessionId: "demo-session",
    model: "gpt-4.1-mini",
    promptTokens: 3000,
    completionTokens: 900,
    metadata: { tool: "summarize" }
  });

  await tracker.recordUsage({
    sessionId: "demo-session",
    model: "gpt-4.1",
    promptTokens: 1200,
    completionTokens: 600,
    metadata: { tool: "analyze" }
  });

  const summary = await tracker.getUsageSummary({ sessionId: "demo-session" });
  const budgetManager = new BudgetManager(tracker);
  await budgetManager.setBudget({
    name: "demo-budget",
    limitUsd: 0.05,
    warningThreshold: 0.6,
    sessionId: "demo-session"
  });
  const budget = await budgetManager.evaluateBudget("demo-budget");

  console.log("Usage summary:", JSON.stringify(summary, null, 2));
  console.log("Budget status:", JSON.stringify(budget, null, 2));

  tracker.close();
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
