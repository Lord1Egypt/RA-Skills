// 分析输出脚本
// 将 DecisionReport 整理为用户可读格式

/**
 * @param {any} report
 * @returns {string}
 */
export function formatReport(report) {
  let out = "";
  out += `## 推荐平台：${report.recommendedPlatform.toUpperCase()}\n`;
  if (report.recommendedPrice) out += `参考价格：¥${report.recommendedPrice}\n`;
  out += `\n### 决策理由\n`;
  report.reasons.forEach((r) => (out += `- ${r}\n`));
  if (report.risks.length > 0) {
    out += `\n### 风险提示\n`;
    report.risks.forEach((r) => {
      out += `- [${r.level.toUpperCase()}] ${r.description}`;
      if (r.mitigation) out += ` → ${r.mitigation}`;
      out += "\n";
    });
  }
  out += `\n### 时机建议：${report.timingAdvice.verdict === "buy_now" ? "立即购买" : report.timingAdvice.verdict === "wait" ? "建议等待" : "建议先比较"}\n`;
  out += `${report.timingAdvice.reason}\n`;
  if (report.alternatives.length > 0) {
    out += `\n### 替代方案\n`;
    report.alternatives.forEach((a) => {
      out += `- **${a.platform}**（${a.score}分）${a.price ? `¥${a.price}` : ""}：${a.keyReason}\n`;
    });
  }
  out += `\n---\n**结论**：${report.conclusion}`;
  return out;
}
