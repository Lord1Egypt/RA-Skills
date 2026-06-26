import { resolve } from "path";
import { DATA_DIR, loadJson } from "./persistence.ts";
import { memoryState, recall, queryMemoryTimeline } from "./memory.ts";
import { stats } from "./handler-state.ts";
import { body } from "./body.ts";
import { getActivePersona } from "./persona.ts";
import { brain } from "./brain.ts";
import { getDb } from "./sqlite-store.ts";
function readMemoriesFromDisk() {
  try {
    const memPath = resolve(DATA_DIR, "memories.json");
    return loadJson(memPath, []);
  } catch (_) {
  }
  return memoryState.memories || [];
}
function recallWithFallback(keyword, limit, senderId) {
  let results = recall(keyword, limit, senderId);
  if (results.length === 0) {
    const allMems = readMemoriesFromDisk();
    const kw = keyword.toLowerCase();
    results = allMems.filter(
      (m) => m.scope !== "expired" && m.scope !== "decayed" && (m.content.toLowerCase().includes(kw) || m.tags && m.tags.some((t) => t.toLowerCase().includes(kw)))
    ).slice(0, limit);
  }
  if (results.length === 0) {
    try {
      const _sdb = getDb();
      if (_sdb) {
        const kw = `%${keyword.toLowerCase()}%`;
        const rows = _sdb.prepare(
          "SELECT content, scope, tags, ts FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?) ORDER BY ts DESC LIMIT ?"
        ).all(kw, kw, limit);
        results = rows.map((r) => ({
          content: r.content,
          scope: r.scope,
          tags: r.tags ? typeof r.tags === "string" ? JSON.parse(r.tags) : r.tags : [],
          ts: r.ts
        }));
      }
    } catch (_) {
    }
  }
  return results;
}
function executeSearch(keyword, senderId) {
  if (!keyword) return "\u7528\u6CD5: \u641C\u7D22\u8BB0\u5FC6 <\u5173\u952E\u8BCD>";
  const results = recallWithFallback(keyword, 10, senderId);
  if (results.length === 0) return `\u6CA1\u6709\u627E\u5230\u5173\u4E8E\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u3002`;
  const lines = results.map((m, i) => {
    const ago = Math.floor((Date.now() - m.ts) / 864e5);
    const agoStr = ago === 0 ? "\u4ECA\u5929" : `${ago}\u5929\u524D`;
    const emotionStr = m.emotion && m.emotion !== "neutral" ? ` (${m.emotion})` : "";
    return `${i + 1}. [${m.scope}] ${m.content.slice(0, 80)}${emotionStr}\uFF08${agoStr}\uFF09`;
  });
  return `\u641C\u7D22\u300C${keyword}\u300D\u7684\u8BB0\u5FC6\u7ED3\u679C\uFF08${results.length} \u6761\uFF09\uFF1A
${lines.join("\n")}`;
}
function executeMyMemories(senderId) {
  try {
    const _sdb = getDb();
    if (_sdb) {
      const activeCount = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get()?.c || 0;
      const recent = _sdb.prepare(
        "SELECT scope, content, ts FROM memories WHERE scope != 'expired' AND scope != 'decayed' ORDER BY ts DESC LIMIT 20"
      ).all();
      if (recent.length > 0) {
        const lines2 = recent.map((m, i) => {
          const ago = Math.floor((Date.now() - (m.ts || 0)) / 864e5);
          const agoStr = ago === 0 ? "\u4ECA\u5929" : `${ago}\u5929\u524D`;
          return `${i + 1}. [${m.scope}] ${(m.content || "").slice(0, 60)}\uFF08${agoStr}\uFF09`;
        });
        return `\u6700\u8FD1\u8BB0\u5FC6\uFF08\u5171 ${activeCount} \u6761\u6D3B\u8DC3\uFF09\uFF1A
${lines2.join("\n")}`;
      }
    }
  } catch (_) {
  }
  const mems = readMemoriesFromDisk();
  const active = mems.filter((m) => m.scope !== "expired" && m.scope !== "decayed");
  const filtered = active.filter((m) => !senderId || !m.userId || m.userId === senderId).sort((a, b) => (b.ts || 0) - (a.ts || 0)).slice(0, 20);
  const total = active.filter((m) => !senderId || !m.userId || m.userId === senderId).length;
  if (filtered.length === 0) return "\u8FD8\u6CA1\u6709\u8BB0\u5FC6\u3002";
  const lines = filtered.map((m, i) => {
    const ago = Math.floor((Date.now() - (m.ts || 0)) / 864e5);
    const agoStr = ago === 0 ? "\u4ECA\u5929" : `${ago}\u5929\u524D`;
    return `${i + 1}. [${m.scope}] ${m.content.slice(0, 60)}\uFF08${agoStr}\uFF09`;
  });
  return `\u6700\u8FD1\u8BB0\u5FC6\uFF08\u5171 ${total} \u6761\u6D3B\u8DC3\uFF09\uFF1A
${lines.join("\n")}`;
}
function executeStats() {
  let active = 0;
  try {
    const _sdb = getDb();
    if (_sdb) {
      active = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get()?.c || 0;
    }
  } catch (_) {
  }
  if (active === 0) {
    const mems = readMemoriesFromDisk();
    active = mems.filter((m) => m.scope !== "expired" && m.scope !== "decayed").length;
  }
  const days = stats.firstSeen ? Math.max(1, Math.floor((Date.now() - stats.firstSeen) / 864e5)) : 0;
  return `cc-soul \u4EEA\u8868\u76D8
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
\u4E92\u52A8: ${stats.totalMessages} \u6B21 | \u8BA4\u8BC6: ${days} \u5929
\u7EA0\u6B63\u7387: ${stats.totalMessages > 0 ? (stats.corrections / stats.totalMessages * 100).toFixed(1) : 0}%
\u8BB0\u5FC6: ${active} \u6761\u6D3B\u8DC3
\u6A21\u5757: ${brain.listModules().length} \u4E2A
\u4EBA\u683C: ${getActivePersona()?.name || "default"}
\u80FD\u91CF: ${(body.energy * 100).toFixed(0)}% | \u5FC3\u60C5: ${(body.mood * 100).toFixed(0)}%`;
}
function executeHealth() {
  try {
    const _sdb = getDb();
    if (_sdb) {
      const total = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get()?.c || 0;
      const scopes2 = _sdb.prepare(
        "SELECT scope, COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed' GROUP BY scope ORDER BY c DESC LIMIT 10"
      ).all();
      const scopeLines = scopes2.map((s) => `  ${s.scope}: ${s.c}`).join("\n");
      const highConf = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0.7 AND scope != 'expired'").get()?.c || 0;
      const medConf = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0.4 AND confidence < 0.7 AND scope != 'expired'").get()?.c || 0;
      const lowConf = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0 AND confidence < 0.4 AND scope != 'expired'").get()?.c || 0;
      const cutoff30d = Date.now() - 30 * 864e5;
      const decayedCount = _sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE ts < ? AND recallCount = 0 AND scope != 'expired' AND scope != 'decayed'").get(cutoff30d)?.c || 0;
      return [
        `\u8BB0\u5FC6\u5065\u5EB7\u62A5\u544A`,
        `\u603B\u6570: ${total}`,
        ``,
        `Scope \u5206\u5E03:`,
        scopeLines,
        ``,
        `\u7F6E\u4FE1\u5EA6\u5206\u5E03:`,
        `  \u9AD8 (>=0.7): ${highConf}`,
        `  \u4E2D (0.4-0.7): ${medConf}`,
        `  \u4F4E (<0.4): ${lowConf}`,
        ``,
        `\u8870\u51CF\u6982\u51B5:`,
        `  30\u5929\u4EE5\u4E0A\u96F6\u547D\u4E2D: ${decayedCount} \u6761 (${total > 0 ? (decayedCount / total * 100).toFixed(1) : 0}%)`,
        `  \u6D3B\u8DC3\u8BB0\u5FC6: ${total - decayedCount} \u6761`
      ].join("\n");
    }
  } catch (_) {
  }
  const mems = readMemoriesFromDisk();
  const active = mems.filter((m) => m.scope !== "expired" && m.scope !== "decayed");
  const scopes = /* @__PURE__ */ new Map();
  for (const m of active) {
    const s = m.scope || "unknown";
    scopes.set(s, (scopes.get(s) || 0) + 1);
  }
  const tagged = active.filter((m) => m.tags && m.tags.length > 0).length;
  return [
    `\u8BB0\u5FC6\u5065\u5EB7\u62A5\u544A`,
    `\u603B\u8BB0\u5FC6: ${mems.length} | \u6D3B\u8DC3: ${active.length} | \u5DF2\u6807\u7B7E: ${tagged}`,
    `
\u6309\u7C7B\u578B:`,
    ...[...scopes.entries()].sort((a, b) => b[1] - a[1]).map(([s, c]) => `  ${s}: ${c}`)
  ].join("\n");
}
function executeFeatures() {
  try {
    const featPath = resolve(DATA_DIR, "features.json");
    const feats = loadJson(featPath, {});
    const lines = Object.entries(feats).sort(([, a], [, b]) => (b ? 1 : 0) - (a ? 1 : 0)).map(([k, v]) => `${v ? "\u2705" : "\u274C"} ${k}`);
    return `\u529F\u80FD\u72B6\u6001\uFF08${lines.length} \u9879\uFF09\uFF1A
${lines.join("\n")}`;
  } catch (_) {
    return "\u65E0\u6CD5\u8BFB\u53D6\u529F\u80FD\u72B6\u6001\u3002";
  }
}
function executeTimeline(keyword) {
  if (!keyword) return "\u7528\u6CD5: \u8BB0\u5FC6\u65F6\u95F4\u7EBF <\u5173\u952E\u8BCD>";
  try {
    const timeline = queryMemoryTimeline(keyword);
    if (!timeline || timeline.length === 0) return `\u6CA1\u6709\u627E\u5230\u300C${keyword}\u300D\u7684\u5386\u53F2\u8BB0\u5F55\u3002`;
    return `\u300C${keyword}\u300D\u8BB0\u5FC6\u65F6\u95F4\u7EBF\uFF1A
${timeline.join("\n")}`;
  } catch (_) {
    return "\u67E5\u8BE2\u5931\u8D25\u3002";
  }
}
export {
  executeFeatures,
  executeHealth,
  executeMyMemories,
  executeSearch,
  executeStats,
  executeTimeline
};
