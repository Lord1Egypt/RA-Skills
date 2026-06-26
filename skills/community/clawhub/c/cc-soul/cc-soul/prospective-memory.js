import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
const PM_PATH = resolve(DATA_DIR, "prospective_memory.json");
let pmStore = loadJson(PM_PATH, []);
function savePM() {
  debouncedSave(PM_PATH, pmStore);
}
let _counter = 0;
function makeId() {
  return `pm_${Date.now()}_${_counter++}`;
}
const FUTURE_PATTERNS = [
  {
    detect: /(?:下周|明天|后天|周[一二三四五六日天]).*(?:面试|interview)/,
    triggerKeywords: "\u9762\u8BD5|interview|\u7D27\u5F20|\u51C6\u5907|offer",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u9762\u8BD5\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 14
  },
  {
    detect: /(?:下周|明天|后天|周[一二三四五六日天]).*(?:出差|出行|旅行|飞)/,
    triggerKeywords: "\u51FA\u5DEE|\u51FA\u884C|\u673A\u573A|\u9152\u5E97|\u884C\u674E|\u822A\u73ED",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u51FA\u884C\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 14
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:换工作|跳槽|离职|辞职)/,
    triggerKeywords: "\u7B80\u5386|\u9762\u8BD5|offer|\u8DF3\u69FD|\u79BB\u804C|\u65B0\u5DE5\u4F5C",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u8DF3\u69FD\u610F\u5411\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 30
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:买房|买车|装修|搬家)/,
    triggerKeywords: "\u623F|\u8F66|\u88C5\u4FEE|\u642C\u5BB6|\u8D37\u6B3E|\u9996\u4ED8|\u770B\u623F",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u8D2D\u4E70/\u642C\u8FC1\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 60
  },
  {
    detect: /(?:下次|以后|记得).*(?:提醒|别忘|注意)/,
    triggerKeywords: "",
    // will be extracted from message
    remindTemplate: (_m, msg) => `\u7528\u6237\u8981\u6C42\u8BB0\u4F4F\uFF1A${msg.slice(0, 80)}`,
    expiryDays: 30
  },
  {
    detect: /(?:deadline|ddl|截止|交付).*(?:下周|月底|号|日)/,
    triggerKeywords: "deadline|ddl|\u622A\u6B62|\u4EA4\u4ED8|\u6765\u4E0D\u53CA|\u8FDB\u5EA6",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u622A\u6B62\u65E5\u671F\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 14
  },
  {
    detect: /(?:下[周个]?月|下季度|明年).*(?:旅[行游]|出[国门]|度假)/,
    triggerKeywords: "\u65C5\u884C|\u51FA\u53D1|\u673A\u7968|\u7B7E\u8BC1|\u884C\u674E|\u9152\u5E97|\u653B\u7565",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u65C5\u884C\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 60
  },
  {
    detect: /(?:下周|这周|明天|后天|周[一二三四五六日天]).*(?:开会|会议|review|评审|述职|分享|演讲|讲座|talk|汇报)/,
    triggerKeywords: "\u4F1A\u8BAE|review|\u8BC4\u5BA1|\u8FF0\u804C|\u6C47\u62A5|PPT|\u6750\u6599|\u5206\u4EAB|\u6F14\u8BB2|\u8BB2\u5EA7|slides",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u4F1A\u8BAE/\u5206\u4EAB\u5B89\u6392\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 7
  },
  {
    detect: /(?:下周|这周|明天|后天|周[一二三四五六日天]).*(?:考试|测验|认证|答辩)/,
    triggerKeywords: "\u8003\u8BD5|\u6D4B\u9A8C|\u8BA4\u8BC1|\u7B54\u8FA9|\u590D\u4E60|\u51C6\u5907|\u901A\u8FC7",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u8003\u8BD5\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 14
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:学|练|入门|转行|转型)/,
    triggerKeywords: "\u5B66\u4E60|\u5165\u95E8|\u6559\u7A0B|\u8BFE\u7A0B|\u8FDB\u5EA6|\u575A\u6301",
    remindTemplate: (_m, msg) => `\u7528\u6237\u4E4B\u524D\u63D0\u5230\u6709\u5B66\u4E60\u8BA1\u5212\uFF1A${msg.slice(0, 60)}`,
    expiryDays: 30
  }
];
function detectProspectiveMemory(userMsg, userId) {
  for (const pattern of FUTURE_PATTERNS) {
    const match = userMsg.match(pattern.detect);
    if (!match) continue;
    const existing = pmStore.find(
      (pm2) => !pm2.firedAt && pm2.trigger === pattern.triggerKeywords && pm2.userId === userId
    );
    if (existing) continue;
    const pm = {
      id: makeId(),
      trigger: pattern.triggerKeywords || userMsg.slice(0, 30),
      remind: pattern.remindTemplate(match, userMsg),
      createdAt: Date.now(),
      expiresAt: pattern.expiryDays > 0 ? Date.now() + pattern.expiryDays * 864e5 : 0,
      source: /提醒|记得|别忘/.test(userMsg) ? "user_explicit" : "auto",
      userId
    };
    pmStore.push(pm);
    savePM();
    console.log(`[cc-soul][prospective] created: "${pm.trigger}" \u2192 "${pm.remind.slice(0, 40)}"`);
  }
}
function checkProspectiveMemory(userMsg, userId) {
  const now = Date.now();
  const msgLower = userMsg.toLowerCase();
  const reminders = [];
  for (const pm of pmStore) {
    if (pm.firedAt) continue;
    if (pm.expiresAt > 0 && now > pm.expiresAt) continue;
    if (pm.userId && pm.userId !== userId) continue;
    const keywords = pm.trigger.split("|").filter((k) => k.length >= 2);
    const matched = keywords.some((kw) => msgLower.includes(kw.toLowerCase()));
    if (!matched) continue;
    pm.firedAt = now;
    reminders.push(pm.remind);
    console.log(`[cc-soul][prospective] FIRED: "${pm.trigger}" \u2192 "${pm.remind.slice(0, 40)}"`);
  }
  if (reminders.length > 0) {
    savePM();
    return `[\u524D\u77BB\u8BB0\u5FC6] ${reminders.join("\uFF1B")}`;
  }
  return null;
}
function cleanupProspectiveMemories() {
  const now = Date.now();
  const FIRED_RETENTION = 7 * 864e5;
  const before = pmStore.length;
  pmStore = pmStore.filter((pm) => {
    if (pm.expiresAt > 0 && now > pm.expiresAt && !pm.firedAt) return false;
    if (pm.firedAt && now - pm.firedAt > FIRED_RETENTION) return false;
    return true;
  });
  if (pmStore.length < before) {
    savePM();
    console.log(`[cc-soul][prospective] cleanup: removed ${before - pmStore.length} expired PMs`);
  }
}
function getProspectiveMemoryCount() {
  return pmStore.filter((pm) => !pm.firedAt && (!pm.expiresAt || pm.expiresAt > Date.now())).length;
}
function getActivePMTriggers() {
  const now = Date.now();
  return pmStore.filter((pm) => !pm.firedAt && (!pm.expiresAt || pm.expiresAt > now)).flatMap((pm) => pm.trigger.split("|").filter((k) => k.length >= 2)).map((k) => k.toLowerCase());
}
const CYCLES_PATH = resolve(DATA_DIR, "keyword_cycles.json");
let keywordCycles = loadJson(CYCLES_PATH, []);
function saveCycles() {
  debouncedSave(CYCLES_PATH, keywordCycles);
}
function learnKeywordCycles(memories) {
  if (memories.length < 50) return;
  const weekdayFreq = /* @__PURE__ */ new Map();
  const hourFreq = /* @__PURE__ */ new Map();
  for (const mem of memories) {
    const words = (mem.content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const d = new Date(mem.ts);
    const day = d.getDay();
    const hour = d.getHours();
    for (const w of new Set(words)) {
      if (!weekdayFreq.has(w)) weekdayFreq.set(w, new Array(7).fill(0));
      if (!hourFreq.has(w)) hourFreq.set(w, new Array(24).fill(0));
      weekdayFreq.get(w)[day]++;
      hourFreq.get(w)[hour]++;
    }
  }
  const newCycles = [];
  for (const [keyword, days] of weekdayFreq) {
    const total = days.reduce((s, v) => s + v, 0);
    if (total < 5) continue;
    const avg = total / 7;
    let peakDay = 0, peakCount = 0;
    for (let i = 0; i < 7; i++) {
      if (days[i] > peakCount) {
        peakCount = days[i];
        peakDay = i;
      }
    }
    if (peakCount >= 3 && peakCount > avg * 2) {
      const hours = hourFreq.get(keyword) || new Array(24).fill(0);
      let peakHour = 0, peakHourCount = 0;
      for (let i = 0; i < 24; i++) {
        if (hours[i] > peakHourCount) {
          peakHourCount = hours[i];
          peakHour = i;
        }
      }
      const confidence = Math.min(0.9, (peakCount / total - 1 / 7) * 3);
      newCycles.push({
        keyword,
        peakDay,
        peakHour,
        frequency: peakCount / total,
        confidence,
        lastSeen: Date.now()
      });
    }
  }
  if (newCycles.length > 0) {
    keywordCycles = newCycles.sort((a, b) => b.confidence - a.confidence).slice(0, 20);
    saveCycles();
    console.log(`[cc-soul][fft-cycles] learned ${keywordCycles.length} keyword cycles`);
  }
}
function getCyclicReminders() {
  const now = /* @__PURE__ */ new Date();
  const today = now.getDay();
  const hour = now.getHours();
  const reminders = [];
  for (const cycle of keywordCycles) {
    if (cycle.peakDay === today && Math.abs(cycle.peakHour - hour) <= 2 && cycle.confidence > 0.3) {
      reminders.push(cycle.keyword);
    }
  }
  return reminders;
}
function getKeywordCycleCount() {
  return keywordCycles.length;
}
function autoDetectFromMemories(memories) {
  const recent = memories.filter((m) => m.scope !== "expired" && m.scope !== "decayed").slice(-20);
  if (recent.length < 5) return;
  const keywordCounts = /* @__PURE__ */ new Map();
  for (const m of recent) {
    const words = (m.content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{4,}/g) || []).map((w) => w.toLowerCase());
    const unique = new Set(words);
    for (const w of unique) {
      if (/^(什么|这个|那个|可以|不是|没有|就是|但是|然后|因为|所以|如果|the|and|for|this|that|with)$/.test(w)) continue;
      keywordCounts.set(w, (keywordCounts.get(w) || 0) + 1);
    }
  }
  for (const [keyword, count] of keywordCounts) {
    if (count < 3) continue;
    const exists = pmStore.some(
      (pm2) => !pm2.firedAt && pm2.trigger.includes(keyword) && pm2.source === "auto"
    );
    if (exists) continue;
    const pm = {
      id: makeId(),
      trigger: keyword,
      remind: `\u7528\u6237\u8FD1\u671F\u591A\u6B21\u63D0\u5230"${keyword}"\uFF08${count}\u6B21\uFF09\uFF0C\u53EF\u80FD\u662F\u6301\u7EED\u5173\u6CE8\u7684\u8BDD\u9898`,
      createdAt: Date.now(),
      expiresAt: Date.now() + 14 * 864e5,
      // 14 days
      source: "auto"
    };
    pmStore.push(pm);
    savePM();
    console.log(`[cc-soul][prospective] auto-created from recurring theme: "${keyword}" (${count}x in last 20)`);
  }
}
export {
  autoDetectFromMemories,
  checkProspectiveMemory,
  cleanupProspectiveMemories,
  detectProspectiveMemory,
  getActivePMTriggers,
  getCyclicReminders,
  getKeywordCycleCount,
  getProspectiveMemoryCount,
  learnKeywordCycles
};
