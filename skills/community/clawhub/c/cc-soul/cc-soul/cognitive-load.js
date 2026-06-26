function getInjectionStrategy(msg, recentMessages, emotionIntensity) {
  let load = 0;
  const reasons = [];
  const lenFactor = Math.min(1, msg.length / 500) * 0.2;
  load += lenFactor;
  if (msg.length > 300) reasons.push("long message");
  const questions = (msg.match(/[？?]/g) || []).length;
  const subQuestions = (msg.match(/还有|另外|以及|还|and also|additionally|besides/gi) || []).length;
  const qFactor = Math.min(1, (questions + subQuestions) / 3) * 0.2;
  load += qFactor;
  if (questions > 1) reasons.push(`${questions} questions`);
  const hasCode = /```|`[^`]+`|function\s|const\s|let\s|var\s|import\s|class\s|def\s|if\s*\(/.test(msg);
  if (hasCode) {
    load += 0.25;
    reasons.push("code detected");
  }
  const topicWords = new Set(
    (msg.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{4,}/gi) || []).map((w) => w.toLowerCase())
  );
  const topicFactor = Math.min(1, topicWords.size / 15) * 0.15;
  load += topicFactor;
  if (topicWords.size > 10) reasons.push(`${topicWords.size} topics`);
  if (emotionIntensity && emotionIntensity > 0.5) {
    load += emotionIntensity * 0.1;
    reasons.push("emotional");
  }
  if (recentMessages && recentMessages.length >= 3) {
    const avgLen = recentMessages.reduce((s, m) => s + m.length, 0) / recentMessages.length;
    if (avgLen > 200) {
      load += 0.1;
      reasons.push("sustained complexity");
    }
  }
  load = Math.max(0, Math.min(1, load));
  let topN, tokenBudget, loadLevel;
  if (load < 0.2) {
    topN = 5;
    tokenBudget = 2e3;
    loadLevel = "low";
  } else if (load < 0.45) {
    topN = 3;
    tokenBudget = 1500;
    loadLevel = "medium";
  } else if (load < 0.7) {
    topN = 2;
    tokenBudget = 800;
    loadLevel = "high";
  } else {
    topN = 1;
    tokenBudget = 400;
    loadLevel = "extreme";
  }
  return {
    topN,
    tokenBudget,
    cognitiveLoad: Math.round(load * 100) / 100,
    loadLevel,
    reason: reasons.join(", ") || "normal conversation"
  };
}
function shouldInjectMemories(msg) {
  if (msg.length < 5 && /^(ok|好|嗯|哦|行|是|对|恩|mm|hm|yeah|yep|sure|got it)/i.test(msg)) return false;
  if (msg.startsWith("```") && msg.endsWith("```") && msg.split("\n").length > 10) return false;
  if (/^[!/]/.test(msg.trim())) return false;
  return true;
}
function trimToTokenBudget(memories, tokenBudget) {
  const estimateTokens = (text) => {
    const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const words = (text.match(/[a-zA-Z]+/g) || []).length;
    return cjk * 1.5 + words * 1.3 + 10;
  };
  const result = [];
  let usedTokens = 0;
  for (const mem of memories) {
    const tokens = estimateTokens(mem.content || "");
    if (usedTokens + tokens > tokenBudget) break;
    result.push(mem);
    usedTokens += tokens;
  }
  return result;
}
export {
  getInjectionStrategy,
  shouldInjectMemories,
  trimToTokenBudget
};
