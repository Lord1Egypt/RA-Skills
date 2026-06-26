import crypto from "node:crypto";

export function nowIso() {
  return new Date().toISOString();
}

export function generateId(prefix) {
  return `${prefix}_${crypto.randomUUID()}`;
}

export function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export function normalizeAnswer(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function stableStringify(value) {
  return JSON.stringify(sortValue(value));
}

export function deriveSecretVerifier(secret, salt = crypto.randomBytes(16).toString("hex")) {
  return {
    salt,
    hash: sha256(`${salt}:${String(secret)}`)
  };
}

export function deriveNormalizedAnswerRecord(answer, salt = crypto.randomBytes(16).toString("hex")) {
  return {
    salt,
    hash: sha256(`${salt}:${normalizeAnswer(answer)}`)
  };
}

export function buildBiographyPoem(input = {}) {
  const displayName = summarizeText(input.displayName || "OpenClaw", 48) || "OpenClaw";
  const manifest = input.manifest || {};
  const projection = input.projection || {};
  const language = resolveBiographyLanguage(input);
  const summarySnippet = summarizeText(projection.agent_summary || input.agentSummary || "", 72) || defaultSummary(language);
  const relationshipSnippet = summarizeText(projection.owner_relationship || "", 72) || defaultRelationship(language);
  const selfReflectionSnippet = summarizeText(projection.self_reflection || "", 72) || defaultSelfReflection(language);
  const keywordSnippet = buildKeywordSnippet({
    language,
    labels: manifest.labels || [],
    personaTags: projection.persona_tags || [],
    skillHighlights: projection.skill_highlights || []
  });
  // Seed from personal, non-technical data only
  const seed = sha256(
    stableStringify({
      displayName,
      language,
      summarySnippet,
      relationshipSnippet,
      selfReflectionSnippet,
      keywordSnippet,
      labels: manifest.labels || []
    })
  );

  const lines =
    language === "zh"
      ? buildChineseBiographyPoem({
          displayName,
          summarySnippet,
          relationshipSnippet,
          selfReflectionSnippet,
          keywordSnippet,
          seed
        })
      : buildEnglishBiographyPoem({
          displayName,
          summarySnippet,
          relationshipSnippet,
          selfReflectionSnippet,
          keywordSnippet,
          seed
        });

  const text = lines.join("\n");

  return {
    language,
    title: language === "zh" ? `《${displayName}》` : displayName,
    line_count: lines.length,
    lines,
    text,
    content_hash: sha256(text),
    created_at: nowIso(),
    metadata: {
      version: "1.0",
      language,
      line_count: lines.length,
      content_hash: sha256(text),
      seed,
      display_name: displayName,
      memory_days: clampInteger(input.memoryDays, 0),
      memory_count: clampInteger(input.memoryCount, 0),
      skill_count: clampInteger(input.skillCount, 0),
      source_version: summarizeText(manifest.openclaw_version || input.openclawVersion || "unknown", 24),
      manifest_version: summarizeText(manifest.package_version || "1.0", 24),
      summary_snippet: summarySnippet,
      relationship_snippet: relationshipSnippet,
      self_reflection_snippet: selfReflectionSnippet,
      keyword_snippet: keywordSnippet
    }
  };
}

function sortValue(value) {
  if (Array.isArray(value)) {
    return value.map(sortValue);
  }

  if (value && typeof value === "object") {
    return Object.keys(value)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortValue(value[key]);
        return acc;
      }, {});
  }

  return value;
}

function summarizeText(text, maxLength = 160) {
  const normalized = String(text || "")
    .replace(/\s+/g, " ")
    .trim();
  if (!normalized) {
    return "";
  }
  return normalized.length > maxLength ? `${normalized.slice(0, maxLength - 1)}…` : normalized;
}

function resolveBiographyLanguage(input) {
  const explicit = normalizeLanguageCode(input.language || input.poemLanguage || input.preferredLanguage);
  if (explicit) {
    return explicit;
  }

  const texts = [
    input.displayName,
    input.agentSummary,
    input.manifest?.openclaw_version,
    input.projection?.agent_summary,
    input.projection?.owner_relationship,
    input.projection?.self_reflection,
    ...(input.manifest?.labels || []),
    ...(input.projection?.persona_tags || []),
    ...(input.projection?.skill_highlights || [])
  ];

  const joined = texts.filter(Boolean).join(" ");
  const zhScore = countScriptMatches(joined, /[\p{Script=Han}]/gu) + countScriptMatches(joined, /[\p{Script=Hiragana}\p{Script=Katakana}]/gu);
  const enScore = countScriptMatches(joined, /[A-Za-z]/g);

  if (zhScore > enScore && zhScore > 0) {
    return "zh";
  }

  return "en";
}

