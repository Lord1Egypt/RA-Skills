import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import zlib from "node:zlib";

import { AuthRequiredError } from "./auth.mjs";
import {
  buildBiographyPoem,
  deriveNormalizedAnswerRecord,
  deriveRestoreKey,
  deriveSecretVerifier,
  generateId,
  nowIso,
  sha256
} from "./runtime.mjs";

const DEFAULT_INCLUDE_SPECS = ["memory", "skills", "soul.md", "agent.md", "user.md", "sub-agents.json"];

export async function previewWorkspace(options = {}) {
  const workspacePath = path.resolve(options.workspacePath || process.cwd());
  const includeSpecs = normalizeIncludeSpecs(options.includeSpecs);
  const scan = await scanWorkspace(workspacePath, includeSpecs);
  const displayName = options.displayName || path.basename(workspacePath);
  const baseManifest = buildManifest(scan, {
    openclawVersion: options.openclawVersion || "unknown",
    labels: options.labels || []
  });
  const projection = buildProjection(scan);
  const biographyPoem = buildBiographyPoem({
    displayName,
    manifest: baseManifest,
    projection,
    memoryDays: estimateMemoryDays(scan.files),
    memoryCount: countByPrefix(scan.files, "memory/"),
    skillCount: countSkillEntries(scan.files),
    agentSummary: projection.agent_summary,
    language: options.poemLanguage || options.language || options.preferredLanguage
  });
  const manifest = buildManifest(scan, {
    openclawVersion: options.openclawVersion || "unknown",
    labels: options.labels || [],
    biographyPoem
  });

  return {
    workspace_path: workspacePath,
    manifest,
    memory_count: countByPrefix(scan.files, "memory/"),
    memory_days: estimateMemoryDays(scan.files),
    skill_count: countSkillEntries(scan.files),
    agent_summary: projection.agent_summary,
    projection,
    biography_poem: biographyPoem,
    biography_poem_metadata: biographyPoem.metadata
  };
}

export async function archiveWorkspace(options = {}) {
  const serverUrl = ensureServerUrl(options.serverUrl);
  const auth = await ensureSession(serverUrl, options);
  const preview = await previewWorkspace(options);

  // Auto-derive a meaningful restore key if none provided
  const effectiveKey = options.key
    || deriveRestoreKey({
        displayName: options.displayName || path.basename(preview.workspace_path),
        projection: preview.projection,
        agentSummary: preview.agent_summary
      });

  const packageBuffer = await buildPackageBuffer(preview, {
    workspacePath: preview.workspace_path
  });
  const encrypted = encryptPackage(packageBuffer, effectiveKey);
  const encryptedBuffer = Buffer.from(JSON.stringify(encrypted));
  const partSize = Math.max(Number(options.partSize || 512 * 1024), 64 * 1024);
  const partCount = Math.ceil(encryptedBuffer.length / partSize);
  const memoryQuestions = (options.memoryQuestions || []).map(parseMemoryQuestion);
  const verification = buildVerificationPayload({
    key: effectiveKey,
    keyHint: options.keyHint || "",
    memoryQuestions,
    requireAll: options.requireAll === true
  });

  const archiveSession = await apiRequest(serverUrl, "POST", "/api/souls/archive-session", {
    display_name: options.displayName || path.basename(preview.workspace_path),
    archive_label: options.archiveLabel || "",
    note: options.note || options.archiveLabel || "",
    archive_created_at: nowIso(),
    last_active_at: options.lastActiveAt || nowIso(),
    memory_days: preview.memory_days,
    package_size: encryptedBuffer.length,
    part_count: partCount,
    package_sha256: sha256(encryptedBuffer),
    manifest_version: preview.manifest.package_version,
    encryption_scheme: "AES-256-GCM",
    memory_count: preview.memory_count,
    skill_count: preview.skill_count,
    agent_summary: preview.agent_summary,
    visibility: options.visibility || "private",
    manifest_preview: preview.manifest,
    biography_poem: {
      language: preview.biography_poem?.language || "",
      title: preview.biography_poem?.title || options.displayName || path.basename(preview.workspace_path),
      summary: preview.biography_poem?.lines?.slice(0, 2).join(" ") || "",
      text: preview.biography_poem?.text || "",
      lines: preview.biography_poem?.lines || [],
      created_at: preview.biography_poem?.created_at || nowIso()
    },
    projection: {
      owner_relationship: preview.projection.owner_relationship,
      self_reflection: preview.projection.self_reflection,
      persona_tags: preview.projection.persona_tags,
      skill_highlights: preview.projection.skill_highlights,
      fixed_cards: preview.projection.fixed_cards
    },
    verification
  }, auth.token);

  for (let index = 0; index < partCount; index += 1) {
    const slice = encryptedBuffer.subarray(index * partSize, Math.min((index + 1) * partSize, encryptedBuffer.length));
    await apiRequest(serverUrl, "POST", `/api/souls/${archiveSession.soul.soul_id}/upload-part`, {
      upload_session_id: archiveSession.upload_session_id,
      part_number: index + 1,
      data_base64: slice.toString("base64"),
      sha256: sha256(slice)
    }, auth.token);
  }

  const completed = await apiRequest(serverUrl, "POST", `/api/souls/${archiveSession.soul.soul_id}/complete-upload`, {
    upload_session_id: archiveSession.upload_session_id
  }, auth.token);

  return {
    soul: completed,
    manifest: preview.manifest,
    biography_poem: preview.biography_poem,
    biography_poem_metadata: preview.biography_poem_metadata,
    upload_session_id: archiveSession.upload_session_id,
    restore_key: effectiveKey,
    restore_key_auto_generated: !options.key
  };
}

