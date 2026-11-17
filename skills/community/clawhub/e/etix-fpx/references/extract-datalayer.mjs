#!/usr/bin/env node
// extract-datalayer.mjs — pull the page-level `dataLayer = [{ 'k' : 'v', ... }]`
// analytics object out of an Etix SSR page (event or venue detail) and print
// it as a flat JSON object on stdout (pipe to `jq`).
//
// Mirrors `extractDataLayer` in etix-mcp's own `src/parse.ts` verbatim — the
// block spans multiple lines in the real page (one `'key' : 'value'` pair
// per line), so a single-line `grep -oE` pass can never match it: grep's `.`
// doesn't match newlines and grep has no lazy quantifier, so `dataLayer\s*=
// \s*\[.*?\]` always comes back empty. Node's regex engine supports both
// (`[\s\S]*?` spans newlines lazily), so this is a plain `node -e`-sized
// port rather than a full parser dependency.
//
// Usage:
//   node extract-datalayer.mjs <html-file|->
//   fpx get 'https://www.etix.com/ticket/p/39004863' -p etix \
//     | node extract-datalayer.mjs - | jq '.org_id, .org_name, .cobrand'

import { readFileSync } from 'node:fs';

const [, , fileArg] = process.argv;
if (!fileArg) {
  console.error('usage: extract-datalayer.mjs <html-file|->');
  process.exit(1);
}

const html = fileArg === '-' ? readFileSync(0, 'utf8') : readFileSync(fileArg, 'utf8');

// Find the opener, then the first `}]` after it — two linear scans rather
// than one lazy `[\s\S]*?` regex, which re-ran to end-of-input for every
// opener on a page that never closes the block (fleet-audit#997).
function dataLayerBody(text) {
  const open = /dataLayer\s*=\s*\[\s*\{/.exec(text);
  if (!open) return undefined;
  const from = open.index + open[0].length;
  const close = /\}\s*\]/g;
  close.lastIndex = from;
  const end = close.exec(text);
  return end ? text.slice(from, end.index) : undefined;
}

const body = dataLayerBody(html);
if (body === undefined) {
  console.error('extract-datalayer: no "dataLayer = [{...}]" block found in the page');
  process.exit(1);
}

// Entity decoding mirrors `decodeHtmlEntities` from
// `@chrischall/mcp-utils/scrape` (what the server calls): numeric entities
// with an out-of-range guard, then the named set, then `&amp;` LAST so a
// double-escaped entity survives exactly one level. Unknown entities pass
// through. tests/extract-datalayer-skill.test.ts pins this to the server.
const NAMED = { nbsp: ' ', lt: '<', gt: '>', quot: '"', apos: "'" };
function codePointOr(code, raw) {
  if (!Number.isInteger(code) || code < 0 || code > 0x10ffff) return raw;
  try { return String.fromCodePoint(code); } catch { return raw; }
}
function decodeHtmlEntities(text) {
  return text
    .replace(/&#(\d+);/g, (whole, d) => codePointOr(Number(d), whole))
    .replace(/&#x([0-9a-fA-F]+);/g, (whole, h) => codePointOr(parseInt(h, 16), whole))
    .replace(/&(nbsp|lt|gt|quot|apos);/gi, (whole, name) => NAMED[name.toLowerCase()] ?? whole)
    .replace(/&amp;/gi, '&');
}

// Undo JS single-quoted-string escapes (`\'`, `\\`, `\xNN`, `\uNNNN`), then
// HTML entities (`&#39;`, `&amp;`) — a name like "Bojangles' Coliseum" may
// arrive in either form.
function unescapeValue(raw) {
  const js = raw.replace(/\\(?:x([0-9a-fA-F]{2})|u([0-9a-fA-F]{4})|([\s\S]))/g, (_, hex, uni, ch) => {
    if (hex) return String.fromCharCode(parseInt(hex, 16));
    if (uni) return String.fromCharCode(parseInt(uni, 16));
    return { n: '\n', r: '\r', t: '\t' }[ch] ?? ch;
  });
  return decodeHtmlEntities(js);
}

// A value may contain escaped quotes ('Bojangles\' Coliseum'), so consume
// `\.` escape pairs instead of stopping at the first `'`.
const out = {};
for (const m of body.matchAll(/'([\w]+)'\s*:\s*'((?:[^'\\]|\\[\s\S])*)'/g)) {
  out[m[1]] = unescapeValue(m[2]);
}

console.log(JSON.stringify(out));
