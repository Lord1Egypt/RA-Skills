#!/usr/bin/env node
'use strict';
// dia-ask-v2.js — focus-safe delegation to Dia's AI assistant.
//
//   node dia-ask-v2.js "<prompt>" [--format md|txt|json|csv] [--timeout 300]
//                      [--no-fallback] [--debug]
//
// Same I/O contract as v1 (dia-ask.js): prints the absolute path of the file Dia
// saved its answer to. Drop-in replacement.
//
// What changed vs v1: the SEND no longer steals focus and can't be corrupted by
// the user typing. v1 activates Dia and injects keystrokes into the global
// keyboard stream (frontmost app), so it (a) grabs focus ~15s and (b) breaks if
// the user types mid-send. v2 injects into an EXISTING Dia window via:
//   - clipboard set with arbitrary unicode (NSPasteboard, locale-independent),
//   - AX focus of the unified-bar text area (no app activation),
//   - keycodes posted to Dia's PID with CGEventPostToPid: Cmd+A, Delete, Cmd+V,
//     then Down (select the "Chat" row of the unified bar) + Enter (send).
// Events go to Dia's process, not the frontmost app -> zero focus theft, and the
// user's own typing (to their app) never collides with the send.
//
// Mechanism validated end-to-end 2026-06-08 (Finder frontmost the whole time;
// Dia received, routed to chat, and answered). See docs/dia-ask-v2-design.md.
//
// If the AX path fails (no Dia window, no text area, focus won't take), v2 falls
// back to v1's proven send unless --no-fallback is given.

const { execFileSync, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { buildPrompt, parseArgs, findOutput, DEFAULT_CONTEXTS } = require('./v2-lib');
const { textToKeystrokes, renderTyped, deadkeysForAttempt } = require('./keymap');

const HERE = __dirname;
const log = (m) => process.stderr.write(`[dia-ask-v2] ${m}\n`);
const sleep = (ms) => execSync(`/bin/sleep ${(ms / 1000).toFixed(2)}`);

function osa(script, t = 20) {
  return execFileSync('/usr/bin/osascript',
    ['-e', `with timeout of ${t} seconds`, '-e', script, '-e', 'end timeout'],
    { encoding: 'utf8' }).trim();
}
function jxaFile(file, args, t = 20) {
  return execFileSync('/usr/bin/osascript', ['-l', 'JavaScript', path.join(HERE, file), ...args.map(String)],
    { encoding: 'utf8', timeout: t * 1000 }).trim();
}

function diaPid() {
  try { const out = execSync('/usr/bin/pgrep -x Dia', { encoding: 'utf8' }).trim(); return out ? parseInt(out.split('\n')[0], 10) : null; }
  catch { return null; }
}

// Is the active keyboard layout one where '"`~^ are dead keys? Posted keycodes
// are interpreted under the active layout, so on US-International a `"` starts an
// accent composition that swallows itself + the next char. Detect it so keymap
// can escape those glyphs. Override with DIA_DEADKEYS=1/0.
function hasDeadKeys() {
  if (process.env.DIA_DEADKEYS === '1') return true;
  if (process.env.DIA_DEADKEYS === '0') return false;
  try {
    const out = execSync('/usr/bin/defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources 2>/dev/null', { encoding: 'utf8' });
    const m = out.match(/"KeyboardLayout Name"\s*=\s*"?([^";]+)"?/);
    return /international/i.test(m ? m[1] : '');
  } catch { return false; }
}


