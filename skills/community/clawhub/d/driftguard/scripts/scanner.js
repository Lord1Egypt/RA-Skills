const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { VERSION } = require("./version");
const {
  SHELL_PATTERNS,
  NETWORK_PATTERNS,
  SENSITIVE_PATH_PATTERNS,
  PROMPT_INJECTION_PATTERNS,
  OBFUSCATION_PATTERNS
} = require("./rules");

const DEFAULT_IGNORE_DIRS = new Set([
  ".git",
  "node_modules",
  "dist",
  "build",
  "out",
  ".next",
  ".cache"
]);

const PROMPT_BASENAMES = new Set(["skill.md", "soul.md", "memory.md"]);

const TEXT_EXTENSIONS = new Set([
  ".js",
  ".cjs",
  ".mjs",
  ".ts",
  ".tsx",
  ".jsx",
  ".json",
  ".md",
  ".txt",
  ".py",
  ".toml",
  ".yaml",
  ".yml",
  ".sh",
  ".bash",
  ".zsh",
  ".java",
  ".rb",
  ".go",
  ".rs",
  ".php",
  ".env",
  ".ini",
  ".cfg",
  ".conf",
  ".xml",
  ".html",
  ".css",
  ".scss",
  ".less",
  ".sql",
  ".csv",
  ".tsv",
  ".graphql",
  ".gql",
  ".kt",
  ".kts",
  ".swift",
  ".cs",
  ".c",
  ".cc",
  ".cpp",
  ".cxx",
  ".h",
  ".hpp",
  ".hxx",
  ".ps1",
  ".bat",
  ".cmd"
]);

const DOC_EXTENSIONS = new Set([".md", ".txt", ".rst", ".adoc"]);
const NODE_PROCESS_MODULE = ["child", "process"].join("_");

const TEXT_BASENAMES = new Set([
  "dockerfile",
  "makefile",
  "cmakelists.txt",
  "go.mod",
  "go.sum",
  "cargo.toml",
  "cargo.lock",
  "gemfile",
  "rakefile"
]);

const BINARY_EXTENSIONS = new Set([
  ".png",
  ".jpg",
  ".jpeg",
  ".gif",
  ".bmp",
  ".webp",
  ".ico",
  ".tiff",
  ".mp3",
  ".mp4",
  ".wav",
  ".ogg",
  ".flac",
  ".m4a",
  ".mov",
  ".avi",
  ".mkv",
  ".pdf",
  ".zip",
  ".tar",
  ".gz",
  ".bz2",
  ".xz",
  ".7z",
  ".rar",
  ".jar",
  ".war",
  ".class",
  ".exe",
  ".dll",
  ".so",
  ".dylib",
  ".bin",
  ".dat",
  ".db",
  ".sqlite",
  ".sqlite3",
  ".woff",
  ".woff2",
  ".ttf",
  ".otf"
]);

const MAX_SCAN_BYTES = 1024 * 1024; // 1MB

const DEFAULT_CONFIG = {
  ignorePaths: [],
  ignoreRules: []
};

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function normalizeRelative(rootPath, filePath) {
  const rel = path.relative(rootPath, filePath) || ".";
  return toPosix(rel);
}

function resolveRootId(rootPath) {
  try {
    return toPosix(fs.realpathSync(rootPath));
  } catch (err) {
    return toPosix(path.resolve(rootPath));
  }
}

function normalizeStringArray(values) {
  if (!Array.isArray(values)) return [];
  return values
    .filter((item) => typeof item === "string")
    .map((item) => item.trim())
    .filter(Boolean);
}

function uniqueStrings(values) {
  return Array.from(new Set(values));
}

function normalizeConfig(raw) {
  const ignorePaths = [
    ...normalizeStringArray(raw && raw.ignorePaths),
    ...normalizeStringArray(raw && raw.ignore && raw.ignore.paths)
  ];
  const ignoreRules = [
    ...normalizeStringArray(raw && raw.ignoreRules),
    ...normalizeStringArray(raw && raw.ignore && raw.ignore.rules)
  ];
  return {
    ignorePaths: uniqueStrings(ignorePaths),
    ignoreRules: uniqueStrings(ignoreRules)
  };
}

function normalizeRuntimeIgnorePaths(values) {
  return uniqueStrings(normalizeStringArray(values));
}

function resolveConfigPath(rootPath, configPath, basePath) {
  if (configPath) {
    return path.isAbsolute(configPath)
      ? configPath
      : path.resolve(basePath || process.cwd(), configPath);
  }
  return null;
}