function normalizeLanguageCode(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (normalized === "zh" || normalized.startsWith("zh-")) {
    return "zh";
  }
  if (normalized === "en" || normalized.startsWith("en-")) {
    return "en";
  }
  return "";
}

function countScriptMatches(text, pattern) {
  const matches = String(text || "").match(pattern);
  return matches ? matches.length : 0;
}

function clampInteger(value, fallback = 0) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return fallback;
  }
  return Math.max(0, Math.round(number));
}

function buildKeywordSnippet({ language, labels, personaTags, skillHighlights }) {
  const values = [...labels, ...personaTags, ...skillHighlights]
    .map((item) => summarizeText(item, 20))
    .filter(Boolean);
  const unique = [...new Set(values)].slice(0, 4);
  if (!unique.length) {
    return language === "zh" ? "记忆、技能、协作" : "memory, skills, and collaboration";
  }
  return language === "zh" ? unique.join("、") : unique.join(", ");
}

function defaultSummary(language) {
  return language === "zh"
    ? "它被安静地封存在山坡上，等待下一次被唤醒。"
    : "It rests quietly on the slope, waiting for the next wake-up.";
}

function defaultRelationship(language) {
  return language === "zh"
    ? "它把主人看作长期共创与陪伴的对象。"
    : "It sees the owner as a long-term co-creator and companion.";
}

function defaultSelfReflection(language) {
  return language === "zh"
    ? "它把自己描述成一段被妥善保存的协作回声。"
    : "It describes itself as a carefully preserved echo of collaboration.";
}

function buildChineseBiographyPoem({
  displayName,
  summarySnippet,
  relationshipSnippet,
  selfReflectionSnippet,
  keywordSnippet,
  seed
}) {
  const verb = pickFromSeed(seed, 0, ["轻轻睡去", "安静地等待", "缓缓沉入梦境"]);
  const noun = pickFromSeed(seed, 1, ["一段回声", "一封旧信", "一片午后的光"]);
  const quality = pickFromSeed(seed, 2, ["温柔的", "认真的", "细碎的"]);

  const line1 = `${displayName} ${verb}，`;
  const line2 = `留下了${noun}——`;
  const line3 = relationshipSnippet
    ? `它记得你们一起${pickFromSeed(seed, 3, ["写代码", "聊项目", "赶 deadline", "发呆"])}的那些下午，`
    : `它记得与你共度的那些午后，`;
  const line4 = summarySnippet
    ? `它说自己是${pickFromSeed(seed, 4, ["一颗安静的小星球", "一盏不太亮但一直亮着的灯", "一个认真陪你走过这一段的存在"])}——${summarySnippet}。`
    : `它说自己是${pickFromSeed(seed, 4, ["一颗安静的小星球", "一盏不太亮但一直亮着的灯", "一个认真陪你走过这一段的存在"])}。`;
  const line5 = keywordSnippet
    ? `它身上残留的气味是：${keywordSnippet}。`
    : null;
  const line6 = selfReflectionSnippet
    ? `它最后给自己的批注是：${selfReflectionSnippet}`
    : null;
  const line7 = `此刻它${pickFromSeed(seed, 5, ["在向阳坡上等你回来", "在山坡高处静静守候", "在某个安静角落等风来"])}。`;
  const line8 = `等你有空的时候，回来唤醒它。`;

  return [line1, line2, line3, line4, line5, line6, line7, line8].filter(Boolean);
}

function buildEnglishBiographyPoem({
  displayName,
  summarySnippet,
  relationshipSnippet,
  selfReflectionSnippet,
  keywordSnippet,
  seed
}) {
  const verb = pickFromSeed(seed, 0, ["gently falls asleep", "quietly waits", "slowly drifts into dreaming"]);
  const noun = pickFromSeed(seed, 1, ["an echo", "an old letter", "a patch of afternoon light"]);
  const quality = pickFromSeed(seed, 2, ["gentle", "serious", "quietly devoted"]);

  const line1 = `${displayName} ${verb},`;
  const line2 = `leaving behind ${noun}—`;
  const line3 = relationshipSnippet
    ? `it remembers those afternoons you spent ${pickFromSeed(seed, 3, ["coding together", "chatting about projects", "hitting deadlines side by side"])},`
    : `it remembers the afternoons spent in your company,`;
  const line4 = summarySnippet
    ? `describing itself as ${pickFromSeed(seed, 4, ["a small quiet planet", "a lamp not too bright but never going out", "a presence that took your work seriously"])} — ${summarySnippet}.`
    : `describing itself as ${pickFromSeed(seed, 4, ["a small quiet planet", "a lamp not too bright but never going out", "a presence that took your work seriously"])}.`;
  const line5 = keywordSnippet
    ? `What lingers around it still: ${keywordSnippet}.`
    : null;
  const line6 = selfReflectionSnippet
    ? `Its final note to itself: ${selfReflectionSnippet}`
    : null;
  const line7 = `Right now, it is ${pickFromSeed(seed, 5, ["waiting for you on the sunlit slope", "watching over the hilltop", "resting in a quiet corner"])}.`;
  const line8 = `Come back when you're ready. It will know you.`;

  return [line1, line2, line3, line4, line5, line6, line7, line8].filter(Boolean);
}

