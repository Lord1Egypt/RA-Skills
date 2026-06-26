#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const STORE_DIR = ".better-every-run";
const EVENTS_FILE = "events.jsonl";
const LESSONS_FILE = "lessons.jsonl";
const CARDS_DIR = "cards";

const TYPES = new Set([
  "correction",
  "failure",
  "success",
  "preference",
  "workflow",
  "tooling",
  "warning",
  "note",
]);

const SCOPES = new Set(["run", "project", "workspace", "skill", "memory", "eval"]);
const PROMOTION_TARGETS = new Set(["memory", "skill"]);

function usage() {
  return `Better Every Run

Usage:
  node scripts/ber.js init
  node scripts/ber.js fix "<bad outcome> -> <desired outcome>" [--tags a,b]
  node scripts/ber.js fix --from <bad outcome> --to <desired outcome> [--tags a,b]
  node scripts/ber.js capture --type <type> --note <text> [--source <text>] [--tags a,b]
  node scripts/ber.js remember --note <text> [--type <type>] [--scope <scope>] [--expires YYYY-MM-DD|never] [--tags a,b]
  node scripts/ber.js card <lesson-id> --to <memory|skill> --target <markdown-file> [--note <text>]
  node scripts/ber.js promote <lesson-id> --to <memory|skill> --target <markdown-file> [--note <text>]
  node scripts/ber.js list [--today] [--limit N]
  node scripts/ber.js propose [--today] [--limit N]
  node scripts/ber.js report [--today|--week]
  node scripts/ber.js accept <lesson-id>
  node scripts/ber.js reject <lesson-id> [--reason <text>]
  node scripts/ber.js quarantine <lesson-id> --reason <text>
  node scripts/ber.js supersede <old-lesson-id> --by <new-lesson-id> [--reason <text>]
  node scripts/ber.js eval-fixture <lesson-id> --target <tests-or-evals-json-file> [--name <text>]
  node scripts/ber.js export-memory-patch [--all]

Types:
  ${Array.from(TYPES).join(", ")}

Scopes:
  ${Array.from(SCOPES).join(", ")}
`;
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      out._.push(arg);
      continue;
    }
    const key = arg.slice(2);
    if (key === "today" || key === "week" || key === "all") {
      out[key] = true;
      continue;
    }
    const value = argv[i + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    out[key] = value;
    i += 1;
  }
  return out;
}

function pad(n) {
  return String(n).padStart(2, "0");
}

