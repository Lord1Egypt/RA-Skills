// Angi RSC flight extractor — dependency-free, no npm deps.
//
// Angi is a Next.js App Router site. A page's real data is not in JSON-LD and
// not in a __NEXT_DATA__ blob: it arrives as React Server Component "flight"
// rows, delivered as JS string literals inside `self.__next_f.push([1,"..."])`.
// Concatenating the unescaped literals yields newline-separated rows of the
// form `<hexid>:<json>`. Values are deduplicated across rows, so a field can
// hold the reference `"$b5"` instead of its value — resolve() follows those.
//
// This is a deliberate dependency-free copy of src/parse.ts (so the skill runs
// as `node rsc.mjs` with no install). tests/skill-rsc-parity.test.ts runs both
// on the same pages: change one, change the other, or CI fails.

/** Recover the concatenated flight text from a raw HTML document. */
export function flightText(html) {
  const re = /self\.__next_f\.push\(\[\d+\s*,\s*"((?:[^"\\]|\\.)*)"/g;
  let out = '';
  for (const m of html.matchAll(re)) {
    // A chunk that will not unescape is skipped rather than aborting the page.
    try { out += JSON.parse(`"${m[1]}"`); } catch { /* ignore */ }
  }
  return out;
}

const ROW_START = /(?:^|\n)([0-9a-f]+):/g;
/** `T<hexByteLength>,` marks a raw text chunk rather than a JSON row. */
const TEXT_CHUNK = /^T([0-9a-f]+),/;

/**
 * Map of rowId -> value, for every row that carries data.
 *
 * Two row encodings matter:
 *  - JSON rows (`3:{...}` / `b5:[...]`), read to end of line.
 *  - Text chunks (`b6:T476,I am just blown away...`) — a raw string of the
 *    given UTF-8 BYTE length, which RSC uses for long strings such as review
 *    bodies. Not JSON: read by length, not parsed. They may contain newlines,
 *    which is why this scans positionally rather than splitting on newline.
 *
 * Missing the text-chunk form leaves the referring field holding a literal
 * "$57" that reads like data — verified against a live profile page where 4 of
 * 50 review bodies arrived this way.
 */
