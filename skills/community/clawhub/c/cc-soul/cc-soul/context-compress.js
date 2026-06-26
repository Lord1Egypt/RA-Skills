const FIVE_MINUTES_MS = 5 * 60 * 1e3;
const ONE_HOUR_MS = 60 * 60 * 1e3;
function classifyTier(ts, now) {
  if (ts == null) return "verbatim";
  const age = now - ts;
  if (age < FIVE_MINUTES_MS) return "verbatim";
  if (age < ONE_HOUR_MS) return "summary";
  return "compressed_fact";
}
function compressByDensity(text, targetRatio = 0.4, userId) {
  const sentences = text.split(/(?<=[。！？!?\.\n])\s*/).filter((s) => s.trim().length > 3);
  if (sentences.length <= 2) return text;
  let userDomainKeywords = /* @__PURE__ */ new Set();
  if (userId) {
    try {
      const pm = require("./person-model.ts");
      const profile = pm.getPersonModel(userId);
      if (profile?.topDomains) {
        for (const d of profile.topDomains) {
          const words = d.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [];
          for (const w of words) userDomainKeywords.add(w.toLowerCase());
        }
      }
    } catch {
    }
  }
  const scored = sentences.map((sent, idx) => {
    const words = (sent.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const unique = new Set(words);
    const uniqueRatio = words.length > 0 ? unique.size / words.length : 0;
    const entityCount = (sent.match(/\d+|`[^`]+`|[A-Z][a-z]+[A-Z]|[A-Z]{2,}/g) || []).length;
    const entityDensity = 1 + Math.min(entityCount * 0.2, 0.8);
    const posWeight = idx === 0 || idx === sentences.length - 1 ? 1.2 : 1;
    const lengthFactor = sent.length < 10 ? 0.5 : 1;
    let personalBoost = 1;
    if (userDomainKeywords.size > 0) {
      const domainHits = words.filter((w) => userDomainKeywords.has(w)).length;
      if (domainHits > 0) personalBoost = 1.5;
    }
    const density = uniqueRatio * entityDensity * posWeight * lengthFactor * personalBoost;
    return { sent, density, idx };
  });
  const targetLen = Math.ceil(text.length * targetRatio);
  scored.sort((a, b) => b.density - a.density);
  const selected = [];
  let currentLen = 0;
  for (const s of scored) {
    if (currentLen >= targetLen) break;
    selected.push(s);
    currentLen += s.sent.length;
  }
  selected.sort((a, b) => a.idx - b.idx);
  return selected.map((s) => s.sent).join(" ");
}
function summarize(text) {
  const trimmed = text.trim();
  if (!trimmed) return trimmed;
  const sentences = trimmed.split(/(?<=[。！？!?\.\n])\s*/).filter((s) => s.trim());
  if (sentences.length <= 2) return trimmed;
  const densityResult = compressByDensity(trimmed, 0.4);
  if (densityResult.length >= trimmed.length * 0.2 && densityResult.length <= trimmed.length * 0.6) {
    return densityResult;
  }
  const first = sentences[0].trim();
  const last = sentences[sentences.length - 1].trim();
  const result = `${first} ... ${last}`;
  const targetLen = Math.ceil(trimmed.length * 0.5);
  if (result.length >= targetLen) return result;
  let built = first;
  for (let i = 1; i < sentences.length - 1; i++) {
    const candidate = `${built} ${sentences[i].trim()} ... ${last}`;
    if (candidate.length >= targetLen) {
      return candidate;
    }
    built = `${built} ${sentences[i].trim()}`;
  }
  return `${built} ... ${last}`;
}
function compressFact(text) {
  const trimmed = text.trim();
  if (!trimmed) return trimmed;
  const tokens = [];
  const patterns = [
    /\d[\d.,]*[%kmgtbKMGTB]?(?:\s*(?:秒|分|小时|天|条|个|次|行|MB|GB|ms|s|min|px|em|rem))?/g,
    /[A-Z][a-zA-Z]+(?:\.[a-zA-Z]+)*/g,
    // PascalCase / dotted paths
    /[a-z][a-zA-Z]*(?:_[a-zA-Z]+)+/g,
    // snake_case
    /`[^`]+`/g,
    // inline code
    /"[^"]{1,30}"/g,
    // short quoted strings
    /[\u4e00-\u9fff]{2,}/g
    // CJK word sequences (2+ chars)
  ];
  const seen = /* @__PURE__ */ new Set();
  for (const pat of patterns) {
    let m;
    pat.lastIndex = 0;
    while ((m = pat.exec(trimmed)) !== null) {
      const tok = m[0].trim();
      if (tok && !seen.has(tok)) {
        seen.add(tok);
        tokens.push(tok);
      }
    }
  }
  if (tokens.length === 0) {
    return trimmed.slice(0, Math.max(1, Math.ceil(trimmed.length * 0.2)));
  }
  tokens.sort((a, b) => trimmed.indexOf(a) - trimmed.indexOf(b));
  const targetLen = Math.max(1, Math.ceil(trimmed.length * 0.2));
  let result = "";
  for (const tok of tokens) {
    const next = result ? `${result} ${tok}` : tok;
    if (next.length > targetLen * 1.5) break;
    result = next;
  }
  return result || tokens[0];
}
function compressAugments(augments) {
  const now = Date.now();
  return augments.map((aug) => {
    const tier = classifyTier(aug.ts, now);
    switch (tier) {
      case "verbatim":
        return { content: aug.content, priority: aug.priority, tokens: aug.tokens };
      case "summary": {
        const compressed = summarize(aug.content);
        const ratio = aug.content.length > 0 ? compressed.length / aug.content.length : 1;
        return {
          content: compressed,
          priority: aug.priority,
          tokens: Math.ceil(aug.tokens * ratio)
        };
      }
      case "compressed_fact": {
        const compressed = compressFact(aug.content);
        const ratio = aug.content.length > 0 ? compressed.length / aug.content.length : 1;
        return {
          content: compressed,
          priority: aug.priority,
          tokens: Math.ceil(aug.tokens * ratio)
        };
      }
    }
  });
}
function estimateTokenSavings(original, compressed) {
  const saved = original - compressed;
  const ratio = original > 0 ? saved / original : 0;
  return { saved, ratio: Math.round(ratio * 1e3) / 1e3 };
}
const contextCompressModule = {
  id: "context-compress",
  name: "\u6E10\u8FDB\u5F0F\u4E0A\u4E0B\u6587\u538B\u7F29",
  priority: 30,
  // runs early so other modules see compressed augments
  onPreprocessed(event) {
    if (!event?.augments || !Array.isArray(event.augments)) return;
    const timedAugments = event.augments.filter(
      (a) => a && typeof a.content === "string" && typeof a.ts === "number"
    ).map((a) => ({
      ...a,
      priority: typeof a.priority === "number" ? a.priority : 5,
      tokens: typeof a.tokens === "number" ? a.tokens : Math.ceil(a.content.length * 0.75)
    }));
    if (timedAugments.length === 0) return;
    const compressed = compressAugments(timedAugments);
    const totalOriginal = timedAugments.reduce((s, a) => s + a.tokens, 0);
    const totalCompressed = compressed.reduce((s, a) => s + a.tokens, 0);
    if (totalCompressed < totalOriginal) {
      const { saved, ratio } = estimateTokenSavings(totalOriginal, totalCompressed);
      return [{
        content: `[context-compress] \u538B\u7F29\u4E86 ${timedAugments.length} \u6761\u589E\u5F3A\uFF0C\u8282\u7701 ${saved} tokens (${(ratio * 100).toFixed(1)}%)`,
        priority: 1,
        tokens: 20
      }];
    }
  }
};
export {
  classifyTier,
  compressAugments,
  compressByDensity,
  compressFact,
  contextCompressModule,
  estimateTokenSavings,
  summarize
};