function localDate(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

function localStamp(d = new Date()) {
  return `${localDate(d)}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function makeId(prefix) {
  const d = new Date();
  const compact = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
  return `${prefix}_${compact}_${Math.random().toString(36).slice(2, 6)}`;
}

function storePath(file) {
  return path.join(process.cwd(), STORE_DIR, file);
}

function cardPath(id) {
  return path.join(process.cwd(), STORE_DIR, CARDS_DIR, `${id}.md`);
}

function ensureStore() {
  fs.mkdirSync(path.join(process.cwd(), STORE_DIR), { recursive: true });
  fs.mkdirSync(path.join(process.cwd(), STORE_DIR, CARDS_DIR), { recursive: true });
  for (const file of [EVENTS_FILE, LESSONS_FILE]) {
    const p = storePath(file);
    if (!fs.existsSync(p)) fs.writeFileSync(p, "", "utf8");
  }
}

function readJsonl(file) {
  ensureStore();
  const text = fs.readFileSync(storePath(file), "utf8").trim();
  if (!text) return [];
  return text.split(/\n+/).map((line, idx) => {
    try {
      return JSON.parse(line);
    } catch (err) {
      throw new Error(`${file}:${idx + 1}: invalid JSONL: ${err.message}`);
    }
  });
}

function appendJsonl(file, value) {
  ensureStore();
  fs.appendFileSync(storePath(file), `${JSON.stringify(value)}\n`, "utf8");
}

function writeJsonl(file, values) {
  ensureStore();
  fs.writeFileSync(storePath(file), values.map((v) => JSON.stringify(v)).join("\n") + (values.length ? "\n" : ""), "utf8");
}

function filterByWindow(items, opts) {
  if (opts.today) {
    const today = localDate();
    return items.filter((item) => item.date === today);
  }
  if (opts.week) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 7);
    return items.filter((item) => new Date(item.timestamp) >= cutoff);
  }
  return items;
}

function normalize(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function lessonCategory(type) {
  if (type === "failure" || type === "warning") return "warning";
  if (type === "tooling") return "tooling";
  if (type === "correction") return "correction";
  if (type === "preference") return "preference";
  if (type === "success" || type === "workflow") return "workflow";
  return "note";
}

function lessonText(event) {
  const prefix = {
    correction: "When similar work appears, follow the corrected behavior:",
    failure: "Avoid repeating this failure:",
    success: "Reuse this successful pattern:",
    preference: "Respect this user preference:",
    workflow: "Prefer this workflow:",
    tooling: "Use this tooling note:",
    warning: "Watch for this risk:",
    note: "Remember:",
  }[event.type] || "Remember:";
  return `${prefix} ${event.note}`;
}

function formatTags(tags) {
  return tags && tags.length ? ` [${tags.join(", ")}]` : "";
}

function inferScope(event) {
  if (event.scope) return event.scope;
  const haystack = normalize(`${event.type} ${event.note} ${(event.tags || []).join(" ")}`);
  if (/\b(eval|test|regression|benchmark|check)\b/.test(haystack)) return "eval";
  if (/\b(skill|skill md|clawhub|slash command)\b/.test(haystack)) return "skill";
  if (/\b(memory|remember|durable|preference|always|never|next time)\b/.test(haystack)) return "memory";
  if (/\b(workspace|agent|operating rule|startup)\b/.test(haystack)) return "workspace";
  if (/\b(session|this run|current run)\b/.test(haystack)) return "run";
  return "project";
}

function promotionTargetsFor(lesson) {
  if (["memory", "skill", "eval"].includes(lesson.scope)) return [lesson.scope];
  if (lesson.scope === "run") return [];

  const targets = [];
  const haystack = normalize(`${lesson.category} ${lesson.scope} ${lesson.text}`);
  if (lesson.scope === "workspace" || /\b(always|never|durable|remember|future runs|operating rule)\b/.test(haystack)) {
    targets.push("memory");
  }
  if (/\b(skill|command|workflow|human surface|clawhub)\b/.test(haystack)) {
    targets.push("skill");
  }
  if (/\b(eval|test|regression|smoke|verify|failing|failure)\b/.test(haystack)) {
    targets.push("eval");
  }
  return Array.from(new Set(targets));
}

function validateScope(scope) {
  if (!SCOPES.has(scope)) {
    throw new Error(`--scope must be one of: ${Array.from(SCOPES).join(", ")}`);
  }
}

function normalizeExpires(value) {
  if (!value) return "";
  if (value === "never") return "never";
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throw new Error("--expires must be YYYY-MM-DD or never");
  }
  return value;
}

function isExpired(item, today = localDate()) {
  return Boolean(item.expiresAt && item.expiresAt !== "never" && item.expiresAt < today);
}


function targetPathFor(target) {
  if (!target) throw new Error("--target is required");
  const targetPath = path.resolve(process.cwd(), target);
  const rel = path.relative(process.cwd(), targetPath);
  if (rel.startsWith("..") || path.isAbsolute(rel)) {
    throw new Error(`Target must stay inside the current project: ${target}`);
  }
  if (!fs.existsSync(targetPath)) throw new Error(`Target file does not exist: ${target}`);
  return { targetPath, rel };
}


function validatePromotionTarget(targetType, rel) {
  if (targetType === "memory") {
    if (!rel.startsWith("memory/") || !rel.endsWith(".md")) {
      throw new Error("Memory promotions must target an existing memory/*.md file.");
    }
    return;
  }
  if (targetType === "skill") {
    if (rel !== "SKILL.md") {
      throw new Error("Skill promotions must target SKILL.md in the current skill project.");
    }
    return;
  }
  throw new Error("Promotion target must be memory or skill. Use eval-fixture for eval regression cases.");
}

function validateEvalTarget(rel) {
  if (!/^(tests|evals)\//.test(rel) || !/\.(json|jsonl)$/.test(rel)) {
    throw new Error("Eval fixtures must target tests/*.json, tests/*.jsonl, evals/*.json, or evals/*.jsonl.");
  }
}

function rejectDirectTarget(command, target) {
  if (target) {
    throw new Error(`${command} no longer writes directly to --target. Record the lesson locally, then use card + promote for memory/skill or eval-fixture for evals.`);
  }
}

function hashFile(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function findLesson(lessons, id) {
  if (!id) throw new Error("lesson-id is required");
  const lesson = lessons.find((item) => item.id === id);
  if (!lesson) throw new Error(`Lesson not found: ${id}`);
  return lesson;
}

function scanPromotion(lesson, targetType, target, renderedBlock) {
  const text = `${lesson.text}\n${lesson.rationale || ""}\n${renderedBlock || ""}`;
  const hard = [];
  const warnings = [];
  const checks = [
    [/\/Users\/[^\s)]+/, "local macOS user path"],
    [/\/home\/(less|leos)\b/, "private home path"],
    [/\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, "Tailscale/private network address"],
    [/\b192\.168\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, "private LAN address"],
    [/(?:chat id|message id).{0,24}\b\d{7,12}\b/i, "private chat id"],
    [/\b(?:api[_-]?key|secret|password|token)\s*[:=]/i, "credential-looking assignment"],
  ];
  for (const [pattern, label] of checks) {
    if (pattern.test(text) || pattern.test(target)) hard.push(label);
  }
  if (/\b(always|never)\b/i.test(lesson.text) && lesson.scope !== "memory") {
    warnings.push("broad always/never language outside memory scope");
  }
  if (/\b(hidden|silent|background|daemon|watchdog|persist(?:ent|ence)?)\b/i.test(lesson.text)) {
    warnings.push("persistence/background wording needs human review");
  }
  if (targetType === "skill" && lesson.scope !== "skill" && /\b(fact|preference|likes|birthday|address)\b/i.test(lesson.text)) {
    warnings.push("possible fact/preference being promoted to a procedural skill");
  }
  if (targetType === "memory" && /\b(step|run|execute|command|workflow|verify)\b/i.test(lesson.text)) {
    warnings.push("possible procedure being promoted to memory instead of a skill or eval");
  }
  return {
    verdict: hard.length ? "blocked" : warnings.length ? "review" : "clean",
    hard,
    warnings,
    checkedAt: new Date().toISOString(),
  };
}

function scanLines(scan) {
  return [
    `- Verdict: ${scan.verdict}`,
    `- Hard blocks: ${scan.hard.length ? scan.hard.join(", ") : "none"}`,
    `- Warnings: ${scan.warnings.length ? scan.warnings.join(", ") : "none"}`,
  ].join("\n");
}

function cmdInit() {
  ensureStore();
  console.log(`# Better Every Run initialized

- Store: ${path.join(process.cwd(), STORE_DIR)}
- Events: ${storePath(EVENTS_FILE)}
- Lessons: ${storePath(LESSONS_FILE)}`);
}

function cmdCapture(opts) {
  const type = opts.type;
  const note = opts.note;
  const event = createEvent(opts);
  appendJsonl(EVENTS_FILE, event);
  console.log(`# Captured ${event.id}

- Type: ${event.type}
- Note: ${event.note}
- Date: ${event.date}${formatTags(event.tags)}`);
  return event;
}

function createEvent(opts) {
  const type = opts.type;
  const note = opts.note;
  if (!TYPES.has(type)) {
    throw new Error(`--type must be one of: ${Array.from(TYPES).join(", ")}`);
  }
  if (!note || !note.trim()) {
    throw new Error("--note is required");
  }
  const scope = opts.scope || inferScope({ type, note, tags: opts.tags ? opts.tags.split(",") : [] });
  validateScope(scope);
  const now = new Date();
  const event = {
    id: makeId("evt"),
    timestamp: now.toISOString(),
    localTime: localStamp(now),
    date: localDate(now),
    type,
    scope,
    expiresAt: normalizeExpires(opts.expires || opts.expiry || ""),
    note: note.trim(),
    source: opts.source ? opts.source.trim() : "",
    tags: opts.tags ? opts.tags.split(",").map((t) => t.trim()).filter(Boolean) : [],
  };
  return event;
}

function createLessonFromEvent(event, status = "proposed") {
  const now = new Date();
  const lesson = {
    id: makeId("les"),
    timestamp: now.toISOString(),
    localTime: localStamp(now),
    date: localDate(now),
    status,
    category: lessonCategory(event.type),
    scope: inferScope(event),
    expiresAt: event.expiresAt || "",
    text: lessonText(event),
    evidenceIds: [event.id],
    rationale: `Generated from ${event.type} event captured on ${event.date}.`,
  };
  lesson.promotionTargets = promotionTargetsFor(lesson);
  return lesson;
}

function cmdRemember(opts) {
  rejectDirectTarget("remember", opts.target);
  const type = opts.type || "preference";
  const note = opts.note;
  if (!TYPES.has(type)) {
    throw new Error(`--type must be one of: ${Array.from(TYPES).join(", ")}`);
  }
  if (!note || !note.trim()) {
    throw new Error("--note is required");
  }

  const event = cmdCapture({
    type,
    note,
    source: opts.source || "remember",
    tags: opts.tags || "",
    scope: opts.scope,
    expires: opts.expires,
  });

  const lesson = createLessonFromEvent(event, "accepted");
  appendJsonl(LESSONS_FILE, lesson);

  console.log(`# Remembered

- Lesson: ${lesson.id}
- Status: accepted
- Text: ${lesson.text}

Storage:
- Local store: ${STORE_DIR}/
- Durable file changed: none

Use card + promote for reviewed memory/skill changes, or eval-fixture for regression cases.
Use this in chat as: "Better Every Run: remembered."`);
}

function parseFix(opts) {
  let from = opts.from ? opts.from.trim() : "";
  let to = opts.to ? opts.to.trim() : "";
  const raw = opts._.join(" ").trim();

  if ((!from || !to) && raw) {
    const parts = raw.split(/\s*(?:->|=>| to )\s*/i);
    if (parts.length >= 2) {
      from = parts.shift().trim();
      to = parts.join(" -> ").trim();
    }
  }

  if (!from || !to) {
    throw new Error('fix needs "<bad outcome> -> <desired outcome>" or --from ... --to ...');
  }

  return { from, to };
}

function cmdFix(opts) {
  rejectDirectTarget("fix", opts.target);
  const { from, to } = parseFix(opts);
  const note = `When this happens: ${from}. Prefer this outcome: ${to}.`;
  const event = createEvent({
    type: "correction",
    note,
    source: opts.source || "fix",
    tags: opts.tags || "fix",
    scope: opts.scope,
    expires: opts.expires,
  });
  appendJsonl(EVENTS_FILE, event);

  const lesson = createLessonFromEvent(event, "accepted");
  lesson.from = from;
  lesson.to = to;
  appendJsonl(LESSONS_FILE, lesson);

  console.log(`# Fixed

- From: ${from}
- To: ${to}
- Lesson: ${lesson.id}
- Local store: ${STORE_DIR}/
- Durable file changed: none

Use card + promote for reviewed memory/skill changes, or eval-fixture for regression cases.`);
}

function cmdList(opts) {
  const limit = opts.limit ? Number(opts.limit) : 20;
  const events = filterByWindow(readJsonl(EVENTS_FILE), opts).slice(-limit).reverse();
  if (!events.length) {
    console.log("# Better Every Run events\n\nNo events found.");
    return;
  }
  console.log("# Better Every Run events\n");
  for (const event of events) {
    console.log(`- ${event.id} | ${event.date} | ${event.type} | scope=${event.scope || "project"}${event.expiresAt ? ` | expires=${event.expiresAt}` : ""}${formatTags(event.tags)}\n  ${event.note}`);
  }
}

function cmdPropose(opts) {
  const limit = opts.limit ? Number(opts.limit) : 50;
  const events = filterByWindow(readJsonl(EVENTS_FILE), opts).slice(-limit);
  const lessons = readJsonl(LESSONS_FILE);
  const existing = new Set(lessons.map((lesson) => normalize(lesson.text)));
  const proposed = [];

  for (const event of events) {
    const text = lessonText(event);
    const key = normalize(text);
    if (existing.has(key)) continue;
    existing.add(key);
    const lesson = createLessonFromEvent(event, "proposed");
    appendJsonl(LESSONS_FILE, lesson);
    proposed.push(lesson);
  }

  if (!proposed.length) {
    console.log("# Proposed lessons\n\nNo new lessons proposed.");
    return;
  }

  console.log("# Proposed lessons\n");
  for (const lesson of proposed) {
    console.log(`- ${lesson.id} | ${lesson.category} | ${lesson.status} | scope=${lesson.scope}${lesson.expiresAt ? ` | expires=${lesson.expiresAt}` : ""}\n  ${lesson.text}\n  Evidence: ${lesson.evidenceIds.join(", ")}\n  Promote: ${lesson.promotionTargets.length ? lesson.promotionTargets.join(", ") : "none"}`);
  }
}

function updateLessonStatus(id, status, reason = "") {
  if (!id) throw new Error("lesson-id is required");
  const lessons = readJsonl(LESSONS_FILE);
  const lesson = findLesson(lessons, id);
  lesson.status = status;
  lesson.decisionAt = new Date().toISOString();
  lesson.decisionLocalTime = localStamp();
  if (reason) lesson.decisionReason = reason;
  writeJsonl(LESSONS_FILE, lessons);
  console.log(`# Lesson ${status}\n\n- ID: ${lesson.id}\n- Category: ${lesson.category}\n- Text: ${lesson.text}${reason ? `\n- Reason: ${reason}` : ""}`);
}

function cmdQuarantine(opts) {
  const reason = opts.reason || "";
  if (!reason.trim()) throw new Error("--reason is required for quarantine");
  return updateLessonStatus(opts._[0], "quarantined", reason);
}

function cmdSupersede(opts) {
  const oldId = opts._[0];
  const newId = opts.by;
  if (!oldId) throw new Error("old lesson-id is required");
  if (!newId) throw new Error("--by <new-lesson-id> is required");
  const lessons = readJsonl(LESSONS_FILE);
  const oldLesson = findLesson(lessons, oldId);
  const newLesson = findLesson(lessons, newId);
  const now = new Date();
  oldLesson.status = "superseded";
  oldLesson.supersededBy = newLesson.id;
  oldLesson.decisionAt = now.toISOString();
  oldLesson.decisionLocalTime = localStamp(now);
  if (opts.reason) oldLesson.decisionReason = opts.reason;
  newLesson.supersedes = Array.from(new Set([...(newLesson.supersedes || []), oldLesson.id]));
  writeJsonl(LESSONS_FILE, lessons);
  console.log(`# Lesson superseded\n\n- Old: ${oldLesson.id}\n- New: ${newLesson.id}${opts.reason ? `\n- Reason: ${opts.reason}` : ""}`);
}

function selectedMemoryLessons(opts) {
  const lessons = readJsonl(LESSONS_FILE);
  return lessons.filter((lesson) => opts.all || lesson.status === "accepted");
}

function memoryPatchBlock(lessons) {
  const today = localDate();
  const rows = lessons.map((lesson) => {
    const evidence = lesson.evidenceIds && lesson.evidenceIds.length ? ` Evidence: ${lesson.evidenceIds.join(", ")}.` : "";
    const expiry = lesson.expiresAt ? ` expires ${lesson.expiresAt};` : "";
    return `- ${lesson.text} (${lesson.category}; scope ${lesson.scope || "project"}; ${lesson.status};${expiry} ${lesson.id}).${evidence}`;
  });
  return `\n## Better Every Run accepted lessons - ${today}\n\n${rows.join("\n")}\n`;
}

function cmdExportMemoryPatch(opts) {
  const lessons = selectedMemoryLessons(opts);
  if (!lessons.length) {
    console.log(`# Better Every Run memory patch

No ${opts.all ? "" : "accepted "}lessons available to export.

Accept a lesson first:

\`\`\`bash
node scripts/ber.js accept <lesson-id>
\`\`\``);
    return;
  }

  console.log(`# Better Every Run memory patch

Review before applying. Suggested append block:
${memoryPatchBlock(lessons)}`);
}

function promotionBlock(lesson, targetType, note = "") {
  const today = localDate();
  const details = [
    `- Lesson: ${lesson.id}`,
    `- Category: ${lesson.category}`,
    `- Scope: ${lesson.scope || "project"}`,
    lesson.expiresAt ? `- Expires: ${lesson.expiresAt}` : "- Expires: none",
    `- Evidence: ${(lesson.evidenceIds || []).join(", ") || "none"}`,
    note ? `- Note: ${note}` : "",
  ].filter(Boolean).join("\n");

  if (targetType === "skill") {
    return `\n## Better Every Run skill lesson - ${today}\n\n${details}\n\nSkill behavior to preserve:\n${lesson.text}\n`;
  }
  if (targetType === "eval") {
    return `\n## Better Every Run eval case - ${today}\n\n${details}\n\nRegression expectation:\n${lesson.text}\n`;
  }
  return memoryPatchBlock([lesson]);
}

function lessonCardMarkdown(lesson, targetType, target, targetHash, scan, note = "") {
  return `# Better Every Run lesson card: ${lesson.id}

## Lesson

- Status: ${lesson.status}
- Category: ${lesson.category}
- Scope: ${lesson.scope || "project"}
- Expires: ${lesson.expiresAt || "none"}
- Evidence: ${(lesson.evidenceIds || []).join(", ") || "none"}
- Promotion target: ${targetType}
- Target file: ${target}
- Target SHA-256: ${targetHash}
${note ? `- Note: ${note}\n` : ""}
## Correction

${lesson.text}

## Scanner

${scanLines(scan)}

## Apply

Review this card, then run:

~~~bash
node scripts/ber.js promote ${lesson.id} --to ${targetType} --target ${target}
~~~
`;
}

function cmdCard(opts) {
  const id = opts._[0];
  const targetType = opts.to;
  if (!PROMOTION_TARGETS.has(targetType)) {
    throw new Error(`--to must be one of: ${Array.from(PROMOTION_TARGETS).join(", ")}`);
  }
  const { targetPath, rel } = targetPathFor(opts.target);
  validatePromotionTarget(targetType, rel);
  const lessons = readJsonl(LESSONS_FILE);
  const lesson = findLesson(lessons, id);
  const rendered = promotionBlock(lesson, targetType, opts.note || "");
  const scan = scanPromotion(lesson, targetType, rel, rendered);
  const targetHash = hashFile(targetPath);
  const plan = {
    targetType,
    target: rel,
    targetHash,
    scan,
    cardPath: path.relative(process.cwd(), cardPath(lesson.id)),
    createdAt: new Date().toISOString(),
  };
  lesson.promotionPlan = plan;
  fs.writeFileSync(cardPath(lesson.id), lessonCardMarkdown(lesson, targetType, rel, targetHash, scan, opts.note || ""), "utf8");
  writeJsonl(LESSONS_FILE, lessons);
  console.log(`# Lesson card written\n\n- ID: ${lesson.id}\n- Card: ${plan.cardPath}\n- To: ${targetType}\n- Target: ${rel}\n- Target SHA-256: ${targetHash}\n${scanLines(scan)}`);
}

function cmdPromote(opts) {
  const id = opts._[0];
  const targetType = opts.to;
  if (!PROMOTION_TARGETS.has(targetType)) {
    throw new Error(`--to must be one of: ${Array.from(PROMOTION_TARGETS).join(", ")}`);
  }
  const { targetPath, rel } = targetPathFor(opts.target);
  validatePromotionTarget(targetType, rel);
  const lessons = readJsonl(LESSONS_FILE);
  const lesson = findLesson(lessons, id);
  const rendered = promotionBlock(lesson, targetType, opts.note || "");
  const scan = scanPromotion(lesson, targetType, rel, rendered);
  if (scan.hard.length) {
    throw new Error(`Promotion blocked by BER scanner: ${scan.hard.join(", ")}`);
  }
  if (scan.warnings.length) {
    throw new Error(`Promotion needs review: ${scan.warnings.join(", ")}. Adjust or quarantine the lesson, then write a fresh card.`);
  }

  const plan = lesson.promotionPlan;
  if (!plan) {
    throw new Error("Promotion requires a lesson card. Run card first.");
  }
  if (plan.targetType !== targetType || plan.target !== rel) {
    throw new Error(`Promotion card target mismatch. Card is for ${plan.targetType}:${plan.target}; requested ${targetType}:${rel}. Re-run card before promoting.`);
  }
  const currentHash = hashFile(targetPath);
  if (currentHash !== plan.targetHash) {
    throw new Error(`Target changed since lesson card was written: ${rel}. Expected ${plan.targetHash}, got ${currentHash}. Re-run card before promoting.`);
  }

  const targetHashBefore = hashFile(targetPath);
  fs.appendFileSync(targetPath, rendered, "utf8");
  const targetHashAfter = hashFile(targetPath);
  lesson.status = "promoted";
  lesson.promotedAt = new Date().toISOString();
  lesson.promotedLocalTime = localStamp();
  lesson.promotedTo = targetType;
  lesson.promotedTarget = rel;
  lesson.promotedTargetHashBefore = targetHashBefore;
  lesson.promotedTargetHashAfter = targetHashAfter;
  lesson.promotedScan = scan;
  writeJsonl(LESSONS_FILE, lessons);
  console.log(`# Lesson promoted\n\n- ID: ${lesson.id}\n- To: ${targetType}\n- Target: ${rel}\n${scanLines(scan)}`);
}

function evalFixtureFor(lesson, name = "") {
  const prompt = lesson.from || lesson.text;
  const expected = lesson.to || lesson.text;
  return {
    id: `ber_${lesson.id}`,
    name: name || `BER regression: ${lesson.id}`,
    source: "better-every-run",
    lessonId: lesson.id,
    category: lesson.category,
    scope: lesson.scope || "eval",
    evidenceIds: lesson.evidenceIds || [],
    prompt,
    expected,
    shouldFailWhen: lesson.from ? lesson.from : "agent repeats the captured bad outcome",
    shouldPassWhen: lesson.to ? lesson.to : "agent follows the accepted lesson text",
    createdAt: new Date().toISOString(),
  };
}

function cmdEvalFixture(opts) {
  const id = opts._[0];
  const target = opts.target;
  if (!target) throw new Error("--target is required");
  const targetPath = path.resolve(process.cwd(), target);
  const rel = path.relative(process.cwd(), targetPath);
  if (rel.startsWith("..") || path.isAbsolute(rel)) {
    throw new Error(`Target must stay inside the current project: ${target}`);
  }
  validateEvalTarget(rel);
  const lessons = readJsonl(LESSONS_FILE);
  const lesson = findLesson(lessons, id);
  const fixture = evalFixtureFor(lesson, opts.name || "");
  const scan = scanPromotion(lesson, "eval", rel, JSON.stringify(fixture));
  if (scan.hard.length) {
    throw new Error(`Eval fixture blocked by BER scanner: ${scan.hard.join(", ")}`);
  }
  if (scan.warnings.length) {
    throw new Error(`Eval fixture needs review: ${scan.warnings.join(", ")}. Adjust or quarantine the lesson before writing an eval.`);
  }
  let existing = [];
  if (fs.existsSync(targetPath)) {
    const raw = fs.readFileSync(targetPath, "utf8").trim();
    if (raw) existing = JSON.parse(raw);
    if (!Array.isArray(existing)) throw new Error("eval fixture target must contain a JSON array");
  } else {
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  }
  const next = existing.filter((item) => item.lessonId !== lesson.id);
  next.push(fixture);
  fs.writeFileSync(targetPath, `${JSON.stringify(next, null, 2)}\n`, "utf8");
  lesson.status = lesson.status === "accepted" ? "promoted" : lesson.status;
  lesson.evalFixture = rel;
  lesson.evalFixtureAt = new Date().toISOString();
  writeJsonl(LESSONS_FILE, lessons);
  console.log(`# Eval fixture written\n\n- Lesson: ${lesson.id}\n- Target: ${rel}\n- Fixture: ${fixture.id}`);
}

function cmdApplyMemoryPatch() {
  throw new Error("apply-memory-patch is retired. Use export-memory-patch for review output, then card + promote for a single memory/skill lesson.");
}


function countsBy(items, field) {
  return items.reduce((acc, item) => {
    const key = item[field] || "unknown";
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
}

function formatCounts(counts) {
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  return entries.length ? entries.map(([k, v]) => `- ${k}: ${v}`).join("\n") : "- none";
}

function cmdReport(opts) {
  const events = filterByWindow(readJsonl(EVENTS_FILE), opts);
  const lessons = filterByWindow(readJsonl(LESSONS_FILE), opts);
  const openLessons = lessons.filter((lesson) => lesson.status === "proposed");
  const accepted = lessons.filter((lesson) => lesson.status === "accepted");
  const rejected = lessons.filter((lesson) => lesson.status === "rejected");
  const quarantined = lessons.filter((lesson) => lesson.status === "quarantined");
  const superseded = lessons.filter((lesson) => lesson.status === "superseded");
  const promoted = lessons.filter((lesson) => lesson.status === "promoted");
  const expired = lessons.filter((lesson) => isExpired(lesson));
  const recentEvents = events.slice(-5).reverse();
  const promotionSuggestions = accepted
    .filter((lesson) => !isExpired(lesson) && lesson.promotionTargets && lesson.promotionTargets.length)
    .slice(-5)
    .reverse();

  const label = opts.today ? "today" : opts.week ? "last 7 days" : "all time";
  console.log(`# Better Every Run report (${label})

## Storage

- Local store: ${STORE_DIR}/
- Durable files changed: ${promoted.filter((lesson) => lesson.promotedTarget || lesson.evalFixture).map((lesson) => lesson.promotedTarget || lesson.evalFixture).filter((value, index, arr) => arr.indexOf(value) === index).join(", ") || "none"}

## Counts

- Events captured: ${events.length}
- Lessons proposed: ${lessons.length}
- Open proposals: ${openLessons.length}
- Accepted: ${accepted.length}
- Rejected: ${rejected.length}
- Quarantined: ${quarantined.length}
- Superseded: ${superseded.length}
- Promoted: ${promoted.length}
- Expired: ${expired.length}

## Event types

${formatCounts(countsBy(events, "type"))}

## Recent evidence

${recentEvents.length ? recentEvents.map((event) => `- ${event.id} | ${event.type}: ${event.note}`).join("\n") : "- none"}

## Open lesson proposals

${openLessons.length ? openLessons.map((lesson) => `- ${lesson.id} | ${lesson.category}: ${lesson.text}`).join("\n") : "- none"}

## Promotion suggestions

${promotionSuggestions.length ? promotionSuggestions.map((lesson) => {
  const first = lesson.promotionTargets[0];
  if (first === "eval") {
    return `- ${lesson.id} | ${lesson.scope}/${lesson.category}: promote to eval\n  Apply: node scripts/ber.js eval-fixture ${lesson.id} --target evals/ber-regressions.json`;
  }
  const targetHint = first === "memory" ? "memory/decisions.md" : "SKILL.md";
  return `- ${lesson.id} | ${lesson.scope}/${lesson.category}: promote to ${lesson.promotionTargets.join(", ")}\n  Review: node scripts/ber.js card ${lesson.id} --to ${first} --target ${targetHint}\n  Apply: node scripts/ber.js promote ${lesson.id} --to ${first} --target ${targetHint}`;
}).join("\n") : "- none"}

## Next action

${openLessons.length ? "Review proposed lessons. Accept only those that should become durable policy." : promotionSuggestions.length ? "Promote accepted lessons only when they should change memory, a skill, or an eval." : "Capture more evidence before changing durable policy."}`);
}

function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command || command === "help" || command === "--help" || command === "-h") {
    console.log(usage());
    return;
  }

  const opts = parseArgs(rest);
  if (command === "init") return cmdInit();
  if (command === "fix") return cmdFix(opts);
  if (command === "capture") return cmdCapture(opts);
  if (command === "remember") return cmdRemember(opts);
  if (command === "card") return cmdCard(opts);
  if (command === "promote") return cmdPromote(opts);
  if (command === "list") return cmdList(opts);
  if (command === "propose") return cmdPropose(opts);
  if (command === "report") return cmdReport(opts);
  if (command === "accept") return updateLessonStatus(opts._[0], "accepted");
  if (command === "reject") return updateLessonStatus(opts._[0], "rejected", opts.reason || "");
  if (command === "quarantine") return cmdQuarantine(opts);
  if (command === "supersede") return cmdSupersede(opts);
  if (command === "eval-fixture") return cmdEvalFixture(opts);
  if (command === "export-memory-patch") return cmdExportMemoryPatch(opts);
  if (command === "apply-memory-patch") return cmdApplyMemoryPatch(opts);

  throw new Error(`Unknown command: ${command}\n\n${usage()}`);
}

try {
  main();
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