export function flightRows(text) {
  const rows = new Map();
  for (const m of text.matchAll(ROW_START)) {
    const id = m[1];
    const rest = text.slice(m.index + m[0].length);

    const t = TEXT_CHUNK.exec(rest);
    if (t) {
      const byteLen = Number.parseInt(t[1], 16);
      const from = rest.slice(t[0].length);
      // UTF-8 is >= 1 byte per char, so byteLen chars always covers byteLen
      // bytes; encode that window and cut it to the exact byte length.
      const bytes = new TextEncoder().encode(from.slice(0, byteLen));
      rows.set(id, new TextDecoder().decode(bytes.slice(0, byteLen)));
      continue;
    }

    const nl = rest.indexOf('\n');
    const line = nl === -1 ? rest : rest.slice(0, nl);
    // Rows like `I[...]`/`HL[...]` are module/preload directives, not data.
    if (!/^[[{"]/.test(line)) continue;
    try { rows.set(id, JSON.parse(line)); } catch { /* ignore */ }
  }
  return rows;
}

/**
 * Replace `"$<rowid>"` references with the referenced value, recursively.
 * `"$undefined"` becomes undefined; `"$$x"` is an escaped literal `"$x"`.
 * Guards against reference cycles and runaway depth.
 */
export function resolve(value, rows, seen = new Set(), depth = 0) {
  if (depth > 24) return value;
  if (typeof value === 'string') {
    if (value === '$undefined') return undefined;
    if (value.startsWith('$$')) return value.slice(1);
    if (/^\$[0-9a-f]+$/.test(value)) {
      const id = value.slice(1);
      if (seen.has(id) || !rows.has(id)) return value; // cycle / unknown: keep the token
      return resolve(rows.get(id), rows, new Set([...seen, id]), depth + 1);
    }
    return value;
  }
  if (Array.isArray(value)) return value.map((v) => resolve(v, rows, seen, depth + 1));
  if (value && typeof value === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(value)) {
      const r = resolve(v, rows, seen, depth + 1);
      if (r !== undefined) out[k] = r;
    }
    return out;
  }
  return value;
}

/**
 * mcp-utils/scrape `matchBalanced`, inlined: the EXCLUSIVE end index of the
 * `{…}` / `[…]` value starting at `start`, or -1 when `start` is not an opener
 * or the structure never closes (or closes with the wrong bracket). Aware of
 * both "…" and '…' strings.
 */
export function matchBalanced(text, start) {
  const opener = text[start];
  if (opener !== '{' && opener !== '[') return -1;
  const stack = [];
  let inString = null;
  let escape = false;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (inString) {
      if (escape) escape = false;
      else if (ch === '\\') escape = true;
      else if (ch === inString) inString = null;
      continue;
    }
    if (ch === '"' || ch === "'") inString = ch;
    else if (ch === '{' || ch === '[') stack.push(ch);
    else if (ch === '}' || ch === ']') {
      const open = stack.pop();
      if ((ch === '}' && open !== '{') || (ch === ']' && open !== '[')) return -1;
      if (stack.length === 0) return i + 1;
    }
  }
  return -1;
}

// Bounds mirrored from src/parse.ts (fleet-audit#1211): see objectsWithKey there.
const MAX_LOOKBACK = 200_000;
const MAX_CANDIDATES_PER_HIT = 64;
const SCAN_BUDGET_FACTOR = 64;
const MIN_SCAN_BUDGET = 1 << 20;

/**
 * Every JSON object in the flight text that owns `key` as a direct property,
 * with references resolved. From each hit, takes the nearest '{' before it
 * whose balanced span encloses the hit, parses, and owns the key. Undocumented
 * payloads drift, so a candidate that fails to parse is skipped rather than
 * thrown. Linear: a '{' that cannot enclose a later hit is dropped for good,
 * each '{' is matched and parsed at most once, and total work is budgeted
 * (the same algorithm as src/parse.ts).
 */
export function objectsWithKey(text, key, { limit = Infinity, resolveRefs = true } = {}) {
  const rows = resolveRefs ? flightRows(text) : null;
  const needle = `"${key}"`;
  const out = [];
  const braces = [];
  for (let p = text.indexOf('{'); p !== -1; p = text.indexOf('{', p + 1)) braces.push(p);
  const prev = Int32Array.from(braces, (_, k) => k);
  const live = (k) => {
    let r = k;
    while (r >= 0 && prev[r] !== r) r = prev[r];
    while (k > r) {
      const next = prev[k];
      prev[k] = r;
      k = next;
    }
    return r;
  };
  const UNKNOWN = -2;
  const ends = new Int32Array(braces.length).fill(UNKNOWN);
  const parsed = new Array(braces.length);
  const taken = new Uint8Array(braces.length);
  let budget = Math.max(SCAN_BUDGET_FACTOR * text.length, MIN_SCAN_BUDGET);
  let below = 0;
  let from = 0;
  scan: while (out.length < limit) {
    const hit = text.indexOf(needle, from);
    if (hit === -1) break;
    from = hit + needle.length;
    while (below < braces.length && braces[below] <= hit) below++;
    let tried = 0;
    for (let k = live(below - 1); k >= 0; k = live(k - 1)) {
      const i = braces[k];
      if (hit - i >= MAX_LOOKBACK) break;
      let end = ends[k];
      if (end === UNKNOWN) {
        end = matchBalanced(text, i);
        budget -= (end === -1 ? text.length : end) - i;
        if (budget < 0) break scan;
        ends[k] = end;
      }
      if (end === -1 || end <= hit) {
        prev[k] = k - 1;
        continue;
      }
      if (++tried > MAX_CANDIDATES_PER_HIT) break;
      let obj = parsed[k];
      if (obj === undefined) {
        budget -= end - i;
        if (budget < 0) break scan;
        try { obj = JSON.parse(text.slice(i, end)); } catch { obj = null; }
        parsed[k] = obj;
      }
      if (!obj || typeof obj !== 'object' || !(key in obj)) continue;
      if (!taken[k]) {
        taken[k] = 1;
        out.push(rows ? resolve(obj, rows) : obj);
      }
      break;
    }
  }
  return out;
}

/** Convenience: pull records straight out of raw HTML. */
export function recordsFromHtml(html, key, opts) {
  return objectsWithKey(flightText(html), key, opts);
}

// ---------------------------------------------------------------------------
// CLI:  node rsc.mjs <key> [--limit N] [--dedupe <field>] [--raw]  < page.html
// Reads an Angi HTML page on stdin, writes a JSON array of matching records to
// stdout. `--dedupe id` is almost always wanted: a search page emits each
// provider twice (once for the sponsored slot, once for the list).
// ---------------------------------------------------------------------------
if (import.meta.url === `file://${process.argv[1]}`) {
  const argv = process.argv.slice(2);
  const key = argv.find((a) => !a.startsWith('--'));
  if (!key) {
    console.error('usage: node rsc.mjs <key> [--limit N] [--dedupe <field>] [--raw] < page.html');
    process.exit(1);
  }
  const flag = (name) => {
    const i = argv.indexOf(name);
    return i === -1 ? undefined : argv[i + 1];
  };
  const limit = flag('--limit') ? Number(flag('--limit')) : Infinity;
  const dedupe = flag('--dedupe');
  const resolveRefs = !argv.includes('--raw');

  // `… | jq length` or `… | head` closes stdout early; without this the write
  // below throws an unhandled EPIPE and dumps a stack trace over the results.
  process.stdout.on('error', (err) => {
    if (err && err.code === 'EPIPE') process.exit(0);
    throw err;
  });

  let html = '';
  process.stdin.setEncoding('utf8');
  for await (const chunk of process.stdin) html += chunk;

  let recs = objectsWithKey(flightText(html), key, { limit, resolveRefs });
  if (dedupe) recs = [...new Map(recs.map((r) => [r[dedupe], r])).values()];
  process.stdout.write(JSON.stringify(recs, null, 2) + '\n');
}
