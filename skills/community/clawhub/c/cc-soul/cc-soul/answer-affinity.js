import { trigrams, trigramSimilarity, tokenize } from "./memory-utils.ts";
function scoreAffinity(injectedMemories, response, query) {
  if (!response || injectedMemories.length === 0) return [];
  const responseLower = response.toLowerCase();
  const results = [];
  for (const mem of injectedMemories) {
    const content = (mem.content || "").toLowerCase();
    if (!content) continue;
    const triSim = trigramSimilarity(trigrams(content), trigrams(responseLower));
    const memWords = new Set(tokenize(content).filter((w) => w.length >= 2));
    const respWords = new Set(tokenize(responseLower).filter((w) => w.length >= 2));
    let keywordOverlap = 0;
    for (const w of memWords) {
      if (respWords.has(w)) keywordOverlap++;
    }
    const kwScore = memWords.size > 0 ? keywordOverlap / memWords.size : 0;
    const entities = content.match(/[A-Z][a-zA-Z]+|[\u4e00-\u9fff]{2,4}/g) || [];
    let entityHits = 0;
    for (const e of entities) {
      if (responseLower.includes(e.toLowerCase())) entityHits++;
    }
    const entityScore = entities.length > 0 ? entityHits / entities.length : 0;
    const affinity = triSim * 0.3 + kwScore * 0.4 + entityScore * 0.3;
    let signal = "unused";
    if (affinity > 0.15) signal = "used";
    else if (affinity > 0.05) signal = "partial";
    results.push({ memory: mem, affinity, signal });
  }
  return results;
}
function applyAffinityFeedback(results) {
  for (const r of results) {
    if (r.signal === "used") {
      r.memory.injectionEngagement = (r.memory.injectionEngagement || 0) + 1;
    } else if (r.signal === "unused") {
      r.memory.injectionMiss = (r.memory.injectionMiss || 0) + 1;
    }
  }
}
function scoreEngagement(userReply, previousResponse) {
  if (!userReply) return 0;
  let engagement = 0.5;
  const lenRatio = userReply.length / Math.max(1, previousResponse.length);
  if (lenRatio > 0.5) engagement += 0.15;
  if (lenRatio > 1) engagement += 0.1;
  if (/[？?]/.test(userReply)) engagement += 0.1;
  if (/谢|感谢|棒|好的|对|没错|exactly|thanks|great|yes|right|correct/i.test(userReply)) engagement += 0.15;
  if (/不对|错了|不是|wrong|no|incorrect/i.test(userReply)) engagement -= 0.2;
  if (userReply.length < 5 && /嗯|哦|ok|mm|hm/i.test(userReply)) engagement -= 0.15;
  return Math.max(0, Math.min(1, engagement));
}
function getInjectionEffectiveness(memories) {
  let totalInjections = 0, engagedCount = 0, missCount = 0;
  for (const mem of memories) {
    const eng = mem.injectionEngagement || 0;
    const miss = mem.injectionMiss || 0;
    if (eng + miss > 0) {
      totalInjections += eng + miss;
      engagedCount += eng;
      missCount += miss;
    }
  }
  return {
    totalInjections,
    engagedCount,
    missCount,
    effectivenessRate: totalInjections > 0 ? engagedCount / totalInjections : 0
  };
}
export {
  applyAffinityFeedback,
  getInjectionEffectiveness,
  scoreAffinity,
  scoreEngagement
};
