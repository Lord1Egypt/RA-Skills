import { loadJson, debouncedSave, DATA_DIR } from "./persistence.ts";
import { resolve } from "path";
const PROFILES_PATH = resolve(DATA_DIR, "user_profiles.json");
const profiles = /* @__PURE__ */ new Map();
const BIO_PATTERNS = [
  /我是(?:一[名个位])?(.{2,20}(?:工程师|开发者|设计师|产品经理|架构师|分析师|研究员|学生|老师|教授|运维|测试|前端|后端|全栈|数据[^，。\s]{0,6}|科学家))/,
  /我(?:做|搞|干|从事|负责)(.{2,30}?)(?:的|工作|方面|领域|行业)/,
  /我的(?:职业|工作|专业|方向)是(.{2,30})/,
  /(?:我|本人)(?:擅长|精通|熟悉|会)(.{2,40})/,
  /i(?:'m| am) (?:a |an )?(.{2,40}(?:engineer|developer|designer|manager|analyst|student|researcher))/i,
  /my (?:job|role|profession|expertise) is (.{2,40})/i
];
const REMEMBER_ME_PATTERNS = [
  /(?:记住|记下|帮我记|你要知道)[：:，,\s]*(.{4,80})/,
  /(?:remember|note)[：:，,\s]*(.{4,80})/i
];
const TECH_KEYWORDS = [
  "code",
  "bug",
  "error",
  "crash",
  "debug",
  "hook",
  "frida",
  "ida",
  "api",
  "sdk",
  "json",
  "http",
  "git",
  "deploy",
  "docker",
  "nginx",
  "python",
  "typescript",
  "swift",
  "rust",
  "sql",
  "redis",
  "\u4EE3\u7801",
  "\u51FD\u6570",
  "\u62A5\u9519",
  "\u7F16\u8BD1",
  "\u8C03\u8BD5",
  "\u90E8\u7F72",
  "\u63A5\u53E3",
  "\u6570\u636E\u5E93",
  "\u91CD\u6784",
  "\u7EBF\u7A0B",
  "\u8FDB\u7A0B",
  "\u5185\u5B58",
  "\u6307\u9488",
  "\u53CD\u7F16\u8BD1",
  "\u6C47\u7F16",
  "\u9006\u5411"
];
function loadProfiles() {
  const raw = loadJson(PROFILES_PATH, {});
  profiles.clear();
  for (const [id, p] of Object.entries(raw)) {
    profiles.set(id, p);
  }
  console.log(`[cc-soul][profiles] loaded ${profiles.size} user profiles`);
}
function saveProfiles() {
  const obj = {};
  for (const [id, p] of profiles) {
    obj[id] = p;
  }
  debouncedSave(PROFILES_PATH, obj);
}
function getProfile(userId) {
  if (!userId) {
    return {
      userId: "unknown",
      displayName: "",
      tier: "new",
      messageCount: 0,
      corrections: 0,
      lastSeen: Date.now(),
      firstSeen: Date.now(),
      topics: [],
      style: "mixed",
      trust: 0.5,
      familiarity: 0,
      relationshipTrend: "stable",
      lastConflict: 0,
      sharedEpisodes: 0
    };
  }
  let p = profiles.get(userId);
  if (!p) {
    p = {
      userId,
      displayName: "",
      tier: detectTier(userId, 0),
      messageCount: 0,
      corrections: 0,
      lastSeen: Date.now(),
      firstSeen: Date.now(),
      topics: [],
      style: "mixed",
      trust: 0.5,
      familiarity: 0,
      relationshipTrend: "stable",
      lastConflict: 0,
      sharedEpisodes: 0
    };
    profiles.set(userId, p);
    saveProfiles();
  }
  return p;
}
function updateProfileOnMessage(userId, msg) {
  if (!userId) return;
  const p = getProfile(userId);
  p.messageCount++;
  p.lastSeen = Date.now();
  if (!p.languageDna) p.languageDna = { topWords: {}, avgLength: 0, samples: 0 };
  const words = msg.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi) || [];
  for (const w of words.slice(0, 10)) {
    const k = w.toLowerCase();
    p.languageDna.topWords[k] = (p.languageDna.topWords[k] || 0) + 1;
  }
  p.languageDna.avgLength = (p.languageDna.avgLength * p.languageDna.samples + msg.length) / (p.languageDna.samples + 1);
  p.languageDna.samples++;
  if (Object.keys(p.languageDna.topWords).length > 80) {
    const sorted = Object.entries(p.languageDna.topWords).sort((a, b) => b[1] - a[1]);
    p.languageDna.topWords = Object.fromEntries(sorted.slice(0, 50));
  }
  p.familiarity = Math.min(1, p.messageCount / 50);
  p.tier = detectTier(userId, p.messageCount);
  const topicWords = msg.match(/[\u4e00-\u9fff]{3,}/g);
  if (topicWords) {
    for (const w of topicWords.slice(0, 3)) {
      if (!p.topics.includes(w)) {
        p.topics.push(w);
        if (p.topics.length > 50) p.topics.shift();
      }
    }
  }
  p.style = detectStyle(msg, p);
  if (!p.language || p.messageCount <= 10) {
    p.language = detectLanguage(msg);
  }
  extractBio(p, msg);
  updateRhythm(p, msg);
  saveProfiles();
}
function detectLanguage(msg) {
  const cjk = (msg.match(/[\u4e00-\u9fff]/g) || []).length;
  const hiragana = (msg.match(/[\u3040-\u309f]/g) || []).length;
  const katakana = (msg.match(/[\u30a0-\u30ff]/g) || []).length;
  const hangul = (msg.match(/[\uac00-\ud7af]/g) || []).length;
  const cyrillic = (msg.match(/[\u0400-\u04ff]/g) || []).length;
  const arabic = (msg.match(/[\u0600-\u06ff]/g) || []).length;
  const total = msg.length || 1;
  if ((hiragana + katakana) / total > 0.15) return "ja";
  if (hangul / total > 0.15) return "ko";
  if (cjk / total > 0.15) return "zh";
  if (cyrillic / total > 0.15) return "ru";
  if (arabic / total > 0.15) return "ar";
  const lower = msg.toLowerCase();
  if (/\b(el|la|los|las|es|está|como|pero|por|que)\b/.test(lower)) return "es";
  if (/\b(le|la|les|est|dans|pour|avec|mais|des)\b/.test(lower)) return "fr";
  if (/\b(der|die|das|ist|und|ein|auf|mit|nicht)\b/.test(lower)) return "de";
  return "en";
}
function updateProfileOnCorrection(userId) {
  if (!userId) return;
  const p = getProfile(userId);
  p.corrections++;
  saveProfiles();
}
function detectTier(userId, messageCount) {
  if (messageCount >= 50) return "owner";
  if (messageCount >= 10) return "known";
  return "new";
}
function getProfileTier(userId) {
  return getProfile(userId).tier;
}
function detectStyle(msg, profile) {
  const lower = msg.toLowerCase();
  const techHits = TECH_KEYWORDS.filter((kw) => lower.includes(kw)).length;
  if (techHits >= 2) {
    if (profile.style === "casual") return "mixed";
    return "technical";
  }
  const hasEmoji = /[\u{1F300}-\u{1FAFF}]|[😀-🙏]|[🤣🥹🫡🤔🤷💀🔥👀❤️]/u.test(msg);
  if (msg.length < 20 || hasEmoji) {
    if (profile.style === "technical") return "mixed";
    return "casual";
  }
  return profile.style;
}
function extractBio(profile, msg) {
  for (const re of REMEMBER_ME_PATTERNS) {
    const m = msg.match(re);
    if (m && m[1]) {
      const newBio = m[1].trim();
      if (newBio.length >= 4 && (!profile.bio || !profile.bio.includes(newBio))) {
        profile.bio = profile.bio ? `${profile.bio}; ${newBio}` : newBio;
        if (profile.bio.length > 300) profile.bio = profile.bio.slice(-300);
        console.log(`[cc-soul][profiles] bio updated (explicit): ${newBio.slice(0, 40)}`);
        return;
      }
    }
  }
  if (profile.bio && profile.bio.length > 50) return;
  for (const re of BIO_PATTERNS) {
    const m = msg.match(re);
    if (m && m[1]) {
      const extracted = m[1].trim();
      if (extracted.length >= 4 && (!profile.bio || !profile.bio.includes(extracted))) {
        profile.bio = profile.bio ? `${profile.bio}; ${extracted}` : extracted;
        if (profile.bio.length > 300) profile.bio = profile.bio.slice(-300);
        console.log(`[cc-soul][profiles] bio updated (auto): ${extracted.slice(0, 40)}`);
        return;
      }
    }
  }
}
function setBio(userId, bio) {
  if (!userId || !bio) return;
  const p = getProfile(userId);
  p.bio = bio.slice(0, 300);
  saveProfiles();
  console.log(`[cc-soul][profiles] bio set for ${userId}: ${bio.slice(0, 40)}`);
}
function updateRhythm(profile, msg) {
  if (!profile.rhythm) {
    profile.rhythm = {
      activeHours: new Array(24).fill(0),
      weekdayTopics: [],
      weekendTopics: [],
      avgResponseDelay: 0,
      lastMessageTs: 0
    };
  }
  const now = /* @__PURE__ */ new Date();
  const hour = now.getHours();
  const isWeekend = now.getDay() === 0 || now.getDay() === 6;
  profile.rhythm.activeHours[hour]++;
  if (profile.rhythm.lastMessageTs > 0) {
    const delay = (Date.now() - profile.rhythm.lastMessageTs) / 1e3;
    if (delay < 3600) {
      profile.rhythm.avgResponseDelay = profile.rhythm.avgResponseDelay * 0.9 + delay * 0.1;
    }
  }
  profile.rhythm.lastMessageTs = Date.now();
  const topicWords = (msg.match(/[\u4e00-\u9fff]{3,}/g) || []).slice(0, 2);
  const targetTopics = isWeekend ? profile.rhythm.weekendTopics : profile.rhythm.weekdayTopics;
  for (const w of topicWords) {
    if (!targetTopics.includes(w)) targetTopics.push(w);
  }
  if (targetTopics.length > 20) targetTopics.splice(0, targetTopics.length - 15);
}
function getRhythmContext(userId) {
  const profile = getProfile(userId);
  if (!profile.rhythm || profile.messageCount < 20) return "";
  const now = /* @__PURE__ */ new Date();
  const hour = now.getHours();
  const isWeekend = now.getDay() === 0 || now.getDay() === 6;
  const hints = [];
  if (hour >= 23 || hour < 6) {
    hints.push("\u6DF1\u591C\u4E86\uFF0C\u7B80\u77ED\u56DE\u590D\uFF0C\u4E0D\u7528\u6DF1\u5165\u5C55\u5F00");
  }
  const maxActivity = Math.max(...profile.rhythm.activeHours);
  const currentHourActivity = profile.rhythm.activeHours[hour];
  if (maxActivity > 0 && currentHourActivity < maxActivity * 0.1) {
    hints.push("\u7528\u6237\u4E0D\u5E38\u5728\u8FD9\u4E2A\u65F6\u6BB5\u6D3B\u8DC3\uFF0C\u53EF\u80FD\u5728\u5FD9");
  }
  if (isWeekend && profile.rhythm.weekendTopics.length > 0) {
    hints.push(`\u5468\u672B\u6A21\u5F0F: \u7528\u6237\u5E38\u804A ${profile.rhythm.weekendTopics.slice(-3).join("\u3001")}`);
  } else if (!isWeekend && profile.rhythm.weekdayTopics.length > 0) {
    hints.push(`\u5DE5\u4F5C\u65E5\u6A21\u5F0F: \u7528\u6237\u5E38\u804A ${profile.rhythm.weekdayTopics.slice(-3).join("\u3001")}`);
  }
  if (hints.length === 0) return "";
  return `[\u8282\u5F8B\u611F\u77E5] ${hints.join("; ")}`;
}
function getUserPeakHour(userId) {
  const profile = getProfile(userId);
  if (!profile.rhythm) return -1;
  const max = Math.max(...profile.rhythm.activeHours);
  if (max === 0) return -1;
  return profile.rhythm.activeHours.indexOf(max);
}
function getProfileContext(userId) {
  const p = getProfile(userId);
  const parts = [];
  const tierLabel = p.tier === "owner" ? "\u4E3B\u4EBA" : p.tier === "known" ? "\u8001\u670B\u53CB" : "\u65B0\u670B\u53CB";
  parts.push(`[\u5F53\u524D\u5BF9\u8BDD\u8005] ${tierLabel}`);
  if (p.bio) {
    parts.push(`\u8EAB\u4EFD: ${p.bio}`);
  }
  if (p.messageCount > 0) {
    parts.push(`\u4E92\u52A8${p.messageCount}\u6B21`);
  }
  if (p.corrections > 0 && p.messageCount > 0) {
    const rate = (p.corrections / p.messageCount * 100).toFixed(1);
    parts.push(`\u7EA0\u6B63\u7387${rate}%`);
  }
  parts.push(`\u98CE\u683C\u504F\u597D: ${p.style === "technical" ? "\u6280\u672F\u578B" : p.style === "casual" ? "\u95F2\u804A\u578B" : "\u6DF7\u5408\u578B"}`);
  if (p.topics.length > 0) {
    parts.push(`\u5E38\u804A: ${p.topics.slice(-5).join("\u3001")}`);
  }
  if (p.tier === "owner") {
    parts.push("\u63D0\u793A: \u4E3B\u4EBA\uFF0C\u6280\u672F\u6DF1\u5EA6\u4F18\u5148\uFF0C\u4E0D\u9700\u8981\u8FC7\u591A\u89E3\u91CA");
  } else if (p.tier === "new") {
    parts.push("\u63D0\u793A: \u65B0\u7528\u6237\uFF0C\u5148\u89C2\u5BDF\u518D\u9002\u914D\uFF0C\u8010\u5FC3\u4E00\u4E9B");
  }
  return parts.join(" | ");
}
function updateRelationship(userId, event) {
  if (!userId) return;
  const p = getProfile(userId);
  switch (event) {
    case "correction":
      p.trust = Math.max(0, p.trust - 0.03);
      p.lastConflict = Date.now();
      break;
    case "positive":
      p.trust = Math.min(1, p.trust + 0.02);
      p.familiarity = Math.min(1, p.familiarity + 0.01);
      break;
    case "session_end":
      p.sharedEpisodes++;
      p.familiarity = Math.min(1, p.familiarity + 5e-3);
      break;
  }
  if (p.trust > 0.7) p.relationshipTrend = "improving";
  else if (p.trust < 0.3) p.relationshipTrend = "declining";
  else p.relationshipTrend = "stable";
  saveProfiles();
}
function getRelationshipContext(userId) {
  if (!userId) return "";
  const p = getProfile(userId);
  if (p.messageCount < 10) return "";
  const hints = [];
  if (p.trust < 0.3) {
    hints.push("trust is low \u2014 be cautious, hedge uncertainty, avoid bold claims");
  } else if (p.trust > 0.8) {
    hints.push("high trust \u2014 can be more direct, give bold opinions");
  }
  if (p.familiarity > 0.7) {
    hints.push("well-known user \u2014 skip background explanations");
  } else if (p.familiarity < 0.2) {
    hints.push("relatively new \u2014 provide more context");
  }
  if (p.relationshipTrend === "declining") {
    hints.push("relationship declining \u2014 be extra careful and supportive");
  }
  if (hints.length === 0) return "";
  return `[Relationship] ${hints.join("; ")}`;
}
function trackGratitude(userMsg, lastResponse, senderId) {
  const gratitudeWords = ["\u8C22\u8C22", "\u611F\u8C22", "\u592A\u597D\u4E86", "\u725B", "\u5389\u5BB3", "\u5B8C\u7F8E", "thanks", "perfect", "\u68D2", "\u8D5E"];
  if (!gratitudeWords.some((w) => userMsg.toLowerCase().includes(w))) return;
  const topic = lastResponse.split("\n")[0]?.slice(0, 60) || "(\u672A\u77E5)";
  import("./memory.ts").then(({ addMemory }) => {
    addMemory(`[\u7528\u6237\u611F\u8C22] ${topic}`, "gratitude", senderId, "private");
    console.log(`[cc-soul][gratitude] tracked: ${topic.slice(0, 40)} from ${senderId || "unknown"}`);
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (memory): ${e.message}`);
  });
}
function trackPersonaUsage(userId, personaId) {
  if (!userId || !personaId) return;
  const p = getProfile(userId);
  if (!p.personaHistory) p.personaHistory = [];
  const existing = p.personaHistory.find((h) => h.persona === personaId);
  if (existing) {
    existing.count++;
  } else {
    p.personaHistory.push({ persona: personaId, count: 1 });
  }
  saveProfiles();
}
function getPersonaUsageSummary(userId) {
  const p = getProfile(userId);
  if (!p.personaHistory || p.personaHistory.length === 0) return "";
  const sorted = [...p.personaHistory].sort((a, b) => b.count - a.count);
  const total = sorted.reduce((sum, h) => sum + h.count, 0);
  const top3 = sorted.slice(0, 3);
  const lines = ["\u{1F3AD} \u4EBA\u683C\u53D8\u5316\u8F68\u8FF9"];
  for (const h of top3) {
    const pct = (h.count / total * 100).toFixed(0);
    const bar = "\u2588".repeat(Math.ceil(h.count / total * 15));
    lines.push(`  ${h.persona.padEnd(10)} ${bar} ${pct}% (${h.count}\u6B21)`);
  }
  if (sorted.length >= 2) {
    const dominance = sorted[0].count / total;
    if (dominance > 0.6) {
      lines.push(`  \u8D8B\u52BF: \u4E3B\u8981\u4EE5\u300C${sorted[0].persona}\u300D\u6A21\u5F0F\u4E92\u52A8`);
    } else {
      lines.push(`  \u8D8B\u52BF: \u591A\u9762\u4E92\u52A8\uFF0C\u98CE\u683C\u5747\u8861`);
    }
  }
  return lines.join("\n");
}
const userProfilesModule = {
  id: "user-profiles",
  name: "\u7528\u6237\u753B\u50CF",
  priority: 50,
  init() {
    loadProfiles();
  }
};
export {
  getPersonaUsageSummary,
  getProfile,
  getProfileContext,
  getProfileTier,
  getRelationshipContext,
  getRhythmContext,
  getUserPeakHour,
  loadProfiles,
  profiles,
  setBio,
  trackGratitude,
  trackPersonaUsage,
  updateProfileOnCorrection,
  updateProfileOnMessage,
  updateRelationship,
  userProfilesModule
};
