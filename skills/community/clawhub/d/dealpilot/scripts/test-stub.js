// 本地自测脚本 - 验证骨架是否可跑通

import { normalizeRequest } from "./normalize.js";
import { decide } from "./decide.js";
import { formatReport } from "./analyze.js";

async function test() {
  console.log("=== DealPilot 骨架自测 ===\n");

  // 测试1: 需求解析
  const raw = { product: "蓝牙耳机", budget: { max: 200 }, urgency: "high" };
  const request = normalizeRequest(raw);
  console.log("输入规范化:", JSON.stringify(request, null, 2));

  // 测试2: 决策引擎
  console.log("\n--- 运行决策引擎 ---");
  const report = await decide(request);
  console.log("决策报告生成:", report ? "✓" : "✗");
  console.log("推荐平台:", report?.recommendedPlatform);
  console.log("结论:", report?.conclusion);

  // 测试3: 输出格式化
  console.log("\n--- 格式化输出 ---");
  const formatted = formatReport(report);
  console.log(formatted);

  console.log("\n=== 自测完成 ===");
}

test().catch(console.error);
