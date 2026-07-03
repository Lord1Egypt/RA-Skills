'use strict';
// Pure, testable logic shared by dia-ask-v2. No side effects beyond reading the
// filesystem (findOutput). The injection (AX + CGEvent) lives in dia-send.js;
// the orchestration in dia-ask-v2.js. Splitting the pure bits out keeps them
// under TDD even though the UI/AX path can only be validated E2E.

const fs = require('fs');
const os = require('os');
const path = require('path');

const FMT = { md: 'Markdown', txt: 'plain text', json: 'JSON', csv: 'CSV (comma-separated)' };

const DEFAULT_CONTEXTS = path.join(
  os.homedir(),
  'Library/Application Support/Dia/User Data/Default/AgentServer/contexts'
);

// Strip Spanish accents (keeping ñ): when the caller runs under a shell without a
// UTF-8 locale, accented bytes can get mangled (á -> "√°") as the prompt travels
// through argv/exec. The v2 injector types unicode directly and would not need
// this, but the guard is cheap and keeps shell-built prompts bulletproof. It is a
// no-op on plain ASCII / English prompts.
function deaccent(s) {
  const m = { 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U' };
  return String(s).replace(/[áéíóúüÁÉÍÓÚÜ]/g, (c) => m[c]);
}

// Build the conversational prompt that asks Dia's assistant to save its answer
// to an exactly-named file. Returns { fname, ext, fullPrompt }. `now` is the
// timestamp seed for the filename (injectable for tests).
function buildPrompt(prompt, format, now) {
  const ext = format in FMT ? format : 'md';
  const stamp = now == null ? Date.now() : now;
  const fname = `dia_out_${stamp}.${ext}`;
  const fullPrompt = deaccent(
    `Dia, ${prompt}\n\nSave your complete answer in ${FMT[ext]} format to a file named exactly ${fname} in my working directory, ready to read. The file must contain only the requested content.`
  );
  return { fname, ext, fullPrompt };
}

function parseArgs(argv) {
  const a = { format: 'md', timeout: 300, debug: false, noFallback: false, prompt: '' };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--format') a.format = String(argv[++i]).toLowerCase();
    else if (argv[i] === '--timeout') a.timeout = Number(argv[++i]);
    else if (argv[i] === '--debug') a.debug = true;
    else if (argv[i] === '--no-fallback') a.noFallback = true;
    else rest.push(argv[i]);
  }
  a.prompt = rest.join(' ').trim();
  return a;
}

// Recursively list files under a directory (work dirs are shallow).
function walk(d, out = []) {
  let ents = [];
  try { ents = fs.readdirSync(d, { withFileTypes: true }); } catch { return out; }
  for (const e of ents) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

// Find the output file in AgentServer context work dirs: exact name preferred,
// else newest non-artifact file modified since `sinceMs`. `contextsDir` is
// injectable for tests (defaults to Dia's real location). `onlyCtxs`, when given,
// restricts the scan to those context subdirs (the new conversation's context):
// faster — avoids walking every accumulated conversation — and more correct, since
// the answer lands in the new conversation's own work dir, so old contexts can
// only yield false matches.
function findOutput(name, sinceMs, contextsDir = DEFAULT_CONTEXTS, onlyCtxs = null) {
  let best = null, bestM = 0;
  let ctxs = [];
  try { ctxs = fs.readdirSync(contextsDir); } catch { return null; }
  if (onlyCtxs && onlyCtxs.length) ctxs = ctxs.filter((c) => onlyCtxs.includes(c));
  for (const ctx of ctxs) {
    const wd = path.join(contextsDir, ctx, 'work');
    for (const f of walk(wd)) {
      let st; try { st = fs.statSync(f); } catch { continue; }
      if (st.mtimeMs < sinceMs) continue;
      if (path.basename(f) === name) return f;
      if (!f.includes('/artifacts/') && st.mtimeMs > bestM) { bestM = st.mtimeMs; best = f; }
    }
  }
  return best;
}

module.exports = { FMT, DEFAULT_CONTEXTS, deaccent, buildPrompt, parseArgs, walk, findOutput };