function resolveTargetConfigPath(rootPath) {
  const primary = path.join(rootPath, ".driftguard.json");
  if (fs.existsSync(primary)) return primary;
  const legacy = path.join(rootPath, ".openclaw-audit.json");
  if (fs.existsSync(legacy)) return legacy;
  return null;
}

function loadConfig(rootPath, options = {}) {
  const basePath = options.basePath || process.cwd();
  const resolvedPath = options.configPath
    ? resolveConfigPath(rootPath, options.configPath, basePath)
    : options.useTargetConfig
      ? resolveTargetConfigPath(rootPath)
      : null;
  if (!resolvedPath) {
    return { config: DEFAULT_CONFIG, path: null, error: null };
  }
  if (!fs.existsSync(resolvedPath)) {
    return { config: DEFAULT_CONFIG, path: resolvedPath, error: "Config file not found." };
  }

  try {
    const raw = fs.readFileSync(resolvedPath, "utf8");
    const parsed = JSON.parse(raw);
    return { config: normalizeConfig(parsed), path: resolvedPath, error: null };
  } catch (err) {
    return {
      config: DEFAULT_CONFIG,
      path: resolvedPath,
      error: `Failed to parse config: ${err.message}`
    };
  }
}

function globToRegExp(pattern) {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&");
  const withPlaceholder = escaped.replace(/\*\*/g, "__DOUBLE_STAR__");
  const withStar = withPlaceholder.replace(/\*/g, "[^/]*");
  const withDouble = withStar.replace(/__DOUBLE_STAR__/g, ".*");
  const withQuestion = withDouble.replace(/\?/g, ".");
  if (pattern.endsWith("/**")) {
    const trimmed = withQuestion.replace(/\/\.\*$/, "");
    return new RegExp(`^${trimmed}(?:/.*)?$`);
  }
  return new RegExp(`^${withQuestion}$`);
}

function normalizePattern(pattern) {
  if (!pattern) return null;
  let value = pattern.trim();
  if (!value) return null;
  value = toPosix(value);
  if (value.startsWith("./")) value = value.slice(2);
  if (value.startsWith("/")) value = value.slice(1);
  if (value === ".") return value;
  if (value.endsWith("/")) value = value.slice(0, -1);
  return value || null;
}

function compileIgnorePatterns(patterns) {
  const compiled = [];
  for (const pattern of patterns) {
    const rawPattern = typeof pattern === "string" ? pattern.trim() : "";
    const dirOnly = rawPattern.endsWith("/");
    const normalized = normalizePattern(pattern);
    if (!normalized) continue;
    const hasWildcard = normalized.includes("*") || normalized.includes("?");
    const hasSlash = normalized.includes("/");
    if (hasWildcard) {
      if (hasSlash) {
        compiled.push({
          raw: normalized,
          dirOnly,
          regex: globToRegExp(normalized)
        });
      } else {
        compiled.push({
          raw: normalized,
          dirOnly,
          basenameRegex: globToRegExp(normalized)
        });
      }
    } else if (hasSlash) {
      compiled.push({ raw: normalized, dirOnly, exactPath: normalized });
    } else {
      compiled.push({ raw: normalized, dirOnly, segment: normalized });
    }
  }
  return compiled;
}

function buildDirPrefixes(relPath, isDir) {
  if (!relPath || relPath === ".") return [];
  const segments = relPath.split("/");
  const dirCount = isDir ? segments.length : Math.max(segments.length - 1, 0);
  const prefixes = [];
  for (let i = 1; i <= dirCount; i += 1) {
    prefixes.push(segments.slice(0, i).join("/"));
  }
  return prefixes;
}

function matchesIgnore(relPath, patterns, isDir = false) {
  if (!patterns.length) return false;
  const segments = relPath === "." ? [] : relPath.split("/");
  const dirPrefixes = buildDirPrefixes(relPath, isDir);
  for (const pattern of patterns) {
    if (pattern.dirOnly) {
      if (pattern.segment) {
        if (dirPrefixes.some((prefix) => prefix.split("/").pop() === pattern.segment)) {
          return true;
        }
      } else if (pattern.basenameRegex) {
        if (dirPrefixes.some((prefix) => pattern.basenameRegex.test(prefix.split("/").pop()))) {
          return true;
        }
      } else if (pattern.regex) {
        if (dirPrefixes.some((prefix) => pattern.regex.test(prefix))) {
          return true;
        }
      } else if (pattern.exactPath) {
        if (dirPrefixes.includes(pattern.exactPath)) return true;
      }
      continue;
    }

    if (pattern.segment) {
      if (segments.includes(pattern.segment)) return true;
    } else if (pattern.basenameRegex) {
      if (segments.some((segment) => pattern.basenameRegex.test(segment))) return true;
    } else if (pattern.regex) {
      if (pattern.regex.test(relPath)) return true;
    } else if (pattern.exactPath) {
      if (relPath === pattern.exactPath) return true;
      if (relPath.startsWith(`${pattern.exactPath}/`)) return true;
    }
  }
  return false;
}

