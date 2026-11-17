#!/usr/bin/env node
// ClawSearch Ultra — Nyheds-overvågning (unik feature: diff + advarsler)
// Kører søgning, gemmer resultater, og viser KUN nye resultater ved næste kørsel.
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SEARCH = path.join(__dirname, "search.mjs");
const STATE_DIR = path.join(os.tmpdir(), "clawsearch-watch");
fs.mkdirSync(STATE_DIR, { recursive: true });

function usage() {
  console.error(`ClawSearch Ultra — nyheds-overvågning

Brug:
  watch.mjs "emne" [--tag navn] [--notify telegram|slack]

Eksempler:
  watch.mjs "BTC pris" --tag btc
  watch.mjs "Vantage spreads" --tag vantage --notify telegram

Første kørsel gemmer baseline; næste kørsel viser kun NYE resultater.
`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0) usage();

const query = args[0];
const tag = args.includes("--tag") ? args[args.indexOf("--tag") + 1] : query.replace(/\W+/g, "_").slice(0, 40);
const notify = args.includes("--notify") ? args[args.indexOf("--notify") + 1] : null;
const stateFile = path.join(STATE_DIR, `${tag}.json`);

let raw;
try {
  raw = execFileSync("node", [SEARCH, query, "--json"], { encoding: "utf8", timeout: 45000 });
} catch (e) {
  console.error(`⚠️ Søgning fejlede: ${e.stderr?.split("\n")[0] || e.message}`);
  process.exit(1);
}

let data;
try { data = JSON.parse(raw); } catch { console.error("⚠️ Kunne ikke fortolke resultat."); process.exit(1); }

const results = data.results || data.federated?.results || [];
const current = new Set(results.map(r => r.url));

let previous = new Set();
if (fs.existsSync(stateFile)) {
  try { previous = new Set(JSON.parse(fs.readFileSync(stateFile, "utf8"))); } catch {}
}

const fresh = results.filter(r => !previous.has(r.url));

// Gem baseline
fs.writeFileSync(stateFile, JSON.stringify([...current], null, 2));

if (fresh.length === 0) {
  console.log(`👀 "${query}" — ingen nye resultater siden sidst (${results.length} kendte).`);
} else {
  console.log(`🆕 ${fresh.length} NYE resultater for "${query}":\n`);
  fresh.slice(0, 10).forEach((r, i) => {
    console.log(`${i + 1}. ${r.title}`);
    console.log(`   🔗 ${r.url}`);
    console.log("");
  });
  if (notify === "telegram") {
    console.log(`📨 [telegram-besked ville blive sendt her: ${fresh.length} nye om "${query}"]`);
  } else if (notify === "slack") {
    console.log(`📨 [slack-webhook ville blive kaldt her]`);
  }
}
