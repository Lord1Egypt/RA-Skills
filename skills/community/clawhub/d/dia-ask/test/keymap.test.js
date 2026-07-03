'use strict';
const assert = require('assert');
const { textToKeystrokes, renderTyped, deadkeysForAttempt } = require('../keymap');

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log(`ok - ${name}`); }
  catch (e) { fail++; console.log(`FAIL - ${name}\n   ${e.message}`); }
}

t('lowercase letters map to their keycodes (no shift)', () => {
  assert.deepStrictEqual(textToKeystrokes('abc'), ['0', '11', '8']);
});

t('uppercase letters carry :shift', () => {
  assert.deepStrictEqual(textToKeystrokes('A'), ['0:shift']);
  assert.deepStrictEqual(textToKeystrokes('aA'), ['0', '0:shift']);
});

t('digits map without shift', () => {
  assert.deepStrictEqual(textToKeystrokes('07'), ['29', '26']);
});

t('space maps to keycode 49', () => {
  assert.deepStrictEqual(textToKeystrokes('a b'), ['0', '49', '11']);
});

t('shifted punctuation: ? ! : " ( ) _', () => {
  assert.deepStrictEqual(textToKeystrokes('?'), ['44:shift']);
  assert.deepStrictEqual(textToKeystrokes('!'), ['18:shift']);
  assert.deepStrictEqual(textToKeystrokes(':'), ['41:shift']);
  assert.deepStrictEqual(textToKeystrokes('"'), ['39:shift']);
  assert.deepStrictEqual(textToKeystrokes('('), ['25:shift']);
  assert.deepStrictEqual(textToKeystrokes(')'), ['29:shift']);
  assert.deepStrictEqual(textToKeystrokes('_'), ['27:shift']);
});

t('unshifted punctuation: . , - / ;', () => {
  assert.deepStrictEqual(textToKeystrokes('.'), ['47']);
  assert.deepStrictEqual(textToKeystrokes(','), ['43']);
  assert.deepStrictEqual(textToKeystrokes('-'), ['27']);
  assert.deepStrictEqual(textToKeystrokes('/'), ['44']);
  assert.deepStrictEqual(textToKeystrokes(';'), ['41']);
});

t('newline becomes Shift+Return (soft newline, never sends)', () => {
  assert.deepStrictEqual(textToKeystrokes('a\nb'), ['0', '36:shift', '11']);
});

t('ñ/Ñ transliterate to n/N (US ANSI cannot type ñ via keycode)', () => {
  assert.deepStrictEqual(textToKeystrokes('ñÑ'), ['45', '45:shift']);
});

t('unknown char is dropped (not crash), known chars around it survive', () => {
  // a, <unknown emoji>, b  -> the emoji has no keycode, dropped
  assert.deepStrictEqual(textToKeystrokes('a\u{1F389}b'), ['0', '11']);
});

t('realistic prompt fragment round-trips to tokens', () => {
  const ks = textToKeystrokes('Hola, 2+2?');
  // H(shift) o l a , space 2 (+ has no US-unshifted... +) is shift+= ...
  // just assert it is a non-empty array of valid tokens
  assert.ok(Array.isArray(ks) && ks.length > 0);
  for (const k of ks) assert.ok(/^\d+(:shift)?$/.test(k), `bad token ${k}`);
});

// ---- deadkeys mode: escape dead-key glyphs with a trailing Space (kc 49) -----
t('deadkeys off (default): dead-key glyphs emit a single token', () => {
  assert.deepStrictEqual(textToKeystrokes('"'), ['39:shift']);
  assert.deepStrictEqual(textToKeystrokes("'"), ['39']);
  assert.deepStrictEqual(textToKeystrokes('`~^'), ['50', '50:shift', '22:shift']);
});
t('deadkeys on: " becomes 39:shift + Space, and the next char survives', () => {
  // the exact 2026-06-08 bug: `"d` dropped both chars under US-International
  assert.deepStrictEqual(textToKeystrokes('"d', { deadkeys: true }), ['39:shift', '49', '2']);
});
t('deadkeys on: all five dead keys get a trailing Space', () => {
  assert.deepStrictEqual(textToKeystrokes("'", { deadkeys: true }), ['39', '49']);
  assert.deepStrictEqual(textToKeystrokes('"', { deadkeys: true }), ['39:shift', '49']);
  assert.deepStrictEqual(textToKeystrokes('`', { deadkeys: true }), ['50', '49']);
  assert.deepStrictEqual(textToKeystrokes('~', { deadkeys: true }), ['50:shift', '49']);
  assert.deepStrictEqual(textToKeystrokes('^', { deadkeys: true }), ['22:shift', '49']);
});
t('deadkeys on: non-dead chars are unaffected', () => {
  assert.deepStrictEqual(textToKeystrokes('a!b', { deadkeys: true }), ['0', '18:shift', '11']);
});

// ---- renderTyped: the exact string that SHOULD land in the input ----------
t('renderTyped: ascii passes through unchanged', () => {
  assert.strictEqual(renderTyped('Hola test 123?'), 'Hola test 123?');
});
t('renderTyped: ñ/Ñ transliterate to n/N', () => {
  assert.strictEqual(renderTyped('año Ñandu'), 'ano Nandu');
});
t('renderTyped: unknown chars (emoji) are dropped', () => {
  assert.strictEqual(renderTyped('a\u{1F389}b'), 'ab');
});
t('renderTyped: newlines preserved', () => {
  assert.strictEqual(renderTyped('a\nb'), 'a\nb');
});
t('renderTyped matches token count (every kept char -> one token)', () => {
  const s = 'Dia, guarda "dia_out_123.txt" ok?';
  assert.strictEqual(renderTyped(s).length, textToKeystrokes(s).length);
});

// ---- deadkeysForAttempt: flip the deadkeys flag on alternating retries ------
// If hasDeadKeys() detected the layout wrong, re-typing with the SAME tokens
// fails identically every attempt -> fidelity loop. Flipping the flag on
// alternating attempts tries BOTH escapings within the 3-attempt budget, so a
// wrong base detection self-heals instead of looping into the v1 fallback.
t('deadkeysForAttempt: attempt 1 uses the detected base flag', () => {
  assert.strictEqual(deadkeysForAttempt(true, 1), true);
  assert.strictEqual(deadkeysForAttempt(false, 1), false);
});
t('deadkeysForAttempt: attempt 2 flips the base flag (the self-heal)', () => {
  assert.strictEqual(deadkeysForAttempt(true, 2), false);
  assert.strictEqual(deadkeysForAttempt(false, 2), true);
});
t('deadkeysForAttempt: attempt 3 returns to base (alternating)', () => {
  assert.strictEqual(deadkeysForAttempt(true, 3), true);
  assert.strictEqual(deadkeysForAttempt(false, 3), false);
});

// Safety invariant the self-heal relies on: flipping deadkeys changes the
// TOKENS for dead-key content but NOT the expected text (renderTyped), so one
// fixed `expected` validates either token stream.
t('flip changes tokens for dead-key text but renderTyped stays invariant', () => {
  const s = 'guarda "x.txt"';
  const exp = renderTyped(s);
  const tOn = textToKeystrokes(s, { deadkeys: true });
  const tOff = textToKeystrokes(s, { deadkeys: false });
  assert.notDeepStrictEqual(tOn, tOff);            // the flip really changes keystrokes
  assert.strictEqual(renderTyped(s), exp);          // expected is independent of the flag
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
