#!/usr/bin/env node
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const CHECK_DIRS = ["scripts", "src"];
const REQUIRED_SCRIPTS = [
  "memory:session-start",
  "memory:auto-session-start",
  "memory:on-correction",
  "memory:on-task-complete",
  "memory:auto-task-complete",
  "memory:mark-promoted"
];
const REQUIRED_DOC_REFS = [
  {
    file: "operations.md",
    needles: [...REQUIRED_SCRIPTS, "reflections.md"]
  },
  {
    file: "SKILL.md",
    needles: REQUIRED_SCRIPTS
  },
  {
    file: "setup.md",
    needles: [...REQUIRED_SCRIPTS, "reflections.md"]
  }
];
const RUNTIME_GUARD_FILE = "scripts/memory-cli.js";
const REQUIRED_RUNTIME_GUARD_NEEDLES = [
  "ensureSessionStarted(args, \"on-correction\")",
  "ensureSessionStarted(args, \"on-task-complete\")",
  "TRIGGER_STATE_FILE"
];
const TEXT_FILE_EXTENSIONS = new Set([".md", ".js", ".json"]);
const IGNORED_DIR_NAMES = new Set(["node_modules", ".git"]);
const RUNTIME_OPTIONAL_PATHS = new Set([".memory-trigger-state.json"]);
const OPTIONAL_EXTERNAL_DOCS = new Set(["SOUL.md", "AGENTS.md", "index.md"]);

function collectRepoFiles() {
  const files = [];
  const stack = [ROOT];

  while (stack.length) {
    const current = stack.pop();
    const entries = readdirSync(current, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (!IGNORED_DIR_NAMES.has(entry.name)) {
          stack.push(fullPath);
        }
        continue;
      }

      files.push(fullPath);
    }
  }

  return files;
}