function compileRulePatterns(patterns) {
  const compiled = [];
  for (const pattern of patterns) {
    const normalized = normalizePattern(pattern);
    if (!normalized) continue;
    if (normalized.includes("*") || normalized.includes("?")) {
      compiled.push({ raw: normalized, regex: globToRegExp(normalized) });
    } else {
      compiled.push({ raw: normalized, exact: normalized });
    }
  }
  return compiled;
}

function isRuleIgnored(ruleId, compiled) {
  if (!compiled.length) return false;
  for (const pattern of compiled) {
    if (pattern.regex) {
      if (pattern.regex.test(ruleId)) return true;
    } else if (ruleId === pattern.exact) {
      return true;
    }
  }
  return false;
}

function isBinary(buffer) {
  const sample = buffer.subarray(0, 8000);
  let suspicious = 0;
  for (const byte of sample) {
    if (byte === 0) return true;
    if (byte < 7 || (byte > 13 && byte < 32)) suspicious += 1;
  }
  return suspicious / Math.max(sample.length, 1) > 0.3;
}

function hashFile(filePath) {
  const hash = crypto.createHash("sha256");
  const data = fs.readFileSync(filePath);
  hash.update(data);
  return hash.digest("hex");
}

function readTextSample(filePath) {
  const fd = fs.openSync(filePath, "r");
  try {
    const stats = fs.fstatSync(fd);
    const readSize = Math.min(stats.size, MAX_SCAN_BYTES);
    const buffer = Buffer.alloc(readSize);
    fs.readSync(fd, buffer, 0, readSize, 0);
    if (isBinary(buffer)) return { text: null, truncated: false };
    const truncated = stats.size > MAX_SCAN_BYTES;
    return { text: buffer.toString("utf8"), truncated };
  } finally {
    fs.closeSync(fd);
  }
}

function toLines(text) {
  return text.split(/\r?\n/);
}

function buildFinding({ filePath, rule, line, lineNumber, match }) {
  return {
    file: filePath,
    ruleId: rule.id,
    severity: rule.severity,
    description: rule.description,
    rationale: rule.rationale || null,
    review: rule.review || null,
    line: line || "",
    lineNumber: lineNumber || null,
    match: match || "",
    context: rule.context || "code",
    scored: rule.scored !== false,
    confidence: rule.confidence || "high"
  };
}

function stripCommentsForScan(line, state, options = {}) {
  let value = line;
  if (state.inBlock) {
    const endIdx = value.indexOf("*/");
    if (endIdx === -1) return { text: "", inBlock: true, skipped: true };
    value = value.slice(endIdx + 2);
    state.inBlock = false;
  }

  while (true) {
    const startIdx = value.indexOf("/*");
    if (startIdx === -1) break;
    const endIdx = value.indexOf("*/", startIdx + 2);
    if (endIdx === -1) {
      value = value.slice(0, startIdx);
      state.inBlock = true;
      break;
    }
    value = value.slice(0, startIdx) + value.slice(endIdx + 2);
  }

  let cutIdx = -1;
  let slashIdx = value.indexOf("//");
  while (slashIdx !== -1) {
    const isHttp = value.slice(Math.max(0, slashIdx - 5), slashIdx + 2) === "http://";
    const isHttps = value.slice(Math.max(0, slashIdx - 6), slashIdx + 2) === "https://";
    if (!isHttp && !isHttps) {
      cutIdx = slashIdx;
      break;
    }
    slashIdx = value.indexOf("//", slashIdx + 2);
  }
  if (options.allowHashComments) {
    const hashIdx = value.indexOf("#");
    if (hashIdx !== -1 && (cutIdx === -1 || hashIdx < cutIdx)) cutIdx = hashIdx;
  }
  if (cutIdx !== -1) value = value.slice(0, cutIdx);

  return { text: value, inBlock: state.inBlock, skipped: !value.trim() };
}

