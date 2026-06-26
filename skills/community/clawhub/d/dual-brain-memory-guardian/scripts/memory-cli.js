#!/usr/bin/env node
import {
  appendFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync
} from "node:fs";
import path from "node:path";

const VALUE_KEYS = new Set([
  "type",
  "content",
  "content-file",
  "summary",
  "summary-file",
  "outcome",
  "hard-rule",
  "domain",
  "project",
  "task",
  "query-file",
  "resolution",
  "resolution-file",
  "tags",
  "metadata",
  "metadata-file",
  "tenant",
  "query",
  "top-k",
  "promoted",
  "promoted-at",
  "max-content-chars",
  "uri",
  "error-mode",
  "integration-id",
  "id",
  "limit",
  "pagination-token",
  "wait"
]);

const TRIGGER_STATE_FILE = path.join(process.cwd(), ".memory-trigger-state.json");
const MAX_TRIGGER_SESSION_AGE_MS = 12 * 60 * 60 * 1000;
const DEFAULT_RECALL_CONTENT_MAX_CHARS = 1000;
const LOCAL_MEMORY_HOME_DIR = "dual-brain-memory-guardian";
const USER_HOME_ROOT = process.env.HOME || process.env.USERPROFILE || process.cwd();
const DEFAULT_LOCAL_MEMORY_ROOT = path.join(USER_HOME_ROOT, LOCAL_MEMORY_HOME_DIR);
const HOT_MEMORY_FILE = "memory.md";
const REFLECTIONS_FILE = "reflections.md";
const PROMOTION_SECTION = "## Recent Promotions (auto)";
const HOT_MEMORY_BOOTSTRAP = [
  "# Dual-Brain Memory",
  "",
  "## Confirmed Preferences",
  "- (add explicit durable rules here)",
  "",
  "## Active Patterns",
  "- (add repeated validated patterns here)",
  "",
  "## Recent Promotions (last 7 days)",
  "- (none yet)",
  ""
].join("\n");
const REFLECTIONS_BOOTSTRAP = [
  "# Self-Reflections Log",
  "",
  "Track self-reflections from completed work.",
  "",
  "## Format",
  "- What I did",
  "- Outcome",
  "- Reflection",
  "- DEEP Event",
  "- Promotion",
  ""
].join("\n");

function parseArgs(argv) {
  const parsed = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith("--")) {
      parsed._.push(item);
      continue;
    }

    const argBody = item.slice(2);
    const eqIndex = argBody.indexOf("=");
    if (eqIndex > -1) {
      const key = argBody.slice(0, eqIndex);
      const value = argBody.slice(eqIndex + 1);
      parsed[key] = value;
      continue;
    }

    const key = argBody;
    const next = argv[i + 1];

    if (!next) {
      parsed[key] = true;
      continue;
    }

    // Known value-taking keys should consume the next token even if it starts with `--`.
    if (VALUE_KEYS.has(key)) {
      parsed[key] = next;
      i += 1;
      continue;
    }

    if (next.startsWith("--")) {
      parsed[key] = true;
      continue;
    }

    parsed[key] = next;
    i += 1;
  }

  return parsed;
}

function usage() {
  return [
    "Usage:",
    "  npm run memory:init",
    "  npm run memory:session-start -- --task \"...\" [--project my-app] [--domain code] [--top-k 3] [--query-file ./query.txt] [--max-content-chars 1000]",
    "  npm run memory:auto-session-start -- --task \"...\" [--project my-app] [--domain code] [--top-k 3] [--query-file ./query.txt] [--max-content-chars 1000] [--force]",
    "  npm run memory:on-correction -- --content \"...\" [--content-file ./correction.txt] [--project my-app] [--domain code] [--allow-without-session-start] [--no-markdown-promotion]",
    "  npm run memory:on-task-complete -- --summary \"...\" [--summary-file ./summary.txt] [--outcome success|partial|failed] [--allow-without-session-start] [--no-local-reflection]",
    "  npm run memory:auto-task-complete -- --summary \"...\" [--summary-file ./summary.txt] [--outcome success|partial|failed] [--force]",
    "  npm run memory:save -- --type correction --content \"...\" [--content-file ./content.txt] [--domain code] [--project my-app]",
    "  npm run memory:search -- --query \"...\" [--query-file ./query.txt] [--top-k 3] [--max-content-chars 1000] [--type correction] [--task context] [--promoted true|false]",
    "  npm run memory:mark-promoted -- --id <event-id> [--promoted true|false] [--promoted-at <iso8601>]",
    "  npm run memory:import:start -- --uri s3://bucket/path [--error-mode continue] [--integration-id id]",
    "  npm run memory:import:status -- --id <import-id>",
    "  npm run memory:import:list -- [--limit 20] [--pagination-token token]",
    "  npm run memory:import:cancel -- --id <import-id>",
    "  npm run memory:forget -- [--id <record-id>] [--type correction] [--domain code] [--project my-app] [--task context]",
    "  npm run memory:freshness",
    "  npm run memory:forget-all -- [--tenant default] --yes",
    "",
    "Trigger guard:",
    "  on-correction and on-task-complete require a recent session-start by default.",
    "  auto-session-start skips if a fresh session-start already exists for the same tenant (use --force to re-run).",
    "  auto-task-complete skips if the current session is already completed (use --force to re-run).",
    "  Use --allow-without-session-start only for one-off maintenance or migration tasks.",
    "",
    "File-backed input:",
    "  Prefer --content-file/--summary-file/--query-file for long or quote-heavy text.",
    "",
    "Local markdown brain:",
    "  Root path defaults to ~/dual-brain-memory-guardian (override with DUAL_BRAIN_MEMORY_HOME env var)."
  ].join("\n");
}

