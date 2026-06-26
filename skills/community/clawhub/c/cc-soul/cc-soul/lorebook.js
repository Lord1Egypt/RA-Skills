import { resolve } from "path";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
const LOREBOOK_PATH = resolve(DATA_DIR, "lorebook.json");
let entries = [];
function loadLorebook() {
  entries = loadJson(LOREBOOK_PATH, []);
  console.log(`[cc-soul][lorebook] loaded ${entries.length} entries`);
}
function saveLorebook() {
  debouncedSave(LOREBOOK_PATH, entries);
}
function addLorebookEntry(entry) {
  const existing = entries.find(
    (e) => e.keywords.some((k) => entry.keywords.includes(k)) && e.content === entry.content
  );
  if (existing) return;
  entries.push({
    ...entry,
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    createdAt: Date.now(),
    hitCount: 0
  });
  if (entries.length > 200) {
    entries.sort((a, b) => b.hitCount - a.hitCount);
    entries = entries.slice(0, 150);
  }
  saveLorebook();
}
function removeLorebookEntry(keyword) {
  const idx = entries.findIndex(
    (e) => e.keywords.some((k) => k.includes(keyword)) || e.content.includes(keyword)
  );
  if (idx >= 0) {
    entries.splice(idx, 1);
    saveLorebook();
    return true;
  }
  return false;
}
function queryLorebook(msg) {
  if (!msg || entries.length === 0) return [];
  const lower = msg.toLowerCase();
  const matched = [];
  for (const entry of entries) {
    if (!entry.enabled) continue;
    const hit = entry.keywords.some((kw) => lower.includes(kw.toLowerCase()));
    if (hit) {
      entry.hitCount++;
      matched.push(entry);
    }
  }
  if (matched.length > 0) saveLorebook();
  return matched.sort((a, b) => b.priority - a.priority).slice(0, 5);
}
function autoPopulateFromMemories(memories) {
  const candidates = memories.filter((m) => {
    if (m.scope === "expired") return false;
    if (m.content.length < 15) return false;
    if ((m.scope === "fact" || m.scope === "preference") && m.emotion === "important") return true;
    if (m.scope === "consolidated") return true;
    if (m.scope === "correction" && m.content.startsWith("[\u7EA0\u6B63\u5F52\u56E0]")) return true;
    return false;
  });
  for (const mem of candidates.slice(-10)) {
    const words = (mem.content.match(/[\u4e00-\u9fff]{2,4}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase()).filter((w) => w.length >= 2).slice(0, 5);
    if (words.length >= 1) {
      addLorebookEntry({
        keywords: words,
        content: mem.content,
        priority: 7,
        enabled: true,
        category: mem.scope === "preference" ? "preference" : "fact"
      });
    }
  }
}
function getLorebookStats() {
  if (entries.length === 0) return "";
  const enabled = entries.filter((e) => e.enabled).length;
  return `\u77E5\u8BC6\u5E93: ${enabled}/${entries.length} \u6761`;
}
const lorebookModule = {
  id: "lorebook",
  name: "\u77E5\u8BC6\u6CE8\u5165",
  priority: 50,
  features: ["lorebook"],
  init() {
    loadLorebook();
  }
};
export {
  addLorebookEntry,
  autoPopulateFromMemories,
  getLorebookStats,
  loadLorebook,
  entries as lorebookEntries,
  lorebookModule,
  queryLorebook,
  removeLorebookEntry
};