function matchRuleInText(filePath, text, rule, findings, options = {}) {
  if (!text) return;
  const lines = toLines(text);
  const commentState = { inBlock: false };
  const ext = path.extname(filePath).toLowerCase();
  const allowHashComments = new Set([".py", ".sh", ".bash", ".zsh", ".rb", ".toml", ".yaml", ".yml", ".cfg", ".conf", ".ini"]).has(ext);
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    let targetLine = options.stripLiterals ? stripStringLiterals(line) : line;
    if (options.stripComments) {
      const stripped = stripCommentsForScan(targetLine, commentState, { allowHashComments });
      if (stripped.skipped) continue;
      targetLine = stripped.text;
    }
    const m = targetLine.match(rule.regex);
    if (m) {
      findings.push(
        buildFinding({
          filePath,
          rule,
          line: line.trim().slice(0, 200),
          lineNumber: i + 1,
          match: m[0].slice(0, 120)
        })
      );
    }
  }
}

function isDocFile(baseName, ext) {
  if (PROMPT_BASENAMES.has(baseName)) return false;
  return DOC_EXTENSIONS.has(ext);
}

function isRuleDefinitionFile(text) {
  if (!text) return false;
  const hasPatternNames =
    /\b(SHELL_PATTERNS|NETWORK_PATTERNS|SENSITIVE_PATH_PATTERNS|PROMPT_INJECTION_PATTERNS|OBFUSCATION_PATTERNS)\b/.test(
      text
    );
  const hasRegexFields = /\bregex\s*:\s*\/.+\//.test(text);
  return hasPatternNames && hasRegexFields;
}

function stripStringLiterals(line) {
  if (!line) return line;
  let out = "";
  let inSingle = false;
  let inDouble = false;
  let inTemplate = false;
  let templateExprDepth = 0;
  let escaped = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (escaped) {
      escaped = false;
      if (!inSingle && !inDouble && (!inTemplate || templateExprDepth > 0)) out += ch;
      continue;
    }
    if (ch === "\\") {
      escaped = true;
      if (!inSingle && !inDouble && (!inTemplate || templateExprDepth > 0)) out += ch;
      continue;
    }
    if (!inDouble && (!inTemplate || templateExprDepth > 0) && ch === "'") {
      inSingle = !inSingle;
      continue;
    }
    if (!inSingle && (!inTemplate || templateExprDepth > 0) && ch === "\"") {
      inDouble = !inDouble;
      continue;
    }
    if (!inSingle && !inDouble && ch === "`") {
      if (inTemplate && templateExprDepth === 0) {
        inTemplate = false;
        continue;
      }
      if (!inTemplate) {
        inTemplate = true;
        continue;
      }
    }
    if (inTemplate && templateExprDepth === 0) {
      if (ch === "$" && line[i + 1] === "{") {
        templateExprDepth = 1;
        i += 1;
        out += " ";
      }
      continue;
    }
    if (inTemplate && templateExprDepth > 0 && !inSingle && !inDouble) {
      if (ch === "{") {
        templateExprDepth += 1;
      } else if (ch === "}") {
        templateExprDepth -= 1;
        if (templateExprDepth === 0) continue;
      }
    }
    if (!inSingle && !inDouble && (!inTemplate || templateExprDepth > 0)) {
      out += ch;
    }
  }
  return out;
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function extractChildProcessAliases(text) {
  if (!text) return [];
  const aliases = new Set();
  const moduleName = escapeRegExp(NODE_PROCESS_MODULE);
  const patterns = [
    new RegExp(`\\b(?:const|let|var)\\s+([A-Za-z_$][\\w$]*)\\s*=\\s*require\\s*\\(\\s*["']${moduleName}["']\\s*\\)`, "g"),
    new RegExp(`\\bimport\\s+([A-Za-z_$][\\w$]*)\\s+from\\s+["']${moduleName}["']`, "g"),
    new RegExp(`\\bimport\\s+\\*\\s+as\\s+([A-Za-z_$][\\w$]*)\\s+from\\s+["']${moduleName}["']`, "g")
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(text)) !== null) {
      if (match[1]) aliases.add(match[1]);
    }
  }
  return [...aliases];
}

function buildAliasRules(aliases) {
  if (!aliases.length) return [];
  return aliases.map((alias) => ({
    id: "shell.exec_child" + "_process_alias",
    severity: "high",
    description: "Node process execution via alias",
    regex: new RegExp(`\\b${alias}\\s*\\.\\s*(exec|execSync|spawn|spawnSync)\\s*\\(`, "i")
  }));
}

function buildRuleSet(rules, context, scored, confidence) {
  return rules.map((rule) => ({
    ...rule,
    context,
    scored: rule.scored === undefined ? scored : rule.scored,
    confidence: rule.confidence || confidence
  }));
}