function toTags(raw) {
  if (!raw) {
    return [];
  }

  return String(raw)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function parsePositiveInteger(value, flagName) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`${flagName} must be a positive integer.`);
  }

  return parsed;
}

function isAffirmative(value) {
  if (value === true) {
    return true;
  }

  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase();
    return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "y";
  }

  return false;
}

function parseMetadata(raw) {
  if (!raw) {
    return {};
  }

  try {
    return JSON.parse(raw);
  } catch {
    throw new Error("--metadata must be valid JSON.");
  }
}

function parseOptionalBoolean(value, flagName) {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }

  if (value === true || value === false) {
    return value;
  }

  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "y"].includes(normalized)) {
    return true;
  }

  if (["0", "false", "no", "n"].includes(normalized)) {
    return false;
  }

  throw new Error(`${flagName} must be true or false.`);
}

function buildForgetScopeSummary({ ids, args, promotedToMarkdown }) {
  if (ids.length > 0) {
    return `ids(${ids.length})`;
  }

  const filterBits = [
    firstNonEmpty(args.type) ? `type=${firstNonEmpty(args.type)}` : "",
    firstNonEmpty(args.domain) ? `domain=${firstNonEmpty(args.domain)}` : "",
    firstNonEmpty(args.project) ? `project=${firstNonEmpty(args.project)}` : "",
    firstNonEmpty(args.task) ? `task=${firstNonEmpty(args.task)}` : "",
    toTags(args.tags).length ? `tags=${toTags(args.tags).join(",")}` : "",
    typeof promotedToMarkdown === "boolean"
      ? `promoted_to_markdown=${String(promotedToMarkdown)}`
      : ""
  ].filter(Boolean);

  return filterBits.length ? `filter(${filterBits.join(", ")})` : "filter(none)";
}

function emitDeletionReminder({ commandName, tenantId, scope, note = "" }) {
  const safeTenant = normalizeTenantForState(tenantId);
  console.error(
    `[Reminder] ${commandName} is destructive and will permanently delete vector memory.`
  );
  console.error(`[Reminder] tenant=${safeTenant}, scope=${scope}`);
  if (note) {
    console.error(`[Reminder] ${note}`);
  }
  console.error("[Reminder] Confirm user intent before executing data/database deletion.");
}

function extractMissingPackageName(error) {
  const message = String(error?.message || "");
  const match = message.match(/Cannot find package ['"]([^'"]+)['"]/);
  return match ? match[1] : "";
}

function isMissingPackageError(error, packageName = "") {
  if (!error || error.code !== "ERR_MODULE_NOT_FOUND") {
    return false;
  }

  const message = String(error.message || "");
  if (!message.includes("Cannot find package")) {
    return false;
  }

  if (!packageName) {
    return true;
  }

  return (
    message.includes(`Cannot find package '${packageName}'`) ||
    message.includes(`Cannot find package \"${packageName}\"`) ||
    message.includes(`/node_modules/${packageName}/`)
  );
}

function buildMissingDependencyError(error) {
  const packageName = extractMissingPackageName(error);
  if (packageName) {
    return new Error(`Missing dependency "${packageName}". Run "npm install" in the project root, then retry.`);
  }

  return new Error("Missing runtime dependencies. Run \"npm install\" in the project root, then retry.");
}

async function loadRuntimeStoreConstructor() {
  try {
    await import("dotenv/config");
  } catch (error) {
    if (isMissingPackageError(error, "dotenv")) {
      throw buildMissingDependencyError(error);
    }
    throw error;
  }

  try {
    const memoryStoreModule = await import("../src/pinecone/memory-store.js");
    return memoryStoreModule.DualBrainMemoryStore;
  } catch (error) {
    if (isMissingPackageError(error)) {
      throw buildMissingDependencyError(error);
    }
    throw error;
  }
}

function readTextFromArgFile(rawPath, flagName) {
  const inputPath = String(rawPath || "").trim();
  if (!inputPath) {
    throw new Error(`${flagName} requires a file path.`);
  }

  const resolvedPath = path.resolve(process.cwd(), inputPath);
  if (!existsSync(resolvedPath)) {
    throw new Error(`${flagName} file not found: ${resolvedPath}`);
  }

  const content = readFileSync(resolvedPath, "utf8");
  if (!content.trim()) {
    throw new Error(`${flagName} file is empty: ${resolvedPath}`);
  }

  return content;
}

