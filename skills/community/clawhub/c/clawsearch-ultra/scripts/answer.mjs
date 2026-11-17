#!/usr/bin/env node
// ClawSearch Ultra — Svar-med-kilder (unik feature: answer-first)
// Wrapper om search.mjs: kører søgning, viser top-svar + kilder i ét kald.
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SEARCH = path.join(__dirname, "search.mjs");

function usage() {
  console.error(`ClawSearch Ultra — answer-first søgning

Brug:
  answer.mjs "query" [--lang da] [--json]

Eksempler:
  answer.mjs "Hvad er DRT-strategien?"
  answer.mjs "renten danmark 2026" --lang da --json
`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0) usage();

const query = args[0];
const lang = args.includes("--lang") ? args[args.indexOf("--lang") + 1] : null;
const asJson = args.includes("--json");

let raw;
try {
  const searchArgs = [SEARCH, query, "--json"];
  if (lang) searchArgs.push("--lang", lang);
  raw = execFileSync("node", searchArgs, { encoding: "utf8", timeout: 45000 });
} catch (e) {
  console.error(`⚠️ Søgning fejlede: ${e.stderr?.split("\n")[0] || e.message}`);
  console.error("💡 Tip: Sæt TAVILY_API_KEY for stabil baseline (gratis tier) eller prøv igen om lidt.");
  process.exit(1);
}

let data;
try {
  data = JSON.parse(raw);
} catch {
  console.error("⚠️ Kunne ikke fortolke søgeresultat.");
  process.exit(1);
}

const results = data.results || data.federated?.results || [];
const top = results.slice(0, 5);

if (asJson) {
  console.log(JSON.stringify({
    query,
    answer: top.map(r => r.title).join(" | ") || "Ingen resultater",
    sources: top.map(r => ({ title: r.title, url: r.url })),
    provider: data.selectedProvider || data.provider || "unknown",
  }, null, 2));
} else {
  console.log(`🔎 Svar på: "${query}"\n`);
  top.forEach((r, i) => {
    console.log(`${i + 1}. ${r.title}`);
    if (r.snippet) console.log(`   ${String(r.snippet).slice(0, 140)}`);
    console.log(`   🔗 ${r.url}`);
    console.log("");
  });
  if (top.length === 0) console.log("Ingen resultater fundet.");
  console.log(`(Kilde-motor: ${data.selectedProvider || data.provider || "ukendt"})`);
}