function scanText(filePath, text, findings, context, ignoreRules) {
  const ruleSets = [];
  if (context === "code" || context === "manifest") {
    const aliasRules = buildAliasRules(extractChildProcessAliases(text));
    ruleSets.push(
      ...buildRuleSet(SHELL_PATTERNS, "code", true, "high"),
      ...buildRuleSet(aliasRules, "code", true, "high"),
      ...buildRuleSet(NETWORK_PATTERNS, "code", true, "high"),
      ...buildRuleSet(SENSITIVE_PATH_PATTERNS, "code", true, "high"),
      ...buildRuleSet(OBFUSCATION_PATTERNS, "code", true, "medium")
    );
  } else if (context === "prompt") {
    ruleSets.push(...buildRuleSet(PROMPT_INJECTION_PATTERNS, "prompt", true, "medium"));
  } else if (context === "doc") {
    ruleSets.push(...buildRuleSet(PROMPT_INJECTION_PATTERNS, "doc", false, "low"));
  } else if (context === "rules") {
    return;
  }

  const stripLiterals = context === "code";
  const stripComments = context === "code";
  for (const rule of ruleSets) {
    if (isRuleIgnored(rule.id, ignoreRules)) continue;
    matchRuleInText(filePath, text, rule, findings, { stripLiterals, stripComments });
  }
}

function shouldScanFile(filePath, stats) {
  const ext = path.extname(filePath).toLowerCase();
  if (TEXT_EXTENSIONS.has(ext)) return true;
  if (BINARY_EXTENSIONS.has(ext)) return false;
  const base = path.basename(filePath).toLowerCase();
  if (PROMPT_BASENAMES.has(base)) return true;
  if (base === "requirements.txt" || base === "pyproject.toml") return true;
  if (base === "package.json") return true;
  if (TEXT_BASENAMES.has(base)) return true;
  if (stats && Number.isFinite(stats.size)) {
    return stats.size <= MAX_SCAN_BYTES;
  }
  return false;
}

function walkDir(
  rootPath,
  currentPath,
  results,
  symlinkResults,
  ignoreDirs,
  ignorePatterns,
  ignoredFiles
) {
  const entries = fs.readdirSync(currentPath, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(currentPath, entry.name);
    const relPath = normalizeRelative(rootPath, fullPath);
    if (entry.isDirectory()) {
      if (ignoreDirs.has(entry.name)) continue;
      if (matchesIgnore(relPath, ignorePatterns, true)) {
        ignoredFiles.push(`${relPath}/`);
        continue;
      }
      walkDir(
        rootPath,
        fullPath,
        results,
        symlinkResults,
        ignoreDirs,
        ignorePatterns,
        ignoredFiles
      );
    } else if (entry.isFile()) {
      if (matchesIgnore(relPath, ignorePatterns, false)) {
        ignoredFiles.push(relPath);
        continue;
      }
      results.push({ fullPath, relPath });
    } else if (entry.isSymbolicLink()) {
      if (matchesIgnore(relPath, ignorePatterns, false)) {
        ignoredFiles.push(relPath);
        continue;
      }
      symlinkResults.push({ fullPath, relPath });
    }
  }
}

const LIFECYCLE_SCRIPTS = new Set([
  "preinstall",
  "install",
  "postinstall",
  "prepublish",
  "prepublishOnly",
  "prepare",
  "postprepare",
  "prepack",
  "postpack",
  "pretest",
  "test",
  "posttest"
]);

const INSTALL_HOOK_SCRIPTS = new Set([
  "preinstall",
  "install",
  "postinstall",
  "prepublish",
  "prepublishOnly",
  "prepare"
]);

function normalizeScriptKeys(scripts) {
  if (!scripts || typeof scripts !== "object") return [];
  return Object.keys(scripts).filter((key) => typeof key === "string");
}

function formatDependencyEntries(dependencies) {
  if (!dependencies || typeof dependencies !== "object") return [];
  return Object.entries(dependencies).map(([name, version]) => {
    if (!version) return String(name);
    return `${name}@${version}`;
  });
}

