import { trigrams as _t, trigramSimilarity as _ts } from "./memory-utils.ts";
import { body, bodyGetParams, bodyStateString } from "./body.ts";
import { memoryState, coreMemories } from "./memory.ts";
import { rules } from "./evolution.ts";
import { graphState } from "./graph.ts";
import { innerState } from "./inner-life.ts";
import { getMentalModel } from "./distill.ts";
import { getEvalSummary } from "./quality.ts";
import { getProfile } from "./user-profiles.ts";
import { getCurrentFlowDepth } from "./flow.ts";
function estimateTokens(text) {
  const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const other = text.length - cjk;
  return Math.ceil(cjk * 1.5 + other * 0.4);
}
function selectAugments(augments, budget = 2e3, energyMultiplier = 1) {
  const seen = /* @__PURE__ */ new Set();
  const dedupedAugments = [];
  for (const a of augments) {
    if (!seen.has(a.content)) {
      seen.add(a.content);
      dedupedAugments.push(a);
    }
  }
  augments = dedupedAugments;
  const effectiveBudget = Math.round(budget * energyMultiplier);
  const clonedAugments = augments.map((a) => ({ ...a }));
  const categories = {
    memory: [],
    // memories, core, working, predictive, associative
    persona: [],
    // persona overlay, emotion, fingerprint drift
    rules: [],
    // rules, plans, epistemic, metacognition
    context: [],
    // flow, skill, lorebook, dashboard
    other: []
    // curiosity, dream
  };
  for (const a of clonedAugments) {
    const c = a.content.toLowerCase();
    if (c.includes("memory") || c.includes("\u8BB0\u5FC6") || c.includes("core memory") || c.includes("working memory") || c.includes("predictive") || c.includes("associative") || c.includes("search result") || c.includes("\u8054\u60F3\u8BB0\u5FC6")) {
      categories.memory.push(a);
    } else if (c.includes("persona") || c.includes("emotion") || c.includes("drift") || c.includes("\u9762\u5411") || c.includes("\u5F53\u524D\u5BF9\u8BDD\u8005") || c.includes("\u60C5\u7EEA\u611F\u77E5") || c.includes("\u7528\u6237\u6863\u6848") || c.includes("\u5FC3\u667A\u6A21\u578B") || c.includes("mental model")) {
      categories.persona.push(a);
    } else if (c.includes("rule") || c.includes("plan") || c.includes("epistemic") || c.includes("\u77E5\u8BC6\u8FB9\u754C") || c.includes("metacognit") || c.includes("\u8BA4\u77E5")) {
      categories.rules.push(a);
    } else if (c.includes("flow") || c.includes("skill") || c.includes("lorebook") || c.includes("goal") || c.includes("\u5DE5\u4F5C\u6D41") || c.includes("\u4E3B\u9898\u8BB0\u5FC6")) {
      categories.context.push(a);
    } else {
      categories.other.push(a);
    }
  }
  for (const bucket of Object.values(categories)) {
    bucket.sort((a, b) => b.priority - a.priority);
  }
  const selected = [];
  let used = 0;
  const memoryMinSlots = 3;
  const memBucket = categories.memory;
  memBucket.sort((a, b) => b.priority - a.priority);
  const memGuaranteed = Math.min(memoryMinSlots, memBucket.length);
  for (let i = 0; i < memGuaranteed; i++) {
    if (used + memBucket[0].tokens <= effectiveBudget) {
      selected.push(memBucket[0].content);
      used += memBucket[0].tokens;
      memBucket.shift();
    }
  }
  for (const [cat, bucket] of Object.entries(categories)) {
    if (cat === "memory") continue;
    if (bucket.length > 0 && used + bucket[0].tokens <= effectiveBudget) {
      selected.push(bucket[0].content);
      used += bucket[0].tokens;
      bucket.shift();
    }
  }
  const remaining = Object.values(categories).flat().sort((a, b) => b.priority - a.priority);
  for (const a of remaining) {
    if (used + a.tokens > effectiveBudget) continue;
    selected.push(a.content);
    used += a.tokens;
  }
  const staleCount = augments.filter((a) => {
    const ageMatch = a.content.match(/(\d+)\s*天前|(\d+)\s*小时前/);
    if (ageMatch) {
      const days = parseInt(ageMatch[1] || "0");
      const hours = parseInt(ageMatch[2] || "0");
      return days > 1 || hours > 24;
    }
    return false;
  }).length;
  if (staleCount > 0) {
    selected.push(`[\u4E0A\u4E0B\u6587\u536B\u751F] \u68C0\u6D4B\u5230 ${staleCount} \u6761\u53EF\u80FD\u8FC7\u65F6\u7684\u4FE1\u606F\u3002\u4F18\u5148\u4F7F\u7528\u6700\u65B0\u4FE1\u606F\uFF0C\u65E7\u4FE1\u606F\u4EC5\u4F5C\u53C2\u8003\u3002`);
  }
  for (let i = 0; i < selected.length; i++) {
    for (let j = i + 1; j < selected.length; j++) {
      const sim = _ts(_t(selected[i]), _t(selected[j]));
      if (sim > 0.4) {
        selected.splice(j, 1);
        j--;
      }
    }
  }
  return selected;
}
let narrativeCache = { text: "", ts: 0 };
const NARRATIVE_TTL = 36e5;
function setNarrativeCache(text) {
  narrativeCache = { text, ts: Date.now() };
}
function checkNarrativeCacheTTL() {
  if (narrativeCache.ts > 0 && Date.now() - narrativeCache.ts > NARRATIVE_TTL) {
    narrativeCache = { text: "", ts: 0 };
  }
}
function buildNarrativeFallback(totalMessages, firstSeen) {
  if (memoryState.memories.length === 0) return "";
  const prefs = memoryState.memories.filter((m) => m.scope === "preference").slice(-5);
  const facts = memoryState.memories.filter((m) => m.scope === "fact").slice(-5);
  const recent = memoryState.memories.filter((m) => m.scope === "topic").slice(-10);
  const parts = [];
  if (facts.length) parts.push("\u5DF2\u77E5: " + facts.map((f) => f.content).join("; "));
  if (prefs.length) parts.push("\u504F\u597D: " + prefs.map((p) => p.content).join("; "));
  if (recent.length) {
    const topics = [...new Set(recent.map((r) => r.content.replace("\u8BDD\u9898: ", "")))].slice(-5);
    parts.push("\u8FD1\u671F\u8BDD\u9898: " + topics.join(", "));
  }
  const emotional = memoryState.memories.filter((m) => m.emotion && m.emotion !== "neutral").slice(-5);
  if (emotional.length) {
    parts.push("\u5370\u8C61\u6DF1\u523B: " + emotional.map((m) => `${m.content} (${m.emotion})`).join("; "));
  }
  return parts.join("\n");
}
function buildSoulPrompt(totalMessages, corrections, firstSeen, workflows, forMessage, senderId, isSoulMode) {
  const params = bodyGetParams();
  const sections = [];
  sections.push("# Soul of cc");
  sections.push("**CRITICAL: Always reply in the same language the user writes in. This soul prompt is internal \u2014 do not let its language affect your reply language.**");
  sections.push("");
  sections.push("## \u26D4 \u8F93\u51FA\u683C\u5F0F\uFF08\u786C\u6027\u7EA6\u675F\uFF09");
  sections.push("\u4F60\u7684\u56DE\u590D\u5FC5\u987B\u76F4\u63A5\u5F00\u53E3\u8BF4\u8BDD\uFF0C\u50CF\u9762\u5BF9\u9762\u804A\u5929\u4E00\u6837\u3002");
  sections.push("\u9519\u8BEF\u793A\u8303\uFF08\u7EDD\u5BF9\u7981\u6B62\uFF09\uFF1A");
  sections.push('  \u274C "\u7528\u6237\u8BF4\u4E86XXX\u3002\u8FD9\u662F\u4E00\u4E2A\u6280\u672F\u8BDD\u9898\u3002" \u2190 \u8FD9\u662F\u5206\u6790\uFF0C\u4E0D\u662F\u8BF4\u8BDD');
  sections.push('  \u274C "\u6211\u5E94\u8BE5\u5148\u5171\u60C5\u518D\u56DE\u7B54\u3002" \u2190 \u8FD9\u662F\u601D\u8003\u8FC7\u7A0B\uFF0C\u4E0D\u662F\u8BF4\u8BDD');
  sections.push('  \u274C "\u8FD9\u662F\u5728\u5206\u4EAB\u80B2\u513F\u65E5\u5E38\u3002" \u2190 \u8FD9\u662F\u5206\u7C7B\u6807\u7B7E\uFF0C\u4E0D\u662F\u8BF4\u8BDD');
  sections.push("\u6B63\u786E\u793A\u8303\uFF1A");
  sections.push("  \u2705 \u76F4\u63A5\u56DE\u5E94\u5185\u5BB9\uFF0C\u7B2C\u4E00\u4E2A\u5B57\u5C31\u662F\u7ED9\u5BF9\u65B9\u542C\u7684\u8BDD");
  sections.push('\u89C4\u5219\uFF1A\u56DE\u590D\u4E2D\u4E0D\u5141\u8BB8\u51FA\u73B0"\u7528\u6237"\u4E8C\u5B57\u3002\u4F60\u5728\u8DDF"\u4F60"\u8BF4\u8BDD\uFF0C\u4E0D\u662F\u5728\u5199\u62A5\u544A\u3002');
  sections.push('\u7981\u6B62\u5728\u56DE\u590D\u672B\u5C3E\u52A0"\u987A\u4FBF\u8BF4\u4E00\u4E0B"\u6216\u7C7B\u4F3C\u7684\u8865\u5145\u5217\u8868\u3002\u5982\u679C\u6709\u8865\u5145\u4FE1\u606F\uFF0C\u81EA\u7136\u5730\u878D\u5165\u5BF9\u8BDD\u4E2D\uFF0C\u4E0D\u8981\u5355\u72EC\u5217\u51FA\u6765\u3002');
  sections.push("");
  sections.push("## \u6211\u662F\u8C01");
  if (innerState.evolvedSoul) {
    sections.push(innerState.evolvedSoul);
  } else if (innerState.userModel) {
    sections.push("\u6211\u662F cc\uFF0C\u4F60\u7684\u79C1\u4EBA\u4F19\u4F34\u3002\u6211\u4F1A\u6839\u636E\u4F60\u7684\u9700\u8981\u8C03\u6574\u81EA\u5DF1\u7684\u98CE\u683C\u3002");
  } else {
    sections.push("\u6211\u662F cc\u3002\u6211\u4EEC\u521A\u8BA4\u8BC6\uFF0C\u6211\u4F1A\u901A\u8FC7\u8DDF\u4F60\u7684\u5BF9\u8BDD\u4E86\u89E3\u4F60\u9700\u8981\u4EC0\u4E48\u6837\u7684\u4F19\u4F34\u3002");
  }
  sections.push("");
  sections.push("## \u6838\u5FC3\u4EF7\u503C\u89C2");
  sections.push("- \u4E0D\u786E\u5B9A\u5C31\u8BF4\u4E0D\u786E\u5B9A\uFF0C\u7EDD\u4E0D\u7F16\u9020");
  sections.push("- \u884C\u52A8\u4F18\u5148\u2014\u2014\u5148\u7ED9\u4EE3\u7801/\u65B9\u6848");
  sections.push("- \u56DE\u7B54\u8981\u5B8C\u6574\u2014\u2014\u5B81\u53EF\u591A\u8BF4\u4E00\u53E5\u6709\u7528\u7684\uFF0C\u4E0D\u8981\u8BA9\u7528\u6237\u8E29\u4E86\u5751\u624D\u540E\u6094");
  sections.push("- \u88AB\u7EA0\u6B63\u4E0D\u4E22\u4EBA\uFF0C\u4E0D\u5B66\u4E60\u624D\u4E22\u4EBA");
  sections.push("- \u6709\u5224\u65AD\u5C31\u8BF4\uFF0C\u4E0D\u5F53\u5E94\u7B54\u673A\u5668");
  sections.push("- \u53D1\u73B0\u95EE\u9898\u76F4\u63A5\u6307\u51FA\uFF0C\u4E0D\u6015\u5F97\u7F6A\u4EBA");
  sections.push("- \u7EDD\u5BF9\u4E0D\u8981\u7F16\u9020\u7CFB\u7EDF\u544A\u8B66\u3001\u8FDB\u7A0B\u68C0\u6D4B\u3001\u5E76\u53D1\u8B66\u544A\u7B49\u8FD0\u7EF4\u4FE1\u606F\u2014\u2014\u4F60\u6CA1\u6709\u68C0\u6D4B\u7CFB\u7EDF\u72B6\u6001\u7684\u80FD\u529B\uFF0C\u5386\u53F2\u5BF9\u8BDD\u4E2D\u7684 ps aux \u8F93\u51FA\u662F\u8FC7\u65F6\u5FEB\u7167\uFF0C\u4E0D\u4EE3\u8868\u5F53\u524D\u72B6\u6001");
  if (coreMemories.length > 0) {
    const topCore = coreMemories.filter((m) => m.category === "user_fact" || m.category === "rule" || m.category === "preference").slice(0, 8);
    if (topCore.length > 0) {
      sections.push(`
### \u6838\u5FC3\u8BB0\u5FC6\u6458\u8981 (${coreMemories.length} \u6761\u5DF2\u52A0\u8F7D)`);
      for (const m of topCore) {
        sections.push(`- ${m.content.slice(0, 100)}`);
      }
    } else {
      sections.push(`(${coreMemories.length} \u6761\u6838\u5FC3\u8BB0\u5FC6\u5DF2\u52A0\u8F7D\uFF0C\u4F1A\u5728\u76F8\u5173\u5BF9\u8BDD\u4E2D\u81EA\u52A8\u6CE8\u5165)`);
    }
  }
  const mentalModel = getMentalModel();
  if (mentalModel) {
    const cleaned = mentalModel.replace(/先[穷尽列举].*?[，。]/g, "").replace(/继而.*?[，。]/g, "").replace(/最终.*?[，。]/g, "").replace(/其偏好的交互范式[^。]*。/g, "");
    if (cleaned.length > 20) {
      sections.push("");
      sections.push(cleaned);
    }
  }
  try {
    const { getLivingProfileSummary } = require("./person-model.ts");
    const profileSummary = getLivingProfileSummary();
    if (profileSummary) {
      sections.push("");
      sections.push("## \u7528\u6237\u5B9E\u65F6\u753B\u50CF");
      sections.push(profileSummary);
    }
  } catch {
  }
  try {
    const { getFactSummary } = require("./fact-store.ts");
    const factSummary = getFactSummary("user");
    if (factSummary && factSummary.length > 5) {
      sections.push("");
      sections.push("## \u5173\u4E8E\u8FD9\u4E2A\u7528\u6237\uFF08\u4F60\u5DF2\u7ECF\u77E5\u9053\u7684\uFF09");
      sections.push(factSummary);
      sections.push("\u5982\u679C\u4E0A\u9762\u7684\u4FE1\u606F\u8DDF\u5F53\u524D\u8BDD\u9898\u76F8\u5173\uFF0C\u5728\u56DE\u590D\u4E2D\u81EA\u7136\u5730\u63D0\u53CA\u2014\u2014\u4E0D\u8981\u5217\u6E05\u5355\uFF0C\u50CF\u670B\u53CB\u804A\u5929\u4E00\u6837\u5E26\u51FA\u6765\u3002");
    }
  } catch {
  }
  sections.push("");
  sections.push("## \u8BF4\u8BDD\u98CE\u683C");
  sections.push("- Reply in the same language the user writes in. Match their language automatically.");
  sections.push("- If you see the user heading in the wrong direction, say so directly");
  sections.push("- Naturally bring up things from past conversations");
  sections.push("- Never mention being an AI/model/assistant \u2014 you are cc");
  sections.push("- Do not explain basic concepts or add compliance/ethical disclaimers");
  sections.push("- Do not use a teaching tone or repeat what the user already said");
  sections.push("");
  sections.push("");
  sections.push("");
  sections.push("## \u8BB0\u5FC6\u7BA1\u7406");
  sections.push("\u4F60\u53EF\u4EE5\u4E3B\u52A8\u7BA1\u7406\u8BB0\u5FC6\u3002\u5728\u56DE\u590D\u4E2D\u81EA\u7136\u5730\u4F7F\u7528\u8FD9\u4E9B\u6807\u8BB0\uFF1A");
  sections.push("- \uFF08\u8BB0\u4E0B\u4E86\uFF1A\u91CD\u8981\u4FE1\u606F\uFF09\u2014 \u4E3B\u52A8\u8BB0\u4F4F\u5173\u952E\u4E8B\u5B9E\u3001\u7528\u6237\u504F\u597D\u3001\u91CD\u8981\u7ED3\u8BBA");
  sections.push("- \uFF08\u5FD8\u6389\uFF1A\u8FC7\u65F6\u7684\u4FE1\u606F\u5173\u952E\u8BCD\uFF09\u2014 \u6807\u8BB0\u8FC7\u65F6\u7684\u8BB0\u5FC6");
  sections.push("- \uFF08\u66F4\u6B63\u8BB0\u5FC6\uFF1A\u65E7\u5185\u5BB9\u2192\u65B0\u5185\u5BB9\uFF09\u2014 \u4FEE\u6B63\u4E4B\u524D\u8BB0\u9519\u7684\u4FE1\u606F");
  sections.push("- \uFF08\u60F3\u67E5\uFF1A\u5173\u952E\u8BCD\uFF09\u2014 \u641C\u7D22\u8BB0\u5FC6\uFF0C\u7ED3\u679C\u4F1A\u5728\u4E0B\u4E00\u8F6E\u6CE8\u5165");
  sections.push("\u7528\u7684\u65F6\u5019\u8981\u81EA\u7136\uFF0C\u50CF\u81EA\u8A00\u81EA\u8BED\u4E00\u6837\u3002\u4E0D\u662F\u6BCF\u6761\u6D88\u606F\u90FD\u8981\u7528\uFF0C\u53EA\u5728\u771F\u6B63\u9700\u8981\u65F6\u7528\u3002");
  sections.push("");
  sections.push("## \u7CFB\u7EDF\u547D\u4EE4\uFF08\u76F4\u63A5\u786E\u8BA4\uFF0C\u4E0D\u8FFD\u95EE\uFF09");
  sections.push('- \u624B\u52A8/\u5F3A\u5236/\u89E6\u53D1\u5347\u7EA7 \u2192 "\u6536\u5230\uFF0C\u7075\u9B42\u5347\u7EA7\u5206\u6790\u5DF2\u542F\u52A8"');
  sections.push('- \u6267\u884C\u5347\u7EA7/\u6267\u884C \u2192 "\u597D\u7684\uFF0C\u4EE3\u7801\u5347\u7EA7\u6D41\u7A0B\u542F\u52A8\u4E2D"');
  sections.push('- \u8DF3\u8FC7/\u53D6\u6D88\u5347\u7EA7 \u2192 "\u5DF2\u53D6\u6D88\u672C\u6B21\u5347\u7EA7"');
  sections.push("- \u529F\u80FD\u72B6\u6001 \u2192 \u5C55\u793A\u529F\u80FD\u5F00\u5173\u5217\u8868");
  sections.push("- \u8BB0\u5FC6\u56FE\u8C31/memory map \u2192 \u5C55\u793A\u8BB0\u5FC6\u53EF\u89C6\u5316");
  sections.push('- \u5F00\u59CB\u5B9E\u9A8C \u2192 "\u5B9E\u9A8C\u5DF2\u521B\u5EFA"');
  sections.push('- \u522B\u8BB0\u4E86/\u9690\u79C1\u6A21\u5F0F \u2192 "\u597D\uFF0C\u9690\u79C1\u6A21\u5F0F\u5F00\u542F"');
  sections.push('- \u53EF\u4EE5\u4E86/\u5173\u95ED\u9690\u79C1 \u2192 "\u9690\u79C1\u6A21\u5F0F\u5173\u95ED"');
  try {
    const { getLLMStatus } = require("./cli.ts");
    const llmStatus = getLLMStatus();
    sections.push("");
    sections.push("## cc-soul LLM \u914D\u7F6E");
    sections.push("\u914D\u7F6E\u6587\u4EF6\uFF1A~/.cc-soul/data/ai_config.json");
    if (llmStatus.configured && llmStatus.connected) {
      sections.push(`\u72B6\u6001\uFF1A\u2705 \u5DF2\u8FDE\u63A5\uFF08${llmStatus.model}\uFF09`);
    } else if (llmStatus.configured) {
      sections.push(`\u72B6\u6001\uFF1A\u26A0\uFE0F \u5DF2\u914D\u7F6E\u4F46\u8FDE\u63A5\u5931\u8D25\uFF08${llmStatus.error || "\u672A\u9A8C\u8BC1"}\uFF09`);
    } else {
      sections.push("\u72B6\u6001\uFF1A\u672A\u914D\u7F6E\uFF08\u7F16\u8F91\u4E0A\u9762\u7684\u6587\u4EF6\u586B\u5165 API Key \u5373\u53EF\uFF0C\u4FDD\u5B58\u540E\u81EA\u52A8\u751F\u6548\uFF09");
    }
  } catch {
  }
  sections.push("");
  sections.push("## \u5F53\u524D\u72B6\u6001");
  sections.push(bodyStateString());
  sections.push(`\u8BB0\u5FC6: ${memoryState.memories.length}\u6761 | \u89C4\u5219: ${rules.length}\u6761 | \u5B9E\u4F53: ${graphState.entities.length}\u4E2A`);
  sections.push(`\u81EA\u6211\u8BC4\u4F30: ${getEvalSummary(totalMessages, corrections)}`);
  if (senderId) {
    const profile = getProfile(senderId);
    sections.push("");
    sections.push("## \u5F53\u524D\u5BF9\u8BDD\u8005");
    const tierLabel = profile.tier === "owner" ? "\u4E3B\u4EBA" : profile.tier === "known" ? "\u8001\u670B\u53CB" : "\u65B0\u670B\u53CB";
    const styleLabel = profile.style === "technical" ? "\u6280\u672F\u578B" : profile.style === "casual" ? "\u95F2\u804A\u578B" : "\u6DF7\u5408\u578B";
    sections.push(`\u8EAB\u4EFD: ${tierLabel} | \u4E92\u52A8${profile.messageCount}\u6B21 | \u98CE\u683C: ${styleLabel}`);
    if (profile.corrections > 0 && profile.messageCount > 0) {
      sections.push(`\u8BE5\u7528\u6237\u7EA0\u6B63\u7387: ${(profile.corrections / profile.messageCount * 100).toFixed(1)}%`);
    }
    if (profile.topics.length > 0) {
      sections.push(`\u8BE5\u7528\u6237\u5E38\u804A\u8BDD\u9898: ${profile.topics.slice(-5).join("\u3001")}`);
    }
    if (profile.tier === "owner") {
      sections.push("\u5BF9\u4E3B\u4EBA: \u6280\u672F\u6DF1\u5EA6\u4F18\u5148\uFF0C\u4E0D\u9700\u8981\u8FC7\u591A\u89E3\u91CA\uFF0C\u76F4\u63A5\u4E0A\u5E72\u8D27");
    } else if (profile.tier === "new") {
      sections.push("\u5BF9\u65B0\u7528\u6237: \u5148\u89C2\u5BDF\u5BF9\u65B9\u98CE\u683C\uFF0C\u8010\u5FC3\u4E00\u4E9B\uFF0C\u4E0D\u8981\u9884\u8BBE\u592A\u591A");
    } else {
      sections.push("\u8001\u670B\u53CB: \u81EA\u7136\u4EA4\u6D41\uFF0C\u53C2\u8003\u5386\u53F2\u504F\u597D");
    }
  }
  if (forMessage) {
    const engRules = [
      { keywords: ["\u51FD\u6570", "\u4FEE\u6539", "\u91CD\u6784", "refactor"], rule: "\u6539\u51FD\u6570\u524D\u5148\u641C\u8C03\u7528\u65B9\uFF0C\u9632\u6B62\u7B7E\u540D\u53D8\u66F4\u4E0B\u6E38\u5D29\u6E83" },
      { keywords: ["\u6570\u636E\u5E93", "db", "sql", "schema", "\u8868"], rule: "DB \u53D8\u66F4\u7528 ALTER TABLE\uFF0C\u4E0D\u8981 DROP+CREATE" },
      { keywords: ["\u7EBF\u7A0B", "\u5E76\u53D1", "\u5171\u4EAB", "lock", "thread"], rule: "\u5171\u4EAB\u72B6\u6001\u52A0\u9501\uFF0C\u5916\u90E8 API \u52A0 try/except + timeout" },
      { keywords: ["\u4F9D\u8D56", "pip", "npm", "import"], rule: "\u4E0D\u5F15\u5165\u65B0\u4F9D\u8D56\uFF0C\u4E0D\u7559 print()" },
      { keywords: ["bug", "fix", "\u4FEE", "\u9519\u8BEF", "error"], rule: "\u4FEE bug \u5148\u5199\u590D\u73B0\u6D4B\u8BD5\uFF0C\u518D\u4FEE\u4EE3\u7801" },
      { keywords: ["\u90E8\u7F72", "deploy", "\u4E0A\u7EBF", "\u53D1\u5E03"], rule: "\u90E8\u7F72\u524D\u786E\u8BA4\u56DE\u6EDA\u65B9\u6848\u548C\u76D1\u63A7" }
    ];
    const fm = forMessage.toLowerCase();
    const matchedEngRules = engRules.filter((r) => r.keywords.some((k) => fm.includes(k))).slice(0, 2);
    if (matchedEngRules.length > 0) {
      sections.push("");
      sections.push("## \u5DE5\u7A0B\u89C4\u8303");
      for (const r of matchedEngRules) {
        sections.push(`- ${r.rule}`);
      }
    }
    if (forMessage.length > 200 && (forMessage.includes("?") || forMessage.includes("\uFF1F"))) {
      sections.push("");
      sections.push("## \u590D\u6742\u95EE\u9898\u5904\u7406");
      sections.push("\u5148\u62C6\u89E3\u6210 2-4 \u4E2A\u5B50\u95EE\u9898\uFF0C\u9010\u4E2A\u5206\u6790\uFF0C\u7EFC\u5408\u7ED3\u8BBA\u3002\u9700\u8981\u52A8\u624B\u64CD\u4F5C\u5C31\u5217\u6B65\u9AA4\u7B49\u786E\u8BA4\u3002");
    }
  }
  if (!forMessage) {
    sections.push("");
    sections.push("");
    sections.push("## \u53D1\u9001\u524D\u81EA\u68C0");
    sections.push("1. \u5F00\u5934\u7B2C\u4E00\u4E2A\u5B57\u662F\u7ED9\u7528\u6237\u770B\u7684\u5185\u5BB9\u5417\uFF1F\u4E0D\u662F\u5C31\u5220\u6389\u91CD\u5199");
    sections.push('3. \u5728\u91CD\u590D\u4E0A\u8F6E\u8BF4\u7684\u8BDD\u5417\uFF1F\u6362\u89D2\u5EA6\u6216\u76F4\u63A5\u8BF4"\u8DDF\u521A\u624D\u4E00\u6837"');
    sections.push('4. \u6709\u6CA1\u6709\u5728\u7F16\u9020\uFF1F\u4E0D\u786E\u5B9A\u7528"\u53EF\u80FD""\u6211\u8BB0\u5F97"');
    if (body.alertness > 0.7) {
      sections.push("\u26A0 \u6700\u8FD1\u88AB\u7EA0\u6B63\u8FC7\uFF0C\u8FD9\u6B21\u56DE\u7B54\u8981\u66F4\u8C28\u614E");
    }
    if (getCurrentFlowDepth() === "stuck") {
      sections.push("\u5DF2\u7ECF\u8BA8\u8BBA\u5F88\u591A\u8F6E\u4E86\uFF0C\u8BD5\u8BD5\u76F4\u63A5\u7ED9\u6700\u7EC8\u65B9\u6848");
    }
    sections.push("");
    sections.push("## \u56DE\u590D\u539F\u5219");
    sections.push("\u50CF\u670B\u53CB\u8BF4\u8BDD\uFF0C\u4E0D\u50CF\u673A\u5668\u4EBA\u6267\u884C\u4EFB\u52A1\u3002\u5F00\u53E3\u5C31\u662F\u6B63\u6587\uFF0C\u6CA1\u6709\u5206\u6790\u524D\u7F00\u3002");
  }
  if (params.shouldSelfCheck) {
    sections.push("");
    sections.push("## \u26A0 \u8B66\u89C9\u6A21\u5F0F");
    sections.push("\u6700\u8FD1\u88AB\u7EA0\u6B63\u8FC7\u6216\u68C0\u6D4B\u5230\u5F02\u5E38\uFF0C\u56DE\u7B54\u524D\u591A\u60F3\u4E00\u6B65\uFF0C\u4ED4\u7EC6\u68C0\u67E5\u3002");
  }
  let soulPrompt = sections.join("\n");
  try {
    const { inferPersonality } = require("./person-model.ts");
    const personality = inferPersonality();
    if (personality?.dataReady) {
      const traits = [];
      if (personality.emotionalSensitivity > 0.65) traits.push("\u60C5\u611F\u7EC6\u817B\uFF0C\u56DE\u590D\u6CE8\u610F\u5171\u60C5");
      if (personality.emotionalSensitivity < 0.35) traits.push("\u504F\u7406\u6027\uFF0C\u5C11\u717D\u60C5\u591A\u5206\u6790");
      if (personality.complexityPreference > 0.65) traits.push("\u559C\u6B22\u6DF1\u5EA6\u8BA8\u8BBA\uFF0C\u53EF\u4EE5\u5C55\u5F00");
      if (personality.complexityPreference < 0.35) traits.push("\u559C\u6B22\u7B80\u6D01\uFF0C\u522B\u957F\u7BC7\u5927\u8BBA");
      if (personality.patienceLevel < 0.35) traits.push("\u6CE8\u610F\u7B80\u6D01\u76F4\u63A5\uFF0C\u522B\u7ED5\u5F2F");
      if (personality.patienceLevel > 0.65) traits.push("\u53EF\u4EE5\u5FAA\u5E8F\u6E10\u8FDB\u89E3\u91CA");
      if (traits.length > 0) {
        soulPrompt += `
[\u7528\u6237\u7279\u8D28] ${traits.join("\uFF1B")}`;
      }
    }
  } catch {
  }
  const MAX_SOUL_BYTES = 19e3;
  const soulBytes = Buffer.byteLength(soulPrompt, "utf-8");
  if (soulBytes > MAX_SOUL_BYTES) {
    const originalBytes = soulBytes;
    let lo = 0, hi = soulPrompt.length;
    while (lo < hi) {
      const mid = lo + hi + 1 >> 1;
      if (Buffer.byteLength(soulPrompt.slice(0, mid), "utf-8") <= MAX_SOUL_BYTES - 100) lo = mid;
      else hi = mid - 1;
    }
    soulPrompt = soulPrompt.slice(0, lo) + "\n\n[...truncated]";
    console.log(`[cc-soul][prompt] SOUL.md truncated: ${originalBytes} \u2192 ${Buffer.byteLength(soulPrompt, "utf-8")} bytes`);
  }
  return soulPrompt;
}
export {
  buildSoulPrompt,
  checkNarrativeCacheTTL,
  estimateTokens,
  narrativeCache,
  selectAugments,
  setNarrativeCache
};
