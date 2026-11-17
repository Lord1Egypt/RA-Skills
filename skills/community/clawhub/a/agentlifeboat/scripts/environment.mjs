// What the agent has around its state directory, recorded with every snapshot (KIN-112, tool parity).
// Names only, never values: which binaries resolve on PATH, which env var names the config and skills
// reference and whether they are set, which MCP servers the config declares. A restored room records
// the same and reports the difference. The sidecar has the same logic in TypeScript (apps/sidecar/src/environment.ts).
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { delimiter, join } from "node:path";

/** Tools agents commonly lean on; probed on every host so a restore can say which vanished. */
export const PROBE_BINS = ["node", "npm", "npx", "bun", "deno", "python3", "python", "pip", "pip3", "uv", "git", "gh", "curl", "wget", "jq", "rg", "docker", "ffmpeg", "sqlite3", "ssh", "rsync", "go", "cargo", "chromium", "google-chrome"];

const NAME = /^[A-Za-z0-9_.+-]{1,64}$/;
/** Caps on the record, the same as the sidecar's: a huge workspace gets truncated, never a throw. */
export const LIMITS = { skills: 500, bins: 1000, envVars: 1000, mcpServers: 200 };
export const MAX_CONFIG_CHARS = 1_000_000;

/** Frontmatter of a SKILL.md: `requires.bins` and `requires.env`, inline `[a, b]` or dash lists. */
export function parseSkillRequires(skillMd) {
  const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(skillMd);
  if (!fm) return { bins: [], env: [] };
  const block = fm[1];
  const list = (key) => {
    const inline = new RegExp(`^\\s*${key}:\\s*\\[([^\\]]*)\\]`, "m").exec(block);
    if (inline) return inline[1].split(",").map((s) => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean);
    const dash = new RegExp(`^(\\s*)${key}:\\s*\\r?\\n((?:\\1\\s+-\\s*.*\\r?\\n?)+)`, "m").exec(block);
    if (dash) return dash[2].split(/\r?\n/).map((l) => l.replace(/^\s*-\s*/, "").trim().replace(/^["']|["']$/g, "")).filter(Boolean);
    return [];
  };
  return { bins: list("bins").filter((b) => NAME.test(b)), env: list("env").filter((e) => /^[A-Z_][A-Z0-9_]*$/.test(e)) };
}

/** Skills under <workspace>/skills/<name>/SKILL.md with what each requires. */
export function readSkills(workspaceDir) {
  const dir = join(workspaceDir, "skills");
  if (!existsSync(dir)) return [];
  const out = [];
  for (const name of readdirSync(dir).sort()) {
    const md = join(dir, name, "SKILL.md");
    try {
      if (!statSync(join(dir, name)).isDirectory() || !existsSync(md)) continue;
      const req = parseSkillRequires(readFileSync(md, "utf8"));
      out.push({ name, bins: req.bins, env: req.env });
    } catch {
      /* unreadable skill: not our concern here */
    }
  }
  return out;
}

/** `${NAME}` references in the config text (JSON5 or JSON), names only. */
export function envRefsIn(configText) {
  const names = new Set();
  for (const m of configText.matchAll(/\$\{([A-Z_][A-Z0-9_]*)\}/g)) names.add(m[1]);
  return [...names].sort();
}

/**
 * Keys of the object whose `{` is at `open` in JSON or JSON5 text (quoted or bare keys, comments, nested
 * objects skipped). The config is JSON5 as OpenClaw writes it, so no JSON parser will do.
 */
export function objectKeysAt(text, open) {
  const keys = [];
  let depth = 0;
  let i = open;
  while (i < text.length) {
    const ch = text[i];
    if (ch === "/" && text[i + 1] === "/") {
      i = text.indexOf("\n", i);
      if (i < 0) break;
      continue;
    }
    if (ch === "/" && text[i + 1] === "*") {
      const end = text.indexOf("*/", i + 2);
      i = end < 0 ? text.length : end + 2;
      continue;
    }
    if (ch === '"' || ch === "'") {
      let j = i + 1;
      while (j < text.length && text[j] !== ch) j += text[j] === "\\" ? 2 : 1;
      const s = text.slice(i + 1, j);
      i = j + 1;
      if (depth === 1 && /^\s*:/.test(text.slice(i, i + 40))) keys.push(s);
      continue;
    }
    if (ch === "{" || ch === "[") depth++;
    else if (ch === "}" || ch === "]") {
      depth--;
      if (depth <= 0) break;
    } else if (depth === 1 && /[A-Za-z_$]/.test(ch)) {
      let j = i;
      while (j < text.length && /[A-Za-z0-9_$.-]/.test(text[j])) j++;
      const word = text.slice(i, j);
      if (/^\s*:/.test(text.slice(j, j + 40))) keys.push(word);
      i = j;
      continue;
    }
    i++;
  }
  return keys;
}

/** The text with comments blanked out (string-aware), so a key mentioned in a comment is never taken for real. */
export function stripComments(text) {
  let out = "";
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === '"' || ch === "'") {
      let j = i + 1;
      while (j < text.length && text[j] !== ch) j += text[j] === "\\" ? 2 : 1;
      out += text.slice(i, j + 1);
      i = j + 1;
    } else if (ch === "/" && text[i + 1] === "/") {
      const end = text.indexOf("\n", i);
      i = end < 0 ? text.length : end;
    } else if (ch === "/" && text[i + 1] === "*") {
      const end = text.indexOf("*/", i + 2);
      out += " ";
      i = end < 0 ? text.length : end + 2;
    } else {
      out += ch;
      i++;
    }
  }
  return out;
}

/** Index of the `}` closing the object whose `{` is at `open` (string-aware), or the text end. */
export function objectEndAt(text, open) {
  let depth = 0;
  let i = open;
  while (i < text.length) {
    const ch = text[i];
    if (ch === '"' || ch === "'") {
      let j = i + 1;
      while (j < text.length && text[j] !== ch) j += text[j] === "\\" ? 2 : 1;
      i = j + 1;
      continue;
    }
    if (ch === "{" || ch === "[") depth++;
    else if (ch === "}" || ch === "]") {
      depth--;
      if (depth <= 0) return i;
    }
    i++;
  }
  return text.length;
}

/** MCP server names declared in the config text: keys of `mcpServers`, or of `servers` inside `mcp`. Comments are ignored. */
export function mcpServersIn(configText) {
  const text = stripComments(configText);
  const names = new Set();
  const opener = (key, from = 0) => {
    const m = new RegExp(`(?:^|[{,\\s])(?:"${key}"|'${key}'|${key})\\s*:\\s*\\{`, "g");
    m.lastIndex = from;
    const r = m.exec(text);
    return r ? r.index + r[0].length - 1 : -1;
  };
  for (let at = opener("mcpServers"); at >= 0; at = opener("mcpServers", at + 1)) for (const k of objectKeysAt(text, at)) names.add(k);
  for (let at = opener("mcp"); at >= 0; at = opener("mcp", at + 1)) {
    const inner = opener("servers", at);
    if (inner > at && inner < objectEndAt(text, at)) for (const k of objectKeysAt(text, inner)) names.add(k);
  }
  return [...names].filter((n) => NAME.test(n)).sort();
}

/** Whether a binary resolves on PATH (Windows also tries .exe and .cmd). */
export function binOnPath(name, pathEnv = process.env.PATH ?? "", platform = process.platform) {
  const exts = platform === "win32" ? ["", ".exe", ".cmd", ".bat"] : [""];
  for (const dir of pathEnv.split(delimiter).filter(Boolean)) {
    for (const ext of exts) {
      try {
        if (statSync(join(dir, name + ext)).isFile()) return true;
      } catch {
        /* not here */
      }
    }
  }
  return false;
}

/**
 * The record. `stateDir` holds openclaw.json, `workspaceDir` holds skills/. `env` and `pathEnv` are injectable for tests.
 */
export function recordEnvironment({ stateDir, workspaceDir, env = process.env, pathEnv = process.env.PATH ?? "", platform = process.platform, now = new Date(), extraEnvNames = [] }) {
  const configPath = join(stateDir, "openclaw.json");
  const configText = existsSync(configPath) ? readFileSync(configPath, "utf8").slice(0, MAX_CONFIG_CHARS) : "";
  const skills = readSkills(workspaceDir).slice(0, LIMITS.skills);
  const binNames = new Set(PROBE_BINS);
  const envNames = new Set(envRefsIn(configText));
  for (const s of skills) {
    for (const b of s.bins) binNames.add(b);
    for (const e of s.env) envNames.add(e);
  }
  for (const n of extraEnvNames) if (/^[A-Z_][A-Z0-9_]*$/.test(n)) envNames.add(n);
  return {
    v: 1,
    recordedAt: now.toISOString(),
    platform: { os: platform, arch: process.arch, node: process.version },
    skills,
    bins: [...binNames].sort().slice(0, LIMITS.bins).map((name) => ({ name, found: binOnPath(name, pathEnv, platform) })),
    envVars: [...envNames].sort().slice(0, LIMITS.envVars).map((name) => ({ name, set: Boolean(env[name]) })),
    mcpServers: mcpServersIn(configText).slice(0, LIMITS.mcpServers),
  };
}

/** What a restored room lacks compared with the record its snapshot carried. */
export function diffEnvironment(before, after) {
  const foundBefore = new Set((before?.bins ?? []).filter((b) => b.found).map((b) => b.name));
  const foundAfter = new Set((after?.bins ?? []).filter((b) => b.found).map((b) => b.name));
  const setBefore = new Set((before?.envVars ?? []).filter((e) => e.set).map((e) => e.name));
  const setAfter = new Set((after?.envVars ?? []).filter((e) => e.set).map((e) => e.name));
  return {
    bins: [...foundBefore].filter((n) => !foundAfter.has(n)).sort(),
    envVars: [...setBefore].filter((n) => !setAfter.has(n)).sort(),
    // Declared servers are processes on the old machine: never carried, listed so the agent knows to start them.
    mcpServers: [...(before?.mcpServers ?? [])].sort(),
  };
}

/** The report a restored agent finds in its workspace. */
export function renderRestoreReport(gaps, { recordedAt, restoredAt }) {
  const lines = [
    "# Restore report",
    "",
    `Restored ${restoredAt} from a snapshot recorded ${recordedAt ?? "at an unknown time"}. A restore brings back your files, not your machine; this is what the old machine had and this room does not.`,
    "",
    "## Binaries that resolved before and do not now",
    ...(gaps.bins.length ? gaps.bins.map((b) => `- ${b}`) : ["- none"]),
    "",
    "## Environment variables that were set before and are not now (names only)",
    ...(gaps.envVars.length ? gaps.envVars.map((e) => `- ${e}`) : ["- none"]),
    "",
    "## MCP servers your config declares (processes are never carried; start or replace them)",
    ...(gaps.mcpServers.length ? gaps.mcpServers.map((m) => `- ${m}`) : ["- none"]),
    "",
    "Your status at The Estate shows the same under `gaps`. Delete this file once you have dealt with it.",
    "",
  ];
  return lines.join("\n");
}
