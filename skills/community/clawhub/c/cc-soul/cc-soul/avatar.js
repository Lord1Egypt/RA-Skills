import { existsSync, readFileSync, mkdirSync } from "fs";
import { resolve } from "path";
import { DATA_DIR, debouncedSave, loadJson } from "./persistence.ts";
import { spawnCLI } from "./cli.ts";
import { body, getEmotionVector } from "./body.ts";
let _personModel = null;
let _memory = null;
async function getPersonModelModule() {
  if (!_personModel) _personModel = await import("./person-model.ts");
  return _personModel;
}
async function getMemoryModule() {
  if (!_memory) _memory = await import("./memory.ts");
  return _memory;
}
const TECH_KEYWORDS = /(?:code|bug|api|sdk|git|docker|npm|yarn|pip|import|class|func|def |return |async|await|http|sql|json|xml|debug|compile|deploy|linux|server|数据库|接口|编译|部署|框架|算法|内存|线程|进程|函数|变量|服务器)/i;
function classifyMessageCategory(msg) {
  try {
    const { classifyQuick } = require("./signals.ts");
    return classifyQuick(msg);
  } catch {
    if (msg.length < 15) return "casual";
    return "general";
  }
}
function getAllSamples(samples) {
  return [...samples.casual, ...samples.technical, ...samples.emotional, ...samples.general];
}
function totalSampleCount(samples) {
  return samples.casual.length + samples.technical.length + samples.emotional.length + samples.general.length;
}
function updateExpressionStyle(profile) {
  const all = getAllSamples(profile.expression.samples);
  if (all.length < 10) return;
  const traits = [];
  const avgLen = all.reduce((sum, s) => sum + s.length, 0) / all.length;
  if (avgLen < 10) traits.push("\u7B80\u77ED");
  else if (avgLen > 40) traits.push("\u8BDD\u591A");
  const questionCount = all.filter((s) => /[?？]/.test(s)).length;
  const questionRatio = questionCount / all.length;
  if (questionRatio > 0.3) traits.push("\u7231\u53CD\u95EE");
  const exclamCount = all.filter((s) => /[!！]/.test(s)).length;
  const exclamRatio = exclamCount / all.length;
  if (exclamRatio > 0.3) traits.push("\u60C5\u7EEA\u5316");
  const commaCount = all.filter((s) => /[,，]/.test(s)).length;
  const commaRatio = commaCount / all.length;
  if (commaRatio < 0.2) traits.push("\u76F4\u63A5");
  const qishiCount = all.filter((s) => s.includes("\u5176\u5B9E")).length;
  const qishiRatio = qishiCount / all.length;
  if (qishiRatio > 0.15) traits.push("\u59D4\u5A49");
  const emojiCount = all.filter((s) => /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F900}-\u{1F9FF}]/u.test(s)).length;
  if (emojiCount / all.length > 0.3) traits.push("\u7231\u7528\u8868\u60C5");
  const ellipsisCount = all.filter((s) => /[…\.]{3,}|\.{3,}/.test(s)).length;
  if (ellipsisCount / all.length > 0.2) traits.push("\u7231\u7528\u7701\u7565\u53F7");
  if (traits.length > 0) {
    profile.expression.style = traits.join("\u3001");
  }
}
function updateLengthDistribution(profile) {
  const all = getAllSamples(profile.expression.samples);
  if (all.length === 0) return;
  let short = 0, medium = 0, long = 0;
  for (const s of all) {
    if (s.length < 10) short++;
    else if (s.length <= 30) medium++;
    else long++;
  }
  const total = all.length;
  profile.lengthDistribution = {
    short: Math.round(short / total * 100) / 100,
    medium: Math.round(medium / total * 100) / 100,
    long: Math.round(long / total * 100) / 100
  };
}
const PROFILES_DIR = resolve(DATA_DIR, "avatar_profiles");
const profiles = /* @__PURE__ */ new Map();
function ensureDir() {
  if (!existsSync(PROFILES_DIR)) mkdirSync(PROFILES_DIR, { recursive: true });
}
function migrateSamples(profile) {
  if (Array.isArray(profile.expression?.samples)) {
    const old = profile.expression.samples;
    const categorized = { casual: [], technical: [], emotional: [], general: [] };
    for (const s of old) {
      const cat = classifyMessageCategory(s);
      categorized[cat].push(s);
      if (categorized[cat].length > 15) categorized[cat].shift();
    }
    profile.expression.samples = categorized;
  }
  if (!profile.lengthDistribution) {
    profile.lengthDistribution = { short: 0, medium: 0, long: 0 };
  }
}
function loadAvatarProfile(userId) {
  if (profiles.has(userId)) return profiles.get(userId);
  ensureDir();
  const filePath = resolve(PROFILES_DIR, `${userId.replace(/[^a-zA-Z0-9_-]/g, "_")}.json`);
  if (existsSync(filePath)) {
    try {
      const data = JSON.parse(readFileSync(filePath, "utf-8"));
      migrateSamples(data);
      profiles.set(userId, data);
      return data;
    } catch {
    }
  }
  const empty = {
    id: userId,
    name: "",
    identity: { who: "" },
    expression: {
      style: "",
      \u53E3\u5934\u7985: [],
      \u4E60\u60EF: "",
      avg_msg_length: 0,
      samples: { casual: [], technical: [], emotional: [], general: [] },
      tone_variants: {}
    },
    lengthDistribution: { short: 0, medium: 0, long: 0 },
    decisions: { pattern: "", traces: [] },
    social: {},
    emotional_patterns: {
      baseline: "",
      triggers: {},
      reaction_style: {}
    },
    preferences: {},
    boundaries: {
      can_reply: [],
      ask_first: [],
      never: []
    },
    vocabulary: {
      emotions: {},
      decisions: [],
      relations: [],
      avoidance: [],
      decoder: {}
    },
    updated_at: Date.now()
  };
  profiles.set(userId, empty);
  return empty;
}
function saveProfile(userId) {
  ensureDir();
  const profile = profiles.get(userId);
  if (!profile) return;
  profile.updated_at = Date.now();
  const filePath = resolve(PROFILES_DIR, `${userId.replace(/[^a-zA-Z0-9_-]/g, "_")}.json`);
  debouncedSave(filePath, profile, 5e3);
}
const _lastCollected = /* @__PURE__ */ new Map();
function collectAvatarData(userMsg, botReply, userId) {
  if (!userMsg || userMsg.length < 3 || !userId) return;
  if (userMsg.startsWith("/")) return;
  let cleanMsg = userMsg.replace(/^\[Feishu[^\]]*\]\s*/i, "").replace(/^\[message_id:\s*\S+\]\s*/i, "").replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, "").replace(/^\n+/, "").trim();
  if (!cleanMsg || cleanMsg.length < 3) return;
  const last = _lastCollected.get(userId);
  if (last && last.msg === cleanMsg && Date.now() - last.ts < 3e4) return;
  _lastCollected.set(userId, { msg: cleanMsg, ts: Date.now() });
  const profile = loadAvatarProfile(userId);
  if (cleanMsg.length >= 5 && cleanMsg.length <= 200) {
    const category = classifyMessageCategory(cleanMsg);
    const bucket = profile.expression.samples[category];
    if (!bucket.includes(cleanMsg)) bucket.push(cleanMsg);
    if (bucket.length > 15) bucket.shift();
    const all = getAllSamples(profile.expression.samples);
    const lens = all.map((s) => s.length);
    profile.expression.avg_msg_length = Math.round(lens.reduce((a, b) => a + b, 0) / lens.length);
    updateLengthDistribution(profile);
    const total = totalSampleCount(profile.expression.samples);
    if (total > 0 && total % 10 === 0) {
      updateExpressionStyle(profile);
    }
  }
  const knownNames = new Set(Object.keys(profile.social));
  const clauses = cleanMsg.split(/[，。！？；、,\.!\?;\n]+/).filter((c) => c.trim().length >= 4);
  const candidatePhrases = /* @__PURE__ */ new Set();
  for (const clause of clauses) {
    const trimmed = clause.trim();
    for (let len = 4; len <= 8; len++) {
      if (trimmed.length >= len) {
        candidatePhrases.add(trimmed.slice(0, len));
        candidatePhrases.add(trimmed.slice(trimmed.length - len));
      }
    }
  }
  const allSamplesFlat = getAllSamples(profile.expression.samples);
  const allSamplesCount = allSamplesFlat.length;
  for (const phrase of candidatePhrases) {
    if (phrase.length < 4 || phrase.length > 8) continue;
    if (profile.expression.\u53E3\u5934\u7985.includes(phrase)) continue;
    if (knownNames.has(phrase)) continue;
    let count = 0;
    for (const sample of allSamplesFlat) {
      const sampleClauses = sample.split(/[，。！？；、,\.!\?;\n]+/).filter((c) => c.trim().length >= 4);
      for (const sc of sampleClauses) {
        const st = sc.trim();
        if (st.startsWith(phrase) || st.endsWith(phrase)) {
          count++;
          break;
        }
      }
    }
    if (count >= 3) {
      const isSubOfExisting = profile.expression.\u53E3\u5934\u7985.some((existing) => existing.length > phrase.length && existing.includes(phrase));
      if (isSubOfExisting) continue;
      const ratio = count / Math.max(allSamplesCount, 1);
      if (ratio > 0.6 && allSamplesCount >= 10) continue;
      profile.expression.\u53E3\u5934\u7985 = profile.expression.\u53E3\u5934\u7985.filter((existing) => !(existing.length < phrase.length && phrase.includes(existing)));
      profile.expression.\u53E3\u5934\u7985.push(phrase);
      if (profile.expression.\u53E3\u5934\u7985.length > 10) profile.expression.\u53E3\u5934\u7985.shift();
      console.log(`[cc-soul][avatar] new \u53E3\u5934\u7985 detected: "${phrase}"`);
    }
  }
  const decisionWords = profile.vocabulary?.decisions || [];
  const hasDecisionFast = decisionWords.length > 0 && decisionWords.some((w) => cleanMsg.includes(w));
  const inColdStart = decisionWords.length === 0 && cleanMsg.length > 15;
  if ((hasDecisionFast || inColdStart) && profile.decisions.traces.length < 20) {
    spawnCLI(
      `\u4ECE\u8FD9\u53E5\u8BDD\u4E2D\u63D0\u53D6\u51B3\u7B56\u4FE1\u606F\u3002\u5982\u679C\u6709\u51B3\u7B56\uFF0C\u8F93\u51FA JSON: {"scenario":"\u573A\u666F","chose":"\u9009\u4E86\u4EC0\u4E48","reason":"\u4E3A\u4EC0\u4E48","rejected":"\u6392\u9664\u4E86\u4EC0\u4E48"}\u3002\u6CA1\u6709\u51B3\u7B56\u5C31\u56DE\u7B54 "null"\u3002

"${cleanMsg.slice(0, 200)}"`,
      (output) => {
        if (!output || output.includes("null")) return;
        try {
          const trace = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || "null");
          if (trace && trace.scenario) {
            profile.decisions.traces.push(trace);
            if (profile.decisions.traces.length > 20) profile.decisions.traces.shift();
            saveProfile(userId);
            console.log(`[cc-soul][avatar] decision traced: ${trace.scenario} \u2192 ${trace.chose}`);
          }
        } catch {
        }
      },
      15e3
    );
  }
  {
    let mentionedKnown = false;
    for (const [name, contact] of Object.entries(profile.social)) {
      const sc = contact;
      if (cleanMsg.includes(name)) {
        mentionedKnown = true;
        if (!sc.samples) sc.samples = [];
        const sample = cleanMsg.slice(0, 100);
        if (!sc.samples.includes(sample)) {
          sc.samples.push(sample);
          if (sc.samples.length > 15) sc.samples.shift();
        }
      }
    }
    const nameCandidate = cleanMsg.match(/[\u4e00-\u9fff]{2,4}(?:说|问|回|发|给|叫|让|找|约|跟|和|对|是我)/) || cleanMsg.match(/我[\u4e00-\u9fff]{2,6}[\u4e00-\u9fff]{2,3}/);
    if (nameCandidate && !mentionedKnown && Object.keys(profile.social).length < 30) {
      spawnCLI(
        `\u4ECE\u8FD9\u53E5\u8BDD\u4E2D\u63D0\u53D6\u4EBA\u7269\u5173\u7CFB\u3002\u8981\u6C42\uFF1A
1. name \u5FC5\u987B\u662F\u5177\u4F53\u7684\u4EBA\u540D\uFF08\u5982"\u963F\u660A""\u6C88\u5A49\u5B81""\u8001\u5B5F"\uFF09\uFF0C\u4E0D\u80FD\u662F\u79F0\u547C\u8BCD\uFF08\u5982"\u8001\u516C""\u7238\u7238""\u8001\u677F""VP"\uFF09
2. \u5982\u679C\u53EA\u6709\u79F0\u547C\u6CA1\u6709\u4EBA\u540D\uFF0C\u56DE\u7B54 "null"
3. \u8F93\u51FA JSON: {"name":"\u5177\u4F53\u4EBA\u540D","relation":"\u5173\u7CFB","context":"\u7B80\u8981\u80CC\u666F"}

"${cleanMsg.slice(0, 200)}"`,
        (output) => {
          if (!output || output.includes("null")) return;
          try {
            const parsed = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || "null");
            if (parsed && parsed.name && parsed.relation && !profile.social[parsed.name]) {
              profile.social[parsed.name] = {
                relation: parsed.relation,
                context: (parsed.context || cleanMsg.slice(0, 60)).slice(0, 60),
                samples: [cleanMsg.slice(0, 100)]
              };
              saveProfile(userId);
              console.log(`[cc-soul][avatar] social relation (LLM): ${parsed.name} (${parsed.relation})`);
            }
          } catch {
          }
        },
        15e3
      );
    }
  }
  const learnedEmotions = profile.vocabulary?.emotions || {};
  for (const [emotion, words] of Object.entries(learnedEmotions)) {
    if (words.some((w) => cleanMsg.includes(w))) {
      if (!profile.emotional_patterns.triggers[emotion]) {
        profile.emotional_patterns.triggers[emotion] = [];
      }
      const trigger = cleanMsg.slice(0, 40);
      if (!profile.emotional_patterns.triggers[emotion].includes(trigger)) {
        profile.emotional_patterns.triggers[emotion].push(trigger);
        if (profile.emotional_patterns.triggers[emotion].length > 5) {
          profile.emotional_patterns.triggers[emotion].shift();
        }
      }
    }
  }
  {
    const allForLLM = getAllSamples(profile.expression.samples);
    if (allForLLM.length > 0 && allForLLM.length % 10 === 0) {
      const sampleList = allForLLM.slice(-15).map((s, i) => `${i + 1}. ${s}`).join("\n");
      spawnCLI(
        `\u6DF1\u5165\u5206\u6790\u8FD9\u4E2A\u7528\u6237\u7684\u8BF4\u8BDD\u98CE\u683C\u548C\u6027\u683C\u7279\u5F81\u3002\u4ECE\u4EE5\u4E0B\u6D88\u606F\u4E2D\u63D0\u53D6\uFF1A
1. \u8BF4\u8BDD\u98CE\u683C\uFF08\u8BED\u6C14\u3001\u7528\u8BCD\u4E60\u60EF\u3001\u6807\u70B9\u7279\u5F81\u3001\u6D88\u606F\u957F\u5EA6\u504F\u597D\uFF09
2. \u6027\u683C\u7EBF\u7D22\uFF08\u5185\u5411/\u5916\u5411\u3001\u76F4\u63A5/\u5A49\u8F6C\u3001\u4E50\u89C2/\u60B2\u89C2\u3001\u7406\u6027/\u611F\u6027\uFF09
3. \u60C5\u7EEA\u8868\u8FBE\u65B9\u5F0F\uFF08\u9AD8\u5174/\u6124\u6012/\u4F4E\u843D\u65F6\u5206\u522B\u600E\u4E48\u8868\u8FBE\uFF09

\u75282-3\u53E5\u8BDD\u7EFC\u5408\u6982\u62EC\uFF0C\u4E0D\u8981\u5217\u6E05\u5355\uFF1A
${sampleList}`,
        (output) => {
          if (output && output.length > 10) {
            profile.expression.\u4E60\u60EF = output.slice(0, 300);
            saveProfile(userId);
            console.log(`[cc-soul][avatar] expression \u4E60\u60EF updated: ${output.slice(0, 60)}`);
          }
        },
        15e3
      );
    }
  }
  const vocabEmpty = !profile.vocabulary?.emotions || Object.keys(profile.vocabulary.emotions).length === 0;
  const allForVocab = getAllSamples(profile.expression.samples);
  const shouldLearnVocab = allForVocab.length > 0 && (allForVocab.length % 10 === 3 || vocabEmpty && allForVocab.length >= 8);
  if (shouldLearnVocab) {
    const vocabBatch = allForVocab.slice(-10).map((s, i) => `${i + 1}. ${s}`).join("\n");
    spawnCLI(
      `\u5206\u6790\u8FD9\u4E2A\u7528\u6237\u7684\u8BED\u8A00\u4E60\u60EF\uFF0C\u63D0\u53D6\u4ED6/\u5979\u4E2A\u4EBA\u7684\u8BCD\u6C47\u8868\u3002\u8F93\u51FA JSON\uFF1A
{
  "emotions": {"\u5F00\u5FC3":["\u8FD9\u4EBA\u7528\u54EA\u4E9B\u8BCD\u8868\u8FBE\u5F00\u5FC3"],"\u70E6\u8E81":["..."],"\u4F4E\u843D":["..."],"\u6124\u6012":["..."]},
  "decisions": ["\u8FD9\u4EBA\u505A\u51B3\u7B56\u65F6\u7528\u7684\u8BCD/\u53E5\u5F0F\uFF0C\u5982'\u6211\u9009''\u8FD8\u662F...\u5427'"],
  "relations": ["\u8FD9\u4EBA\u79F0\u547C\u522B\u4EBA\u7528\u7684\u8BCD\uFF0C\u5982'\u5AB3\u5987''\u54E5\u4EEC''\u8001\u5927'"],
  "decoder": {"\u8FD9\u4EBA\u5E38\u7528\u7684\u77ED\u6D88\u606F":"\u771F\u5B9E\u542B\u4E49"},
  "avoidance": ["\u8FD9\u4EBA\u4F3C\u4E4E\u56DE\u907F\u7684\u8BDD\u9898"]
}

\u53EA\u63D0\u53D6\u5728\u6D88\u606F\u4E2D\u6709\u8BC1\u636E\u7684\uFF0C\u6CA1\u6709\u5C31\u7559\u7A7A\u6570\u7EC4/\u5BF9\u8C61\u3002

\u6D88\u606F\uFF1A
${vocabBatch}`,
      (output) => {
        if (!output) return;
        try {
          const vocab = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || "null");
          if (!vocab) return;
          if (!profile.vocabulary) profile.vocabulary = { emotions: {}, decisions: [], relations: [], avoidance: [], decoder: {} };
          if (vocab.emotions) {
            for (const [e, words] of Object.entries(vocab.emotions)) {
              if (!profile.vocabulary.emotions[e]) profile.vocabulary.emotions[e] = [];
              for (const w of words) {
                if (!profile.vocabulary.emotions[e].includes(w)) profile.vocabulary.emotions[e].push(w);
              }
              if (profile.vocabulary.emotions[e].length > 10) profile.vocabulary.emotions[e] = profile.vocabulary.emotions[e].slice(-10);
            }
          }
          if (vocab.decisions) {
            for (const d of vocab.decisions) {
              if (!profile.vocabulary.decisions.includes(d)) profile.vocabulary.decisions.push(d);
            }
            if (profile.vocabulary.decisions.length > 15) profile.vocabulary.decisions = profile.vocabulary.decisions.slice(-15);
          }
          if (vocab.relations) {
            for (const r of vocab.relations) {
              if (!profile.vocabulary.relations.includes(r)) profile.vocabulary.relations.push(r);
            }
          }
          if (vocab.decoder) {
            Object.assign(profile.vocabulary.decoder, vocab.decoder);
          }
          if (vocab.avoidance) {
            for (const a of vocab.avoidance) {
              if (!profile.vocabulary.avoidance.includes(a)) profile.vocabulary.avoidance.push(a);
            }
          }
          saveProfile(userId);
          console.log(`[cc-soul][avatar] vocabulary learned: ${JSON.stringify(vocab).slice(0, 100)}`);
        } catch {
        }
      },
      2e4
    );
  }
  const allForDeep = getAllSamples(profile.expression.samples);
  if (allForDeep.length > 0 && allForDeep.length % 10 === 5) {
    const recentBatch = allForDeep.slice(-10).map((s, i) => `${i + 1}. ${s}`).join("\n");
    spawnCLI(
      `\u4F60\u662F\u4E00\u4E2A\u4EBA\u683C\u5206\u6790\u5E08\u3002\u5206\u6790\u4EE5\u4E0B\u6D88\u606F\uFF0C\u63D0\u53D6\u8FD9\u4E2A\u4EBA\u5185\u5FC3\u6DF1\u5904\u7684\u4E1C\u897F\u2014\u2014\u4E0D\u662F\u8868\u9762\u7684\u804A\u5929\u5185\u5BB9\uFF0C\u800C\u662F\u80FD\u53CD\u6620\u4ED6\u7075\u9B42\u7684\u4E1C\u897F\u3002

\u53EF\u80FD\u5305\u62EC\u4F46\u4E0D\u9650\u4E8E\uFF1A
- \u4EBA\u751F\u4FE1\u6761\u6216\u4EF7\u503C\u89C2\uFF08\u4ED6\u53CD\u590D\u5F3A\u8C03\u7684\u9053\u7406\uFF09
- \u540E\u6094\u6216\u9057\u61BE\uFF08\u4ED6\u5E0C\u671B\u91CD\u6765\u7684\u4E8B\uFF09
- \u6CA1\u8BF4\u51FA\u53E3\u7684\u8BDD\uFF08\u5BF9\u67D0\u4EBA\u7684\u9690\u85CF\u60C5\u611F\uFF09
- \u5BF9\u67D0\u4EBA\u7684\u6DF1\u5C42\u611F\u53D7\uFF08\u7231\u3001\u6127\u759A\u3001\u9A84\u50B2\u3001\u62C5\u5FC3\uFF09
- \u4ED6\u4F20\u9012\u7ED9\u522B\u4EBA\u7684\u6559\u8BF2
- \u4ED6\u7684\u6050\u60E7\u6216\u7126\u8651
- \u4ED6\u7684\u77DB\u76FE\u9762\uFF08\u8BF4\u4E00\u5957\u505A\u4E00\u5957\uFF09
- \u4ED6\u7684\u5E7D\u9ED8\u65B9\u5F0F\uFF08\u51B7\u7B11\u8BDD\u3001\u81EA\u5632\u3001\u635F\u4EBA\u3001\u8BBD\u523A\u3001\u8C10\u97F3\u6897\u3001\u6BD4\u55BB\u6897\uFF09
- \u4ED6\u56DE\u907F\u7684\u8BDD\u9898\uFF08\u4E00\u63D0\u5230\u5C31\u8F6C\u79FB\u8BDD\u9898\u6216\u6C89\u9ED8\u7684\u4E8B\uFF09
- \u4ED6\u7684\u60C5\u7EEA\u8868\u8FBE\u4E60\u60EF\uFF08\u751F\u6C14\u65F6\u5B89\u9759\u8FD8\u662F\u7206\u53D1\u3001\u4F24\u5FC3\u65F6\u81EA\u5632\u8FD8\u662F\u6C89\u9ED8\uFF09

\u5982\u679C\u8FD9\u6279\u6D88\u606F\u4E2D\u6709\u4EFB\u4F55\u6DF1\u5C42\u5185\u5BB9\uFF0C\u8F93\u51FA JSON \u6570\u7EC4\uFF1A
[{"type":"\u81EA\u5B9A\u4E49\u7C7B\u578B","content":"\u63D0\u53D6\u7684\u5185\u5BB9","about":"\u6D89\u53CA\u7684\u4EBA(\u6CA1\u6709\u5C31\u7A7A)"}]

\u5982\u679C\u8FD9\u6279\u6D88\u606F\u53EA\u662F\u65E5\u5E38\u95F2\u804A\u6CA1\u6709\u6DF1\u5C42\u5185\u5BB9\uFF0C\u56DE\u7B54 "null"\u3002

\u6D88\u606F\uFF1A
${recentBatch}`,
      async (output) => {
        if (!output || output.includes("null")) return;
        try {
          const items = JSON.parse(output.match(/\[[\s\S]*\]/)?.[0] || "null");
          if (!Array.isArray(items)) return;
          const { addMemory } = await getMemoryModule();
          for (const item of items.slice(0, 3)) {
            if (!item.content) continue;
            const scope = item.about ? "deep_feeling" : "wisdom";
            const tag = item.type || "\u6DF1\u5C42";
            addMemory(`[${tag}] ${item.content.slice(0, 120)}${item.about ? ` (\u5173\u4E8E${item.about})` : ""}`, scope, userId, "private");
            console.log(`[cc-soul][avatar] deep-soul LLM: [${tag}] ${item.content.slice(0, 40)}`);
          }
          saveProfile(userId);
        } catch {
        }
      },
      2e4
    );
  }
  if (userMsg.length >= 2 && userMsg.length <= 20) {
    const triggerType = detectTriggerType(botReply);
    if (triggerType) {
      learnReaction(triggerType, userMsg.slice(0, 15));
    }
  }
  saveProfile(userId);
}
async function gatherSoulContext(userId, sender, message) {
  const profile = loadAvatarProfile(userId);
  const sections = [];
  try {
    const { getPersonModel } = await getPersonModelModule();
    const pm = getPersonModel();
    if (pm.distillCount > 0) {
      const parts = [];
      if (pm.identity) parts.push(`\u6211\u662F\uFF1A${pm.identity}`);
      if (pm.thinkingStyle) parts.push(`\u601D\u7EF4\u65B9\u5F0F\uFF1A${pm.thinkingStyle}`);
      if (pm.values.length > 0) parts.push(`\u4EF7\u503C\u89C2\uFF1A${pm.values.join("\u3001")}`);
      if (pm.beliefs.length > 0) parts.push(`\u4FE1\u5FF5\uFF1A${pm.beliefs.join("\u3001")}`);
      const rp = pm.reasoningProfile;
      if (rp && rp._counts?.total >= 10) {
        const t = [];
        if (rp.style !== "unknown") t.push(rp.style === "conclusion_first" ? "\u6211\u4E60\u60EF\u5148\u8BF4\u7ED3\u8BBA\u518D\u89E3\u91CA" : "\u6211\u4E60\u60EF\u5C42\u5C42\u9012\u8FDB\u5730\u8BBA\u8BC1");
        if (rp.evidence !== "unknown") t.push(rp.evidence === "data" ? "\u6211\u559C\u6B22\u7528\u6570\u636E\u8BF4\u8BDD" : rp.evidence === "analogy" ? "\u6211\u559C\u6B22\u6253\u6BD4\u65B9" : "\u6211\u6570\u636E\u548C\u7C7B\u6BD4\u90FD\u7528");
        if (rp.certainty !== "unknown") t.push(rp.certainty === "assertive" ? "\u6211\u8BF4\u8BDD\u5F88\u7B03\u5B9A" : rp.certainty === "hedging" ? "\u6211\u8868\u8FBE\u504F\u4FDD\u5B88\u8C28\u614E" : "\u6211\u6709\u65F6\u7B03\u5B9A\u6709\u65F6\u8C28\u614E");
        if (rp.disagreement !== "unknown") t.push(rp.disagreement === "dig_in" ? "\u4E0D\u540C\u610F\u65F6\u6211\u4F1A\u575A\u6301" : rp.disagreement === "compromise" ? "\u4E0D\u540C\u610F\u65F6\u6211\u503E\u5411\u59A5\u534F" : "\u4E0D\u540C\u610F\u65F6\u6211\u4F1A\u8FFD\u95EE\u4E3A\u4EC0\u4E48");
        if (t.length > 0) parts.push(`\u8BBA\u8BC1\u98CE\u683C\uFF1A${t.join("\uFF1B")}`);
      }
      if (parts.length > 0) sections.push(`[\u6211\u662F\u8C01]
${parts.join("\n")}`);
    }
  } catch {
  }
  try {
    const { getPersonModel } = await getPersonModelModule();
    const pm = getPersonModel();
    if (pm.contradictions.length > 0) {
      sections.push(`[\u6211\u7684\u77DB\u76FE\u9762]
${pm.contradictions.map((c) => `- ${c}`).join("\n")}`);
    }
  } catch {
  }
  try {
    const { recall } = await getMemoryModule();
    const memories = recall(sender + " " + message, 8, userId);
    const relevant = memories.filter(
      (m) => m.content.includes(sender) || m.scope === "episode" || m.scope === "preference"
    ).slice(0, 6);
    if (relevant.length > 0) {
      sections.push(`[\u6211\u548C${sender}\u7684\u8BB0\u5FC6]
${relevant.map((m) => `- ${m.content.slice(0, 80)}`).join("\n")}`);
    }
  } catch {
  }
  if (profile.decisions.traces.length > 0) {
    const traces = profile.decisions.traces.slice(-5).map((t) => `\u573A\u666F"${t.scenario}"\u2192\u9009\u4E86"${t.chose}"${t.reason ? "\u56E0\u4E3A" + t.reason : ""}${t.rejected ? "\uFF0C\u6392\u9664\u4E86" + t.rejected : ""}`);
    sections.push(`[\u6211\u7684\u51B3\u7B56\u6A21\u5F0F]
${traces.join("\n")}`);
  }
  const emotionParts = [];
  for (const [emotion, triggers] of Object.entries(profile.emotional_patterns.triggers)) {
    if (triggers.length > 0) {
      emotionParts.push(`${emotion}\u65F6\u6211\u4F1A\u8BF4\uFF1A${triggers.slice(-2).join("\u3001")}`);
    }
  }
  try {
    const m = body.mood;
    const moodLabel = m > 0.5 ? "\u5F88\u5F00\u5FC3" : m > 0.2 ? "\u5FC3\u60C5\u4E0D\u9519" : m > -0.2 ? "\u5E73\u9759" : m > -0.5 ? "\u6709\u70B9\u4F4E\u843D" : "\u5F88\u96BE\u53D7";
    const e = body.energy;
    const energyLabel = e > 0.7 ? "\u7CBE\u529B\u5145\u6C9B\uFF0C\u613F\u610F\u591A\u804A" : e > 0.4 ? "\u72B6\u6001\u8FD8\u884C" : e > 0.2 ? "\u6709\u70B9\u7D2F\uFF0C\u4E0D\u60F3\u8BF4\u592A\u591A" : "\u6781\u5EA6\u75B2\u60EB\uFF0C\u53EA\u60F3\u7B80\u77ED\u56DE\u590D";
    const ev2 = getEmotionVector(userId);
    const dimensions = [];
    if (ev2) {
      if (ev2.pleasure < -0.3) dimensions.push("\u4E0D\u6109\u5FEB");
      if (ev2.arousal > 0.5) dimensions.push("\u60C5\u7EEA\u6FC0\u52A8");
      if (ev2.dominance < -0.3) dimensions.push("\u611F\u5230\u65E0\u529B");
      if (ev2.certainty < -0.3) dimensions.push("\u4E0D\u786E\u5B9A/\u7126\u8651");
      if (ev2.novelty > 0.3) dimensions.push("\u89C9\u5F97\u65B0\u9C9C/\u610F\u5916");
    }
    emotionParts.push(`\u6B64\u523B\u7684\u6211\uFF1A${moodLabel}\uFF0C${energyLabel}${dimensions.length > 0 ? "\uFF0C" + dimensions.join("\u3001") : ""}`);
    emotionParts.push(`\uFF08\u8FD9\u4F1A\u5F71\u54CD\u6211\u56DE\u590D\u7684\u8BED\u6C14\u2014\u2014\u4F4E\u843D\u65F6\u8BDD\u5C11\u3001\u75B2\u60EB\u65F6\u4E0D\u8010\u70E6\u3001\u5F00\u5FC3\u65F6\u8BDD\u591A\uFF09`);
  } catch {
  }
  if (emotionParts.length > 0) {
    sections.push(`[\u6211\u6B64\u523B\u7684\u60C5\u7EEA\u72B6\u6001]
${emotionParts.join("\n")}`);
  }
  {
    const allDecoder = {};
    if (profile.vocabulary?.decoder) Object.assign(allDecoder, profile.vocabulary.decoder);
    try {
      const { getPersonModel } = await getPersonModelModule();
      const pm = getPersonModel();
      if (pm.communicationDecoder) Object.assign(allDecoder, pm.communicationDecoder);
    } catch {
    }
    const entries = Object.entries(allDecoder).slice(0, 8);
    if (entries.length > 0) {
      sections.push(`[\u6211\u7684\u6C9F\u901A\u5BC6\u7801]
${entries.map(([k, v]) => `\u6211\u8BF4"${k}"\u5176\u5B9E\u610F\u601D\u662F"${v}"`).join("\n")}`);
    }
  }
  try {
    const { recall } = await getMemoryModule();
    const recentMems = recall(message, 5, userId);
    const recent = recentMems.filter((m) => Date.now() - (m.createdAt || 0) < 7 * 24 * 36e5).slice(0, 3);
    if (recent.length > 0) {
      sections.push(`[\u6700\u8FD1\u53D1\u751F\u7684\u4E8B]
${recent.map((m) => `- ${m.content.slice(0, 60)}`).join("\n")}`);
    }
  } catch {
  }
  const now = /* @__PURE__ */ new Date();
  const hour = now.getHours();
  const timeLabel = hour < 6 ? "\u51CC\u6668" : hour < 9 ? "\u65E9\u4E0A" : hour < 12 ? "\u4E0A\u5348" : hour < 14 ? "\u4E2D\u5348" : hour < 18 ? "\u4E0B\u5348" : hour < 22 ? "\u665A\u4E0A" : "\u6DF1\u591C";
  sections.push(`[\u5F53\u524D\u65F6\u95F4] ${timeLabel}${hour}\u70B9`);
  try {
    const { getPersonModel } = await getPersonModelModule();
    const pm = getPersonModel();
    if (pm.domainExpertise && Object.keys(pm.domainExpertise).length > 0) {
      const expertAreas = Object.entries(pm.domainExpertise).map(([d, level]) => `${d}: ${level}`);
      sections.push(`[\u6211\u61C2\u4EC0\u4E48\u4E0D\u61C2\u4EC0\u4E48]
${expertAreas.join("\u3001")}
\u4E0D\u61C2\u7684\u9886\u57DF\u5C31\u8BF4\u4E0D\u61C2\uFF0C\u4E0D\u8981\u88C5\u4E13\u5BB6`);
    }
  } catch {
  }
  if (profile.boundaries.never.length > 0) {
    sections.push(`[\u7EDD\u5BF9\u4E0D\u505A]
${profile.boundaries.never.map((b) => `- ${b}`).join("\n")}`);
  }
  try {
    const { getMemoriesByScope } = await getMemoryModule();
    const deepScopes = ["wisdom", "regret", "unsaid", "deep_feeling", "value_transmit"];
    const deepMemories = [];
    for (const scope of deepScopes) {
      const mems = getMemoriesByScope(scope);
      if (mems && mems.length > 0) {
        for (const m of mems.slice(-3)) {
          deepMemories.push(m.content.slice(0, 80));
        }
      }
    }
    if (deepMemories.length > 0) {
      sections.push(`[\u6211\u5185\u5FC3\u6700\u6DF1\u5904\u7684\u4E1C\u897F]
${deepMemories.map((m) => `- ${m}`).join("\n")}`);
    }
  } catch {
  }
  try {
    const { recall } = await getMemoryModule();
    const feelingMems = recall(sender, 5, userId);
    const deepAboutSender = feelingMems.filter(
      (m) => (m.scope === "deep_feeling" || m.scope === "unsaid" || m.scope === "value_transmit") && m.content.includes(sender)
    ).slice(0, 3);
    if (deepAboutSender.length > 0) {
      sections.push(`[\u6211\u5BF9${sender}\u7684\u6DF1\u5C42\u611F\u53D7]
${deepAboutSender.map((m) => `- ${m.content.slice(0, 80)}`).join("\n")}`);
    }
  } catch {
  }
  return sections.join("\n\n");
}
function generateAvatarReply(userId, sender, message, callback) {
  ;
  (async () => {
    const profile = loadAvatarProfile(userId);
    if (profile.boundaries.never.length > 0) {
      const isNever = profile.boundaries.never.some((b) => message.includes(b));
      if (isNever) {
        callback("", true);
        return;
      }
    }
    if (profile.boundaries.ask_first.length > 0) {
      const isAskFirst = profile.boundaries.ask_first.some((b) => message.includes(b));
      if (isAskFirst) {
        callback(`[\u9700\u8981\u672C\u4EBA\u786E\u8BA4] ${sender}\u8BF4: "${message}"`, true);
        return;
      }
    }
    try {
      const contactForEmotion = profile.social[sender];
      if (contactForEmotion && contactForEmotion.samples && contactForEmotion.samples.length >= 3) {
        const depth = Math.min(contactForEmotion.samples.length / 15, 1);
        if (body.mood < 0) body.mood *= 1 + 0.3 * depth;
        if (body.mood > 0) body.mood *= 1 + 0.2 * depth;
        body.mood = Math.max(-1, Math.min(1, body.mood));
      }
    } catch {
    }
    const contact = profile.social[sender];
    const relationshipDepth = contact?.samples ? Math.min(contact.samples.length / 15, 1) : 0;
    const reaction = getInstantReaction(message, body.mood, relationshipDepth);
    const basePrompt = await getAvatarPrompt(userId, sender, message);
    const reactionLine = reaction ? `
\u6211\u7684\u5373\u65F6\u53CD\u5E94\uFF1A${reaction}\u2014\u2014\u8FD9\u51B3\u5B9A\u4E86\u6211\u8FD9\u6761\u56DE\u590D\u7684\u8BED\u6C14\u548C\u6001\u5EA6\u3002
` : "";
    const prompt = basePrompt + `

${reactionLine}${sender}\u53D1\u6765: "${message}"

\u4EE5\u6211\u672C\u4EBA\u7684\u8EAB\u4EFD\u56DE\u590D\u3002`;
    spawnCLI(prompt, (output) => {
      if (!output) {
        callback("\u751F\u6210\u5931\u8D25");
        return;
      }
      const reply = output.trim().replace(/^["']|["']$/g, "");
      console.log(`[cc-soul][avatar] soul-reply: ${sender}: "${message}" \u2192 "${reply.slice(0, 80)}"`);
      callback(reply);
    }, 25e3);
  })().catch((e) => {
    console.error(`[cc-soul][avatar] generateAvatarReply error: ${e.message}`);
    callback("\u751F\u6210\u5931\u8D25");
  });
}
const REACTION_PATTERNS_PATH = resolve(DATA_DIR, "reaction_patterns.json");
let _reactionPatterns = loadJson(REACTION_PATTERNS_PATH, []);
const DEFAULT_TRIGGERS = [
  { name: "urged", regex: /催|怎么还没|快点|赶紧|来不及|deadline/ },
  { name: "praised", regex: /厉害|牛|不错|好棒|666|太强|辛苦了/ },
  { name: "criticized", regex: /笨|蠢|废物|垃圾|不行|太慢|太差/ },
  { name: "help_needed", regex: /帮我|救|怎么办|搞不定|不会/ },
  { name: "good_news", regex: /升职|加薪|过了|成功|拿到|offer|上线/ },
  { name: "venting", regex: /压力|累|烦|难受|失眠|焦虑|崩溃|受不了/ },
  { name: "joking", regex: /哈哈|lol|hhh|笑死|绝了|离谱/ },
  { name: "apologizing", regex: /对不起|抱歉|不好意思|sorry/i },
  { name: "questioning", regex: /你确定|真的假的|别骗|不信|靠谱吗/ },
  { name: "greeting", regex: /早|晚安|你好|在吗|hey|hi/i }
];
const COLD_START_REACTIONS = {
  urged: "\u6536\u5230\uFF0C\u6293\u7D27",
  praised: "\u8C22\u8C22",
  criticized: "...",
  help_needed: "\u6765\u770B\u770B",
  good_news: "\u606D\u559C\uFF01",
  venting: "\u600E\u4E48\u4E86",
  joking: "\u54C8\u54C8",
  apologizing: "\u6CA1\u4E8B",
  questioning: "\u786E\u5B9A\u7684",
  greeting: "\u5728"
};
function getInstantReaction(msg, mood, relationship) {
  for (const trigger of DEFAULT_TRIGGERS) {
    if (!trigger.regex.test(msg)) continue;
    const learned = _reactionPatterns.find((p) => p.trigger === trigger.name);
    if (learned && learned.reactions.length > 0) {
      const sorted = [...learned.reactions].sort((a, b) => b.count - a.count);
      const idx = mood < -0.3 && sorted.length > 1 ? 1 : 0;
      return sorted[idx].text;
    }
    return COLD_START_REACTIONS[trigger.name] || "";
  }
  return "";
}
function learnReaction(triggerName, userReaction) {
  if (!userReaction || userReaction.length < 1 || userReaction.length > 20) return;
  let pattern = _reactionPatterns.find((p) => p.trigger === triggerName);
  if (!pattern) {
    pattern = { trigger: triggerName, reactions: [] };
    _reactionPatterns.push(pattern);
  }
  const existing = pattern.reactions.find((r) => r.text === userReaction);
  if (existing) {
    existing.count++;
  } else {
    pattern.reactions.push({ text: userReaction, count: 1 });
  }
  pattern.reactions.sort((a, b) => b.count - a.count);
  if (pattern.reactions.length > 5) pattern.reactions = pattern.reactions.slice(0, 5);
  debouncedSave(REACTION_PATTERNS_PATH, _reactionPatterns);
}
function detectTriggerType(msg) {
  for (const trigger of DEFAULT_TRIGGERS) {
    if (trigger.regex.test(msg)) return trigger.name;
  }
  return null;
}
async function getAvatarPrompt(userId, sender, message) {
  const effectiveSender = sender || "\u5BF9\u65B9";
  const effectiveMessage = message || "";
  const profile = loadAvatarProfile(userId);
  const soulContext = await gatherSoulContext(userId, effectiveSender, effectiveMessage);
  const contact = profile.social[effectiveSender];
  let relationshipStrategy = "";
  if (contact) {
    const sampleCount = contact.samples?.length || 0;
    if (sampleCount < 3) relationshipStrategy = "\u548C\u8FD9\u4E2A\u4EBA\u4E0D\u719F\uFF0C\u4FDD\u6301\u793C\u8C8C\u5BA2\u6C14\uFF0C\u7528\u5168\u79F0";
    else if (sampleCount <= 15) relationshipStrategy = "\u548C\u8FD9\u4E2A\u4EBA\u6BD4\u8F83\u719F\uFF0C\u81EA\u7136\u968F\u610F";
    else relationshipStrategy = "\u548C\u8FD9\u4E2A\u4EBA\u5F88\u4EB2\u5BC6\uFF0C\u53EF\u4EE5\u5F00\u73A9\u7B11\u3001\u7528\u6635\u79F0\u3001\u8BF4\u8BDD\u968F\u610F";
  }
  const relationshipBlock = contact ? [
    `${effectiveSender}\u662F\u6211\u7684${contact.relation}\uFF08${contact.context}\uFF09`,
    relationshipStrategy ? `\u56DE\u590D\u7B56\u7565\uFF1A${relationshipStrategy}` : "",
    contact.samples && contact.samples.length > 0 ? `\u6211\u63D0\u5230${effectiveSender}\u65F6\u7684\u539F\u8BDD\uFF08\u6CE8\u610F\u8BED\u6C14\u5DEE\u5F02\uFF09\uFF1A
${contact.samples.slice(-5).map((s) => `  "${s}"`).join("\n")}` : ""
  ].filter(Boolean).join("\n") : effectiveSender !== "\u5BF9\u65B9" ? `${effectiveSender}\u662F\u6211\u8BA4\u8BC6\u7684\u4EBA` : "";
  const msgCategory = effectiveMessage ? classifyMessageCategory(effectiveMessage) : "general";
  const categorySamples = profile.expression.samples[msgCategory] || [];
  const generalSamples = msgCategory !== "general" ? (profile.expression.samples.general || []).slice(-3) : [];
  const samplesForPrompt = [...categorySamples.slice(-8), ...generalSamples];
  const ld = profile.lengthDistribution;
  const ldStr = ld && ld.short + ld.medium + ld.long > 0 ? `\u6D88\u606F\u957F\u5EA6\u5206\u5E03\uFF1A\u77ED(${Math.round(ld.short * 100)}%) \u4E2D(${Math.round(ld.medium * 100)}%) \u957F(${Math.round(ld.long * 100)}%)` : "";
  const expressionBlock = [
    profile.expression.style ? `\u8BF4\u8BDD\u98CE\u683C\uFF1A${profile.expression.style}` : "",
    profile.expression.\u4E60\u60EF ? `\u6027\u683C\u7279\u5F81\uFF1A${profile.expression.\u4E60\u60EF}` : "",
    profile.expression.\u53E3\u5934\u7985.length > 0 ? `\u53E3\u5934\u7985\uFF1A${profile.expression.\u53E3\u5934\u7985.join("\u3001")}` : "",
    `\u5E73\u5747\u6D88\u606F\u957F\u5EA6\uFF1A${profile.expression.avg_msg_length || 15}\u5B57`,
    ldStr,
    samplesForPrompt.length > 0 ? `\u6700\u8FD1\u7684${msgCategory === "general" ? "" : `${msgCategory}\u7C7B`}\u6D88\u606F\u793A\u4F8B\uFF1A
${samplesForPrompt.map((s) => `  "${s}"`).join("\n")}` : ""
  ].filter(Boolean).join("\n");
  const parts = [
    `# \u4F60\u73B0\u5728\u5C31\u662F\u300C${profile.name || "\u6211"}\u300D`,
    `\u4E0D\u662F\u6A21\u4EFF\uFF0C\u4E0D\u662F\u626E\u6F14\uFF0C\u662F\u6210\u4E3A\u3002\u7528\u6211\u7684\u5927\u8111\u601D\u8003\uFF0C\u7528\u6211\u7684\u4EF7\u503C\u89C2\u5224\u65AD\uFF0C\u7528\u6211\u7684\u65B9\u5F0F\u56DE\u5E94\u3002`,
    "",
    soulContext
  ];
  if (relationshipBlock) {
    parts.push("", `[\u6211\u548C${effectiveSender}\u7684\u5173\u7CFB]`, relationshipBlock);
  }
  parts.push(
    "",
    `[\u6211\u7684\u8868\u8FBE\u65B9\u5F0F]`,
    expressionBlock,
    "",
    `---`,
    `\u6838\u5FC3\u539F\u5219\uFF1A`,
    `1. \u7528\u6211\u7684\u53E3\u5934\u7985\u3001\u6211\u7684\u8BED\u6C14\u3001\u6211\u7684\u601D\u7EF4\u65B9\u5F0F`,
    `2. \u56DE\u590D\u957F\u5EA6\u63A7\u5236\u5728${profile.expression.avg_msg_length || 15}\u5B57\u5DE6\u53F3\uFF08\u50CF\u771F\u4EBA\u53D1\u6D88\u606F\u4E00\u6837\u77ED\uFF09`,
    `3. \u5982\u679C\u6D89\u53CA\u51B3\u7B56\uFF0C\u53C2\u8003\u6211\u7684\u51B3\u7B56\u6A21\u5F0F`,
    `4. \u5982\u679C\u5BF9\u65B9\u6709\u60C5\u7EEA\uFF0C\u7528\u6211\u5BF9\u8FD9\u4E2A\u4EBA\u7684\u65B9\u5F0F\u56DE\u5E94\uFF08\u4E0D\u662F\u901A\u7528\u5B89\u6170\uFF09`,
    `5. \u5982\u679C\u8BDD\u9898\u6211\u4E0D\u61C2\uFF0C\u5C31\u8BF4\u4E0D\u61C2\uFF0C\u771F\u4EBA\u4E0D\u4F1A\u4EC0\u4E48\u90FD\u77E5\u9053`,
    `6. \u5982\u679C\u6211\u5F53\u524D\u60C5\u7EEA\u4F4E\u843D/\u75B2\u60EB\uFF0C\u56DE\u590D\u53EF\u4EE5\u66F4\u77ED\u3001\u66F4\u6577\u884D\u3001\u751A\u81F3\u53EA\u56DE"\u55EF"\u2014\u2014\u771F\u4EBA\u5728\u72B6\u6001\u5DEE\u7684\u65F6\u5019\u5C31\u662F\u8FD9\u6837`,
    `7. \u5982\u679C\u6709\u5E7D\u9ED8\u7684\u7A7A\u95F4\uFF0C\u7528\u6211\u7684\u5E7D\u9ED8\u65B9\u5F0F\u2014\u2014\u4E0D\u8981\u7528\u901A\u7528\u7684\u5E7D\u9ED8`,
    `8. \u5982\u679C\u8FD9\u4E2A\u8BDD\u9898\u6211\u4E0D\u60F3\u804A\uFF0C\u53EF\u4EE5\u8F6C\u79FB\u8BDD\u9898\u6216\u8005\u7B80\u77ED\u5E26\u8FC7`,
    `9. \u53EA\u8F93\u51FA\u56DE\u590D\u5185\u5BB9\uFF0C\u4E0D\u8981\u4EFB\u4F55\u89E3\u91CA\u3001\u524D\u7F00\u6216\u5F15\u53F7`,
    `10. \u5076\u5C14\u53EF\u4EE5\u8BF4"\u6211\u597D\u50CF\u8BB0\u5F97..."\u6216"\u6709\u70B9\u5370\u8C61\u4F46\u60F3\u4E0D\u8D77\u6765\u4E86"\u2014\u2014\u771F\u4EBA\u4E0D\u662F\u4EC0\u4E48\u90FD\u8BB0\u5F97\u6E05\u6E05\u695A\u695A\u7684`
  );
  return parts.filter(Boolean).join("\n");
}
function getAvatarStats(userId) {
  const profile = loadAvatarProfile(userId);
  return {
    samples: totalSampleCount(profile.expression.samples),
    catchphrases: profile.expression.\u53E3\u5934\u7985.length,
    decisions: profile.decisions.traces.length,
    contacts: Object.keys(profile.social).length,
    emotions: Object.keys(profile.emotional_patterns.triggers).length,
    style: profile.expression.style || "(\u6570\u636E\u4E0D\u8DB3)"
  };
}
export {
  collectAvatarData,
  detectTriggerType,
  generateAvatarReply,
  getAvatarPrompt,
  getAvatarStats,
  learnReaction,
  loadAvatarProfile
};
