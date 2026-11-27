/**
 * 答案守卫代码模板
 * 在代码节点中评估主答案是否满足质量要求，不满足则生成兜底文本。
 * 输入：answer（主答案文本）、supportContact（可选人工支持渠道）
 * 输出：finalText（最终回复）、retry（是否触发兜底）
 */
const DEFAULT_SUPPORT_CONTACT = "人工支持渠道";

function isLowQuality(answer) {
  if (typeof answer !== "string" || !answer) {
    return true;
  }
  const trimmed = answer.trim();
  if (trimmed.length < 10) {
    return true;
  }
  if (/^(暂无|未找到|不知道|无法|出错|Error|NaN|null|undefined)/i.test(trimmed)) {
    return true;
  }
  if (/\{\{[^}]+\}\}/.test(trimmed)) {
    return true;
  }
  return false;
}

function buildFallback(answer, supportContact) {
  const safeAnswer = typeof answer === "string" && answer.trim() ? answer.trim() : "（无有效回复）";
  const contact = typeof supportContact === "string" && supportContact.trim()
    ? supportContact.trim()
    : DEFAULT_SUPPORT_CONTACT;
  return `抱歉，当前回复可能不够准确：${safeAnswer}\n建议：1）补充更多细节后重新提问；2）通过${contact}获取人工帮助。`;
}

async function main({ params }) {
  const answer = params.answer || "";
  if (isLowQuality(answer)) {
    return { finalText: buildFallback(answer, params.supportContact), retry: true };
  }
  return { finalText: answer, retry: false };
}
