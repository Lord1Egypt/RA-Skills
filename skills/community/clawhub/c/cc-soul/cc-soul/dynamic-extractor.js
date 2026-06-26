const SEED_STRUCTURES = [
  // 所有权/宠物
  { words: ["\u517B\u4E86", "\u5582", "\u905B", "\u5BB6\u6709", "\u6709\u4E00\u53EA", "\u6709\u4E00\u6761", "\u6709\u4E00\u4E2A", "have a", "own a", "my pet", "feed", "walk"], slot: "ownership", predicate: "has_pet", seedStrength: "strong" },
  // 居住
  { words: ["\u4F4F\u5728", "\u642C\u5230", "\u642C\u53BB", "\u642C\u5BB6\u5230", "live in", "moved to", "located in", "based in"], slot: "location", predicate: "lives_in", seedStrength: "strong" },
  { gapPatterns: [{ prefix: "\u4F4F\u5728", suffix: "" }, { prefix: "live in", suffix: "" }, { prefix: "moved to", suffix: "" }, { prefix: "based in", suffix: "" }], slot: "location", predicate: "lives_in", seedStrength: "strong" },
  // 偏好
  { words: ["\u559C\u6B22", "\u7231", "\u504F\u597D", "\u8FF7\u4E0A", "\u7740\u8FF7", "\u7279\u522B\u559C\u6B22", "\u8D85\u559C\u6B22", "like", "love", "prefer", "enjoy", "into", "fan of"], slot: "preference", predicate: "likes", seedStrength: "strong" },
  // 反感
  { words: ["\u8BA8\u538C", "\u4E0D\u559C\u6B22", "\u53D7\u4E0D\u4E86", "\u4E0D\u60F3\u7528", "\u70E6\u6B7B", "hate", "dislike", "can't stand", "don't like"], slot: "dislike", predicate: "dislikes", seedStrength: "strong" },
  // 工作
  { gapPatterns: [{ prefix: "\u5728", suffix: "\u5DE5\u4F5C" }, { prefix: "\u5728", suffix: "\u4E0A\u73ED" }, { prefix: "\u5165\u804C", suffix: "" }, { prefix: "\u52A0\u5165\u4E86", suffix: "" }, { prefix: "work at", suffix: "" }, { prefix: "work for", suffix: "" }, { prefix: "employed at", suffix: "" }, { prefix: "joined", suffix: "" }], slot: "workplace", predicate: "works_at", seedStrength: "strong" },
  // 关系
  { words: ["\u5973\u670B\u53CB", "\u7537\u670B\u53CB", "\u8001\u5A46", "\u8001\u516C", "\u5BF9\u8C61", "\u5AB3\u5987", "\u53E6\u4E00\u534A", "\u7231\u4EBA", "girlfriend", "boyfriend", "wife", "husband", "partner", "spouse"], slot: "relationship", predicate: "relationship", seedStrength: "strong" },
  // 家庭
  { words: ["\u5973\u513F", "\u513F\u5B50", "\u5B69\u5B50", "\u7238", "\u5988", "\u54E5", "\u59D0", "\u5F1F", "\u59B9", "daughter", "son", "child", "dad", "mom", "brother", "sister", "father", "mother"], slot: "family", predicate: "has_family", seedStrength: "strong" },
  // 职业
  { gapPatterns: [{ prefix: "\u6211\u662F", suffix: "\u5DE5\u7A0B\u5E08" }, { prefix: "\u6211\u662F", suffix: "\u5F00\u53D1" }, { prefix: "\u6211\u662F\u505A", suffix: "\u7684" }, { prefix: "i am a", suffix: "" }, { prefix: "i work as", suffix: "" }, { prefix: "my job is", suffix: "" }], slot: "occupation", predicate: "occupation", seedStrength: "strong" },
  // 习惯
  { words: ["\u6BCF\u5929", "\u4E60\u60EF", "\u7ECF\u5E38", "\u603B\u662F", "\u4E00\u822C\u90FD", "every day", "usually", "always", "habit", "routine"], slot: "habit", predicate: "habit", seedStrength: "medium" },
  // 学习
  { words: ["\u5728\u5B66", "\u5728\u7814\u7A76", "\u5F00\u59CB\u5B66", "\u5165\u95E8", "\u6700\u8FD1\u5728\u770B", "\u60F3\u5B66", "\u51C6\u5907\u5B66", "\u6253\u7B97\u5B66", "learning", "studying", "started learning", "getting into", "picked up"], slot: "learning", predicate: "learning", seedStrength: "medium" },
  // 引用（弱信号）
  { words: ["\u63D0\u5230", "\u8BF4\u8FC7", "\u804A\u5230", "\u542C\u8BF4", "mentioned", "said", "talked about", "heard"], slot: "mention", predicate: "mentioned", seedStrength: "weak" },
  // 比较偏好
  { gapPatterns: [{ prefix: "", suffix: "\u6BD4" }], slot: "comparison", predicate: "prefers", seedStrength: "medium" },
  // ── S2: 英文扩展模式（补充覆盖面）──
  // 教育
  { words: ["graduated from", "studied at", "majored in", "degree in", "enrolled in", "attended"], slot: "education", predicate: "education", seedStrength: "strong" },
  // 健康
  { words: ["allergic to", "can't eat", "diagnosed with", "suffer from", "taking medication", "prescribed"], slot: "health", predicate: "health_condition", seedStrength: "strong" },
  // 年龄/身份
  { gapPatterns: [{ prefix: "i'm", suffix: "years old" }, { prefix: "i am", suffix: "years old" }, { prefix: "my name is", suffix: "" }, { prefix: "call me", suffix: "" }], slot: "identity", predicate: "identity", seedStrength: "strong" },
  // 乐器/运动
  { words: ["play the", "play guitar", "play piano", "play violin", "practice", "train for"], slot: "activity", predicate: "plays", seedStrength: "medium" },
  // 语言
  { words: ["speak", "fluent in", "native speaker", "bilingual", "learning to speak"], slot: "language", predicate: "speaks", seedStrength: "medium" },
  // 旅行
  { words: ["traveled to", "visited", "went to", "been to", "trip to", "vacation in"], slot: "travel", predicate: "traveled_to", seedStrength: "medium" },
  // 购买/拥有
  { words: ["bought", "purchased", "got a new", "recently got", "just bought"], slot: "purchase", predicate: "bought", seedStrength: "medium" },
  // 创作
  { words: ["painted", "wrote", "built", "created", "made", "designed", "composed"], slot: "creation", predicate: "created", seedStrength: "medium" },
  // 婚姻
  { words: ["married to", "engaged to", "dating", "in a relationship", "my fianc\xE9", "my fianc\xE9e"], slot: "relationship", predicate: "married_to", seedStrength: "strong" },
  // 恐惧
  { words: ["afraid of", "scared of", "phobia", "terrified of", "can't stand"], slot: "fear", predicate: "fears", seedStrength: "medium" },
  // 目标
  { words: ["want to", "planning to", "hope to", "dream of", "goal is", "aiming for"], slot: "goal", predicate: "wants_to", seedStrength: "weak" }
];
const _userStrength = /* @__PURE__ */ new Map();
function getEffectiveStrength(structureWord, userId) {
  if (userId) {
    const userMap = _userStrength.get(userId);
    if (userMap) {
      const data = userMap.get(structureWord);
      if (data && data.total >= 2) {
        return data.hits / data.total;
      }
    }
  }
  for (const s of SEED_STRUCTURES) {
    if (s.words?.includes(structureWord)) {
      return s.seedStrength === "strong" ? 1 : s.seedStrength === "medium" ? 0.5 : 0.3;
    }
  }
  return 0.3;
}
function updateStructureStrength(structureWord, userId, wasCorrectSlot) {
  if (!_userStrength.has(userId)) _userStrength.set(userId, /* @__PURE__ */ new Map());
  const userMap = _userStrength.get(userId);
  const data = userMap.get(structureWord) ?? { hits: 0, total: 0 };
  data.total++;
  if (wasCorrectSlot) data.hits++;
  userMap.set(structureWord, data);
}
function dynamicExtract(content, userId) {
  const results = [];
  if (!content || content.length < 4) return results;
  for (const structure of SEED_STRUCTURES) {
    if (structure.gapPatterns) {
      for (const gp of structure.gapPatterns) {
        const extracted = matchGapPattern(content, gp);
        if (extracted && extracted.length >= 1 && extracted.length <= 15) {
          const strength = getEffectiveStrength(gp.prefix || gp.suffix, userId);
          const threshold = structure.seedStrength === "strong" ? 0.3 : structure.seedStrength === "medium" ? 0.5 : 0.7;
          if (strength >= threshold) {
            results.push({
              subject: "user",
              predicate: structure.predicate,
              object: extracted.replace(/[，。！？\s]+$/, "").replace(/[了的呢吧啊嘛]+$/, ""),
              confidence: Math.min(0.95, strength),
              source: "user_said",
              structureWord: gp.prefix || gp.suffix,
              slot: structure.slot
            });
          }
        }
      }
    }
    if (structure.words) {
      for (const word of structure.words) {
        const idx = content.indexOf(word);
        if (idx < 0) continue;
        const beforeWord = content.slice(Math.max(0, idx - 6), idx);
        const thirdPerson = /老板|同事|他|她|朋友|对方|客户/.test(beforeWord);
        if (thirdPerson && structure.predicate !== "relationship") continue;
        const afterWord = content.slice(idx + word.length).trim();
        const contentWord = afterWord.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1];
        if (!contentWord || contentWord.length < 1) continue;
        const strength = getEffectiveStrength(word, userId);
        const threshold = structure.seedStrength === "strong" ? 0.3 : structure.seedStrength === "medium" ? 0.5 : 0.7;
        if (strength >= threshold) {
          let object = contentWord.replace(/[，。！？\s]+$/, "").replace(/[了的呢吧啊嘛]+$/, "");
          if (object.length < 1) continue;
          if (structure.slot === "relationship") {
            object = object.replace(/^叫/, "");
            object = `${word}\uFF1A${object}`;
          }
          results.push({
            subject: "user",
            predicate: structure.predicate,
            object,
            confidence: Math.min(0.95, strength),
            source: "user_said",
            structureWord: word,
            slot: structure.slot
          });
        }
        break;
      }
    }
  }
  try {
    const learnedStructures = getLearnedStructureWords(userId);
    for (const ls of learnedStructures) {
      for (const word of ls.words ?? []) {
        const idx = content.indexOf(word);
        if (idx < 0) continue;
        const afterWord = content.slice(idx + word.length).trim();
        const contentWord = afterWord.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1];
        if (!contentWord) continue;
        results.push({
          subject: "user",
          predicate: ls.predicate,
          object: contentWord.replace(/[，。！？\s]+$/, ""),
          confidence: 0.6,
          source: "ai_inferred",
          structureWord: word,
          slot: ls.slot
        });
        break;
      }
    }
  } catch {
  }
  const seen = /* @__PURE__ */ new Set();
  const deduped = results.filter((r) => {
    const key = `${r.predicate}:${r.object}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  return deduped;
}
function matchGapPattern(text, pattern) {
  if (!pattern.prefix && !pattern.suffix) return null;
  if (pattern.prefix && !pattern.suffix) {
    const idx = text.indexOf(pattern.prefix);
    if (idx < 0) return null;
    const after = text.slice(idx + pattern.prefix.length).trim();
    return after.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1] ?? null;
  }
  const re = new RegExp(`${escapeRegex(pattern.prefix)}([^\uFF0C\u3002\uFF01\uFF1F,;\uFF1B\\n]{1,15})${escapeRegex(pattern.suffix)}`);
  const match = text.match(re);
  return match ? match[1].trim() : null;
}
function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
const _learnedStructures = /* @__PURE__ */ new Map();
function getLearnedStructureWords(userId) {
  if (!userId) return [];
  return _learnedStructures.get(userId) ?? [];
}
function discoverNewStructureWords(userId) {
  try {
    const aamMod = require("./aam.ts");
    if (!aamMod.getCooccurrence) return;
    const { memoryState } = require("./memory.ts");
    const userMems = memoryState.memories.filter((m) => m.userId === userId && m.source === "user_said");
    if (userMems.length < 10) return;
    const phraseFollowers = /* @__PURE__ */ new Map();
    for (const m of userMems) {
      const content = m.content || "";
      const matches = content.matchAll(new RegExp("(\\p{Script=Han}{2,3})\\s*(\\p{Script=Han}{2,4})", "gu"));
      for (const match of matches) {
        const phrase = match[1];
        const follower = match[2];
        if (!phraseFollowers.has(phrase)) phraseFollowers.set(phrase, []);
        phraseFollowers.get(phrase).push(follower);
      }
    }
    for (const [phrase, followers] of phraseFollowers) {
      if (followers.length < 3) continue;
      if (SEED_STRUCTURES.some((s) => s.words?.includes(phrase))) continue;
      const existing = _learnedStructures.get(userId) ?? [];
      if (existing.some((s) => s.words?.includes(phrase))) continue;
      const unique = [...new Set(followers)];
      if (unique.length < 2) continue;
      let intraCooccurrence = 0;
      const maxPairs = unique.length * (unique.length - 1) / 2;
      for (let i = 0; i < unique.length && i < 10; i++) {
        for (let j = i + 1; j < unique.length && j < 10; j++) {
          if (aamMod.getCooccurrence(unique[i], unique[j]) >= 2) intraCooccurrence++;
        }
      }
      const concentration = maxPairs > 0 ? intraCooccurrence / maxPairs : 0;
      if (concentration > 0.3) {
        const newStructure = {
          words: [phrase],
          slot: `learned_${phrase}`,
          predicate: `related_to_${phrase}`,
          seedStrength: "medium",
          learned: true
        };
        if (!_learnedStructures.has(userId)) _learnedStructures.set(userId, []);
        _learnedStructures.get(userId).push(newStructure);
        const list = _learnedStructures.get(userId);
        if (list.length > 20) list.splice(0, list.length - 20);
        console.log(`[cc-soul][dynamic-extractor] discovered structure word "${phrase}" for ${userId.slice(0, 8)} (concentration=${concentration.toFixed(2)})`);
      }
    }
  } catch {
  }
}
const _endSignalData = /* @__PURE__ */ new Map();
function learnEndSignal(lastUserMsg, followUpBehavior, userId) {
  const key = userId ?? "_global";
  if (!_endSignalData.has(key)) _endSignalData.set(key, /* @__PURE__ */ new Map());
  const userMap = _endSignalData.get(key);
  const tails = extractTailPhrases(lastUserMsg);
  for (const tail of tails) {
    const data = userMap.get(tail) ?? { endCount: 0, continueCount: 0 };
    if (followUpBehavior === "continue") {
      data.continueCount++;
    } else {
      data.endCount++;
    }
    userMap.set(tail, data);
  }
}
function isEndSignal(msg, userId) {
  const tails = extractTailPhrases(msg);
  const key = userId ?? "_global";
  const userMap = _endSignalData.get(key);
  if (userMap) {
    for (const tail of tails) {
      const data = userMap.get(tail);
      if (data && data.endCount + data.continueCount >= 3) {
        const rate = data.endCount / (data.endCount + data.continueCount);
        if (rate > 0.7) return true;
        if (rate < 0.3) return false;
      }
    }
  }
  return /搞定|可以了|好了|解决了|明白了|OK|行吧|没问题|谢谢|thanks/i.test(msg);
}
function extractTailPhrases(msg) {
  const phrases = [];
  const cjkMatches = msg.match(/[\u4e00-\u9fff]{2,6}/g) || [];
  if (cjkMatches.length > 0) {
    phrases.push(cjkMatches[cjkMatches.length - 1]);
    if (cjkMatches.length > 1) phrases.push(cjkMatches[cjkMatches.length - 2]);
  }
  const enMatches = msg.match(/[a-zA-Z]{2,10}/gi) || [];
  if (enMatches.length > 0) phrases.push(enMatches[enMatches.length - 1].toLowerCase());
  return phrases;
}
const WORK_CONTEXT_SEEDS = /* @__PURE__ */ new Set(["\u4EE3\u7801", "\u9879\u76EE", "\u4F1A\u8BAE", "review", "\u4E0A\u7EBF", "\u90E8\u7F72", "\u9700\u6C42", "\u6392\u671F", "\u52A0\u73ED", "\u8FDB\u5EA6", "\u6587\u6863", "bug", "\u6D4B\u8BD5"]);
const LIFE_CONTEXT_SEEDS = /* @__PURE__ */ new Set(["\u5403\u996D", "\u770B\u7535\u5F71", "\u901B\u8857", "\u56DE\u5BB6", "\u5468\u672B", "\u65C5\u6E38", "\u505A\u996D", "\u6563\u6B65", "\u7EA6\u4F1A", "\u751F\u65E5"]);
const COMMAND_SEEDS = /* @__PURE__ */ new Set(["\u8BA9\u6211", "\u8981\u6C42", "\u5B89\u6392", "\u6279\u51C6", "\u5BA1\u6279", "\u4EA4\u7ED9", "\u50AC", "\u6307\u793A", "\u53EB\u6211"]);
function inferRelationship(personName, userId) {
  try {
    const aamMod = require("./aam.ts");
    if (!aamMod.getCooccurrence) return "unknown";
    let workScore = 0, lifeScore = 0, commandScore = 0;
    for (const w of WORK_CONTEXT_SEEDS) {
      workScore += aamMod.getCooccurrence(personName, w) ?? 0;
    }
    for (const w of LIFE_CONTEXT_SEEDS) {
      lifeScore += aamMod.getCooccurrence(personName, w) ?? 0;
    }
    for (const w of COMMAND_SEEDS) {
      commandScore += aamMod.getCooccurrence(personName, w) ?? 0;
    }
    const total = workScore + lifeScore + commandScore;
    if (total < 3) return "unknown";
    if (commandScore > workScore * 0.5) return "superior";
    if (workScore > lifeScore * 2) return "colleague";
    if (lifeScore > workScore * 2) return "close_relation";
    return "acquaintance";
  } catch {
    return "unknown";
  }
}
export {
  discoverNewStructureWords,
  dynamicExtract,
  getEffectiveStrength,
  inferRelationship,
  isEndSignal,
  learnEndSignal,
  updateStructureStrength
};
