#!/usr/bin/env node
'use strict';
// dia-ask.js — baseline sender (also the fallback used by dia-ask-v2.js). Delegates a
// task to Dia's AI assistant and reads its answer as an exact text FILE (no OCR of the
// payload, no scroll limits). This path opens a fresh Dia window and briefly takes focus;
// prefer dia-ask-v2.js when a Dia window is already open and you don't want focus stolen.
//
//   node dia-ask.js "<prompt>" [--format md|txt|json|csv] [--timeout 300] [--debug]
//
// How it works:
//   1. open a fresh fullscreen Dia window and type a conversational prompt that asks
//      the assistant to SAVE its full answer to a uniquely-named file in its work dir;
//   2. confirm the chat started by watching for a new AgentServer context dir (a misfire,
//      e.g. focus stolen, leaves none) and re-send once if needed — no OCR involved;
//   3. poll Dia's AgentServer work dirs until that file appears and stops growing;
//   4. print the file's absolute path to stdout (read it with your file tools).
//
// Why files: Dia's assistant is an agent that can write to disk. Reading the file gives
// exact text — formulas, code, any length — which screen OCR never could.

const { execFileSync, execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const CONTEXTS = path.join(os.homedir(), 'Library/Application Support/Dia/User Data/Default/AgentServer/contexts');

const FMT = { md: 'Markdown', txt: 'plain text', json: 'JSON', csv: 'CSV (comma-separated)' };

function parseArgs(argv) {
  const a = { format: 'md', timeout: 300, debug: false, prompt: '' };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--format') a.format = String(argv[++i]).toLowerCase();
    else if (argv[i] === '--timeout') a.timeout = Number(argv[++i]);
    else if (argv[i] === '--debug') a.debug = true;
    else rest.push(argv[i]);
  }
  a.prompt = rest.join(' ').trim();
  return a;
}

const log = (m) => process.stderr.write(`[dia-ask] ${m}\n`);
const sleep = (ms) => execSync(`/bin/sleep ${(ms / 1000).toFixed(2)}`);
function osa(s, t = 20) { return execFileSync('/usr/bin/osascript', ['-e', `with timeout of ${t} seconds`, '-e', s, '-e', 'end timeout'], { encoding: 'utf8' }).trim(); }
function keystroke(ch, mods) { const u = mods ? ` using {${mods.map(m => m + ' down').join(', ')}}` : ''; osa(`tell application "System Events" to keystroke "${ch}"${u}`); }
function pressReturn() { osa(`tell application "System Events" to key code 36`); }
function getClipboard() { try { return execSync('/usr/bin/pbpaste', { encoding: 'utf8', env: { ...process.env, LC_CTYPE: 'UTF-8' } }); } catch { return null; } }
function setClipboard(t) { try { execSync('/usr/bin/pbcopy', { input: t, env: { ...process.env, LC_CTYPE: 'UTF-8' } }); } catch {} }
// Strip Spanish accents (keeping ñ): under a shell without a UTF-8 locale, accented
// bytes can get mangled (á -> "√°") through argv/exec. No-op on plain ASCII/English.
function deaccent(s) { const m = { 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U' }; return String(s).replace(/[áéíóúüÁÉÍÓÚÜ]/g, (c) => m[c]); }

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

// Find the output file: exact name preferred, else newest non-artifact file since `sinceMs`.
function findOutput(name, sinceMs) {
  let best = null, bestM = 0;
  let ctxs = [];
  try { ctxs = fs.readdirSync(CONTEXTS); } catch { return null; }
  for (const ctx of ctxs) {
    const wd = path.join(CONTEXTS, ctx, 'work');
    for (const f of walk(wd)) {
      let st; try { st = fs.statSync(f); } catch { continue; }
      if (st.mtimeMs < sinceMs) continue;
      if (path.basename(f) === name) return f;
      if (!f.includes('/artifacts/') && st.mtimeMs > bestM) { bestM = st.mtimeMs; best = f; }
    }
  }
  return best;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.prompt) { log('usage: dia-ask.js "<prompt>" [--format md|txt|json|csv] [--timeout N] [--debug]'); process.exit(2); }
  const ext = args.format in FMT ? args.format : 'md';
  const fname = `dia_out_${Date.now()}.${ext}`;
  const fullPrompt = deaccent(`Dia, ${args.prompt}\n\nSave your complete answer in ${FMT[ext]} format to a file named exactly ${fname} in my working directory, ready to read. The file must contain only the requested content.`);

  const saved = getClipboard();
  const startMs = Date.now() - 2000;

  const send = () => {
    setClipboard(fullPrompt);
    osa(`tell application "Dia" to activate`); sleep(900);
    keystroke('n', ['command']); sleep(1600);                                // new window (blank, frontmost)
    try { osa(`tell application "System Events" to tell process "Dia" to click menu item "Enter Full Screen" of menu 1 of (menu bar item "View" of menu bar 1)`); } catch {}
    sleep(2500);
    keystroke('v', ['command']); sleep(700);                                 // paste into unified bar
    pressReturn();                                                           // conversational -> chat mode
  };

  try {
    log(`sending prompt (out=${fname}, fmt=${ext})...`);
    send();

    // Detect that the chat actually started via a NEW AgentServer context dir (file-based,
    // reliable). Each conversation gets its own contexts/<UUID>/. If none appears, the
    // prompt likely misfired (focus stolen / went to the address bar) -> re-send once.
    const ctxSet = () => { try { return new Set(fs.readdirSync(CONTEXTS)); } catch { return new Set(); } };
    const before = ctxSet();
    const newCtx = () => [...ctxSet()].some((c) => !before.has(c));
    const waitStarted = (tries) => { for (let i = 0; i < tries; i++) { sleep(3000); if (newCtx() || findOutput(fname, startMs)) return true; } return false; };
    let started = waitStarted(12);                                           // ~36s for the agent to spin up its context
    if (args.debug) log(`chat started: ${started}`);
    if (!started) { log('chat did not start — re-sending once...'); send(); started = waitStarted(12); if (args.debug) log(`chat started (retry): ${started}`); }

    // poll for the output file (generation of long docs can take minutes).
    log('waiting for output file...');
    const deadline = Date.now() + args.timeout * 1000;
    let found = null;
    while (Date.now() < deadline) {
      const f = findOutput(fname, startMs);
      if (f) {
        const s1 = fs.statSync(f).size; sleep(4000);
        let s2 = 0; try { s2 = fs.statSync(f).size; } catch {}
        if (s1 > 0 && s1 === s2) { found = f; break; }
        if (args.debug) log(`file growing: ${s1} -> ${s2}`);
      } else sleep(4000);
    }

    if (!found) throw new Error(`No output file after ${args.timeout}s (chat may not have started, or generation too slow)`);
    const bytes = fs.statSync(found).size;
    log(`done: ${bytes} bytes`);
    process.stdout.write(found + '\n');                                      // stdout = absolute path
  } finally {
    if (saved !== null) setClipboard(saved);
  }
}

main().catch((e) => { log(`ERROR: ${e.message}`); process.exit(1); });
