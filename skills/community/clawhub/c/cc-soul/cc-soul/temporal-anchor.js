function extractAnchors(memories) {
  const anchors = [];
  for (const mem of memories) {
    if (!mem.content || !mem.ts) continue;
    const ei = mem.emotionIntensity || 0;
    if (ei >= 0.7) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.9,
        source: "flashbulb"
      });
      continue;
    }
    if ((mem.importance || 0) >= 8) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.75,
        source: "explicit"
      });
      continue;
    }
    const timeMatch = mem.content.match(
      /(\d{4})年|(\d{1,2})月(\d{1,2})[日号]|去年|今年|上个月|上周|前天|昨天|当时|那时候|那年|january|february|march|april|may|june|july|august|september|october|november|december|\d{1,2}\s+\w+\s+\d{4}|last\s+(week|month|year|time|night|summer|winter|spring|fall)|a\s+(few|couple)\s+(days|weeks|months|years)\s+ago|back\s+(in|when)|recently|the\s+other\s+day|earlier\s+this|years?\s+ago|months?\s+ago|weeks?\s+ago/i
    );
    if (timeMatch) {
      anchors.push({
        description: mem.content.slice(0, 50),
        timestamp: mem.ts,
        confidence: 0.7,
        source: "explicit"
      });
    }
  }
  anchors.sort((a, b) => a.timestamp - b.timestamp);
  return anchors;
}
function inferTimeRange(query, anchors, recentContext) {
  if (anchors.length === 0) return null;
  const now = Date.now();
  if (/那之后|后来|然后|接着|after that|since then|afterwards/.test(query)) {
    const recent = findReferencedAnchor(query, anchors, recentContext);
    if (recent) return { from: recent.timestamp, to: now };
  }
  if (/那之前|以前|曾经|before that|prior to|previously/.test(query)) {
    const recent = findReferencedAnchor(query, anchors, recentContext);
    if (recent) return { from: 0, to: recent.timestamp };
  }
  if (/同一时期|那段时间|那时候|那会儿|around that time|back then/.test(query)) {
    const recent = findReferencedAnchor(query, anchors, recentContext);
    if (recent) {
      const window = 30 * 864e5;
      return { from: recent.timestamp - window, to: recent.timestamp + window };
    }
  }
  return null;
}
function findReferencedAnchor(query, anchors, recentContext) {
  const searchText = (query + " " + (recentContext || "")).toLowerCase();
  let bestAnchor = null;
  let bestOverlap = 0;
  for (const anchor of anchors) {
    const anchorWords = anchor.description.toLowerCase().match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/g) || [];
    let overlap = 0;
    for (const w of anchorWords) {
      if (searchText.includes(w)) overlap++;
    }
    if (overlap > bestOverlap) {
      bestOverlap = overlap;
      bestAnchor = anchor;
    }
  }
  if (!bestAnchor) {
    bestAnchor = anchors.filter((a) => a.source === "flashbulb").pop() || null;
  }
  return bestAnchor;
}
function inferFactTimeline(facts) {
  const timeline = /* @__PURE__ */ new Map();
  const groups = /* @__PURE__ */ new Map();
  for (const fact of facts) {
    const key = `${fact.subject}:${fact.predicate}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(fact);
  }
  for (const [key, factsGroup] of groups) {
    factsGroup.sort((a, b) => (a.ts || 0) - (b.ts || 0));
    for (let i = 0; i < factsGroup.length; i++) {
      const fact = factsGroup[i];
      const nextFact = factsGroup[i + 1];
      const factKey = `${key}:${fact.object}`;
      timeline.set(factKey, {
        from: fact.ts || 0,
        to: fact.validUntil && fact.validUntil > 0 ? fact.validUntil : nextFact ? nextFact.ts : Date.now()
      });
    }
  }
  return timeline;
}
export {
  extractAnchors,
  inferFactTimeline,
  inferTimeRange
};
