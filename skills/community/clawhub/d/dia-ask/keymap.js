'use strict';
// US-ANSI char -> keycode map for posting real keycodes to Dia's PID.
//
// Why keycodes (not clipboard paste, not CGEventKeyboardSetUnicodeString):
//   - Dia's React/web chat input ignores the unicode string carried by a posted
//     event (validated 2026-06-08) and does NOT receive Cmd+V "paste" commands
//     posted to the app PID when Dia isn't frontmost. But it DOES receive plain
//     character keycodes in every window state. So keycodes are the only
//     focus-safe mechanism that works regardless of window state.
//
// The prompt is deaccented upstream (buildPrompt) so accented vowels never reach
// here. ñ/Ñ have no US-ANSI keycode -> transliterated to n/N (logged by caller).
// Characters with no mapping (emoji, CJK, etc.) are dropped. This is a deliberate
// trade: v2 prioritizes zero-focus-theft for the common ASCII case; exotic-unicode
// prompts should use v1 (clipboard) instead.

// base: char -> keycode (unshifted)
const BASE = {
  a: 0, b: 11, c: 8, d: 2, e: 14, f: 3, g: 5, h: 4, i: 34, j: 38, k: 40, l: 37, m: 46,
  n: 45, o: 31, p: 35, q: 12, r: 15, s: 1, t: 17, u: 32, v: 9, w: 13, x: 7, y: 16, z: 6,
  '0': 29, '1': 18, '2': 19, '3': 20, '4': 21, '5': 23, '6': 22, '7': 26, '8': 28, '9': 25,
  ' ': 49, '\t': 48,
  '.': 47, ',': 43, '-': 27, '/': 44, ';': 41, "'": 39, '=': 24,
  '[': 33, ']': 30, '\\': 42, '`': 50,
};

// shifted: char -> the keycode that with Shift produces it
const SHIFTED = {
  '!': 18, '@': 19, '#': 20, '$': 21, '%': 23, '^': 22, '&': 26, '*': 28, '(': 25, ')': 29,
  '_': 27, '+': 24, ':': 41, '"': 39, '?': 44, '<': 43, '>': 47, '{': 33, '}': 30, '|': 42,
  '~': 50,
};

// Dead keys on U.S.-International (and similar) layouts: these glyphs start an
// accent composition instead of inserting immediately, so a posted keycode for
// one of them swallows itself AND the next character (validated 2026-06-08:
// `"` + `d` -> both dropped). When `deadkeys` mode is on we follow each with a
// Space (keycode 49); on these layouts "dead key + Space" emits the bare glyph
// and the Space is consumed by the composition (so nothing extra is inserted).
// On a plain ANSI layout these are NOT dead keys, so the default is OFF (callers
// enable it only after detecting a dead-key layout) — otherwise the trailing
// Space would be a literal space. renderTyped is unchanged: the visible result
// is still the single glyph, so fidelity checks keep matching.
const DEAD = new Set(["'", '"', '`', '~', '^']);

// Returns an array of dia-cgpost tokens: "<kc>" or "<kc>:shift".
// Newline -> Shift+Return (keycode 36) so it inserts a soft newline and never
// submits the message mid-typing. `opts.deadkeys` escapes dead-key glyphs with a
// trailing Space (see DEAD above).
function textToKeystrokes(text, opts = {}) {
  const esc = !!opts.deadkeys;
  const out = [];
  const push = (token, ch) => { out.push(token); if (esc && DEAD.has(ch)) out.push('49'); };
  for (const ch of String(text)) {
    if (ch === '\n' || ch === '\r') { out.push('36:shift'); continue; }
    if (ch === 'ñ') { out.push('45'); continue; }
    if (ch === 'Ñ') { out.push('45:shift'); continue; }
    const lower = ch.toLowerCase();
    if (ch >= 'A' && ch <= 'Z') { out.push(`${BASE[lower]}:shift`); continue; }
    if (Object.prototype.hasOwnProperty.call(BASE, ch)) { push(String(BASE[ch]), ch); continue; }
    if (Object.prototype.hasOwnProperty.call(SHIFTED, ch)) { push(`${SHIFTED[ch]}:shift`, ch); continue; }
    // unknown char -> drop
  }
  return out;
}

// The exact string that SHOULD appear in the input after typing `text` with
// textToKeystrokes — used to verify fidelity (readback vs expected). Same
// transforms: ñ/Ñ -> n/N, unknown chars dropped, everything else (incl. newline)
// kept. Mirrors textToKeystrokes char-for-char (one kept char == one token).
function renderTyped(text) {
  let out = '';
  for (const ch of String(text)) {
    if (ch === '\n' || ch === '\r') { out += '\n'; continue; }
    if (ch === 'ñ') { out += 'n'; continue; }
    if (ch === 'Ñ') { out += 'N'; continue; }
    const lower = ch.toLowerCase();
    if (ch >= 'A' && ch <= 'Z') { out += ch; continue; }
    if (Object.prototype.hasOwnProperty.call(BASE, ch)) { out += ch; continue; }
    if (Object.prototype.hasOwnProperty.call(SHIFTED, ch)) { out += ch; continue; }
    // unknown -> dropped
  }
  return out;
}

// Which deadkeys flag to use on a given 1-based fidelity attempt. hasDeadKeys()
// reads a cached plist and can be wrong; re-typing with the same tokens then
// fails identically every attempt -> a type-delete-retype loop. Alternating the
// flag (base, !base, base, ...) tries both escapings within the retry budget so
// a wrong base detection self-heals. renderTyped (the expected text) is
// invariant to the flag, so the same fidelity check validates either stream.
function deadkeysForAttempt(base, attempt) {
  return attempt % 2 === 1 ? !!base : !base;
}

module.exports = { textToKeystrokes, renderTyped, deadkeysForAttempt, BASE, SHIFTED };
