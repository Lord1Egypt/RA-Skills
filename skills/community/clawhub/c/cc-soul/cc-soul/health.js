import { existsSync } from "fs";
import { execSync } from "child_process";
import { memoryState } from "./memory.ts";
import { body } from "./body.ts";
import { rules } from "./evolution.ts";
import { graphState } from "./graph.ts";
import { MEMORIES_PATH, STATS_PATH } from "./persistence.ts";
import { getAllFeatures } from "./features.ts";
let lastHealthCheck = 0;
const HEALTH_CHECK_INTERVAL = 30 * 6e4;
const moduleErrors = /* @__PURE__ */ new Map();
const moduleActivity = /* @__PURE__ */ new Map();
let errorWindowStart = Date.now();
function recordModuleError(moduleName, error) {
  const record = moduleErrors.get(moduleName) || { count: 0, lastError: "", lastErrorAt: 0 };
  record.count++;
  record.lastError = error.slice(0, 200);
  record.lastErrorAt = Date.now();
  moduleErrors.set(moduleName, record);
}
function recordModuleActivity(moduleName) {
  moduleActivity.set(moduleName, Date.now());
}
function getModuleErrorSummary() {
  const errorsByModule = {};
  let totalErrors = 0;
  for (const [mod, record] of moduleErrors) {
    errorsByModule[mod] = record.count;
    totalErrors += record.count;
  }
  const silentModules = [];
  const oneHourAgo = Date.now() - 36e5;
  const expectedActiveModules = ["memory", "cognition", "body", "prompt-builder", "quality"];
  for (const mod of expectedActiveModules) {
    const lastActive = moduleActivity.get(mod) || 0;
    if (errorWindowStart < oneHourAgo && (lastActive === 0 || lastActive < oneHourAgo)) {
      silentModules.push(mod);
    }
  }
  return { totalErrors, errorsByModule, silentModules };
}
function resetModuleErrors() {
  moduleErrors.clear();
  errorWindowStart = Date.now();
}
function getErrorDetails() {
  if (moduleErrors.size === 0) return "";
  const lines = [];
  for (const [mod, record] of moduleErrors) {
    if (record.count > 0) {
      lines.push(`  ${mod}: ${record.count} \u6B21\u9519\u8BEF (\u6700\u8FD1: ${record.lastError.slice(0, 80)})`);
    }
  }
  return lines.length > 0 ? `\u6A21\u5757\u9519\u8BEF\u7EDF\u8BA1:
${lines.join("\n")}` : "";
}
function healthCheck() {
  const now = Date.now();
  if (now - lastHealthCheck < HEALTH_CHECK_INTERVAL) {
    return { status: "healthy", issues: [], stats: {} };
  }
  lastHealthCheck = now;
  const issues = [];
  if (!existsSync(MEMORIES_PATH)) issues.push("memories.json missing");
  if (!existsSync(STATS_PATH)) issues.push("stats.json missing");
  if (memoryState.memories.length === 0) issues.push("memory empty (0 memories)");
  const expired = memoryState.memories.filter((m) => m.scope === "expired").length;
  if (expired > memoryState.memories.length * 0.5) {
    issues.push(`>50% memories expired (${expired}/${memoryState.memories.length})`);
  }
  if (body.energy < 0 || body.energy > 1) issues.push(`body.energy out of range: ${body.energy}`);
  if (body.mood < -1 || body.mood > 1) issues.push(`body.mood out of range: ${body.mood}`);
  const features = getAllFeatures();
  if (Object.keys(features).length === 0) issues.push("features.json not loaded");
  const errorSummary = getModuleErrorSummary();
  if (errorSummary.totalErrors > 10) {
    const topErrorModule = Object.entries(errorSummary.errorsByModule).sort(([, a], [, b]) => b - a)[0];
    if (topErrorModule) {
      issues.push(`high error rate: ${topErrorModule[0]} has ${topErrorModule[1]} errors`);
    }
  }
  if (errorSummary.silentModules.length > 0) {
    issues.push(`silent modules (>1hr inactive): ${errorSummary.silentModules.join(", ")}`);
  }
  let status = "healthy";
  if (issues.length > 0 && issues.length <= 2) status = "degraded";
  if (issues.length > 2) status = "critical";
  const report = {
    status,
    issues,
    stats: {
      memories: memoryState.memories.length,
      rules: rules.length,
      entities: graphState.entities.length,
      energy: body.energy.toFixed(2),
      mood: body.mood.toFixed(2),
      features: Object.values(features).filter((v) => v).length,
      moduleErrors: errorSummary.totalErrors
    }
  };
  if (issues.length > 0) {
    console.warn(`[cc-soul][health] ${status}: ${issues.join("; ")}`);
  }
  checkCliConcurrency();
  return report;
}
let lastCleanupCheck = 0;
const CLEANUP_COOLDOWN = 6e4;
async function postReplyCleanup() {
  try {
    const m = await import("./cli.ts");
    m.killGatewayClaude?.();
  } catch {
    try {
      const psOutput = execSync(
        `ps aux | grep "[c]laude" | grep -v "Claude.app" | grep -v "chrome_crashpad" | awk '{print $2}'`,
        { timeout: 3e3 }
      ).toString().trim();
      if (!psOutput) return;
      const pids = psOutput.split("\n").map((p) => p.trim()).filter(Boolean);
      let killed = 0;
      for (const pid of pids) {
        if (!/^\d+$/.test(pid)) continue;
        try {
          const cwd = execSync(`lsof -p ${pid} 2>/dev/null | grep cwd | awk '{print $NF}'`, { timeout: 2e3 }).toString().trim();
          if (cwd.includes(".openclaw/hooks")) {
            process.kill(parseInt(pid), "SIGTERM");
            killed++;
          }
        } catch {
        }
      }
      if (killed > 0) {
        console.log(`[cc-soul][health] \u56DE\u590D\u5B8C\u6210\uFF0C\u6E05\u7406\u4E86 ${killed} \u4E2A gateway claude \u8FDB\u7A0B`);
      }
    } catch {
    }
  }
}
function checkCliConcurrency() {
}
const healthModule = {
  id: "health",
  name: "\u5065\u5EB7\u76D1\u63A7",
  priority: 80
};
export {
  getErrorDetails,
  getModuleErrorSummary,
  healthCheck,
  healthModule,
  postReplyCleanup,
  recordModuleActivity,
  recordModuleError,
  resetModuleErrors
};
