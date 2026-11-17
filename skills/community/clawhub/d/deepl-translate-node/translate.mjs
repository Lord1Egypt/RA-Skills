#!/usr/bin/env node
/**
 * Translate text via the DeepL API (Free tier by default, Pro via DEEPL_API_HOST). Cross-platform (Node 18+).
 *
 * Reads the auth key from the DEEPL_API_KEY environment variable (never hardcode).
 * Prints ONLY the translated text on stdout; on failure prints a line starting with
 * "ERROR:" to stderr and exits non-zero. Newlines / paragraphs are preserved.
 * Always terminates: the request is capped at 60s, so an endpoint that connects and
 * then never answers fails loudly instead of hanging the caller forever.
 *
 * Usage:
 *   node translate.mjs --target ZH --text "Hello world"
 *   node translate.mjs --target EN-US --source JA --text "持分会社"
 *   node translate.mjs --target ZH --glossary "API=接口;token=令牌" --text "..."
 *
 * Flags: --text/-t (required) · --target (required) · --source (optional,
 *        auto-detect if omitted) · --glossary "a=b;c=d" (optional; a literal,
 *        case-sensitive replace of each pair over the returned text).
 * For DeepL Pro, set DEEPL_API_HOST=api.deepl.com (default is api-free.deepl.com).
 */

const ENDPOINT = `https://${process.env.DEEPL_API_HOST || "api-free.deepl.com"}/v2/translate`;

function fail(msg) {
  // stderr, not stdout: stdout carries the translation and nothing else, so a caller doing
  // `t=$(node translate.mjs ...)` cannot end up with "ERROR: ..." as the translated text.
  console.error("ERROR: " + msg);
  process.exitCode = 1;
}

const VALUE_FLAGS = new Set([
  "--text", "-t", "--target", "--target-lang", "--source", "--source-lang", "--glossary",
]);
const FLAG_LIST = "--text/-t, --target/--target-lang, --source/--source-lang, --glossary";

// Every flag takes a value, so anything unrecognised is a mistake worth naming. Dropping it
// quietly turned a typo into "No text provided." — an error message pointing somewhere else.
function parseArgs(argv) {
  const opt = {};
  for (let i = 0; i < argv.length; i++) {
    let a = argv[i];
    let value;
    const eq = a.indexOf("=");
    if (a.startsWith("-") && eq > 0) {
      // `--flag=value` is the form that can carry a value starting with `--`; only the
      // space-separated form gets the "that looks like the next flag" guard.
      value = a.slice(eq + 1);
      a = a.slice(0, eq);
    } else {
      value = argv[++i];
      if (value !== undefined && value.startsWith("--")) { fail(`${a} needs a value`); return null; }
    }
    if (!VALUE_FLAGS.has(a)) {
      fail(a.startsWith("-") ? `unknown option ${a} (flags: ${FLAG_LIST})` : `unexpected argument "${a}"`);
      return null;
    }
    if (value === undefined) { fail(`${a} needs a value`); return null; }
    if (a === "--text" || a === "-t") opt.text = value;
    else if (a.startsWith("--target")) opt.target = value;
    else if (a.startsWith("--source")) opt.source = value;
    else opt.glossary = value;
  }
  return opt;
}

async function main() {
  const opt = parseArgs(process.argv.slice(2));
  if (!opt) return;

  const key = process.env.DEEPL_API_KEY;
  if (!key || !key.trim()) {
    return fail('DEEPL_API_KEY is not set. Set it first, e.g.  export DEEPL_API_KEY="your-key"  (PowerShell: $env:DEEPL_API_KEY="your-key"; persistent on Windows: setx DEEPL_API_KEY "your-key").');
  }
  if (!opt.target) return fail("--target <lang> is required (e.g. ZH, EN-US, JA).");
  // Falsy, not just null: an empty --text has nothing to translate and would still spend a call.
  if (!opt.text) return fail('No text provided. Use --text "..." (the whole string, newlines allowed).');

  const body = { text: [opt.text], target_lang: opt.target };
  if (opt.source) body.source_lang = opt.source;

  let resp;
  try {
    resp = await fetch(ENDPOINT, {
      method: "POST",
      headers: { Authorization: "DeepL-Auth-Key " + key, "Content-Type": "application/json" },
      body: JSON.stringify(body),
      // fetch has no default timeout: a connection that is accepted and then never answered
      // (a throttled or blackholed endpoint, a captive portal, a stalled proxy) leaves this
      // hanging forever with no output and no exit — the caller waits until it is killed.
      signal: AbortSignal.timeout(60_000),
    });
  } catch (e) {
    if (e.name === "TimeoutError")
      return fail("DeepL did not respond within 60s. The endpoint may be unreachable or throttled from this network; check connectivity (and DEEPL_API_HOST if you are on Pro).");
    return fail("DeepL request failed: " + e.message);
  }

  if (!resp.ok) {
    if (resp.status === 403) return fail("403 Forbidden — bad or missing DEEPL_API_KEY, or the key lacks the permission scope for this endpoint.");
    if (resp.status === 456) return fail("456 — DeepL usage limit reached (character quota for the billing period, a Cost Control or key-level limit, or the number of glossaries the plan allows). Read the details from the DeepL console.");
    // The reason lives in the body, not the status: a bad language code answers 400 with
    // {"message":"Bad request. Reason: Value for 'target_lang' not supported."} Truncating
    // keeps a stray HTML error page from burying the ERROR: line.
    const detail = await resp.text().catch(() => "");
    const trimmed = detail.trim().slice(0, 300);
    return fail("DeepL request failed: HTTP " + resp.status + (trimmed ? " — " + trimmed : ""));
  }

  let data;
  try {
    data = await resp.json();
  } catch (e) {
    // A body that starts and then stalls trips the same AbortSignal as a connection that
    // never answers, but surfaces here rather than at the fetch. Name it for what it is
    // instead of blaming DeepL's JSON.
    if (e.name === "TimeoutError" || /aborted|timeout/i.test(e.message))
      return fail("DeepL started replying but the response never finished within 60s. Treat it as a network problem, not a bad key or bad input.");
    return fail("Invalid JSON from DeepL: " + e.message);
  }
  let result = data && data.translations && data.translations[0] && data.translations[0].text;
  if (result == null) return fail("DeepL returned no translation.");

  // Optional exact-match glossary post-processing (replace ALL occurrences).
  if (opt.glossary) {
    for (const pair of opt.glossary.split(";")) {
      if (!pair.trim()) continue;
      const m = pair.match(/^(.*?)=(.*)$/);
      if (!m) {
        // stderr keeps stdout pure, and saying so beats a pair that quietly does nothing —
        // `term:translation` is an easy typo and the output still looks like a translation.
        console.error(`WARNING: glossary pair "${pair.trim()}" has no "=" and was skipped.`);
        continue;
      }
      const from = m[1].trim();
      const to = m[2].trim();
      if (from) result = result.replaceAll(from, () => to);
    }
  }

  process.stdout.write(result + "\n");
}

main();