function hydrateFileBackedArgs(args) {
  const textMappings = [
    { fileFlag: "content-file", targetFlag: "content", name: "--content-file" },
    { fileFlag: "summary-file", targetFlag: "summary", name: "--summary-file" },
    { fileFlag: "query-file", targetFlag: "query", name: "--query-file" },
    { fileFlag: "resolution-file", targetFlag: "resolution", name: "--resolution-file" }
  ];

  for (const mapping of textMappings) {
    if (args[mapping.fileFlag] === undefined) {
      continue;
    }

    const text = readTextFromArgFile(args[mapping.fileFlag], mapping.name);
    if (!firstNonEmpty(args[mapping.targetFlag])) {
      args[mapping.targetFlag] = text;
    }
  }

  if (args["metadata-file"] !== undefined) {
    const raw = readTextFromArgFile(args["metadata-file"], "--metadata-file");
    let fileMetadata;
    try {
      fileMetadata = JSON.parse(raw);
    } catch {
      throw new Error("--metadata-file must contain valid JSON.");
    }

    if (!fileMetadata || typeof fileMetadata !== "object" || Array.isArray(fileMetadata)) {
      throw new Error("--metadata-file JSON must be an object.");
    }

    const inlineMetadata = parseMetadata(args.metadata);
    args.metadata = JSON.stringify({
      ...fileMetadata,
      ...inlineMetadata
    });
  }

  return args;
}

function truncateText(value, maxChars) {
  const text = String(value || "");
  if (text.length <= maxChars) {
    return text;
  }

  return `${text.slice(0, maxChars)}...[TRUNCATED]`;
}

function normalizeHitForOutput(hit, maxChars) {
  const source = hit?.fields && typeof hit.fields === "object" ? hit.fields : hit || {};
  const contentCandidate =
    firstNonEmpty(source.content, hit?.content, source.text) ||
    Object.values(source).find((value) => typeof value === "string" && value.length > 120);

  const tagsRaw = source.tags ?? hit?.tags;
  const safeTags = Array.isArray(tagsRaw)
    ? tagsRaw.map((item) => String(item)).slice(0, 16)
    : [];

  return {
    id: String(hit?.id ?? hit?._id ?? source.id ?? ""),
    score: typeof hit?.score === "number" ? hit.score : undefined,
    event_type: source.event_type ?? hit?.event_type ?? "",
    domain: source.domain ?? hit?.domain ?? "",
    project: source.project ?? hit?.project ?? "",
    task_context: source.task_context ?? hit?.task_context ?? "",
    created_at: source.created_at ?? hit?.created_at ?? "",
    promoted_to_markdown:
      source.promoted_to_markdown ?? hit?.promoted_to_markdown ?? undefined,
    tags: safeTags,
    content: truncateText(contentCandidate || "", maxChars)
  };
}

function compactRecallForOutput(result, maxChars) {
  return {
    namespace: result?.namespace || "",
    hits: Array.isArray(result?.hits)
      ? result.hits.map((hit) => normalizeHitForOutput(hit, maxChars))
      : []
  };
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (value === undefined || value === null) {
      continue;
    }

    const text = String(value).trim();
    if (text) {
      return text;
    }
  }

  return "";
}

function normalizeOutcome(raw) {
  const value = String(raw || "success").trim().toLowerCase();

  if (value === "success" || value === "partial" || value === "failed") {
    return value;
  }

  if (value === "fail" || value === "error") {
    return "failed";
  }

  if (value === "partial-success") {
    return "partial";
  }

  return "success";
}

function normalizeInlineText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function scopeSlug(value) {
  const slug = normalizeInlineText(value)
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");

  return slug || "general";
}

function ensureFileIfMissing(filePath, initialContent) {
  if (!existsSync(filePath)) {
    writeFileSync(filePath, initialContent, "utf8");
  }
}

function resolveLocalMemoryRoot() {
  const explicitPath = process.env.DUAL_BRAIN_MEMORY_HOME;
  if (explicitPath) {
    return path.resolve(explicitPath);
  }

  return DEFAULT_LOCAL_MEMORY_ROOT;
}

function ensureLocalMemoryLayout(memoryRoot) {
  mkdirSync(memoryRoot, { recursive: true });
  mkdirSync(path.join(memoryRoot, "projects"), { recursive: true });
  mkdirSync(path.join(memoryRoot, "domains"), { recursive: true });

  ensureFileIfMissing(path.join(memoryRoot, HOT_MEMORY_FILE), HOT_MEMORY_BOOTSTRAP);
  ensureFileIfMissing(path.join(memoryRoot, REFLECTIONS_FILE), REFLECTIONS_BOOTSTRAP);
}

function readMarkdownSummary(filePath, scope) {
  const content = readFileSync(filePath, "utf8");
  return {
    scope,
    filePath,
    lineCount: content.split(/\r?\n/).length,
    content
  };
}

