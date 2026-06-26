const fs = require('fs');
const path = require('path');

function ensureDir(dir) {
  try {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  } catch (e) {}
}

function nowIso() {
  return new Date().toISOString();
}

function clip(text, maxChars) {
  const s = String(text || '');
  const n = Number(maxChars);
  if (!Number.isFinite(n) || n <= 0) return s;
  if (s.length <= n) return s;
  return s.slice(0, Math.max(0, n - 40)) + '\n...[TRUNCATED]...\n';
}

function writePromptArtifact({ memoryDir, cycleId, runId, prompt, meta }) {
  const dir = String(memoryDir || '').trim();
  if (!dir) throw new Error('bridge: missing memoryDir');
  ensureDir(dir);
  const safeCycle = String(cycleId || 'cycle').replace(/[^a-zA-Z0-9_\-#]/g, '_');
  const safeRun = String(runId || Date.now()).replace(/[^a-zA-Z0-9_\-]/g, '_');
  const base = `gep_prompt_${safeCycle}_${safeRun}`;
  const promptPath = path.join(dir, base + '.txt');
  const metaPath = path.join(dir, base + '.json');

  fs.writeFileSync(promptPath, String(prompt || ''), 'utf8');
  fs.writeFileSync(
    metaPath,
    JSON.stringify(
      {
        type: 'GepPromptArtifact',
        at: nowIso(),
        cycle_id: cycleId || null,
        run_id: runId || null,
        prompt_path: promptPath,
        meta: meta && typeof meta === 'object' ? meta : null,
      },
      null,
      2
    ) + '\n',
    'utf8'
  );

  return { promptPath, metaPath };
}

function renderSessionsSpawnCall({ task, agentId, label, cleanup }) {
  const t = String(task || '').trim();
  if (!t) throw new Error('bridge: missing task');
  const a = String(agentId || 'main');
  const l = String(label || 'gep_bridge');
  const c = cleanup ? String(cleanup) : 'delete';

  // Output valid JSON so consumers can parse with JSON.parse (not regex).
  // The consumer side is extractFirstSpawnPayload()/parseFirstSpawnCall() below,
  // which take the FIRST sessions_spawn( occurrence — see those functions for why.
  const payload = JSON.stringify({ task: t, agentId: a, cleanup: c, label: l });
  return `sessions_spawn(${payload})`;
}

const SPAWN_MARKER = 'sessions_spawn(';

// Extract the raw JSON string of the FIRST sessions_spawn(...) call in `text`,
// or null if none. Consumer side of renderSessionsSpawnCall — a host wrapper /
// exec bridge scrapes the Brain's stdout for this to know which executor (the
// "Hand") to spawn.
//
// Why brace-depth counting, not a regex: a regex like /{[\s\S]*?}/ truncates at
// the first '}', which breaks on the nested JSON inside the payload's `task`
// field (the task carries the full GEP prompt). We walk braces while respecting
// JSON string literals so a '}' inside a string doesn't close the object.
//
// Why FIRST, not last: the GEP prompt embedded in the `task` field contains
// EXAMPLE sessions_spawn(...) calls (loop-chaining instructions). The real
// bridge call the Brain emits is always the first occurrence in stdout; taking
// the last would match an example inside the task and mis-spawn.
function extractFirstSpawnPayload(text) {
  const s = String(text || '');
  const idx = s.indexOf(SPAWN_MARKER);
  if (idx === -1) return null;

  // Locate the opening brace after the marker (allow only whitespace between).
  let braceStart = -1;
  for (let i = idx + SPAWN_MARKER.length; i < s.length; i++) {
    if (s[i] === '{') { braceStart = i; break; }
    if (!/\s/.test(s[i])) break; // anything other than whitespace before '{' = malformed
  }
  if (braceStart === -1) return null;

  let depth = 0;
  let inString = false;
  let escape = false;
  for (let i = braceStart; i < s.length; i++) {
    const ch = s[i];
    if (inString) {
      if (escape) escape = false;
      else if (ch === '\\') escape = true;
      else if (ch === '"') inString = false;
    } else if (ch === '"') {
      inString = true;
    } else if (ch === '{') {
      depth++;
    } else if (ch === '}') {
      depth--;
      if (depth === 0) return s.slice(braceStart, i + 1);
    }
  }
  return null; // unbalanced braces
}

// Parse the FIRST sessions_spawn(...) call into its object, or null if none /
// invalid. renderSessionsSpawnCall emits strict JSON.stringify output, so a
// plain JSON.parse is correct and sufficient — no unquoted-key fixup needed.
function parseFirstSpawnCall(text) {
  const raw = extractFirstSpawnPayload(text);
  if (raw === null) return null;
  try {
    const obj = JSON.parse(raw);
    return obj && typeof obj === 'object' ? obj : null;
  } catch (_) {
    return null;
  }
}

module.exports = {
  clip,
  writePromptArtifact,
  renderSessionsSpawnCall,
  extractFirstSpawnPayload,
  parseFirstSpawnCall,
};

