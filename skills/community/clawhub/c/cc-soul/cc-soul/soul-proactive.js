import "./persistence.ts";
let lastCheck = 0;
const COOLDOWN = 10 * 60 * 1e3;
async function generateProactiveItems() {
  const now = Date.now();
  if (now - lastCheck < COOLDOWN) return [];
  lastCheck = now;
  const userId = "default";
  const items = [];
  try {
    const { loadJson, DATA_DIR } = await import("./persistence.ts");
    const { resolve } = await import("path");
    const moodHistory = loadJson(resolve(DATA_DIR, "mood_history.json"), []);
    const recent = moodHistory.filter((m) => now - m.ts < 3 * 24 * 36e5);
    const avgMood = recent.length > 0 ? recent.reduce((s, m) => s + (m.mood || 0), 0) / recent.length : 0;
    if (avgMood < -0.3 && recent.length >= 3) {
      items.push({ type: "care", message: "\u7528\u6237\u6700\u8FD1\u60C5\u7EEA\u504F\u4F4E\u843D\uFF0C\u56DE\u590D\u65F6\u591A\u4E00\u4E9B\u5173\u6000\u548C\u7406\u89E3", priority: 9, userId, createdAt: now });
    }
  } catch {
  }
  try {
    const { peekPendingFollowUps } = await import("./inner-life.ts");
    for (const fu of peekPendingFollowUps().slice(0, 2)) {
      items.push({ type: "followup", message: `\u53EF\u4EE5\u81EA\u7136\u5730\u95EE\u4E00\u4E0B\uFF1A${fu}`, priority: 7, userId, createdAt: now });
    }
  } catch {
  }
  try {
    const { getDb } = await import("./sqlite-store.ts");
    const db = getDb();
    if (db) {
      const goals = db.prepare?.("SELECT * FROM goals WHERE progress >= 50 AND progress < 100")?.all?.() || [];
      for (const g of goals) {
        items.push({ type: "milestone", message: `\u7528\u6237\u7684\u76EE\u6807"${g.description}"\u5DF2\u5B8C\u6210 ${g.progress}%`, priority: 6, userId, createdAt: now });
      }
    }
  } catch {
  }
  try {
    const { getProfile } = await import("./user-profiles.ts");
    const profile = getProfile(userId);
    if (profile?.rhythm && profile.messageCount > 50) {
      const hours = profile.rhythm.activeHours || [];
      const peak = hours.indexOf(Math.max(...hours));
      if (peak >= 0) {
        const now_h = (/* @__PURE__ */ new Date()).getHours();
        if (Math.abs(now_h - peak) > 6) {
          items.push({ type: "insight", message: `\u7528\u6237\u901A\u5E38\u5728 ${peak}:00 \u6700\u6D3B\u8DC3\uFF0C\u73B0\u5728\u4E0D\u662F\u4ED6\u7684\u6D3B\u8DC3\u65F6\u6BB5`, priority: 4, userId, createdAt: now });
        }
      }
    }
  } catch {
  }
  try {
    const { loadAvatarProfile } = await import("./avatar.ts");
    const profile = loadAvatarProfile(userId);
    for (const [name, contact] of Object.entries(profile.social || {})) {
      const sc = contact;
      if (sc.samples?.length >= 5) {
        const allSamples = [...profile.expression.samples?.casual || [], ...profile.expression.samples?.technical || [], ...profile.expression.samples?.emotional || [], ...profile.expression.samples?.general || []];
        const recentMentions = allSamples.filter((s) => s.includes(name)).length;
        if (recentMentions === 0) {
          items.push({ type: "relationship", message: `\u7528\u6237\u6700\u8FD1\u6CA1\u63D0\u5230${name}\uFF08${sc.relation}\uFF09`, priority: 5, userId, createdAt: now });
        }
      }
    }
  } catch {
  }
  try {
    const { getMemoriesByScope } = await import("./memory.ts");
    const wisdoms = getMemoriesByScope("wisdom") || [];
    const old = wisdoms.filter((m) => now - (m.createdAt || 0) > 30 * 24 * 36e5 && (m.recallCount || 0) < 2);
    if (old.length > 0) {
      const pick = old[Math.floor(Math.random() * old.length)];
      items.push({ type: "revival", message: `\u7528\u6237\u4E4B\u524D\u8BF4\u8FC7\uFF1A"${pick.content.replace(/^\[.*?\]\s*/, "").slice(0, 50)}"`, priority: 3, userId, createdAt: now });
    }
  } catch {
  }
  const seen = /* @__PURE__ */ new Set();
  return items.filter((i) => {
    if (seen.has(i.type)) return false;
    seen.add(i.type);
    return true;
  }).sort((a, b) => b.priority - a.priority).slice(0, 5);
}
export {
  generateProactiveItems
};
