import {
  metrics,
  stats,
  getHeartbeatRunning,
  setHeartbeatRunning,
  getHeartbeatStartedAt,
  setHeartbeatStartedAt
} from "./handler-state.ts";
import { dbGetDueReminders, dbMarkReminderFired } from "./sqlite-store.ts";
import { bodyTick } from "./body.ts";
import {
  consolidateMemories,
  scanForContradictions,
  evaluateAndPromoteMemories,
  cleanupWorkingMemory,
  processMemoryDecay,
  batchTagUntaggedMemories,
  auditMemoryHealth,
  sqliteMaintenance,
  pruneExpiredMemories,
  reviveDecayedMemories,
  compressOldMemories
} from "./memory.ts";
import { cleanupPlans } from "./inner-life.ts";
import { computePageRank, decayActivations, invalidateStaleEntities, invalidateStaleRelations, enrichCausalFromMemories } from "./graph.ts";
import { isEnabled } from "./features.ts";
import { checkAutoTune } from "./auto-tune.ts";
import { resampleHardExamples } from "./quality.ts";
import { runDistillPipeline } from "./distill.ts";
import { healthCheck, recordModuleError, recordModuleActivity } from "./health.ts";
import { notifySoulActivity } from "./notify.ts";
import { brain } from "./brain.ts";
import { distillPersonModel } from "./person-model.ts";
import { tickBatchQueue } from "./cli.ts";
import { heartbeatScanAbsence } from "./absence-detection.ts";
import { scanBlindSpotQuestions } from "./epistemic.ts";
import { updateDeepUnderstand } from "./deep-understand.ts";
import { innerState } from "./inner-life.ts";
function getHeartbeatMode() {
  const lastActivity = innerState.lastActivityTime || metrics.lastHeartbeat || 0;
  const inactive = Date.now() - lastActivity;
  if (inactive < 30 * 6e4) return "awake";
  if (inactive < 6 * 36e5) return "light_sleep";
  return "deep_sleep";
}
let _cliSemaphore = 0;
const MAX_CLI_CONCURRENT = 3;
let _cliFailures = 0;
let _cliCircuitOpenAt = 0;
function safeCLI(name, fn, safeFn) {
  if (_cliFailures >= 3) {
    if (Date.now() - _cliCircuitOpenAt < 36e5) {
      return;
    }
    console.log(`[cc-soul][heartbeat] CLI circuit half-open, attempting ${name}`);
  }
  if (_cliSemaphore >= MAX_CLI_CONCURRENT) {
    return;
  }
  _cliSemaphore++;
  safeFn(name, () => {
    try {
      fn();
      if (_cliFailures > 0) {
        _cliFailures = 0;
      }
    } catch (e) {
      _cliFailures++;
      if (_cliFailures >= 3) {
        _cliCircuitOpenAt = Date.now();
        console.error(`[cc-soul][heartbeat] CLI circuit OPEN (${name}: ${e.message})`);
        try {
          require("./decision-log.ts").logDecision("circuit_open", "cli", `failures=${_cliFailures}, ${name}: ${e.message}`);
        } catch {
        }
      }
      throw e;
    } finally {
      _cliSemaphore--;
    }
  });
}
function runHeartbeat() {
  if (getHeartbeatRunning() && getHeartbeatStartedAt() > 0 && Date.now() - getHeartbeatStartedAt() > 25 * 6e4) {
    console.error("[cc-soul][heartbeat] force-releasing stuck heartbeat lock (>25min)");
    setHeartbeatRunning(false);
  }
  if (getHeartbeatRunning()) return;
  setHeartbeatRunning(true);
  setHeartbeatStartedAt(Date.now());
  metrics.lastHeartbeat = Date.now();
  try {
    const safe = (name, fn) => {
      try {
        const result = fn();
        if (result && typeof result.then === "function") {
          ;
          result.then(() => recordModuleActivity(name)).catch((e) => {
            recordModuleError(name, e.message);
            console.error(`[cc-soul][heartbeat][${name}] async: ${e.message}`);
          });
        } else {
          recordModuleActivity(name);
        }
      } catch (e) {
        recordModuleError(name, e.message);
        console.error(`[cc-soul][heartbeat][${name}] ${e.message}`);
      }
    };
    const mode = getHeartbeatMode();
    console.log(`[cc-soul][heartbeat] mode=${mode}`);
    safe("bodyTick", () => bodyTick());
    safe("batchTag", () => batchTagUntaggedMemories());
    safe("workingCleanup", () => cleanupWorkingMemory());
    safe("brainHeartbeat", () => brain.fire("onHeartbeat"));
    safe("health", () => healthCheck());
    safe("planCleanup", () => cleanupPlans());
    safe("batchQueue", () => tickBatchQueue());
    if (isEnabled("absence_detection")) safe("absenceDetection", () => heartbeatScanAbsence());
    safe("reminders", () => {
      const due = dbGetDueReminders();
      for (const r of due) {
        notifySoulActivity(`[\u63D0\u9192] ${r.msg}`);
        dbMarkReminderFired(r.id);
      }
    });
    if (mode === "awake") {
      console.log("[cc-soul][heartbeat] awake mode \u2014 light tasks only");
    } else {
      safeCLI("consolidate", () => consolidateMemories(), safe);
      safeCLI("contradiction", () => scanForContradictions(), safe);
      safe("memoryPromotion", () => evaluateAndPromoteMemories());
      safe("smartForgetSweep", () => {
        try {
          const { smartForgetModule } = require("./smart-forget.ts");
          smartForgetModule.onHeartbeat();
        } catch {
        }
      });
      safe("memoryDecay", () => processMemoryDecay());
      safe("bayesDecay", () => {
        try {
          require("./confidence-cascade.ts").batchTimeDecay(require("./memory.ts").memoryState.memories);
        } catch {
        }
      });
      safe("aamDecay", () => {
        try {
          require("./aam.ts").decayCooccurrence();
        } catch {
        }
      });
      safe("pmiClusters", () => {
        try {
          require("./aam.ts").buildPMIClusters();
        } catch {
        }
      });
      safe("pruneExpired", () => pruneExpiredMemories());
      safe("reviveDecayed", () => reviveDecayedMemories());
      safe("memoryAudit", () => auditMemoryHealth());
      safe("compressOld", () => compressOldMemories());
      safe("sqliteMaintenance", () => {
        sqliteMaintenance().catch(() => {
        });
      });
      safe("pageRank", () => computePageRank());
      safe("activationDecay", () => decayActivations());
      safe("staleEntities", () => invalidateStaleEntities());
      safe("staleRelations", () => invalidateStaleRelations());
      safe("enrichCausal", () => enrichCausalFromMemories());
      safe("entityCrystal", async () => {
        try {
          const { graphState, generateEntitySummary } = await import("./graph.ts");
          const now = Date.now();
          for (const entity of graphState.entities) {
            if (entity.invalid_at !== null) continue;
            if (entity.mentions < 3) continue;
            const lastCrystal = entity.attrs.find((a) => a.startsWith("crystal:"));
            const lastTs = lastCrystal ? parseInt(lastCrystal.split("|")[1] || "0") : 0;
            if (now - lastTs < 864e5) continue;
            const summary = generateEntitySummary(entity.name);
            if (summary) {
              entity.attrs = entity.attrs.filter((a) => !a.startsWith("crystal:"));
              entity.attrs.push(`crystal:${summary.slice(0, 100)}|${now}`);
            }
          }
        } catch {
        }
      });
      safe("predictivePreload", () => {
        try {
          const { getTopPredictions, getTimeSlot } = require("./behavioral-phase-space.ts");
          const topPredictions = getTopPredictions(2);
          if (!topPredictions || topPredictions.length === 0 || topPredictions[0].probability < 0.7) return;
          const prediction = topPredictions[0];
          const hour = (/* @__PURE__ */ new Date()).getHours();
          const currentSlot = getTimeSlot();
          const slotRanges = {
            early_morning: [6, 9],
            morning: [9, 12],
            afternoon: [12, 18],
            evening: [18, 23],
            late_night: [23, 6]
          };
          const range = slotRanges[currentSlot];
          if (!range) return;
          const inRange = range[0] <= range[1] ? hour >= range[0] - 1 && hour <= range[1] + 1 : hour >= range[0] - 1 || hour <= range[1] + 1;
          if (!inRange) return;
          const predictedTopic = prediction.domain;
          if (!predictedTopic) return;
          const { memoryState } = require("./memory.ts");
          let preheated = 0;
          for (const m of memoryState.memories) {
            if (!m || m.scope === "expired" || m.scope === "decayed") continue;
            if (m.content && m.content.includes(predictedTopic)) {
              m._preheated = true;
              m.confidence = Math.min(1, (m.confidence || 0.7) + 0.05);
              preheated++;
              if (preheated >= 5) break;
            }
          }
          if (preheated > 0) {
            console.log(`[cc-soul][heartbeat] pre-heated ${preheated} memories for predicted topic="${predictedTopic}" (conf=${prediction.probability.toFixed(2)})`);
            try {
              require("./decision-log.ts").logDecision("preheat", predictedTopic, `${preheated} memories, conf=${prediction.probability.toFixed(2)}, slot=${currentSlot}`);
            } catch {
            }
          }
        } catch {
        }
      });
      if (isEnabled("self_upgrade")) safe("autoTune", () => checkAutoTune(stats));
      safeCLI("qualityResample", () => resampleHardExamples(), safe);
      safe("blindSpotQuestions", () => scanBlindSpotQuestions());
      safe("deepUnderstand", () => updateDeepUnderstand());
      safe("structureWordDiscovery", async () => {
        try {
          const { discoverNewStructureWords } = await import("./dynamic-extractor.ts");
          const { getSessionState, getLastActiveSessionKey } = await import("./handler-state.ts");
          const sess = getSessionState(getLastActiveSessionKey());
          const userId = sess?.userId || "default";
          discoverNewStructureWords(userId);
        } catch {
        }
      });
      safe("behaviorLearn", async () => {
        const { learnFromObservations } = await import("./behavioral-phase-space.ts");
        learnFromObservations();
      });
      safe("pmCleanup", async () => {
        const { cleanupProspectiveMemories, autoDetectFromMemories } = await import("./prospective-memory.ts");
        cleanupProspectiveMemories();
        try {
          const { memoryState } = await import("./memory.ts");
          if (memoryState.memories.length > 0) {
            autoDetectFromMemories(memoryState.memories);
          }
        } catch {
        }
      });
      if (mode === "deep_sleep") {
        console.log("[cc-soul][heartbeat] deep_sleep mode \u2014 full consolidation");
        safeCLI("distill", () => runDistillPipeline(), safe);
        safeCLI("personModel", () => distillPersonModel(), safe);
        safe("crystallize", async () => {
          const { crystallizeTraits } = await import("./person-model.ts");
          crystallizeTraits();
        });
        safe("skillExtract", async () => {
          try {
            const { traceCausalChain, graphState } = await import("./graph.ts");
            const { memoryState } = await import("./memory.ts");
            const { DATA_DIR, loadJson, debouncedSave } = await import("./persistence.ts");
            const { resolve } = await import("path");
            const SKILLS_PATH = resolve(DATA_DIR, "skills.json");
            let skills = loadJson(SKILLS_PATH, []);
            if (skills.length >= 50) return;
            const resolvedEpisodes = memoryState.memories.filter(
              (m) => m && m.scope === "event" && /解决|搞定|成功|修好/.test(m.content)
            ).slice(-10);
            for (const resolved of resolvedEpisodes) {
              const entities = (await import("./graph.ts")).findMentionedEntities(resolved.content);
              if (entities.length === 0) continue;
              const chain = traceCausalChain(entities.slice(0, 1), 2);
              if (chain.length === 0) continue;
              const trigger = entities.slice(0, 2);
              const steps = chain.map((c) => c.slice(0, 50));
              const id = `skill_${Date.now()}_${Math.random().toString(36).slice(2, 5)}`;
              const hasSimilar = skills.some((s) => s.trigger.some((t) => trigger.includes(t)));
              if (hasSimilar) continue;
              skills.push({ id, trigger, steps, learnedFrom: [resolved.content.slice(0, 40)], successRate: 0.5, lastUsed: 0, domain: entities[0] });
            }
            try {
              const { getRules } = await import("./evolution.ts");
              const rules = getRules?.() ?? [];
              for (const r of rules.filter((r2) => r2.hits >= 5 && r2.hits / (r2.hits + (r2.misses ?? 0) + 1) > 0.7)) {
                const trigger = (r.conditions ?? []).slice(0, 3);
                if (trigger.length === 0) continue;
                const hasSimilar = skills.some((s) => s.trigger.some((t) => trigger.includes(t)));
                if (hasSimilar) continue;
                skills.push({
                  id: `skill_rule_${Date.now()}_${Math.random().toString(36).slice(2, 5)}`,
                  trigger,
                  steps: [r.rule],
                  learnedFrom: [r.source ?? "evolution"],
                  successRate: r.hits / (r.hits + (r.misses ?? 0) + 1),
                  lastUsed: 0,
                  domain: trigger[0]
                });
              }
            } catch {
            }
            if (skills.length > 50) skills = skills.slice(-50);
            debouncedSave(SKILLS_PATH, skills, 5e3);
          } catch {
          }
        });
      }
    }
  } catch (e) {
    console.error(`[cc-soul][heartbeat] ${e.message}`);
  } finally {
    setHeartbeatRunning(false);
  }
}
export {
  runHeartbeat
};
