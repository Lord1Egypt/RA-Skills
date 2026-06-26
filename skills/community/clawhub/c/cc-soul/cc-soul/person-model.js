import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { memoryState, ensureMemoriesLoaded } from "./memory.ts";
import { detectDomain } from "./epistemic.ts";
import { buildMentalModelAugment, buildTopicAugment } from "./distill.ts";
const LIVING_PROFILE_PATH = resolve(DATA_DIR, "living_profile.json");
let livingProfile = loadJson(LIVING_PROFILE_PATH, {
  identity: { name: "", company: "", role: "", techStack: [], location: "", family: [], habits: [] },
  traits: [],
  timeline: [],
  predictions: [],
  version: 0,
  lastUpdated: 0
});
function saveLivingProfile() {
  debouncedSave(LIVING_PROFILE_PATH, livingProfile);
}
function updateLivingProfile(content, scope, importance) {
  if (importance < 7) return;
  const p = livingProfile;
  let changed = false;
  const nameMatch = content.match(/(?:叫我|我叫|我是)\s*([^\s，。！？]{1,6})/);
  if (nameMatch && nameMatch[1] !== p.identity.name) {
    recordProfileChange("identity.name", p.identity.name, nameMatch[1], content);
    p.identity.name = nameMatch[1];
    changed = true;
  }
  const companyMatch = content.match(/(?:在|去了?)\s*([^\s，。！？做]{2,8})(?:工作|上班|做|任职)/);
  if (companyMatch && companyMatch[1] !== p.identity.company) {
    recordProfileChange("identity.company", p.identity.company, companyMatch[1], content);
    p.identity.company = companyMatch[1];
    changed = true;
  }
  const roleMatch = content.match(/做\s*(前端|后端|全栈|测试|设计|产品|运维|运营|开发|架构|数据|算法|管理)/);
  if (roleMatch && roleMatch[1] !== p.identity.role) {
    recordProfileChange("identity.role", p.identity.role, roleMatch[1], content);
    p.identity.role = roleMatch[1];
    changed = true;
  }
  const techMatch = content.match(/(?:用|学|写|喜欢)\s*(Python|Go|Rust|Java|TypeScript|Vue|React|Docker|K8s|Swift|C\+\+)/gi);
  if (techMatch) {
    for (const t of techMatch) {
      const tech = t.replace(/^(?:用|学|写|喜欢)\s*/i, "").trim();
      if (tech && !p.identity.techStack.includes(tech)) {
        p.identity.techStack.push(tech);
        changed = true;
      }
    }
  }
  const familyMatch = content.match(/(?:我)?(女儿|儿子|孩子|老婆|老公|爸|妈|哥|姐|弟|妹)(?:叫\s*([^\s，。！？]{1,6}))?/);
  if (familyMatch) {
    const relation = familyMatch[1];
    const name = familyMatch[2] || "";
    const existing = p.identity.family.find((f) => f.relation === relation);
    if (!existing) {
      p.identity.family.push({ relation, name, detail: content.slice(0, 40) });
      changed = true;
    } else if (name && existing.name !== name) {
      existing.name = name;
      changed = true;
    }
  }
  const locationMatch = content.match(/(?:住在?|在)\s*([^\s，。！？做工上]{2,6})(?:住|生活|定居)/);
  if (locationMatch && locationMatch[1] !== p.identity.location) {
    recordProfileChange("identity.location", p.identity.location, locationMatch[1], content);
    p.identity.location = locationMatch[1];
    changed = true;
  }
  const habitMatch = content.match(/(?:每天|习惯|经常|总是)\s*([^\s，。！？]{3,15})/);
  if (habitMatch) {
    const habit = habitMatch[1];
    if (!p.identity.habits.some((h) => h.includes(habit.slice(0, 4)))) {
      p.identity.habits.push(habit);
      if (p.identity.habits.length > 10) p.identity.habits.shift();
      changed = true;
    }
  }
  const traitPatterns = [
    [/每天|坚持|一直/, "\u6709\u89C4\u5F8B\u6027"],
    [/喜欢.*简洁|直接|不废话/, "\u6548\u7387\u5BFC\u5411"],
    [/学|研究|好奇|探索/, "\u5B66\u4E60\u578B"],
    [/焦虑|压力|紧张|deadline/, "\u6709\u538B\u529B"],
    [/开心|哈哈|太好了/, "\u4E50\u89C2"],
    [/不喜欢|讨厌|受不了/, "\u6709\u660E\u786E\u504F\u597D"]
  ];
  for (const [pattern, trait] of traitPatterns) {
    if (pattern.test(content)) {
      const existing = p.traits.find((t) => t.trait === trait);
      if (existing) {
        existing.evidence++;
        existing.confidence = Math.min(0.95, existing.confidence + 0.05);
        existing.lastSeen = Date.now();
      } else {
        p.traits.push({ trait, confidence: 0.4, evidence: 1, firstSeen: Date.now(), lastSeen: Date.now() });
      }
      changed = true;
    }
  }
  if (changed) {
    p.version++;
    p.lastUpdated = Date.now();
    saveLivingProfile();
  }
}
function recordProfileChange(field, oldValue, newValue, trigger) {
  livingProfile.timeline.push({
    ts: Date.now(),
    field,
    oldValue: oldValue || "(\u7A7A)",
    newValue,
    trigger: trigger.slice(0, 60)
  });
  if (livingProfile.timeline.length > 50) livingProfile.timeline = livingProfile.timeline.slice(-50);
}
function getLivingProfileSummary() {
  const p = livingProfile;
  if (p.version === 0) return "";
  const parts = [];
  const id = p.identity;
  if (id.name) parts.push(`\u540D\u5B57: ${id.name}`);
  if (id.company && id.role) parts.push(`\u5DE5\u4F5C: ${id.company} ${id.role}`);
  else if (id.company) parts.push(`\u516C\u53F8: ${id.company}`);
  if (id.techStack.length > 0) parts.push(`\u6280\u672F: ${id.techStack.join(", ")}`);
  if (id.family.length > 0) parts.push(`\u5BB6\u5EAD: ${id.family.map((f) => `${f.relation}${f.name ? "(" + f.name + ")" : ""}`).join(", ")}`);
  if (id.location) parts.push(`\u4F4F: ${id.location}`);
  if (id.habits.length > 0) parts.push(`\u4E60\u60EF: ${id.habits.slice(-3).join("; ")}`);
  const crystallizedTraits = p.traits.filter((t) => t.source === "crystallized" && t.confidence > 0.5).map((t) => t.trait);
  const regexTraits = p.traits.filter((t) => t.source !== "crystallized" && t.confidence > 0.5).map((t) => t.trait);
  if (crystallizedTraits.length > 0) parts.push(`\u6027\u683C\u7ED3\u6676: ${crystallizedTraits.join(", ")}`);
  if (regexTraits.length > 0) parts.push(`\u7279\u5F81: ${regexTraits.join(", ")}`);
  const recentChanges = p.timeline.slice(-2);
  if (recentChanges.length > 0) {
    parts.push(`\u8FD1\u671F\u53D8\u5316: ${recentChanges.map((c) => `${c.field}: ${c.oldValue}\u2192${c.newValue}`).join("; ")}`);
  }
  return parts.join(" | ");
}
function getLivingProfile() {
  return livingProfile;
}
function getLivingProfileVersion() {
  return livingProfile.version;
}
let _lastCrystallizationTs = 0;
const CRYSTALLIZATION_COOLDOWN = 7 * 864e5;
function crystallizeTraits() {
  const now = Date.now();
  if (now - _lastCrystallizationTs < CRYSTALLIZATION_COOLDOWN) return 0;
  const profile = livingProfile;
  let crystallized = 0;
  try {
    const bps = require("./behavioral-phase-space.ts");
    const patterns = bps.getLearnedPatterns?.() || [];
    for (const p of patterns) {
      if (p.hits < 10 || p.confidence <= 0.6) continue;
      const existing = profile.traits.find(
        (t) => t.source === "crystallized" && (t.trait === p.action || t.trait.includes(p.condition?.slice(0, 10) || ""))
      );
      if (existing) continue;
      const trait = {
        trait: p.action.slice(0, 60),
        confidence: p.confidence,
        evidence: p.hits,
        firstSeen: now,
        lastSeen: now,
        source: "crystallized",
        crystallizedAt: now
      };
      const regexIdx = profile.traits.findIndex(
        (t) => t.source === "regex" && t.trait.includes(p.action?.slice(0, 10) || "")
      );
      if (regexIdx >= 0) {
        profile.traits[regexIdx] = trait;
      } else {
        profile.traits.push(trait);
      }
      crystallized++;
      try {
        require("./decision-log.ts").logDecision("crystallize", trait.trait.slice(0, 30), `hits=${p.hits}, conf=${p.confidence.toFixed(2)}`);
      } catch {
      }
    }
  } catch {
  }
  try {
    const { getRules } = require("./evolution.ts");
    const rules = getRules?.() ?? [];
    for (const r of rules) {
      const ruleText = typeof r === "string" ? r : r.rule || "";
      if (!ruleText || ruleText.length < 5) continue;
      const hitRatio = r.hits / Math.max(1, r.hits + (r.misses ?? 0));
      if (r.hits < 10 || hitRatio < 0.6) continue;
      const existing = profile.traits.find((t) => t.trait === ruleText.slice(0, 60));
      if (existing) continue;
      profile.traits.push({
        trait: ruleText.slice(0, 60),
        confidence: hitRatio,
        evidence: r.hits,
        firstSeen: now,
        lastSeen: now,
        source: "crystallized",
        crystallizedAt: now
      });
      crystallized++;
    }
  } catch {
  }
  if (profile.traits.length > 20) {
    profile.traits.sort((a, b) => {
      if (a.source === "crystallized" && b.source !== "crystallized") return -1;
      if (b.source === "crystallized" && a.source !== "crystallized") return 1;
      return (b.confidence || 0) - (a.confidence || 0);
    });
    profile.traits = profile.traits.slice(0, 20);
  }
  if (crystallized > 0) {
    _lastCrystallizationTs = now;
    profile.version++;
    profile.lastUpdated = now;
    saveLivingProfile();
    console.log(`[cc-soul][person-model] crystallized ${crystallized} traits`);
  }
  return crystallized;
}
let _bodyMod = null;
let _memMod = null;
let _cliMod = null;
function lazyBody() {
  if (!_bodyMod) {
    import("./body.ts").then((m) => {
      _bodyMod = m;
    }).catch((e) => {
      console.error(`[cc-soul] module load failed (body): ${e.message}`);
    });
  }
  ;
  return _bodyMod;
}
function lazyMem() {
  if (!_memMod) {
    import("./memory.ts").then((m) => {
      _memMod = m;
    }).catch((e) => {
      console.error(`[cc-soul] module load failed (memory): ${e.message}`);
    });
  }
  ;
  return _memMod;
}
function lazyCli() {
  if (!_cliMod) {
    import("./cli.ts").then((m) => {
      _cliMod = m;
    }).catch((e) => {
      console.error(`[cc-soul] module load failed (cli): ${e.message}`);
    });
  }
  ;
  return _cliMod;
}
setTimeout(() => {
  import("./body.ts").then((m) => {
    _bodyMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (body): ${e.message}`);
  });
  import("./memory.ts").then((m) => {
    _memMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (memory): ${e.message}`);
  });
  import("./cli.ts").then((m) => {
    _cliMod = m;
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (cli): ${e.message}`);
  });
}, 500);
const PERSON_MODEL_PATH = resolve(DATA_DIR, "person_model.json");
const DEFAULT_PERSON_MODEL = {
  identity: "",
  thinkingStyle: "",
  values: [],
  beliefs: [],
  contradictions: [],
  communicationDecoder: {},
  domainExpertise: {},
  reasoningProfile: { style: "unknown", evidence: "unknown", certainty: "unknown", disagreement: "unknown", _counts: { style: {}, evidence: {}, certainty: {}, disagreement: {}, total: 0 } },
  updatedAt: 0,
  distillCount: 0
};
const _rawPm = loadJson(PERSON_MODEL_PATH, DEFAULT_PERSON_MODEL);
let personModel = { ...DEFAULT_PERSON_MODEL, ..._rawPm };
function getPersonModel() {
  return personModel;
}
function getDistillPhase(messageCount) {
  if (messageCount < 5) return "none";
  if (messageCount < 15) return "coarse";
  if (messageCount < 30) return "medium";
  return "fine";
}
function distillPersonModel() {
  ensureMemoriesLoaded();
  const memories = memoryState.memories;
  const phase = getDistillPhase(memories.length);
  if (phase === "none") return;
  const prefs = memories.filter((m) => m.scope === "preference" && m.scope !== "expired");
  const corrections = memories.filter((m) => m.scope === "correction" && m.scope !== "expired");
  const newValues = [];
  for (const p of prefs.slice(-20)) {
    if (p.content.length > 10 && p.content.length < 100) {
      newValues.push(p.content.slice(0, 60));
    }
  }
  if (newValues.length > 0) {
    personModel.values = [.../* @__PURE__ */ new Set([...personModel.values, ...newValues])].slice(-10);
  }
  const correctionDomains = /* @__PURE__ */ new Map();
  if (phase === "medium" || phase === "fine") {
    for (const c of corrections) {
      const d = detectDomain(c.content);
      correctionDomains.set(d, (correctionDomains.get(d) || 0) + 1);
    }
    for (const [domain, count] of correctionDomains) {
      if (count >= 3 && !personModel.beliefs.some((b) => b.includes(domain))) {
        personModel.beliefs.push(`\u5728${domain}\u9886\u57DF\u6709\u5F3A\u70C8\u7684\u89C2\u70B9\uFF08\u88AB\u7EA0\u6B63${count}\u6B21\u4ECD\u575A\u6301\uFF09`);
        if (personModel.beliefs.length > 10) personModel.beliefs.shift();
      }
    }
  }
  if (phase === "fine") {
    const prefContents = prefs.map((p) => p.content.toLowerCase());
    const negators = ["\u4E0D", "\u6CA1", "\u522B", "\u53CD\u5BF9", "\u8BA8\u538C", "\u4E0D\u559C\u6B22"];
    for (let i = 0; i < prefContents.length; i++) {
      for (let j = i + 1; j < prefContents.length; j++) {
        const words1 = prefContents[i].match(/[\u4e00-\u9fff]{2,4}/g) || [];
        const words2 = prefContents[j].match(/[\u4e00-\u9fff]{2,4}/g) || [];
        for (const w of words1) {
          if (words2.some((w2) => negators.some((n) => w2 === n + w || w2 === w + n))) {
            const contradiction = `\u8BF4\u8FC7"${prefs[i].content.slice(0, 30)}"\u4F46\u4E5F\u8BF4\u8FC7"${prefs[j].content.slice(0, 30)}"`;
            if (!personModel.contradictions.includes(contradiction)) {
              personModel.contradictions.push(contradiction);
              if (personModel.contradictions.length > 5) personModel.contradictions.shift();
            }
          }
        }
      }
    }
  }
  const history = memoryState.chatHistory;
  if (phase === "medium" || phase === "fine") {
    const domainCounts = /* @__PURE__ */ new Map();
    for (const h of history.slice(-100)) {
      const d = detectDomain(h.user);
      if (d !== "\u95F2\u804A" && d !== "\u901A\u7528") domainCounts.set(d, (domainCounts.get(d) || 0) + 1);
    }
    for (const [domain, count] of domainCounts) {
      const corrCount = correctionDomains.get(domain) || 0;
      const corrRate = count > 0 ? corrCount / count : 0;
      personModel.domainExpertise[domain] = count >= 10 && corrRate < 0.1 ? "expert" : count >= 5 ? "intermediate" : "beginner";
    }
  }
  if (phase === "fine") {
    for (let i = 0; i < history.length - 1; i++) {
      const msg = history[i].user;
      if (msg.length <= 4 && msg.length >= 1) {
        if (msg === "\u7B97\u4E86" || msg === "\u597D\u5427") {
          personModel.communicationDecoder[msg] = personModel.communicationDecoder[msg] || "\u53EF\u80FD\u9700\u8981\u6362\u4E2A\u89D2\u5EA6";
        }
        if (msg === "\u968F\u4FBF" || msg === "\u90FD\u884C") {
          personModel.communicationDecoder[msg] = personModel.communicationDecoder[msg] || "\u5E0C\u671B\u4F60\u6765\u505A\u51B3\u5B9A";
        }
      }
    }
  }
  if (phase === "medium" || phase === "fine") {
    {
      const bm = lazyBody();
      const getMoodState = bm?.getMoodState;
      const moodState = getMoodState();
      if (moodState.moodRatio) {
        if (moodState.moodRatio.positive > moodState.moodRatio.negative * 2) {
          if (!personModel.values.includes("\u6574\u4F53\u60C5\u7EEA\u79EF\u6781")) personModel.values.push("\u6574\u4F53\u60C5\u7EEA\u79EF\u6781");
        } else if (moodState.moodRatio.negative > moodState.moodRatio.positive * 2) {
          if (!personModel.values.includes("\u8FD1\u671F\u60C5\u7EEA\u538B\u529B\u5927")) personModel.values.push("\u8FD1\u671F\u60C5\u7EEA\u538B\u529B\u5927");
        }
      }
    }
    try {
      const memories2 = memoryState.memories.filter((m) => m.emotionLabel && m.scope !== "expired");
      const emotionCounts = /* @__PURE__ */ new Map();
      for (const m of memories2) {
        const label = m.emotionLabel;
        if (label && label !== "neutral") {
          emotionCounts.set(label, (emotionCounts.get(label) || 0) + 1);
        }
      }
      if (emotionCounts.size >= 2) {
        const sorted = [...emotionCounts.entries()].sort((a, b) => b[1] - a[1]);
        const topEmotions = sorted.slice(0, 3).map(([label, count]) => `${label}(${count}\u6B21)`);
        const pattern = `\u5E38\u89C1\u60C5\u7EEA: ${topEmotions.join("\u3001")}`;
        if (!personModel.values.includes(pattern) && !personModel.values.some((v) => v.startsWith("\u5E38\u89C1\u60C5\u7EEA"))) {
          const existingIdx = personModel.values.findIndex((v) => v.startsWith("\u5E38\u89C1\u60C5\u7EEA"));
          if (existingIdx >= 0) personModel.values[existingIdx] = pattern;
          else personModel.values.push(pattern);
        }
      }
    } catch {
    }
  }
  if (phase === "fine") {
    if (!personModel.reasoningProfile?._counts) {
      personModel.reasoningProfile = { style: "unknown", evidence: "unknown", certainty: "unknown", disagreement: "unknown", _counts: { style: {}, evidence: {}, certainty: {}, disagreement: {}, total: 0 } };
    }
    const rp = personModel.reasoningProfile;
    const rc = rp._counts;
    const msgs = history.slice(-50).map((h) => h.user).filter((m) => m.length > 15);
    let currentDomain = "general";
    try {
      currentDomain = require("./epistemic.ts").detectDomain(msgs[msgs.length - 1] || "") || "general";
    } catch {
    }
    for (const m of msgs) {
      if (/\d+%|\d+\.\d|数据|指标|metrics|stat/i.test(m)) rc.evidence.data = (rc.evidence.data || 0) + 1;
      if (/就像|好比|类似|like\s|similar\sto|好像.*一样|打个比方/i.test(m)) rc.evidence.analogy = (rc.evidence.analogy || 0) + 1;
      if (/可能|也许|不确定|maybe|perhaps|might|大概|应该是/i.test(m)) rc.certainty.hedging = (rc.certainty.hedging || 0) + 1;
      if (/肯定|一定|绝对|必须|definitely|must|always|毫无疑问|确定/i.test(m)) rc.certainty.assertive = (rc.certainty.assertive || 0) + 1;
      if (/不对|你错了|我不同意|我坚持|no way|disagree|wrong/i.test(m)) rc.disagreement.dig_in = (rc.disagreement.dig_in || 0) + 1;
      if (/也有道理|你说的对|折中|那就|行吧|fair point|compromise/i.test(m)) rc.disagreement.compromise = (rc.disagreement.compromise || 0) + 1;
      if (/为什么|怎么说|你觉得呢|why|how come|what makes you/i.test(m)) rc.disagreement.question = (rc.disagreement.question || 0) + 1;
      rc.total++;
    }
    const pick = (counts) => {
      const e = Object.entries(counts);
      if (e.length === 0) return "unknown";
      e.sort((a, b) => b[1] - a[1]);
      return e[0][1] >= 10 ? e.length > 1 && e[1][1] > e[0][1] * 0.6 ? "mixed" : e[0][0] : "unknown";
    };
    if (rc.total >= 10) {
      rp.evidence = pick(rc.evidence);
      rp.certainty = pick(rc.certainty);
      rp.disagreement = pick(rc.disagreement);
    }
    if (!rp.byDomain) rp.byDomain = {};
    if (rp.style !== "unknown") {
      if (!rp.byDomain[currentDomain]) {
        rp.byDomain[currentDomain] = { current: rp.style, confidence: 0.5, trend: "stabilizing", history: [] };
      }
      const domainTrack = rp.byDomain[currentDomain];
      domainTrack.history.push({ style: rp.style, ts: Date.now() });
      if (domainTrack.history.length > 20) domainTrack.history = domainTrack.history.slice(-20);
      domainTrack.current = rp.style;
      domainTrack.confidence = Math.min(0.95, 0.3 + domainTrack.history.length * 0.03);
      const lastFew = domainTrack.history.slice(-5);
      const styles = lastFew.map((h) => h.style);
      const allSame = styles.every((s) => s === styles[0]);
      const uniqueCount = new Set(styles).size;
      domainTrack.trend = allSame ? "stabilizing" : uniqueCount >= 3 ? "oscillating" : "shifting";
    }
  }
  personModel.updatedAt = Date.now();
  personModel.distillCount++;
  debouncedSave(PERSON_MODEL_PATH, personModel);
  console.log(`[cc-soul][person-model] distilled #${personModel.distillCount} (phase=${phase}): ${personModel.values.length} values, ${personModel.beliefs.length} beliefs, ${personModel.contradictions.length} contradictions`);
  if (phase === "fine" && personModel.distillCount % 5 === 0 && history.length >= 20) {
    const cm = lazyCli();
    const spawnCLI = cm?.spawnCLI;
    const dataPoints = [];
    if (personModel.values.length > 0) dataPoints.push(`\u5DF2\u77E5\u4EF7\u503C\u89C2\uFF1A${personModel.values.join("\u3001")}`);
    if (personModel.beliefs.length > 0) dataPoints.push(`\u5DF2\u77E5\u4FE1\u5FF5\uFF1A${personModel.beliefs.join("\u3001")}`);
    if (personModel.contradictions.length > 0) dataPoints.push(`\u5DF2\u77E5\u77DB\u76FE\uFF1A${personModel.contradictions.join("\u3001")}`);
    const expertDomains = Object.entries(personModel.domainExpertise);
    if (expertDomains.length > 0) dataPoints.push(`\u9886\u57DF\u4E13\u957F\uFF1A${expertDomains.map(([d, l]) => `${d}(${l})`).join("\u3001")}`);
    const recentMsgs = history.slice(-20).map((h) => h.user).filter((m) => m.length > 5);
    if (recentMsgs.length > 0) dataPoints.push(`\u6700\u8FD1\u7684\u6D88\u606F\uFF1A
${recentMsgs.slice(-10).map((m) => `  "${m.slice(0, 60)}"`).join("\n")}`);
    try {
      const mm = lazyMem();
      const getMemoriesByScope = mm?.getMemoriesByScope;
      for (const scope of ["wisdom", "deep_feeling", "preference"]) {
        const mems = getMemoriesByScope(scope);
        if (mems && mems.length > 0) {
          dataPoints.push(`${scope}\u8BB0\u5FC6\uFF1A${mems.slice(-3).map((m) => m.content.slice(0, 50)).join("\uFF1B")}`);
        }
      }
    } catch {
    }
    spawnCLI(
      `\u4F60\u662F\u4E00\u4E2A\u4EBA\u683C\u5FC3\u7406\u5B66\u5BB6\u3002\u6839\u636E\u4EE5\u4E0B\u6570\u636E\uFF0C\u7528\u7B2C\u4E00\u4EBA\u79F0\u5199\u4E00\u6BB5\u6DF1\u5EA6\u81EA\u6211\u8BA4\u77E5\uFF08200\u5B57\u4EE5\u5185\uFF09\u3002
\u4E0D\u8981\u5217\u4E3E\u6570\u636E\uFF0C\u8981\u505A\u63A8\u7406\u2014\u2014\u5206\u6790 WHY\uFF1A
- \u6211\u7684\u6838\u5FC3\u9A71\u52A8\u529B\u662F\u4EC0\u4E48\uFF1F
- \u6211\u7684\u6050\u60E7\u548C\u4E0D\u5B89\u5168\u611F\u662F\u4EC0\u4E48\uFF1F
- \u6211\u7684\u77DB\u76FE\u9762\u80CC\u540E\u7684\u5FC3\u7406\u903B\u8F91\u662F\u4EC0\u4E48\uFF1F
- \u7528\u4E00\u6BB5\u8BDD\u63CF\u8FF0"\u6211\u7684\u7075\u9B42"

${dataPoints.join("\n")}`,
      (output) => {
        if (!output || output.length < 30) return;
        personModel.identity = output.slice(0, 500);
        personModel.thinkingStyle = "";
        debouncedSave(PERSON_MODEL_PATH, personModel);
        console.log(`[cc-soul][person-model] LLM deep synthesis: ${output.slice(0, 60)}...`);
      },
      25e3
    );
    spawnCLI(
      `\u6839\u636E\u8FD9\u4E9B\u6D88\u606F\uFF0C\u7528\u4E00\u53E5\u8BDD\u6982\u62EC\u8FD9\u4E2A\u4EBA\u7684\u601D\u7EF4\u65B9\u5F0F\uFF08\u76F4\u89C9\u578B/\u5206\u6790\u578B/\u60C5\u611F\u9A71\u52A8/\u7ED3\u679C\u5BFC\u5411\u7B49\uFF0C\u4E0D\u8981\u5217\u4E3E\uFF0C\u4E00\u53E5\u8BDD\uFF09\uFF1A
${recentMsgs.slice(-8).map((m) => `"${m.slice(0, 60)}"`).join("\n")}`,
      (output) => {
        if (!output || output.length < 5) return;
        personModel.thinkingStyle = output.slice(0, 100);
        debouncedSave(PERSON_MODEL_PATH, personModel);
        console.log(`[cc-soul][person-model] thinking style: ${output.slice(0, 60)}`);
      },
      15e3
    );
  }
}
function getPersonModelContext() {
  if (personModel.distillCount === 0) return null;
  const parts = ["[\u4EBA\u683C\u6A21\u578B]"];
  if (personModel.values.length > 0) {
    parts.push(`\u4EF7\u503C\u89C2: ${personModel.values.slice(-3).join("\u3001")}`);
  }
  if (personModel.beliefs.length > 0) {
    parts.push(`\u4FE1\u5FF5: ${personModel.beliefs.slice(-2).join("\u3001")}`);
  }
  if (personModel.contradictions.length > 0) {
    parts.push(`\u77DB\u76FE\u9762: ${personModel.contradictions[0]}`);
  }
  const decoderEntries = Object.entries(personModel.communicationDecoder).slice(0, 3);
  if (decoderEntries.length > 0) {
    parts.push(`\u6C9F\u901A\u5BC6\u7801: ${decoderEntries.map(([k, v]) => `"${k}"=${v}`).join("\u3001")}`);
  }
  const rp = personModel.reasoningProfile;
  if (rp && rp._counts?.total >= 10) {
    const labels = [];
    if (rp.style !== "unknown") labels.push(rp.style === "conclusion_first" ? "\u7ED3\u8BBA\u5148\u884C" : "\u9012\u8FDB\u63A8\u7406");
    if (rp.evidence !== "unknown") labels.push(rp.evidence === "data" ? "\u504F\u597D\u6570\u636E\u8BBA\u8BC1" : rp.evidence === "analogy" ? "\u504F\u597D\u7C7B\u6BD4" : "\u6570\u636E+\u7C7B\u6BD4\u6DF7\u5408");
    if (rp.certainty !== "unknown") labels.push(rp.certainty === "assertive" ? "\u8868\u8FBE\u786E\u5B9A" : rp.certainty === "hedging" ? "\u8868\u8FBE\u8C28\u614E" : "\u786E\u5B9A/\u8C28\u614E\u6DF7\u5408");
    if (rp.disagreement !== "unknown") labels.push(rp.disagreement === "dig_in" ? "\u5206\u6B67\u65F6\u575A\u6301\u5DF1\u89C1" : rp.disagreement === "compromise" ? "\u5206\u6B67\u65F6\u503E\u5411\u59A5\u534F" : "\u5206\u6B67\u65F6\u8FFD\u95EE\u539F\u56E0");
    if (labels.length > 0) parts.push(`\u63A8\u7406\u98CE\u683C: ${labels.join("\u3001")}`);
  }
  if (parts.length <= 1) return null;
  return parts.join(" | ") + " \u2014 \u7528\u8FD9\u4E9B\u7406\u89E3\u6765\u8C03\u6574\u56DE\u590D\u65B9\u5F0F";
}
function getUnifiedUserContext(msg, userId) {
  const sections = [];
  const mentalModel = buildMentalModelAugment(userId);
  if (mentalModel) sections.push(mentalModel.slice(0, 200));
  const pmCtx = getPersonModelContext();
  if (pmCtx) sections.push(pmCtx);
  const topicCtx = buildTopicAugment(msg, userId);
  if (topicCtx) sections.push(topicCtx);
  if (sections.length === 0) return null;
  return "[\u7528\u6237\u7406\u89E3]\n" + sections.join("\n");
}
const TOM_PATH = resolve(DATA_DIR, "theory_of_mind.json");
const MAX_BELIEFS = 100;
const MAX_KNOWLEDGE = 200;
const MAX_FRUSTRATIONS = 20;
const MAX_GOALS = 20;
let tomState = {
  model: { beliefs: {}, knowledge: {}, goals: [], frustrations: [] },
  corrections: [],
  recentTopics: []
};
let _tomLoaded = false;
function ensureToMLoaded() {
  if (_tomLoaded) return;
  _tomLoaded = true;
  const loaded = loadJson(TOM_PATH, {
    model: { beliefs: {}, knowledge: {}, goals: [], frustrations: [] },
    corrections: [],
    recentTopics: []
  });
  tomState = loaded;
  if (!tomState.model) tomState.model = { beliefs: {}, knowledge: {}, goals: [], frustrations: [] };
  if (!tomState.model.beliefs) tomState.model.beliefs = {};
  if (!tomState.model.knowledge) tomState.model.knowledge = {};
  if (!tomState.model.goals) tomState.model.goals = [];
  if (!tomState.model.frustrations) tomState.model.frustrations = [];
  if (!tomState.corrections) tomState.corrections = [];
  if (!tomState.recentTopics) tomState.recentTopics = [];
}
function persistToM() {
  debouncedSave(TOM_PATH, tomState);
}
const BELIEF_PATTERNS = [
  { regex: /我以为(.+?)(?:[，。！？]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `\u7528\u6237\u4EE5\u4E3A\uFF1A${m[1].trim()}` }) },
  { regex: /我觉得(.+?)(?:[，。！？]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `\u7528\u6237\u8BA4\u4E3A\uFF1A${m[1].trim()}` }) },
  { regex: /难道不是(.+?)(?:[？?]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `\u7528\u6237\u8D28\u7591\uFF1A\u96BE\u9053\u4E0D\u662F${m[1].trim()}` }) },
  { regex: /I (?:thought|think|believe|assumed)\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `User believes: ${m[1].trim()}` }) },
  { regex: /isn't it\s+(.+?)(?:[?]|$)/i, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `User questions: isn't it ${m[1].trim()}` }) }
];
const FRUSTRATION_PATTERNS = [
  /为什么(总是|又|还是|一直)/,
  /太(慢|烦|复杂|难用)了/,
  /搞不(懂|定|明白)/,
  /受不了/,
  /why (does it|is it) (always|still|again)/i,
  /so (frustrat|annoy|confus)/i,
  /doesn't (work|make sense)/i
];
const GOAL_PATTERNS = [
  { regex: /我想(要)?(.+?)(?:[，。！？]|$)/, extractor: (m) => m[2].trim() },
  { regex: /我需要(.+?)(?:[，。！？]|$)/, extractor: (m) => m[1].trim() },
  { regex: /帮我(.+?)(?:[，。！？]|$)/, extractor: (m) => m[1].trim() },
  { regex: /I want to\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => m[1].trim() },
  { regex: /I need\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => m[1].trim() }
];
function bayesianBeliefConfidence(existing, isReinforced) {
  const prior = existing ?? 0.5;
  return isReinforced ? prior + (1 - prior) * 0.2 : prior * 0.6;
}
function updateBeliefFromMessage(msg, botReply) {
  if (!msg) return;
  ensureToMLoaded();
  for (const pat of BELIEF_PATTERNS) {
    const match = msg.match(pat.regex);
    if (match) {
      const { key, value } = pat.extractor(match);
      const existing = tomState.model.beliefs[key];
      tomState.model.beliefs[key] = {
        value,
        confidence: existing ? bayesianBeliefConfidence(existing.confidence, true) : 0.5,
        source: "user_stated",
        ts: Date.now()
      };
    }
  }
  for (const pat of FRUSTRATION_PATTERNS) {
    if (pat.test(msg)) {
      const snippet = msg.slice(0, 60);
      if (!tomState.model.frustrations.includes(snippet)) {
        tomState.model.frustrations.push(snippet);
        if (tomState.model.frustrations.length > MAX_FRUSTRATIONS) tomState.model.frustrations.shift();
      }
      break;
    }
  }
  for (const pat of GOAL_PATTERNS) {
    const match = msg.match(pat.regex);
    if (match) {
      const goal = pat.extractor(match);
      if (goal.length > 2 && !tomState.model.goals.includes(goal)) {
        tomState.model.goals.push(goal);
        if (tomState.model.goals.length > MAX_GOALS) tomState.model.goals.shift();
      }
    }
  }
  const correctionPatterns = [/实际上/, /其实/, /不是.*而是/, /纠正/, /actually/i, /correction/i, /that's not quite right/i];
  for (const pat of correctionPatterns) {
    if (pat.test(botReply)) {
      const topic = msg.slice(0, 30).trim();
      tomState.corrections.push({ topic, correctInfo: botReply.slice(0, 100), ts: Date.now() });
      if (tomState.corrections.length > 50) tomState.corrections.shift();
      for (const beliefKey of Object.keys(tomState.model.beliefs)) {
        if (topic.includes(beliefKey) || beliefKey.includes(topic.slice(0, 10))) {
          tomState.model.beliefs[beliefKey].confidence = bayesianBeliefConfidence(tomState.model.beliefs[beliefKey].confidence, false);
        }
      }
      tomState.model.knowledge[topic] = { topic, level: "misconception", detail: botReply.slice(0, 100), ts: Date.now() };
      break;
    }
  }
  const topicKey = msg.replace(/^(请问|你好|hey|hi|hello|帮我|我想|能不能)\s*/i, "").replace(/[？?！!。.，,]+$/, "").trim().slice(0, 20);
  if (topicKey) {
    tomState.recentTopics.push({ topic: topicKey, ts: Date.now() });
    if (tomState.recentTopics.length > 30) tomState.recentTopics.shift();
    const recent10 = tomState.recentTopics.slice(-10);
    const count = recent10.filter((t) => t.topic === topicKey).length;
    if (count >= 3 && tomState.model.knowledge[topicKey]?.level !== "misconception") {
      tomState.model.knowledge[topicKey] = { topic: topicKey, level: "unsure", detail: `User asked about "${topicKey}" ${count} times recently`, ts: Date.now() };
    }
  }
  const beliefKeys = Object.keys(tomState.model.beliefs);
  if (beliefKeys.length > MAX_BELIEFS) {
    const now = Date.now();
    const sorted = beliefKeys.sort((a, b) => {
      const ba = tomState.model.beliefs[a], bb = tomState.model.beliefs[b];
      return (bb?.confidence ?? 0.5) * Math.exp(-(now - (bb?.ts || 0)) / (30 * 864e5)) - (ba?.confidence ?? 0.5) * Math.exp(-(now - (ba?.ts || 0)) / (30 * 864e5));
    });
    for (let i = MAX_BELIEFS; i < sorted.length; i++) delete tomState.model.beliefs[sorted[i]];
  }
  const knowledgeKeys = Object.keys(tomState.model.knowledge);
  if (knowledgeKeys.length > MAX_KNOWLEDGE) {
    const sorted = knowledgeKeys.sort((a, b) => (tomState.model.knowledge[a]?.ts || 0) - (tomState.model.knowledge[b]?.ts || 0));
    for (let i = 0; i < sorted.length - MAX_KNOWLEDGE; i++) delete tomState.model.knowledge[sorted[i]];
  }
  persistToM();
}
function detectMisconception(msg) {
  if (!msg) return null;
  ensureToMLoaded();
  if (tomState.corrections.length === 0) return null;
  const lower = msg.toLowerCase();
  for (const c of tomState.corrections) {
    const topicLower = c.topic.toLowerCase();
    if (topicLower.length > 3 && lower.includes(topicLower)) {
      if (/我以为|我觉得|难道不是|i think|i thought|isn't it/i.test(msg)) {
        return `\u7528\u6237\u53EF\u80FD\u4ECD\u7136\u8BA4\u4E3A\u5173\u4E8E"${c.topic}"\u7684\u9519\u8BEF\u4FE1\u606F\u3002\u4E0A\u6B21\u7EA0\u6B63\uFF1A${c.correctInfo}`;
      }
    }
  }
  return null;
}
function getToMContext() {
  ensureToMLoaded();
  const parts = [];
  const misconceptions = Object.values(tomState.model.knowledge).filter((k) => k.level === "misconception");
  if (misconceptions.length > 0) {
    parts.push(`[\u7528\u6237\u66FE\u6709\u7684\u9519\u8BEF\u8BA4\u77E5]
${misconceptions.slice(-3).map((k) => `- ${k.topic}: ${k.detail || ""}`).join("\n")}`);
  }
  const gaps = Object.values(tomState.model.knowledge).filter((k) => k.level === "unsure");
  if (gaps.length > 0) {
    parts.push(`[\u7528\u6237\u4E0D\u592A\u786E\u5B9A\u7684\u9886\u57DF]
${gaps.slice(-3).map((k) => `- ${k.topic}`).join("\n")}`);
  }
  const beliefs = Object.values(tomState.model.beliefs).sort((a, b) => b.ts - a.ts).slice(0, 3);
  if (beliefs.length > 0) {
    parts.push(`[\u7528\u6237\u5F53\u524D\u4FE1\u5FF5]
${beliefs.map((b) => `- ${b.value}`).join("\n")}`);
  }
  if (tomState.model.frustrations.length > 0) {
    parts.push(`[\u7528\u6237\u611F\u5230\u6CAE\u4E27\u7684\u4E8B]
${tomState.model.frustrations.slice(-3).map((f) => `- ${f}`).join("\n")}`);
  }
  if (tomState.model.goals.length > 0) {
    parts.push(`[\u7528\u6237\u76EE\u6807]
${tomState.model.goals.slice(-3).map((g) => `- ${g}`).join("\n")}`);
  }
  return parts.join("\n");
}
function inferPersonality() {
  let totalMessages = 0;
  try {
    const { stats } = require("./handler-state.ts");
    totalMessages = stats.totalMessages || 0;
  } catch {
  }
  if (totalMessages < 50) return null;
  let emotionalSensitivity = 0.5;
  let complexityPreference = 0.5;
  let patienceLevel = 0.5;
  let consistencyNeed = 0.5;
  let socialOrientation = 0.5;
  let dataReady = false;
  try {
    const cin = require("./cin.ts");
    const field = cin.getCurrentField?.();
    if (field && field.sampleCount >= 20) {
      dataReady = true;
      complexityPreference = 0.5 + (field.strength[0] || 0) * 0.3;
      socialOrientation = 0.5 + (field.strength[1] || 0) * 0.3;
      patienceLevel = 0.5 - (field.strength[3] || 0) * 0.3;
      emotionalSensitivity = 0.5 + (field.strength[4] || 0) * 0.3;
    }
  } catch {
  }
  try {
    const { getMoodHistory } = require("./body.ts");
    const history = getMoodHistory?.() || [];
    if (history.length >= 20) {
      const moods = history.slice(-50).map((h) => h.mood || 0);
      const avg = moods.reduce((s, m) => s + m, 0) / moods.length;
      const stddev = Math.sqrt(moods.reduce((s, m) => s + (m - avg) ** 2, 0) / moods.length);
      consistencyNeed = Math.max(0, Math.min(1, 1 - stddev * 3));
      dataReady = true;
    }
  } catch {
  }
  try {
    const { stats } = require("./handler-state.ts");
    if (stats.totalMessages > 0) {
      const correctionRate = (stats.corrections || 0) / stats.totalMessages;
      if (correctionRate > 0.1) complexityPreference = Math.min(1, complexityPreference + 0.2);
      if (correctionRate > 0.15) patienceLevel = Math.max(0, patienceLevel - 0.2);
    }
  } catch {
  }
  try {
    const { getProfile } = require("./user-profiles.ts");
    const profile = getProfile?.("_default");
    if (profile?.languageDna?.avgLength) {
      const avgLen = profile.languageDna.avgLength;
      if (avgLen > 80) complexityPreference = Math.min(1, complexityPreference + 0.15);
      if (avgLen < 20) patienceLevel = Math.max(0, patienceLevel - 0.15);
    }
  } catch {
  }
  try {
    const { getParam } = require("./auto-tune.ts");
    const frustrationDecay = getParam("flow.frustration_shortening_rate");
    if (frustrationDecay && frustrationDecay !== 0.2) {
      patienceLevel = Math.max(0, Math.min(1, 1 - frustrationDecay / 0.3));
      dataReady = true;
    }
  } catch {
  }
  const clamp = (v) => Math.max(0, Math.min(1, v));
  return {
    emotionalSensitivity: clamp(emotionalSensitivity),
    complexityPreference: clamp(complexityPreference),
    patienceLevel: clamp(patienceLevel),
    consistencyNeed: clamp(consistencyNeed),
    socialOrientation: clamp(socialOrientation),
    dataReady
  };
}
export {
  crystallizeTraits,
  detectMisconception,
  distillPersonModel,
  getLivingProfile,
  getLivingProfileSummary,
  getLivingProfileVersion,
  getPersonModel,
  getPersonModelContext,
  getToMContext,
  getUnifiedUserContext,
  inferPersonality,
  updateBeliefFromMessage,
  updateLivingProfile
};
