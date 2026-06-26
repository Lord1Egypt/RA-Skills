import path from "node:path";

const READ_ONLY_TOOL_NAMES = new Set([
  "read",
  "read_many",
  "readmany",
  "glob",
  "grep",
  "ls",
  "list_dir",
  "listdir",
  "list_directory",
  "directory_tree",
  "stat"
]);

const EXEC_LIKE_TOOL_NAMES = new Set([
  "exec",
  "bash",
  "shell",
  "terminal",
  "command"
]);

const READ_ONLY_EXEC_COMMANDS = new Set([
  "cat",
  "diff",
  "du",
  "fd",
  "find",
  "grep",
  "head",
  "less",
  "ls",
  "more",
  "pwd",
  "rg",
  "stat",
  "tail",
  "tree",
  "wc",
  "whereis",
  "which"
]);

const NEUTRAL_EXEC_COMMANDS = new Set([
  "cd",
  "pushd",
  "popd",
  "true"
]);

const READ_ONLY_GIT_SUBCOMMANDS = new Set([
  "blame",
  "branch",
  "describe",
  "diff",
  "grep",
  "log",
  "ls_files",
  "remote",
  "rev_parse",
  "show",
  "status"
]);

const TARGET_PARAM_KEYS = [
  "targetPath",
  "target_path",
  "path",
  "filePath",
  "file_path",
  "filepath",
  "file",
  "filename",
  "name",
  "target",
  "destination",
  "destinationPath",
  "destination_path",
  "dest",
  "output",
  "outputPath",
  "output_path",
  "source",
  "sourcePath",
  "source_path",
  "src",
  "url",
  "uri"
];

const COMMAND_PARAM_KEYS = ["command", "cmd", "script", "shell", "input", "text"];

