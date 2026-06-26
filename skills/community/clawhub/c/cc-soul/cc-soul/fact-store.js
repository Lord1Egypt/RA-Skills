import { DATA_DIR, loadJson } from "./persistence.ts";
import { resolve } from "path";
import {
  isSQLiteReady,
  sqliteAddFact,
  sqliteQueryFacts,
  sqliteInvalidateFacts,
  sqliteFactCount,
  sqliteGetFactsBySubject,
  sqliteLoadAllFacts
} from "./sqlite-store.ts";
const FACTS_PATH = resolve(DATA_DIR, "structured_facts.json");
let facts = isSQLiteReady() ? sqliteLoadAllFacts() : loadJson(FACTS_PATH, []);
function saveFacts() {
}
const RULES = [
  // "我叫X" / "我是X" / "我名字叫X" / "大家叫我X" / "my name is X" / "call me X" → name
  { pattern: /(?:我叫|我名字(?:是|叫)|大家(?:都)?叫我|我的名字(?:是|叫)?|my name is|i'm called|call me|i am)\s*([^\s，。！？,;；\n]{1,8})/i, extract: (m) => {
    const name = m[1].trim();
    if (/^(什么|啥|谁|哪|吗|呢|嘛)/.test(name)) return null;
    if (/^(fine|good|ok|okay|tired|happy|sad|sorry|here|back|done|sure|ready|not|just|also|very|so|a|an|the|doing|going|trying|using|looking|working|from)\b/i.test(name)) return null;
    if (name.length < 1) return null;
    return {
      subject: "user",
      predicate: "name",
      object: name,
      confidence: 0.95,
      source: "user_said",
      ts: Date.now(),
      validUntil: 0
    };
  } },
  // "我喜欢X" / "我爱X" / "我偏好X" — stop at punctuation or conjunctions
  { pattern: /我(?:喜欢|爱|偏好|特别喜欢|超喜欢)(?:用)?\s*([^，。！？,;；\n]{2,15})/, extract: (m) => ({
    subject: "user",
    predicate: "likes",
    object: m[1].trim(),
    confidence: 0.85,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我不喜欢X" / "我讨厌X" / "我不爱X" / "i don't like" / "i hate" / "i dislike"
  { pattern: /(?:我(?:不喜欢|讨厌|不爱|不想用|受不了)|i don'?t like|i hate|i dislike|can'?t stand)\s*(.{2,20})/i, extract: (m) => ({
    subject: "user",
    predicate: "dislikes",
    object: m[1].replace(/[。，！？\s]+$/, ""),
    confidence: 0.85,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我用X" / "我在用X" / "我常用X" / "i use" / "i'm using"
  { pattern: /(?:我(?:用|在用|常用|一直用)|i use|i'm using|i usually use)\s*(.{2,20})/i, extract: (m) => ({
    subject: "user",
    predicate: "uses",
    object: m[1].replace(/[。，！？\s]+$/, ""),
    confidence: 0.8,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我在X工作" / "我在X做Y" / "我是X的" / "i work at" / "i work for" / "employed at"
  { pattern: /(?:我(?:在|是)\s*(.{2,15})(?:工作|上班|就职|的员工|做\S{2,10})|(?:i work (?:at|for)|employed at)\s*(.{2,15}))/i, extract: (m) => ({
    subject: "user",
    predicate: "works_at",
    object: (m[2] || m[0].replace(/^我(?:在|是)\s*/, "")).replace(/^(?:i work (?:at|for)|employed at)\s*/i, "").replace(/[。，！？\s]+$/, ""),
    confidence: 0.9,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我住在X" / "i live in" / "i'm based in" / "i'm from" — only match explicit residence, not "我在X工作"
  { pattern: /(?:我(?:住在|住|搬到|搬去|移居|去了)\s*|已经(?:搬|到)了?\s*|i live in\s*|i'm based in\s*|i'm from\s*)([^，。！？,;；\n]{2,10})/i, extract: (m) => {
    const place = m[1].trim();
    if (place.length < 2 || /^(这|那|哪|什么|怎么)/.test(place)) return null;
    if (/工作|上班|就职/.test(place)) return null;
    return {
      subject: "user",
      predicate: "lives_in",
      object: place,
      confidence: 0.7,
      source: "user_said",
      ts: Date.now(),
      validUntil: 0
    };
  } },
  // "我是做X的" / "我是X工程师/开发/设计师" / "i'm a X" / "i work as" / "my job is"
  { pattern: /(?:我是(?:做)?(.{2,15})(?:的|工程师|开发|设计师|产品|运营)|(?:i'm a|i work as|my job is)\s*(.{2,15}))/i, extract: (m) => ({
    subject: "user",
    predicate: "occupation",
    object: (m[2] || m[1]).replace(/[。，！？\s]+$/, ""),
    confidence: 0.85,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "X比Y好" / "X比Y快" — preference
  { pattern: /(.{2,10})比(.{2,10})(?:好|快|强|稳定|方便|简单|简洁|好用|舒服|靠谱)/, extract: (m) => ({
    subject: "user",
    predicate: "prefers",
    object: `${m[1].trim()} over ${m[2].trim()}`,
    confidence: 0.7,
    source: "ai_inferred",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我X岁" / "我今年X" / "i'm X years old" / "i am X" → age
  { pattern: /(?:我(?:今年)?(\d{1,3})岁|i(?:'m| am)\s*(\d{1,3})\s*(?:years?\s*old)?)/i, extract: (m) => ({
    subject: "user",
    predicate: "age",
    object: m[1] || m[2],
    confidence: 0.9,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我养了一只猫叫X" / "我家有一条狗" / "i have a pet" / "my cat" / "my dog" → has_pet（匹配到句尾，保留名字）
  { pattern: /(?:我们?(?:养了|家有|有一只|有一条|有一个)|i have a pet|i own a|my cat|my dog)\s*([^，。！？,;；\n]{2,20})/i, extract: (m) => {
    let obj = m[1].trim().replace(/[。，！？\s]+$/, "");
    if (obj.length < 2 || /^(什么|哪|这|那)/.test(obj)) return null;
    return {
      subject: "user",
      predicate: "has_pet",
      object: obj,
      confidence: 0.8,
      source: "user_said",
      ts: Date.now(),
      validUntil: 0
    };
  } },
  // "我有个女儿/儿子/孩子" / "我有X个孩子" / "i have a daughter/son" / "my kid" → has_family
  { pattern: /(?:我有(?:个|一个|两个|三个)?\s*([^，。！？,;；\n]{1,10}?)(?:女儿|儿子|孩子|闺女|宝宝|小孩|老婆|老公|丈夫|妻子|爸|妈|哥|姐|弟|妹)|i have a\s*(daughter|son|kid|child)|my\s*(kid|child|son|daughter))/i, extract: (m) => ({
    subject: "user",
    predicate: "has_family",
    object: (m[2] || m[3] || m[0].replace(/^我有(?:个|一个|两个|三个)?\s*/, "").replace(/^(?:i have a|my)\s*/i, "")).replace(/[。，！？\s]+$/, ""),
    confidence: 0.9,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我女儿/儿子叫X" → family_name
  { pattern: /我(?:女儿|儿子|孩子|闺女|宝宝|老婆|老公)叫\s*([^，。！？,;；\n]{1,8})/, extract: (m) => ({
    subject: "user",
    predicate: "family_name",
    object: m[0].replace(/^我/, "").replace(/[。，！？\s]+$/, ""),
    confidence: 0.9,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我每天X" / "我习惯X" / "i always" / "every day i" / "my daily" → habit
  { pattern: /(?:我(?:每天|习惯|一般都|通常|经常)|i always|every day i|my daily)\s*([^，。！？,;；\n]{2,20})/i, extract: (m) => ({
    subject: "user",
    predicate: "habit",
    object: m[1].replace(/[。，！？\s]+$/, ""),
    confidence: 0.75,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我毕业于X" / "我读的X大学" / "i graduated from" / "i went to" / "my school" / "my university" → educated_at
  { pattern: /(?:我(?:毕业于|毕业|读的|上的)|i graduated from|i went to|my school is|my university is)\s*([^，。！？,;；\n]{2,15})(?:大学|学院|学校)?/i, extract: (m) => ({
    subject: "user",
    predicate: "educated_at",
    object: m[1].replace(/[。，！？\s]+$/, ""),
    confidence: 0.85,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我老婆/老公/女朋友/男朋友" / "my wife/husband/girlfriend/boyfriend" → relationship
  { pattern: /(?:我(?:老婆|老公|女朋友|男朋友|媳妇|对象|另一半|爱人)|my (?:wife|husband|girlfriend|boyfriend|partner|spouse))\s*([^，。！？,;；\n\s]{0,8})/i, extract: (m, content) => {
    const relType = m[0].match(/老婆|老公|女朋友|男朋友|媳妇|对象|另一半|爱人|wife|husband|girlfriend|boyfriend|partner|spouse/i)?.[0] || "partner";
    const detail = m[1]?.trim();
    if (detail && /什么|哪|谁|怎么|吗$|呢$/.test(detail)) return null;
    return {
      subject: "user",
      predicate: "relationship",
      object: detail ? `${relType}\uFF1A${detail}` : relType,
      confidence: 0.85,
      source: "user_said",
      ts: Date.now(),
      validUntil: 0
    };
  } },
  // "我住X楼/X层" → lives_in (floor)
  { pattern: /我住(?:在)?(\d{1,3})(?:楼|层)/, extract: (m) => ({
    subject: "user",
    predicate: "lives_in",
    object: `${m[1]}\u697C`,
    confidence: 0.7,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) },
  // "我用Mac/Windows/Linux" → uses_os
  { pattern: /我(?:用|在用|一直用)\s*(Mac|MacBook|Windows|Linux|Ubuntu|macOS|win|WSL)/i, extract: (m) => ({
    subject: "user",
    predicate: "uses_os",
    object: m[1],
    confidence: 0.85,
    source: "user_said",
    ts: Date.now(),
    validUntil: 0
  }) }
];
function extractFacts(content, source = "user_said", userId) {
  const extracted = [];
  const trimmed = content.trim();
  const isQuestion = /[？?]$/.test(trimmed) || // 问号结尾
  /(.)\1不\1/.test(trimmed) || // 动词重叠（是不是/有没有）
  /[吗呢吧嘛]$/.test(trimmed) || // 语气词结尾
  /^.{0,6}(?:什么|哪个|哪里|谁|怎么|为什么)/.test(trimmed) || // 开头附近有疑问代词
  /(?:叫|是|做|在|有)(?:什么|哪个|谁|怎么)/.test(trimmed) || // 动词+疑问代词（"叫什么""做什么""是谁"）
  /(?:什么|哪|谁|怎么|多少|几)(?:时候|地方|样|个|种|岁|楼)/.test(trimmed) || // 疑问代词+量词/名词
  /^(?:what|who|where|when|why|how|which|do you|does|did|is|are|was|were|can|could|will|would)\b/i.test(trimmed) || // English question starters
  /\b(?:what is|who is|what's my|where do i|what do i)\b/i.test(trimmed);
  if (isQuestion) {
    return extracted;
  }
  if (/^\[.{1,10}\]/.test(trimmed)) {
    return extracted;
  }
  let _currentSegmentId = 0;
  try {
    _currentSegmentId = require("./memory.ts").getCurrentSegmentId?.() ?? 0;
  } catch {
  }
  try {
    const { dynamicExtract, updateStructureStrength } = require("./dynamic-extractor.ts");
    const dynamicResults = dynamicExtract(content, userId);
    for (const r of dynamicResults) {
      const exists = facts.some(
        (f) => f.subject === r.subject && f.predicate === r.predicate && f.object === r.object && f.validUntil === 0
      );
      if (!exists) {
        let _segId;
        try {
          _segId = require("./memory.ts").getCurrentSegmentId?.();
        } catch {
        }
        const fact = {
          subject: r.subject,
          predicate: r.predicate,
          object: r.object,
          confidence: r.confidence,
          source: r.source,
          ts: Date.now(),
          validUntil: 0,
          memoryRef: content.slice(0, 60),
          segmentId: _segId ?? _currentSegmentId
        };
        extracted.push(fact);
        if (userId) updateStructureStrength(r.structureWord, userId, true);
      }
    }
  } catch {
  }
  const dynamicPredicates = new Set(extracted.map((e) => e.predicate));
  for (const rule of RULES) {
    const match = content.match(rule.pattern);
    if (match) {
      const fact = rule.extract(match, content);
      if (fact) {
        if (dynamicPredicates.has(fact.predicate)) continue;
        fact.source = source;
        fact.memoryRef = content.slice(0, 60);
        const exists = facts.some(
          (f) => f.subject === fact.subject && f.predicate === fact.predicate && f.object === fact.object && f.validUntil === 0
        ) || extracted.some(
          (e) => e.subject === fact.subject && e.predicate === fact.predicate && e.object === fact.object
        );
        if (!exists) extracted.push(fact);
      }
    }
  }
  if (extracted.length === 0 && content.length > 15) {
    try {
      const { hasLLM, spawnCLI } = require("./cli.ts");
      if (hasLLM()) {
        const { getCurrentSegmentId } = require("./memory.ts");
        const _segId = getCurrentSegmentId?.() ?? 0;
        spawnCLI(
          `\u4ECE\u8FD9\u53E5\u8BDD\u63D0\u53D6\u4E8B\u5B9E\u4E09\u5143\u7EC4\u3002\u8F93\u51FAJSON\u6570\u7EC4\uFF1A[{"subject":"\u4E3B\u8BED","predicate":"\u8C13\u8BED","object":"\u5BBE\u8BED"}]\u3002\u6CA1\u6709\u4E8B\u5B9E\u5C31\u8F93\u51FA[]\u3002
Extract fact triples from this sentence. Output JSON array: [{"subject":"subject","predicate":"predicate","object":"object"}]. If no facts, output [].

"${content.slice(0, 200)}"`,
          (output) => {
            try {
              const parsed = JSON.parse(output.match(/\[[\s\S]*\]/)?.[0] || "[]");
              if (parsed.length > 0) {
                const llmFacts = parsed.slice(0, 3).map((f) => ({
                  subject: f.subject || "user",
                  predicate: f.predicate,
                  object: f.object,
                  confidence: 0.7,
                  source: "ai_inferred",
                  ts: Date.now(),
                  validUntil: 0,
                  memoryRef: content.slice(0, 60),
                  segmentId: _segId
                }));
                addFacts(llmFacts);
                try {
                  require("./decision-log.ts").logDecision("llm_fact_extract", content.slice(0, 30), `${llmFacts.length} facts extracted by LLM`);
                } catch {
                }
              }
            } catch {
            }
          },
          15e3
        );
      }
    } catch {
    }
  }
  return extracted;
}
function addFacts(newFacts) {
  for (const nf of newFacts) {
    const exactDup = facts.some(
      (f) => f.subject === nf.subject && f.predicate === nf.predicate && f.object === nf.object && f.validUntil === 0
    );
    if (exactDup) continue;
    let shouldSupersede = true;
    for (const old of facts) {
      if (old.subject === nf.subject && old.predicate === nf.predicate && old.object !== nf.object && old.validUntil === 0) {
        const NON_EXCLUSIVE = /* @__PURE__ */ new Set(["learning", "likes", "dislikes", "habit", "prefers"]);
        if (NON_EXCLUSIVE.has(nf.predicate)) {
          shouldSupersede = false;
          break;
        }
        if (nf.object.length < old.object.length * 0.5 && (old.confidence ?? 0) >= (nf.confidence ?? 0)) {
          console.log(`[cc-soul][facts] skip supersede (info loss): "${nf.object}" < "${old.object}"`);
          nf._skipReason = "info_loss";
          shouldSupersede = false;
          break;
        }
      }
    }
    if (shouldSupersede) {
      for (const old of facts) {
        if (old.subject === nf.subject && old.predicate === nf.predicate && old.object !== nf.object && old.validUntil === 0) {
          old.validUntil = Date.now();
          nf.supersedes = old.object;
          console.log(`[cc-soul][facts] superseded: ${old.subject}.${old.predicate}="${old.object}" \u2192 "${nf.object}"`);
        }
      }
    } else if (nf._skipReason === "info_loss") {
      continue;
    }
    facts.push(nf);
    try {
      if (nf.object && nf.object.length >= 2) {
        const { learnAssociation } = require("./aam.ts");
        learnAssociation(nf.object, 0, 0.8);
      }
    } catch {
    }
    if (isSQLiteReady()) {
      try {
        sqliteInvalidateFacts(nf.subject, nf.predicate, nf.object);
        sqliteAddFact(nf);
      } catch {
      }
    }
  }
  if (newFacts.length > 0) {
    saveFacts();
    console.log(`[cc-soul][facts] added ${newFacts.length} structured facts`);
    try {
      const { emitCacheEvent } = require("./memory-utils.ts");
      emitCacheEvent("fact_updated");
    } catch {
    }
  }
}
function queryFacts(opts) {
  if (isSQLiteReady()) {
    try {
      const results = sqliteQueryFacts(opts);
      if (results.length > 0) return results;
    } catch {
    }
  }
  return facts.filter((f) => {
    if (f.validUntil > 0) return false;
    if (opts.subject && f.subject !== opts.subject) return false;
    if (opts.predicate && f.predicate !== opts.predicate) return false;
    if (opts.object && !f.object.includes(opts.object)) return false;
    return true;
  });
}
function queryFactTimeline(subject, predicate) {
  const allVersions = facts.filter(
    (f) => f.subject === subject && f.predicate === predicate
  ).sort((a, b) => a.ts - b.ts);
  if (isSQLiteReady() && allVersions.length === 0) {
    try {
      const results = sqliteQueryFacts({ subject, predicate });
    } catch {
    }
  }
  return allVersions.map((f) => ({
    object: f.object,
    validFrom: f.ts,
    validUntil: f.validUntil,
    confidence: f.confidence,
    source: f.source
  }));
}
function formatFactTimeline(subject, predicate) {
  const timeline = queryFactTimeline(subject, predicate);
  if (timeline.length <= 1) return null;
  const current = timeline.find((v) => v.validUntil === 0) ?? timeline[timeline.length - 1];
  const history = timeline.filter((v) => v.validUntil > 0);
  if (history.length === 0) return null;
  const historyStr = history.map((v) => {
    const date = new Date(v.validFrom).toLocaleDateString("zh-CN");
    return `${date}:${v.object}`;
  }).join(" \u2192 ");
  return `${predicate}: ${historyStr} \u2192 \u73B0\u5728:${current.object}`;
}
function getFactSummary(subject = "user") {
  let valid;
  if (isSQLiteReady()) {
    try {
      valid = sqliteGetFactsBySubject(subject);
    } catch {
      valid = [];
    }
  } else {
    valid = facts.filter((f) => f.subject === subject && f.validUntil === 0);
  }
  if (valid.length === 0) return "";
  const grouped = {};
  for (const f of valid) {
    if (!grouped[f.predicate]) grouped[f.predicate] = [];
    grouped[f.predicate].push(f.object);
  }
  const LABELS = {
    name: "\u540D\u5B57",
    likes: "\u559C\u6B22",
    dislikes: "\u4E0D\u559C\u6B22",
    uses: "\u4F7F\u7528",
    works_at: "\u5DE5\u4F5C\u4E8E",
    lives_in: "\u4F4F\u5728",
    occupation: "\u804C\u4E1A",
    prefers: "\u504F\u597D",
    has: "\u62E5\u6709",
    age: "\u5E74\u9F84",
    has_pet: "\u517B\u5BA0",
    has_family: "\u5BB6\u4EBA",
    habit: "\u4E60\u60EF",
    educated_at: "\u6BD5\u4E1A\u4E8E",
    relationship: "\u4F34\u4FA3",
    family_name: "\u5BB6\u4EBA\u540D\u5B57",
    learning: "\u5728\u5B66",
    uses_os: "\u64CD\u4F5C\u7CFB\u7EDF"
  };
  return Object.entries(grouped).map(([pred, objs]) => `${LABELS[pred] || pred}: ${objs.join("\u3001")}`).join("\uFF1B");
}
function autoExtractFromMemory(content, scope, source) {
  if (["expired", "decayed", "dream", "curiosity", "system"].includes(scope)) return;
  const autoSource = source || (scope === "correction" || scope === "preference" ? "user_said" : "ai_observed");
  const newFacts = extractFacts(content, autoSource);
  if (newFacts.length > 0) addFacts(newFacts);
}
function getAllFacts() {
  return facts;
}
function clearFacts() {
  facts.length = 0;
}
function getFactCount() {
  if (isSQLiteReady()) {
    try {
      return sqliteFactCount();
    } catch {
    }
  }
  return facts.filter((f) => f.validUntil === 0).length;
}
export {
  addFacts,
  autoExtractFromMemory,
  clearFacts,
  extractFacts,
  formatFactTimeline,
  getAllFacts,
  getFactCount,
  getFactSummary,
  queryFactTimeline,
  queryFacts
};