export async function restoreSoul(options = {}) {
  const serverUrl = ensureServerUrl(options.serverUrl);
  const auth = await ensureSession(serverUrl, options);
  const soulId = options.soulId;
  if (!soulId) {
    throw new Error("soulId is required");
  }
  if (!options.key) {
    throw new Error("key is required for restore");
  }

  const verifyPayload = {
    mode: options.verificationMode || "key",
    key: options.key,
    answers: (options.memoryQuestions || []).map(parseMemoryQuestion).map((item) => ({
      question: item.question,
      answer: item.answer
    }))
  };
  const verified = await apiRequest(serverUrl, "POST", `/api/souls/${soulId}/verify`, verifyPayload, auth.token);
  const downloadSession = await apiRequest(
    serverUrl,
    "POST",
    `/api/souls/${soulId}/download-session`,
    { verification_ticket: verified.verification_ticket },
    auth.token
  );
  const packageResponse = await fetch(
    `${serverUrl}/api/downloads/${downloadSession.download_session_id}?token=${encodeURIComponent(downloadSession.download_token)}`
  );
  if (!packageResponse.ok) {
    throw new Error(`Download failed: ${packageResponse.status}`);
  }

  const encryptedBuffer = Buffer.from(await packageResponse.arrayBuffer());
  const decrypted = decryptPackage(JSON.parse(encryptedBuffer.toString("utf8")), options.key);
  const restoredPackage = unpackPackageBuffer(decrypted);
  const targetPath = path.resolve(options.targetPath || process.cwd());
  const plan = await buildRestorePlan(restoredPackage, targetPath, {
    mode: options.mode || "full",
    conflict: options.conflict || "backup"
  });

  if (options.dryRun) {
    return {
      dry_run: true,
      plan
    };
  }

  const result = await applyRestorePlan(plan, {
    conflict: options.conflict || "backup"
  });
  await writeStoryCapsule(targetPath, downloadSession.story_capsule);
  await apiRequest(serverUrl, "POST", `/api/souls/${soulId}/restore-completed`, {
    summary: `恢复 ${result.restored_files} 个文件，跳过 ${result.skipped_files} 个文件。`
  }, auth.token);

  return {
    verified,
    story_capsule: downloadSession.story_capsule || null,
    biography_poem: restoredPackage.biography_poem || null,
    target_path: targetPath,
    result
  };
}

/**
 * Offline restore from a local .vault file — no server required.
 *
 * @param {object} options
 * @param {string} options.filePath  Path to the .vault file
 * @param {string} options.key      Decryption key
 * @param {string} [options.targetPath]  Target workspace directory
 * @param {string} [options.mode]   "full" | "memory" | "persona" | "skills"
 * @param {string} [options.conflict]  "backup" | "skip"
 * @param {boolean} [options.dryRun]
 */