// Enable AX, focus Dia's chat/unified-bar input (the only settable AXTextArea)
// without activating Dia, and report whether an active chat thread exists.
// Returns { focused: bool, raw: string, bubbles: number }.
//   bubbles = count of non-empty read-only AXTextAreas (conversation messages).
//   >= 2 means we're inside a live chat thread (so Enter submits); < 2 means a
//   fresh unified bar (so we route via Down -> "Chat" row -> Enter). A single
//   non-empty read-only area (the "Use other apps?" notice) does not count.
function focusAndState() {
  const r = osa(`
    tell application "System Events" to tell process "Dia"
      try
        set value of attribute "AXManualAccessibility" to true
      end try
      delay 0.25
      if (count of windows) is 0 then return "NOWINDOW"
      set tas to {}
      set els to entire contents of window 1
      repeat with e in els
        try
          if (role of e) is "AXTextArea" then set end of tas to e
        end try
      end repeat
      if (count of tas) is 0 then return "NOTEXTAREA"
      set theInput to missing value
      set bubbles to 0
      repeat with e in tas
        try
          if (settable of attribute "AXValue" of e) then
            set theInput to e
          else
            if (length of ((value of e) as text)) > 0 then set bubbles to bubbles + 1
          end if
        end try
      end repeat
      if theInput is missing value then return "NOINPUT"
      try
        set value of attribute "AXFocused" of theInput to true
      end try
      delay 0.2
      set ok to false
      try
        set ok to (value of attribute "AXFocused" of theInput) as boolean
      end try
      if not ok then
        try
          perform action "AXPress" of theInput
          delay 0.2
          set ok to (value of attribute "AXFocused" of theInput) as boolean
        end try
      end if
      return "FOCUS=" & ok & " BUBBLES=" & bubbles
    end tell`);
  const focused = /FOCUS=true/.test(r);
  const m = r.match(/BUBBLES=(\d+)/);
  return { focused, raw: r, bubbles: m ? parseInt(m[1], 10) : 0 };
}

// Post keycode tokens to Dia's PID in one osascript spawn (no batch boundaries,
// which caused single-key drops). dia-cgpost paces each key itself.
function postKeys(pid, tokens) {
  if (!tokens.length) return;
  jxaFile('dia-cgpost.js', [pid, ...tokens], 120);
}

// Read the current value of Dia's settable chat input (for fidelity checks).
function readInput() {
  return osa(`
    tell application "System Events" to tell process "Dia"
      set els to entire contents of window 1
      repeat with e in els
        try
          if (role of e) is "AXTextArea" then
            if (settable of attribute "AXValue" of e) then return (value of e as text)
          end if
        end try
      end repeat
      return ""
    end tell`);
}

const norm = (s) => String(s).replace(/\s+/g, ' ').trim();

// Clear the input with backspaces sized to its current length (Cmd+A is not
// honored by Dia's web input). Normally the input is empty, so this is a few
// no-ops; it also recovers from residue left by a previous failed attempt.
function clearInput(pid) {
  const len = readInput().length;
  postKeys(pid, new Array(len + 12).fill('51'));
}

// The focus-safe send: type the prompt as real keycodes into Dia's input and
// submit. No clipboard, no app activation, no Cmd-chords (Dia's web input ignores
// posted Cmd+V / Cmd+A) -> works in any window state and never steals focus.
// Throws on any failure so main() can fall back to v1.
function sendV2(pid, fullPrompt, debug) {
  const st = focusAndState();
  if (debug) log(`focusAndState -> ${st.raw}`);
  if (!st.focused) throw new Error(`AX focus failed (${st.raw})`);

  const baseDeadkeys = hasDeadKeys();
  // expected is invariant to the deadkeys flag (renderTyped ignores it), so it's
  // computed once and validates whichever escaping a given attempt uses.
  const expected = norm(renderTyped(fullPrompt));
  if (debug) log(`bubbles=${st.bubbles}, baseDeadkeys=${baseDeadkeys}, route=${st.bubbles >= 2 ? 'chat/Enter' : 'unifiedbar/Down+Enter'}`);

  // Type, then verify the input matches char-for-char; retry on any drop. A
  // corrupted prompt (dropped keys) would run the wrong task, so we never submit
  // unverified text. hasDeadKeys() reads a cached plist and can be wrong, which
  // would make every same-token retry fail identically (a type-delete-retype
  // loop); so alternate the deadkeys flag per attempt to self-heal that case.
  let ok = false;
  for (let attempt = 1; attempt <= 3 && !ok; attempt++) {
    const deadkeys = deadkeysForAttempt(baseDeadkeys, attempt);
    const tokens = textToKeystrokes(fullPrompt, { deadkeys });
    if (debug) log(`attempt ${attempt}: typing ${tokens.length} keycodes (deadkeys=${deadkeys})`);
    clearInput(pid);
    sleep(120);
    postKeys(pid, tokens);
    sleep(300);
    const got = norm(readInput());
    if (got === expected) { ok = true; break; }
    if (debug) {
      let i = 0; while (i < got.length && i < expected.length && got[i] === expected[i]) i++;
      log(`fidelity mismatch attempt ${attempt}: expLen=${expected.length} gotLen=${got.length} firstDiff@${i}`);
      log(`  exp@${i}: ${JSON.stringify(expected.slice(Math.max(0, i - 12), i + 12))}`);
      log(`  got@${i}: ${JSON.stringify(got.slice(Math.max(0, i - 12), i + 12))}`);
    }
  }
  if (!ok) throw new Error('input fidelity check failed after 3 attempts');

  if (st.bubbles >= 2) {
    jxaFile('dia-cgpost.js', [pid, '36']);                  // active chat -> Enter submits
  } else {
    jxaFile('dia-cgpost.js', [pid, '125']);                 // unified bar: Down -> "Chat" row
    sleep(300);
    jxaFile('dia-cgpost.js', [pid, '36']);                  // Enter -> send to chat
  }
}