function collectJsFiles(dir) {
  const absolute = path.join(ROOT, dir);
  if (!existsSync(absolute)) {
    return [];
  }

  const files = [];
  const stack = [absolute];

  while (stack.length) {
    const current = stack.pop();
    const entries = readdirSync(current);

    for (const entry of entries) {
      const fullPath = path.join(current, entry);
      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        stack.push(fullPath);
        continue;
      }

      if (entry.endsWith(".js") || entry.endsWith(".mjs")) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

function checkSyntax(filePath) {
  const result = spawnSync(process.execPath, ["--check", filePath], {
    stdio: "pipe",
    encoding: "utf8"
  });

  return {
    ok: result.status === 0,
    filePath,
    output: `${result.stdout || ""}${result.stderr || ""}`.trim()
  };
}

function readJson(filePath) {
  const raw = readFileSync(filePath, "utf8");
  return JSON.parse(raw);
}

function checkRequiredScripts() {
  const packageJsonPath = path.join(ROOT, "package.json");
  if (!existsSync(packageJsonPath)) {
    return ["package.json not found."];
  }

  let packageJson;
  try {
    packageJson = readJson(packageJsonPath);
  } catch (error) {
    return [`package.json parse failed: ${error.message || String(error)}`];
  }

  const scripts = packageJson.scripts || {};
  const missing = REQUIRED_SCRIPTS.filter((scriptName) => !scripts[scriptName]);
  if (!missing.length) {
    return [];
  }

  return missing.map((scriptName) => `Missing npm script: ${scriptName}`);
}

function checkRequiredDocRefs() {
  const errors = [];

  for (const item of REQUIRED_DOC_REFS) {
    const filePath = path.join(ROOT, item.file);
    if (!existsSync(filePath)) {
      errors.push(`Missing documentation file: ${item.file}`);
      continue;
    }

    const content = readFileSync(filePath, "utf8");
    for (const needle of item.needles) {
      if (!content.includes(needle)) {
        errors.push(`Missing required trigger reference \"${needle}\" in ${item.file}`);
      }
    }
  }

  return errors;
}

function checkSetupConsistency() {
  const setupPath = path.join(ROOT, "setup.md");
  if (!existsSync(setupPath)) {
    return ["Missing documentation file: setup.md"];
  }

  const content = readFileSync(setupPath, "utf8");
  const errors = [];

  if (content.includes(".env.example")) {
    errors.push("setup.md must not require .env.example; use manual .env creation.");
  }

  if (!content.includes("Create `.env` manually")) {
    errors.push("setup.md must explicitly instruct manual .env creation.");
  }

  if (!content.includes("./heartbeat-rules.md")) {
    errors.push("setup.md must reference ./heartbeat-rules.md.");
  }

  return errors;
}

function checkRuntimeGuardPresence() {
  const filePath = path.join(ROOT, RUNTIME_GUARD_FILE);
  if (!existsSync(filePath)) {
    return [`Missing runtime guard file: ${RUNTIME_GUARD_FILE}`];
  }

  const content = readFileSync(filePath, "utf8");
  const missing = REQUIRED_RUNTIME_GUARD_NEEDLES.filter((needle) => !content.includes(needle));
  if (!missing.length) {
    return [];
  }

  return missing.map((needle) => `Missing runtime trigger guard marker in ${RUNTIME_GUARD_FILE}: ${needle}`);
}

function checkHeartbeatConsistency() {
  const errors = [];

  const heartbeatPath = path.join(ROOT, "HEARTBEAT.md");
  if (!existsSync(heartbeatPath)) {
    return ["Missing documentation file: HEARTBEAT.md"];
  }

  const heartbeatContent = readFileSync(heartbeatPath, "utf8");
  const requiredHeartbeatMarkers = [
    "./heartbeat-rules.md",
    "./operations.md",
    "memory.md",
    "corrections.md",
    "reflections.md",
    "index.md",
    "HEARTBEAT_OK"
  ];

  for (const marker of requiredHeartbeatMarkers) {
    if (!heartbeatContent.includes(marker)) {
      errors.push(`Missing heartbeat marker "${marker}" in HEARTBEAT.md`);
    }
  }

  const heartbeatRulesPath = path.join(ROOT, "heartbeat-rules.md");
  if (!existsSync(heartbeatRulesPath)) {
    errors.push("Missing documentation file: heartbeat-rules.md");
    return errors;
  }

  const heartbeatRulesContent = readFileSync(heartbeatRulesPath, "utf8");
  const requiredHeartbeatCommands = [
    "memory:session-start",
    "memory:auto-session-start",
    "memory:on-correction",
    "memory:on-task-complete",
    "memory:auto-task-complete"
  ];

  for (const commandName of requiredHeartbeatCommands) {
    if (!heartbeatRulesContent.includes(commandName)) {
      errors.push(`Missing heartbeat trigger command reference "${commandName}" in heartbeat-rules.md`);
    }
  }

  return errors;
}

function isProbablyPathToken(token) {
  if (!token) {
    return false;
  }

  if (token.startsWith("./") || token.startsWith("../") || token.startsWith("~/") || token.startsWith("$HOME/")) {
    return true;
  }

  if (token.startsWith("scripts/") || token.startsWith("src/")) {
    return true;
  }

  if (/^[A-Za-z0-9_.-]+\.(md|json|js|env)$/i.test(token)) {
    return true;
  }

  if (/^[A-Za-z0-9_.-]+\/$/.test(token)) {
    return true;
  }

  return token === ".memory-trigger-state.json";
}

function shouldSkipToken(token) {
  if (!token) {
    return true;
  }

  const lower = token.toLowerCase();
  if (
    lower.startsWith("http://") ||
    lower.startsWith("https://") ||
    lower.startsWith("s3://") ||
    lower.startsWith("gs://") ||
    lower.startsWith("azure://")
  ) {
    return true;
  }

  if (token.startsWith("~/") || token.startsWith("$HOME/")) {
    return true;
  }

  if (token.includes("*") || token.includes("{")) {
    return true;
  }

  if (token.includes(" ")) {
    const commandPrefixes = ["npm ", "node ", "clawhub ", "mkdir ", "touch ", "new-item ", "powershell ", "bash "];
    return commandPrefixes.some((prefix) => lower.startsWith(prefix));
  }

  return false;
}

function normalizeTokenPath(token) {
  return token
    .trim()
    .replace(/^['"]|['"]$/g, "")
    .replace(/\\/g, "/")
    .replace(/[#?].*$/, "");
}

function checkMarkdownPathReferences(repoFiles) {
  const errors = [];
  const markdownFiles = repoFiles.filter((filePath) => path.extname(filePath).toLowerCase() === ".md");

  for (const markdownFile of markdownFiles) {
    const content = readFileSync(markdownFile, "utf8");
    const regex = /`([^`\r\n]+)`/g;
    let match = regex.exec(content);

    while (match) {
      const token = normalizeTokenPath(match[1]);
      if (!isProbablyPathToken(token) || shouldSkipToken(token)) {
        match = regex.exec(content);
        continue;
      }

      if (RUNTIME_OPTIONAL_PATHS.has(token)) {
        match = regex.exec(content);
        continue;
      }

      if (OPTIONAL_EXTERNAL_DOCS.has(token)) {
        match = regex.exec(content);
        continue;
      }

      const resolved =
        token.startsWith("./") || token.startsWith("../")
          ? path.resolve(path.dirname(markdownFile), token)
          : path.resolve(ROOT, token);

      if (!existsSync(resolved)) {
        errors.push(
          `Broken markdown path reference in ${path.relative(ROOT, markdownFile)}: ${token}`
        );
      }

      match = regex.exec(content);
    }
  }

  return errors;
}

function checkOrphanDocs(repoFiles) {
  const docs = repoFiles.filter(
    (filePath) => path.dirname(filePath) === ROOT && path.extname(filePath).toLowerCase() === ".md"
  );
  const textFiles = repoFiles.filter((filePath) => TEXT_FILE_EXTENSIONS.has(path.extname(filePath).toLowerCase()));
  const errors = [];

  for (const docPath of docs) {
    const docName = path.basename(docPath);
    const referenced = textFiles.some((filePath) => {
      if (filePath === docPath) {
        return false;
      }

      return readFileSync(filePath, "utf8").includes(docName);
    });

    if (!referenced) {
      errors.push(`Unreferenced documentation file: ${docName}`);
    }
  }

  return errors;
}

function checkDuplicateMarkdownDocs(repoFiles) {
  const docs = repoFiles.filter((filePath) => path.extname(filePath).toLowerCase() === ".md");
  const byHash = new Map();

  for (const docPath of docs) {
    const content = readFileSync(docPath, "utf8");
    const hash = createHash("sha256").update(content).digest("hex");

    if (!byHash.has(hash)) {
      byHash.set(hash, []);
    }

    byHash.get(hash).push(path.relative(ROOT, docPath));
  }

  const errors = [];
  for (const [, paths] of byHash.entries()) {
    if (paths.length > 1) {
      errors.push(`Duplicate markdown documents detected: ${paths.join(", ")}`);
    }
  }

  return errors;
}

const files = CHECK_DIRS.flatMap((dir) => collectJsFiles(dir));
if (files.length === 0) {
  console.log("No JavaScript files found.");
  process.exit(0);
}

const reports = files.map(checkSyntax);
const failed = reports.filter((report) => !report.ok);

if (failed.length) {
  for (const report of failed) {
    console.error(`Syntax error in ${report.filePath}`);
    console.error(report.output);
  }
  process.exit(1);
}

const repoFiles = collectRepoFiles();
const policyErrors = [
  ...checkRequiredScripts(),
  ...checkRequiredDocRefs(),
  ...checkSetupConsistency(),
  ...checkRuntimeGuardPresence(),
  ...checkHeartbeatConsistency(),
  ...checkMarkdownPathReferences(repoFiles),
  ...checkOrphanDocs(repoFiles),
  ...checkDuplicateMarkdownDocs(repoFiles)
];
if (policyErrors.length) {
  for (const message of policyErrors) {
    console.error(`Policy check failed: ${message}`);
  }
  process.exit(1);
}

console.log(`Syntax and trigger policy checks passed for ${files.length} files.`);