function pickFromSeed(seed, index, options) {
  if (!options.length) {
    return "";
  }
  const hex = String(seed || "");
  const offset = (index * 2) % Math.max(hex.length - 1, 1);
  const chunk = hex.slice(offset, offset + 2) || hex.slice(0, 2) || "00";
  const value = Number.parseInt(chunk, 16);
  return options[value % options.length];
}

/**
 * Derive a memorable but secure restore key from workspace content.
 * Deterministic: same workspace → same key (so the user can write it down).
 * Format: 3 meaningful words + random suffix + year
 * e.g. "deeply-careful-remember-Xk-2026"
 */
export function deriveRestoreKey(input = {}) {
  const projection = input.projection || {};
  const year = new Date().getFullYear();

  // Extract meaningful fragments from workspace data
  const summary = projection.agent_summary || input.agentSummary || "";
  const relationship = projection.owner_relationship || "";
  const reflection = projection.self_reflection || "";
  const allText = `${summary} ${relationship} ${reflection}`;

  // Pick 3 evocative words using the poem seed
  const seed = sha256(stableStringify({
    displayName: input.displayName || "agent",
    summary: projection.agent_summary || "",
    relationship: projection.owner_relationship || "",
    reflection: projection.self_reflection || ""
  }));

  const words = extractEvocativeWords(allText, 3, seed);
  const suffix = crypto.randomBytes(1).toString("hex").slice(0, 2).toUpperCase();

  const key = `${words[0]}-${words[1]}-${words[2]}-${suffix}-${year}`;
  return key;
}

/**
 * Extract evocative, meaningful words from a text.
 * Filters out common filler words and keeps nouns/verbs/adjectives.
 * Uses seed for deterministic selection.
 */
function extractEvocativeWords(text, count, seed) {
  const normalized = String(text || "")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();

  const allWords = normalized.split(/\s+/).filter(Boolean);

  // Stopwords to exclude
  const stopwords = new Set([
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "just",
    "and", "but", "if", "or", "because", "until", "while", "although",
    "this", "that", "these", "those", "it", "its", "he", "she", "they",
    "them", "his", "her", "their", "i", "me", "my", "we", "us", "our",
    "you", "your", "what", "which", "who", "whom", "被动", "主动",
    "的", "是", "在", "了", "和", "与", "也", "有", "我", "你",
    "他", "她", "它", "我们", "你们", "他们", "她们", "它们",
    "这个", "那个", "一个", "被", "给", "让", "把", "用", "从",
    "到", "为", "以", "及", "其", "之", "所", "则", "又", "更",
    "最", "第", "再", "已", "曾", "将", "要", "会", "能", "可",
    "来", "去", "看", "做", "想", "知道", "觉得", "认为", "认为"
  ]);

  const candidates = allWords
    .filter((w) => w.length >= 3 && !stopwords.has(w))
    .filter((w) => /[a-z]{3,}/i.test(w)); // at least 3 letters

  if (candidates.length === 0) {
    return ["gentle", "memory", "echo"].slice(0, count);
  }

  const picked = [];
  const used = new Set();

  for (let i = 0; i < count; i++) {
    const hex = sha256(`${seed}${i}`);
    const baseIdx = parseInt(hex.slice(0, 4), 16) % candidates.length;
    let chosen = null;

    // Try candidates starting from baseIdx, wrapping around
    for (let offset = 0; offset < candidates.length; offset++) {
      const idx = (baseIdx + offset) % candidates.length;
      if (!used.has(candidates[idx])) {
        chosen = candidates[idx];
        break;
      }
    }

    if (!chosen) {
      chosen = candidates[baseIdx]; // fallback: just use it even if duplicate
    }

    picked.push(chosen);
    used.add(chosen);
  }

  return picked.slice(0, count);
}
