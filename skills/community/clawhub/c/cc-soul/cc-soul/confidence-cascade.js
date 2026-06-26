function initBeta(mem) {
  if (mem.bayesAlpha === void 0) mem.bayesAlpha = 2;
  if (mem.bayesBeta === void 0) mem.bayesBeta = 1;
}
function positiveEvidence(mem, difficulty = 0.5) {
  initBeta(mem);
  const delta = 0.3 + difficulty * 0.7;
  mem.bayesAlpha += delta;
  mem.confidence = betaMean(mem);
}
function negativeEvidence(mem, strength = 0.5) {
  initBeta(mem);
  const delta = 0.5 + strength * 1.5;
  mem.bayesBeta += delta;
  mem.confidence = betaMean(mem);
}
function timeDecay(mem, daysSinceRecall) {
  initBeta(mem);
  if (daysSinceRecall <= 1) return;
  const decay = Math.min(0.1, Math.log2(daysSinceRecall) * 0.02);
  mem.bayesBeta += decay;
  mem.confidence = betaMean(mem);
}
function betaMean(mem) {
  const alpha = mem.bayesAlpha ?? 2;
  const beta = mem.bayesBeta ?? 1;
  return alpha / (alpha + beta);
}
function betaVariance(mem) {
  const a = mem.bayesAlpha ?? 2;
  const b = mem.bayesBeta ?? 1;
  return a * b / ((a + b) ** 2 * (a + b + 1));
}
function needsVerification(mem) {
  const v = betaVariance(mem);
  const c = betaMean(mem);
  return v > 0.03 && c > 0.3 && c < 0.8;
}
function batchTimeDecay(memories) {
  const now = Date.now();
  let updated = 0;
  for (const mem of memories) {
    const lastRecall = mem.lastRecalled || mem.lastAccessed || mem.ts || now;
    const daysSince = (now - lastRecall) / 864e5;
    if (daysSince > 1) {
      timeDecay(mem, daysSince);
      updated++;
    }
  }
  return updated;
}
function confidenceTier(mem) {
  const c = betaMean(mem);
  const v = betaVariance(mem);
  if (c >= 0.85 && v < 0.02) return "verified";
  if (c >= 0.6) return "probable";
  if (c >= 0.4) return "uncertain";
  return "dubious";
}
function confidenceRecallModifier(mem) {
  const c = betaMean(mem);
  const v = betaVariance(mem);
  let modifier = 0.5 + c * 0.5;
  if (v > 0.03 && c > 0.3) {
    modifier += 0.1;
  }
  return Math.max(0.3, Math.min(1.3, modifier));
}
export {
  batchTimeDecay,
  betaMean,
  betaVariance,
  confidenceRecallModifier,
  confidenceTier,
  initBeta,
  needsVerification,
  negativeEvidence,
  positiveEvidence,
  timeDecay
};
