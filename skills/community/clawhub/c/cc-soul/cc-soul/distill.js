import { resolve } from "path";
import { DATA_DIR, loadJson } from "./persistence.ts";
import { memoryState, addMemory } from "./memory.ts";
import { spawnCLI } from "./cli.ts";
import { logDecision } from "./decision-log.ts";
import { WORD_PATTERN } from "./memory-utils.ts";
import { detectPolarityFlip } from "./memory-utils.ts";
const MENTAL_MODELS_PATH = resolve(DATA_DIR, "mental_models.json");
const TOPIC_NODES_PATH = resolve(DATA_DIR, "topic_nodes.json");
const DISTILL_STATE_PATH = resolve(DATA_DIR, "distill_state.json");
const L1_TO_L2_BASE = 6 * 36e5;
const L2_TO_L3_BASE = 12 * 36e5;
const L3_REFRESH_BASE = 24 * 36e5;
const L1_TO_L2_COOLDOWN = L1_TO_L2_BASE;
const L2_TO_L3_COOLDOWN = L2_TO_L3_BASE;
const L3_REFRESH_COOLDOWN = L3_REFRESH_BASE;
const MIN_MEMORIES_FOR_DISTILL = 20;
const MAX_TOPIC_NODES = 80;
const MAX_MODEL_LENGTH = 600;
let topicNodes = [];
let mentalModels = /* @__PURE__ */ new Map();
let distillState = { lastL1toL2: 0, lastL2toL3: 0, lastL3Refresh: 0, totalDistills: 0 };
function loadDistillState() {
  let sqlMod = null;
  try {
    sqlMod = require("./sqlite-store.ts");
  } catch {
  }
  if (sqlMod?.dbLoadTopicNodes) {
    const dbNodes = sqlMod.dbLoadTopicNodes();
    if (dbNodes.length > 0) {
      topicNodes = dbNodes;
    } else {
      topicNodes = loadJson(TOPIC_NODES_PATH, []);
      for (const n of topicNodes) {
        try {
          sqlMod.dbSaveTopicNode(n);
        } catch {
        }
      }
    }
  } else {
    topicNodes = loadJson(TOPIC_NODES_PATH, []);
  }
  if (sqlMod?.dbLoadDistillState) {
    distillState = sqlMod.dbLoadDistillState(distillState);
  } else {
    distillState = loadJson(DISTILL_STATE_PATH, distillState);
  }
  if (sqlMod?.dbLoadMentalModels) {
    const dbModels = sqlMod.dbLoadMentalModels();
    if (dbModels.size > 0) {
      mentalModels = dbModels;
    } else {
      const raw = loadJson(MENTAL_MODELS_PATH, {});
      mentalModels.clear();
      for (const [id, m] of Object.entries(raw)) {
        mentalModels.set(id, m);
        try {
          sqlMod.dbSaveMentalModel(m);
        } catch {
        }
      }
    }
  } else {
    const raw = loadJson(MENTAL_MODELS_PATH, {});
    mentalModels.clear();
    for (const [id, m] of Object.entries(raw)) {
      mentalModels.set(id, m);
    }
  }
  console.log(`[cc-soul][distill] loaded: ${topicNodes.length} topics, ${mentalModels.size} mental models`);
}
function saveTopicNodes() {
  let sqlMod = null;
  try {
    sqlMod = require("./sqlite-store.ts");
  } catch {
  }
  if (sqlMod?.dbSaveTopicNode) {
    for (const n of topicNodes) {
      try {
        sqlMod.dbSaveTopicNode(n);
      } catch {
      }
    }
  }
}
function saveMentalModels() {
  let sqlMod = null;
  try {
    sqlMod = require("./sqlite-store.ts");
  } catch {
  }
  if (sqlMod?.dbSaveMentalModel) {
    for (const [_, m] of mentalModels) {
      try {
        sqlMod.dbSaveMentalModel(m);
      } catch {
      }
    }
  }
}
function saveDistillState_() {
  let sqlMod = null;
  try {
    sqlMod = require("./sqlite-store.ts");
  } catch {
  }
  if (sqlMod?.dbSaveDistillState) {
    try {
      sqlMod.dbSaveDistillState(distillState);
    } catch {
    }
  }
}
function distillL1toL2() {
  const now = Date.now();
  if (now - distillState.lastL1toL2 < L1_TO_L2_COOLDOWN) return;
  const MIN_SESSIONS_FOR_DISTILL = 3;
  try {
    const { getSessionState, getLastActiveSessionKey } = require("./handler-state.ts");
    const sess = getSessionState(getLastActiveSessionKey());
    const sessionCount = sess?.sessionCount ?? sess?.turnCount ?? 0;
    if (sessionCount < MIN_SESSIONS_FOR_DISTILL) return;
  } catch {
  }
  distillState.lastL1toL2 = now;
  const active = memoryState.memories.filter(
    (m) => m.scope !== "expired" && m.scope !== "archived" && m.scope !== "decayed" && m.content.length > 10
  );
  if (active.length < MIN_MEMORIES_FOR_DISTILL) return;
  const byUser = /* @__PURE__ */ new Map();
  for (const m of active) {
    const key = m.userId || "_global";
    if (!byUser.has(key)) byUser.set(key, []);
    byUser.get(key).push(m);
  }
  let cliCallsThisRound = 0;
  const MAX_CLI_PER_DISTILL = 8;
  const unclusteredByUser = /* @__PURE__ */ new Map();
  for (const [userId, memories] of byUser) {
    if (memories.length < 5) continue;
    if (cliCallsThisRound >= MAX_CLI_PER_DISTILL) break;
    const clusters = clusterByKeywords(memories);
    const clusteredSet = /* @__PURE__ */ new Set();
    for (const cl of clusters) {
      if (cl.length >= 2) for (const m of cl) clusteredSet.add(m.content);
    }
    const unc = memories.filter((m) => !clusteredSet.has(m.content));
    if (unc.length > 0) unclusteredByUser.set(userId, unc);
    clusters.sort((a, b) => {
      const emotionScore = (cluster) => cluster.reduce((sum, m) => {
        const w = m.emotion === "important" || m.emotion === "warm" ? 1.5 : m.emotion === "painful" ? 1.3 : 1;
        return sum + w;
      }, 0);
      return emotionScore(b) - emotionScore(a);
    });
    for (const cluster of clusters) {
      if (cluster.length < 2) continue;
      if (cliCallsThisRound >= MAX_CLI_PER_DISTILL) break;
      const clusterText = cluster.map((m) => m.content.slice(0, 80)).join("\n");
      const existingNode = topicNodes.find(
        (n) => n.userId === (userId === "_global" ? void 0 : userId) && keywordOverlap(n.topic, clusterText) > 0.3
      );
      if (existingNode && now - existingNode.lastUpdated < L1_TO_L2_COOLDOWN) continue;
      const zeroLLMResult = zeroLLMDistill(cluster.map((m) => m.content));
      if (zeroLLMResult && zeroLLMResult.length > 10) {
        const topicName = cluster[0].content.slice(0, 10).replace(/[，。！？\s]+$/, "") || "\u672A\u5206\u7C7B";
        const node = {
          topic: topicName.slice(0, 20),
          summary: zeroLLMResult.slice(0, 200),
          sourceCount: cluster.length,
          lastUpdated: Date.now(),
          userId: userId === "_global" ? void 0 : userId
        };
        if (existingNode) {
          existingNode.topic = node.topic;
          existingNode.summary = node.summary;
          existingNode.sourceCount += cluster.length;
          existingNode.lastUpdated = node.lastUpdated;
        } else {
          topicNodes.push(node);
          if (topicNodes.length > MAX_TOPIC_NODES) {
            topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated);
            topicNodes.length = MAX_TOPIC_NODES;
          }
        }
        saveTopicNodes();
        console.log(`[cc-soul][distill] L1\u2192L2 (zero-LLM): "${node.topic}" (${cluster.length} memories \u2192 1 node)`);
        continue;
      }
      const prompt = [
        "\u5C06\u4EE5\u4E0B\u8BB0\u5FC6\u7247\u6BB5\u84B8\u998F\u4E3A\u4E00\u4E2A\u4E3B\u9898\u8282\u70B9\u3002\u683C\u5F0F\uFF1A",
        "\u4E3B\u9898: <2-6\u5B57\u7684\u4E3B\u9898\u540D>",
        "\u6458\u8981: <1-2\u53E5\u8BDD\u7684\u6838\u5FC3\u7406\u89E3\uFF0C\u4E0D\u8D85\u8FC7100\u5B57>",
        "",
        "\u8BB0\u5FC6\u7247\u6BB5:",
        ...cluster.slice(0, 15).map((m) => `- ${m.content.slice(0, 120)}`)
      ].join("\n");
      cliCallsThisRound++;
      spawnCLI(prompt, (output) => {
        if (!output || output.length < 10) return;
        const topicMatch = output.match(/主题[:：]\s*(.+?)(?:\n|$)/);
        const summaryMatch = output.match(/摘要[:：]\s*(.+?)(?:\n|$)/);
        if (!topicMatch || !summaryMatch) return;
        const node = {
          topic: topicMatch[1].trim().slice(0, 20),
          summary: summaryMatch[1].trim().slice(0, 200),
          sourceCount: cluster.length,
          lastUpdated: Date.now(),
          userId: userId === "_global" ? void 0 : userId
        };
        if (existingNode) {
          existingNode.topic = node.topic;
          existingNode.summary = node.summary;
          existingNode.sourceCount += cluster.length;
          existingNode.lastUpdated = node.lastUpdated;
        } else {
          topicNodes.push(node);
          if (topicNodes.length > MAX_TOPIC_NODES) {
            topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated);
            topicNodes.length = MAX_TOPIC_NODES;
          }
        }
        saveTopicNodes();
        console.log(`[cc-soul][distill] L1\u2192L2: "${node.topic}" (${cluster.length} memories \u2192 1 node)`);
      });
    }
  }
  for (const [userId, unclustered] of unclusteredByUser) {
    const uid = userId === "_global" ? void 0 : userId;
    const orphans = distillState.orphanMemoryContents ??= [];
    for (const m of unclustered) {
      const matched = assignMemoryToNode(m.content, topicNodes, uid);
      if (matched) {
        matched.sourceCount++;
        matched.lastUpdated = now;
      } else {
        if (!orphans.includes(m.content.slice(0, 200))) {
          orphans.push(m.content.slice(0, 200));
          distillState.orphanAccumulatedAt ??= now;
        }
      }
    }
    if (orphans.length >= 5) {
      const PMI_THRESHOLD = 0.5;
      const viable = clusterOrphansByPMI(orphans, PMI_THRESHOLD);
      for (const oc of viable) {
        const topicName = oc[0].slice(0, 10).replace(/[，。！？\s]+$/, "") || "\u672A\u5206\u7C7B";
        const summary = zeroLLMDistill(oc) || oc.map((s) => s.slice(0, 40)).join("\uFF1B");
        topicNodes.push({
          topic: topicName.slice(0, 20),
          summary: summary.slice(0, 200),
          sourceCount: oc.length,
          lastUpdated: now,
          userId: uid
        });
        for (const content of oc) {
          const idx = orphans.indexOf(content);
          if (idx >= 0) orphans.splice(idx, 1);
        }
      }
      if (orphans.length >= 20) {
        const topicName = "\u6742\u9879\u8BDD\u9898";
        const summary = zeroLLMDistill(orphans.slice(0, 15)) || orphans.slice(0, 5).map((s) => s.slice(0, 30)).join("\uFF1B");
        topicNodes.push({
          topic: topicName,
          summary: summary.slice(0, 200),
          sourceCount: orphans.length,
          lastUpdated: now,
          userId: uid
        });
        orphans.length = 0;
        distillState.orphanAccumulatedAt = void 0;
        console.log(`[cc-soul][distill] PMI orphans force-grouped into fallback node`);
      }
      if (topicNodes.length > MAX_TOPIC_NODES) {
        topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated);
        topicNodes.length = MAX_TOPIC_NODES;
      }
      saveTopicNodes();
    }
  }
  distillState.totalDistills++;
  saveDistillState_();
}
const SECTION_COOLDOWNS = {
  identity: 7 * 864e5,
  // 7 天
  style: 3 * 864e5,
  // 3 天
  facts: 864e5,
  // 1 天
  dynamics: 3 * 36e5
  // 3 小时
};
const SECTION_PROMPTS = {
  identity: { name: "\u8EAB\u4EFD", desc: "\u8EAB\u4EFD\u3001\u804C\u4E1A\u3001\u6280\u672F\u6808\u3001\u4E13\u4E1A\u80CC\u666F" },
  style: { name: "\u6C9F\u901A\u98CE\u683C", desc: "\u6C9F\u901A\u504F\u597D\u3001\u8BF4\u8BDD\u98CE\u683C\u3001\u96F7\u533A\u3001\u559C\u597D" },
  facts: { name: "\u5173\u952E\u4E8B\u5B9E", desc: "\u7A33\u5B9A\u504F\u597D\u3001\u4E60\u60EF\u3001\u5BB6\u5EAD\u60C5\u51B5\u3001\u957F\u671F\u76EE\u6807" },
  dynamics: { name: "\u8FD1\u671F\u72B6\u6001", desc: "\u5F53\u524D\u60C5\u7EEA\u57FA\u7EBF\u3001\u6B63\u5728\u5173\u6CE8\u7684\u8BDD\u9898/\u9879\u76EE\u3001\u8FD1\u671F\u884C\u4E3A\u53D8\u5316" }
};
const DYNAMICS_STALE_THRESHOLD = 14 * 864e5;
function distillL2toL3() {
  const now = Date.now();
  distillState.lastL2toL3 = now;
  const userIds = /* @__PURE__ */ new Set();
  for (const n of topicNodes) {
    if (n.userId) userIds.add(n.userId);
  }
  for (const m of memoryState.memories) {
    if (m.userId && m.scope !== "expired") userIds.add(m.userId);
  }
  userIds.add("_global");
  let cliCalls = 0;
  const MAX_CLI_L3 = 4;
  for (const userId of userIds) {
    if (cliCalls >= MAX_CLI_L3) break;
    const isGlobal = userId === "_global";
    const userTopics = topicNodes.filter((n) => isGlobal ? !n.userId : n.userId === userId);
    const userMems = memoryState.memories.filter(
      (m) => (isGlobal ? !m.userId : m.userId === userId) && m.scope !== "expired" && m.scope !== "archived" && (m.scope === "preference" || m.scope === "correction" || m.scope === "fact" || m.scope === "consolidated")
    ).slice(-20);
    if (userTopics.length === 0 && userMems.length < 3) continue;
    const existing = mentalModels.get(userId);
    if (existing && !existing.sections) {
      existing.sections = {
        identity: existing.model.slice(0, 150),
        style: "",
        facts: "",
        dynamics: ""
      };
      existing.sectionUpdated = {
        identity: 0,
        style: 0,
        facts: 0,
        dynamics: 0
      };
    }
    const sections = existing?.sections ?? { identity: "", style: "", facts: "", dynamics: "" };
    const sectionUpdated = existing?.sectionUpdated ?? { identity: 0, style: 0, facts: 0, dynamics: 0 };
    if (sections.dynamics && now - sectionUpdated.dynamics > DYNAMICS_STALE_THRESHOLD) {
      sections.dynamics = "";
    }
    const URGENT_TRIGGERS = {
      identity: /换工作|辞职|转行|改名|毕业|入职|退休|创业/,
      facts: /搬家|搬到|分手|结婚|生了|买了房|换了手机/,
      style: /以后.*别|不要再|换个方式|太啰嗦|说重点/
    };
    const recentMsgs = memoryState.chatHistory.slice(-5).map((h) => h.user).join(" ");
    const urgentSections = /* @__PURE__ */ new Set();
    for (const [sec, re] of Object.entries(URGENT_TRIGGERS)) {
      if (re.test(recentMsgs)) urgentSections.add(sec);
    }
    for (const sectionKey of ["identity", "style", "facts", "dynamics"]) {
      if (cliCalls >= MAX_CLI_L3) break;
      const cooldown = SECTION_COOLDOWNS[sectionKey];
      const isUrgent = urgentSections.has(sectionKey);
      if (!isUrgent && now - sectionUpdated[sectionKey] < cooldown) continue;
      if (isUrgent) {
        try {
          require("./decision-log.ts").logDecision("urgent_refresh", sectionKey, `trigger matched in recent msgs`);
        } catch {
        }
      }
      const sectionInfo = SECTION_PROMPTS[sectionKey];
      const currentContent = sections[sectionKey] || "\uFF08\u7A7A\uFF09";
      const evidence = [];
      for (const t of userTopics.slice(0, 10)) {
        evidence.push(`[${t.topic}] ${t.summary}`);
      }
      for (const m of userMems.slice(-10)) {
        evidence.push(`[${m.scope}] ${m.content.slice(0, 80)}`);
      }
      if (evidence.length === 0) continue;
      const prompt = [
        `\u5F53\u524D\u5BF9\u7528\u6237\u300C${sectionInfo.name}\u300D\u7684\u7406\u89E3\uFF1A`,
        "---",
        currentContent,
        "---",
        "",
        "\u65B0\u7684\u8BC1\u636E\uFF1A",
        ...evidence.map((e) => `- ${e}`),
        "",
        "\u8BF7\u57FA\u4E8E\u65B0\u8BC1\u636E\u66F4\u65B0\u4E0A\u9762\u7684\u7406\u89E3\u3002\u89C4\u5219\uFF1A",
        "1. \u4FDD\u7559\u4ECD\u7136\u6210\u7ACB\u7684\u65E7\u5185\u5BB9",
        "2. \u7528\u65B0\u8BC1\u636E\u4FEE\u6B63\u6216\u8865\u5145",
        "3. \u5982\u679C\u8BC1\u636E\u4E0E\u65E7\u5185\u5BB9\u77DB\u76FE\uFF0C\u4EE5\u65B0\u8BC1\u636E\u4E3A\u51C6\u5E76\u6807\u6CE8\u53D8\u5316",
        `4. \u8303\u56F4\u9650\u5B9A\uFF1A\u53EA\u5199${sectionInfo.desc}\u76F8\u5173\u7684\u5185\u5BB9`,
        "5. \u4E0D\u8D85\u8FC7 150 \u5B57",
        "6. \u53EA\u8F93\u51FA\u66F4\u65B0\u540E\u7684\u5185\u5BB9\uFF0C\u4E0D\u8981\u5143\u8BF4\u660E"
      ].join("\n");
      cliCalls++;
      spawnCLI(prompt, (output) => {
        if (!output || output.length < 10) return;
        const newContent = output.slice(0, 150);
        if (currentContent !== "\uFF08\u7A7A\uFF09" && currentContent.length > 0) {
          const oldWords = new Set((currentContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
          const newWords = new Set((newContent.match(WORD_PATTERN.CJK2_EN3) || []).map((w) => w.toLowerCase()));
          let overlap = 0;
          for (const w of oldWords) {
            if (newWords.has(w)) overlap++;
          }
          const sim = overlap / Math.max(1, Math.max(oldWords.size, newWords.size));
          if (sim > 0.92) {
            sectionUpdated[sectionKey] = now;
            return;
          }
        }
        if (currentContent !== "\uFF08\u7A7A\uFF09" && currentContent.length > 10) {
          const { trigrams: _tri, trigramSimilarity: _triSim } = require("./memory-utils.ts");
          const retentionSim = _triSim(_tri(currentContent), _tri(newContent));
          if (retentionSim < 0.5) {
            sections[sectionKey] = `${currentContent}
[\u8FD1\u671F\u8865\u5145] ${newContent}`.slice(0, 150);
            try {
              require("./decision-log.ts").logDecision("retention_guard", sectionKey, `sim=${retentionSim.toFixed(2)}<0.5, merged`);
            } catch {
            }
            sectionUpdated[sectionKey] = now;
            return;
          }
        }
        {
          let _findEnts = null;
          try {
            _findEnts = require("./graph.ts").findMentionedEntities;
          } catch {
          }
          if (_findEnts) {
            const oldEnts = new Set(_findEnts(currentContent));
            const newEnts = new Set(_findEnts(newContent));
            if (oldEnts.size > 2) {
              let lost = 0;
              for (const e of oldEnts) {
                if (!newEnts.has(e)) lost++;
              }
              if (lost / oldEnts.size > 0.3) {
                try {
                  require("./decision-log.ts").logDecision("distill_shield", sectionKey, `lost ${lost}/${oldEnts.size} entities, rejected`);
                } catch {
                }
                sectionUpdated[sectionKey] = now;
                return;
              }
            }
          }
        }
        sections[sectionKey] = newContent;
        sectionUpdated[sectionKey] = now;
        const model = {
          userId,
          model: [sections.identity, sections.style, sections.facts, sections.dynamics].filter(Boolean).join("\n").slice(0, MAX_MODEL_LENGTH),
          sections,
          sectionUpdated,
          topics: userTopics.slice(0, 10).map((n) => n.topic),
          lastUpdated: now,
          version: (existing?.version ?? 0) + 1
        };
        mentalModels.set(userId, model);
        saveMentalModels();
        console.log(`[cc-soul][distill] L2\u2192L3: ${isGlobal ? "global" : userId.slice(0, 8)} section=${sectionKey} v${model.version}`);
      }, 6e4);
    }
  }
  saveDistillState_();
}
function getMentalModel(userId) {
  if (userId) {
    const m = mentalModels.get(userId);
    if (m) return m.model;
  }
  const g = mentalModels.get("_global");
  return g?.model ?? "";
}
function getRelevantTopics(msg, userId, maxNodes = 5) {
  if (topicNodes.length === 0) return [];
  const RELEVANCE_THRESHOLD = 0.2;
  const scored = [];
  for (const node of topicNodes) {
    if (userId && node.userId && node.userId !== userId) continue;
    const overlap = keywordOverlap(msg, `${node.topic} ${node.summary}`);
    if (overlap > 0.1) {
      scored.push({ node, score: overlap });
    }
  }
  scored.sort((a, b) => b.score - a.score);
  const hits = scored.filter((s) => s.score >= RELEVANCE_THRESHOLD);
  for (const h of hits) {
    h.node.hitCount = (h.node.hitCount ?? 0) + 1;
    h.node.lastHitTs = Date.now();
  }
  const misses = scored.filter(
    (s) => s.score > 0.1 && s.score < RELEVANCE_THRESHOLD && !hits.includes(s)
  );
  for (const m of misses) {
    m.node.missCount = (m.node.missCount ?? 0) + 1;
  }
  if (topicNodes.length > 0 && scored.length === 0) {
    if (msg.length > 4 && !/^[？?]/.test(msg)) {
      const recentNodes = [...topicNodes].sort((a, b) => (b.lastUpdated || 0) - (a.lastUpdated || 0)).slice(0, 3);
      for (const node of recentNodes) {
        node.missCount = (node.missCount ?? 0) + 1;
      }
      if (recentNodes.length > 0) saveTopicNodes();
    }
  }
  if (hits.length > 0 || misses.length > 0) {
    saveTopicNodes();
  }
  return hits.slice(0, maxNodes).map((s) => s.node);
}
function auditTopicNodes() {
  const now = Date.now();
  let staleCount = 0;
  let promoted = 0;
  for (const node of topicNodes) {
    const total = (node.hitCount ?? 0) + (node.missCount ?? 0);
    const ratio = total > 0 ? (node.hitCount ?? 0) / total : 0;
    const ageDays = (now - node.lastUpdated) / 864e5;
    if (ratio < 0.2 && ageDays > 7 && total >= 3) {
      node.stale = true;
      staleCount++;
      logDecision(
        "stale_topic",
        node.topic,
        `ratio=${ratio.toFixed(2)}, age=${ageDays.toFixed(0)}d, hits=${node.hitCount ?? 0}/${total}`
      );
    }
    if ((node.hitCount ?? 0) > 10 && ratio > 0.6) {
      try {
        addMemory(
          `[\u84B8\u998F\u664B\u5347] ${node.topic}: ${node.summary}`,
          "consolidated",
          node.userId,
          "global"
        );
        promoted++;
        logDecision(
          "promote_topic",
          node.topic,
          `ratio=${ratio.toFixed(2)}, hits=${node.hitCount}`
        );
      } catch {
      }
    }
  }
  const recentMemories = memoryState.memories.filter(
    (m) => m.scope !== "expired" && m.scope !== "archived" && Date.now() - m.ts < 7 * 864e5 && // 最近 7 天
    m.content.length > 10
  );
  let orphanMemories = 0;
  for (const m of recentMemories) {
    const hasMatch = topicNodes.some((n) => {
      if (m.userId && n.userId && n.userId !== m.userId) return false;
      return keywordOverlap(m.content, `${n.topic} ${n.summary}`) > 0.2;
    });
    if (!hasMatch) orphanMemories++;
  }
  const staleRatio = topicNodes.length > 0 ? staleCount / topicNodes.length : 0;
  if (staleRatio > 0.3 || orphanMemories >= 5) {
    for (const node of topicNodes) {
      if (node.stale) {
        node.lastUpdated = 0;
        node.stale = false;
      }
    }
    saveTopicNodes();
    console.log(`[cc-soul][distill] audit triggered re-distill: staleRatio=${staleRatio.toFixed(2)}, orphans=${orphanMemories}`);
  }
  return { staleCount, promoted, orphanMemories };
}
function buildTopicAugment(msg, userId) {
  const relevant = getRelevantTopics(msg, userId);
  if (relevant.length === 0) return "";
  const lines = relevant.map((n) => `- [${n.topic}] ${n.summary}`);
  return `[\u4E3B\u9898\u8BB0\u5FC6] \u76F8\u5173\u4E3B\u9898\u7406\u89E3:
${lines.join("\n")}`;
}
function buildMentalModelAugment(userId) {
  const model = getMentalModel(userId);
  if (!model) return "";
  return `[\u7528\u6237\u5FC3\u667A\u6A21\u578B]
${model}`;
}
function runDistillPipeline() {
  try {
    const sqlMod = require("./sqlite-store.ts");
    if (sqlMod?.dbPopPendingDistill) {
      const pending = sqlMod.dbPopPendingDistill(3);
      for (const p of pending) {
        if (p.contents.length >= 2) {
          const result = zeroLLMDistill(p.contents);
          if (result && result.length > 10) {
            const node = {
              topic: result.slice(0, 20),
              summary: result.slice(0, 200),
              sourceCount: p.contents.length,
              lastUpdated: Date.now(),
              hitCount: 0,
              missCount: 0
            };
            topicNodes.push(node);
            saveTopicNodes();
            console.log(`[cc-soul][distill] pending decay distill: "${node.topic}"`);
          }
        }
      }
    }
  } catch {
  }
  auditTopicNodes();
  distillL1toL2();
  distillL2toL3();
}
function getDistillStats() {
  return {
    topicNodes: topicNodes.length,
    mentalModels: mentalModels.size,
    ...distillState
  };
}
function zeroLLMDistill(memories) {
  const parts = [];
  let extractFacts = null;
  try {
    extractFacts = require("./fact-store.ts").extractFacts;
  } catch {
  }
  const allFacts = [];
  if (extractFacts) {
    for (const content of memories) {
      const facts = extractFacts(content);
      for (const f of facts) {
        allFacts.push({ subject: f.subject, predicate: f.predicate, object: f.object });
      }
    }
  }
  const uniqueFacts = allFacts.filter(
    (f, i) => allFacts.findIndex((x) => x.subject === f.subject && x.predicate === f.predicate && x.object === f.object) === i
  ).slice(0, 3);
  if (uniqueFacts.length > 0) {
    parts.push(uniqueFacts.map((f) => `${f.subject}${f.predicate}${f.object}`).join("\uFF0C"));
  }
  let findMentionedEntities = null;
  try {
    findMentionedEntities = require("./graph.ts").findMentionedEntities;
  } catch {
  }
  if (findMentionedEntities) {
    const entityCounts = /* @__PURE__ */ new Map();
    for (const content of memories) {
      const entities = findMentionedEntities(content);
      for (const e of entities) entityCounts.set(e, (entityCounts.get(e) ?? 0) + 1);
    }
    const coreEntities = [...entityCounts.entries()].filter(([_, count]) => count >= 2).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([name]) => name);
    if (coreEntities.length > 0 && parts.length === 0) {
      parts.push(`\u6D89\u53CA\uFF1A${coreEntities.join("\u3001")}`);
    }
  }
  const behaviors = [];
  const allText = memories.join(" ");
  const likeMatch = allText.match(/(?:喜欢|爱|偏好)(.{2,15}?)(?=[，。！？\s]|$)/g);
  if (likeMatch) {
    for (const m of likeMatch.slice(0, 2)) {
      behaviors.push(m.replace(/[，。！？\s]+$/, ""));
    }
  }
  const dislikeMatch = allText.match(/(?:讨厌|不喜欢|受不了)(.{2,15}?)(?=[，。！？\s]|$)/g);
  if (dislikeMatch) {
    for (const m of dislikeMatch.slice(0, 2)) {
      behaviors.push(m.replace(/[，。！？\s]+$/, ""));
    }
  }
  const habitMatch = allText.match(/(?:每天|经常|习惯|总是)(.{2,20}?)(?=[，。！？\s]|$)/g);
  if (habitMatch) {
    behaviors.push(habitMatch[0].replace(/[，。！？\s]+$/, ""));
  }
  if (behaviors.length > 0) {
    parts.push(behaviors.join("\uFF1B"));
  }
  for (let i = 0; i < memories.length; i++) {
    for (let j = i + 1; j < memories.length; j++) {
      const a = memories[i], b = memories[j];
      if (detectPolarityFlip(a, b)) {
        const wordsA = new Set(a.match(/[\u4e00-\u9fff]{2,4}/g) || []);
        const wordsB = new Set(b.match(/[\u4e00-\u9fff]{2,4}/g) || []);
        let shared = 0;
        for (const w of wordsA) {
          if (wordsB.has(w)) shared++;
        }
        if (shared >= 1) {
          parts.push(`\u89C2\u70B9\u53D8\u5316\uFF1A\u4ECE\u6B63\u9762\u8F6C\u8D1F\u9762`);
          try {
            const { penalizeTruthfulness } = require("./smart-forget.ts");
            const olderContent = a;
            const matchedMem = memoryState.memories.find((m) => m && m.content === olderContent);
            if (matchedMem) {
              penalizeTruthfulness(matchedMem, `\u77DB\u76FE\u68C0\u6D4B\uFF1A\u4E0E"${b.slice(0, 20)}"\u51B2\u7A81`);
            }
          } catch {
          }
          break;
        }
      }
    }
    if (parts.length >= 4) break;
  }
  if (parts.length === 0) {
    const STOP_WORDS = new Set("\u7684\u4E86\u662F\u5728\u6211\u4F60\u4ED6\u5979\u5B83\u4E0D\u6709\u8FD9\u90A3\u5C31\u4E5F\u548C\u4F46\u90FD\u8981\u4F1A\u53EF\u4EE5\u5982\u679C\u56E0\u4E3A\u6240\u4EE5\u7136\u540E\u5DF2\u7ECF\u8FD8\u6CA1\u5230\u88AB\u628A\u4ECE\u7528\u4E8E\u5173\u4E8E\u5BF9\u4E8E\u63D0\u5230".match(/[\u4e00-\u9fff]/g) || []);
    const allWords = /* @__PURE__ */ new Map();
    for (const content of memories) {
      const words = (content.match(WORD_PATTERN.CJK24_EN3) || []).map((w) => w.toLowerCase());
      for (const w of words) {
        const chars = w.match(/[\u4e00-\u9fff]/g) || [];
        if (chars.length > 0 && chars.every((c) => STOP_WORDS.has(c))) continue;
        allWords.set(w, (allWords.get(w) || 0) + 1);
      }
    }
    const topWords = [...allWords.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([w]) => w);
    if (topWords.length > 0) parts.push(`\u5173\u4E8E${topWords.slice(0, 3).join("\u3001")}\u7684\u8BA8\u8BBA`);
  }
  return parts.join("\uFF1B").slice(0, 200) || memories[0]?.slice(0, 60) || "";
}
function adjustTopicConfidence(topicName, delta) {
  const node = topicNodes.find((n) => n.topic === topicName);
  if (!node) return;
  const confidence = (node.confidence ?? 0.5) + delta;
  node.confidence = Math.max(0.1, Math.min(0.95, confidence));
  if (node.confidence < 0.3) {
    node.lastUpdated = 0;
    node.stale = true;
    logDecision(
      "stale_topic",
      topicName,
      `confidence=${node.confidence.toFixed(2)}<0.3, delta=${delta}`
    );
  }
  saveTopicNodes();
}
const CJK_WORD_RE = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi;
function extractWords(text) {
  return (text.match(CJK_WORD_RE) || []).map((w) => w.toLowerCase());
}
function memoryPMISimilarity(memContent, nodeText) {
  let aamPmi = null;
  try {
    aamPmi = require("./aam.ts").pmi;
  } catch {
    return 0;
  }
  if (!aamPmi) return 0;
  const mWords = [...new Set(extractWords(memContent))];
  const nWords = [...new Set(extractWords(nodeText))];
  if (mWords.length === 0 || nWords.length === 0) return 0;
  let sum = 0, count = 0;
  for (const mw of mWords) {
    for (const nw of nWords) {
      if (mw === nw) {
        sum += 3;
        count++;
        continue;
      }
      const p = aamPmi(mw, nw);
      if (p > 0) {
        sum += p;
        count++;
      }
    }
  }
  return count > 0 ? sum / count : 0;
}
function assignMemoryToNode(memContent, nodes, userId) {
  let best = null, bestScore = 0;
  for (const n of nodes) {
    if (userId && n.userId && n.userId !== userId) continue;
    const score = memoryPMISimilarity(memContent, `${n.topic} ${n.summary}`);
    if (score > bestScore) {
      bestScore = score;
      best = n;
    }
  }
  return bestScore > 0.3 ? best : null;
}
function clusterOrphansByPMI(orphans, threshold) {
  const clusters = [];
  const assigned = /* @__PURE__ */ new Set();
  for (let i = 0; i < orphans.length; i++) {
    if (assigned.has(i)) continue;
    const cluster = [orphans[i]];
    assigned.add(i);
    for (let j = i + 1; j < orphans.length; j++) {
      if (assigned.has(j)) continue;
      if (memoryPMISimilarity(orphans[i], orphans[j]) > threshold) {
        cluster.push(orphans[j]);
        assigned.add(j);
      }
    }
    if (cluster.length >= 2) clusters.push(cluster);
  }
  return clusters;
}
function clusterByKeywords(memories) {
  const CJK_WORD = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi;
  const clusters = [];
  const assigned = /* @__PURE__ */ new Set();
  for (let i = 0; i < memories.length; i++) {
    if (assigned.has(i)) continue;
    const cluster = [memories[i]];
    assigned.add(i);
    const wordsI = new Set((memories[i].content.match(CJK_WORD) || []).map((w) => w.toLowerCase()));
    if (wordsI.size === 0) continue;
    for (let j = i + 1; j < memories.length; j++) {
      if (assigned.has(j)) continue;
      const wordsJ = new Set((memories[j].content.match(CJK_WORD) || []).map((w) => w.toLowerCase()));
      if (wordsJ.size === 0) continue;
      let hits = 0;
      for (const w of wordsI) {
        if (wordsJ.has(w)) hits++;
      }
      const overlap = hits / Math.max(1, Math.min(wordsI.size, wordsJ.size));
      if (overlap >= 0.4) {
        cluster.push(memories[j]);
        assigned.add(j);
      }
    }
    if (cluster.length >= 2) {
      clusters.push(cluster);
    }
  }
  return clusters;
}
function keywordOverlap(a, b) {
  const CJK_WORD = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi;
  const wordsA = new Set((a.match(CJK_WORD) || []).map((w) => w.toLowerCase()));
  const wordsB = new Set((b.match(CJK_WORD) || []).map((w) => w.toLowerCase()));
  if (wordsA.size === 0 || wordsB.size === 0) return 0;
  let hits = 0;
  for (const w of wordsA) {
    if (wordsB.has(w)) hits++;
  }
  return hits / Math.max(1, Math.min(wordsA.size, wordsB.size));
}
export {
  adjustTopicConfidence,
  auditTopicNodes,
  buildMentalModelAugment,
  buildTopicAugment,
  distillL1toL2,
  distillL2toL3,
  getDistillStats,
  getMentalModel,
  getRelevantTopics,
  loadDistillState,
  runDistillPipeline,
  zeroLLMDistill
};