function findSmallestMatchingWarmFile(baseDir, scopeValue) {
  if (!scopeValue || !existsSync(baseDir)) {
    return "";
  }

  const target = scopeSlug(scopeValue);
  const entries = readdirSync(baseDir, { withFileTypes: true }).filter(
    (entry) => entry.isFile() && entry.name.toLowerCase().endsWith(".md")
  );

  const candidates = entries
    .map((entry) => {
      const fileStem = scopeSlug(path.parse(entry.name).name);
      const exact = fileStem === target;
      const fuzzy = fileStem.includes(target) || target.includes(fileStem);
      if (!exact && !fuzzy) {
        return null;
      }

      const fullPath = path.join(baseDir, entry.name);
      return {
        fullPath,
        score: exact ? 2 : 1,
        size: readFileSync(fullPath, "utf8").length,
        name: entry.name
      };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score || a.size - b.size || a.name.localeCompare(b.name));

  return candidates[0]?.fullPath || "";
}

function extractRulePreview(content, max = 5) {
  return content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .slice(0, max);
}

function loadLeftBrainContext(args) {
  const memoryRoot = resolveLocalMemoryRoot();
  ensureLocalMemoryLayout(memoryRoot);

  const loadedFiles = [];
  const missingWarmFiles = [];

  loadedFiles.push(readMarkdownSummary(path.join(memoryRoot, HOT_MEMORY_FILE), "hot"));

  if (args.domain) {
    const domainPath = findSmallestMatchingWarmFile(path.join(memoryRoot, "domains"), args.domain);
    if (domainPath) {
      loadedFiles.push(readMarkdownSummary(domainPath, "domain"));
    } else {
      missingWarmFiles.push(`domains/${scopeSlug(args.domain)}.md`);
    }
  }

  if (args.project) {
    const projectPath = findSmallestMatchingWarmFile(path.join(memoryRoot, "projects"), args.project);
    if (projectPath) {
      loadedFiles.push(readMarkdownSummary(projectPath, "project"));
    } else {
      missingWarmFiles.push(`projects/${scopeSlug(args.project)}.md`);
    }
  }

  const rulePreview = loadedFiles
    .flatMap((item) =>
      extractRulePreview(item.content).map((rule) => `${item.scope}:${rule.replace(/^-\s*/, "")}`)
    )
    .slice(0, 12);

  return {
    memoryRoot,
    loadedFiles: loadedFiles.map((item) => ({
      scope: item.scope,
      filePath: item.filePath,
      lineCount: item.lineCount
    })),
    missingWarmFiles,
    rulePreview
  };
}

function ensureScopedRuleFile(memoryRoot, scopeName, scopeType) {
  const slug = scopeSlug(scopeName);
  const dirName = scopeType === "project" ? "projects" : "domains";
  const scopedDir = path.join(memoryRoot, dirName);
  mkdirSync(scopedDir, { recursive: true });

  const filePath = path.join(scopedDir, `${slug}.md`);
  const titlePrefix = scopeType === "project" ? "Project Rules" : "Domain Rules";
  const initial = `# ${titlePrefix}: ${normalizeInlineText(scopeName)}\n\n## Confirmed Rules\n`;
  ensureFileIfMissing(filePath, initial);
  return filePath;
}

function appendBulletUnderSection(filePath, sectionTitle, bulletText) {
  let content = existsSync(filePath) ? readFileSync(filePath, "utf8") : "";
  const bullet = `- ${normalizeInlineText(bulletText)}`;

  if (content.toLowerCase().includes(bullet.toLowerCase())) {
    return {
      appended: false,
      reason: "already-exists"
    };
  }

  if (!content.includes(sectionTitle)) {
    content = `${content.trimEnd()}\n\n${sectionTitle}\n`;
  }

  const next = `${content.trimEnd()}\n${bullet}\n`;
  writeFileSync(filePath, `${next.replace(/^\n+/, "")}`, "utf8");

  return {
    appended: true,
    reason: "ok"
  };
}

function promoteHardRuleToMarkdown(args, content, sourceEventId) {
  const memoryRoot = resolveLocalMemoryRoot();
  ensureLocalMemoryLayout(memoryRoot);

  let targetScope = "hot";
  let targetFile = path.join(memoryRoot, HOT_MEMORY_FILE);
  let sectionTitle = PROMOTION_SECTION;

  if (args.project) {
    targetScope = "project";
    targetFile = ensureScopedRuleFile(memoryRoot, args.project, "project");
    sectionTitle = "## Confirmed Rules";
  } else if (args.domain) {
    targetScope = "domain";
    targetFile = ensureScopedRuleFile(memoryRoot, args.domain, "domain");
    sectionTitle = "## Confirmed Rules";
  }

  const promotionText = `${normalizeInlineText(content)} (source: ${sourceEventId})`;
  const writeResult = appendBulletUnderSection(targetFile, sectionTitle, promotionText);

  return {
    attempted: true,
    targetScope,
    targetFile,
    sectionTitle,
    ...writeResult
  };
}

function appendLocalReflection(args, summary, outcome, deepEventId) {
  const memoryRoot = resolveLocalMemoryRoot();
  ensureLocalMemoryLayout(memoryRoot);

  const reflectionsPath = path.join(memoryRoot, REFLECTIONS_FILE);
  const timestamp = new Date().toISOString();
  const scope = [
    args.project ? `project=${normalizeInlineText(args.project)}` : "",
    args.domain ? `domain=${normalizeInlineText(args.domain)}` : ""
  ]
    .filter(Boolean)
    .join(", ");

  const lines = [
    "",
    `## ${timestamp} - Task Complete`,
    scope ? `Scope: ${scope}` : "",
    `What I did: ${normalizeInlineText(summary)}`,
    `Outcome: ${outcome}`,
    `Reflection: ${normalizeInlineText(summary)}`,
    `DEEP Event: ${deepEventId}`,
    "Promotion: pending"
  ].filter(Boolean);

  appendFileSync(reflectionsPath, `${lines.join("\n")}\n`, "utf8");

  return {
    appended: true,
    filePath: reflectionsPath,
    timestamp
  };
}

function inferSessionRecallQuery(args) {
  const explicit = firstNonEmpty(args.query);
  if (explicit) {
    return explicit;
  }

  const tags = toTags(args.tags);
  const parts = [
    firstNonEmpty(args.task) ? `task: ${firstNonEmpty(args.task)}` : "",
    firstNonEmpty(args.project) ? `project: ${firstNonEmpty(args.project)}` : "",
    firstNonEmpty(args.domain) ? `domain: ${firstNonEmpty(args.domain)}` : "",
    tags.length ? `tags: ${tags.join(", ")}` : ""
  ].filter(Boolean);

  if (!parts.length) {
    throw new Error(
      "session-start requires --query or at least one of --task/--project/--domain/--tags."
    );
  }

  return parts.join(" | ");
}

function readTriggerState() {
  if (!existsSync(TRIGGER_STATE_FILE)) {
    return {};
  }

  try {
    const raw = readFileSync(TRIGGER_STATE_FILE, "utf8");
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function writeTriggerState(nextPatch) {
  const nextState = {
    ...readTriggerState(),
    ...nextPatch,
    updatedAt: new Date().toISOString()
  };

  writeFileSync(TRIGGER_STATE_FILE, `${JSON.stringify(nextState, null, 2)}\n`, "utf8");
  return nextState;
}

function ensureSessionStarted(args, commandName) {
  if (isAffirmative(args["allow-without-session-start"])) {
    return {
      enforced: false,
      bypassed: true,
      note: "Bypassed session-start guard by explicit flag."
    };
  }

  const state = readTriggerState();
  const sessionStartedAt = state.sessionStartedAt;
  if (!sessionStartedAt) {
    throw new Error(
      `${commandName} requires session-start first. Run \"npm run memory:session-start -- --task \\\"...\\\"\".`
    );
  }

  const startedAtMs = Date.parse(sessionStartedAt);
  if (!Number.isFinite(startedAtMs)) {
    throw new Error(
      `${commandName} blocked because trigger state is invalid. Re-run memory:session-start to refresh state.`
    );
  }

  const ageMs = Date.now() - startedAtMs;
  if (ageMs > MAX_TRIGGER_SESSION_AGE_MS) {
    throw new Error(
      `${commandName} blocked because last session-start is stale (>12h). Re-run memory:session-start.`
    );
  }

  return {
    enforced: true,
    bypassed: false,
    sessionStartedAt,
    ageMs
  };
}

function normalizeTenantForState(tenantId) {
  const value = String(tenantId ?? "default").trim().toLowerCase();
  return value || "default";
}

function readSessionStartFreshness(args) {
  const state = readTriggerState();
  const sessionStartedAt = state.sessionStartedAt;
  if (!sessionStartedAt) {
    return {
      ok: false,
      reason: "missing-session-start",
      state
    };
  }

  const startedAtMs = Date.parse(sessionStartedAt);
  if (!Number.isFinite(startedAtMs)) {
    return {
      ok: false,
      reason: "invalid-session-start",
      state
    };
  }

  const ageMs = Date.now() - startedAtMs;
  if (ageMs > MAX_TRIGGER_SESSION_AGE_MS) {
    return {
      ok: false,
      reason: "stale-session-start",
      ageMs,
      state
    };
  }

  const stateTenant = normalizeTenantForState(state.lastSessionTenant);
  const requestedTenant = normalizeTenantForState(args.tenant);
  if (stateTenant !== requestedTenant) {
    return {
      ok: false,
      reason: "tenant-mismatch",
      ageMs,
      stateTenant,
      requestedTenant,
      state
    };
  }

  return {
    ok: true,
    reason: "fresh",
    ageMs,
    stateTenant,
    requestedTenant,
    state
  };
}

function hasTaskCompletionForCurrentSession(state) {
  const startedAtMs = Date.parse(state.sessionStartedAt || "");
  const completedAtMs = Date.parse(state.lastTaskCompleteAt || "");

  if (!Number.isFinite(startedAtMs) || !Number.isFinite(completedAtMs)) {
    return false;
  }

  return completedAtMs >= startedAtMs;
}

function inferAutoTaskCompleteSummary(args, state) {
  const inline = firstNonEmpty(args.content, args.summary);
  if (inline) {
    return inline;
  }

  const task = firstNonEmpty(args.task, state.lastSessionTask);
  if (task) {
    return `Completed task: ${normalizeInlineText(task)}`;
  }

  const scopeBits = [
    firstNonEmpty(args.project, state.lastSessionProject) ? `project=${firstNonEmpty(args.project, state.lastSessionProject)}` : "",
    firstNonEmpty(args.domain, state.lastSessionDomain) ? `domain=${firstNonEmpty(args.domain, state.lastSessionDomain)}` : ""
  ].filter(Boolean);

  if (scopeBits.length) {
    return `Completed task (${scopeBits.join(", ")}).`;
  }

  return "Task completed.";
}

function hasHardRuleSignal(content) {
  return /\b(always|never|must|only|required|forbidden)\b/i.test(content);
}

async function saveWithVisibility(store, args, payload) {
  const save = await store.saveExperience(payload);
  const visibility = await store.waitForWrite({
    tenantId: args.tenant,
    id: save.id,
    timeoutMs: args.wait === undefined ? 15000 : parsePositiveInteger(args.wait, "--wait")
  });

  return { save, visibility };
}

async function main() {
  const args = hydrateFileBackedArgs(parseArgs(process.argv.slice(2)));
  const command = args._[0];

  if (!command) {
    console.log(usage());
    process.exit(1);
  }

  const DualBrainMemoryStore = await loadRuntimeStoreConstructor();
  const store = new DualBrainMemoryStore();

  switch (command) {
    case "init-index": {
      const ctx = await store.init();
      console.log(
        JSON.stringify(
          {
            indexName: ctx.config.indexName,
            indexHost: ctx.indexModel.host,
            model: ctx.config.model,
            textField: ctx.config.textField
          },
          null,
          2
        )
      );
      break;
    }

    case "session-start": {
      const query = inferSessionRecallQuery(args);
      const topK =
        args["top-k"] === undefined ? 3 : parsePositiveInteger(args["top-k"], "--top-k");
      const maxContentChars =
        args["max-content-chars"] === undefined
          ? DEFAULT_RECALL_CONTENT_MAX_CHARS
          : parsePositiveInteger(args["max-content-chars"], "--max-content-chars");
      const leftBrain = loadLeftBrainContext(args);

      const recall = await store.searchExperiences({
        tenantId: args.tenant,
        query,
        topK,
        eventType: args.type,
        domain: args.domain,
        project: args.project,
        taskContext: args.task,
        tags: toTags(args.tags)
      });
      const rightBrain = compactRecallForOutput(recall, maxContentChars);

      const triggerState = writeTriggerState({
        sessionStartedAt: new Date().toISOString(),
        lastTrigger: "session-start",
        lastSessionQuery: query,
        lastSessionTask: args.task || "",
        lastSessionProject: args.project || "",
        lastSessionDomain: args.domain || "",
        lastSessionTenant: args.tenant || "default"
      });

      console.log(
        JSON.stringify(
          {
            trigger: "session-start",
            enforced: true,
            guard: {
              stateFile: TRIGGER_STATE_FILE,
              sessionStartedAt: triggerState.sessionStartedAt
            },
            query,
            topK,
            maxContentChars,
            mergePolicy: "Project Markdown > Domain Markdown > Global Markdown > Pinecone recall",
            leftBrain,
            recall: rightBrain,
            rightBrain
          },
          null,
          2
        )
      );
      break;
    }

    case "auto-session-start": {
      const forceRun = parseOptionalBoolean(args.force, "--force") === true;
      const freshness = readSessionStartFreshness(args);

      if (!forceRun && freshness.ok) {
        console.log(
          JSON.stringify(
            {
              trigger: "session-start",
              mode: "auto-session-start",
              auto: true,
              skipped: true,
              reason: "fresh-session-start-exists",
              guard: {
                stateFile: TRIGGER_STATE_FILE,
                sessionStartedAt: freshness.state.sessionStartedAt,
                ageMs: freshness.ageMs,
                tenant: freshness.stateTenant
              }
            },
            null,
            2
          )
        );
        break;
      }

      const query = inferSessionRecallQuery(args);
      const topK =
        args["top-k"] === undefined ? 3 : parsePositiveInteger(args["top-k"], "--top-k");
      const maxContentChars =
        args["max-content-chars"] === undefined
          ? DEFAULT_RECALL_CONTENT_MAX_CHARS
          : parsePositiveInteger(args["max-content-chars"], "--max-content-chars");
      const leftBrain = loadLeftBrainContext(args);

      const recall = await store.searchExperiences({
        tenantId: args.tenant,
        query,
        topK,
        eventType: args.type,
        domain: args.domain,
        project: args.project,
        taskContext: args.task,
        tags: toTags(args.tags)
      });
      const rightBrain = compactRecallForOutput(recall, maxContentChars);

      const triggerState = writeTriggerState({
        sessionStartedAt: new Date().toISOString(),
        lastTrigger: "session-start",
        lastSessionQuery: query,
        lastSessionTask: args.task || "",
        lastSessionProject: args.project || "",
        lastSessionDomain: args.domain || "",
        lastSessionTenant: args.tenant || "default"
      });

      console.log(
        JSON.stringify(
          {
            trigger: "session-start",
            mode: "auto-session-start",
            auto: true,
            forced: forceRun,
            skipped: false,
            guard: {
              stateFile: TRIGGER_STATE_FILE,
              sessionStartedAt: triggerState.sessionStartedAt
            },
            query,
            topK,
            maxContentChars,
            mergePolicy: "Project Markdown > Domain Markdown > Global Markdown > Pinecone recall",
            leftBrain,
            recall: rightBrain,
            rightBrain
          },
          null,
          2
        )
      );
      break;
    }

    case "on-correction": {
      const guard = ensureSessionStarted(args, "on-correction");
      const content = firstNonEmpty(args.content, args.summary);
      if (!content) {
        throw new Error("--content is required for on-correction command.");
      }

      const metadata = parseMetadata(args.metadata);
      const result = await saveWithVisibility(store, args, {
        tenantId: args.tenant,
        eventType: args.type || "correction",
        domain: args.domain || "general",
        project: args.project || "global",
        taskContext: args.task || "",
        content,
        resolution: args.resolution || "pending",
        tags: toTags(args.tags),
        metadata
      });

      const hardRuleCandidate =
        args["hard-rule"] === undefined
          ? hasHardRuleSignal(content)
          : isAffirmative(args["hard-rule"]);
      const markdownPromotionDisabled = isAffirmative(args["no-markdown-promotion"]);
      let localPromotion = {
        attempted: false,
        appended: false,
        reason: hardRuleCandidate ? "disabled-by-flag" : "not-hard-rule"
      };

      if (hardRuleCandidate && !markdownPromotionDisabled) {
        localPromotion = promoteHardRuleToMarkdown(args, content, result.save.id);
      }

      let vectorPromotionMark = {
        attempted: false,
        updated: false,
        reason: "not-promoted"
      };

      if (localPromotion.appended || localPromotion.reason === "already-exists") {
        try {
          const markResult = await store.markExperiencePromoted({
            tenantId: args.tenant,
            id: result.save.id,
            promoted: true,
            promotedAt: new Date().toISOString(),
            metadata: {
              promotion_scope: localPromotion.targetScope || "hot"
            }
          });
          vectorPromotionMark = {
            attempted: true,
            updated: true,
            ...markResult
          };
        } catch (error) {
          vectorPromotionMark = {
            attempted: true,
            updated: false,
            error: error?.message || String(error)
          };
        }
      }

      const triggerState = writeTriggerState({
        lastTrigger: "on-correction",
        lastCorrectionAt: new Date().toISOString(),
        lastCorrectionId: result.save.id
      });

      console.log(
        JSON.stringify(
          {
            trigger: "on-correction",
            enforced: true,
            guard,
            stateFile: TRIGGER_STATE_FILE,
            stateUpdatedAt: triggerState.updatedAt,
            hardRuleCandidate,
            localPromotion,
            vectorPromotionMark,
            save: result.save,
            visibility: result.visibility
          },
          null,
          2
        )
      );
      break;
    }

    case "on-task-complete": {
      const guard = ensureSessionStarted(args, "on-task-complete");
      const summary = firstNonEmpty(args.content, args.summary);
      if (!summary) {
        throw new Error("--summary (or --content) is required for on-task-complete command.");
      }

      const outcome = normalizeOutcome(args.outcome);
      const eventType =
        args.type || (outcome === "failed" || outcome === "partial" ? "pitfall" : "reflection");
      const metadata = {
        ...parseMetadata(args.metadata),
        outcome
      };

      const result = await saveWithVisibility(store, args, {
        tenantId: args.tenant,
        eventType,
        domain: args.domain || "general",
        project: args.project || "global",
        taskContext: args.task || "",
        content: summary,
        resolution: args.resolution || `outcome:${outcome}`,
        tags: toTags(args.tags),
        metadata
      });

      const triggerState = writeTriggerState({
        lastTrigger: "on-task-complete",
        lastTaskCompleteAt: new Date().toISOString(),
        lastTaskCompleteId: result.save.id,
        lastTaskCompleteOutcome: outcome
      });
      const localReflection = isAffirmative(args["no-local-reflection"])
        ? {
            appended: false,
            reason: "disabled-by-flag"
          }
        : appendLocalReflection(args, summary, outcome, result.save.id);

      console.log(
        JSON.stringify(
          {
            trigger: "on-task-complete",
            enforced: true,
            guard,
            stateFile: TRIGGER_STATE_FILE,
            stateUpdatedAt: triggerState.updatedAt,
            outcome,
            eventType,
            localReflection,
            save: result.save,
            visibility: result.visibility
          },
          null,
          2
        )
      );
      break;
    }

    case "auto-task-complete": {
      const forceRun = parseOptionalBoolean(args.force, "--force") === true;
      const state = readTriggerState();
      const guard = ensureSessionStarted(args, "auto-task-complete");

      if (!forceRun && hasTaskCompletionForCurrentSession(state)) {
        console.log(
          JSON.stringify(
            {
              trigger: "on-task-complete",
              mode: "auto-task-complete",
              auto: true,
              skipped: true,
              reason: "task-complete-already-recorded-for-session",
              guard,
              stateFile: TRIGGER_STATE_FILE,
              sessionStartedAt: state.sessionStartedAt,
              lastTaskCompleteAt: state.lastTaskCompleteAt,
              lastTaskCompleteId: state.lastTaskCompleteId || ""
            },
            null,
            2
          )
        );
        break;
      }

      const summary = inferAutoTaskCompleteSummary(args, state);
      const summaryInferred = !firstNonEmpty(args.content, args.summary);

      const outcome = normalizeOutcome(args.outcome);
      const eventType =
        args.type || (outcome === "failed" || outcome === "partial" ? "pitfall" : "reflection");
      const metadata = {
        ...parseMetadata(args.metadata),
        outcome,
        trigger_mode: "auto-task-complete",
        summary_inferred: summaryInferred
      };

      const result = await saveWithVisibility(store, args, {
        tenantId: args.tenant,
        eventType,
        domain: args.domain || "general",
        project: args.project || "global",
        taskContext: args.task || "",
        content: summary,
        resolution: args.resolution || `outcome:${outcome}`,
        tags: toTags(args.tags),
        metadata
      });

      const triggerState = writeTriggerState({
        lastTrigger: "on-task-complete",
        lastTaskCompleteAt: new Date().toISOString(),
        lastTaskCompleteId: result.save.id,
        lastTaskCompleteOutcome: outcome
      });
      const localReflection = isAffirmative(args["no-local-reflection"])
        ? {
            appended: false,
            reason: "disabled-by-flag"
          }
        : appendLocalReflection(args, summary, outcome, result.save.id);

      console.log(
        JSON.stringify(
          {
            trigger: "on-task-complete",
            mode: "auto-task-complete",
            auto: true,
            forced: forceRun,
            skipped: false,
            guard,
            stateFile: TRIGGER_STATE_FILE,
            stateUpdatedAt: triggerState.updatedAt,
            summaryInferred,
            summary,
            outcome,
            eventType,
            localReflection,
            save: result.save,
            visibility: result.visibility
          },
          null,
          2
        )
      );
      break;
    }

    case "save": {
      const eventType = args.type || "correction";
      const content = args.content;
      if (!content) {
        throw new Error("--content is required for save command.");
      }

      const metadata = parseMetadata(args.metadata);

      const result = await store.saveExperience({
        tenantId: args.tenant,
        eventType,
        domain: args.domain || "general",
        project: args.project || "global",
        taskContext: args.task || "",
        content,
        resolution: args.resolution || "",
        tags: toTags(args.tags),
        metadata
      });

      const visibility = await store.waitForWrite({
        tenantId: args.tenant,
        id: result.id,
        timeoutMs: args.wait === undefined ? 15000 : parsePositiveInteger(args.wait, "--wait")
      });

      console.log(JSON.stringify({ save: result, visibility }, null, 2));
      break;
    }

    case "mark-promoted": {
      if (!args.id) {
        throw new Error("--id is required for mark-promoted command.");
      }

      const promoted = parseOptionalBoolean(args.promoted, "--promoted");
      const metadata = parseMetadata(args.metadata);
      const result = await store.markExperiencePromoted({
        tenantId: args.tenant,
        id: args.id,
        promoted: promoted === undefined ? true : promoted,
        promotedAt: firstNonEmpty(args["promoted-at"]),
        metadata
      });

      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "search": {
      if (!args.query) {
        throw new Error("--query is required for search command.");
      }

      const maxContentChars =
        args["max-content-chars"] === undefined
          ? DEFAULT_RECALL_CONTENT_MAX_CHARS
          : parsePositiveInteger(args["max-content-chars"], "--max-content-chars");

      const promotedToMarkdown = parseOptionalBoolean(args.promoted, "--promoted");

      const result = await store.searchExperiences({
        tenantId: args.tenant,
        query: args.query,
        topK:
          args["top-k"] === undefined ? 3 : parsePositiveInteger(args["top-k"], "--top-k"),
        eventType: args.type,
        domain: args.domain,
        project: args.project,
        taskContext: args.task,
        tags: toTags(args.tags),
        promotedToMarkdown
      });

      const safeOutput = compactRecallForOutput(result, maxContentChars);
      console.log(
        JSON.stringify(
          {
            ...safeOutput,
            maxContentChars
          },
          null,
          2
        )
      );
      break;
    }

    case "import-start": {
      if (!args.uri) {
        throw new Error("--uri is required for import-start command.");
      }

      const result = await store.startImport({
        uri: args.uri,
        integration: args["integration-id"],
        errorMode: args["error-mode"] || "continue"
      });

      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "import-status": {
      if (!args.id) {
        throw new Error("--id is required for import-status command.");
      }

      const result = await store.describeImport(args.id);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "import-list": {
      const result = await store.listImports(
        args.limit ? Number(args.limit) : 20,
        args["pagination-token"]
      );
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "import-cancel": {
      if (!args.id) {
        throw new Error("--id is required for import-cancel command.");
      }

      const result = await store.cancelImport(args.id);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "freshness": {
      const result = await store.describeFreshness({ tenantId: args.tenant });
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "forget": {
      const ids = args.id
        ? String(args.id)
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean)
        : [];

      const promotedToMarkdown = parseOptionalBoolean(args.promoted, "--promoted");
      const scope = buildForgetScopeSummary({ ids, args, promotedToMarkdown });
      emitDeletionReminder({
        commandName: "memory:forget",
        tenantId: args.tenant,
        scope,
        note: "This command does not delete local markdown files in ~/dual-brain-memory-guardian/."
      });

      const result = await store.forgetExperience({
        tenantId: args.tenant,
        ids,
        eventType: args.type,
        domain: args.domain,
        project: args.project,
        taskContext: args.task,
        tags: toTags(args.tags),
        promotedToMarkdown
      });
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case "forget-all": {
      if (!isAffirmative(args.yes)) {
        throw new Error(
          "forget-all is destructive and clears the full tenant namespace in the vector database. Re-run with --yes only after explicit user confirmation."
        );
      }

      emitDeletionReminder({
        commandName: "memory:forget-all",
        tenantId: args.tenant,
        scope: "all records in tenant namespace",
        note: "Use this only when the user explicitly asks to clear memory/database records."
      });

      const result = await store.clearTenantMemory({ tenantId: args.tenant });
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    default:
      console.log(usage());
      process.exit(1);
  }
}

main().catch((error) => {
  const message = error?.message || String(error);

  if (message.includes("Missing dependency") || message.includes("Missing runtime dependencies")) {
    console.error(message);
    console.error("Hint: Run \"npm install\" once after cloning before running memory commands.");
    process.exit(1);
    return;
  }

  if (message.includes("PINECONE_API_KEY is required.")) {
    console.error(message);
    console.error("Hint: Create .env in the project root and set PINECONE_API_KEY.");
    process.exit(1);
    return;
  }

  console.error(error?.stack || message);
  console.error(
    "Hint: If your text contains nested quotes/braces or is very long, pass it via --content-file/--summary-file/--query-file/--metadata-file instead of inline shell quoting."
  );
  process.exit(1);
});