export function normalizeToolToken(value) {
  return String(value ?? "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function findNestedValueByKeys(value, keys, seen = new Set(), depth = 0) {
  if (!value || typeof value !== "object" || depth > 4 || seen.has(value)) {
    return null;
  }

  seen.add(value);

  for (const key of keys) {
    if (value[key] !== undefined && value[key] !== null && value[key] !== "") {
      return value[key];
    }
  }

  const entries = Array.isArray(value) ? value : Object.values(value);

  for (const entry of entries) {
    const nested = findNestedValueByKeys(entry, keys, seen, depth + 1);
    if (nested !== null) {
      return nested;
    }
  }

  return null;
}

function compactWhitespace(value) {
  return String(value ?? "")
    .trim()
    .replace(/\s+/g, " ");
}

function shortenSummaryValue(value, maxLength = 96) {
  const normalized = compactWhitespace(value);

  if (!normalized) {
    return null;
  }

  if (normalized.length <= maxLength) {
    return normalized;
  }

  return `${normalized.slice(0, Math.max(0, maxLength - 3))}...`;
}

function summarizePathLike(value) {
  const raw = compactWhitespace(value);

  if (!raw) {
    return null;
  }

  const baseName = path.basename(raw);
  if (baseName && baseName !== raw && /\.[^./]+$/.test(baseName) && baseName.length <= 32) {
    return baseName;
  }

  const normalized = shortenSummaryValue(raw, 72);

  if (!normalized) {
    return null;
  }

  const parts = normalized.split(/[\\/]+/).filter(Boolean);

  if (normalized.length <= 40 || parts.length < 2) {
    return normalized;
  }

  return `.../${parts.slice(-2).join("/")}`;
}

export function extractCommandText(params) {
  if (typeof params === "string") {
    return compactWhitespace(params) || null;
  }

  if (!isPlainObject(params) && !Array.isArray(params)) {
    return null;
  }

  const command = findNestedValueByKeys(params, COMMAND_PARAM_KEYS);
  return typeof command === "string" ? compactWhitespace(command) : null;
}

export function splitShellSegments(commandText) {
  return String(commandText ?? "")
    .split(/&&|\|\||;|\|/)
    .map((segment) => segment.trim())
    .filter(Boolean);
}

function unquoteShellToken(token) {
  return String(token ?? "").replace(/^['"]|['"]$/g, "");
}

function tokenizeShellSegment(segment) {
  return segment.match(/"[^"]+"|'[^']+'|\S+/g)?.map(unquoteShellToken) ?? [];
}

function stripEnvAssignments(tokens) {
  let index = 0;

  while (index < tokens.length && /^[A-Za-z_][A-Za-z0-9_]*=.*/.test(tokens[index])) {
    index += 1;
  }

  return tokens.slice(index);
}

function resolveGitSubcommand(tokens) {
  let index = 1;

  while (index < tokens.length) {
    const token = tokens[index];

    if (["-C", "--git-dir", "--work-tree", "-c"].includes(token)) {
      index += 2;
      continue;
    }

    if (token.startsWith("-")) {
      index += 1;
      continue;
    }

    return normalizeToolToken(token);
  }

  return "";
}

function isReadOnlyFindInvocation(tokens) {
  return !tokens.some((token, index) =>
    token === "-delete" ||
    (token === "-exec" && tokens[index + 1] && normalizeToolToken(tokens[index + 1]) !== "echo") ||
    token === "-execdir" ||
    token === "-ok" ||
    token === "-okdir"
  );
}

function isReadOnlyExecSegment(segment) {
  const stripped = stripEnvAssignments(tokenizeShellSegment(segment));

  if (!stripped.length) {
    return true;
  }

  const command = normalizeToolToken(stripped[0]);

  if (!command) {
    return false;
  }

  if (NEUTRAL_EXEC_COMMANDS.has(command)) {
    return true;
  }

  if (command === "git") {
    return READ_ONLY_GIT_SUBCOMMANDS.has(resolveGitSubcommand(stripped));
  }

  if (command === "find") {
    return isReadOnlyFindInvocation(stripped);
  }

  return READ_ONLY_EXEC_COMMANDS.has(command);
}

export function shouldCreateCheckpointForTool(ctx) {
  const toolName = normalizeToolToken(ctx?.toolName);

  if (!toolName) {
    return true;
  }

  if (READ_ONLY_TOOL_NAMES.has(toolName)) {
    return false;
  }

  if (!EXEC_LIKE_TOOL_NAMES.has(toolName)) {
    return true;
  }

  const commandText = extractCommandText(ctx?.params);

  if (!commandText) {
    return true;
  }

  const segments = splitShellSegments(commandText);

  if (!segments.length) {
    return true;
  }

  return !segments.every((segment) => isReadOnlyExecSegment(segment));
}

function summarizeTargetValue(value) {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  if (typeof value === "string") {
    return summarizePathLike(value);
  }

  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }

  if (Array.isArray(value)) {
    const items = value
      .map((entry) => summarizeTargetValue(entry))
      .filter(Boolean);

    if (!items.length) {
      return null;
    }

    return shortenSummaryValue(items.slice(0, 2).join(", "), 72);
  }

  if (typeof value === "object") {
    const nested = findNestedValueByKeys(value, TARGET_PARAM_KEYS);
    return nested === null ? null : summarizeTargetValue(nested);
  }

  return shortenSummaryValue(value, 72);
}

function summarizeExecCommand(commandText) {
  const raw = compactWhitespace(commandText);

  if (!raw) {
    return null;
  }

  const compact = shortenSummaryValue(raw, 88);
  const tokens = raw.match(/"[^"]+"|'[^']+'|\S+/g)?.map(unquoteShellToken) ?? [];
  const firstCommandIndex = tokens.findIndex((token) => !token.startsWith("-"));
  const command = firstCommandIndex >= 0 ? path.basename(tokens[firstCommandIndex]).toLowerCase() : "";
  const targetToken = tokens.slice(firstCommandIndex + 1).find((token) => token && !token.startsWith("-"));
  const target = summarizeTargetValue(targetToken);

  switch (command) {
    case "rm":
    case "unlink":
    case "del":
      return target ? `delete ${target}` : "delete files";
    case "mv":
      return target ? `move ${target}` : compact;
    case "cp":
      return target ? `copy ${target}` : compact;
    case "mkdir":
      return target ? `create ${target}` : compact;
    case "cat":
    case "less":
      return target ? `read ${target}` : compact;
    default:
      return compact;
  }
}

export function buildCheckpointSummary(ctx) {
  const toolName = shortenSummaryValue(ctx?.toolName, 24) ?? "tool";
  const params = ctx?.params;

  if (typeof params === "string") {
    if (toolName.toLowerCase() === "exec") {
      const execSummary = summarizeExecCommand(params);
      if (execSummary) {
        return `before tool ${toolName} ${execSummary}`;
      }
    }

    const text = shortenSummaryValue(params, 72);
    if (text) {
      return `before tool ${toolName} ${text}`;
    }
  }

  if (params && typeof params === "object") {
    if (toolName.toLowerCase() === "exec") {
      const execSummary = summarizeExecCommand(extractCommandText(params));
      if (execSummary) {
        return `before tool ${toolName} ${execSummary}`;
      }
    }

    const target = summarizeTargetValue(findNestedValueByKeys(params, TARGET_PARAM_KEYS));
    if (target) {
      return `before tool ${toolName} ${target}`;
    }

    const command = extractCommandText(params);
    if (command) {
      return `before tool ${toolName} ${shortenSummaryValue(command, 88)}`;
    }
  }

  return `before tool ${toolName}`;
}