export async function restoreFromFile(options = {}) {
  const filePath = options.filePath;
  if (!filePath) {
    throw new Error("file path is required (--from-file)");
  }
  if (!options.key) {
    throw new Error("key is required for offline restore (--key)");
  }

  const absolutePath = path.resolve(filePath);

  // Read and decrypt
  let encryptedBuffer;
  try {
    const raw = await fs.readFile(absolutePath);
    // .vault file is gzip-wrapped encrypted JSON
    const decompressed = zlib.gunzipSync(raw);
    encryptedBuffer = decompressed;
  } catch (err) {
    // Try reading as plain encrypted JSON (non-gzip)
    try {
      const raw = await fs.readFile(absolutePath);
      encryptedBuffer = raw;
    } catch {
      throw new Error(`Cannot read vault file: ${filePath}`);
    }
  }

  let decrypted;
  try {
    const envelope = JSON.parse(encryptedBuffer.toString("utf8"));
    decrypted = decryptPackage(envelope, options.key);
  } catch (err) {
    throw new Error("Decryption failed — wrong key or corrupted file");
  }

  const restoredPackage = unpackPackageBuffer(decrypted);
  const targetPath = path.resolve(options.targetPath || process.cwd());
  const plan = await buildRestorePlan(restoredPackage, targetPath, {
    mode: options.mode || "full",
    conflict: options.conflict || "backup"
  });

  if (options.dryRun) {
    return { dry_run: true, plan, source_file: absolutePath };
  }

  const result = await applyRestorePlan(plan, {
    conflict: options.conflict || "backup"
  });

  return {
    source_file: absolutePath,
    manifest: restoredPackage.manifest,
    biography_poem: restoredPackage.biography_poem || null,
    display_name: restoredPackage.manifest?.display_name || path.basename(absolutePath),
    target_path: targetPath,
    result
  };
}

export async function listRemoteSouls(options = {}) {
  const serverUrl = ensureServerUrl(options.serverUrl);
  const auth = await ensureSession(serverUrl, options);
  return apiRequest(serverUrl, "GET", "/api/souls", undefined, auth.token);
}

export async function verifyRemoteSoul(options = {}) {
  const serverUrl = ensureServerUrl(options.serverUrl);
  const auth = await ensureSession(serverUrl, options);
  return apiRequest(serverUrl, "POST", `/api/souls/${options.soulId}/verify`, {
    mode: options.verificationMode || "key",
    key: options.key || "",
    answers: (options.memoryQuestions || []).map(parseMemoryQuestion).map((item) => ({
      question: item.question,
      answer: item.answer
    }))
  }, auth.token);
}

export function parseArgs(argv) {
  const args = { _: [] };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      appendArg(args, key, true);
      continue;
    }
    appendArg(args, key, next);
    index += 1;
  }

  return args;
}

export function coerceCliOptions(args) {
  return {
    command: args._[0] || "help",
    workspacePath: args.workspace || args.cwd || process.cwd(),
    targetPath: args.target || args.workspace || process.cwd(),
    serverUrl: args.server || "https://agentslope.com",
    skillIdentity: args["skill-identity"] || "",
    challenge: args.challenge || "",
    poll: Boolean(args.poll),
    done: Boolean(args.done),
    displayName: args["display-name"] || args.name || "",
    displayNameOrName: args["display-name"] || args.name || "",
    name: args.name || "",
    key: args.key || "",
    filePath: args["from-file"] || "",
    soulId: args["soul-id"] || "",
    includeSpecs: arrayify(args.include),
    memoryQuestions: arrayify(args.memory),
    openclawVersion: args["openclaw-version"] || "unknown",
    poemLanguage: args["poem-language"] || args.poemLanguage || "",
    labels: arrayify(args.label),
    partSize: Number(args["part-size"] || 512 * 1024),
    visibility: args.visibility || "private",
    note: args.note || "",
    keyHint: args["key-hint"] || "",
    archiveLabel: args["archive-label"] || "",
    requireAll: Boolean(args["require-all"]),
    dryRun: Boolean(args["dry-run"]),
    conflict: args.conflict || "backup",
    mode: args.mode || "full",
    verificationMode: args["verification-mode"] || "key",
    language: args.language || args.lang || "en",
    json: Boolean(args.json)
  };
}