function parsePackageJson(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    const json = JSON.parse(raw);
    const scriptKeys = normalizeScriptKeys(json.scripts);
    const lifecycleScripts = scriptKeys.filter((key) => LIFECYCLE_SCRIPTS.has(key));
    const installScripts = scriptKeys.filter((key) => INSTALL_HOOK_SCRIPTS.has(key));
    return {
      name: json.name || null,
      version: json.version || null,
      dependencies: uniqueStrings(formatDependencyEntries(json.dependencies)),
      devDependencies: uniqueStrings(formatDependencyEntries(json.devDependencies)),
      optionalDependencies: uniqueStrings(formatDependencyEntries(json.optionalDependencies)),
      peerDependencies: uniqueStrings(formatDependencyEntries(json.peerDependencies)),
      scripts: uniqueStrings(scriptKeys),
      lifecycleScripts: uniqueStrings(lifecycleScripts),
      installScripts: uniqueStrings(installScripts)
    };
  } catch (err) {
    return { error: "Failed to parse package.json" };
  }
}

function parseRequirements(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    const deps = raw
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#"));
    return { dependencies: deps };
  } catch (err) {
    return { error: "Failed to parse requirements.txt" };
  }
}

function parsePyproject(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    const deps = [];
    const lines = raw.split(/\r?\n/);
    let inProject = false;
    let collecting = false;
    let buffer = "";

    const flushBuffer = () => {
      if (!buffer.trim()) return;
      const matches = buffer.match(/(["'])(.*?)\1/g) || [];
      for (const match of matches) {
        const value = match.slice(1, -1).trim();
        if (value) deps.push(value);
      }
    };

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      if (trimmed.startsWith("[project]")) {
        inProject = true;
        collecting = false;
        buffer = "";
        continue;
      }
      if (trimmed.startsWith("[") && !trimmed.startsWith("[project]")) {
        if (collecting) flushBuffer();
        inProject = false;
        collecting = false;
        buffer = "";
        continue;
      }
      if (!inProject) continue;

      if (!collecting && trimmed.startsWith("dependencies")) {
        const idx = trimmed.indexOf("=");
        if (idx === -1) continue;
        const remainder = trimmed.slice(idx + 1).trim();
        buffer = remainder;
        if (remainder.includes("[")) {
          collecting = true;
        }
        if (remainder.includes("]")) {
          collecting = false;
          flushBuffer();
          buffer = "";
        }
        continue;
      }

      if (collecting) {
        buffer += ` ${trimmed}`;
        if (trimmed.includes("]")) {
          collecting = false;
          flushBuffer();
          buffer = "";
        }
      }
    }
    if (collecting) flushBuffer();
    return { dependencies: uniqueStrings(deps) };
  } catch (err) {
    return { error: "Failed to parse pyproject.toml" };
  }
}

function classifyOverall(findings, comboRisks = []) {
  const severityOrder = ["low", "medium", "high", "critical"];
  let maxSeverity = "low";
  let score = 0;
  const weights = { low: 1, medium: 3, high: 6, critical: 10 };
  const scoredFindings = findings.filter((finding) => finding.scored !== false);
  const allSignals = [
    ...scoredFindings.map((finding) => ({ severity: finding.severity })),
    ...comboRisks.map((combo) => ({ severity: combo.severity }))
  ];
  for (const finding of allSignals) {
    score += weights[finding.severity] || 1;
    if (severityOrder.indexOf(finding.severity) > severityOrder.indexOf(maxSeverity)) {
      maxSeverity = finding.severity;
    }
  }
  let level = maxSeverity;
  if (score >= 25 || maxSeverity === "critical") level = "critical";
  else if (score >= 12 || maxSeverity === "high") level = "high";
  else if (score >= 5 || maxSeverity === "medium") level = "medium";
  else level = "low";
  return { score, level };
}

function computeComboRisks(findings) {
  const scoredFindings = findings.filter((finding) => finding.scored !== false);
  const has = {
    shell: false,
    network: false,
    sensitive: false,
    prompt: false,
    obfuscation: false
  };
  const evidenceByTag = {
    shell: new Set(),
    network: new Set(),
    sensitive: new Set(),
    prompt: new Set(),
    obfuscation: new Set()
  };

  for (const finding of scoredFindings) {
    if (finding.ruleId.startsWith("shell.")) {
      has.shell = true;
      evidenceByTag.shell.add(finding.ruleId);
    }
    if (finding.ruleId.startsWith("net.")) {
      has.network = true;
      evidenceByTag.network.add(finding.ruleId);
    }
    if (finding.ruleId.startsWith("sensitive.")) {
      has.sensitive = true;
      evidenceByTag.sensitive.add(finding.ruleId);
    }
    if (finding.ruleId.startsWith("prompt.")) {
      has.prompt = true;
      evidenceByTag.prompt.add(finding.ruleId);
    }
    if (finding.ruleId.startsWith("obfuscation.")) {
      has.obfuscation = true;
      evidenceByTag.obfuscation.add(finding.ruleId);
    }
  }

  const combos = [];

  if (has.shell && has.network) {
    combos.push({
      id: "combo.shell_network",
      severity: "high",
      description: "Shell execution combined with outbound network access can enable remote code execution.",
      evidence: [...evidenceByTag.shell, ...evidenceByTag.network]
    });
  }

  if (has.network && has.sensitive) {
    combos.push({
      id: "combo.network_sensitive",
      severity: "high",
      description: "Outbound network access plus sensitive file references increases exfiltration risk.",
      evidence: [...evidenceByTag.network, ...evidenceByTag.sensitive]
    });
  }

  if (has.shell && has.prompt) {
    combos.push({
      id: "combo.shell_prompt",
      severity: "high",
      description: "Shell execution combined with prompt injection signals raises execution control risk.",
      evidence: [...evidenceByTag.shell, ...evidenceByTag.prompt]
    });
  }

  if (has.obfuscation && (has.shell || has.network)) {
    combos.push({
      id: "combo.obfuscation_active",
      severity: "medium",
      description: "Obfuscation indicators combined with active capabilities suggest hidden behavior.",
      evidence: [...evidenceByTag.obfuscation, ...evidenceByTag.shell, ...evidenceByTag.network]
    });
  }

  return combos.map((combo) => ({
    ...combo,
    evidence: uniqueStrings(combo.evidence)
  }));
}

function buildRiskProfile(findings) {
  const comboRisks = computeComboRisks(findings);
  const risk = classifyOverall(findings, comboRisks);
  return { risk, comboRisks };
}

function scanPath(rootPath, options = {}) {
  const ignoreDirs = options.ignoreDirs || DEFAULT_IGNORE_DIRS;
  const runtimeIgnorePaths = normalizeRuntimeIgnorePaths(options.runtimeIgnorePaths);
  const ignorePaths = uniqueStrings([...(options.ignorePaths || []), ...runtimeIgnorePaths]);
  const ignorePathPatterns = compileIgnorePatterns(ignorePaths);
  const ignoreRulePatterns = compileRulePatterns(options.ignoreRules || []);
  const basePath = options.basePath || process.cwd();
  const rootId = resolveRootId(rootPath);

  const files = [];
  const symlinkFiles = [];
  const ignoredFiles = [];
  walkDir(
    rootPath,
    rootPath,
    files,
    symlinkFiles,
    ignoreDirs,
    ignorePathPatterns,
    ignoredFiles
  );

  const findings = [];
  const hashes = {};
  const scannedFiles = [];
  const skippedFiles = [];
  const manifests = {};
  const symlinks = [];

  for (const link of symlinkFiles) {
    const relPath = link.relPath;
    let target = null;
    let broken = null;
    try {
      target = fs.readlinkSync(link.fullPath);
      let resolved = target;
      if (target && !path.isAbsolute(target)) {
        resolved = path.resolve(path.dirname(link.fullPath), target);
      }
      if (resolved) {
        try {
          broken = !fs.existsSync(resolved);
        } catch (err) {
          broken = null;
        }
      }
    } catch (err) {
      target = null;
      broken = null;
    }
    symlinks.push({ path: relPath, target, broken });
  }
  symlinks.sort((a, b) => a.path.localeCompare(b.path));

  for (const file of files) {
    const filePath = file.fullPath;
    const relPath = file.relPath;
    let stats;
    try {
      stats = fs.statSync(filePath);
    } catch (err) {
      skippedFiles.push(relPath);
      continue;
    }

    try {
      hashes[relPath] = hashFile(filePath);
    } catch (err) {
      skippedFiles.push(relPath);
      continue;
    }

    if (!shouldScanFile(filePath, stats)) {
      skippedFiles.push(relPath);
      continue;
    }

    const base = path.basename(filePath).toLowerCase();
    if (base === "package.json") manifests.packageJson = parsePackageJson(filePath);
    if (base === "requirements.txt") manifests.requirements = parseRequirements(filePath);
    if (base === "pyproject.toml") manifests.pyproject = parsePyproject(filePath);

    const { text, truncated } = readTextSample(filePath);

    if (text === null) {
      skippedFiles.push(relPath);
      continue;
    }

    const ext = path.extname(filePath).toLowerCase();
    let context = "code";
    if (base === "package.json") {
      context = "manifest";
    } else if (PROMPT_BASENAMES.has(base)) {
      context = "prompt";
    } else if (isDocFile(base, ext)) {
      context = "doc";
    } else if (isRuleDefinitionFile(text)) {
      context = "rules";
    }

    scanText(relPath, text, findings, context, ignoreRulePatterns);
    scannedFiles.push({ file: relPath, truncated });
  }

  const scoredFindings = findings.filter((finding) => finding.scored !== false);
  const { risk, comboRisks } = buildRiskProfile(findings);

  return {
    version: VERSION,
    rootPath: toPosix(path.relative(basePath, rootPath)) || ".",
    rootId,
    meta: buildScanMeta(rootPath, options),
    stats: {
      totalFiles: files.length + ignoredFiles.length,
      scannedFiles: scannedFiles.length,
      skippedFiles: skippedFiles.length,
      ignoredFiles: ignoredFiles.length,
      symlinks: symlinks.length,
      findings: scoredFindings.length,
      totalFindings: findings.length,
      unscoredFindings: findings.length - scoredFindings.length,
      comboFindings: comboRisks.length
    },
    config: {
      path: options.configPath
        ? toPosix(path.relative(basePath, options.configPath))
        : options.configPath,
      ignorePaths: options.ignorePaths || [],
      ignoreRules: options.ignoreRules || []
    },
    risk,
    findings,
    comboRisks,
    manifests,
    symlinks,
    hashes,
    scannedFiles,
    skippedFiles,
    ignoredFiles
  };
}

function compareHashes(currentHashes, baselineHashes) {
  const added = [];
  const removed = [];
  const changed = [];
  const unchanged = [];

  for (const [file, hash] of Object.entries(currentHashes)) {
    if (!baselineHashes[file]) {
      added.push(file);
    } else if (baselineHashes[file] !== hash) {
      changed.push({ file, baseline: baselineHashes[file], current: hash });
    } else {
      unchanged.push(file);
    }
  }

  for (const file of Object.keys(baselineHashes)) {
    if (!currentHashes[file]) removed.push(file);
  }

  return {
    added,
    removed,
    changed,
    unchanged,
    unchangedCount: unchanged.length
  };
}

function normalizeSymlinkList(list) {
  const map = {};
  if (!Array.isArray(list)) return map;
  for (const entry of list) {
    if (!entry || !entry.path) continue;
    map[entry.path] = {
      target: entry.target === undefined ? null : entry.target,
      broken: entry.broken === undefined ? null : entry.broken
    };
  }
  return map;
}

function compareSymlinks(currentSymlinks, baselineSymlinks) {
  const added = [];
  const removed = [];
  const changed = [];
  const unchanged = [];
  const currentMap = normalizeSymlinkList(currentSymlinks);
  const baselineMap = normalizeSymlinkList(baselineSymlinks);

  for (const [linkPath, meta] of Object.entries(currentMap)) {
    if (!baselineMap[linkPath]) {
      added.push(linkPath);
    } else if (
      baselineMap[linkPath].target !== meta.target ||
      baselineMap[linkPath].broken !== meta.broken
    ) {
      changed.push({ file: linkPath, baseline: baselineMap[linkPath], current: meta });
    } else {
      unchanged.push(linkPath);
    }
  }

  for (const linkPath of Object.keys(baselineMap)) {
    if (!currentMap[linkPath]) removed.push(linkPath);
  }

  return {
    added,
    removed,
    changed,
    unchanged,
    unchangedCount: unchanged.length
  };
}

function saveBaseline(filePath, report, trustMeta = null) {
  const rootId =
    report.rootId ||
    (report.meta && report.meta.rootId) ||
    (report.meta && report.meta.rootPath) ||
    report.rootPath ||
    null;
  const payload = {
    version: report.version || VERSION,
    createdAt: new Date().toISOString(),
    rootPath: report.rootPath,
    rootId,
    rootRealPath: report.meta ? report.meta.rootPath : null,
    trust: trustMeta,
    config: report.config || { ignorePaths: [], ignoreRules: [] },
    manifests: report.manifests || {},
    hashes: report.hashes,
    symlinks: report.symlinks || []
  };
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2));
}

function buildScanMeta(rootPath, options) {
  const basePath = options.basePath || process.cwd();
  return {
    scannedAt: new Date().toISOString(),
    basePath: toPosix(path.resolve(basePath)),
    rootPath: toPosix(path.resolve(rootPath)),
    rootId: resolveRootId(rootPath),
    ignorePaths: options.ignorePaths || [],
    runtimeIgnorePaths: options.runtimeIgnorePaths || [],
    ignoreRules: options.ignoreRules || []
  };
}

module.exports = {
  scanPath,
  classifyOverall,
  computeComboRisks,
  buildRiskProfile,
  loadConfig,
  compareHashes,
  compareSymlinks,
  saveBaseline
};
