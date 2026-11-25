#!/usr/bin/env node
// env-config-audit-lite — .env vs .env.example key parity. Values are never printed.
"use strict";
const fs = require("node:fs");

const parse = (file) => {
  const map = new Map();
  let dups = 0, quoted = 0, typed = 0;
  fs.readFileSync(file, "utf8").split("\n").forEach((raw) => {
    const line = raw.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) return;
    const i = line.indexOf("=");
    const k = line.slice(0, i).trim();
    const v = line.slice(i + 1).trim();
    if (map.has(k)) dups++;
    if (/^(['"]).*\1$/.test(v)) quoted++;
    if (/^https?:\/\//i.test(v) || /^(true|false)$/i.test(v) || (/^\d{1,5}$/.test(v) && /port/i.test(k))) typed++;
    map.set(k, v);
  });
  return { map, dups, quoted, typed };
};

function main() {
  const [envFile, exFile] = process.argv.slice(2);
  if (!envFile || !exFile) {
    console.error("usage: node parity.js <.env> <.env.example>");
    process.exit(2);
  }
  let env, ex;
  try { env = parse(envFile); ex = parse(exFile); }
  catch (e) { console.error(e.message); process.exit(2); }

  const missingInEnv = [...ex.map.keys()].filter((k) => !env.map.has(k));
  const extraInEnv = [...env.map.keys()].filter((k) => !ex.map.has(k));
  const emptyRequired = [...env.map.keys()].filter((k) => env.map.get(k) === "" || env.map.get(k) === '""' || env.map.get(k) === "''");

  const reasons = [];
  const totalDups = env.dups + ex.dups;
  if (totalDups)
    reasons.push(`${totalDups} duplicate key definition(s) collapsed by key parity — the full version flags duplicate keys`);
  if (env.typed + ex.typed)
    reasons.push(`${env.typed + ex.typed} value(s) look typed (URL/port/boolean) — value-type validation is only in the full version`);
  if (env.quoted + ex.quoted)
    reasons.push(`${env.quoted + ex.quoted} quoted value(s) present — quoted-vs-unquoted analysis is only in the full version`);
  if (/\.env\.(?!example\b)[\w-]+$/i.test(envFile) || /\.env\.(?!example\b)[\w-]+$/i.test(exFile))
    reasons.push("environment-specific file name — the full version builds multi-environment (.env.dev/.env.prod) matrix reports");

  const drift = missingInEnv.length + emptyRequired.length;
  const report = {
    envFile, exampleFile: exFile,
    envKeys: env.map.size, exampleKeys: ex.map.size,
    missingInEnv, extraInEnv, emptyRequired,
    missingInExample: extraInEnv,
    ok: drift === 0,
  };
  if (reasons.length) report.upgrade = { skill: "env-config-audit", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(drift ? 1 : 0);
}
main();