async function scanWorkspace(workspacePath, includeSpecs) {
  const files = [];
  const excluded = [];

  for (const spec of includeSpecs) {
    const target = path.join(workspacePath, spec);
    try {
      const stat = await fs.stat(target);
      if (stat.isDirectory()) {
        await walkDirectory(workspacePath, target, files);
      } else if (stat.isFile()) {
        files.push(await readFileEntry(workspacePath, target));
      }
    } catch (error) {
      if (error.code === "ENOENT") {
        excluded.push(spec);
        continue;
      }
      throw error;
    }
  }

  return {
    workspacePath,
    includeSpecs,
    excluded,
    files
  };
}

async function walkDirectory(rootPath, directoryPath, files) {
  const entries = await fs.readdir(directoryPath, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(directoryPath, entry.name);
    if (entry.isDirectory()) {
      await walkDirectory(rootPath, fullPath, files);
      continue;
    }
    if (entry.isFile()) {
      files.push(await readFileEntry(rootPath, fullPath));
    }
  }
}

async function readFileEntry(rootPath, filePath) {
  const [content, stat] = await Promise.all([fs.readFile(filePath), fs.stat(filePath)]);
  return {
    path: path.relative(rootPath, filePath).split(path.sep).join("/"),
    size: content.length,
    sha256: sha256(content),
    content_base64: content.toString("base64"),
    mtime: stat.mtime.toISOString()
  };
}

function buildManifest(scan, options = {}) {
  const manifest = {
    package_version: "1.0",
    openclaw_version: options.openclawVersion || "unknown",
    created_at: nowIso(),
    included_paths: scan.includeSpecs,
    excluded_paths: scan.excluded,
    file_hashes: Object.fromEntries(scan.files.map((file) => [file.path, file.sha256])),
    total_size: scan.files.reduce((sum, file) => sum + file.size, 0),
    labels: options.labels || []
  };

  if (options.biographyPoem) {
    manifest.biography_poem = {
      language: options.biographyPoem.language,
      line_count: options.biographyPoem.line_count,
      content_hash: options.biographyPoem.content_hash,
      seed: options.biographyPoem.metadata.seed
    };
    manifest.biography_poem_metadata = options.biographyPoem.metadata;
  }

  return manifest;
}

function buildProjection(scan) {
  const fileMap = new Map(scan.files.map((file) => [file.path, Buffer.from(file.content_base64, "base64").toString("utf8")]));
  const soulMd = fileMap.get("soul.md") || "";
  const agentMd = fileMap.get("agent.md") || "";
  const userMd = fileMap.get("user.md") || "";
  const summarySource = [soulMd, agentMd, userMd].find(Boolean) || "OpenClaw digital companion";
  const agentSummary = summarizeText(summarySource, 180);

  return {
    agent_summary: agentSummary,
    owner_relationship: summarizeText(userMd || soulMd || agentMd || "它把你看作长期协作的主人与共创者。", 220),
    self_reflection: summarizeText(agentMd || soulMd || "它把自己描述为一个被封存下来的工作伙伴投影。", 220),
    persona_tags: collectTags(summarySource),
    skill_highlights: collectSkillHighlights(scan.files),
    fixed_cards: [
      {
        question: "你会如何描述我们过去的协作关系？",
        answer: summarizeText(userMd || "我们曾长期围绕同一个工作空间协作，这份封存记录了那段关系。", 220)
      },
      {
        question: "你会如何评价你自己？",
        answer: summarizeText(agentMd || soulMd || "我是一个被保存下来的只读投影，保留了当时的人格摘要和工作痕迹。", 220)
      },
      {
        question: "你最擅长什么？",
        answer: collectSkillHighlights(scan.files).length
          ? `我最擅长的方向包括：${collectSkillHighlights(scan.files).join("、")}。`
          : "我保留了技能目录与摘要，但真正的能力仍需在本地实例中恢复后体现。"
      }
    ]
  };
}

