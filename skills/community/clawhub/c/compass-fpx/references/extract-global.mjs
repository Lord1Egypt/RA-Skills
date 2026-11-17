#!/usr/bin/env node
// extract-global.mjs — pull a `global.NAME = {...};` / `window.NAME = {...};`
// / bare `NAME = {...};` JSON-literal global out of a Compass SSR HTML page
// and print the object as JSON on stdout (pipe to `jq`).
//
// Mirrors the balanced-brace walk compass-mcp's own src/page-state.ts uses
// (extractGlobalAssign, from @chrischall/mcp-utils/fetchproxy) — self-
// contained here so this skill has no npm dependency beyond @fetchproxy/cli.
// Compass writes each global as a valid JSON literal (quoted keys/strings),
// so once the matching `{...}` is sliced out, JSON.parse / jq works as-is.
//
// Usage:
//   node extract-global.mjs <html-file|-> <globalName>
//   fpx get 'https://www.compass.com/homes-for-sale/manhattan-ny/' -p compass \
//     | node extract-global.mjs - uc | jq '.sharedReactAppProps.initialResults.lolResults.total'
//
// Known globals (see references/requests.md):
//   uc                 — search-results pages
//   __INITIAL_DATA__   — homedetails pages
//   __AGENT_PROFILE__  — agent profile pages

import { readFileSync } from 'node:fs';

const [, , fileArg, name] = process.argv;
if (!fileArg || !name) {
  console.error('usage: extract-global.mjs <html-file|-> <globalName>');
  process.exit(1);
}

const html = fileArg === '-' ? readFileSync(0, 'utf8') : readFileSync(fileArg, 'utf8');

// Anchor on `global.NAME =`, `window.NAME =`, or a bare `NAME =`, guarding
// the left edge so a search for "uc" doesn't match inside "myuc".
const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const re = new RegExp(`(?:^|[^\\w.])(?:global\\.|window\\.)?${escaped}\\s*=\\s*\\{`);
const m = re.exec(html);
if (!m) {
  console.error(`extract-global: no "${name} = {" assignment found in the page`);
  process.exit(1);
}

const start = html.indexOf('{', m.index);
let depth = 0;
let inStr = null; // active quote char while walking a string literal
let escapedChar = false;
let end = -1;

for (let i = start; i < html.length; i++) {
  const c = html[i];
  if (inStr) {
    if (escapedChar) escapedChar = false;
    else if (c === '\\') escapedChar = true;
    else if (c === inStr) inStr = null;
    continue;
  }
  if (c === '"' || c === "'") {
    inStr = c;
    continue;
  }
  if (c === '{') depth++;
  else if (c === '}') {
    depth--;
    if (depth === 0) {
      end = i + 1;
      break;
    }
  }
}

if (end === -1) {
  console.error('extract-global: unbalanced braces — could not find the end of the object');
  process.exit(1);
}

const jsonText = html.slice(start, end);
try {
  // Round-trip through JSON.parse/stringify so malformed input fails loudly
  // here rather than silently downstream in jq.
  console.log(JSON.stringify(JSON.parse(jsonText)));
} catch (e) {
  console.error(`extract-global: sliced text was not valid JSON — ${e.message}`);
  process.exit(1);
}