function fallbackToV1(args) {
  log('falling back to v1 (dia-ask.js)...');
  const v1Args = [args.prompt, '--format', args.format, '--timeout', String(args.timeout)];
  if (args.debug) v1Args.push('--debug');
  const out = execFileSync('node', [path.join(HERE, 'dia-ask.js'), ...v1Args],
    { encoding: 'utf8', stdio: ['ignore', 'pipe', 'inherit'] }).trim();
  return out.split('\n').filter(Boolean).pop();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.prompt) { log('usage: dia-ask-v2.js "<prompt>" [--format md|txt|json|csv] [--timeout N] [--no-fallback] [--debug]'); process.exit(2); }

  const { fname, ext, fullPrompt } = buildPrompt(args.prompt, args.format, Date.now());
  const startMs = Date.now() - 2000;
  const pid = diaPid();

  if (!pid) {
    if (args.noFallback) { log('ERROR: Dia not running and --no-fallback set'); process.exit(1); }
    log('Dia not running — using v1 (it will open a window).');
    process.stdout.write(fallbackToV1(args) + '\n');
    return;
  }

  const ctxSet = () => { try { return new Set(fs.readdirSync(DEFAULT_CONTEXTS)); } catch { return new Set(); } };
  try {
    log(`sending (focus-safe) to Dia pid ${pid} (out=${fname}, fmt=${ext})...`);
    const before = ctxSet();
    sendV2(pid, fullPrompt, args.debug);

    // Confirm the chat actually started: a new AgentServer context dir appears,
    // or the output file shows up. If neither after ~36s, retry the send once.
    const newCtxNames = () => [...ctxSet()].filter((c) => !before.has(c));
    const newCtx = () => newCtxNames().length > 0;
    const waitStarted = (tries) => { for (let i = 0; i < tries; i++) { sleep(3000); if (newCtx() || findOutput(fname, startMs)) return true; } return false; };
    let started = waitStarted(12);
    if (args.debug) log(`chat started: ${started}`);
    if (!started) {
      log('chat did not start — re-sending once...');
      sendV2(pid, fullPrompt, args.debug);
      started = waitStarted(12);
      if (args.debug) log(`chat started (retry): ${started}`);
    }
    if (!started) throw new Error('chat never started via AX path');

    log('waiting for output file...');
    const deadline = Date.now() + args.timeout * 1000;
    let found = null;
    while (Date.now() < deadline) {
      // Scan only the new conversation's context(s) — a shallow readdir to find
      // them, then a recursive walk of just those (not every accumulated chat).
      // Falls back to a full scan if none were detected (e.g. file already found
      // during the started-check before a ctx dir was observed).
      const only = newCtxNames();
      const f = findOutput(fname, startMs, DEFAULT_CONTEXTS, only.length ? only : null);
      if (f) {
        const s1 = fs.statSync(f).size; sleep(4000);
        let s2 = 0; try { s2 = fs.statSync(f).size; } catch {}
        if (s1 > 0 && s1 === s2) { found = f; break; }
        if (args.debug) log(`file growing: ${s1} -> ${s2}`);
      } else sleep(4000);
    }
    if (!found) throw new Error(`No output file after ${args.timeout}s`);
    log(`done: ${fs.statSync(found).size} bytes`);
    process.stdout.write(found + '\n');
  } catch (e) {
    log(`v2 path failed: ${e.message}`);
    if (args.noFallback) process.exit(1);
    const p = fallbackToV1(args);
    process.stdout.write(p + '\n');
  }
}

main().catch((e) => { log(`ERROR: ${e.message}`); process.exit(1); });