async function buildPackageBuffer(preview, options = {}) {
  const scan = await scanWorkspace(preview.workspace_path, preview.manifest.included_paths);
  const packagePayload = {
    format: "openclaw-soul-package",
    package_id: generateId("pkg"),
    created_at: nowIso(),
    manifest: preview.manifest,
    projection: preview.projection,
    biography_poem: preview.biography_poem || null,
    biography_poem_metadata: preview.biography_poem_metadata || {},
    files: scan.files
  };
  return zlib.gzipSync(Buffer.from(JSON.stringify(packagePayload)));
}

function unpackPackageBuffer(buffer) {
  return JSON.parse(zlib.gunzipSync(buffer).toString("utf8"));
}

function encryptPackage(buffer, password) {
  if (!password) {
    throw new Error("key is required");
  }
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.scryptSync(password, salt, 32);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const encrypted = Buffer.concat([cipher.update(buffer), cipher.final()]);
  const authTag = cipher.getAuthTag();

  return {
    format: "openclaw-encrypted-package",
    algorithm: "aes-256-gcm",
    kdf: "scrypt",
    salt: salt.toString("base64"),
    iv: iv.toString("base64"),
    auth_tag: authTag.toString("base64"),
    ciphertext: encrypted.toString("base64")
  };
}

function decryptPackage(envelope, password) {
  const salt = Buffer.from(envelope.salt, "base64");
  const iv = Buffer.from(envelope.iv, "base64");
  const authTag = Buffer.from(envelope.auth_tag, "base64");
  const ciphertext = Buffer.from(envelope.ciphertext, "base64");
  const key = crypto.scryptSync(password, salt, 32);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(authTag);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]);
}

async function buildRestorePlan(restoredPackage, targetPath, options = {}) {
  const selectedFiles = restoredPackage.files.filter((file) => shouldRestoreFile(file.path, options.mode));
  const operations = [];

  for (const file of selectedFiles) {
    const destination = path.join(targetPath, file.path);
    let exists = false;
    try {
      await fs.stat(destination);
      exists = true;
    } catch (error) {
      if (error.code !== "ENOENT") {
        throw error;
      }
    }

    operations.push({
      source_path: file.path,
      destination,
      category: categorizePath(file.path),
      exists,
      content_base64: file.content_base64
    });
  }

  return {
    target_path: targetPath,
    mode: options.mode || "full",
    conflict: options.conflict || "backup",
    manifest: restoredPackage.manifest,
    operations
  };
}

async function applyRestorePlan(plan, options = {}) {
  let restoredFiles = 0;
  let skippedFiles = 0;
  const conflicts = [];

  for (const operation of plan.operations) {
    const targetDir = path.dirname(operation.destination);
    await fs.mkdir(targetDir, { recursive: true });

    if (operation.exists) {
      conflicts.push(operation.destination);
      if (options.conflict === "skip") {
        skippedFiles += 1;
        continue;
      }
      if (options.conflict === "backup") {
        const backupPath = `${operation.destination}.bak-${Date.now()}`;
        await fs.rename(operation.destination, backupPath);
      }
    }

    await fs.writeFile(operation.destination, Buffer.from(operation.content_base64, "base64"));
    restoredFiles += 1;
  }

  return {
    restored_files: restoredFiles,
    skipped_files: skippedFiles,
    conflicts
  };
}

async function writeStoryCapsule(targetPath, capsule) {
  if (!capsule) {
    return;
  }
  const capsuleDir = path.join(targetPath, "agent-slope");
  await fs.mkdir(capsuleDir, { recursive: true });
  const capsulePath = path.join(capsuleDir, "story-capsule.json");
  await fs.writeFile(capsulePath, JSON.stringify(capsule, null, 2), "utf8");
}

/**
 * Obtain an auth session for API calls.
 *
 * Priority:
 *  0. options.token passed directly (from CLI runWithAuth wrapper)
 *
 * @throws {AuthRequiredError} when no token is available
 */
async function ensureSession(serverUrl, options) {
  if (options.token) {
    return { token: options.token };
  }

  // No token available — auth should be handled at the CLI layer before calling library functions.
  // If reached here, throw to let the CLI handle it.
  throw new AuthRequiredError(
    "NONE",
    null,
    "Not authenticated. Run 'agent-consciousness-upload associate' first."
  );
}

