#!/usr/bin/env node
/**
 * Translate text via the DeepL API (Free tier by default, Pro via DEEPL_API_HOST). Cross-platform (Node 18+).
 *
 * Reads the auth key from the DEEPL_API_KEY environment variable (never hardcode).
 * Prints ONLY the translated text on success; prints a line starting with
 * "ERROR:" and exits non-zero on failure. Newlines / paragraphs are preserved.
 *
 * Usage:
 *   node translate.mjs --target ZH --text "Hello world"
 *   node translate.mjs --target EN-US --source JA --text "持分会社"
 *   node translate.mjs --target ZH --glossary "API=接口;token=令牌" --text "..."
 *
 * Flags: --text/-t (required) · --target (required) · --source (optional,
 *        auto-detect if omitted) · --glossary "a=b;c=d" (optional exact-match).
 * For DeepL Pro, set DEEPL_API_HOST=api.deepl.com (default is api-free.deepl.com).
 */

const ENDPOINT = `https://${process.env.DEEPL_API_HOST || "api-free.deepl.com"}/v2/translate`;

function fail(msg) {
  console.log("ERROR: " + msg);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const opt = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--text" || a === "-t") opt.text = argv[++i];
    else if (a === "--target" || a === "--target-lang") opt.target = argv[++i];
    else if (a === "--source" || a === "--source-lang") opt.source = argv[++i];
    else if (a === "--glossary") opt.glossary = argv[++i];
  }
  return opt;
}

async function main() {
  const opt = parseArgs(process.argv.slice(2));

  const key = process.env.DEEPL_API_KEY;
  if (!key || !key.trim()) {
    return fail('DEEPL_API_KEY is not set. Set it first, e.g.  export DEEPL_API_KEY="your-key"  (PowerShell: $env:DEEPL_API_KEY="your-key"; persistent on Windows: setx DEEPL_API_KEY "your-key").');
  }
  if (!opt.target) return fail("--target <lang> is required (e.g. ZH, EN-US, JA).");
  if (opt.text == null) return fail('No text provided. Use --text "..." (the whole string, newlines allowed).');

  const body = { text: [opt.text], target_lang: opt.target };
  if (opt.source) body.source_lang = opt.source;

  let resp;
  try {
    resp = await fetch(ENDPOINT, {
      method: "POST",
      headers: { Authorization: "DeepL-Auth-Key " + key, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (e) {
    return fail("DeepL request failed: " + e.message);
  }

  if (!resp.ok) {
    if (resp.status === 403) return fail("403 Forbidden — bad or missing DEEPL_API_KEY.");
    if (resp.status === 456) return fail("456 — DeepL Free quota exhausted for this billing period.");
    return fail("DeepL request failed: HTTP " + resp.status);
  }

  let data;
  try {
    data = await resp.json();
  } catch (e) {
    return fail("Invalid JSON from DeepL: " + e.message);
  }
  let result = data && data.translations && data.translations[0] && data.translations[0].text;
  if (result == null) return fail("DeepL returned no translation.");

  // Optional exact-match glossary post-processing (replace ALL occurrences).
  if (opt.glossary) {
    for (const pair of opt.glossary.split(";")) {
      const m = pair.match(/^(.*?)=(.*)$/);
      if (m) {
        const from = m[1].trim();
        const to = m[2].trim();
        if (from) result = result.replaceAll(from, to);
      }
    }
  }

  process.stdout.write(result + "\n");
}

main();