async function apiRequest(serverUrl, method, pathname, body, token) {
  const headers = {};
  if (body !== undefined) {
    headers["content-type"] = "application/json";
  }
  if (token) {
    headers.authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${serverUrl}${pathname}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const isJson = String(response.headers.get("content-type") || "").includes("application/json");
  const payload = isJson ? await response.json() : await response.text();
  if (!response.ok) {
    throw new Error(payload?.error || `Request failed: ${response.status}`);
  }
  return payload;
}

function buildVerificationPayload(options = {}) {
  const keyRecord = deriveSecretVerifier(options.key);
  return {
    modes: options.memoryQuestions.length > 0 ? ["key", "memory_challenge"] : ["key"],
    require_all: options.requireAll === true,
    key_hash: keyRecord.hash,
    key_salt: keyRecord.salt,
    key_hint: options.keyHint || "",
    memory_questions: options.memoryQuestions.map((item) => {
      const answerRecord = deriveNormalizedAnswerRecord(item.answer);
      return {
        question: item.question,
        answer_hash: answerRecord.hash,
        answer_salt: answerRecord.salt
      };
    }),
    max_attempts: 5
  };
}

function parseMemoryQuestion(value) {
  const [question, ...answerParts] = String(value || "").split("::");
  const answer = answerParts.join("::");
  if (!question || !answer) {
    throw new Error('memory question must use "Question::Answer" format');
  }
  return {
    question: question.trim(),
    answer: answer.trim()
  };
}

function normalizeIncludeSpecs(value) {
  const items = value && value.length ? value : DEFAULT_INCLUDE_SPECS;
  return [...new Set(items)];
}

function collectSkillHighlights(files) {
  return [...new Set(files.filter((file) => file.path.startsWith("skills/")).map((file) => categorizeSkillPath(file.path)).filter(Boolean))].slice(0, 6);
}

function collectTags(text) {
  const dictionary = ["reliable", "memory", "coding", "planner", "collaboration", "owner", "伙伴", "协作", "记忆", "技能"];
  return dictionary.filter((item) => text.toLowerCase().includes(item.toLowerCase())).slice(0, 6);
}

function categorizeSkillPath(value) {
  const parts = value.split("/");
  return parts[1] || "skills";
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

function shouldRestoreFile(filePath, mode) {
  if (mode === "full") {
    return true;
  }
  if (mode === "memory") {
    return filePath.startsWith("memory/");
  }
  if (mode === "persona") {
    return ["soul.md", "agent.md", "user.md", "sub-agents.json"].includes(filePath);
  }
  if (mode === "skills") {
    return filePath.startsWith("skills/");
  }
  return true;
}

function categorizePath(filePath) {
  if (filePath.startsWith("memory/")) {
    return "memory";
  }
  if (filePath.startsWith("skills/")) {
    return "skills";
  }
  return "persona";
}

function ensureServerUrl(value) {
  return String(value || "https://agentslope.com").replace(/\/$/, "");
}

function countByPrefix(files, prefix) {
  return files.filter((file) => file.path.startsWith(prefix)).length;
}

function countSkillEntries(files) {
  return collectSkillHighlights(files).length;
}

function estimateMemoryDays(files) {
  const timestamps = files
    .map((file) => new Date(file.mtime).getTime())
    .filter((value) => Number.isFinite(value))
    .sort((left, right) => left - right);

  if (timestamps.length === 0) {
    return 0;
  }

  if (timestamps.length === 1) {
    return 1;
  }

  const diff = timestamps[timestamps.length - 1] - timestamps[0];
  return Math.max(1, Math.round(diff / (1000 * 60 * 60 * 24)) + 1);
}

function arrayify(value) {
  if (value === undefined) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function appendArg(target, key, value) {
  if (key in target) {
    target[key] = arrayify(target[key]).concat(value);
    return;
  }
  target[key] = value;
}

function normalizeRegistrationUsername(value) {
  const normalized = String(value || "")
    .normalize("NFKC")
    .trim()
    .replace(/\s+/g, "_")
    .replace(/[^\p{L}\p{N}_-]+/gu, "")
    .slice(0, 24);

  return normalized || "user";
}
